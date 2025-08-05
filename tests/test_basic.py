#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本测试文件
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestBasicFunctionality(unittest.TestCase):
    """基本功能测试"""
    
    def test_imports(self):
        """测试模块导入"""
        try:
            from src.utils.config import SERVER_HOST, SERVER_PORT
            self.assertEqual(SERVER_HOST, "localhost")
            self.assertEqual(SERVER_PORT, 8080)
        except ImportError as e:
            self.fail(f"导入失败: {e}")
    
    def test_config_validation(self):
        """测试配置验证"""
        try:
            from src.utils.config import validate_config
            errors = validate_config()
            # 如果模型文件不存在，这是正常的
            # 我们只测试函数能正常运行
            self.assertIsInstance(errors, list)
        except ImportError as e:
            self.fail(f"配置验证失败: {e}")
    
    def test_required_files_check(self):
        """测试必需文件检查"""
        try:
            from src.utils.config import check_required_files
            missing_files = check_required_files()
            self.assertIsInstance(missing_files, list)
        except ImportError as e:
            self.fail(f"文件检查失败: {e}")

if __name__ == '__main__':
    unittest.main() 