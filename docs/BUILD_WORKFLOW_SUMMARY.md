# OCR服务器构建工作流总结

## 概述

本项目已配置完整的GitHub Actions工作流，用于自动构建OCR服务器的多平台可执行文件。

## 支持的平台

- **macOS ARM64** (Apple Silicon)
- **macOS x86_64** (Intel)
- **Windows x64** (Intel/AMD)
- **Windows ARM64**

## 构建方式

### 1. GitHub Actions自动构建

#### 触发方式：
- **版本标签推送**: `git tag v1.0.0 && git push origin v1.0.0`
- **手动触发**: 在GitHub Actions页面手动运行

#### 构建脚本：
使用 `build/scripts/build_optimized.py` 进行优化构建

### 2. 本地构建测试

#### 快速构建：
```bash
# 使用快速构建脚本
./scripts/quick_build.sh

# 或使用Python脚本
python scripts/build_local.py
```

#### 手动构建：
```bash
# 安装依赖
pip install -r models/requirements.txt
pip install pyinstaller==5.13.2

# 运行优化构建脚本
python build/scripts/build_optimized.py
```

## 构建产物

### 文件位置：
- **可执行文件**: `dist/packages/ocr_server` (macOS/Linux) 或 `dist/packages/ocr_server.exe` (Windows)
- **发布包**: 根据平台生成相应的压缩包

### 命名规则：
- macOS ARM64: `ocr_server_macos_arm64_v1.0.0.tar.gz`
- macOS x86_64: `ocr_server_macos_x86_64_v1.0.0.tar.gz`
- Windows x64: `ocr_server_windows_x64_v1.0.0.zip`
- Windows ARM64: `ocr_server_windows_arm64_v1.0.0.zip`

## 优化特性

### 1. 体积优化
- 排除不必要的模块 (matplotlib, scipy, pandas等)
- 使用UPX压缩 (macOS)
- 移除调试信息 (strip)

### 2. 依赖管理
- 精确的隐藏导入配置
- 自动包含必要的数据文件
- 最小化依赖包

### 3. 跨平台支持
- 自动检测平台架构
- 适配不同操作系统的构建参数
- 统一的构建流程

## 工作流步骤

### 1. 环境准备
```yaml
- 检出代码
- 设置Python环境 (3.9)
- 安装系统依赖
- 安装Python依赖
```

### 2. 构建过程
```yaml
- 运行优化构建脚本
- 生成可执行文件
- 重命名并整理输出
```

### 3. 打包发布
```yaml
- 创建压缩包
- 上传构建产物
- 创建GitHub Release (版本标签触发)
```

## 使用说明

### 1. 运行可执行文件
```bash
# macOS/Linux
./ocr_server

# Windows
ocr_server.exe

# 指定端口
./ocr_server -p 9000
```

### 2. 服务访问
- 默认端口: 5000
- API端点: `http://localhost:5000/ocr`
- 支持图片上传和OCR识别

## 故障排除

### 常见问题：

1. **构建失败**
   - 检查必要文件是否存在
   - 确认Python版本兼容性
   - 查看构建日志

2. **可执行文件过大**
   - 检查模块排除配置
   - 确认UPX压缩是否生效

3. **运行时错误**
   - 确认数据文件已包含
   - 检查隐藏导入配置

### 调试命令：
```bash
# 检查文件大小
ls -lh dist/packages/

# 测试可执行文件
./dist/packages/ocr_server --help

# 查看构建日志
python build/scripts/build_optimized.py
```

## 版本管理

### 发布流程：
1. 更新代码并提交
2. 创建版本标签: `git tag v1.0.0`
3. 推送标签: `git push origin v1.0.0`
4. 等待GitHub Actions完成构建
5. 检查GitHub Release页面

### 版本号规范：
- 使用语义化版本号 (如: 1.0.0, 1.1.0, 2.0.0)
- 标签格式: `v1.0.0`
- 构建产物自动包含版本号

## 配置说明

### 修改构建参数：
- 编辑 `build/scripts/build_optimized.py`
- 修改 `build/configs/ocr_server_optimized.spec`
- 调整隐藏导入和排除模块

### 自定义输出：
- 修改可执行文件名称
- 调整输出目录结构
- 添加图标或元数据

## 性能优化

### 构建优化：
- 并行构建多个平台
- 缓存依赖安装
- 增量构建支持

### 运行时优化：
- 内存使用优化
- 启动时间优化
- 模型加载优化

## 安全考虑

1. **依赖安全**: 定期更新requirements.txt
2. **代码签名**: 考虑为macOS构建添加签名
3. **权限控制**: 确保GitHub Actions权限合理
4. **敏感信息**: 避免在构建中暴露敏感数据

## 联系支持

如遇问题：
1. 检查GitHub Actions日志
2. 查看故障排除部分
3. 在项目Issues中报告问题
4. 提供详细的错误信息 