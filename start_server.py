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
    
    def do_GET(self):
        # Check if the request is for app-ads.txt
        if self.path == '/app-ads.txt':
            try:
                # Read the app-ads.txt file
                with open('app-ads.txt', 'rb') as f:
                    content = f.read()
                
                # Set headers to force download
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Content-Disposition', 'attachment; filename="app-ads.txt"')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                
                # Send the file content
                self.wfile.write(content)
                return
            except FileNotFoundError:
                self.send_error(404, "File not found")
                return
            except Exception as e:
                self.send_error(500, f"Server error: {str(e)}")
                return
        
        # For all other requests, use the default behavior
        super().do_GET()

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
