"""
Pytest parameterization examples.

This module demonstrates various ways to use pytest.mark.parametrize:
- Basic parameterization with single parameter
- Multiple parameters
- Using fixture values as parameters
- Parameterizing with different data types
- Using ids for better test names
"""

import pytest
import math


# Basic parameterization with single parameter
@pytest.mark.parametrize("number", [1, 2, 3, 4, 5])
def test_number_is_positive(number):
    """Test that all provided numbers are positive."""
    assert number > 0


@pytest.mark.parametrize("number", [0, -1, -5, -10])
def test_number_is_not_positive(number):
    """Test that all provided numbers are not positive."""
    assert number <= 0


# Multiple parameters
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (2, 3, 5),
    (10, 5, 15),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_addition(a, b, expected):
    """Test addition with multiple parameter sets."""
    assert a + b == expected


@pytest.mark.parametrize("base, exponent, expected", [
    (2, 3, 8),
    (3, 2, 9),
    (5, 0, 1),
    (1, 100, 1),
    (10, 2, 100),
])
def test_exponentiation(base, exponent, expected):
    """Test exponentiation with multiple parameters."""
    assert base ** exponent == expected


# Using different data types
@pytest.mark.parametrize("value, expected_type", [
    (42, int),
    (3.14, float),
    ("hello", str),
    ([1, 2, 3], list),
    ({"key": "value"}, dict),
    (True, bool),
])
def test_type_checking(value, expected_type):
    """Test that values have expected types."""
    assert isinstance(value, expected_type)


# Using ids for better test names
@pytest.mark.parametrize("number, description", [
    (2, "even_small"),
    (4, "even_medium"),
    (100, "even_large"),
], ids=["small", "medium", "large"])
def test_even_numbers_with_ids(number, description):
    """Test even numbers with custom test IDs."""
    assert number % 2 == 0


# Parameterizing with complex data structures
@pytest.mark.parametrize("user_data", [
    {"name": "Alice", "age": 25, "email": "alice@example.com"},
    {"name": "Bob", "age": 30, "email": "bob@example.com"},
    {"name": "Charlie", "age": 35, "email": "charlie@example.com"},
])
def test_user_data_structure(user_data):
    """Test user data structure validation."""
    required_keys = {"name", "age", "email"}
    assert set(user_data.keys()) == required_keys
    assert isinstance(user_data["name"], str)
    assert isinstance(user_data["age"], int)
    assert "@" in user_data["email"]


# Parameterizing string operations
@pytest.mark.parametrize("text, expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("PyTest", "PYTEST"),
    ("", ""),
    ("123", "123"),
], ids=["lowercase", "mixed", "camelcase", "empty", "numbers"])
def test_string_uppercase(text, expected):
    """Test string uppercase conversion."""
    assert text.upper() == expected


# Mathematical operations with edge cases
@pytest.mark.parametrize("number, expected", [
    (0, 0),
    (1, 1),
    (4, 2),
    (9, 3),
    (16, 4),
    (25, 5),
])
def test_square_root(number, expected):
    """Test square root calculation."""
    assert math.sqrt(number) == expected


# Testing with boolean values
@pytest.mark.parametrize("value, expected", [
    (True, False),
    (False, True),
    (1, False),  # Truthy values
    (0, True),   # Falsy values
    ("", True),  # Empty string is falsy
    ("hello", False),  # Non-empty string is truthy
])
def test_boolean_negation(value, expected):
    """Test boolean negation logic."""
    assert (not bool(value)) == expected


# Combining parametrize with fixtures
@pytest.fixture
def multiplier():
    """Fixture providing a multiplier value."""
    return 3


@pytest.mark.parametrize("number", [1, 2, 3, 4, 5])
def test_multiplication_with_fixture(number, multiplier):
    """Test multiplication using both parametrize and fixture."""
    result = number * multiplier
    assert result == number * 3
    assert result % 3 == 0


# Multiple parametrize decorators
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_cartesian_product(x, y):
    """Test with cartesian product of parameters (generates 4 tests)."""
    assert x < y
    assert x + y > 0


# Parameterizing exception testing
@pytest.mark.parametrize("dividend, divisor", [
    (10, 0),
    (5, 0),
    (-3, 0),
])
def test_division_by_zero(dividend, divisor):
    """Test that division by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        dividend / divisor


# Using indirect parametrization (advanced)
@pytest.fixture
def calculation_input(request):
    """Fixture that processes parametrized input."""
    a, b, operation = request.param
    return {"a": a, "b": b, "operation": operation}


@pytest.mark.parametrize("calculation_input", [
    (5, 3, "add"),
    (10, 2, "subtract"),
    (4, 6, "multiply"),
], indirect=True)
def test_calculations_with_indirect(calculation_input):
    """Test calculations using indirect parametrization."""
    a = calculation_input["a"]
    b = calculation_input["b"]
    op = calculation_input["operation"]
    
    if op == "add":
        assert a + b > 0
    elif op == "subtract":
        assert isinstance(a - b, int)
    elif op == "multiply":
        assert a * b > 0