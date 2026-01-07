"""
Build script for Windows Optimizer
This will create a standalone executable with admin privileges
"""

import subprocess
import sys
import os

def build_exe():
    """Build the executable using PyInstaller"""
    
    print("Building Windows Optimizer executable...")
    print("=" * 50)
    
    # PyInstaller command with options
    command = [
        'pyinstaller',
        '--onefile',                    # Single executable file
        '--windowed',                   # No console window
        '--name=WindowsOptimizer',      # Name of the executable
        '--icon=NONE',                  # You can add an .ico file here
        '--add-data=requirements.txt;.', # Include requirements
        '--uac-admin',                  # Request admin privileges
        'windows_optimizer.py'
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(command, check=True)
        
        print("=" * 50)
        print("Build completed successfully!")
        print("Executable location: dist/WindowsOptimizer.exe")
        print("\nThe app will request admin privileges when launched.")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("PyInstaller not found. Installing dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Please run this script again.")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()