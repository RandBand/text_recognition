#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
编码处理工具模块
解决Windows下的UnicodeEncodeError问题
"""

import platform
import sys
import os

def setup_windows_encoding():
    """设置Windows环境下的编码处理"""
    if platform.system() == 'Windows':
        import codecs
        import locale
        
        # 尝试设置控制台编码为UTF-8
        try:
            # 设置环境变量
            os.environ['PYTHONIOENCODING'] = 'utf-8'
            
            # 重新配置stdout和stderr
            if hasattr(sys.stdout, 'detach'):
                sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
            if hasattr(sys.stderr, 'detach'):
                sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
            
            # 设置locale
            if hasattr(locale, 'setlocale'):
                try:
                    locale.setlocale(locale.LC_ALL, 'C.UTF-8')
                except locale.Error:
                    try:
                        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
                    except locale.Error:
                        pass
        except Exception:
            # 如果设置失败，使用安全的打印函数
            setup_safe_print()

def setup_safe_print():
    """设置安全的打印函数"""
    def safe_print(*args, **kwargs):
        try:
            print(*args, **kwargs)
        except UnicodeEncodeError:
            # 如果出现编码错误，尝试使用ASCII编码
            for arg in args:
                try:
                    print(str(arg).encode('ascii', 'replace').decode('ascii'), end=' ')
                except:
                    print('[编码错误]', end=' ')
            print()
    
    # 替换print函数
    import builtins
    builtins.print = safe_print

def safe_print(*args, **kwargs):
    """安全的打印函数，处理编码错误"""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # 如果出现编码错误，尝试使用ASCII编码
        for arg in args:
            try:
                print(str(arg).encode('ascii', 'replace').decode('ascii'), end=' ')
            except:
                print('[编码错误]', end=' ')
        print()

# 在模块导入时自动设置编码
setup_windows_encoding() 