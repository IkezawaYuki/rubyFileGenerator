# -*- mode: python -*-

block_cipher = None


a = Analysis(['entrance.py'],
             pathex=['/Users/ikezaway/PycharmProjects/rubyFileGenerator'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += [('entrance_image.ico','/Users/ikezaway/PycharmProjects/rubyFileGenerator/entrance_image.ico','DATA')]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='entrance',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='/Users/ikezaway/PycharmProjects/rubyFileGenerator/entrance_image.ico')
