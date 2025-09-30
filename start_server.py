#!/usr/bin/env python3
"""
Simple HTTP server for running Mars Defence website
Usage: python start_server.py
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    """Starts local HTTP server"""
    try:
        # Change to script directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Mars Defence Server started!")
            print(f"📱 Open your browser and go to: http://localhost:{PORT}")
            print(f"📁 Server is running in directory: {os.getcwd()}")
            print(f"⏹️  Press Ctrl+C to stop")
            print("-" * 50)
            
            # Automatically open browser
            try:
                webbrowser.open(f'http://localhost:{PORT}')
                print("🌐 Browser opened automatically")
            except:
                print("⚠️  Could not open browser automatically")
            
            print("-" * 50)
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Try another port:")
            print(f"   python start_server.py --port 8001")
        else:
            print(f"❌ Server startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--port":
        try:
            PORT = int(sys.argv[2])
        except (IndexError, ValueError):
            print("❌ Invalid port format. Use: --port 8000")
            sys.exit(1)
    
    start_server()
