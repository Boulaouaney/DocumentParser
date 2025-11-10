# 🐱 CatParser - The Purrfect Document Parser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Rust](https://img.shields.io/badge/rust-1.70+-orange.svg)](https://www.rust-lang.org/)

A **blazingly fast** 🚀, **cat-themed** 🐱 document parser written in Rust with Python bindings. Built for parsing large JSON Lines files (especially arXiv paper metadata) with maximum performance and delightful output.

## ✨ Features

- 🚀 **Blazingly Fast**: Written in Rust with parallel processing using Rayon
- 🐱 **Cat-Themed**: Delightful ASCII art cats and puns throughout
- 🎨 **Colorful Output**: Beautiful terminal output with colored text
- 🔧 **Easy to Use**: Simple Python API with sensible defaults
- 📦 **Memory Efficient**: Streams large files without loading everything into memory
- ⚡ **Parallel Processing**: Automatically uses all available CPU cores
- 🛡️ **Error Handling**: Gracefully handles malformed JSON and missing fields
- 🐍 **Python Bindings**: Seamless integration with Python via PyO3

## 📊 Performance

CatParser is optimized for speed:

- Processes **millions of documents per second** on modern hardware
- Uses parallel processing across all CPU cores
- Written in Rust for maximum performance
- Zero-copy parsing where possible
- Efficient memory usage with streaming

## 📋 Requirements

### For Building from Source

- **Rust**: 1.70 or newer ([Install Rust](https://rustup.rs/))
- **Python**: 3.8 or newer
- **Maturin**: Python build system for Rust extensions

### For Using Pre-built Packages

- **Python**: 3.8 or newer

## 🚀 Installation

### Option 1: Install with uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/Boulaouaney/DocumentParser.git
cd DocumentParser

# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Build and install
uv build
uv pip install dist/catparser-*.whl

# Or sync from source
uv sync
```

### Option 2: Install from Source (Development)

```bash
# Clone the repository
git clone https://github.com/Boulaouaney/DocumentParser.git
cd DocumentParser

# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Create virtual environment and install
uv venv
uv pip install maturin
uv run maturin develop --release
```

### Option 3: Traditional pip Installation

```bash
# Install Python dependencies
pip install maturin

# Build and install in development mode
maturin develop --release

# Or build a wheel for distribution
maturin build --release
pip install target/wheels/catparser-*.whl
```

## 📚 Usage

### Command Line Interface

```bash
# Using uv (recommended)
uv run catparser data.jsonl

# Or if installed globally
catparser data.jsonl

# Parse with custom chunk size
uv run catparser data.jsonl --chunk-size 50000

# Silent mode (no colorful output)
uv run catparser data.jsonl --quiet

# Show system information
uv run catparser --info
```

### Python API

#### Basic Usage

```python
from catparser import CatParser

# Create a parser instance
parser = CatParser()

# Parse a file
results = parser.parse("data.jsonl")

# Access results
print(f"Total articles: {results['total_articles']}")
print(f"Years range: {results['years_range']}")
print(f"Year distribution: {results['year_counts']}")
```

#### Custom Configuration

```python
from catparser import CatParser

# Create parser with custom settings
parser = CatParser(
    chunk_size=50000,  # Process 50k lines at a time
    verbose=True       # Show colorful progress output
)

results = parser.parse("large_dataset.jsonl")
```

#### Parse and Display

```python
from catparser import CatParser

# Parse and automatically display pretty results
parser = CatParser()
results = parser.parse_and_display("data.jsonl")
```

#### Convenience Function

```python
from catparser import parse_with_whiskers

# Quick parsing with one function call
results = parse_with_whiskers(
    "data.jsonl",
    chunk_size=10000,
    verbose=True,
    display=True  # Show pretty output
)
```

#### System Information

```python
from catparser import get_system_info

# Get info about available resources
info = get_system_info()
print(f"CPU cores: {info['cpu_count']}")
print(f"Recommended chunk size: {info['recommended_chunk_size']}")
```

### Advanced Usage

#### Analyze Results

```python
from catparser import CatParser

parser = CatParser(verbose=False)
results = parser.parse("data.jsonl")

# Analyze year distribution
for year, count in sorted(results['year_counts'].items()):
    print(f"{year}: {count} articles")

# Analyze version distribution
for versions, count in sorted(results['version_counts'].items()):
    print(f"{versions} versions: {count} articles")
```

#### Optimal Performance

```python
from catparser import CatParser, get_system_info

# Get system info
info = get_system_info()
cpu_count = info['cpu_count']

# Calculate optimal chunk size for your file
# Aim for 4x CPU count number of chunks
file_lines = 1_000_000
optimal_chunk_size = file_lines // (cpu_count * 4)

# Use optimal settings
parser = CatParser(chunk_size=optimal_chunk_size)
results = parser.parse("large_file.jsonl")
```

## 📂 Project Structure

```
DocumentParser/
├── Cargo.toml              # Rust package manifest
├── pyproject.toml          # Python package configuration
├── README.md               # This file
├── LICENSE                 # MIT License
├── .gitignore             # Git ignore rules
│
├── src/                    # Rust source code
│   ├── lib.rs             # Main library with PyO3 bindings
│   ├── parser.rs          # Core parsing logic
│   ├── cat_theme.rs       # Cat-themed output utilities
│   └── types.rs           # Data structures
│
├── python/                 # Python wrapper
│   └── catparser/
│       ├── __init__.py    # Python API
│       └── __main__.py    # CLI entry point
│
└── examples/               # Examples and sample data
    ├── basic_usage.py     # Usage examples
    └── sample_data.jsonl  # Sample data for testing
```

## 🎯 Input Format

CatParser expects JSON Lines format (`.jsonl`), where each line is a valid JSON object representing an arXiv document:

```json
{"id":"0704.0001","versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"}]}
{"id":"0704.0002","versions":[{"created":"Mon, 2 Apr 2007 20:24:56 GMT"},{"created":"Tue, 3 Apr 2007 10:15:30 GMT"}]}
```

Required fields:
- `versions`: Array of version objects
- `versions[0].created`: Creation date in format "Day, DD Mon YYYY HH:MM:SS TZ"

## 📊 Output Format

The parser returns a dictionary with the following structure:

```python
{
    'year_counts': {2007: 150, 2008: 200, ...},      # Articles per year
    'version_counts': {1: 500, 2: 300, 3: 100, ...}, # Articles by version count
    'total_articles': 1000,                           # Successfully parsed
    'total_errors': 5,                                # Failed to parse
    'years_range': (2007, 2023)                       # Min and max years
}
```

## 🎨 Colorful Output

When `verbose=True`, CatParser displays beautiful, colorful output with:

- 🐱 ASCII art cats for different statuses
- 🌈 Color-coded progress messages
- 📊 Pretty formatted statistics
- 🎭 Cat-themed puns and messages
- 📈 Visual bar charts for distributions

## 🧪 Running Examples

```bash
# Run the basic usage examples
python examples/basic_usage.py

# Try the sample data
catparser examples/sample_data.jsonl
```

## 🛠️ Development

### Building for Development

```bash
# Build the Rust extension in debug mode
maturin develop

# Build in release mode (much faster)
maturin develop --release
```

### Running Tests

```bash
# Run Rust tests
cargo test

# Run Python tests (if available)
pytest
```

### Formatting and Linting

```bash
# Format Rust code
cargo fmt

# Lint Rust code
cargo clippy

# Format Python code
black python/

# Lint Python code
ruff python/
```

## 🚀 Performance Tips

1. **Chunk Size**: Adjust based on file size
   - Small files (< 100k lines): Use default (10,000)
   - Medium files (100k - 1M lines): Use 50,000
   - Large files (> 1M lines): Use 100,000+

2. **CPU Cores**: More cores = faster processing
   - Default uses all available cores via Rayon
   - Automatically scales to your hardware

3. **Silent Mode**: Disable verbose output for maximum speed
   ```python
   parser = CatParser(verbose=False)
   ```

4. **Memory**: Parser streams data for efficient memory usage
   - No need to worry about large files
   - Memory usage stays constant

## 🐛 Troubleshooting

### Build Errors

**Problem**: `maturin: command not found`
```bash
pip install maturin
```

**Problem**: Rust not installed
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

**Problem**: Python.h not found
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# macOS
brew install python
```

### Runtime Errors

**Problem**: `ImportError: cannot import name 'catparser_rust'`
- Make sure you've built the extension: `maturin develop --release`

**Problem**: File not found
- Check the file path is correct
- Use absolute paths if relative paths don't work

**Problem**: Parsing errors
- Verify your JSON Lines format is correct
- Check that dates are in the expected format

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Built with [Rust](https://www.rust-lang.org/) 🦀
- Python bindings via [PyO3](https://pyo3.rs/)
- Parallel processing with [Rayon](https://github.com/rayon-rs/rayon)
- Colorful output with [colored](https://github.com/mackwic/colored)
- Cat-themed because cats are awesome! 🐱

## 📞 Support

If you encounter any issues or have questions:

1. Check the [examples](examples/) for usage patterns
2. Review this README for configuration options
3. Open an issue on GitHub

---

Made with ❤️ and 🐱 by the CatParser Team

**Meow-velous parsing awaits!** ✨
