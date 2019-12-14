# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['ui_main.py',
'/home/utry/PycharmProjects/qtUi/src/usher/manager/manager.py'
],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ui_main',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
