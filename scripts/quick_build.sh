#!/bin/bash
# -*- coding: utf-8 -*-
"""
快速构建脚本 - 用于快速测试PyInstaller打包
支持macOS和Linux平台
"""

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查必要文件
check_required_files() {
    print_info "检查必要文件..."
    
    local required_files=(
        "run_server.py"
        "models/det.onnx"
        "models/rec.onnx"
        "models/ppocr_keys_v1.txt"
        "assets/fonts/simfang.ttf"
    )
    
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_error "以下必要文件缺失:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        exit 1
    fi
    
    print_success "所有必要文件存在"
}

# 安装依赖
install_dependencies() {
    print_info "安装Python依赖..."
    
    # 升级pip
    python3 -m pip install --upgrade pip
    
    # 安装项目依赖
    python3 -m pip install -r models/requirements.txt
    
    # 安装PyInstaller
    python3 -m pip install pyinstaller==5.13.2
    
    print_success "依赖安装完成"
}

# 获取平台信息
get_platform_info() {
    local system=$(uname -s | tr '[:upper:]' '[:lower:]')
    local machine=$(uname -m)
    
    if [[ "$system" == "darwin" ]]; then
        if [[ "$machine" == "arm64" ]]; then
            echo "macos arm64"
        else
            echo "macos x86_64"
        fi
    elif [[ "$system" == "linux" ]]; then
        if [[ "$machine" == "aarch64" ]]; then
            echo "linux arm64"
        else
            echo "linux x86_64"
        fi
    else
        print_error "不支持的操作系统: $system"
        exit 1
    fi
}

# 构建可执行文件
build_executable() {
    local platform_info=$1
    local platform=$(echo $platform_info | cut -d' ' -f1)
    local arch=$(echo $platform_info | cut -d' ' -f2)
    
    print_info "构建 $platform $arch 平台的可执行文件..."
    
    # 创建构建目录
    local build_dir="build/${platform}-${arch}"
    mkdir -p "$build_dir"
    
    # 确定可执行文件名称
    local exe_name="ocr_server_${arch}"
    
    # 构建PyInstaller命令
    local cmd=(
        "pyinstaller"
        "--clean"
        "--distpath=$build_dir"
        "--workpath=$build_dir/build"
        "--specpath=$build_dir"
        "--name=$exe_name"
        "--onefile"
        "--console"
        "--strip"
        "--add-data=models/det.onnx:."
        "--add-data=models/rec.onnx:."
        "--add-data=models/ppocr_keys_v1.txt:."
        "--add-data=assets/fonts/simfang.ttf:."
        "--hidden-import=cv2"
        "--hidden-import=numpy.core._methods"
        "--hidden-import=numpy.lib.format"
        "--hidden-import=PIL._tkinter_finder"
        "--hidden-import=onnxruntime.capi.onnxruntime_pybind11_state"
        "--hidden-import=shapely.geometry"
        "--hidden-import=pyclipper"
        "--hidden-import=http.server"
        "--hidden-import=urllib.parse"
        "--hidden-import=json"
        "--hidden-import=base64"
        "--hidden-import=io"
        "--hidden-import=threading"
        "--hidden-import=time"
        "--hidden-import=math"
        "--hidden-import=copy"
        "--hidden-import=random"
        "--hidden-import=argparse"
        "--hidden-import=glob"
        "--exclude-module=matplotlib"
        "--exclude-module=scipy"
        "--exclude-module=pandas"
        "--exclude-module=jupyter"
        "--exclude-module=IPython"
        "--exclude-module=notebook"
        "--exclude-module=tornado"
        "--exclude-module=zmq"
        "--exclude-module=tkinter"
        "--exclude-module=PyQt5"
        "--exclude-module=PySide2"
        "--exclude-module=wx"
        "--exclude-module=PyQt4"
        "--exclude-module=setuptools"
        "--exclude-module=pkg_resources"
        "--exclude-module=distutils"
        "--exclude-module=lib2to3"
        "--exclude-module=test"
        "--exclude-module=unittest"
        "--exclude-module=doctest"
        "--exclude-module=pdb"
        "--exclude-module=profile"
        "--exclude-module=pstats"
        "--exclude-module=timeit"
        "--exclude-module=trace"
        "--exclude-module=turtle"
        "--exclude-module=tcl"
        "--exclude-module=tk"
        "--exclude-module=_tkinter"
        "--exclude-module=PySide"
        "--exclude-module=PyQt6"
        "--exclude-module=PySide6"
        "--exclude-module=wxPython"
        "--exclude-module=wx._core"
        "--exclude-module=wx._controls"
        "--exclude-module=wx._gdi"
        "--exclude-module=matplotlib.backends"
        "--exclude-module=matplotlib.figure"
        "--exclude-module=matplotlib.pyplot"
        "--exclude-module=matplotlib.axes"
        "--exclude-module=matplotlib.patches"
        "--exclude-module=scipy.spatial"
        "--exclude-module=scipy.ndimage"
        "--exclude-module=scipy.signal"
        "--exclude-module=pandas.core"
        "--exclude-module=pandas.io"
        "--exclude-module=pandas.plotting"
        "--exclude-module=numpy.testing"
        "--exclude-module=numpy.f2py"
        "--exclude-module=numpy.distutils"
        "--exclude-module=PIL.ImageQt"
        "--exclude-module=PIL.ImageTk"
        "--exclude-module=PIL.ImageDraw2"
        "--exclude-module=cv2.cv"
        "--exclude-module=cv2.data"
        "--exclude-module=cv2.misc"
        "--exclude-module=shapely.speedups"
        "--exclude-module=shapely.vectorized"
        "--exclude-module=requests"
        "--exclude-module=urllib3"
        "--exclude-module=certifi"
        "--exclude-module=charset_normalizer"
        "--exclude-module=idna"
        "--exclude-module=chardet"
        "--exclude-module=flask"
        "--exclude-module=werkzeug"
        "--exclude-module=jinja2"
        "--exclude-module=markupsafe"
        "--exclude-module=itsdangerous"
        "--exclude-module=click"
        "--exclude-module=blinker"
        "--exclude-module=colorama"
        "run_server.py"
    )
    
    # 在macOS上添加UPX压缩
    if [[ "$platform" == "macos" ]]; then
        cmd+=("--upx-dir=/usr/local/bin")
    fi
    
    # 执行构建
    "${cmd[@]}"
    
    print_success "构建完成！可执行文件位置: $build_dir/$exe_name"
    
    # 显示文件大小
    if [[ -f "$build_dir/$exe_name" ]]; then
        local size=$(du -h "$build_dir/$exe_name" | cut -f1)
        print_info "可执行文件大小: $size"
    fi
}

# 创建发布包
create_package() {
    local platform_info=$1
    local version=${2:-"1.0.0"}
    local platform=$(echo $platform_info | cut -d' ' -f1)
    local arch=$(echo $platform_info | cut -d' ' -f2)
    
    print_info "创建 $platform $arch 平台的发布包..."
    
    local build_dir="build/${platform}-${arch}"
    local exe_name="ocr_server_${arch}"
    local package_name="ocr_server_${platform}_${arch}_${version}.tar.gz"
    
    if [[ -f "$build_dir/$exe_name" ]]; then
        # 创建tar.gz包
        tar -czf "$build_dir/$package_name" -C "$build_dir" "$exe_name"
        
        local package_size=$(du -h "$build_dir/$package_name" | cut -f1)
        print_success "发布包创建完成: $build_dir/$package_name (大小: $package_size)"
    else
        print_error "可执行文件不存在: $build_dir/$exe_name"
        exit 1
    fi
}

# 主函数
main() {
    echo "=== OCR服务器快速构建脚本 ==="
    echo
    
    # 检查必要文件
    check_required_files
    
    # 安装依赖
    install_dependencies
    
    # 获取平台信息
    local platform_info=$(get_platform_info)
    print_info "当前平台: $platform_info"
    
    # 构建可执行文件
    build_executable "$platform_info"
    
    # 创建发布包
    local version=${1:-"1.0.0"}
    create_package "$platform_info" "$version"
    
    echo
    print_success "=== 构建成功完成！ ==="
    print_info "平台: $platform_info"
    print_info "版本: $version"
    echo
    print_info "构建产物位置:"
    local platform=$(echo $platform_info | cut -d' ' -f1)
    local arch=$(echo $platform_info | cut -d' ' -f2)
    echo "  - 可执行文件: build/${platform}-${arch}/ocr_server_${arch}"
    echo "  - 发布包: build/${platform}-${arch}/ocr_server_${platform}_${arch}_${version}.tar.gz"
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [版本号]"
    echo
    echo "参数:"
    echo "  版本号    指定版本号 (默认: 1.0.0)"
    echo
    echo "示例:"
    echo "  $0              # 使用默认版本号 1.0.0"
    echo "  $0 2.0.0       # 使用版本号 2.0.0"
    echo
    echo "支持平台:"
    echo "  - macOS ARM64 (Apple Silicon)"
    echo "  - macOS x86_64 (Intel)"
    echo "  - Linux ARM64"
    echo "  - Linux x86_64"
}

# 检查参数
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# 执行主函数
main "$@" 