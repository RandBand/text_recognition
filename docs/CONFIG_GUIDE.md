# 配置系统使用指南

## 📋 概述

项目现在使用统一的配置系统，所有配置项都在 `config.py` 文件中集中管理。这样可以确保配置的一致性，并简化维护工作。

## 🔧 配置项说明

### 服务器配置
```python
SERVER_HOST = "localhost"      # 服务器主机地址
SERVER_PORT = 8080            # 服务器端口
SERVER_DEBUG = False          # 调试模式
API_BASE_URL = "http://localhost:8080"  # API基础URL
```

### 模型配置
```python
DET_MODEL_PATH = "det.onnx"           # 检测模型路径
REC_MODEL_PATH = "rec.onnx"           # 识别模型路径
OCR_KEYS_PATH = "ppocr_keys_v1.txt"   # 字符映射文件路径
FONT_PATH = "simfang.ttf"             # 字体文件路径
```

### 测试配置
```python
TEST_IMAGES_DIR = "imgs"              # 测试图片目录
TEST_IMAGES = ["1.jpg", "11.jpg", "12.jpg"]  # 测试图片列表
```

### OCR参数配置
```python
DET_DB_THRESH = 0.3          # 检测阈值
DET_DB_BOX_THRESH = 0.5      # 检测框阈值
MAX_CANDIDATES = 2000         # 最大候选数
UNCLIP_RATIO = 1.6           # 解裁剪比例
USE_DILATION = True           # 是否使用膨胀
DROP_SCORE = 0.5             # 置信度过滤阈值
```

### 超时配置
```python
REQUEST_TIMEOUT = 30          # 请求超时时间（秒）
HEALTH_CHECK_TIMEOUT = 5      # 健康检查超时时间（秒）
```

## 🚀 使用方法

### 1. 修改端口
要修改服务器端口，只需要在 `config.py` 中修改 `SERVER_PORT`：

```python
# 修改前
SERVER_PORT = 8080

# 修改后
SERVER_PORT = 9090
```

修改后，所有使用该端口的文件都会自动使用新端口。

### 2. 修改模型路径
要修改模型文件路径：

```python
# 修改前
DET_MODEL_PATH = "det.onnx"

# 修改后
DET_MODEL_PATH = "models/det.onnx"
```

### 3. 添加测试图片
要添加新的测试图片：

```python
# 修改前
TEST_IMAGES = ["1.jpg", "11.jpg", "12.jpg"]

# 修改后
TEST_IMAGES = ["1.jpg", "11.jpg", "12.jpg", "new_image.jpg"]
```

### 4. 调整OCR参数
要调整OCR识别参数：

```python
# 提高检测精度
DET_DB_THRESH = 0.2          # 降低阈值，提高检测精度
DET_DB_BOX_THRESH = 0.3      # 降低框阈值

# 提高过滤标准
DROP_SCORE = 0.7              # 提高置信度要求
```

## 📁 配置文件位置

```
text_recognition/
├── config.py                 # 主配置文件
├── simple_api_server.py      # API服务器（使用配置）
├── tests/                    # 测试文件（使用配置）
│   ├── simple_test.py
│   └── test_simple_api.py
├── examples/                 # 示例文件（使用配置）
│   └── client_example.py
└── scripts/                  # 脚本文件（使用配置）
    └── quick_start.py
```

## 🔍 配置验证

运行以下命令验证配置：

```bash
python config.py
```

输出示例：
```
✅ 配置验证通过

📋 配置信息:
{
  "server": {
    "host": "localhost",
    "port": 8080,
    "debug": false,
    "base_url": "http://localhost:8080"
  },
  "models": {
    "det_model": "det.onnx",
    "rec_model": "rec.onnx",
    "ocr_keys": "ppocr_keys_v1.txt",
    "font": "simfang.ttf"
  },
  ...
}
```

## 🛠️ 配置函数

### 路径相关函数
```python
get_test_image_path(filename)  # 获取测试图片完整路径
get_test_images()              # 获取所有测试图片路径
get_api_url(endpoint)          # 获取API完整URL
```

### 验证函数
```python
check_required_files()         # 检查必需文件
validate_config()              # 验证配置有效性
get_config_info()              # 获取配置信息
```

## ⚠️ 注意事项

1. **端口范围**: 端口必须在 1024-65535 范围内
2. **文件存在**: 所有模型文件必须存在
3. **路径正确**: 确保所有路径都是正确的
4. **导入顺序**: 在使用配置前确保已导入

## 🔄 配置更新流程

1. 修改 `config.py` 中的配置项
2. 运行 `python config.py` 验证配置
3. 测试相关功能确保正常工作
4. 更新文档（如需要）

## 📝 最佳实践

1. **集中管理**: 所有配置都在 `config.py` 中
2. **验证配置**: 修改配置后先验证
3. **文档更新**: 重要配置变更要更新文档
4. **版本控制**: 配置变更要提交到版本控制
5. **备份配置**: 重要配置要备份

## 🎯 配置示例

### 生产环境配置
```python
SERVER_HOST = "0.0.0.0"      # 允许外部访问
SERVER_PORT = 80              # 标准HTTP端口
SERVER_DEBUG = False          # 关闭调试模式
REQUEST_TIMEOUT = 60          # 增加超时时间
```

### 开发环境配置
```python
SERVER_HOST = "localhost"     # 仅本地访问
SERVER_PORT = 8080           # 开发端口
SERVER_DEBUG = True           # 开启调试模式
REQUEST_TIMEOUT = 30          # 标准超时时间
```

### 测试环境配置
```python
SERVER_HOST = "localhost"
SERVER_PORT = 9090           # 测试端口
DROP_SCORE = 0.3             # 降低过滤标准
MAX_CANDIDATES = 1000        # 减少候选数
``` 