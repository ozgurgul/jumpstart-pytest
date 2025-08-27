"""
Basic pytest fixture examples.

This module demonstrates various types of pytest fixtures:
- Function scope fixtures (default)
- Module and session scope fixtures
- Fixture with setup and teardown
- Using fixtures in tests
"""

import pytest
import tempfile
import os


@pytest.fixture
def sample_data():
    """A simple fixture returning test data."""
    return {"name": "Alice", "age": 30, "city": "New York"}


@pytest.fixture
def number_list():
    """Fixture providing a list of numbers for testing."""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def temp_file():
    """Fixture that creates a temporary file and cleans it up."""
    # Setup: create a temporary file
    fd, temp_path = tempfile.mkstemp(suffix='.txt')
    with os.fdopen(fd, 'w') as f:
        f.write("Hello, pytest fixtures!")
    
    # Provide the file path to the test
    yield temp_path
    
    # Teardown: cleanup the temporary file
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture(scope="module")
def expensive_resource():
    """Module-scoped fixture - created once per test module."""
    print("\nSetting up expensive resource...")
    resource = {"connection": "database", "status": "connected"}
    yield resource
    print("\nTearing down expensive resource...")


@pytest.fixture(scope="session")
def global_config():
    """Session-scoped fixture - created once per test session."""
    return {
        "api_url": "https://api.example.com",
        "timeout": 30,
        "retries": 3
    }


# Tests using fixtures

def test_sample_data_content(sample_data):
    """Test that demonstrates using a simple fixture."""
    assert sample_data["name"] == "Alice"
    assert sample_data["age"] == 30
    assert sample_data["city"] == "New York"


def test_sample_data_keys(sample_data):
    """Another test using the same fixture."""
    expected_keys = {"name", "age", "city"}
    assert set(sample_data.keys()) == expected_keys


def test_number_list_operations(number_list):
    """Test using a list fixture."""
    assert len(number_list) == 5
    assert sum(number_list) == 15
    assert max(number_list) == 5
    assert min(number_list) == 1


def test_temp_file_exists(temp_file):
    """Test that uses a fixture with setup/teardown."""
    # The fixture created a temp file for us
    assert os.path.exists(temp_file)
    
    # Read the content
    with open(temp_file, 'r') as f:
        content = f.read()
    
    assert content == "Hello, pytest fixtures!"


def test_temp_file_write(temp_file):
    """Another test using the same temp file fixture."""
    # Each test gets its own temp file
    with open(temp_file, 'a') as f:
        f.write("\nAdditional content")
    
    with open(temp_file, 'r') as f:
        content = f.read()
    
    assert "Additional content" in content


def test_expensive_resource_usage(expensive_resource):
    """Test using a module-scoped fixture."""
    assert expensive_resource["connection"] == "database"
    assert expensive_resource["status"] == "connected"


def test_another_expensive_resource_usage(expensive_resource):
    """Another test using the same module-scoped fixture (reused)."""
    # This uses the same fixture instance as the previous test
    expensive_resource["last_accessed"] = "test_another_expensive_resource_usage"
    assert "last_accessed" in expensive_resource


def test_global_config_usage(global_config):
    """Test using a session-scoped fixture."""
    assert global_config["api_url"] == "https://api.example.com"
    assert global_config["timeout"] == 30
    assert global_config["retries"] == 3


def test_multiple_fixtures(sample_data, number_list, global_config):
    """Test that uses multiple fixtures at once."""
    assert isinstance(sample_data, dict)
    assert isinstance(number_list, list)
    assert isinstance(global_config, dict)
    
    # Combine data from different fixtures
    total_items = len(sample_data) + len(number_list) + len(global_config)
    assert total_items == 11  # 3 + 5 + 3