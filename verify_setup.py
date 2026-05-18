"""
Verification Script
Checks if the project structure and dependencies are set up correctly
"""
import os
import sys
import importlib.util
from pathlib import Path

def check_file(path):
    if os.path.exists(path):
        print(f"✅ Found {path}")
        return True
    else:
        print(f"❌ Missing {path}")
        return False

def check_dependency(package):
    spec = importlib.util.find_spec(package)
    if spec is not None:
        print(f"✅ Found package: {package}")
        return True
    else:
        print(f"❌ Missing package: {package}")
        return False

def main():
    print("Verifying InnerTube API Setup...")
    print("-" * 40)
    
    # Check Project Structure
    print("\nChecking Project Structure:")
    files_to_check = [
        "main.py",
        "config.py",
        "requirements.txt",
        "routes/__init__.py",
        "routes/youtube.py",
        "routes/channels.py",
        "routes/playlists.py",
        "routes/music.py",
        "services/__init__.py",
        "services/innertube_client.py",
        "utils/__init__.py",
        "static/index.html",
        "static/styles.css",
        "static/script.js"
    ]
    
    all_files_exist = True
    for file_path in files_to_check:
        if not check_file(file_path):
            all_files_exist = False
            
    # Check Dependencies
    print("\nChecking Dependencies (may require pip install):")
    dependencies = [
        "fastapi",
        "uvicorn",
        "innertube",
        "pydantic",
        "cachetools"
    ]
    
    all_deps_exist = True
    for dep in dependencies:
        if not check_dependency(dep):
            all_deps_exist = False
            
    print("-" * 40)
    if all_files_exist and all_deps_exist:
        print("🎉 Verification Successful! You are ready to run the API.")
        print("Run 'start_server.bat' or 'python main.py' to start.")
    else:
        print("⚠️ Verification Failed. Please check missing files or dependencies.")
        print("Run 'pip install -r requirements.txt' to install dependencies.")

if __name__ == "__main__":
    main()
