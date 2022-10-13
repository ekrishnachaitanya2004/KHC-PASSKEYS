#!/usr/bin/env python3
import os
import sys
import pyudev
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('usb_setup.log'),
        logging.StreamHandler()
    ]
)

class USBSetup:
    def __init__(self):
        self.context = pyudev.Context()
        self.authorized_devices = set()
        self.load_authorized_devices()

    def load_authorized_devices(self):
        """Load existing authorized devices"""
        try:
            if os.path.exists('authorized_devices.txt'):
                with open('authorized_devices.txt', 'r') as f:
                    self.authorized_devices = set(line.strip() for line in f)
        except Exception as e:
            logging.error(f"Error loading authorized devices: {e}")

    def save_authorized_devices(self):
        """Save authorized devices to file"""
        try:
            with open('authorized_devices.txt', 'w') as f:
                for device_id in self.authorized_devices:
                    f.write(f"{device_id}\n")
            logging.info("Authorized devices saved successfully")
        except Exception as e:
            logging.error(f"Error saving authorized devices: {e}")

    def get_device_id(self, device):
        """Get unique identifier for USB device"""
        try:
            serial = device.attributes.get('serial')
            if serial:
                return serial.decode('utf-8')
            return device.device_path
        except Exception as e:
            logging.error(f"Error getting device ID: {e}")
            return None

    def list_usb_devices(self):
        """List all connected USB devices"""
        devices = []
        for device in self.context.list_devices(subsystem='block', DEVTYPE='partition'):
            if 'usb' in device.device_path.lower():
                device_id = self.get_device_id(device)
                if device_id:
                    devices.append((device_id, device))
        return devices

    def register_device(self, device_id):
        """Register a new USB device"""
        if device_id not in self.authorized_devices:
            self.authorized_devices.add(device_id)
            self.save_authorized_devices()
            logging.info(f"Device {device_id} registered successfully")
            return True
        return False

    def remove_device(self, device_id):
        """Remove a registered USB device"""
        if device_id in self.authorized_devices:
            self.authorized_devices.remove(device_id)
            self.save_authorized_devices()
            logging.info(f"Device {device_id} removed successfully")
            return True
        return False

    def run(self):
        """Interactive setup process"""
        print("\n=== USB Authentication Setup ===")
        print("1. List connected USB devices")
        print("2. Register new USB device")
        print("3. Remove registered USB device")
        print("4. List registered devices")
        print("5. Exit")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-5): ")
                
                if choice == '1':
                    devices = self.list_usb_devices()
                    if devices:
                        print("\nConnected USB devices:")
                        for i, (device_id, device) in enumerate(devices, 1):
                            print(f"{i}. Device ID: {device_id}")
                    else:
                        print("No USB devices found")
                
                elif choice == '2':
                    devices = self.list_usb_devices()
                    if devices:
                        print("\nSelect a device to register:")
                        for i, (device_id, _) in enumerate(devices, 1):
                            print(f"{i}. Device ID: {device_id}")
                        
                        try:
                            device_choice = int(input("\nEnter device number: ")) - 1
                            if 0 <= device_choice < len(devices):
                                device_id = devices[device_choice][0]
                                if self.register_device(device_id):
                                    print("Device registered successfully!")
                                else:
                                    print("Device already registered")
                            else:
                                print("Invalid device number")
                        except ValueError:
                            print("Please enter a valid number")
                    else:
                        print("No USB devices found")
                
                elif choice == '3':
                    if self.authorized_devices:
                        print("\nRegistered devices:")
                        for i, device_id in enumerate(self.authorized_devices, 1):
                            print(f"{i}. Device ID: {device_id}")
                        
                        try:
                            device_choice = int(input("\nEnter device number to remove: ")) - 1
                            device_ids = list(self.authorized_devices)
                            if 0 <= device_choice < len(device_ids):
                                device_id = device_ids[device_choice]
                                if self.remove_device(device_id):
                                    print("Device removed successfully!")
                                else:
                                    print("Device not found")
                            else:
                                print("Invalid device number")
                        except ValueError:
                            print("Please enter a valid number")
                    else:
                        print("No registered devices")
                
                elif choice == '4':
                    if self.authorized_devices:
                        print("\nRegistered devices:")
                        for i, device_id in enumerate(self.authorized_devices, 1):
                            print(f"{i}. Device ID: {device_id}")
                    else:
                        print("No registered devices")
                
                elif choice == '5':
                    print("Setup completed")
                    break
                
                else:
                    print("Invalid choice. Please try again.")
            
            except KeyboardInterrupt:
                print("\nSetup interrupted by user")
                break
            except Exception as e:
                logging.error(f"Error during setup: {e}")
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    setup = USBSetup()
    setup.run() 