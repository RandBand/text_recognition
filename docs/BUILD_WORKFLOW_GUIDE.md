# OCR服务器多平台构建工作流指南

## 概述

本项目提供了完整的GitHub Actions工作流，用于自动构建OCR服务器的多平台可执行文件。支持以下平台和架构：

- **macOS ARM64** (Apple Silicon)
- **macOS x86_64** (Intel)
- **Windows x64** (Intel/AMD)
- **Windows ARM64**

## 文件结构

```
.github/workflows/
├── build_packages.yml          # 主要构建工作流
scripts/
├── build_local.py             # 本地构建脚本
docs/
├── BUILD_WORKFLOW_GUIDE.md   # 本指南
```

## 工作流特性

### 1. 自动触发条件
- **版本标签推送**: 当推送以 `v` 开头的标签时自动触发
- **手动触发**: 可在GitHub Actions页面手动触发，支持自定义版本号

### 2. 构建优化
- **依赖排除**: 排除不必要的模块以减小包体积
- **UPX压缩**: 在macOS上使用UPX进行可执行文件压缩
- **Strip调试信息**: 移除调试符号减小文件大小
- **单文件打包**: 生成独立的可执行文件

### 3. 资源文件包含
自动包含以下必要文件：
- `models/det.onnx` - 检测模型
- `models/rec.onnx` - 识别模型
- `models/ppocr_keys_v1.txt` - 字符集文件
- `assets/fonts/simfang.ttf` - 字体文件

## 使用方法

### 方法一：GitHub Actions自动构建

#### 1. 推送版本标签触发构建
```bash
# 创建并推送版本标签
git tag v1.0.0
git push origin v1.0.0
```

#### 2. 手动触发构建
1. 访问GitHub仓库的Actions页面
2. 选择"构建多平台OCR服务器包"工作流
3. 点击"Run workflow"
4. 输入版本号（如：1.0.0）
5. 点击"Run workflow"开始构建

### 方法二：本地构建测试

#### 1. 运行本地构建脚本
```bash
# 安装依赖并构建当前平台的可执行文件
python scripts/build_local.py
```

#### 2. 手动PyInstaller构建
```bash
# 安装依赖
pip install -r models/requirements.txt
pip install pyinstaller==5.13.2

# macOS构建
pyinstaller --clean \
  --name ocr_server \
  --onefile \
  --console \
  --strip \
  --add-data "models/det.onnx:." \
  --add-data "models/rec.onnx:." \
  --add-data "models/ppocr_keys_v1.txt:." \
  --add-data "assets/fonts/simfang.ttf:." \
  run_server.py

# Windows构建
pyinstaller --clean ^
  --name ocr_server.exe ^
  --onefile ^
  --console ^
  --strip ^
  --add-data "models\det.onnx;." ^
  --add-data "models\rec.onnx;." ^
  --add-data "models\ppocr_keys_v1.txt;." ^
  --add-data "assets\fonts\simfang.ttf;." ^
  run_server.py
```

## 构建产物

### 文件命名规则
- **macOS ARM64**: `ocr_server_macos_arm64_v1.0.0.tar.gz`
- **macOS x86_64**: `ocr_server_macos_x86_64_v1.0.0.tar.gz`
- **Windows x64**: `ocr_server_windows_x64_v1.0.0.zip`
- **Windows ARM64**: `ocr_server_windows_arm64_v1.0.0.zip`

### 下载位置
- **GitHub Actions**: 构建完成后可在Actions页面下载构建产物
- **GitHub Release**: 当推送版本标签时，会自动创建Release并上传所有平台的构建产物

## 工作流步骤详解

### 1. 环境准备
```yaml
- 检出代码
- 设置Python环境 (Python 3.9)
- 安装系统依赖 (macOS: Homebrew, pkg-config)
- 安装Python依赖 (requirements.txt + PyInstaller)
```

### 2. 构建过程
```yaml
- 创建构建目录
- 执行PyInstaller打包
- 包含必要的数据文件
- 排除不必要的模块
- 应用优化选项 (strip, upx)
```

### 3. 打包发布
```yaml
- 创建压缩包 (tar.gz for macOS, zip for Windows)
- 上传构建产物到GitHub Actions
- 创建GitHub Release (仅版本标签触发)
```

## 优化配置

### 隐藏导入 (Hidden Imports)
确保包含所有必要的模块：
```yaml
- cv2
- numpy.core._methods
- numpy.lib.format
- PIL._tkinter_finder
- onnxruntime.capi.onnxruntime_pybind11_state
- shapely.geometry
- pyclipper
- http.server
- urllib.parse
- json, base64, io, threading, time, math, copy, random, argparse, glob
```

### 排除模块 (Excluded Modules)
排除不必要的模块以减小包体积：
```yaml
- matplotlib, scipy, pandas
- jupyter, IPython, notebook
- tornado, zmq, tkinter
- PyQt5, PySide2, wx
- setuptools, pkg_resources, distutils
- test, unittest, doctest, pdb
- 各种GUI和科学计算库
```

## 故障排除

### 常见问题

#### 1. 构建失败
- 检查所有必要文件是否存在
- 确认Python版本兼容性
- 查看GitHub Actions日志获取详细错误信息

#### 2. 可执行文件过大
- 检查是否排除了不必要的模块
- 确认UPX压缩是否生效
- 考虑使用更严格的模块排除规则

#### 3. 运行时错误
- 确认所有数据文件已正确包含
- 检查隐藏导入是否完整
- 测试可执行文件在目标平台上的兼容性

### 调试技巧

#### 1. 本地测试
```bash
# 在构建前测试Python脚本
python run_server.py

# 测试PyInstaller配置
pyinstaller --debug=all run_server.py
```

#### 2. 检查构建产物
```bash
# 检查可执行文件大小
ls -lh build/*/ocr_server*

# 检查包含的文件
unzip -l build/windows-x64/ocr_server_windows_x64_v1.0.0.zip
tar -tzf build/macos-arm64/ocr_server_macos_arm64_v1.0.0.tar.gz
```

## 版本管理

### 版本号规范
- 使用语义化版本号 (如: 1.0.0, 1.1.0, 2.0.0)
- 标签格式: `v1.0.0`
- 构建产物自动包含版本号

### 发布流程
1. 更新代码并提交
2. 创建版本标签: `git tag v1.0.0`
3. 推送标签: `git push origin v1.0.0`
4. 等待GitHub Actions完成构建
5. 检查GitHub Release页面
6. 下载并测试各平台构建产物

## 自定义配置

### 修改Python版本
在 `.github/workflows/build_packages.yml` 中修改：
```yaml
env:
  PYTHON_VERSION: '3.9'  # 改为需要的版本
```

### 添加新的排除模块
在PyInstaller命令中添加：
```bash
--exclude-module=新模块名
```

### 修改构建参数
- 更改可执行文件名称: `--name=新名称`
- 添加图标: `--icon=图标文件路径`
- 修改输出格式: `--onedir` 或 `--onefile`

## 性能优化建议

1. **并行构建**: 工作流中的4个平台构建任务并行执行
2. **缓存优化**: 考虑添加pip缓存以加速依赖安装
3. **增量构建**: 对于大型项目，考虑使用Docker镜像预装依赖
4. **压缩优化**: 在macOS上使用UPX压缩可执行文件

## 安全考虑

1. **依赖安全**: 定期更新requirements.txt中的依赖版本
2. **代码签名**: 考虑为macOS构建添加代码签名
3. **权限控制**: 确保GitHub Actions权限设置合理
4. **敏感信息**: 避免在构建过程中暴露敏感信息

## 联系支持

如果遇到构建问题，请：
1. 检查GitHub Actions日志
2. 查看本指南的故障排除部分
3. 在项目Issues中报告问题
4. 提供详细的错误信息和复现步骤 