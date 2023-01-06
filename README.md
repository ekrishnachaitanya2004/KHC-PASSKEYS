# USB Passkey Authentication System

A secure USB-based authentication system that transforms a standard USB drive into a physical security key.

## Features

- USB device detection and monitoring
- Secure key storage and verification
- Automatic access control
- Real-time USB removal detection
- Encrypted authentication
- Modern GUI interface
- Windows executable support

## Requirements

- Python 3.8+
- Windows/Linux/Unix system
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running from Source
1. Run the setup script to initialize your USB key:
   ```bash
   python setup_usb.py
   ```
2. Start the authentication service:
   ```bash
   python usb_auth_service.py
   ```

### Windows Executable
1. Build the executable:
   ```bash
   python build.py
   ```
2. Find the executable in the `dist` directory
3. Run `USB_Auth_System.exe`

## Security Notes

- Keep your USB key secure and don't share it
- The system uses encryption to protect authentication data
- USB device identification is based on unique hardware identifiers

## License

MIT License 