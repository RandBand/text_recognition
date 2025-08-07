
# macOS运行时钩子 - 解决模块导入问题
import sys
import os

# 设置环境变量
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

# 等待PyInstaller引导程序完全初始化
def wait_for_pyinstaller_init():
    """等待PyInstaller引导程序完全初始化"""
    import time
    max_wait = 10  # 最多等待10秒
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            # 检查PyInstaller引导程序是否已初始化
            if hasattr(sys, '_pyinstaller_pyz'):
                return True
            time.sleep(0.1)
        except Exception:
            time.sleep(0.1)
    
    return False

# 确保ipaddress模块可用
try:
    import ipaddress
except ImportError:
    # 如果ipaddress不可用，创建一个简单的替代
    class IPv4Address:
        def __init__(self, address):
            self.address = address
        def __str__(self):
            return self.address
    
    class IPv4Network:
        def __init__(self, network):
            self.network = network
        def __str__(self):
            return self.network
    
    class ipaddress:
        IPv4Address = IPv4Address
        IPv4Network = IPv4Network

# 确保pathlib模块可用
try:
    import pathlib
except ImportError:
    pass

# 确保urllib模块可用
try:
    import urllib
    import urllib.parse
    import urllib.request
    import urllib.error
    import urllib.response
except ImportError:
    pass

# 确保zipimport模块可用
try:
    import zipimport
except ImportError:
    pass

# 确保其他必要的模块可用
try:
    import codecs
    import locale
    import builtins
    import collections
    import collections.abc
    import typing
    import importlib
    import importlib.machinery
    import importlib.util
except ImportError:
    pass

# 修复sys.modules中的模块引用
def fix_module_references():
    """修复sys.modules中的模块引用"""
    try:
        # 确保ipaddress在sys.modules中
        if 'ipaddress' not in sys.modules:
            sys.modules['ipaddress'] = ipaddress
        
        # 确保其他必要模块在sys.modules中
        for module_name in ['pathlib', 'urllib', 'urllib.parse', 'urllib.request', 
                           'urllib.error', 'urllib.response', 'codecs', 'locale', 
                           'builtins', 'collections', 'collections.abc', 'typing',
                           'importlib', 'importlib.machinery', 'importlib.util', 'zipimport']:
            if module_name not in sys.modules:
                try:
                    __import__(module_name)
                except ImportError:
                    pass
    except Exception:
        pass

# 等待PyInstaller初始化完成后再执行修复
if wait_for_pyinstaller_init():
    fix_module_references()
else:
    # 如果等待超时，仍然尝试修复，但更小心
    try:
        fix_module_references()
    except Exception:
        pass
