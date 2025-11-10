# 🐱 CatParser Quick Start Guide

Welcome to CatParser! This guide will get you up and running in no time!

## 🚀 Installation

```bash
# Using uv (recommended - super fast!)
uv pip install -e .

# Using regular pip
pip install -e .
```

## 🎯 First Parse

Try parsing the included sample data:

```bash
catparser parse examples/sample_data.jsonl
```

You should see:
- 🎨 Beautiful cat-themed banner
- 📊 Progress bars showing parsing progress
- 📈 Summary tables with results
- 🖼️ Generated plots (saved as PNG)

## 💻 Command Line Usage

### Basic Commands

```bash
# Parse with default settings
catparser parse data.jsonl

# Specify output directory
catparser parse data.jsonl --output ./my-results

# Use more CPU cores (4 cores in this example)
catparser parse data.jsonl --processes 4

# Skip plots (faster)
catparser parse data.jsonl --no-plots

# Quiet mode
catparser parse data.jsonl --quiet
```

### Fun Commands

```bash
# Just meow at you!
catparser meow

# Test performance with different core counts
catparser purrformance examples/sample_data.jsonl

# Show version
catparser --version
```

### Cat-Themed Aliases

All of these work the same:

```bash
catparser parse data.jsonl
meow-parser parse data.jsonl
purr-parse parse data.jsonl
```

## 🐍 Python API

### Quick Start

```python
from catparser import parse_documents_with_whiskers

# One-liner parsing!
results = parse_documents_with_whiskers("data.jsonl")

print(f"Parsed {results['total_articles']} articles!")
```

### More Control

```python
from catparser import KittenParser

# Create parser
parser = KittenParser(num_processes=4)

# Parse documents
results = parser.parse(
    file_path="data.jsonl",
    output_dir="./results",
    create_plots=True
)

# Use results
for year, count in results['year_counts'].items():
    print(f"{year}: {count} articles")
```

## 📊 Understanding Results

After parsing, you'll get:

1. **Console Output**: Beautiful tables showing:
   - Total articles processed
   - Year distribution
   - Version statistics
   - Error counts

2. **Plots** (if enabled): PNG file with:
   - Articles by year (bar chart)
   - Version distribution (bar chart)

3. **Results Dictionary** (Python API):
   ```python
   {
       'total_articles': 1000,
       'year_counts': {2020: 300, 2021: 400, ...},
       'version_counts': {1: 500, 2: 300, ...},
       'total_errors': 5,
       'error_samples': [...]
   }
   ```

## 🎨 Example Output

```
╭──────────────────── 🐱 Welcome! 🐱 ─────────────────────╮
│                  CatParser                               │
│                                                          │
│     /\_/\                                                │
│    ( o.o )                                               │
│     > ^ <                                                │
│                                                          │
│  Whisker-sharp document analysis! 🎯                     │
╰──────────────────────────────────────────────────────────╯

🐾 Parsing documents with whiskers... ━━━━━━ 100% 0:00:05

         🐱 Parsing Summary
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Metric                ┃    Value ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Total Articles        │   18     │
│ Total Errors          │    0     │
│ Success Rate          │ 100.00%  │
└───────────────────────┴──────────┘
```

## 🔧 Troubleshooting

### File Not Found
```bash
# Make sure file path is correct
ls examples/sample_data.jsonl

# Use absolute path if needed
catparser parse /full/path/to/data.jsonl
```

### Performance Issues
```bash
# Try different core counts
catparser purrformance data.jsonl

# Or manually adjust
catparser parse data.jsonl --processes 8
```

### Import Errors
```bash
# Reinstall in development mode
uv pip install -e .

# Or with all dependencies
uv pip install -e ".[dev]"
```

## 📚 Next Steps

1. Run the example script:
   ```bash
   python examples/example_usage.py
   ```

2. Try with your own data:
   - Prepare a JSON lines file
   - Each line should be a valid JSON object
   - Include "versions" field with creation dates

3. Check out the main [README.md](../README.md) for more details!

## 🎉 Have Fun!

Remember: Parsing data should be enjoyable! That's why we added cats! 😺

```
  /\_/\
 ( ^.^ )  < "Happy parsing!"
  > ^ <
```
