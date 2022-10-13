# USB Passkey Authentication System

A secure USB-based authentication system that transforms a standard USB drive into a physical security key.

## Features

- USB device detection and monitoring
- Secure key storage and verification
- Automatic access control
- Real-time USB removal detection
- Encrypted authentication

## Requirements

- Python 3.8+
- Linux/Unix system (for USB monitoring)
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the setup script to initialize your USB key:
   ```bash
   python setup_usb.py
   ```

## Usage

1. Run the authentication service:
   ```bash
   python usb_auth_service.py
   ```
2. Insert your registered USB drive to authenticate
3. Remove the USB drive to lock the system

## Security Notes

- Keep your USB key secure and don't share it
- The system uses encryption to protect authentication data
- USB device identification is based on unique hardware identifiers

## License

MIT License 