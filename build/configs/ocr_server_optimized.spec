# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Only include necessary model files
datas = [
    ('../../models/det.onnx', '.'),
    ('../../models/rec.onnx', '.'),
    ('../../models/ppocr_keys_v1.txt', '.'),
    ('../../assets/fonts/simfang.ttf', '.'),
]

# Precise hidden imports to avoid unnecessary modules
hiddenimports = [
    'cv2',
    'numpy.core._methods',
    'numpy.lib.format',
    'PIL._tkinter_finder',
    'onnxruntime.capi.onnxruntime_pybind11_state',
    'shapely.geometry',
    'pyclipper',
    'http.server',
    'urllib.parse',
    'json',
    'base64',
    'io',
    'threading',
    'time',
    'math',
    'copy',
    'random',
    'argparse',
    'glob'
]

# Exclude unnecessary modules
excludes = [
    'matplotlib', 'scipy', 'pandas', 'jupyter', 'IPython', 'notebook',
    'tornado', 'zmq', 'tkinter', 'PyQt5', 'PySide2', 'wx', 'PyQt4',
    'IPython', 'jupyter_client', 'jupyter_core', 'jupyterlab',
    'notebook', 'qtpy', 'spyder', 'spyder_kernels', 'qtconsole',
    'nbconvert', 'nbformat', 'traitlets', 'ipykernel', 'ipython_genutils',
    'jedi', 'parso', 'pexpect', 'ptyprocess', 'decorator', 'pickleshare',
    'prompt_toolkit', 'wcwidth', 'colorama', 'backcall', 'appnope',
    'setuptools', 'pkg_resources', 'distutils', 'lib2to3', 'test',
    'unittest', 'doctest', 'pdb', 'profile', 'pstats', 'timeit',
    'trace', 'turtle', 'tkinter', 'tcl', 'tk', '_tkinter',
    'PySide', 'PyQt4', 'PyQt5', 'PySide2', 'PySide6', 'PyQt6',
    'wx', 'wxPython', 'wx._core', 'wx._controls', 'wx._gdi',
    'matplotlib', 'matplotlib.backends', 'matplotlib.figure',
    'matplotlib.pyplot', 'matplotlib.axes', 'matplotlib.patches',
    'scipy', 'scipy.spatial', 'scipy.ndimage', 'scipy.signal',
    'pandas', 'pandas.core', 'pandas.io', 'pandas.plotting',
    'numpy.testing', 'numpy.f2py', 'numpy.distutils',
    'PIL.ImageQt', 'PIL.ImageTk', 'PIL.ImageDraw2',
    'cv2.cv', 'cv2.data', 'cv2.misc',
    'shapely.speedups', 'shapely.vectorized',
    'requests', 'urllib3', 'certifi', 'charset_normalizer',
    'idna', 'chardet', 'flask', 'werkzeug', 'jinja2', 'markupsafe',
    'itsdangerous', 'click', 'blinker', 'colorama'
]

a = Analysis(
    ['../../run_server.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ocr_server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # 去除调试信息
    upx=True,    # 使用UPX压缩
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
