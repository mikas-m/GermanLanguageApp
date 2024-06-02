# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path
path = os.path.abspath(".")

a = Analysis(
    [("appPC.py")],
    pathex=[path],
    datas=[('appPC.kv', '.'), ('gwords.db', '.')],
    hiddeinport=[],
    hookspath=[kivymd_hooks_path],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
a.datas += [('design\\swiss_scenery.jpg','C:\\Users\\mikas\\PycharmProjects\\germanija\\App\\design\\swiss_scenery.jpg','DATA'), 
('design\\arrow_straight.png','C:\\Users\\mikas\\PycharmProjects\\germanija\\App\\design\\arrow_straight.png','DATA'),
('design\\triskele.png','C:\\Users\\mikas\\PycharmProjects\\germanija\\App\\design\\triskele.png','DATA'),
('design\\DirtyHeadline-x39K.ttf', 'C:\\Users\\mikas\\PycharmProjects\\germanija\\App\\design\\DirtyHeadline-x39K.ttf', 'DATA'),
('design\\myicon.ico', 'C:\\Users\\mikas\\PycharmProjects\\germanija\\App\\design\\myicon.ico', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    debug=False,
    strip=False,
    upx=True,
    name="GermanLanguage",
    console=True,
)
