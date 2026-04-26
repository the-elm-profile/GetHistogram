# GetHistogram

A powerful Python-based software providing both CLI and GUI interfaces for creating highly customizable and editable histograms. The GUI is available at https://gethist.streamlit.app.

## Description

GetHistogram simplifies the process of generating professional-quality histograms with extensive customization options. Whether you prefer working from the command line or through an intuitive graphical interface, GetHistogram offers flexible tools to create, modify, and export histograms for data analysis, presentations, and publications.

### Features

- **CLI Interface**: Command-line tools for batch processing and scripting
- **GUI Interface**: User-friendly web interface powered by Streamlit
- **Customizable Histograms**: Extensive editing options for appearance and data representation
- **Multiple Export Formats**: Save histograms in various formats for different use cases
- **Easy Integration**: Python-based architecture for easy integration into existing workflows

## Getting Started

### Dependencies

- Python 3.7 or higher
- pip (Python package manager)
- See `requirements.txt` for Python package dependencies

**Operating Systems:**
- Windows 10+
- macOS 10.14+
- Linux (Ubuntu 18.04+, Fedora 30+, or equivalent)

### Installing

1. **Clone the repository:**
   ```bash
   git clone https://github.com/the-elm-profile/GetHistogram.git
   cd GetHistogram
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python -m gethistogram --version
   ```
   
## Usage Examples

### Example 1: Simple CLI Usage
```bash
python gh-cli.py
```

### Example 2: GUI Usage
Acess the link:
https://gethist.streamlit.app

## Project Structure
```
GetHistogram/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── Streamlit-GUI
│   └── gh-gui.py        # Streamlit GUI application
├── Terminal-CLI/
│   └── gh-cli.py
└── CSV-Samples/
    └── Rand.csv         # A CSV sample with radom numbers
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3 - see the [LICENSE](LICENSE) file for details.

## Authors

- [@the-elm-profile](https://github.com/the-elm-profile)

## Support

For issues, questions, or suggestions, please open an [issue on GitHub](https://github.com/the-elm-profile/GetHistogram/issues).

---

**Note:** This project is currently under active development. Features and documentation may be subject to change.
