# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew 
from charset_normalizer import md__mypyc
from kivymd import hooks_path as kivymd_hooks_path

block_cipher = None

def get_mediapipe_path():
    import mediapipe
    mediapipe_path = mediapipe.__path__[0]
    return mediapipe_path

a = Analysis(
    ['launch.py'],
    pathex=['E:\\Documents\\Github\\FIT_CS_Thesis_Kivy\\app\\'],
    binaries=[],
    datas=[
        ('*kv', '.'), 
        ('*py', '.'), 
        ('Unified_Model_01.h5', '.'), 
        ('Unfiied_Model_03_Beginner_Best.h5', '.'), 
        ('Medium_Model_Simple_02.h5', '.'), 
        ('font/zh-cn.ttf', 'font'), 
        ('materials/',  'materials'),
        ],
    hiddenimports=["charset_normalizer.md__mypyc"],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

mediapipe_tree = Tree(get_mediapipe_path(), prefix='mediapipe', excludes=["*.pyc"])
a.datas += mediapipe_tree
a.binaries = filter(lambda x: 'mediapipe' not in x[0], a.binaries)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YogaLauncher',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
