# -*- coding: utf-8 -*-

def mangle(s):
    debug_this = False
    s1 = s.split()[0::2]
    s2 = s.split()[1::3]
    if debug_this:
        print s1
        print s2
    return " ".join(s1+s2)
 
original_string = "I am learning how to use (Pdb)"
mangled_string = mangle(original_string)
print mangled_string