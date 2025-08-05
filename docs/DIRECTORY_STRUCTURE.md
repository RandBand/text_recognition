# 项目目录结构说明

## 📁 整体结构

```
text_recognition/
├── main.py                    # OCR核心功能
├── simple_api_server.py       # API服务器主文件
├── requirements.txt           # Python依赖
├── README.md                 # 项目入口文档
├── docs/                     # 📚 文档目录
├── tests/                    # 🧪 测试目录
├── examples/                 # 💡 示例目录
├── scripts/                  # 🔧 脚本目录
├── imgs/                     # 🖼️ 测试图片目录
├── det.onnx                 # 🤖 检测模型
├── rec.onnx                 # 🤖 识别模型
├── ppocr_keys_v1.txt        # 📝 字符映射文件
└── simfang.ttf              # 🔤 字体文件
```

## 📚 docs/ - 文档目录

```
docs/
├── README.md            # 详细使用说明
├── PROJECT_SUMMARY.md   # 项目总结
├── FILES.md             # 文件说明
└── DIRECTORY_STRUCTURE.md # 本文件
```

**功能**: 包含项目的所有文档，为用户提供完整的使用指南和技术说明。

## 🧪 tests/ - 测试目录

```
tests/
├── simple_test.py       # OCR功能测试
└── test_simple_api.py   # API接口测试
```

**功能**: 包含所有测试文件，用于验证OCR功能和API接口的正确性。

## 💡 examples/ - 示例目录

```
examples/
└── client_example.py    # 客户端使用示例
```

**功能**: 包含使用示例和客户端代码，帮助用户理解如何使用API。

## 🔧 scripts/ - 脚本目录

```
scripts/
└── quick_start.py       # 快速启动脚本
```

**功能**: 包含自动化脚本，简化用户操作，提供一键启动功能。

## 🖼️ imgs/ - 测试图片目录

```
imgs/
├── 1.jpg               # 测试图片1
├── 11.jpg              # 测试图片2
├── 12.jpg              # 测试图片3
└── ...                 # 其他测试图片
```

**功能**: 包含各种测试图片，用于验证OCR功能。

## 🤖 模型文件

```
├── det.onnx            # 文字检测模型 (2.3MB)
├── rec.onnx            # 文字识别模型 (10MB)
├── ppocr_keys_v1.txt   # 字符映射文件 (26KB)
└── simfang.ttf         # 字体文件 (10MB)
```

**功能**: 包含OCR识别所需的所有模型文件和配置。

## 📋 核心文件

```
├── main.py                    # OCR核心功能 (25KB)
├── simple_api_server.py       # API服务器主文件 (7.6KB)
├── requirements.txt           # Python依赖 (135B)
└── README.md                 # 项目入口文档 (3.5KB)
```

**功能**: 项目的核心功能文件，包含OCR处理和API服务。

## 🎯 目录设计原则

### 1. 功能分离
- **docs/**: 所有文档集中管理
- **tests/**: 所有测试文件集中管理
- **examples/**: 所有示例代码集中管理
- **scripts/**: 所有脚本文件集中管理

### 2. 清晰命名
- 每个目录都有明确的英文名称
- 文件名使用下划线分隔，便于阅读
- 目录名使用复数形式，表示包含多个文件

### 3. 层次结构
- 根目录只保留核心文件
- 按功能分类组织文件
- 避免文件散乱分布

### 4. 易于维护
- 相关文件集中存放
- 便于查找和管理
- 支持团队协作开发

## 🚀 使用建议

### 新用户
1. 阅读 `README.md` 了解项目
2. 运行 `python scripts/quick_start.py` 快速启动
3. 查看 `docs/` 目录获取详细文档

### 开发者
1. 查看 `tests/` 目录了解测试用例
2. 参考 `examples/` 目录的示例代码
3. 使用 `scripts/` 目录的自动化脚本

### 部署者
1. 确保所有模型文件在正确位置
2. 检查 `requirements.txt` 安装依赖
3. 使用 `simple_api_server.py` 启动服务

## 📊 文件统计

| 目录 | 文件数量 | 主要功能 |
|------|----------|----------|
| docs/ | 4 | 文档管理 |
| tests/ | 2 | 功能测试 |
| examples/ | 1 | 使用示例 |
| scripts/ | 1 | 自动化脚本 |
| imgs/ | 20 | 测试图片 |
| 根目录 | 8 | 核心文件 |

**总计**: 36个文件，6个目录 