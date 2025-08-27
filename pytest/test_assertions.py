"""
Pytest assertion examples.

This module demonstrates various types of assertions in pytest:
- Basic equality and inequality assertions
- Membership testing
- Exception testing
- Approximate equality for floats
- String matching and containment
- Collection assertions
- Boolean assertions
"""

import pytest
import math
import re


def test_basic_equality():
    """Test basic equality assertions."""
    assert 1 + 1 == 2
    assert "hello" == "hello"
    assert [1, 2, 3] == [1, 2, 3]
    assert {"key": "value"} == {"key": "value"}


def test_inequality_assertions():
    """Test various inequality assertions."""
    assert 5 > 3
    assert 2 < 10
    assert 5 >= 5
    assert 3 <= 7
    assert 4 != 5


def test_membership_assertions():
    """Test membership using 'in' and 'not in'."""
    # List membership
    assert 3 in [1, 2, 3, 4, 5]
    assert 6 not in [1, 2, 3, 4, 5]
    
    # String containment
    assert "test" in "This is a test string"
    assert "xyz" not in "This is a test string"
    
    # Dictionary key membership
    data = {"name": "Alice", "age": 30}
    assert "name" in data
    assert "email" not in data


def test_boolean_assertions():
    """Test boolean value assertions."""
    assert True
    assert not False
    assert bool(1)
    assert not bool(0)
    assert bool("hello")
    assert not bool("")
    assert bool([1, 2, 3])
    assert not bool([])


def test_none_assertions():
    """Test None value assertions."""
    value = None
    assert value is None
    
    other_value = "not none"
    assert other_value is not None


def test_type_assertions():
    """Test type checking assertions."""
    assert isinstance(42, int)
    assert isinstance(3.14, float)
    assert isinstance("hello", str)
    assert isinstance([1, 2, 3], list)
    assert isinstance({"key": "value"}, dict)
    
    # Negative type assertions
    assert not isinstance(42, str)
    assert not isinstance("hello", int)


def test_approximate_equality():
    """Test approximate equality for floating point numbers."""
    # Using pytest.approx for floating point comparisons
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert math.pi == pytest.approx(3.14159, rel=1e-4)
    assert math.sqrt(2) == pytest.approx(1.414213, abs=1e-5)
    
    # Approximate equality for lists
    assert [0.1 + 0.2, 0.3 + 0.4] == pytest.approx([0.3, 0.7])


def test_string_assertions():
    """Test string-specific assertions."""
    text = "Hello, World!"
    
    # Basic string operations
    assert text.startswith("Hello")
    assert text.endswith("World!")
    assert "World" in text
    assert text.lower() == "hello, world!"
    assert text.upper() == "HELLO, WORLD!"
    assert len(text) == 13


def test_list_assertions():
    """Test list-specific assertions."""
    numbers = [1, 2, 3, 4, 5]
    
    assert len(numbers) == 5
    assert numbers[0] == 1
    assert numbers[-1] == 5
    assert sum(numbers) == 15
    assert max(numbers) == 5
    assert min(numbers) == 1
    assert sorted(numbers) == numbers  # Already sorted


def test_dictionary_assertions():
    """Test dictionary-specific assertions."""
    person = {
        "name": "Alice",
        "age": 30,
        "city": "New York",
        "skills": ["Python", "pytest", "testing"]
    }
    
    assert len(person) == 4
    assert person["name"] == "Alice"
    assert "age" in person
    assert person.get("country", "USA") == "USA"  # Default value
    assert len(person["skills"]) == 3


def test_exception_assertions():
    """Test that specific exceptions are raised."""
    
    # Test that ZeroDivisionError is raised
    with pytest.raises(ZeroDivisionError):
        1 / 0
    
    # Test that ValueError is raised with specific message
    with pytest.raises(ValueError, match="invalid literal"):
        int("not_a_number")
    
    # Test that TypeError is raised
    with pytest.raises(TypeError):
        "string" + 42
    
    # Capture exception info for further testing
    with pytest.raises(ZeroDivisionError) as exc_info:
        10 / 0
    
    assert "division by zero" in str(exc_info.value)


def test_multiple_assertions():
    """Test multiple related assertions together."""
    data = {"numbers": [1, 2, 3, 4, 5], "total": 15}
    
    # Multiple assertions about the same data
    assert "numbers" in data
    assert "total" in data
    assert len(data["numbers"]) == 5
    assert sum(data["numbers"]) == data["total"]
    assert all(isinstance(n, int) for n in data["numbers"])


def test_regex_matching():
    """Test regular expression matching."""
    email = "test@example.com"
    phone = "123-456-7890"
    
    # Basic pattern matching
    assert re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
    assert re.match(r"^\d{3}-\d{3}-\d{4}$", phone)
    
    # Using search instead of match
    text = "The price is $25.99"
    price_match = re.search(r"\$(\d+\.\d{2})", text)
    assert price_match is not None
    assert price_match.group(1) == "25.99"


def test_custom_assertion_messages():
    """Test assertions with custom error messages."""
    x = 5
    y = 10
    
    # Custom message for clarity
    assert x < y, f"Expected {x} to be less than {y}"
    
    # More complex custom message
    items = [1, 2, 3]
    assert len(items) > 0, f"List should not be empty, but got: {items}"


def test_range_assertions():
    """Test values within ranges."""
    temperature = 25
    
    # Check if value is in range
    assert 0 <= temperature <= 100
    assert temperature in range(20, 30)
    
    # Check multiple values in range
    temperatures = [22, 25, 28, 31]
    assert all(t >= 20 for t in temperatures)
    assert any(t > 30 for t in temperatures)


def test_set_assertions():
    """Test set operations and assertions."""
    set1 = {1, 2, 3, 4}
    set2 = {3, 4, 5, 6}
    
    assert len(set1) == 4
    assert 3 in set1
    assert 7 not in set1
    
    # Set operations
    assert set1.intersection(set2) == {3, 4}
    assert set1.union(set2) == {1, 2, 3, 4, 5, 6}
    assert set1.difference(set2) == {1, 2}


def test_conditional_assertions():
    """Test assertions with conditional logic."""
    age = 25
    
    if age >= 18:
        assert age >= 18, "Should be adult"
        status = "adult"
    else:
        assert age < 18, "Should be minor"
        status = "minor"
    
    assert status == "adult"


def helper_function(x, y):
    """Helper function for testing function calls."""
    if x == 0:
        raise ValueError("x cannot be zero")
    return x + y


def test_function_calls():
    """Test function call results and exceptions."""
    # Test normal function call
    result = helper_function(5, 3)
    assert result == 8
    
    # Test function raises exception
    with pytest.raises(ValueError, match="x cannot be zero"):
        helper_function(0, 5)