#!/usr/bin/env python3
"""
Setup script for Live News Video Hub
This script helps initialize the project and install dependencies.
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        print(f"✅ Node.js {version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is not installed or not in PATH")
        return False

def setup_frontend():
    """Setup the Next.js frontend"""
    print("\n🚀 Setting up Frontend...")
    
    if not os.path.exists("node_modules"):
        if not run_command("npm install"):
            return False
    else:
        print("✅ Frontend dependencies already installed")
    
    return True

def setup_backend():
    """Setup the FastAPI backend"""
    print("\n🐍 Setting up Backend...")
    
    backend_dir = "backend"
    if not os.path.exists(backend_dir):
        print("❌ Backend directory not found")
        return False
    
    # Create virtual environment if it doesn't exist
    venv_dir = os.path.join(backend_dir, "venv")
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        if not run_command("python -m venv venv", cwd=backend_dir):
            return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
        python_path = os.path.join(venv_dir, "Scripts", "python")
    else:
        pip_path = os.path.join(venv_dir, "bin", "pip")
        python_path = os.path.join(venv_dir, "bin", "python")
    
    # Install requirements
    requirements_file = os.path.join(backend_dir, "requirements.txt")
    if os.path.exists(requirements_file):
        if not run_command(f'"{pip_path}" install -r requirements.txt', cwd=backend_dir):
            return False
    else:
        print("❌ requirements.txt not found in backend directory")
        return False
    
    return True

def create_env_file():
    """Create .env file for backend if it doesn't exist"""
    env_file = "backend/.env"
    if not os.path.exists(env_file):
        print("\n📝 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("# Live News Video Hub Environment Variables\n")
            f.write("DATABASE_URL=sqlite:///./news_videos.db\n")
            f.write("# Add your YouTube API key here if needed\n")
            f.write("# API_KEY=your_youtube_api_key\n")
        print("✅ Created backend/.env file")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("📺 Live News Video Hub Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        print("\nPlease install Node.js from https://nodejs.org/")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed")
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the backend: cd backend && python main.py")
    print("2. Start the frontend: npm run dev")
    print("3. Open http://localhost:3000 in your browser")
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main()
