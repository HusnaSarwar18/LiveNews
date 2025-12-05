#!/usr/bin/env python3
"""
Start script for Live News Video Hub
This script starts both the frontend and backend servers.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class ServerManager:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_backend(self):
        """Start the FastAPI backend server"""
        backend_dir = Path("backend")
        if not backend_dir.exists():
            print("❌ Backend directory not found")
            return None
        
        # Check if virtual environment exists
        venv_python = backend_dir / "venv" / "Scripts" / "python.exe" if os.name == "nt" else backend_dir / "venv" / "bin" / "python"
        
        if venv_python.exists():
            python_cmd = str(venv_python)
        else:
            python_cmd = "python"
        
        print("🚀 Starting backend server...")
        try:
            process = subprocess.Popen(
                [python_cmd, "main.py"],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            return process
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return None
    
    def start_frontend(self):
        """Start the Next.js frontend server"""
        print("🚀 Starting frontend server...")
        try:
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            return process
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return None
    
    def log_output(self, process, name):
        """Log output from a process"""
        for line in iter(process.stdout.readline, ''):
            if not self.running:
                break
            if line:
                print(f"[{name}] {line.rstrip()}")
    
    def start_servers(self):
        """Start both servers"""
        print("📺 Starting Live News Video Hub...")
        print("=" * 50)
        
        # Start backend
        backend_process = self.start_backend()
        if backend_process:
            self.processes.append(backend_process)
            backend_thread = threading.Thread(
                target=self.log_output, 
                args=(backend_process, "BACKEND")
            )
            backend_thread.daemon = True
            backend_thread.start()
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start frontend
        frontend_process = self.start_frontend()
        if frontend_process:
            self.processes.append(frontend_process)
            frontend_thread = threading.Thread(
                target=self.log_output, 
                args=(frontend_process, "FRONTEND")
            )
            frontend_thread.daemon = True
            frontend_thread.start()
        
        print("\n🎉 Servers are starting up!")
        print("📱 Frontend will be available at: http://localhost:3000")
        print("🔧 Backend API will be available at: http://localhost:8000")
        print("📖 API documentation at: http://localhost:8000/docs")
        print("\n⏹️  Press Ctrl+C to stop all servers")
        print("=" * 50)
        
        try:
            # Keep the main thread alive
            while self.running and any(p.poll() is None for p in self.processes):
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            self.stop_servers()
    
    def stop_servers(self):
        """Stop all running servers"""
        self.running = False
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(f"Error stopping process: {e}")
        
        print("✅ All servers stopped")

def main():
    """Main function"""
    manager = ServerManager()
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print("\n🛑 Received shutdown signal...")
        manager.stop_servers()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start servers
    manager.start_servers()

if __name__ == "__main__":
    main()
