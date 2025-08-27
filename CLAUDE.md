# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Python repository named "jumpstart-pytest" designed for learning and demonstrating pytest testing techniques. The repository contains example test files organized by skill level:

- **pytest**: Rudimentary examples covering fixtures, loops, assertions, parameterization, and conditional testing
- **pytest-levelup**: Intermediate examples featuring Python classes and advanced testing patterns

## Quick Start

To get started with this pytest learning repository:

```bash
# Clone and navigate to the repository
cd jumpstart-pytest

# Install pytest (if not already installed)
pip install pytest

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests in a specific directory
pytest pytest/          # Run basic examples
pytest pytest-levelup/  # Run intermediate examples

# Run specific test files
pytest pytest/test_fixtures.py
pytest pytest-levelup/test_classes.py
```

## Project Structure

Current structure:
- `.gitignore`: Comprehensive Python gitignore covering multiple package managers and development tools
- `.git/`: Git repository initialization
- `pytest/`: Directory containing rudimentary pytest examples (fixtures, loops, assertions, parameterization, conditionals)
- `pytest-levelup/`: Directory containing intermediate pytest examples with Python classes
- `CLAUDE.md`: This guidance file

## Development Environment

This repository is designed to work with minimal setup - just Python and pytest. For enhanced development:

```bash
# Basic setup
pip install pytest

# For enhanced testing features
pip install pytest-cov      # Coverage reporting
pip install pytest-xdist    # Parallel test execution
pip install pytest-mock     # Mocking utilities
```

The comprehensive `.gitignore` supports multiple Python package managers if you want to use them:
- **pip**: Traditional Python package installer
- **poetry**: Modern dependency management
- **uv**: Fast Python package installer
- **pdm**: Python dependency manager

## Testing Framework - pytest

This repository focuses specifically on pytest testing patterns and techniques:

### Core pytest Features Demonstrated
- **Fixtures**: Reusable test setup and teardown
- **Parameterization**: Running same test with different inputs  
- **Assertions**: Built-in assertion introspection
- **Markers**: Custom test categorization
- **Classes**: Organized test grouping

### Key pytest Commands
```bash
pytest                    # Run all tests
pytest -v                # Verbose output
pytest -s                # Show print statements
pytest -x                # Stop on first failure
pytest --tb=short        # Shorter traceback
pytest -k "pattern"      # Run tests matching pattern
pytest --collect-only    # Show discoverable tests
pytest pytest/           # Run specific directory
pytest -m "marker"       # Run tests with specific marker
```

## Common Development Tasks

Essential commands for working with this pytest learning repository:

### Running Tests
```bash
# Basic test execution
pytest                           # Run all tests
pytest pytest/                  # Run basic examples only
pytest pytest-levelup/          # Run intermediate examples only

# Development workflow
pytest -v                       # Verbose output to see what's being tested
pytest -s                       # Show print statements (useful for debugging)
pytest --tb=short              # Shorter tracebacks for cleaner output

# Learning-focused commands  
pytest --collect-only           # See all available tests without running
pytest -k "fixture"            # Run only tests with "fixture" in the name
pytest -k "not slow"           # Skip tests marked as slow
```

### Adding New Tests
```bash
# Create new test files following pytest naming convention
touch pytest/test_new_feature.py
touch pytest-levelup/test_advanced_feature.py

# Run your new tests to verify they work
pytest pytest/test_new_feature.py -v
```

### Development Setup
```bash
pip install pytest              # Basic installation
pip install pytest pytest-cov  # With coverage reporting
```

## Code Standards

When adding new tests to this learning repository:

### File Naming
- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_function_name()`
- Test classes: `TestClassName`
- Test methods in classes: `test_method_name()`

### Organization
- **Basic examples** go in `pytest/` directory
- **Intermediate/advanced examples** go in `pytest-levelup/` directory
- Group related tests in the same file
- Use descriptive test names that explain what is being tested

### Best Practices
- Write clear, focused test functions
- Use fixtures for common setup/teardown
- Add docstrings to explain complex test scenarios
- Use parametrize for testing multiple inputs
- Include both positive and negative test cases

### Example Test Structure
```python
import pytest

@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_something_works(sample_data):
    """Test that demonstrates a specific pytest feature."""
    assert sample_data["key"] == "value"

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 3),
])
def test_with_parameters(input, expected):
    assert input + 1 == expected
```

## Notes

This repository serves as a hands-on learning environment for pytest. Each test file demonstrates specific pytest features and patterns. Use this repository to practice writing tests, experiment with pytest features, and build confidence with Python testing.