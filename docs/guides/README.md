# OCR文字识别API服务

这是一个基于ONNX模型的OCR文字识别API服务，支持接收base64编码的图片并返回识别结果。

## 🚀 快速开始

### 一键启动（推荐）
```bash
python scripts/quick_start.py
```

### 手动启动
```bash
# 安装依赖
pip install -r requirements.txt

# 启动API服务器
python simple_api_server.py

# 测试OCR功能
python tests/simple_test.py

# 测试API接口
python tests/test_simple_api.py

# 运行客户端示例
python examples/client_example.py
```

## 📁 项目结构

```
text_recognition/
├── main.py                    # OCR核心功能
├── simple_api_server.py       # API服务器主文件
├── requirements.txt           # Python依赖
├── docs/                     # 文档目录
│   ├── README.md            # 详细使用说明
│   ├── PROJECT_SUMMARY.md   # 项目总结
│   └── FILES.md             # 文件说明
├── tests/                    # 测试目录
│   ├── simple_test.py       # OCR功能测试
│   └── test_simple_api.py   # API接口测试
├── examples/                 # 示例目录
│   └── client_example.py    # 客户端使用示例
├── scripts/                  # 脚本目录
│   └── quick_start.py       # 快速启动脚本
├── det.onnx                 # 检测模型
├── rec.onnx                 # 识别模型
├── ppocr_keys_v1.txt        # 字符映射文件
├── simfang.ttf              # 字体文件
└── imgs/                    # 测试图片目录
```

## 🔧 功能特性

- 🔍 **文字检测**: 自动检测图片中的文字区域
- 📝 **文字识别**: 识别检测到的文字内容
- 📍 **定位框**: 返回文字的精确边界框坐标
- 🎯 **置信度**: 提供识别结果的置信度评分
- 🌐 **RESTful API**: 提供标准的HTTP API接口

## 📖 文档

- [详细使用说明](docs/README.md) - 完整的使用指南和API文档
- [项目总结](docs/PROJECT_SUMMARY.md) - 项目概述和完成情况
- [文件说明](docs/FILES.md) - 每个文件的作用和用途

## 🧪 测试

```bash
# 测试OCR功能
python tests/simple_test.py

# 测试API接口
python tests/test_simple_api.py
```

## 📡 API接口

- `POST /ocr` - OCR识别接口
- `GET /health` - 健康检查接口
- `GET /` - API信息接口

服务地址: `http://localhost:8080`

## 💡 使用示例

```python
import requests
import base64

# 将图片转换为base64
with open('image.jpg', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

# 发送请求
response = requests.post('http://localhost:8080/ocr', 
                        json={'image': image_base64})
result = response.json()

if result['success']:
    for item in result['data']['results']:
        print(f"文字: {item['text']}")
        print(f"置信度: {item['confidence']}")
```

## 🛠️ 技术栈

- **后端**: Python内置HTTP服务器
- **图像处理**: OpenCV, PIL
- **机器学习**: ONNX Runtime
- **几何计算**: Shapely, Pyclipper
- **数值计算**: NumPy

## 📋 依赖

```
flask==2.3.3
opencv-python==4.8.1.78
numpy==1.24.3
Pillow==10.0.1
onnxruntime==1.16.1
shapely==2.0.2
pyclipper==1.3.0
requests==2.31.0
```

## ⚠️ 注意事项

1. 确保所有模型文件都在正确的位置
2. 图片支持常见的格式：JPEG, PNG, BMP等
3. Base64编码的图片字符串不应包含前缀
4. 服务启动后，第一次请求可能需要较长时间来加载模型

## �� 许可证

本项目仅供学习和研究使用。 