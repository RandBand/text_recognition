#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试简单API服务器的功能
"""

import requests
import base64
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_BASE_URL, get_test_images, REQUEST_TIMEOUT, HEALTH_CHECK_TIMEOUT

def image_to_base64(image_path):
    """将图片文件转换为base64字符串"""
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def test_health_check(api_url=f"{API_BASE_URL}/health"):
    """测试健康检查接口"""
    try:
        response = requests.get(api_url, timeout=HEALTH_CHECK_TIMEOUT)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 健康检查通过: {result['message']}")
            return True
        else:
            print(f"❌ 健康检查失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_api_info(api_url=f"{API_BASE_URL}/"):
    """测试API信息接口"""
    try:
        response = requests.get(api_url, timeout=HEALTH_CHECK_TIMEOUT)
        if response.status_code == 200:
            result = response.json()
            print("✅ API信息获取成功:")
            print(f"服务名称: {result['message']}")
            print("可用接口:")
            for endpoint, description in result['endpoints'].items():
                print(f"  {endpoint}: {description}")
            return True
        else:
            print(f"❌ API信息获取失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API信息获取失败: {e}")
        return False

def test_ocr_api(image_path, api_url=f"{API_BASE_URL}/ocr"):
    """测试OCR API"""
    try:
        # 将图片转换为base64
        base64_image = image_to_base64(image_path)
        
        # 准备请求数据
        data = {
            "image": base64_image
        }
        
        # 发送POST请求
        response = requests.post(api_url, json=data, timeout=REQUEST_TIMEOUT)
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"✅ 图片 {image_path} 识别成功!")
                print(f"识别到 {result['data']['text_count']} 个文本区域:")
                
                for i, item in enumerate(result['data']['results']):
                    print(f"  {i+1}. 文本: '{item['text']}'")
                    print(f"     置信度: {item['confidence']:.3f}")
                    print(f"     边界框: ({item['bbox']['xmin']}, {item['bbox']['ymin']}) - ({item['bbox']['xmax']}, {item['bbox']['ymax']})")
                    print(f"     角点坐标: {item['bbox']['points']}")
                    print()
                return True
            else:
                print(f"❌ 图片 {image_path} 识别失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ HTTP请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    print("🚀 开始测试简单OCR API...")
    print("=" * 50)
    
    # 测试健康检查
    print("1. 测试健康检查接口:")
    if not test_health_check():
        print("❌ 健康检查失败，停止测试")
        return
    print()
    
    # 测试API信息
    print("2. 测试API信息接口:")
    if not test_api_info():
        print("❌ API信息获取失败，停止测试")
        return
    print()
    
    # 测试OCR识别
    print("3. 测试OCR识别接口:")
    test_images = get_test_images()
    
    success_count = 0
    for i, image_path in enumerate(test_images, 1):
        if not os.path.exists(image_path):
            print(f"⚠️  图片不存在: {image_path}")
            continue
            
        print(f"测试图片 {i}: {image_path}")
        if test_ocr_api(image_path):
            success_count += 1
        print("-" * 30)
    
    print(f"🎉 测试完成! 成功识别 {success_count}/{len(test_images)} 张图片")

if __name__ == "__main__":
    main() 