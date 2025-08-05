#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR API服务配置文件
统一管理所有配置项
"""

import os

# ==================== 服务器配置 ====================
# API服务器配置
SERVER_HOST = "localhost"
SERVER_PORT = 8080
SERVER_DEBUG = False

# API基础URL
API_BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"

# ==================== 模型配置 ====================
# 模型文件路径
DET_MODEL_PATH = "models/det.onnx"
REC_MODEL_PATH = "models/rec.onnx"
OCR_KEYS_PATH = "models/ppocr_keys_v1.txt"
FONT_PATH = "assets/fonts/simfang.ttf"

# ==================== 测试配置 ====================
# 测试图片目录
TEST_IMAGES_DIR = "assets/images"
# 测试图片列表
TEST_IMAGES = [
    "1.jpg",
    "11.jpg", 
    "12.jpg"
]

# ==================== OCR配置 ====================
# OCR检测参数
DET_DB_THRESH = 0.3
DET_DB_BOX_THRESH = 0.5
MAX_CANDIDATES = 2000
UNCLIP_RATIO = 1.6
USE_DILATION = True

# OCR识别参数
DROP_SCORE = 0.5

# ==================== 路径配置 ====================
# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 获取测试图片的完整路径
def get_test_image_path(filename):
    """获取测试图片的完整路径"""
    return os.path.join(PROJECT_ROOT, TEST_IMAGES_DIR, filename)

def get_test_images():
    """获取所有测试图片的完整路径"""
    return [get_test_image_path(img) for img in TEST_IMAGES]

# ==================== API端点配置 ====================
# API端点
ENDPOINTS = {
    "ocr": "/ocr",
    "health": "/health",
    "info": "/"
}

# 获取完整的API URL
def get_api_url(endpoint):
    """获取完整的API URL"""
    return f"{API_BASE_URL}{ENDPOINTS.get(endpoint, endpoint)}"

# ==================== 日志配置 ====================
# 日志格式
LOG_FORMAT = "[{time}] {message}"
LOG_LEVEL = "INFO"

# ==================== 超时配置 ====================
# 请求超时时间（秒）
REQUEST_TIMEOUT = 30
HEALTH_CHECK_TIMEOUT = 5

# ==================== 响应配置 ====================
# 成功响应格式
SUCCESS_RESPONSE = {
    "success": True,
    "message": "OCR服务运行正常"
}

# 错误响应格式
ERROR_RESPONSE = {
    "success": False,
    "error": "未知错误"
}

# ==================== 验证配置 ====================
# 必需的文件列表
REQUIRED_FILES = [
    DET_MODEL_PATH,
    REC_MODEL_PATH,
    OCR_KEYS_PATH,
    FONT_PATH
]

def check_required_files():
    """检查必需的文件是否存在"""
    missing_files = []
    for file_path in REQUIRED_FILES:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    return missing_files

# ==================== 配置验证 ====================
def validate_config():
    """验证配置的有效性"""
    errors = []
    
    # 检查端口范围
    if not (1024 <= SERVER_PORT <= 65535):
        errors.append(f"端口 {SERVER_PORT} 不在有效范围内 (1024-65535)")
    
    # 检查必需文件
    missing_files = check_required_files()
    if missing_files:
        errors.append(f"缺少必需文件: {', '.join(missing_files)}")
    
    return errors

# ==================== 配置信息 ====================
def get_config_info():
    """获取配置信息"""
    return {
        "server": {
            "host": SERVER_HOST,
            "port": SERVER_PORT,
            "debug": SERVER_DEBUG,
            "base_url": API_BASE_URL
        },
        "models": {
            "det_model": DET_MODEL_PATH,
            "rec_model": REC_MODEL_PATH,
            "ocr_keys": OCR_KEYS_PATH,
            "font": FONT_PATH
        },
        "test": {
            "images_dir": TEST_IMAGES_DIR,
            "images": TEST_IMAGES
        },
        "ocr": {
            "det_db_thresh": DET_DB_THRESH,
            "det_db_box_thresh": DET_DB_BOX_THRESH,
            "max_candidates": MAX_CANDIDATES,
            "unclip_ratio": UNCLIP_RATIO,
            "use_dilation": USE_DILATION,
            "drop_score": DROP_SCORE
        }
    }

if __name__ == "__main__":
    # 验证配置
    errors = validate_config()
    if errors:
        print("❌ 配置验证失败:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ 配置验证通过")
        print("\n📋 配置信息:")
        import json
        print(json.dumps(get_config_info(), indent=2, ensure_ascii=False)) 