#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR API客户端示例
演示如何使用OCR API进行文字识别
"""

import requests
import base64
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image
import io
from config import API_BASE_URL, get_test_images, REQUEST_TIMEOUT, HEALTH_CHECK_TIMEOUT

class OCRClient:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url.rstrip('/')
    
    def image_to_base64(self, image_path):
        """将图片文件转换为base64字符串"""
        try:
            with open(image_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
        except Exception as e:
            raise Exception(f"图片转换失败: {e}")
    
    def pil_to_base64(self, pil_image):
        """将PIL图像转换为base64字符串"""
        try:
            # 将PIL图像转换为字节流
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # 转换为base64
            encoded_string = base64.b64encode(img_byte_arr).decode('utf-8')
            return encoded_string
        except Exception as e:
            raise Exception(f"PIL图像转换失败: {e}")
    
    def recognize_text(self, image_input):
        """
        识别图片中的文字
        
        Args:
            image_input: 可以是图片路径(str)或PIL图像对象
            
        Returns:
            dict: 识别结果
        """
        try:
            # 处理不同类型的输入
            if isinstance(image_input, str):
                # 图片路径
                base64_image = self.image_to_base64(image_input)
            elif hasattr(image_input, 'save'):
                # PIL图像对象
                base64_image = self.pil_to_base64(image_input)
            else:
                raise ValueError("不支持的输入类型，请提供图片路径或PIL图像对象")
            
            # 准备请求数据
            data = {"image": base64_image}
            
            # 发送请求
            response = requests.post(f"{self.base_url}/ocr", json=data, timeout=REQUEST_TIMEOUT)
            
            # 检查响应
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    return result['data']
                else:
                    raise Exception(f"OCR识别失败: {result.get('error', '未知错误')}")
            else:
                raise Exception(f"HTTP请求失败，状态码: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"识别过程出错: {e}")
    
    def health_check(self):
        """检查服务健康状态"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=HEALTH_CHECK_TIMEOUT)
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "error": f"状态码: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

def print_results(results):
    """打印识别结果"""
    print(f"📊 识别到 {results['text_count']} 个文本区域:")
    print("=" * 50)
    
    for i, item in enumerate(results['results'], 1):
        print(f"🔍 文本 {i}:")
        print(f"   内容: '{item['text']}'")
        print(f"   置信度: {item['confidence']:.3f}")
        print(f"   边界框: ({item['bbox']['xmin']}, {item['bbox']['ymin']}) - ({item['bbox']['xmax']}, {item['bbox']['ymax']})")
        print(f"   角点坐标: {item['bbox']['points']}")
        print("-" * 30)

def main():
    # 创建客户端
    client = OCRClient()
    
    print("🔍 OCR文字识别客户端示例")
    print("=" * 50)
    
    # 检查服务状态
    print("1. 检查服务状态...")
    health = client.health_check()
    if health['success']:
        print(f"✅ {health['message']}")
    else:
        print(f"❌ 服务不可用: {health.get('error', '未知错误')}")
        return
    
    print()
    
    # 测试图片列表
    test_images = get_test_images()
    
    # 识别每张图片
    for i, image_path in enumerate(test_images, 1):
        if not os.path.exists(image_path):
            print(f"⚠️  图片不存在: {image_path}")
            continue
            
        print(f"2.{i} 识别图片: {image_path}")
        try:
            results = client.recognize_text(image_path)
            print_results(results)
        except Exception as e:
            print(f"❌ 识别失败: {e}")
        
        print()

if __name__ == "__main__":
    main() 