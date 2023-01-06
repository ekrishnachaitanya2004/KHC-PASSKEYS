import PyInstaller.__main__
import os
import shutil

def build_exe():
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        
    # PyInstaller arguments
    args = [
        'usb_auth_gui.py',  # Main script
        '--name=USB_Auth_System',  # Name of the executable
        '--onefile',  # Create a single executable file
        '--windowed',  # Don't show console window
        '--icon=icon.ico',  # Application icon (if you have one)
        '--add-data=authorized_devices.txt;.',  # Include data files
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace existing build without asking
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("Build completed! Executable is in the 'dist' directory.")

if __name__ == "__main__":
    build_exe() 