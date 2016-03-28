from __future__ import division
import tkinter as tk
from tkinter.filedialog import askopenfilename
import scipy.misc as sm
import pdb
from PIL import ImageTk, Image
from PIL import ImageEnhance
import math
import exiftool
import numpy as np
import os
import pandas as pd

def load_jpg( basename = 'FLIR0288'):
    # load the png
    jpg = Image.open(basename + '.jpg')
    jpg = jpg.resize((640,480), Image.ANTIALIAS)
    jpg2 = jpg.convert('L')
    # enhance contrast
    enhancer = ImageEnhance.Contrast(jpg2)
    jpg2 = enhancer.enhance(2.0)
    tkjpg = ImageTk.PhotoImage( jpg2)

    return tkjpg

def make_png(basename = 'FLIR0288'):
    et = exiftool.ExifTool()
    et.start()
    
    # convert jpeg to png
    cur_jpeg = basename + '.jpg'
    byte_image = et.execute( b'-b', b'-RawThermalImage', cur_jpeg.encode('utf-8'))
    with open(cur_jpeg[:-4] + '.png', 'wb') as png_file:
        png_file.write(byte_image)
        
    # swap endian
    png_image = sm.imread(basename + '.png')
    png_image = png_image.astype('int16')
    png_image.byteswap('<')
    sm.imsave(basename + '.png', png_image)
    return png_image

def make_temp_image(basename, png):
    # load exif data
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(basename + '.jpg')
    planck_r1 = metadata[u'APP1:PlanckR1']
    planck_r2 = metadata[u'APP1:PlanckR2']
    planck_b = metadata[u'APP1:PlanckB']
    planck_o = metadata[u'APP1:PlanckO']
    planck_f = metadata[u'APP1:PlanckF']

    # sometimes there are 0 values in a row; fix them by setting to min
    if png.min() < -planck_o: # problem with png file
        temp_min = png[png > 10].min()
        png[png <= 10] = temp_min

    temp_func = np.vectorize(lambda x: calc_temp(x, planck_r1, planck_r2, planck_b, planck_o, planck_f))
    return temp_func(png)

def calc_temp(pixel, planck_r1, planck_r2, planck_b, planck_o, planck_f):
    kelvin = 273.15
    return planck_b / math.log(planck_r1 / (planck_r2 * (pixel + planck_o)) + planck_f) - kelvin


class MouseGUI(tk.Frame):
    def __init__(self, parent, tk_jpg):

        #setting up a tkinter canvas with scrollbars
        frame = tk.Frame(parent, bd=2, relief=tk.SUNKEN)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.xscroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        self.xscroll.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.yscroll = tk.Scrollbar(frame)
        self.yscroll.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.canvas = tk.Canvas(frame, bd=0, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set, width = 640, height=480)
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.xscroll.config(command=self.canvas.xview)
        self.yscroll.config(command=self.canvas.yview)
        frame.pack(fill=tk.BOTH,expand=1)

        self.canvas.create_image(0,0,image=tk_jpg,anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        parent.bind("q", self.quit_window)
        parent.bind("<space>", self.next_mouse)
        self.canvas.bind("<Button 1>",self.printcoords)
        
        self.quit = False
    
    def printcoords(self,event):
        #outputting x and y coords to console
        x = math.floor(event.x / 8)
        y = math.floor(event.y / 8)
        print( (flir_file, x,y, temp_image[y][x ] ) )
        img_temps.append([flir_file, temp_image[y][x ] ])

    def quit_window(self,event):
        self.quit = True
        root.destroy()

    def next_mouse(self, event):
        root.destroy()

if __name__ == "__main__":

    all_files = os.listdir('.')
    
    assert 'exiftool.exe' in all_files, 'exiftool.exe must be in the directory'
    jpegs = [x[:-4] for x in all_files if x[-4:] == '.jpg']
    img_temps = []
    for flir_file in jpegs:
        root = tk.Tk()
        tk_jpg = load_jpg(flir_file)
        temp_image = make_png(flir_file)
        temp_image = make_temp_image(flir_file, temp_image) # png is in global namespace, and used by MouseGUI object
        cur_mouse = MouseGUI(root, tk_jpg)
        root.mainloop()
        if cur_mouse.quit:
            break

    img_df = pd.DataFrame(img_temps, columns = ['Image', 'Temperature'])
    img_df.to_csv('tail temps.csv')
