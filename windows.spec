# -*- mode: python -*-

from kivy.tools.packaging.pyinstaller_hooks import install_hooks
import kivy.core.video
import os
install_hooks(globals())

gst_plugin_path = "C:\\Users\\Davide Depau\\Desktop\\Kivy\\gstreamer"

def Datafiles(*filenames, **kw):
    def datafile(path, strip_path=True):
        parts = path.split('/')
        path = name = os.path.join(*parts)
        if strip_path:
            name = os.path.basename(path)
        return name, path, 'DATA'

    strip_path = kw.get('strip_path', True)
    return TOC(
        datafile(filename, strip_path=strip_path)
        for filename in filenames
        if os.path.isfile(filename))

datafiles = Datafiles("presentation.kv")

a = Analysis(['main.py'],
             pathex=['a:\\'],
             hiddenimports=[],
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Presentazione su Arduino di Davide Depau.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True)#, version='version.txt')#, icon='icon.ico' )
coll = COLLECT(exe,
			   Tree('A:\\libs\\'),
			   Tree('A:\\pygments\\'),
			   Tree(gst_plugin_path),
			   Tree(os.path.join(gst_plugin_path, 'bin')),
			   Tree([f for f in os.environ.get('KIVY_SDL2_PATH', '').split(';') if 'bin' in f][0]),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='Versione per Windows')
