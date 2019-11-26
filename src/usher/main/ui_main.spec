# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['ui_main.py',
'/home/utry/PycharmProjects/qtUi/src/usher/manager/manager.py'
],
             pathex=['/home/utry/PycharmProjects/qtUi/src/usher/main'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5', 'PyQt5.QtCore', 'json', 'std_msgs', 'std_msgs.msg',
             'logging.handlers', 'PyQt5.QtWidgets', 'requests', 'tracemalloc', 'rospy', 'roslaunch',
             'cv2'],
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
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
