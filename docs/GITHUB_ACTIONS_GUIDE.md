# GitHub Actions 构建指南

## 概述

本项目使用 GitHub Actions 来自动构建多架构的可执行文件包。支持以下架构：

- **macOS**: Intel (x64) 和 Apple Silicon (ARM64)
- **Windows**: AMD64 (x64) 和 ARM64

## 工作流文件

项目包含两个 GitHub Actions 工作流文件：

1. `.github/workflows/build.yml` - 完整版本，包含测试和Linux构建
2. `.github/workflows/build-simple.yml` - 简化版本，仅构建macOS和Windows

## 触发条件

工作流会在以下情况下自动触发：

- 推送到 `main` 或 `master` 分支
- 创建 Pull Request 到 `main` 或 `master` 分支
- 发布新的 Release

## 构建产物

每次构建会生成以下文件：

### macOS
- `ocr_server_macos_x64` - Intel Mac 可执行文件
- `ocr_server_macos_arm64` - Apple Silicon Mac 可执行文件

### Windows
- `ocr_server_windows_x64.exe` - AMD64 Windows 可执行文件
- `ocr_server_windows_arm64.exe` - ARM64 Windows 可执行文件

## 使用方法

### 1. 上传到 GitHub

```bash
# 初始化 Git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit"

# 添加远程仓库（替换为您的 GitHub 仓库 URL）
git remote add origin https://github.com/yourusername/text_recognition.git

# 推送到 GitHub
git push -u origin main
```

### 2. 查看构建状态

1. 访问您的 GitHub 仓库页面
2. 点击 "Actions" 标签页
3. 查看构建进度和结果

### 3. 下载构建产物

构建完成后，您可以在 Actions 页面下载构建产物：

1. 点击成功的构建任务
2. 在 "Artifacts" 部分下载相应的文件

### 4. 创建 Release

要创建包含所有构建产物的 Release：

1. 在 GitHub 仓库页面点击 "Releases"
2. 点击 "Create a new release"
3. 填写版本号和描述
4. 发布 Release

系统会自动构建并上传所有架构的包。

## 本地测试

在推送之前，建议先在本地测试构建：

```bash
# 安装依赖
pip install -r models/requirements.txt
pip install pyinstaller

# 构建 macOS 版本
pyinstaller --onefile \
  --add-data "models:models" \
  --add-data "assets:assets" \
  --hidden-import cv2 \
  --hidden-import numpy \
  --hidden-import PIL \
  --hidden-import onnxruntime \
  --hidden-import shapely \
  --hidden-import pyclipper \
  --name "ocr_server" \
  run_server.py
```

## 故障排除

### 常见问题

1. **构建失败**: 检查依赖是否正确安装
2. **文件缺失**: 确保 `models/` 和 `assets/` 目录存在
3. **权限问题**: 确保 GitHub Actions 有足够权限

### 调试步骤

1. 查看 Actions 日志中的错误信息
2. 检查 Python 版本兼容性
3. 验证所有必需文件是否存在

## 自定义配置

### 修改构建参数

在 `.github/workflows/build-simple.yml` 中：

- 修改 `python-version` 来使用不同的 Python 版本
- 调整 `architecture` 矩阵来构建不同架构
- 添加或移除 `--hidden-import` 参数

### 添加新的依赖

1. 更新 `models/requirements.txt`
2. 在 PyInstaller 命令中添加相应的 `--hidden-import`

## 注意事项

1. 构建产物可能较大，包含所有依赖
2. 首次构建可能需要较长时间
3. 确保模型文件路径正确
4. 定期更新依赖版本以修复安全漏洞 