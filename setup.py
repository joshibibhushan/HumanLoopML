"""
Setup script for HumanLoopML
"""

import os
import subprocess
import sys

def main():
    print("=" * 60)
    print("HumanLoopML Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ required")
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    
    # Install dependencies
    print("\nInstalling dependencies...")
    requirements_path = os.path.join('api', 'requirements.txt')
    
    if not os.path.exists(requirements_path):
        print(f"ERROR: {requirements_path} not found")
        sys.exit(1)
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install dependencies")
        sys.exit(1)
    
    # Create necessary directories
    print("\nCreating directories...")
    directories = [
        'models',
        'data/feedback',
        'data/metrics'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created {directory}/")
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Train baseline model: python training/train_baseline.py")
    print("2. Start API: cd api && uvicorn main:app --reload")
    print("3. Open docs/index.html in your browser")
    print("\nSee README.md for detailed instructions.")

if __name__ == "__main__":
    main()
