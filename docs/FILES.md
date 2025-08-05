# 项目文件说明

## 目录结构

```
text_recognition/
├── main.py                    # OCR核心功能
├── simple_api_server.py       # API服务器主文件
├── requirements.txt           # Python依赖
├── docs/                     # 文档目录
├── tests/                    # 测试目录
├── examples/                 # 示例目录
├── scripts/                  # 脚本目录
├── models/                   # 模型文件（待创建）
└── imgs/                    # 测试图片目录
```

## 核心文件

### 配置管理
- `config.py` - 统一配置文件
  - 集中管理所有配置项
  - 服务器、模型、测试等配置
  - 提供配置验证和路径管理功能

### API服务器
- `simple_api_server.py` - 主要API服务器，使用Python内置HTTP服务器
  - 提供OCR识别接口
  - 支持base64图片输入
  - 返回JSON格式的识别结果
  - 使用统一配置管理

### OCR核心功能
- `main.py` - 原始OCR识别核心功能
  - 包含所有OCR处理类和方法
  - 文字检测和识别功能
  - 模型加载和推理

## 文档目录 (docs/)

### 项目文档
- `README.md` - 项目使用说明
  - 详细的使用指南
  - API接口说明
  - 示例代码

- `PROJECT_SUMMARY.md` - 项目总结
  - 项目概述和完成情况
  - 技术实现细节
  - 测试结果

- `FILES.md` - 本文件，项目文件说明

## 测试目录 (tests/)

### 功能测试
- `simple_test.py` - OCR功能测试
  - 验证OCR核心功能是否正常工作
  - 测试图片识别和结果输出
  - 使用统一配置管理

### API测试
- `test_simple_api.py` - API接口测试
  - 完整的API接口测试
  - 健康检查、信息获取、OCR识别测试
  - 使用统一配置管理

## 示例目录 (examples/)

### 客户端示例
- `client_example.py` - 客户端使用示例
  - 演示如何使用OCR API
  - 包含完整的客户端类
  - 支持图片路径和PIL图像输入
  - 使用统一配置管理

## 脚本目录 (scripts/)

### 快速启动
- `quick_start.py` - 快速启动脚本
  - 一键检查依赖、测试功能、启动服务
  - 自动化测试和验证流程
  - 适合新用户快速上手
  - 使用统一配置管理

## 配置文件

### 统一配置
- `config.py` - 统一配置文件
  - 集中管理所有配置项
  - 服务器、模型、测试等配置
  - 提供配置验证和路径管理功能

### 依赖管理
- `requirements.txt` - Python依赖包列表
  - 包含所有必要的第三方库
  - 指定版本号确保兼容性

## 模型文件

### ONNX模型
- `det.onnx` - 文字检测模型
- `rec.onnx` - 文字识别模型

### 配置文件
- `ppocr_keys_v1.txt` - 字符映射文件
  - 包含所有可识别字符的映射关系

### 字体文件
- `simfang.ttf` - 字体文件
  - 用于文字渲染和显示

## 测试资源

### 图片目录
- `imgs/` - 测试图片目录
  - 包含各种测试图片
  - 用于验证OCR功能

## 文件大小统计

```
text_recognition/
├── config.py               # 3.2KB - 统一配置文件
├── main.py                 # 25KB - OCR核心功能
├── simple_api_server.py    # 7.6KB - API服务器
├── requirements.txt        # 135B - 依赖文件
├── docs/                   # 文档目录
│   ├── README.md          # 3.8KB - 使用说明
│   ├── PROJECT_SUMMARY.md # 4.7KB - 项目总结
│   ├── FILES.md           # 2.7KB - 本文件
│   └── CONFIG_GUIDE.md    # 8.5KB - 配置指南
├── tests/                  # 测试目录
│   ├── simple_test.py     # 2.3KB - 功能测试
│   └── test_simple_api.py # 4.2KB - API测试
├── examples/               # 示例目录
│   └── client_example.py  # 4.7KB - 客户端示例
├── scripts/                # 脚本目录
│   └── quick_start.py     # 4.4KB - 快速启动脚本
├── det.onnx               # 2.3MB - 检测模型
├── rec.onnx               # 10MB - 识别模型
├── ppocr_keys_v1.txt      # 26KB - 字符映射
├── simfang.ttf            # 10MB - 字体文件
└── imgs/                  # 测试图片目录
```

## 使用建议

1. **快速开始**: 使用 `python scripts/quick_start.py` 一键启动
2. **开发环境**: 使用 `python tests/simple_test.py` 验证OCR功能
3. **API服务**: 使用 `python simple_api_server.py` 启动服务
4. **功能测试**: 使用 `python tests/test_simple_api.py` 测试API
5. **客户端开发**: 参考 `examples/client_example.py` 的用法
6. **部署**: 确保所有模型文件都在正确位置

## 目录功能说明

### 📁 docs/ - 文档目录
包含项目的所有文档，包括使用说明、项目总结和文件说明。

### 📁 tests/ - 测试目录
包含所有测试文件，用于验证OCR功能和API接口。

### 📁 examples/ - 示例目录
包含使用示例和客户端代码，帮助用户理解如何使用API。

### 📁 scripts/ - 脚本目录
包含自动化脚本，如快速启动脚本，简化用户操作。

### 📁 models/ - 模型目录（建议创建）
建议将模型文件移动到专门的models目录，使结构更清晰。 