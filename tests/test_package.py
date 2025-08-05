#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
打包测试脚本
用于验证打包后的程序是否正常工作
"""

import os
import sys
import time
import requests
import subprocess
import json
import base64
from pathlib import Path
from PIL import Image
import io

def test_executable_exists():
    """测试可执行文件是否存在"""
    print("🔍 检查可执行文件...")
    
    # 检查标准打包
    standard_path = Path("dist/ocr_server_package/ocr_server")
    if standard_path.exists():
        print(f"✅ 标准打包文件存在: {standard_path}")
        return standard_path
    
    # 检查优化打包
    optimized_path = Path("dist_optimized/ocr_minimal/ocr_server")
    if optimized_path.exists():
        print(f"✅ 优化打包文件存在: {optimized_path}")
        return optimized_path
    
    print("❌ 未找到可执行文件")
    return None

def create_test_image():
    """创建测试图片"""
    print("🖼️  创建测试图片...")
    
    # 创建一个简单的测试图片
    img = Image.new('RGB', (200, 100), color='white')
    draw = ImageDraw.Draw(img)
    
    # 添加一些文字
    try:
        from PIL import ImageFont
        font = ImageFont.load_default()
        draw.text((10, 40), "Hello World", fill='black', font=font)
    except:
        # 如果没有字体，就画一些简单的图形
        draw.rectangle([10, 10, 190, 90], outline='black', width=2)
        draw.text((50, 40), "TEST", fill='black')
    
    # 保存为base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_data = buffer.getvalue()
    base64_img = base64.b64encode(img_data).decode('utf-8')
    
    print("✅ 测试图片创建完成")
    return base64_img

def start_server(executable_path):
    """启动服务器"""
    print("🚀 启动OCR服务器...")
    
    try:
        # 切换到可执行文件所在目录
        os.chdir(executable_path.parent)
        
        # 启动服务器进程
        process = subprocess.Popen(
            [str(executable_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待服务器启动
        time.sleep(3)
        
        # 检查进程是否还在运行
        if process.poll() is None:
            print("✅ 服务器启动成功")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ 服务器启动失败:")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 启动服务器时出错: {e}")
        return None

def test_health_check():
    """测试健康检查接口"""
    print("🏥 测试健康检查接口...")
    
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ 健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查出错: {e}")
        return False

def test_ocr_api():
    """测试OCR API接口"""
    print("🔤 测试OCR API接口...")
    
    try:
        # 创建测试图片
        test_image = create_test_image()
        
        # 发送OCR请求
        data = {"image": test_image}
        response = requests.post(
            "http://localhost:8080/ocr",
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ OCR API测试通过")
            print(f"📊 识别结果: {result}")
            return True
        else:
            print(f"❌ OCR API测试失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OCR API测试出错: {e}")
        return False

def test_info_api():
    """测试信息接口"""
    print("ℹ️  测试信息接口...")
    
    try:
        response = requests.get("http://localhost:8080/", timeout=5)
        if response.status_code == 200:
            print("✅ 信息接口测试通过")
            return True
        else:
            print(f"❌ 信息接口测试失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 信息接口测试出错: {e}")
        return False

def stop_server(process):
    """停止服务器"""
    if process:
        print("🛑 停止服务器...")
        process.terminate()
        try:
            process.wait(timeout=5)
            print("✅ 服务器已停止")
        except subprocess.TimeoutExpired:
            process.kill()
            print("⚠️  强制停止服务器")

def main():
    """主测试函数"""
    print("🧪 OCR打包测试工具")
    print("=" * 50)
    
    # 1. 检查可执行文件
    executable_path = test_executable_exists()
    if not executable_path:
        print("❌ 请先运行打包脚本")
        return 1
    
    # 2. 启动服务器
    process = start_server(executable_path)
    if not process:
        return 1
    
    try:
        # 3. 测试各个接口
        tests = [
            ("健康检查", test_health_check),
            ("信息接口", test_info_api),
            ("OCR API", test_ocr_api),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 测试: {test_name}")
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        
        # 4. 输出测试结果
        print(f"\n📊 测试结果: {passed}/{total} 通过")
        
        if passed == total:
            print("🎉 所有测试通过! 打包成功!")
            return 0
        else:
            print("⚠️  部分测试失败，请检查打包配置")
            return 1
            
    finally:
        # 5. 停止服务器
        stop_server(process)

if __name__ == "__main__":
    sys.exit(main()) 