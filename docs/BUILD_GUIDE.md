# OCR项目构建指南

## 概述

本指南介绍如何构建OCR项目的可执行文件，支持macOS和Windows平台。

## 快速开始

### 1. 环境准备

确保已安装以下依赖：

```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装PyInstaller
pip install pyinstaller
```

### 2. 一键构建

在项目根目录运行：

```bash
python scripts/build_universal.py
```

这个脚本会：
- 自动检测操作系统和可用工具
- 创建优化的配置文件
- 执行构建并验证结果

## 构建脚本说明

### scripts/build_universal.py
- **功能**: 跨平台通用构建脚本
- **支持平台**: macOS, Windows
- **特性**: 
  - 自动检测系统环境
  - 智能选择优化选项
  - 修复numpy打包问题
  - 自动验证构建结果

### scripts/build_local.py
- **功能**: 本地开发构建脚本
- **用途**: 开发环境快速构建

### scripts/quick_build.sh
- **功能**: Shell脚本构建工具
- **用途**: 自动化构建流程

## 平台差异

### macOS
- 支持UPX压缩（如果安装）
- 支持strip工具优化
- 生成无扩展名的可执行文件

### Windows
- 禁用UPX和strip工具（避免兼容性问题）
- 生成.exe扩展名的可执行文件
- 自动处理numpy模块依赖

## 常见问题

### Q: 构建失败怎么办？
A: 检查以下几点：
1. 确保在项目根目录运行脚本
2. 检查Python和PyInstaller版本
3. 确保所有依赖已正确安装

### Q: 可执行文件太大？
A: 这是正常的，因为包含了：
- OCR模型文件
- NumPy和OpenCV库
- 所有必要的依赖

### Q: 运行时出现numpy错误？
A: 使用`build_universal.py`脚本，它已修复numpy打包问题。

### Q: 如何减小文件大小？
A: 可以尝试：
1. 使用UPX压缩（macOS/Linux）
2. 优化excludes列表
3. 只包含必要的hiddenimports

## 构建输出

构建成功后，会在`dist/`目录生成：
- **macOS**: `ocr_server`
- **Windows**: `ocr_server.exe`

文件大小通常在70-80MB左右，这是正常的。

## 验证构建

运行以下命令验证构建结果：

```bash
# macOS
./dist/ocr_server --help

# Windows
dist/ocr_server.exe --help
```

如果显示帮助信息，说明构建成功。

## 故障排除

### 1. 检查环境
```bash
python --version
pip list | grep PyInstaller
```

### 2. 清理缓存
```bash
python -m PyInstaller --clean
```

### 3. 重新安装依赖
```bash
pip install -r requirements.txt --force-reinstall
```

### 4. 查看详细错误
```bash
python scripts/build_universal.py 2>&1 | tee build.log
```

## 高级配置

如需自定义构建配置，可以编辑`build/configs/ocr_server_universal.spec`文件：

- `hiddenimports`: 添加缺失的模块
- `excludes`: 排除不需要的模块
- `datas`: 添加额外的数据文件
- `strip/upx`: 控制优化选项

## 联系支持

如遇到问题，请提供：
1. 操作系统和Python版本
2. 完整的错误信息
3. 使用的构建命令 