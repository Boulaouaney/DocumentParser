# 🐱 Contributing to CatParser

Thank you for your interest in contributing to CatParser! We love contributions almost as much as we love cats! 😻

## 🐾 Ways to Contribute

- 🐛 **Bug Reports**: Found a bug? Let us know!
- 💡 **Feature Requests**: Have an idea? We'd love to hear it!
- 📝 **Documentation**: Improve our docs or add examples
- 🎨 **More Cat Puns**: We can never have too many!
- 🧪 **Tests**: Help us keep the code purr-fect
- 🔧 **Code**: Fix bugs or add features

## 🚀 Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/DocumentParser.git
cd DocumentParser
```

### 2. Set Up Development Environment

```bash
# Install with development dependencies
uv pip install -e ".[dev]"

# Or with regular pip
pip install -e ".[dev]"
```

### 3. Create a Branch

```bash
git checkout -b feature/your-awesome-feature
# or
git checkout -b fix/bug-description
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=catparser --cov-report=html

# Run specific test file
pytest tests/test_parser.py

# Run with verbose output
pytest -v
```

## 🎨 Code Style

We use these tools to keep our code clean:

```bash
# Format code with black
black src/

# Lint with ruff
ruff check src/

# Type check with mypy
mypy src/
```

### Code Guidelines

- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions focused and small
- Add cat puns where appropriate! 😺
- Follow PEP 8 style guide

## 📝 Commit Messages

Write clear, descriptive commit messages:

```bash
# Good
git commit -m "Add support for CSV output format"
git commit -m "Fix memory leak in chunk processing"
git commit -m "Add more cat ASCII art because why not"

# Not so good
git commit -m "fix stuff"
git commit -m "updates"
```

## 🔄 Pull Request Process

1. **Update tests**: Add tests for new features
2. **Update docs**: Document new features or changes
3. **Run tests**: Make sure all tests pass
4. **Format code**: Run black and ruff
5. **Create PR**: Write a clear description of changes

### PR Title Format

```
[Type] Brief description

Types:
- [Feature] New functionality
- [Fix] Bug fixes
- [Docs] Documentation changes
- [Test] Test additions/changes
- [Refactor] Code refactoring
- [Cat] More cat-related improvements 😺
```

## 🐱 Adding Cat Puns

We love cat puns! When adding new cat puns:

1. Add them to `src/catparser/cat_art.py`
2. Make sure they're family-friendly
3. Test that they display correctly
4. The more groan-inducing, the better!

Example:
```python
CAT_PUNS = [
    "Pawsitively parsing! 🐾",
    "Your new pun here! 😺",
]
```

## 🎨 Adding Cat ASCII Art

New cat art is always welcome!

```python
NEW_CAT = r"""
  /\_/\
 ( o.o )
  > ^ <
"""
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

- **Description**: What went wrong?
- **Steps to Reproduce**: How can we see the bug?
- **Expected Behavior**: What should happen?
- **Actual Behavior**: What actually happened?
- **Environment**: OS, Python version, etc.
- **Cat Pictures**: Optional but appreciated! 😺

## 💡 Feature Requests

For feature requests, describe:

- **Problem**: What problem does this solve?
- **Solution**: What's your proposed solution?
- **Alternatives**: Any alternative solutions?
- **Cat Theme**: How can we make it cat-themed? 🐱

## 📚 Documentation

Improving documentation is a great way to contribute!

- Fix typos or unclear explanations
- Add examples
- Improve docstrings
- Create tutorials
- Add more cat puns to the docs

## 🌟 Recognition

Contributors will be:

- Listed in our contributors section
- Given virtual cat treats 🐱🍪
- Thanked profusely
- Appreciated forever!

## ❓ Questions?

- Open an issue for questions
- Check existing issues and PRs
- Read the documentation

## 🎉 Thank You!

Thank you for making CatParser more paw-some! Every contribution, no matter how small, is appreciated!

```
  /\_/\
 ( ^.^ )  < "Thanks for contributing!"
  > ^ <
```

---

**Remember**: Be kind, have fun, and keep it cat-themed! 😻
