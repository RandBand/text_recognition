#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR服务器启动入口
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.simple_api_server import main

if __name__ == '__main__':
    main() 