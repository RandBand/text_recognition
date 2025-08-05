#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地构建脚本 - 用于测试PyInstaller打包过程
支持macOS和Windows平台的本地构建
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def get_platform_info():
    """获取当前平台信息"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "darwin":
        if machine == "arm64":
            return "macos", "arm64"
        else:
            return "macos", "x86_64"
    elif system == "windows":
        if machine == "arm64":
            return "windows", "arm64"
        else:
            return "windows", "x64"
    else:
        return "linux", "x64"

def install_dependencies():
    """安装必要的依赖"""
    print("正在安装Python依赖...")
    
    # 升级pip
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    
    # 安装项目依赖
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "models/requirements.txt"], check=True)
    
    # 安装PyInstaller
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller==5.13.2"], check=True)

def build_executable(platform_name, arch):
    """构建可执行文件"""
    print(f"正在构建 {platform_name} {arch} 平台的可执行文件...")
    
    # 创建构建目录
    build_dir = Path(f"build/{platform_name}-{arch}")
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # 确定可执行文件名称
    if platform_name == "windows":
        exe_name = f"ocr_server_{arch}.exe"
    else:
        exe_name = f"ocr_server_{arch}"
    
    # 构建PyInstaller命令
    cmd = [
        "pyinstaller",
        "--clean",
        f"--distpath={build_dir}",
        f"--workpath={build_dir}/build",
        f"--specpath={build_dir}",
        f"--name={exe_name}",
        "--onefile",
        "--console",
        "--strip",
        "--add-data=models/det.onnx;." if platform_name == "windows" else "--add-data=models/det.onnx:.",
        "--add-data=models/rec.onnx;." if platform_name == "windows" else "--add-data=models/rec.onnx:.",
        "--add-data=models/ppocr_keys_v1.txt;." if platform_name == "windows" else "--add-data=models/ppocr_keys_v1.txt:.",
        "--add-data=assets/fonts/simfang.ttf;." if platform_name == "windows" else "--add-data=assets/fonts/simfang.ttf:.",
        "--hidden-import=cv2",
        "--hidden-import=numpy.core._methods",
        "--hidden-import=numpy.lib.format",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=onnxruntime.capi.onnxruntime_pybind11_state",
        "--hidden-import=shapely.geometry",
        "--hidden-import=pyclipper",
        "--hidden-import=http.server",
        "--hidden-import=urllib.parse",
        "--hidden-import=json",
        "--hidden-import=base64",
        "--hidden-import=io",
        "--hidden-import=threading",
        "--hidden-import=time",
        "--hidden-import=math",
        "--hidden-import=copy",
        "--hidden-import=random",
        "--hidden-import=argparse",
        "--hidden-import=glob",
        "--exclude-module=matplotlib",
        "--exclude-module=scipy",
        "--exclude-module=pandas",
        "--exclude-module=jupyter",
        "--exclude-module=IPython",
        "--exclude-module=notebook",
        "--exclude-module=tornado",
        "--exclude-module=zmq",
        "--exclude-module=tkinter",
        "--exclude-module=PyQt5",
        "--exclude-module=PySide2",
        "--exclude-module=wx",
        "--exclude-module=PyQt4",
        "--exclude-module=setuptools",
        "--exclude-module=pkg_resources",
        "--exclude-module=distutils",
        "--exclude-module=lib2to3",
        "--exclude-module=test",
        "--exclude-module=unittest",
        "--exclude-module=doctest",
        "--exclude-module=pdb",
        "--exclude-module=profile",
        "--exclude-module=pstats",
        "--exclude-module=timeit",
        "--exclude-module=trace",
        "--exclude-module=turtle",
        "--exclude-module=tcl",
        "--exclude-module=tk",
        "--exclude-module=_tkinter",
        "--exclude-module=PySide",
        "--exclude-module=PyQt6",
        "--exclude-module=PySide6",
        "--exclude-module=wxPython",
        "--exclude-module=wx._core",
        "--exclude-module=wx._controls",
        "--exclude-module=wx._gdi",
        "--exclude-module=matplotlib.backends",
        "--exclude-module=matplotlib.figure",
        "--exclude-module=matplotlib.pyplot",
        "--exclude-module=matplotlib.axes",
        "--exclude-module=matplotlib.patches",
        "--exclude-module=scipy.spatial",
        "--exclude-module=scipy.ndimage",
        "--exclude-module=scipy.signal",
        "--exclude-module=pandas.core",
        "--exclude-module=pandas.io",
        "--exclude-module=pandas.plotting",
        "--exclude-module=numpy.testing",
        "--exclude-module=numpy.f2py",
        "--exclude-module=numpy.distutils",
        "--exclude-module=PIL.ImageQt",
        "--exclude-module=PIL.ImageTk",
        "--exclude-module=PIL.ImageDraw2",
        "--exclude-module=cv2.cv",
        "--exclude-module=cv2.data",
        "--exclude-module=cv2.misc",
        "--exclude-module=shapely.speedups",
        "--exclude-module=shapely.vectorized",
        "--exclude-module=requests",
        "--exclude-module=urllib3",
        "--exclude-module=certifi",
        "--exclude-module=charset_normalizer",
        "--exclude-module=idna",
        "--exclude-module=chardet",
        "--exclude-module=flask",
        "--exclude-module=werkzeug",
        "--exclude-module=jinja2",
        "--exclude-module=markupsafe",
        "--exclude-module=itsdangerous",
        "--exclude-module=click",
        "--exclude-module=blinker",
        "--exclude-module=colorama",
        "run_server.py"
    ]
    
    # 在macOS上添加UPX压缩
    if platform_name == "macos":
        cmd.insert(-1, "--upx-dir=/usr/local/bin")
    
    # 执行构建
    subprocess.run(cmd, check=True)
    
    print(f"构建完成！可执行文件位置: {build_dir}/{exe_name}")

def create_package(platform_name, arch, version="1.0.0"):
    """创建发布包"""
    print(f"正在创建 {platform_name} {arch} 平台的发布包...")
    
    build_dir = Path(f"build/{platform_name}-{arch}")
    
    if platform_name == "windows":
        exe_name = f"ocr_server_{arch}.exe"
        package_name = f"ocr_server_{platform_name}_{arch}_{version}.zip"
        
        # 使用PowerShell创建ZIP包
        if platform.system().lower() == "windows":
            subprocess.run([
                "powershell", "Compress-Archive", 
                "-Path", str(build_dir / exe_name),
                "-DestinationPath", str(build_dir / package_name)
            ], check=True)
        else:
            # 在非Windows系统上使用zip命令
            subprocess.run([
                "zip", "-j", str(build_dir / package_name), str(build_dir / exe_name)
            ], check=True)
    else:
        exe_name = f"ocr_server_{arch}"
        package_name = f"ocr_server_{platform_name}_{arch}_{version}.tar.gz"
        
        # 创建tar.gz包
        subprocess.run([
            "tar", "-czf", str(build_dir / package_name), 
            "-C", str(build_dir), exe_name
        ], check=True)
    
    print(f"发布包创建完成: {build_dir}/{package_name}")

def main():
    """主函数"""
    print("=== OCR服务器本地构建脚本 ===")
    
    # 获取平台信息
    platform_name, arch = get_platform_info()
    print(f"当前平台: {platform_name} {arch}")
    
    # 检查必要文件
    required_files = [
        "run_server.py",
        "models/det.onnx",
        "models/rec.onnx", 
        "models/ppocr_keys_v1.txt",
        "assets/fonts/simfang.ttf"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("错误：以下必要文件缺失:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        sys.exit(1)
    
    try:
        # 安装依赖
        install_dependencies()
        
        # 构建可执行文件
        build_executable(platform_name, arch)
        
        # 创建发布包
        version = input("请输入版本号 (默认: 1.0.0): ").strip() or "1.0.0"
        create_package(platform_name, arch, version)
        
        print("\n=== 构建成功完成！ ===")
        print(f"平台: {platform_name} {arch}")
        print(f"版本: {version}")
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n构建被用户中断")
        sys.exit(1)

if __name__ == "__main__":
    main() 