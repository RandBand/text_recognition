# OCR项目打包指南

## 概述

本项目提供了两种打包方案，用于将OCR文本识别项目打包为独立的可执行文件，方便分发给其他用户使用。

## 打包方案

### 方案1：标准打包（推荐新手）

使用 `build_script.py` 进行标准打包：

```bash
python build_script.py
```

**特点：**
- 包含完整的依赖和文档
- 适合大多数用户
- 包含详细的使用说明

### 方案2：优化打包（推荐生产环境）

使用 `build_optimized.py` 进行体积优化打包：

```bash
python build_optimized.py
```

**特点：**
- 大幅减小包体积
- 排除不必要的依赖
- 使用UPX压缩（如果可用）

## 打包前准备

### 1. 检查必需文件

确保以下文件存在于项目根目录：
- `det.onnx` - 文本检测模型
- `rec.onnx` - 文本识别模型  
- `ppocr_keys_v1.txt` - 字符字典
- `simfang.ttf` - 字体文件
- `simple_api_server.py` - 主程序

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 测试程序

确保程序能正常运行：

```bash
python simple_api_server.py
```

## 打包过程

### 步骤1：运行打包脚本

```bash
# 标准打包
python build_script.py

# 或优化打包
python build_optimized.py
```

### 步骤2：检查输出

打包完成后，会在以下位置生成文件：

**标准打包：**
- `dist/ocr_server_package/` - 完整分发包

**优化打包：**
- `dist_optimized/ocr_minimal/` - 最小化分发包

### 步骤3：测试可执行文件

```bash
# 进入分发包目录
cd dist/ocr_server_package  # 或 dist_optimized/ocr_minimal

# 启动服务器
./start_server.sh  # Linux/Mac
# 或
start_server.bat   # Windows
```

## 分发包内容

### 标准分发包
```
ocr_server_package/
├── ocr_server          # 主程序
├── det.onnx           # 检测模型
├── rec.onnx           # 识别模型
├── ppocr_keys_v1.txt  # 字符字典
├── simfang.ttf        # 字体文件
├── start_server.sh    # 启动脚本(Linux/Mac)
├── start_server.bat   # 启动脚本(Windows)
└── README.txt         # 使用说明
```

### 最小化分发包
```
ocr_minimal/
├── ocr_server         # 主程序
├── det.onnx          # 检测模型
├── rec.onnx          # 识别模型
├── ppocr_keys_v1.txt # 字符字典
├── simfang.ttf       # 字体文件
├── start.sh          # 启动脚本(Linux/Mac)
└── start.bat         # 启动脚本(Windows)
```

## 体积优化技巧

### 1. 使用UPX压缩

安装UPX可以进一步减小可执行文件大小：

**macOS:**
```bash
brew install upx
```

**Ubuntu/Debian:**
```bash
sudo apt-get install upx
```

**Windows:**
下载UPX并添加到PATH环境变量。

### 2. 排除不必要的模块

优化脚本已经排除了以下模块：
- 图形界面库（tkinter, PyQt等）
- 科学计算库（matplotlib, scipy等）
- 开发工具（jupyter, IPython等）
- 测试模块（unittest, doctest等）

### 3. 模型文件优化

如果可能，可以考虑：
- 使用量化后的模型文件
- 压缩模型文件（但可能影响性能）
- 使用更小的模型

## 常见问题

### Q1: 打包失败怎么办？

**解决方案：**
1. 检查Python环境是否正确
2. 确保所有依赖已安装
3. 检查必需文件是否存在
4. 查看错误日志定位问题

### Q2: 可执行文件太大怎么办？

**解决方案：**
1. 使用优化打包脚本
2. 安装UPX进行压缩
3. 检查是否包含了不必要的文件
4. 考虑使用更小的模型文件

### Q3: 在其他电脑上运行失败？

**解决方案：**
1. 确保目标系统架构匹配
2. 检查系统依赖（如glibc版本）
3. 尝试在相同操作系统上打包
4. 使用Docker容器进行打包

### Q4: 如何减小模型文件大小？

**解决方案：**
1. 使用模型量化技术
2. 使用更小的模型架构
3. 压缩模型文件（可能影响性能）
4. 考虑使用在线模型服务

## 性能优化建议

### 1. 运行时优化
- 使用SSD存储模型文件
- 增加系统内存
- 使用GPU加速（如果支持）

### 2. 模型优化
- 使用量化模型
- 使用更小的模型
- 使用模型剪枝技术

### 3. 系统优化
- 关闭不必要的系统服务
- 优化系统内存使用
- 使用性能模式

## 分发建议

### 1. 文件压缩
使用7z或zip压缩分发包：
```bash
7z a ocr_server.zip dist/ocr_server_package/
```

### 2. 版本管理
- 为每个版本创建标签
- 记录版本变更
- 提供回滚方案

### 3. 用户文档
- 提供详细的使用说明
- 包含常见问题解答
- 提供技术支持联系方式

## 安全注意事项

### 1. 代码安全
- 不要包含敏感信息
- 使用安全的依赖版本
- 定期更新依赖

### 2. 分发安全
- 验证下载文件的完整性
- 使用HTTPS分发
- 提供数字签名

### 3. 运行时安全
- 限制文件访问权限
- 使用安全的网络配置
- 监控异常行为 