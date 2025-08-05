#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的OCR功能测试
"""

import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import det_rec_functions, filter_box_rec
from config import DET_MODEL_PATH, REC_MODEL_PATH, OCR_KEYS_PATH, get_test_image_path

def test_ocr_function():
    """测试OCR功能"""
    try:
        print("🔍 开始测试OCR功能...")
        
        # 读取测试图片
        image_path = get_test_image_path("1.jpg")
        print(f"📸 读取图片: {image_path}")
        
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ 无法读取图片: {image_path}")
            return False
        
        print(f"✅ 图片读取成功，尺寸: {image.shape}")
        
        # 创建OCR系统
        print("🤖 初始化OCR系统...")
        ocr_system = det_rec_functions(
            image, 
            DET_MODEL_PATH, 
            REC_MODEL_PATH, 
            OCR_KEYS_PATH
        )
        print("✅ OCR系统初始化成功")
        
        # 获取检测框
        print("🔍 开始文字检测...")
        dt_boxes = ocr_system.get_boxes()
        print(f"✅ 检测到 {len(dt_boxes)} 个文字区域")
        
        # 识别文字
        print("📝 开始文字识别...")
        rec_results, rec_results_info = ocr_system.recognition_img(dt_boxes)
        print(f"✅ 识别完成，结果数量: {len(rec_results)}")
        
        # 过滤结果
        dt_boxes, rec_results = filter_box_rec(dt_boxes, rec_results)
        print(f"✅ 过滤后结果数量: {len(rec_results)}")
        
        # 显示结果
        print("\n📊 识别结果:")
        print("=" * 50)
        for i, (box, rec_result) in enumerate(zip(dt_boxes, rec_results)):
            text, score = rec_result
            print(f"文本 {i+1}: '{text}' (置信度: {score:.3f})")
            
            # 计算边界框
            box = box.astype(np.int32)
            xmin = int(np.min(box[:, 0]))
            xmax = int(np.max(box[:, 0]))
            ymin = int(np.min(box[:, 1]))
            ymax = int(np.max(box[:, 1]))
            print(f"  边界框: ({xmin}, {ymin}) - ({xmax}, {ymax})")
        
        print("\n🎉 OCR功能测试成功!")
        return True
        
    except Exception as e:
        print(f"❌ OCR功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_ocr_function() 