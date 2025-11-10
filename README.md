# 🐱 CatParser - Purr-fectly Fast Document Parsing! 🐾

```
    /\_/\
   ( o.o )  < "Meow! Parse documents with whisker-sharp precision!"
    > ^ <
   /|   |\
  (_|   |_)
```

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**CatParser** is a *purr-fectly* fast and *fur-iously* efficient document parser designed for processing large JSON lines files with the agility of a kitten and the reliability of a cat landing on its feet!

Built with multiprocessing for maximum speed and featuring beautiful rich terminal outputs with cat-themed puns that will make you smile while your data gets processed at lightning speed! ⚡

---

## ✨ Features

- 🚀 **Blazing Fast**: Multiprocessing support for parallel document processing
- 🎨 **Beautiful Output**: Rich terminal UI with progress bars and colorful tables
- 😺 **Cat-Themed**: Because everything is better with cats!
- 📊 **Visualizations**: Automatic generation of analysis plots
- 🐾 **Easy to Use**: Simple CLI with sensible defaults
- 🧶 **Reliable**: Robust error handling and reporting
- 🎯 **Production-Ready**: Built with modern Python best practices

---

## 🎬 Quick Start

### Installation with uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/generalMG/DocumentParser.git
cd DocumentParser

# Install with uv (fast and modern!)
uv pip install -e .

# Or install from PyPI (once published)
uv pip install catparser
```

### Installation with pip

```bash
pip install -e .
```

### Your First Parse

```bash
# Parse your JSON lines file
catparser parse your_data.jsonl

# Or use one of the cat-themed aliases!
meow-parser parse your_data.jsonl
purr-parse parse your_data.jsonl
```

---

## 📖 Usage

### Basic Parsing

```bash
# Parse with default settings
catparser parse data.jsonl

# Specify output directory
catparser parse data.jsonl --output ./results

# Use more CPU cores (more paws!)
catparser parse data.jsonl --processes 8

# Skip visualization plots
catparser parse data.jsonl --no-plots

# Quiet mode (less meowing, more serious)
catparser parse data.jsonl --quiet
```

### Performance Testing

Test different core counts to find optimal performance:

```bash
catparser purrformance data.jsonl
```

This will benchmark parsing with different numbers of CPU cores and show you the speed improvements!

### Just for Fun

Want to hear a meow?

```bash
catparser meow
```

### Python API

Use CatParser in your Python code:

```python
from catparser import KittenParser, parse_documents_with_whiskers

# Quick and easy
results = parse_documents_with_whiskers(
    "data.jsonl",
    output_dir="./results",
    num_processes=4
)

# Or use the class directly
parser = KittenParser(num_processes=8)
results = parser.parse("data.jsonl", create_plots=True)

print(f"Parsed {results['total_articles']} articles!")
```

---

## 🎯 What Does It Do?

CatParser processes JSON lines files containing document metadata (like arXiv papers) and:

1. **Extracts temporal data**: Counts articles by publication year
2. **Analyzes versions**: Tracks how many versions each article has
3. **Handles errors gracefully**: Reports errors without stopping
4. **Creates visualizations**: Generates beautiful plots of the analysis
5. **Provides rich feedback**: Shows progress and results in a beautiful terminal UI

Perfect for analyzing large document collections, research paper datasets, or any JSON lines data with temporal information!

---

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/generalMG/DocumentParser.git
cd DocumentParser

# Install with development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/

# Lint code
ruff check src/
```

### Project Structure

```
DocumentParser/
├── src/
│   └── catparser/
│       ├── __init__.py          # Package initialization
│       ├── cat_art.py           # Cat ASCII art and decorations
│       ├── cli.py               # Command-line interface
│       └── parser.py            # Core parsing logic
├── tests/                       # Test files
├── examples/                    # Example data and scripts
├── pyproject.toml              # Project configuration
├── README.md                   # This file!
└── LICENSE                     # MIT License
```

---

## 📊 Example Output

When you run CatParser, you'll see beautiful output like this:

```
╭──────────────────── 🐱 Welcome! 🐱 ─────────────────────╮
│                                                          │
│   ______      ______                                     │
│  / ____/___ _/ ____/___ ____________                     │
│ / /   / __ `/ __/ / __ `/ ___/ ___/                      │
│/ /___/ /_/ / /___/ /_/ / /  (__  )                       │
│\____/\__,_/_____/\__,_/_/  /____/                        │
│                                                          │
│     /\_/\                                                │
│    ( o.o )                                               │
│     > ^ <                                                │
│    /|   |\                                               │
│   (_|   |_)                                              │
│                                                          │
│  Whisker-sharp document analysis! 🎯                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                          │
│                   Made with 😻 and 🐾                     │
╰──────────────────────────────────────────────────────────╯

🐾 ──────────────────────────────────────────────────── 🐾

         🐾 Parsing Configuration
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Setting           ┃ Value             ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ File              │ arxiv.jsonl       │
│ CPU Cores (Paws)  │ 4                 │
│ Output Directory  │ .                 │
└───────────────────┴───────────────────┘
```

---

## 🎨 Features Showcase

### Rich Progress Bars

```
Counting chunks... (like counting sheep, but for cats!)
😸 Parsing documents with whiskers... ━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

### Beautiful Tables

Results are displayed in colorful, easy-to-read tables showing:
- Total articles processed
- Error counts ("hairballs")
- Success rates
- Top years by article count
- Version distributions

### Cat-Themed Messages

Throughout the parsing process, you'll see adorable cat activities:
- 🐱 Grooming the data...
- 🐾 Padding through files...
- 😺 Purring contentedly...
- 🎯 Pouncing on errors...
- 🧶 Untangling JSON strings...

---

## 🤔 Why Cats?

Because parsing data should be fun! And everything is better with cats. Also:

- Cats are fast → CatParser is fast ⚡
- Cats are precise → CatParser is accurate 🎯
- Cats land on their feet → CatParser handles errors gracefully 🛡️
- Cats are adorable → CatParser makes data analysis delightful 😻

---

## 📦 Dependencies

CatParser uses these paw-some packages:

- **rich**: Beautiful terminal formatting and progress bars
- **typer**: Modern CLI framework
- **matplotlib**: Data visualization
- **pyfiglet**: ASCII art text
- **emoji**: Because emojis are fun!

All managed efficiently with **uv** for fast installation!

---

## 🤝 Contributing

Contributions are welcome! Whether it's:

- 🐛 Bug reports
- 💡 Feature suggestions
- 📝 Documentation improvements
- 🎨 More cat puns (always appreciated!)

Please feel free to open an issue or submit a pull request!

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Thanks to all the cat lovers out there! 😻
- Built with love, Python, and way too many cat puns 🐾
- Special thanks to the open-source community for amazing tools!

---

## 📞 Contact

Have questions? Found a bug? Want to share your cat pictures?

- GitHub: [generalMG/DocumentParser](https://github.com/generalMG/DocumentParser)
- Issues: [Report a bug](https://github.com/generalMG/DocumentParser/issues)

---

<div align="center">

**Made with 😻 by cat enthusiasts, for data enthusiasts!**

```
  /\_/\
 ( ^.^ )  < "Happy parsing!"
  > ^ <
```

*Purr-fect code, purr-fect results!* 🐾

</div>
