# 🚀 CatParser Quick Start Guide

Get up and running with CatParser in minutes!

## 🎯 Prerequisites

- **Rust** 1.70+ ([Install Rust](https://rustup.rs/))
- **Python** 3.8+
- **pip** (Python package manager)

## ⚡ Quick Installation

### Step 1: Install Prerequisites

```bash
# Install Rust (if not installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Clone and Build with uv

```bash
# Clone the repository
git clone https://github.com/Boulaouaney/DocumentParser.git
cd DocumentParser

# Build and install with uv
uv build
uv pip install dist/catparser-*.whl

# Or sync from source
uv sync
```

### Step 3: Verify Installation

```bash
# Check installation
uv run catparser --info

# Test parsing
uv run catparser examples/sample_data.jsonl
```

## 🐱 Your First Parse

### Try the Sample Data

```bash
uv run catparser examples/sample_data.jsonl
```

You should see beautiful colorful output with ASCII cats! 🎨🐱

### Use in Python

```bash
# Start Python with uv
uv run python
```

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
uv run catparser data.jsonl

# Custom chunk size for large files
uv run catparser large_data.jsonl --chunk-size 50000

# Silent mode
uv run catparser data.jsonl --quiet
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
