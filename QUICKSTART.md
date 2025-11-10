# 🚀 CatParser Quick Start Guide

Get up and running with CatParser in minutes!

## 🎯 Prerequisites

- **Rust** 1.70+ ([Install Rust](https://rustup.rs/))
- **Python** 3.8+
- **pip** (Python package manager)

## ⚡ Quick Installation

### Step 1: Install Rust (if not installed)

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### Step 2: Clone and Build

```bash
# Clone the repository
git clone https://github.com/Boulaouaney/DocumentParser.git
cd DocumentParser

# Install maturin
pip install maturin

# Build and install (this takes a minute)
maturin build --release
pip install target/wheels/catparser-*.whl

# Add Python wrapper to your path
export PYTHONPATH=$PWD/python:$PYTHONPATH
```

### Step 3: Verify Installation

```bash
python3 -c "import catparser_rust; print('✅ Rust module works!')"
python3 -m catparser --info
```

## 🐱 Your First Parse

### Try the Sample Data

```bash
python3 -m catparser examples/sample_data.jsonl
```

You should see beautiful colorful output with ASCII cats! 🎨🐱

### Use in Python

```python
from catparser import CatParser

# Create parser
parser = CatParser()

# Parse a file
results = parser.parse("examples/sample_data.jsonl")

# Check results
print(f"Parsed {results['total_articles']} articles!")
print(f"Years: {results['years_range']}")
```

### Use from Command Line

```bash
# Parse with pretty output
python3 -m catparser data.jsonl

# Custom chunk size for large files
python3 -m catparser large_data.jsonl --chunk-size 50000

# Silent mode
python3 -m catparser data.jsonl --quiet
```

## 📊 Expected Output

When you run CatParser, you'll see:

1. 🎨 **Beautiful Banner** - Colorful ASCII art header
2. 🐱 **Cat Mascot** - ASCII art cat showing progress
3. 🌈 **Colored Progress** - Real-time parsing updates
4. 📈 **Statistics** - Articles count, processing time, throughput
5. 📊 **Charts** - Visual bar charts of year and version distributions

## 🎓 Next Steps

1. **Read the [Full README](README.md)** for detailed documentation
2. **Check [examples/basic_usage.py](examples/basic_usage.py)** for more examples
3. **Try parsing your own data** - any JSON Lines file with arXiv format

## 🐛 Troubleshooting

### "Module not found" errors

```bash
# Make sure PYTHONPATH is set
export PYTHONPATH=$PWD/python:$PYTHONPATH

# Or add to your ~/.bashrc for persistence
echo 'export PYTHONPATH=/path/to/DocumentParser/python:$PYTHONPATH' >> ~/.bashrc
```

### Build errors

```bash
# Make sure Rust is installed and updated
rustup update

# Rebuild from scratch
cargo clean
maturin build --release
```

### Import errors

```bash
# Verify Rust module is built
python3 -c "import catparser_rust; print('OK')"

# Check installation
pip list | grep catparser
```

## 💡 Pro Tips

1. **For large files**: Increase chunk size
   ```bash
   python3 -m catparser huge_file.jsonl --chunk-size 100000
   ```

2. **For maximum speed**: Use silent mode
   ```python
   parser = CatParser(verbose=False)
   results = parser.parse("data.jsonl")
   ```

3. **Check system resources**:
   ```bash
   python3 -m catparser --info
   ```

## 🎉 You're Ready!

You're now ready to parse documents at blazing speed with delightful cat-themed output!

For more information, check the [README](README.md) or run:
```bash
python3 -m catparser --help
```

Happy purr-sing! 🐱✨
