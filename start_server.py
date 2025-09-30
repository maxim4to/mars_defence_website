#!/usr/bin/env python3
"""
Простой HTTP сервер для запуска сайта Mars Defence
Использование: python start_server.py
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем CORS заголовки для локальной разработки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    """Запускает локальный HTTP сервер"""
    try:
        # Переходим в директорию со скриптом
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Mars Defence Server запущен!")
            print(f"📱 Откройте браузер и перейдите по адресу: http://localhost:{PORT}")
            print(f"📁 Сервер работает в директории: {os.getcwd()}")
            print(f"⏹️  Для остановки нажмите Ctrl+C")
            print("-" * 50)
            
            # Автоматически открываем браузер
            try:
                webbrowser.open(f'http://localhost:{PORT}')
                print("🌐 Браузер открыт автоматически")
            except:
                print("⚠️  Не удалось открыть браузер автоматически")
            
            print("-" * 50)
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Порт {PORT} уже используется. Попробуйте другой порт:")
            print(f"   python start_server.py --port 8001")
        else:
            print(f"❌ Ошибка запуска сервера: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--port":
        try:
            PORT = int(sys.argv[2])
        except (IndexError, ValueError):
            print("❌ Неверный формат порта. Используйте: --port 8000")
            sys.exit(1)
    
    start_server()
