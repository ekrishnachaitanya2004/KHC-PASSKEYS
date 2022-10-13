#!/usr/bin/env python3
import os
import sys
import time
import logging
from datetime import datetime
import pyudev
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('usb_auth.log'),
        logging.StreamHandler()
    ]
)

class USBAuthService:
    def __init__(self):
        self.authorized_devices = set()
        self.is_authenticated = False
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='block', device_type='partition')
        self.load_authorized_devices()
        
    def load_authorized_devices(self):
        """Load authorized device IDs from storage"""
        try:
            if os.path.exists('authorized_devices.txt'):
                with open('authorized_devices.txt', 'r') as f:
                    self.authorized_devices = set(line.strip() for line in f)
                logging.info(f"Loaded {len(self.authorized_devices)} authorized devices")
        except Exception as e:
            logging.error(f"Error loading authorized devices: {e}")

    def get_device_id(self, device):
        """Get unique identifier for USB device"""
        try:
            # Get device serial number or UUID
            serial = device.attributes.get('serial')
            if serial:
                return serial.decode('utf-8')
            # Fallback to device path
            return device.device_path
        except Exception as e:
            logging.error(f"Error getting device ID: {e}")
            return None

    def authenticate_device(self, device):
        """Authenticate USB device"""
        device_id = self.get_device_id(device)
        if device_id and device_id in self.authorized_devices:
            self.is_authenticated = True
            logging.info(f"Device {device_id} authenticated successfully")
            return True
        logging.warning(f"Unauthorized device detected: {device_id}")
        return False

    def handle_device_event(self, device):
        """Handle USB device events"""
        action = device.action
        if action == 'add':
            if self.authenticate_device(device):
                self.grant_access()
            else:
                self.deny_access()
        elif action == 'remove':
            self.revoke_access()

    def grant_access(self):
        """Grant system access"""
        logging.info("Access granted")
        # Implement your access granting logic here
        # For example, unlock the system, start specific services, etc.

    def deny_access(self):
        """Deny system access"""
        logging.info("Access denied")
        # Implement your access denial logic here
        # For example, lock the system, show warning message, etc.

    def revoke_access(self):
        """Revoke system access when USB is removed"""
        if self.is_authenticated:
            self.is_authenticated = False
            logging.info("Access revoked - USB device removed")
            self.deny_access()

    def run(self):
        """Main service loop"""
        logging.info("USB Authentication Service started")
        observer = pyudev.MonitorObserver(self.monitor, self.handle_device_event)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            logging.info("Service stopped by user")
        observer.join()

if __name__ == "__main__":
    service = USBAuthService()
    service.run() 