#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR API服务快速启动脚本
"""

import os
import sys
import subprocess
import time
import requests

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import (
    SERVER_HOST, SERVER_PORT, API_BASE_URL,
    REQUEST_TIMEOUT, HEALTH_CHECK_TIMEOUT,
    check_required_files, validate_config
)

def check_dependencies():
    """检查必要的文件是否存在"""
    missing_files = check_required_files()
    
    if missing_files:
        print("❌ 缺少必要的文件:")
        for file in missing_files:
            print(f"  - {file}")
        print("\n请确保所有模型文件都在正确的位置。")
        return False
    
    print("✅ 所有必要文件检查通过")
    return True

def test_ocr_function():
    """测试OCR功能"""
    print("🔍 测试OCR功能...")
    try:
        result = subprocess.run([sys.executable, "tests/simple_test.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ OCR功能测试通过")
            return True
        else:
            print("❌ OCR功能测试失败")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ OCR功能测试出错: {e}")
        return False

def start_api_server():
    """启动API服务器"""
    print("🚀 启动API服务器...")
    try:
        # 启动服务器进程
        process = subprocess.Popen([sys.executable, "simple_api_server.py"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务器启动
        time.sleep(3)
        
        # 测试服务器是否正常运行
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=HEALTH_CHECK_TIMEOUT)
            if response.status_code == 200:
                print("✅ API服务器启动成功!")
                print(f"📡 服务地址: {API_BASE_URL}")
                print(f"🔧 健康检查: {API_BASE_URL}/health")
                print(f"📖 API文档: {API_BASE_URL}/")
                return process
            else:
                print("❌ API服务器启动失败")
                process.terminate()
                return None
        except requests.exceptions.RequestException:
            print("❌ 无法连接到API服务器")
            process.terminate()
            return None
            
    except Exception as e:
        print(f"❌ 启动API服务器出错: {e}")
        return None

def test_api_function():
    """测试API功能"""
    print("🧪 测试API功能...")
    try:
        result = subprocess.run([sys.executable, "tests/test_simple_api.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ API功能测试通过")
            return True
        else:
            print("❌ API功能测试失败")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ API功能测试出错: {e}")
        return False

def main():
    print("🚀 OCR API服务快速启动")
    print("=" * 50)
    
    # 检查依赖文件
    if not check_dependencies():
        return
    
    print()
    
    # 测试OCR功能
    if not test_ocr_function():
        print("❌ OCR功能测试失败，停止启动")
        return
    
    print()
    
    # 启动API服务器
    server_process = start_api_server()
    if not server_process:
        print("❌ API服务器启动失败")
        return
    
    print()
    
    # 测试API功能
    if not test_api_function():
        print("⚠️  API功能测试失败，但服务器仍在运行")
    
    print()
    print("🎉 快速启动完成!")
    print("=" * 50)
    print("📋 可用命令:")
    print("  - 启动服务器: python simple_api_server.py")
    print("  - 测试功能: python tests/simple_test.py")
    print("  - 测试API: python tests/test_simple_api.py")
    print("  - 客户端示例: python examples/client_example.py")
    print("=" * 50)
    
    # 保持服务器运行
    try:
        print("按 Ctrl+C 停止服务器")
        server_process.wait()
    except KeyboardInterrupt:
        print("\n👋 正在停止服务器...")
        server_process.terminate()
        server_process.wait()
        print("✅ 服务器已停止")

if __name__ == "__main__":
    main() 