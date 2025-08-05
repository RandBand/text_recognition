#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR项目通用打包脚本
支持macOS和Windows平台的自动检测和优化打包
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def check_system_tools():
    """检查系统工具可用性"""
    tools = {}
    
    # 检查UPX
    try:
        result = subprocess.run(['upx', '--version'], 
                              capture_output=True, text=True)
        tools['upx'] = result.returncode == 0
    except FileNotFoundError:
        tools['upx'] = False
    
    # 检查strip
    try:
        result = subprocess.run(['strip', '--version'], 
                              capture_output=True, text=True)
        tools['strip'] = result.returncode == 0
    except FileNotFoundError:
        tools['strip'] = False
    
    return tools

def create_universal_spec():
    """创建通用优化的spec文件"""
    tools = check_system_tools()
    is_windows = platform.system() == 'Windows'
    upx_available = tools.get('upx', False) and not is_windows
    strip_available = tools.get('strip', False) and not is_windows
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 系统检测
import platform
import subprocess

def check_system_tools():
    tools = {{}}
    try:
        result = subprocess.run(['upx', '--version'], 
                              capture_output=True, text=True)
        tools['upx'] = result.returncode == 0
    except FileNotFoundError:
        tools['upx'] = False
    
    try:
        result = subprocess.run(['strip', '--version'], 
                              capture_output=True, text=True)
        tools['strip'] = result.returncode == 0
    except FileNotFoundError:
        tools['strip'] = False
    
    return tools

# 系统检测
is_windows = platform.system() == 'Windows'
tools = check_system_tools()
upx_available = tools.get('upx', False) and not is_windows
strip_available = tools.get('strip', False) and not is_windows

# 基础模块列表
base_hiddenimports = [
    'cv2',
    'numpy',
    'numpy.core',
    'numpy.core._methods',
    'numpy.core._multiarray_umath',
    'numpy.core._dtype_ctypes',
    'numpy.core._internal',
    'numpy.lib.format',
    'numpy.lib._datasource',
    'numpy.lib._iotools',
    'numpy.lib._version',
    'numpy.lib.utils',
    'numpy.random',
    'numpy.random._pickle',
    'numpy.random.mtrand',
    'numpy.random.bit_generator',
    'secrets',  # 显式添加secrets模块，解决Windows打包问题
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

# Windows特定配置
if is_windows:
    # Windows下需要额外的模块
    windows_extra_imports = [
        'secrets',
        'numpy.random._pickle',
        'numpy.random.mtrand',
        'numpy.random.bit_generator',
        'numpy.random._common',
        'numpy.random._bounded_integers',
        'numpy.random._mt19937',
        'numpy.random._pcg64',
        'numpy.random._philox',
        'numpy.random._sfc64',
        'numpy.random._generator'
    ]
    hiddenimports = base_hiddenimports + windows_extra_imports
else:
    hiddenimports = base_hiddenimports

# 包含所有必要的资源文件
datas = [
    ('../../models/det.onnx', 'models'),
    ('../../models/rec.onnx', 'models'),
    ('../../models/ppocr_keys_v1.txt', 'models'),
    ('../../assets/fonts/simfang.ttf', 'assets/fonts'),
    ('../../requirements.txt', '.'),
]



# 排除不必要的模块
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
    hooksconfig={{}},
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
    strip={strip_available},  # 根据系统可用性决定
    upx={upx_available},      # 根据系统可用性决定
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    # 确保build/configs目录存在
    os.makedirs('build/configs', exist_ok=True)
    
    # 写入通用优化的spec文件
    with open('build/configs/ocr_server_universal.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ 已创建通用优化的spec配置文件")
    return tools

def create_package_structure():
    """创建完整的包结构"""
    package_dir = "dist/ocr_server_package"
    
    # 清理之前的包
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    # 创建包目录结构
    os.makedirs(package_dir, exist_ok=True)
    os.makedirs(f"{package_dir}/models", exist_ok=True)
    os.makedirs(f"{package_dir}/assets/fonts", exist_ok=True)
    
    # 复制可执行文件
    exe_name = 'ocr_server.exe' if platform.system() == 'Windows' else 'ocr_server'
    exe_path = f"dist/{exe_name}"
    
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, f"{package_dir}/{exe_name}")
        print(f"✅ 已复制可执行文件: {exe_name}")
    else:
        print(f"❌ 可执行文件未找到: {exe_path}")
        return False
    
    # 复制模型文件
    model_files = [
        ('models/det.onnx', f"{package_dir}/models/det.onnx"),
        ('models/rec.onnx', f"{package_dir}/models/rec.onnx"),
        ('models/ppocr_keys_v1.txt', f"{package_dir}/models/ppocr_keys_v1.txt"),
    ]
    
    for src, dst in model_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ 已复制模型文件: {src}")
        else:
            print(f"⚠️  模型文件未找到: {src}")
    
    # 复制字体文件
    font_files = [
        ('assets/fonts/simfang.ttf', f"{package_dir}/assets/fonts/simfang.ttf"),
    ]
    
    for src, dst in font_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ 已复制字体文件: {src}")
        else:
            print(f"⚠️  字体文件未找到: {src}")
    
    # 复制图片文件
    if os.path.exists('assets/images'):
        shutil.copytree('assets/images', f"{package_dir}/assets/images", dirs_exist_ok=True)
        print(f"✅ 已复制图片文件")
    
    # 复制文档文件
    doc_files = [
        ('docs/README.md', f"{package_dir}/docs/README.md"),
        ('docs/USAGE_GUIDE.md', f"{package_dir}/docs/USAGE_GUIDE.md"),
        ('requirements.txt', f"{package_dir}/requirements.txt"),
    ]
    
    for src, dst in doc_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ 已复制文档文件: {src}")
        else:
            print(f"⚠️  文档文件未找到: {src}")
    
    # 创建启动脚本
    create_startup_scripts(package_dir, exe_name)
    
    return True

def create_startup_scripts(package_dir, exe_name):
    """创建启动脚本"""
    # Windows批处理文件
    if platform.system() == 'Windows':
        bat_content = f'''@echo off
echo OCR服务器启动中...
echo 默认端口: 5000
echo 访问地址: http://localhost:5000
echo.
echo 按 Ctrl+C 停止服务器
echo.
{exe_name} --help
echo.
echo 启动服务器...
{exe_name}
pause
'''
        with open(f"{package_dir}/start_server.bat", 'w', encoding='utf-8') as f:
            f.write(bat_content)
        print(f"✅ 已创建Windows启动脚本: start_server.bat")
    
    # Unix/Linux/macOS shell脚本
    shell_content = f'''#!/bin/bash
echo "OCR服务器启动中..."
echo "默认端口: 5000"
echo "访问地址: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""
./{exe_name} --help
echo ""
echo "启动服务器..."
./{exe_name}
'''
    with open(f"{package_dir}/start_server.sh", 'w', encoding='utf-8') as f:
        f.write(shell_content)
    
    # 设置执行权限
    if platform.system() != 'Windows':
        os.chmod(f"{package_dir}/start_server.sh", 0o755)
    
    print(f"✅ 已创建Unix启动脚本: start_server.sh")

def main():
    """主构建流程"""
    print("🚀 OCR项目通用打包工具")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists('run_server.py'):
        print("❌ 错误：请在项目根目录运行此脚本")
        return 1
    
    # 系统信息
    print(f"📋 系统信息:")
    print(f"   操作系统: {platform.system()} {platform.release()}")
    print(f"   Python版本: {sys.version}")
    print(f"   架构: {platform.machine()}")
    
    # 检查工具可用性
    print(f"\n🔧 工具检查:")
    tools = create_universal_spec()
    
    print(f"   UPX压缩工具: {'✅ 可用' if tools.get('upx', False) else '❌ 不可用'}")
    print(f"   Strip工具: {'✅ 可用' if tools.get('strip', False) else '❌ 不可用'}")
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller已安装: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，请运行: pip install pyinstaller")
        return 1
    
    # 检查numpy
    try:
        import numpy
        print(f"✅ NumPy已安装: {numpy.__version__}")
    except ImportError:
        print("❌ NumPy未安装，请运行: pip install numpy")
        return 1
    
    # 清理之前的构建
    print(f"\n🧹 清理之前的构建...")
    if os.path.exists('build/build_universal'):
        shutil.rmtree('build/build_universal')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # 开始构建
    print(f"\n🔨 开始构建...")
    try:
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            'build/configs/ocr_server_universal.spec',
            '--distpath', 'dist',
            '--workpath', 'build/build_universal',
            '--clean'
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=False)
        
        print(f"\n✅ 构建成功!")
        
        # 创建完整的包结构
        print(f"\n📦 创建完整包结构...")
        if create_package_structure():
            print(f"\n✅ 完整包创建成功!")
            
            # 显示包信息
            package_dir = "dist/ocr_server_package"
            if os.path.exists(package_dir):
                total_size = 0
                file_count = 0
                for root, dirs, files in os.walk(package_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                        file_count += 1
                
                size_mb = total_size / (1024 * 1024)
                print(f"📦 包位置: {package_dir}")
                print(f"📏 包大小: {size_mb:.1f} MB")
                print(f"📄 文件数量: {file_count}")
                
                # 显示包内容
                print(f"\n📋 包内容:")
                for root, dirs, files in os.walk(package_dir):
                    level = root.replace(package_dir, '').count(os.sep)
                    indent = ' ' * 2 * level
                    print(f"{indent}{os.path.basename(root)}/")
                    subindent = ' ' * 2 * (level + 1)
                    for file in files:
                        print(f"{subindent}{file}")
            else:
                print(f"❌ 包目录未找到: {package_dir}")
        else:
            print(f"❌ 包创建失败")
            return 1
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 构建失败: {e}")
        print(f"请检查错误信息并重试")
        return 1
    except Exception as e:
        print(f"\n❌ 未知错误: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main()) 