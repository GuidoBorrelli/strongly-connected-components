# Contributing to Strongly Connected Components

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs
- Check if the bug has already been reported in [Issues](../../issues)
- If not, create a new issue with:
  - Clear, descriptive title
  - Detailed description of the bug
  - Steps to reproduce
  - Expected vs actual behavior
  - Your environment (Python version, OS, etc.)

### Suggesting Enhancements
- Use the Issues page to suggest new features
- Provide clear description of the enhancement
- Explain why it would be useful
- List any alternative implementations you've considered

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/strongly-connected-components.git
   cd strongly-connected-components
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add docstrings to all functions
   - Add type hints where applicable
   - Include tests for new functionality

4. **Test your changes**
   ```bash
   python main.py
   ```

5. **Commit your changes**
   ```bash
   git commit -am "Add feature: description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Reference any related issues
   - Describe your changes clearly
   - Ensure all tests pass

## Code Style Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use descriptive variable and function names
- Add type hints to function signatures
- Write docstrings in Google style format
- Keep functions small and focused

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions/classes
- Update type hints
- Include examples for new features

## Testing

- Run correctness tests: `python main.py` (with `TEST=True`)
- Run benchmarks: `python main.py` (with `TEST=False`)
- Ensure all algorithms return consistent results

## Questions?

- Check the README.md first
- Look at existing issues and discussions
- Create a new discussion or issue

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing!

