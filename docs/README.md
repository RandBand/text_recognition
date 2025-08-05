# OCR文字识别API服务

这是一个基于ONNX模型的OCR文字识别API服务，支持接收base64编码的图片并返回识别结果。

## 功能特性

- 🔍 文字检测：自动检测图片中的文字区域
- 📝 文字识别：识别检测到的文字内容
- 📍 定位框：返回文字的精确边界框坐标
- 🎯 置信度：提供识别结果的置信度评分
- 🌐 RESTful API：提供标准的HTTP API接口

## 项目结构

```
text_recognition/
├── main.py                    # OCR核心功能
├── simple_api_server.py       # API服务器主文件
├── requirements.txt           # Python依赖
├── docs/                     # 文档目录
│   ├── README.md            # 项目说明
│   ├── PROJECT_SUMMARY.md   # 项目总结
│   └── FILES.md             # 文件说明
├── tests/                    # 测试目录
│   ├── simple_test.py       # OCR功能测试
│   └── test_simple_api.py   # API接口测试
├── examples/                 # 示例目录
│   └── client_example.py    # 客户端使用示例
├── scripts/                  # 脚本目录
│   └── quick_start.py       # 快速启动脚本
├── models/                   # 模型文件
│   ├── det.onnx            # 检测模型
│   ├── rec.onnx            # 识别模型
│   ├── ppocr_keys_v1.txt   # 字符映射文件
│   └── simfang.ttf         # 字体文件
└── imgs/                    # 测试图片目录
    ├── 1.jpg
    ├── 11.jpg
    └── 12.jpg
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 一键启动（推荐）
```bash
python scripts/quick_start.py
```

### 手动启动
```bash
# 启动API服务器
python simple_api_server.py

# 测试OCR功能
python tests/simple_test.py

# 测试API接口
python tests/test_simple_api.py

# 运行客户端示例
python examples/client_example.py
```

服务将在 `http://localhost:8080` 启动。

## API接口说明

### 1. OCR识别接口

**接口地址：** `POST /ocr`

**请求格式：**
```json
{
    "image": "base64编码的图片字符串"
}
```

**响应格式：**
```json
{
    "success": true,
    "data": {
        "text_count": 2,
        "results": [
            {
                "text": "识别的文字",
                "confidence": 0.95,
                "bbox": {
                    "xmin": 100,
                    "ymin": 50,
                    "xmax": 300,
                    "ymax": 80,
                    "points": [[100, 50], [300, 50], [300, 80], [100, 80]]
                }
            }
        ]
    }
}
```

### 2. 健康检查接口

**接口地址：** `GET /health`

**响应格式：**
```json
{
    "success": true,
    "message": "OCR服务运行正常"
}
```

### 3. API信息接口

**接口地址：** `GET /`

返回API使用说明和接口列表。

## 使用示例

### Python客户端示例

```python
import requests
import base64

def image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

# 准备请求数据
image_base64 = image_to_base64('your_image.jpg')
data = {'image': image_base64}

# 发送请求
response = requests.post('http://localhost:8080/ocr', json=data)
result = response.json()

if result['success']:
    for item in result['data']['results']:
        print(f"文字: {item['text']}")
        print(f"置信度: {item['confidence']}")
        print(f"边界框: {item['bbox']}")
```

### cURL示例

```bash
# 将图片转换为base64
base64_image=$(base64 -i your_image.jpg)

# 发送请求
curl -X POST http://localhost:8080/ocr \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$base64_image\"}"
```

## 测试

运行测试脚本验证API功能：

```bash
# 测试OCR功能
python tests/simple_test.py

# 测试API接口
python tests/test_simple_api.py
```

## 技术栈

- **后端框架**: Python内置HTTP服务器
- **图像处理**: OpenCV, PIL
- **机器学习**: ONNX Runtime
- **几何计算**: Shapely, Pyclipper
- **数值计算**: NumPy

## 注意事项

1. 确保所有模型文件都在正确的位置
2. 图片支持常见的格式：JPEG, PNG, BMP等
3. Base64编码的图片字符串不应包含前缀（如 `data:image/jpeg;base64,`）
4. 服务启动后，第一次请求可能需要较长时间来加载模型

## 错误处理

API会返回标准的HTTP状态码和JSON格式的错误信息：

- `400`: 请求参数错误
- `500`: 服务器内部错误

错误响应格式：
```json
{
    "success": false,
    "error": "错误描述"
}
```

## 文档

- [项目总结](docs/PROJECT_SUMMARY.md) - 详细的项目概述和完成情况
- [文件说明](docs/FILES.md) - 每个文件的作用和用途 