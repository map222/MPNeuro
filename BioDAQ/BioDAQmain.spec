# -*- mode: python -*-
a = Analysis(['BioDAQmain.py'],
             pathex=['C:\\Users\\palmiteradmin\\Documents\\GitHub\\MPNeuro\\BioDAQ'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='BioDAQmain.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='BioDAQmain')
