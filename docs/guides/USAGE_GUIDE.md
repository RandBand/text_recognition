# OCR文本识别项目打包使用指南

## 🎉 打包成功！

您的OCR项目已经成功打包为独立的可执行文件，可以分发给其他用户使用。

## 📦 打包结果

### 文件位置
- **分发包**: `dist/ocr_server_package/`
- **压缩包**: `dist/ocr_server_macos.tar.gz` (103MB)

### 包含文件
```
ocr_server_package/
├── ocr_server          # 主程序 (86MB)
├── det.onnx           # 检测模型 (2.3MB)
├── rec.onnx           # 识别模型 (10.2MB)
├── ppocr_keys_v1.txt  # 字符字典 (26KB)
├── simfang.ttf        # 字体文件 (10.1MB)
├── start_server.sh    # 启动脚本(Linux/Mac)
├── start_server.bat   # 启动脚本(Windows)
└── README.txt         # 使用说明
```

## 🚀 使用方法

### 1. 解压文件
```bash
tar -xzf ocr_server_macos.tar.gz
cd ocr_server_package
```

### 2. 启动服务器
**Linux/Mac:**
```bash
./start_server.sh
```

**Windows:**
```cmd
start_server.bat
```

### 3. 测试服务
```bash
# 健康检查
curl http://localhost:8080/health

# 服务器信息
curl http://localhost:8080/
```

## 🔧 API接口

### OCR识别
```bash
curl -X POST http://localhost:8080/ocr \
  -H "Content-Type: application/json" \
  -d '{"image": "base64编码的图片数据"}'
```

### 响应格式
```json
{
  "text_count": 2,
  "results": [
    {
      "text": "识别的文本",
      "confidence": 0.95,
      "bbox": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    }
  ]
}
```

## 📊 性能特点

### 包大小分析
- **总大小**: 109MB
- **主程序**: 86MB (包含Python运行时和所有依赖)
- **模型文件**: 22.5MB
- **其他文件**: 0.5MB

### 优化建议
1. **进一步减小体积**:
   - 使用UPX压缩可执行文件
   - 使用量化后的模型
   - 排除不必要的依赖

2. **提高性能**:
   - 使用GPU加速
   - 优化模型推理
   - 增加缓存机制

## 🔍 故障排除

### 常见问题

**Q1: 启动失败**
```bash
# 检查文件权限
chmod +x ocr_server
chmod +x start_server.sh

# 检查依赖文件
ls -la *.onnx *.txt *.ttf
```

**Q2: 端口被占用**
```bash
# 修改端口
# 编辑 start_server.sh，将端口改为其他值
```

**Q3: 内存不足**
```bash
# 增加系统内存
# 或使用更小的模型
```

### 日志查看
程序运行时会输出详细日志，包括：
- 服务器启动信息
- API请求日志
- 错误信息

## 📋 分发清单

### 必需文件
- [x] `ocr_server` - 主程序
- [x] `det.onnx` - 检测模型
- [x] `rec.onnx` - 识别模型
- [x] `ppocr_keys_v1.txt` - 字符字典
- [x] `simfang.ttf` - 字体文件
- [x] `start_server.sh` - 启动脚本
- [x] `start_server.bat` - Windows启动脚本
- [x] `README.txt` - 使用说明

### 可选文件
- [ ] 示例图片
- [ ] 配置文件
- [ ] 日志目录

## 🎯 下一步计划

### 短期优化
1. **体积优化**: 使用UPX压缩，目标减小到80MB以下
2. **性能优化**: 添加GPU支持，提高推理速度
3. **功能增强**: 添加批量处理、多语言支持

### 长期规划
1. **跨平台**: 为Windows、Linux分别打包
2. **容器化**: 提供Docker镜像
3. **云部署**: 支持云端部署和API服务

## 📞 技术支持

如果遇到问题，请检查：
1. 系统架构是否匹配 (当前为macOS ARM64)
2. 是否有足够的磁盘空间和内存
3. 网络端口是否被占用

## 🎉 恭喜！

您的OCR项目已经成功打包为独立的可执行文件，可以分发给其他用户使用。用户只需要解压文件并运行启动脚本即可使用，无需安装Python环境或任何依赖。 