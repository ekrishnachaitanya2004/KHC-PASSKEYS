#!/usr/bin/env python3
import os
import sys
import hashlib
import uuid
import json
import time
import platform
import logging
from datetime import datetime
from cryptography.fernet import Fernet

# Platform-specific imports
if platform.system() == 'Windows':
    import win32api
    import win32con
    import win32security
    import win32file
    import win32event
    import win32service
    import win32serviceutil
    import win32timezone
    import servicemanager
    import socket

class USBSecurityService:
    def __init__(self):
        self.running = True
        self.key_file = "security.key"
        self.config_file = "config.json"
        self.setup_logging()
        self.setup_platform_specific()

    def setup_platform_specific(self):
        """Setup platform-specific components"""
        if platform.system() == 'Windows':
            self.setup_windows_service()
        elif platform.system() == 'Linux':
            self.setup_linux_service()
        elif platform.system() == 'Darwin':  # macOS
            self.setup_macos_service()

    def setup_windows_service(self):
        """Setup Windows service components"""
        if len(sys.argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(self)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(self)

    def setup_linux_service(self):
        """Setup Linux service components"""
        # Implement Linux service setup if needed
        pass

    def setup_macos_service(self):
        """Setup macOS service components"""
        # Implement macOS service setup if needed
        pass

    def setup_logging(self):
        """Setup logging for the service"""
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usb_security.log")
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def get_usb_identifier(self):
        """Get unique identifier for the USB drive"""
        try:
            if platform.system() == 'Windows':
                # Windows-specific USB identification
                drive_letter = os.path.splitdrive(os.path.abspath(__file__))[0]
                volume_info = win32api.GetVolumeInformation(drive_letter)
                identifier = f"{volume_info[1]}_{drive_letter}"
            elif platform.system() == 'Linux':
                # Linux-specific USB identification
                device_path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
                device_info = os.popen(f"udevadm info -q property -n {device_path}").read()
                serial = [line.split('=')[1] for line in device_info.split('\n') if 'ID_SERIAL=' in line][0]
                identifier = f"{serial}_{device_path}"
            elif platform.system() == 'Darwin':
                # macOS-specific USB identification
                device_path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
                device_info = os.popen(f"diskutil info {device_path}").read()
                serial = [line.split(':')[1].strip() for line in device_info.split('\n') if 'Serial Number' in line][0]
                identifier = f"{serial}_{device_path}"
            else:
                # Fallback for other systems
                identifier = str(uuid.uuid4())
            return identifier
        except Exception as e:
            logging.error(f"Error getting USB identifier: {e}")
            return None

    def generate_security_key(self):
        """Generate a new security key"""
        try:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
        except Exception as e:
            logging.error(f"Error generating security key: {e}")
            return None

    def load_security_key(self):
        """Load existing security key"""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    return f.read()
            return None
        except Exception as e:
            logging.error(f"Error loading security key: {e}")
            return None

    def save_config(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
            return True
        except Exception as e:
            logging.error(f"Error saving config: {e}")
            return False

    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return {}

    def verify_usb(self):
        """Verify USB drive authenticity"""
        try:
            usb_id = self.get_usb_identifier()
            if not usb_id:
                return False

            config = self.load_config()
            if 'authorized_id' not in config:
                # First time setup
                config['authorized_id'] = usb_id
                self.save_config(config)
                return True

            return config['authorized_id'] == usb_id
        except Exception as e:
            logging.error(f"Error verifying USB: {e}")
            return False

    def grant_access(self):
        """Grant system access"""
        try:
            if platform.system() == 'Windows':
                # Windows-specific access granting
                pass
            elif platform.system() == 'Linux':
                # Linux-specific access granting
                pass
            elif platform.system() == 'Darwin':
                # macOS-specific access granting
                pass
            logging.info("Access granted")
        except Exception as e:
            logging.error(f"Error granting access: {e}")

    def deny_access(self):
        """Deny system access"""
        try:
            if platform.system() == 'Windows':
                # Windows-specific access denial
                pass
            elif platform.system() == 'Linux':
                # Linux-specific access denial
                pass
            elif platform.system() == 'Darwin':
                # macOS-specific access denial
                pass
            logging.info("Access denied")
        except Exception as e:
            logging.error(f"Error denying access: {e}")

    def main(self):
        """Main service loop"""
        logging.info("USB Security Service started")
        
        # Initialize security key
        key = self.load_security_key()
        if not key:
            key = self.generate_security_key()
            if not key:
                logging.error("Failed to initialize security key")
                return

        while self.running:
            try:
                # Check USB verification
                if self.verify_usb():
                    logging.info("USB verification successful")
                    self.grant_access()
                else:
                    logging.warning("USB verification failed")
                    self.deny_access()

                time.sleep(1)  # Check every second
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                time.sleep(1)

if __name__ == '__main__':
    service = USBSecurityService()
    service.main() 