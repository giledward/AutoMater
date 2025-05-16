# AutoMater

A modern, sleek hotkey-driven task automation tool built with Python. AutoMater provides a clean interface for triggering various automated actions through a quick-access popup menu.

## 🌟 Features

- **Modern UI**: Sleek, borderless popup interface that's easy to use
- **Global Hotkey**: Quick access with Shift+F12 from anywhere
- **Multiple Modes**: 10 different automation modes (0-9)
- **Built-in Auto-Clicker**: High-speed clicking automation (Mode 3)
- **DPI Aware**: Crisp rendering on high-resolution displays
- **Error Handling**: Robust error management and user feedback

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.6+ installed on your system. You'll also need the following packages:

```bash
pip install keyboard
pip install mouse
```

### Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Navigate to the project directory
2. Run the selector:
```bash
python SelectorV1.py
```

## 📖 How to Use

1. Press `Shift+F12` to open the input popup
2. Enter a number (0-9) and press Enter to activate/deactivate that mode
3. Press `Escape` to dismiss the popup without action

### Mode Reference

- **Mode 0**: Exit the application
- **Mode 3**: Auto-clicker mode (19,000 clicks with minimal delay)
- **Modes 1-2, 4-9**: Toggle modes for custom automation (can be customized)

## ⚙️ Customization

You can customize the behavior of each mode by modifying the `execute_action` method in `SelectorV1.py`. Each mode can be programmed to perform different automated tasks.

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




