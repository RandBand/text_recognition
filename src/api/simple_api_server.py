#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的OCR API服务器
使用Python内置的http.server
"""

import json
import base64
import cv2
import numpy as np
import io
import argparse
import sys
import platform
import os
from PIL import Image
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from src.core.main import det_rec_functions, filter_box_rec
import threading
import time
from src.utils.config import (
    SERVER_HOST, SERVER_PORT, SERVER_DEBUG,
    DET_MODEL_PATH, REC_MODEL_PATH, OCR_KEYS_PATH,
    SUCCESS_RESPONSE, ERROR_RESPONSE,
    REQUEST_TIMEOUT, LOG_FORMAT
)

# 导入编码处理模块
try:
    from src.utils.encoding_utils import setup_windows_encoding
    setup_windows_encoding()
except ImportError:
    # 如果无法导入，使用内联的编码处理
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

class OCRRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理GET请求"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/health':
            self.send_health_response()
        elif path == '/':
            self.send_info_response()
        else:
            self.send_error_response(404, "接口不存在")
    
    def do_POST(self):
        """处理POST请求"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/ocr':
            self.handle_ocr_request()
        else:
            self.send_error_response(404, "接口不存在")
    
    def handle_ocr_request(self):
        """处理OCR识别请求"""
        try:
            # 获取请求内容长度
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error_response(400, "请求体为空")
                return
            
            # 读取请求数据
            post_data = self.rfile.read(content_length)
            
            # 解析JSON数据
            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_error_response(400, "JSON格式错误")
                return
            
            # 检查必要字段
            if 'image' not in data:
                self.send_error_response(400, "缺少image字段")
                return
            
            # 处理base64图片
            base64_image = data['image']
            image = self.base64_to_image(base64_image)
            
            # 执行OCR识别
            results = self.process_image(image)
            
            # 返回结果
            self.send_success_response({
                'text_count': len(results),
                'results': results
            })
            
        except Exception as e:
            self.send_error_response(500, f"服务器内部错误: {str(e)}")
    
    def base64_to_image(self, base64_string):
        """将base64字符串转换为OpenCV图像"""
        try:
            # 移除可能的data:image/jpeg;base64,前缀
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # 解码base64
            image_data = base64.b64decode(base64_string)
            
            # 转换为PIL图像
            image = Image.open(io.BytesIO(image_data))
            
            # 转换为OpenCV格式
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            return image_cv
        except Exception as e:
            raise ValueError(f"Base64解码失败: {e}")
    
    def process_image(self, image):
        """处理图像并返回OCR结果"""
        try:
            # 创建OCR系统实例
            ocr_system = det_rec_functions(
                image, 
                DET_MODEL_PATH, 
                REC_MODEL_PATH, 
                OCR_KEYS_PATH
            )
            
            # 获取检测框
            dt_boxes = ocr_system.get_boxes()
            
            # 识别文本
            rec_results, rec_results_info = ocr_system.recognition_img(dt_boxes)
            
            # 根据置信度过滤结果
            dt_boxes, rec_results = filter_box_rec(dt_boxes, rec_results)
            
            # 格式化结果
            results = []
            for i, (box, rec_result) in enumerate(zip(dt_boxes, rec_results)):
                text, score = rec_result
                
                # 计算边界框坐标
                box = box.astype(np.int32)
                xmin = int(np.min(box[:, 0]))
                xmax = int(np.max(box[:, 0]))
                ymin = int(np.min(box[:, 1]))
                ymax = int(np.max(box[:, 1]))
                
                # 格式化边界框为四个角点坐标
                box_points = box.tolist()
                
                result = {
                    "text": text,
                    "confidence": float(score),
                    "bbox": {
                        "xmin": xmin,
                        "ymin": ymin,
                        "xmax": xmax,
                        "ymax": ymax,
                        "points": box_points  # 四个角点坐标
                    }
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            raise Exception(f"OCR处理失败: {e}")
    
    def send_success_response(self, data):
        """发送成功响应"""
        response = {
            'success': True,
            'data': data
        }
        self.send_json_response(200, response)
    
    def send_error_response(self, status_code, message):
        """发送错误响应"""
        response = {
            'success': False,
            'error': message
        }
        self.send_json_response(status_code, response)
    
    def send_json_response(self, status_code, data):
        """发送JSON响应"""
        response_data = json.dumps(data, ensure_ascii=False, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(response_data.encode('utf-8'))
    
    def send_health_response(self):
        """发送健康检查响应"""
        self.send_json_response(200, SUCCESS_RESPONSE)
    
    def send_info_response(self):
        """发送API信息响应"""
        response = {
            'success': True,
            'message': 'OCR识别API服务',
            'endpoints': {
                'POST /ocr': 'OCR识别接口，需要传入base64编码的图片',
                'GET /health': '健康检查接口',
                'GET /': 'API说明'
            },
            'usage': {
                'method': 'POST',
                'url': '/ocr',
                'content_type': 'application/json',
                'body': {
                    'image': 'base64编码的图片字符串'
                }
            }
        }
        self.send_json_response(200, response)
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def run_server(host=SERVER_HOST, port=SERVER_PORT):
    """运行HTTP服务器"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, OCRRequestHandler)
    
    print(f"🚀 OCR API服务器启动成功!")
    print(f"📡 服务地址: http://{host}:{port}")
    print(f"🔧 健康检查: http://{host}:{port}/health")
    print(f"📖 API文档: http://{host}:{port}/")
    print("=" * 50)
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        httpd.server_close()

def find_available_port(host, start_port, max_attempts=100):
    """查找可用端口"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            if result != 0:  # 端口未被占用
                return port
        except Exception:
            continue
    
    return None

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='OCR API服务器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s                    # 使用默认端口8080
  %(prog)s -p 9000           # 使用端口9000
  %(prog)s --port 9000       # 使用端口9000
  %(prog)s -h 0.0.0.0 -p 9000  # 绑定到所有接口的9000端口
  %(prog)s --help            # 显示帮助信息
        """
    )
    
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=SERVER_PORT,
        help=f'服务器端口号 (默认: {SERVER_PORT})'
    )
    
    parser.add_argument(
        '-H', '--host',
        type=str,
        default=SERVER_HOST,
        help=f'服务器主机地址 (默认: {SERVER_HOST})'
    )
    
    parser.add_argument(
        '--auto-port',
        action='store_true',
        help='自动查找可用端口（当指定端口被占用时）'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='OCR API服务器 v1.0'
    )
    
    return parser.parse_args()

def main():
    """主函数"""
    args = parse_arguments()
    
    # 验证端口号
    if args.port < 1 or args.port > 65535:
        print(f"❌ 错误: 端口号必须在1-65535之间，当前值: {args.port}")
        sys.exit(1)
    
    # 检查端口是否被占用
    port_to_use = args.port
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((args.host, args.port))
        sock.close()
        
        if result == 0:  # 端口被占用
            if args.auto_port:
                print(f"⚠️  端口 {args.port} 已被占用，正在查找可用端口...")
                available_port = find_available_port(args.host, args.port + 1)
                if available_port:
                    port_to_use = available_port
                    print(f"✅ 找到可用端口: {port_to_use}")
                else:
                    print(f"❌ 错误: 在端口 {args.port} 附近未找到可用端口")
                    sys.exit(1)
            else:
                print(f"❌ 错误: 端口 {args.port} 已被占用")
                print(f"💡 提示: 使用 --auto-port 参数自动查找可用端口")
                sys.exit(1)
        else:
            print(f"✅ 端口 {args.port} 可用")
    except Exception as e:
        print(f"⚠️  端口检测失败: {e}")
    
    print(f"🔧 启动配置:")
    print(f"   主机: {args.host}")
    print(f"   端口: {port_to_use}")
    if port_to_use != args.port:
        print(f"   (原指定端口 {args.port} 已被占用)")
    print("=" * 50)
    
    run_server(host=args.host, port=port_to_use)

if __name__ == '__main__':
    main() 