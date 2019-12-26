# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['ui_main.py'],
             pathex=['/home/utry/PycharmProjects/qtUi/src/usher/main',
             '/home/utry/PycharmProjects/qtUi/',
             '/home/utry/PycharmProjects/qtUi/src/'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          name='ui_main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ui_main')
