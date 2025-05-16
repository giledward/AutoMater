# AutoMater

A modern hotkey-driven task automation tool with a sleek interface. Quickly control programs and automate tasks through a simple popup menu.

## Features

- Modern, borderless popup interface
- Global hotkey access (Shift+F12)
- Program launcher and process manager
- High-speed auto-clicker
- Custom script execution
- JSON-based configuration

## Installation

```bash
# Install Python 3.6+ and required packages
pip install keyboard mouse psutil
```

## Usage

1. Press `Shift+F12` to open the control panel
2. Enter a number (0-9) to activate/deactivate modes
3. Press `Escape` to dismiss

## Default Modes

- `0`: Exit application
- `1`: Chrome
- `2`: Notepad
- `3`: Auto-clicker (19,000 clicks)
- `4`: Calculator
- `5-6`: Custom scripts
- `7-9`: Custom programs

## Configuration

Edit `config.json` to customize:
- Program paths
- Process names
- Auto-clicker settings
- Script locations
- Mode descriptions

## Requirements

- Python 3.6+
- Windows OS
- Administrative privileges (for some features)

## Quick Start

1. Clone/download the repository
2. Install dependencies
3. Run `python SelectorV1.py`
4. Use Shift+F12 to start automating

## 🛠️ Technical Details

- Built with Python and Tkinter
- Uses modern UI elements with ttk styling
- Implements proper DPI awareness for Windows
- Global hotkey management with keyboard suppression
- Thread-safe operation

## ⚠️ Important Notes

- Some features may require administrative privileges
- Auto-clicker functionality should be used responsibly
- The application captures global hotkeys, ensure Shift+F12 doesn't conflict with other applications

## 🤝 Contributing

Feel free to fork this project and submit pull requests. You can also open issues for bugs or feature requests.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔄 Version History

- v1.0.0 - Initial release with modern UI and basic functionality

## 🙏 Acknowledgments

- Built with Python's tkinter for UI
- Uses keyboard and mouse libraries for automation
- Inspired by the need for quick-access automation tools




