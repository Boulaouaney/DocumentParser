# 🧪 Testing Guide for CatParser

Comprehensive testing suite for the CatParser document parser.

## 📊 Test Coverage

### Rust Tests (13 total)
- **Unit Tests**: 2 tests in `src/parser.rs`
- **Integration Tests**: 11 tests in `tests/integration_tests.rs`
- **All tests passing** ✅

### Python Tests (19 total)
- **Unit Tests**: 9 tests for CatParser class
- **Convenience Function Tests**: 3 tests
- **Results Structure Tests**: 4 tests
- **Real World Scenario Tests**: 3 tests
- **All tests passing** ✅

### Total: 32 Tests ✅

---

## 🚀 Running Tests

### Run All Rust Tests

```bash
# Run all Rust tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_parse_valid_documents

# Run in release mode (faster)
cargo test --release
```

### Run All Python Tests

```bash
# Set Python path
export PYTHONPATH=$PWD/python:$PYTHONPATH

# Run all Python tests
python3 -m pytest python/tests/ -v

# Run with coverage
python3 -m pytest python/tests/ --cov=catparser

# Run specific test class
python3 -m pytest python/tests/test_catparser.py::TestCatParser -v

# Run specific test
python3 -m pytest python/tests/test_catparser.py::TestCatParser::test_parse_valid_data -v
```

### Run All Tests Together

```bash
# Rust tests
cargo test --quiet

# Python tests
export PYTHONPATH=$PWD/python:$PYTHONPATH
python3 -m pytest python/tests/ -v
```

---

## 📁 Test Structure

```
DocumentParser/
├── tests/
│   ├── integration_tests.rs      # Rust integration tests
│   └── data/                      # Test data files
│       ├── large_dataset.jsonl   # 25 documents spanning 2007-2024
│       ├── error_cases.jsonl     # Documents with various errors
│       ├── edge_cases.jsonl      # Edge cases (unicode, versions, etc.)
│       └── performance_test.jsonl # Performance testing data
│
├── python/tests/
│   ├── __init__.py
│   └── test_catparser.py         # Python unit tests
│
└── examples/
    └── sample_data.jsonl          # Sample data for demos
```

---

## 🧪 Test Categories

### 1. Unit Tests (Rust)

Located in `src/parser.rs`:

```rust
#[test]
fn test_parse_line() { ... }

#[test]
fn test_parse_results_merge() { ... }
```

**What they test:**
- Individual line parsing
- Date extraction
- Results merging logic

### 2. Integration Tests (Rust)

Located in `tests/integration_tests.rs`:

#### Basic Functionality
- ✅ `test_parse_valid_documents` - Parse valid JSON Lines
- ✅ `test_parse_empty_file` - Handle empty files
- ✅ `test_parse_with_errors` - Graceful error handling

#### Data Validation
- ✅ `test_parse_multiple_years` - Multiple year ranges
- ✅ `test_parse_multiple_versions` - Version counting
- ✅ `test_malformed_dates` - Invalid date formats
- ✅ `test_unicode_content` - Unicode support

#### Performance & Scaling
- ✅ `test_parse_with_different_chunk_sizes` - Chunk size variations
- ✅ `test_large_file_simulation` - 10,000 document test
- ✅ `test_parse_results_merge` - Results aggregation
- ✅ `test_parse_results_finalize` - Year range calculation

### 3. Python Unit Tests

Located in `python/tests/test_catparser.py`:

#### TestCatParser Class
- ✅ Parser initialization with various settings
- ✅ Valid data parsing
- ✅ Empty file handling
- ✅ Error handling
- ✅ Different chunk sizes
- ✅ Nonexistent file errors
- ✅ Optimal chunk size calculation
- ✅ Verbose and silent modes

#### TestConvenienceFunctions
- ✅ `parse_with_whiskers()` function
- ✅ Display mode
- ✅ System information retrieval

#### TestResultsStructure
- ✅ Results dictionary structure
- ✅ Year counts format
- ✅ Version counts format
- ✅ Years range format

#### TestRealWorldScenarios
- ✅ Large dataset (1000 documents)
- ✅ Mixed valid/invalid data
- ✅ Unicode handling

---

## 📝 Test Data

### Sample Data Files

#### `tests/data/large_dataset.jsonl`
- 25 documents
- Years: 2007-2024
- Various version counts (1-3 versions)
- **Use for**: General testing

#### `tests/data/error_cases.jsonl`
- 9 lines total
- 3 valid documents
- 6 various error types:
  - Invalid JSON syntax
  - Missing versions field
  - Empty versions array
  - Invalid date formats
  - Missing created field
  - Malformed data
- **Use for**: Error handling tests

#### `tests/data/edge_cases.jsonl`
- 10 documents
- Edge cases:
  - Single to ten versions
  - Old dates (1991)
  - Recent dates (2024)
  - Unicode titles (Chinese, Russian, emoji)
  - Long IDs
  - Special characters
- **Use for**: Edge case validation

#### `tests/data/performance_test.jsonl`
- 20 documents
- Sequential dates
- **Use for**: Performance benchmarking

---

## 🎯 What Each Test Validates

### Parsing Correctness
- ✅ Accurate year extraction
- ✅ Correct version counting
- ✅ Proper error counting
- ✅ Date format parsing

### Error Handling
- ✅ Graceful handling of invalid JSON
- ✅ Missing field handling
- ✅ Malformed date handling
- ✅ File not found errors

### Performance
- ✅ Parallel processing works
- ✅ Chunk-based processing
- ✅ Large file handling (10k+ documents)
- ✅ Memory efficiency

### Data Integrity
- ✅ Results merging accuracy
- ✅ Year range calculation
- ✅ Count aggregation
- ✅ Unicode support

### API Correctness
- ✅ Python bindings work
- ✅ Return values correct
- ✅ Function signatures
- ✅ Error propagation

---

## 🔍 Adding New Tests

### Adding a Rust Test

```rust
// In tests/integration_tests.rs
#[test]
fn test_your_new_feature() {
    let data = r#"{"id":"test","versions":[{"created":"Mon, 1 Jan 2020 10:00:00 GMT"}]}"#;
    let (_dir, path) = create_test_file(data);
    let results = parse_file(&path, 1000, false).unwrap();

    assert_eq!(results.total_articles, 1);
    // Add more assertions
}
```

### Adding a Python Test

```python
# In python/tests/test_catparser.py
def test_your_new_feature(self, tmp_path):
    """Test description"""
    test_file = tmp_path / "test.jsonl"
    # Create test data

    parser = CatParser(verbose=False)
    results = parser.parse(str(test_file))

    assert results['total_articles'] == expected_count
    # Add more assertions
```

---

## 📈 Test Statistics

### Rust Tests
- **Total**: 13 tests
- **Unit**: 2 tests
- **Integration**: 11 tests
- **Pass Rate**: 100% ✅
- **Execution Time**: ~0.07s

### Python Tests
- **Total**: 19 tests
- **Test Classes**: 4
- **Pass Rate**: 100% ✅
- **Execution Time**: ~0.13s

### Combined
- **Total Tests**: 32
- **Total Pass Rate**: 100% ✅
- **Combined Execution Time**: ~0.20s

---

## 🐛 Debugging Failed Tests

### Rust Test Failures

```bash
# Run with full output
cargo test -- --nocapture

# Run specific test with trace
RUST_BACKTRACE=1 cargo test test_name

# Check for memory issues (requires valgrind)
cargo test --target x86_64-unknown-linux-gnu
valgrind target/debug/deps/catparser_rust-*
```

### Python Test Failures

```bash
# Run with verbose output
python3 -m pytest python/tests/ -vv

# Run with print statements
python3 -m pytest python/tests/ -s

# Run with pdb debugger
python3 -m pytest python/tests/ --pdb

# Get detailed failure info
python3 -m pytest python/tests/ -vv --tb=long
```

---

## ✅ Test Checklist

Before committing code, ensure:

- [ ] All Rust tests pass: `cargo test`
- [ ] All Python tests pass: `pytest python/tests/`
- [ ] New features have corresponding tests
- [ ] Edge cases are covered
- [ ] Error cases are tested
- [ ] Documentation is updated
- [ ] No warnings in test output

---

## 📊 Continuous Testing

### Watch Mode (Rust)

```bash
# Install cargo-watch
cargo install cargo-watch

# Run tests on file changes
cargo watch -x test
```

### Watch Mode (Python)

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests on file changes
export PYTHONPATH=$PWD/python:$PYTHONPATH
ptw python/tests/
```

---

## 🎉 Test Results Summary

```
╔════════════════════════════════════════╗
║     🧪 CatParser Test Suite 🧪        ║
╚════════════════════════════════════════╝

Rust Tests:     13/13 passed ✅
Python Tests:   19/19 passed ✅
Total Tests:    32/32 passed ✅

Coverage:       Comprehensive
Performance:    Fast (~0.2s total)
Status:         All Systems Go! 🚀

🐱 Paws-itively tested! 🐱
```

---

## 📚 Further Reading

- [Rust Testing Documentation](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [PyO3 Testing Guide](https://pyo3.rs/latest/testing.html)

---

**Happy Testing! 🧪✨**
