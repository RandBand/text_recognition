# OCR 文字识别服务器

一个基于 Python 的 OCR 文字识别服务器，支持多语言文字识别。

## 🚀 快速开始

### 使用 GitHub Actions 构建

1. **上传到 GitHub**
   ```bash
   ./scripts/setup_github.sh
   ```

2. **查看构建状态**
   - 访问您的 GitHub 仓库
   - 点击 "Actions" 标签页
   - 等待构建完成

3. **下载构建产物**
   - 在 Actions 页面下载对应架构的可执行文件
   - macOS: `ocr_server_macos_x64` 或 `ocr_server_macos_arm64`
   - Windows: `ocr_server_windows_x64.exe` 或 `ocr_server_windows_arm64.exe`

### 本地运行

1. **安装依赖**
   ```bash
   pip install -r models/requirements.txt
   ```

2. **启动服务器**
   ```bash
   python run_server.py
   ```

3. **测试 API**
   ```bash
   curl -X POST http://localhost:8080/ocr \
     -H "Content-Type: application/json" \
     -d '{"image": "base64_encoded_image"}'
   ```

## 📦 支持的架构

- **macOS**: Intel (x64) 和 Apple Silicon (ARM64)
- **Windows**: AMD64 (x64) 和 ARM64

## 🔧 API 接口

### OCR 识别
- **URL**: `POST /ocr`
- **请求体**: `{"image": "base64_encoded_image"}`
- **响应**: `{"text_count": 1, "results": [{"text": "识别的文字", "confidence": 0.95}]}`

### 健康检查
- **URL**: `GET /health`
- **响应**: `{"success": true, "message": "OCR服务运行正常"}`

### 服务信息
- **URL**: `GET /`
- **响应**: 服务状态和版本信息

## 📁 项目结构

```
text_recognition/
├── .github/workflows/     # GitHub Actions 配置
├── assets/                # 字体和测试图片
├── models/                # OCR 模型文件
├── src/                   # 源代码
├── tests/                 # 测试文件
├── docs/                  # 文档
└── scripts/               # 工具脚本
```

## 📖 文档

- [GitHub Actions 使用指南](docs/GITHUB_ACTIONS_GUIDE.md)
- [项目结构说明](docs/DIRECTORY_STRUCTURE.md)
- [配置指南](docs/CONFIG_GUIDE.md)
- [使用指南](docs/guides/USAGE_GUIDE.md)

## 🛠️ 开发

### 本地构建

```bash
# 安装 PyInstaller
pip install pyinstaller

# 构建可执行文件
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

### 运行测试

```bash
python -m pytest tests/ -v
```

## 📝 许可证

本项目采用 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如果您遇到问题，请：

1. 查看 [文档](docs/)
2. 提交 [Issue](https://github.com/yourusername/text_recognition/issues)
3. 查看 [GitHub Actions 日志](https://github.com/yourusername/text_recognition/actions) 