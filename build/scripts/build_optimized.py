#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR项目优化打包脚本
专门针对体积优化，使用多种技术减小包大小
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_optimized_spec():
    """创建优化的spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 只包含必要的模型文件
datas = [
    ('../../models/det.onnx', '.'),
    ('../../models/rec.onnx', '.'),
    ('../../models/ppocr_keys_v1.txt', '.'),
    ('../../assets/fonts/simfang.ttf', '.'),
]

# 精确的隐藏导入，避免不必要的模块
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

# 排除大量不必要的模块
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
'''
    
    with open('build/configs/ocr_server_optimized.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ 创建优化配置文件: build/configs/ocr_server_optimized.spec")

def install_upx():
    """安装UPX压缩工具"""
    print("📦 检查UPX压缩工具...")
    
    # 检查UPX是否已安装
    try:
        subprocess.run(['upx', '--version'], capture_output=True, check=True)
        print("✅ UPX已安装")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  UPX未安装，将跳过二进制压缩")
        return False

def build_optimized():
    """构建优化的可执行文件"""
    print("🔨 开始构建优化版本...")
    
    # 切换到项目根目录
    project_root = os.path.join(os.path.dirname(__file__), '..', '..')
    os.chdir(project_root)
    print(f"📁 切换到项目根目录: {os.getcwd()}")
    
    # 使用优化配置构建
    result = subprocess.run([
        'pyinstaller',
        '--clean',
        '--distpath', 'dist/packages',
        '--workpath', 'build/build_optimized',
        'build/configs/ocr_server_optimized.spec'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 优化构建成功!")
        return True
    else:
        print("❌ 构建失败:")
        print(result.stderr)
        return False

def create_minimal_package():
    """创建最小化分发包"""
    print("📦 创建最小化分发包...")
    
    dist_dir = Path("dist/packages/ocr_minimal")
    dist_dir.mkdir(exist_ok=True)
    
    # 复制可执行文件
    if os.path.exists("dist/packages/ocr_server"):
        shutil.copy2("dist/packages/ocr_server", dist_dir / "ocr_server")
    
    # 只复制必要的模型文件
    essential_files = [
        "models/det.onnx",
        "models/rec.onnx", 
        "models/ppocr_keys_v1.txt",
        "assets/fonts/simfang.ttf"
    ]
    
    for file in essential_files:
        if os.path.exists(file):
            # 创建目标目录
            target_dir = dist_dir / os.path.dirname(file)
            target_dir.mkdir(parents=True, exist_ok=True)
            # 复制文件
            shutil.copy2(file, dist_dir / file)
    
    # 创建启动脚本
    create_minimal_startup_script(dist_dir)
    
    print(f"✅ 最小化分发包创建完成: {dist_dir}")
    return dist_dir

def create_minimal_startup_script(dist_dir):
    """创建最小化启动脚本"""
    if sys.platform.startswith('win'):
        script_content = '''@echo off
echo OCR服务器启动中...
echo 使用示例:
echo   start.bat                    # 使用默认端口8080
echo   start.bat -p 9000           # 使用端口9000
echo   start.bat --port 9000       # 使用端口9000
echo   start.bat -H 0.0.0.0 -p 9000  # 绑定到所有接口的9000端口
echo   start.bat --auto-port       # 自动查找可用端口
echo.
if "%1"=="" (
    ocr_server.exe
) else (
    ocr_server.exe %*
)
'''
        script_path = dist_dir / "start.bat"
    else:
        script_content = '''#!/bin/bash
echo "OCR服务器启动中..."
echo "使用示例:"
echo "  ./start.sh                    # 使用默认端口8080"
echo "  ./start.sh -p 9000           # 使用端口9000"
echo "  ./start.sh --port 9000       # 使用端口9000"
echo "  ./start.sh -H 0.0.0.0 -p 9000  # 绑定到所有接口的9000端口"
echo "  ./start.sh --auto-port       # 自动查找可用端口"
echo "  ./start.sh --help            # 显示帮助信息"
echo ""
if [ $# -eq 0 ]; then
    ./ocr_server
else
    ./ocr_server "$@"
fi
'''
        script_path = dist_dir / "start.sh"
    
    # 先创建文件，再设置权限
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # 在非Windows系统上设置执行权限
    if not sys.platform.startswith('win'):
        os.chmod(script_path, 0o755)

def analyze_size():
    """分析包大小"""
    dist_dir = Path("dist/packages/ocr_minimal")
    if not dist_dir.exists():
        return
    
    print("\n📊 包大小分析:")
    total_size = 0
    
    for file in dist_dir.rglob('*'):
        if file.is_file():
            size = file.stat().st_size
            total_size += size
            print(f"  {file.name}: {size / 1024 / 1024:.2f} MB")
    
    print(f"\n📦 总大小: {total_size / 1024 / 1024:.2f} MB")

def main():
    """主函数"""
    print("🚀 OCR项目优化打包工具")
    print("=" * 50)
    
    try:
        # 1. 安装PyInstaller
        print("📦 安装PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        
        # 2. 检查UPX
        install_upx()
        
        # 3. 创建优化配置
        create_optimized_spec()
        
        # 4. 构建优化版本
        if build_optimized():
            # 5. 创建最小化分发包
            dist_dir = create_minimal_package()
            
            print("\n🎉 优化打包完成!")
            print(f"📁 分发包位置: {dist_dir}")
            
            # 6. 分析包大小
            analyze_size()
            
        else:
            print("❌ 构建失败")
            return 1
            
    except Exception as e:
        print(f"❌ 打包过程中出现错误: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 