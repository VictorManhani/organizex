# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew

block_cipher = None

a = Analysis(['main.py'],
             pathex=['C:\\Users\\User\\Desktop\\Organizex-Photo_Organizer-master'],
             binaries=[],
             datas=[('C:\\Users\\User\\Desktop\\Organizex-Photo_Organizer-master\\img\\blue.png', './img/'), ('C:\\Users\\User\\Desktop\\Organizex-Photo_Organizer-master\\img\\logo.png', './img/')],
             hiddenimports=['win32timezone'],
             hookspath=[],
             runtime_hooks=[],
             excludes=["FixTk", "tcl", "tk", "_tkinter", "tkinter", "Tkinter", "numpy", "scipy", "Qt", "PySide2", "shiboken2"],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='organizex',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)

coll = COLLECT(exe,
               Tree('C:\\Users\\User\\Desktop\\Organizex-Photo_Organizer-master'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               upx=True,
               upx_exclude=[],
               name='main', icon='C:\\Users\\User\\Desktop\\Organizex-Photo_Organizer-master\\img\\logo.ico')
