#!/usr/bin/env python3
import os
import sys
import shutil
import platform
import customtkinter as ctk
from tkinter import messagebox
import json
from cryptography.fernet import Fernet
from datetime import datetime

# Platform-specific imports
if platform.system() == 'Windows':
    import win32api
    import win32con
    import win32file
    import win32security

class USBInstaller:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("USB Security Installer")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_gui()
        
    def setup_gui(self):
        # Title
        title_label = ctk.CTkLabel(
            self.root,
            text="USB Security Installer",
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=20)
        
        # Drive Selection Frame
        drive_frame = ctk.CTkFrame(self.root)
        drive_frame.pack(pady=10, padx=20, fill="x")
        
        drive_label = ctk.CTkLabel(
            drive_frame,
            text="Select USB Drive:",
            font=("Helvetica", 12)
        )
        drive_label.pack(pady=5)
        
        self.drive_var = ctk.StringVar()
        self.drive_menu = ctk.CTkOptionMenu(
            drive_frame,
            values=self.get_removable_drives(),
            variable=self.drive_var
        )
        self.drive_menu.pack(pady=5)
        
        # Refresh Button
        refresh_button = ctk.CTkButton(
            drive_frame,
            text="Refresh Drives",
            command=self.refresh_drives
        )
        refresh_button.pack(pady=5)
        
        # Installation Options
        options_frame = ctk.CTkFrame(self.root)
        options_frame.pack(pady=10, padx=20, fill="x")
        
        options_label = ctk.CTkLabel(
            options_frame,
            text="Installation Options",
            font=("Helvetica", 14, "bold")
        )
        options_label.pack(pady=5)
        
        # Auto-start option
        self.autostart_var = ctk.BooleanVar(value=True)
        autostart_check = ctk.CTkCheckBox(
            options_frame,
            text="Start automatically when USB is inserted",
            variable=self.autostart_var
        )
        autostart_check.pack(pady=5)
        
        # Progress Frame
        progress_frame = ctk.CTkFrame(self.root)
        progress_frame.pack(pady=10, padx=20, fill="x")
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to install",
            font=("Helvetica", 12)
        )
        self.progress_label.pack(pady=5)
        
        # Install Button
        install_button = ctk.CTkButton(
            self.root,
            text="Install",
            command=self.install
        )
        install_button.pack(pady=20)
        
    def get_removable_drives(self):
        """Get list of removable drives based on platform"""
        drives = []
        if platform.system() == 'Windows':
            # Windows-specific drive detection
            bitmask = win32api.GetLogicalDrives()
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if bitmask & 1:
                    drive = f"{letter}:\\"
                    if win32file.GetDriveType(drive) == win32con.DRIVE_REMOVABLE:
                        drives.append(drive)
                bitmask >>= 1
        elif platform.system() == 'Linux':
            # Linux-specific drive detection
            output = os.popen("df -h").read()
            for line in output.split('\n'):
                if '/dev/sd' in line and 'media' in line:
                    drive = line.split()[0]
                    drives.append(drive)
        elif platform.system() == 'Darwin':
            # macOS-specific drive detection
            output = os.popen("df -h").read()
            for line in output.split('\n'):
                if '/Volumes/' in line:
                    drive = line.split()[0]
                    drives.append(drive)
        
        return drives if drives else ["No USB drives found"]
    
    def refresh_drives(self):
        """Refresh the list of removable drives"""
        drives = self.get_removable_drives()
        self.drive_menu.configure(values=drives)
        if drives[0] != "No USB drives found":
            self.drive_var.set(drives[0])
    
    def install(self):
        """Install the security program to the selected USB drive"""
        drive = self.drive_var.get()
        if drive == "No USB drives found":
            messagebox.showerror("Error", "No USB drive selected")
            return
            
        try:
            # Create program directory
            if platform.system() == 'Windows':
                program_dir = os.path.join(drive, "USB_Security")
            elif platform.system() == 'Linux':
                program_dir = os.path.join(drive, "USB_Security")
            elif platform.system() == 'Darwin':
                program_dir = os.path.join(drive, "USB_Security")
            
            os.makedirs(program_dir, exist_ok=True)
            
            # Copy program files
            self.copy_program_files(program_dir)
            
            # Create autorun configuration
            self.create_autorun(program_dir)
            
            # Initialize security configuration
            self.initialize_security(program_dir)
            
            messagebox.showinfo("Success", "Installation completed successfully!")
            self.progress_label.configure(text="Installation completed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Installation failed: {str(e)}")
            self.progress_label.configure(text="Installation failed")
    
    def copy_program_files(self, target_dir):
        """Copy program files to USB drive"""
        self.progress_label.configure(text="Copying program files...")
        
        # Copy main program
        shutil.copy2("usb_program.py", os.path.join(target_dir, "usb_program.py"))
        
        # Copy platform-specific files if needed
        if platform.system() == 'Windows':
            # Copy Windows-specific files
            pass
        elif platform.system() == 'Linux':
            # Copy Linux-specific files
            pass
        elif platform.system() == 'Darwin':
            # Copy macOS-specific files
            pass
    
    def create_autorun(self, program_dir):
        """Create autorun configuration based on platform"""
        self.progress_label.configure(text="Creating autorun configuration...")
        
        if platform.system() == 'Windows':
            # Windows autorun.inf
            autorun_path = os.path.join(program_dir, "autorun.inf")
            with open(autorun_path, "w") as f:
                f.write(f"""[AutoRun]
open=pythonw.exe "{os.path.join(program_dir, 'usb_program.py')}"
icon={os.path.join(program_dir, 'icon.ico')}
label=USB Security
""")
        elif platform.system() == 'Linux':
            # Linux udev rules
            udev_rules = f"""SUBSYSTEM=="block", ACTION=="add", ENV{{ID_BUS}}=="usb", RUN+="/usr/bin/python3 {os.path.join(program_dir, 'usb_program.py')}"
"""
            with open("/etc/udev/rules.d/99-usb-security.rules", "w") as f:
                f.write(udev_rules)
            os.system("udevadm control --reload-rules")
        elif platform.system() == 'Darwin':
            # macOS launchd configuration
            launchd_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.usb.security</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{os.path.join(program_dir, 'usb_program.py')}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
            with open("/Library/LaunchAgents/com.usb.security.plist", "w") as f:
                f.write(launchd_plist)
    
    def initialize_security(self, program_dir):
        """Initialize security configuration"""
        self.progress_label.configure(text="Initializing security...")
        
        # Generate security key
        key = Fernet.generate_key()
        with open(os.path.join(program_dir, "security.key"), "wb") as f:
            f.write(key)
        
        # Create initial configuration
        config = {
            "installed": True,
            "install_date": str(datetime.now()),
            "autostart": self.autostart_var.get(),
            "platform": platform.system()
        }
        
        with open(os.path.join(program_dir, "config.json"), "w") as f:
            json.dump(config, f)
    
    def run(self):
        """Start the installer"""
        self.root.mainloop()

if __name__ == "__main__":
    installer = USBInstaller()
    installer.run() 