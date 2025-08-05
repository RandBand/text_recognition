# OCR项目文件结构

## 目录结构

```
text_recognition/
├── src/                          # 源代码目录
│   ├── __init__.py              # 包初始化文件
│   ├── core/                    # 核心功能模块
│   │   ├── __init__.py
│   │   └── main.py             # OCR核心算法
│   ├── api/                     # API服务模块
│   │   ├── __init__.py
│   │   └── simple_api_server.py # HTTP API服务器
│   └── utils/                   # 工具模块
│       ├── __init__.py
│       └── config.py           # 配置文件
├── models/                      # 模型文件目录
│   ├── det.onnx               # 检测模型
│   ├── rec.onnx               # 识别模型
│   └── ppocr_keys_v1.txt     # 字符集文件
├── assets/                     # 资源文件目录
│   ├── fonts/                 # 字体文件
│   │   └── simfang.ttf       # 中文字体
│   └── images/                # 测试图片
│       ├── 1.jpg
│       ├── 11.jpg
│       └── 12.jpg
├── build/                      # 构建相关目录
│   ├── scripts/               # 构建脚本
│   │   ├── build_optimized.py
│   │   ├── build_simple.py
│   │   └── build_script.py
│   ├── configs/               # 构建配置
│   │   └── ocr_server_optimized.spec
│   └── build_optimized/       # 构建临时文件
├── dist/                       # 分发目录
│   └── packages/              # 打包输出
│       └── ocr_minimal/       # 最小化分发包
├── docs/                       # 文档目录
│   ├── guides/                # 使用指南
│   │   ├── README.md
│   │   ├── USAGE_GUIDE.md
│   │   ├── PACKAGING_GUIDE.md
│   │   └── PORT_CUSTOMIZATION_GUIDE.md
│   └── api/                   # API文档
├── tests/                      # 测试目录
│   ├── simple_test.py
│   ├── test_simple_api.py
│   └── test_package.py
├── scripts/                    # 脚本目录
│   └── quick_start.py
├── examples/                   # 示例目录
│   └── client_example.py
├── run_server.py              # 主入口文件
├── requirements.txt           # 依赖文件
└── PROJECT_STRUCTURE.md      # 项目结构说明
```

## 功能模块说明

### 1. 核心模块 (src/core/)
- **main.py**: OCR文本检测和识别的核心算法
- 包含文本检测、文本识别、结果过滤等功能

### 2. API模块 (src/api/)
- **simple_api_server.py**: HTTP API服务器
- 提供RESTful API接口
- 支持端口自定义和自动端口检测

### 3. 工具模块 (src/utils/)
- **config.py**: 项目配置文件
- 统一管理服务器配置、模型路径、API参数等

### 4. 模型文件 (models/)
- **det.onnx**: 文本检测模型
- **rec.onnx**: 文本识别模型
- **ppocr_keys_v1.txt**: 字符集文件

### 5. 资源文件 (assets/)
- **fonts/**: 字体文件目录
- **images/**: 测试图片目录

### 6. 构建系统 (build/)
- **scripts/**: 构建脚本目录
- **configs/**: 构建配置文件
- 支持多种打包方式（简单打包、优化打包等）

### 7. 分发目录 (dist/)
- **packages/**: 打包输出目录
- 包含可执行文件和必要的资源文件

### 8. 文档 (docs/)
- **guides/**: 使用指南和说明文档
- **api/**: API文档和接口说明

## 主要功能

### 1. OCR文本识别
- 支持多种图片格式
- 高精度文本检测和识别
- 支持多语言文本

### 2. HTTP API服务
- RESTful API接口
- 支持端口自定义
- 自动端口占用检测
- 健康检查和状态监控

### 3. 打包分发
- 支持多种打包方式
- 优化包大小
- 跨平台支持
- 一键部署

### 4. 开发工具
- 完整的测试套件
- 示例代码
- 详细文档
- 快速启动脚本

## 使用方式

### 开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
python run_server.py

# 使用自定义端口
python run_server.py -p 9000

# 自动端口检测
python run_server.py -p 8080 --auto-port
```

### 生产环境
```bash
# 构建优化版本
python build/scripts/build_optimized.py

# 运行打包后的程序
cd dist/packages/ocr_minimal
./start.sh -p 9000
```

## 文件命名规范

### 1. Python文件
- 使用小写字母和下划线
- 模块名使用描述性名称
- 主入口文件使用动词+名词

### 2. 目录命名
- 使用小写字母
- 使用描述性名称
- 避免缩写和特殊字符

### 3. 配置文件
- 使用有意义的名称
- 包含版本信息
- 使用标准格式（.spec, .py等）

## 版本控制

### 忽略文件
- 构建输出目录 (dist/, build/)
- 临时文件 (__pycache__/)
- 系统文件 (.DS_Store)
- 日志文件 (*.log)

### 跟踪文件
- 源代码文件
- 配置文件
- 文档文件
- 模型文件（小文件）

## 维护说明

### 1. 添加新功能
- 在相应的模块目录下创建新文件
- 更新__init__.py文件
- 添加相应的测试和文档

### 2. 修改配置
- 更新src/utils/config.py
- 同步更新构建脚本中的路径
- 更新相关文档

### 3. 更新依赖
- 修改requirements.txt
- 测试兼容性
- 更新构建脚本

### 4. 发布新版本
- 更新版本号
- 重新构建包
- 更新文档
- 创建发布说明 