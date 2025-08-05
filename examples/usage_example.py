#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR 服务器使用示例
"""

import requests
import base64
import json
import time

def encode_image_to_base64(image_path):
    """将图片文件编码为base64字符串"""
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_ocr_api(server_url="http://localhost:8080"):
    """测试OCR API"""
    
    # 测试健康检查
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{server_url}/health", timeout=5)
        print(f"✅ 健康检查: {response.status_code}")
        print(f"响应: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 健康检查失败: {e}")
        return False
    
    # 测试服务信息
    print("\n📋 获取服务信息...")
    try:
        response = requests.get(f"{server_url}/", timeout=5)
        print(f"✅ 服务信息: {response.status_code}")
        print(f"响应: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 服务信息获取失败: {e}")
    
    # 测试OCR识别（如果有测试图片）
    print("\n🔤 测试OCR识别...")
    test_images = [
        "assets/images/11.jpg",
        "assets/images/12.jpg"
    ]
    
    for image_path in test_images:
        try:
            # 检查文件是否存在
            import os
            if not os.path.exists(image_path):
                print(f"⚠️  测试图片不存在: {image_path}")
                continue
            
            # 编码图片
            base64_image = encode_image_to_base64(image_path)
            
            # 发送OCR请求
            payload = {"image": base64_image}
            response = requests.post(
                f"{server_url}/ocr",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ OCR识别成功: {image_path}")
                print(f"识别到 {result.get('text_count', 0)} 个文本")
                for i, text_result in enumerate(result.get('results', [])):
                    print(f"  文本 {i+1}: {text_result.get('text', '')} (置信度: {text_result.get('confidence', 0):.2f})")
            else:
                print(f"❌ OCR识别失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                
        except Exception as e:
            print(f"❌ 处理图片 {image_path} 时出错: {e}")

def main():
    """主函数"""
    print("🚀 OCR 服务器测试")
    print("=" * 50)
    
    # 检查服务器是否运行
    server_url = "http://localhost:8080"
    
    print(f"📡 连接到服务器: {server_url}")
    
    # 测试API
    test_ocr_api(server_url)
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")

if __name__ == "__main__":
    main() 