#!/usr/bin/env python3
import os
import sys
import time
import logging
import threading
from datetime import datetime
import pyudev
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import customtkinter as ctk
from PIL import Image, ImageTk

class USBAuthGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("USB Authentication System")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize authentication service
        self.auth_service = USBAuthService()
        self.setup_gui()
        
        # Start USB monitoring in a separate thread
        self.monitor_thread = threading.Thread(target=self.auth_service.run, daemon=True)
        self.monitor_thread.start()
        
        # Start status update loop
        self.update_status()
        
    def setup_gui(self):
        # Title
        title_label = ctk.CTkLabel(
            self.root,
            text="USB Authentication System",
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=20)
        
        # Status Frame
        status_frame = ctk.CTkFrame(self.root)
        status_frame.pack(pady=10, padx=20, fill="x")
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Status: Waiting for USB...",
            font=("Helvetica", 14)
        )
        self.status_label.pack(pady=10)
        
        # Device List Frame
        device_frame = ctk.CTkFrame(self.root)
        device_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        device_label = ctk.CTkLabel(
            device_frame,
            text="Registered Devices",
            font=("Helvetica", 16, "bold")
        )
        device_label.pack(pady=10)
        
        # Device List
        self.device_listbox = ctk.CTkTextbox(
            device_frame,
            width=300,
            height=200
        )
        self.device_listbox.pack(pady=10, padx=10)
        
        # Buttons Frame
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10, padx=20, fill="x")
        
        # Register Button
        self.register_button = ctk.CTkButton(
            button_frame,
            text="Register New Device",
            command=self.show_register_dialog
        )
        self.register_button.pack(pady=5, padx=5, fill="x")
        
        # Remove Button
        self.remove_button = ctk.CTkButton(
            button_frame,
            text="Remove Device",
            command=self.show_remove_dialog
        )
        self.remove_button.pack(pady=5, padx=5, fill="x")
        
        # Refresh Button
        self.refresh_button = ctk.CTkButton(
            button_frame,
            text="Refresh Device List",
            command=self.refresh_device_list
        )
        self.refresh_button.pack(pady=5, padx=5, fill="x")
        
        # Initial device list update
        self.refresh_device_list()
        
    def update_status(self):
        """Update the status label based on authentication state"""
        if self.auth_service.is_authenticated:
            self.status_label.configure(
                text="Status: Authenticated ✓",
                text_color="green"
            )
        else:
            self.status_label.configure(
                text="Status: Not Authenticated ✗",
                text_color="red"
            )
        self.root.after(1000, self.update_status)
        
    def refresh_device_list(self):
        """Update the device list display"""
        self.device_listbox.delete("1.0", "end")
        if self.auth_service.authorized_devices:
            for device_id in self.auth_service.authorized_devices:
                self.device_listbox.insert("end", f"{device_id}\n")
        else:
            self.device_listbox.insert("end", "No registered devices")
            
    def show_register_dialog(self):
        """Show dialog for registering new devices"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Register New Device")
        dialog.geometry("300x200")
        
        # List connected devices
        devices = self.auth_service.list_usb_devices()
        if devices:
            device_var = ctk.StringVar(value=devices[0][0])
            
            label = ctk.CTkLabel(
                dialog,
                text="Select a device to register:",
                font=("Helvetica", 12)
            )
            label.pack(pady=10)
            
            device_menu = ctk.CTkOptionMenu(
                dialog,
                values=[d[0] for d in devices],
                variable=device_var
            )
            device_menu.pack(pady=10)
            
            def register():
                device_id = device_var.get()
                if self.auth_service.register_device(device_id):
                    self.refresh_device_list()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Device already registered")
            
            register_button = ctk.CTkButton(
                dialog,
                text="Register",
                command=register
            )
            register_button.pack(pady=10)
        else:
            label = ctk.CTkLabel(
                dialog,
                text="No USB devices found",
                font=("Helvetica", 12)
            )
            label.pack(pady=10)
            
    def show_remove_dialog(self):
        """Show dialog for removing devices"""
        if not self.auth_service.authorized_devices:
            messagebox.showinfo("Info", "No registered devices to remove")
            return
            
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Remove Device")
        dialog.geometry("300x200")
        
        device_var = ctk.StringVar(value=list(self.auth_service.authorized_devices)[0])
        
        label = ctk.CTkLabel(
            dialog,
            text="Select a device to remove:",
            font=("Helvetica", 12)
        )
        label.pack(pady=10)
        
        device_menu = ctk.CTkOptionMenu(
            dialog,
            values=list(self.auth_service.authorized_devices),
            variable=device_var
        )
        device_menu.pack(pady=10)
        
        def remove():
            device_id = device_var.get()
            if self.auth_service.remove_device(device_id):
                self.refresh_device_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to remove device")
        
        remove_button = ctk.CTkButton(
            dialog,
            text="Remove",
            command=remove
        )
        remove_button.pack(pady=10)
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = USBAuthGUI()
    app.run() 