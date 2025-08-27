"""
Pytest mocking examples.

This module demonstrates various mocking patterns using unittest.mock:
- Basic mocking with patch decorator
- Mock objects and return values
- Mocking class methods and attributes
- Patch context managers
- Mock side effects and exceptions
- Spy patterns and call verification
- Advanced mocking scenarios
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call, mock_open
import requests
import os
import json


# Example classes and functions to mock
class EmailService:
    """Email service class for demonstration."""
    
    def send_email(self, to, subject, body):
        """Send an email (would normally make external API call)."""
        # This would normally make an actual API call
        response = requests.post("https://api.emailservice.com/send", {
            "to": to,
            "subject": subject,
            "body": body
        })
        return response.status_code == 200
    
    def get_email_count(self, user_id):
        """Get email count for user."""
        response = requests.get(f"https://api.emailservice.com/count/{user_id}")
        return response.json().get("count", 0)


class UserManager:
    """User manager class with external dependencies."""
    
    def __init__(self, email_service=None):
        self.email_service = email_service or EmailService()
        self.users = {}
    
    def create_user(self, username, email):
        """Create a new user and send welcome email."""
        user = {"username": username, "email": email, "id": len(self.users) + 1}
        self.users[username] = user
        
        # Send welcome email
        welcome_sent = self.email_service.send_email(
            to=email,
            subject="Welcome!",
            body=f"Welcome {username}!"
        )
        
        user["welcome_sent"] = welcome_sent
        return user
    
    def get_user_stats(self, username):
        """Get user statistics including email count."""
        if username not in self.users:
            return None
        
        user = self.users[username]
        email_count = self.email_service.get_email_count(user["id"])
        
        return {
            "username": username,
            "email": user["email"],
            "email_count": email_count
        }


def fetch_user_data(user_id):
    """Function that fetches user data from external API."""
    response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    if response.status_code == 200:
        return response.json()
    return None


def save_to_file(filename, data):
    """Function that saves data to a file."""
    with open(filename, 'w') as f:
        json.dump(data, f)
    return True


def read_config_file(filename):
    """Function that reads configuration from file."""
    with open(filename, 'r') as f:
        return json.load(f)


# Basic mocking tests

@patch('requests.get')
def test_fetch_user_data_success(mock_get):
    """Test successful API call with mock."""
    # Configure mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    }
    mock_get.return_value = mock_response
    
    # Call function
    result = fetch_user_data(1)
    
    # Assertions
    assert result["name"] == "John Doe"
    assert result["email"] == "john@example.com"
    mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/users/1")


@patch('requests.get')
def test_fetch_user_data_failure(mock_get):
    """Test API call failure with mock."""
    # Configure mock to return error response
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    # Call function
    result = fetch_user_data(999)
    
    # Assertions
    assert result is None
    mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/users/999")


# Mocking with patch decorator on class methods

class TestEmailService:
    """Test class demonstrating method mocking."""
    
    @patch('requests.post')
    def test_send_email_success(self, mock_post):
        """Test successful email sending."""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Create service and test
        service = EmailService()
        result = service.send_email("test@example.com", "Test", "Hello")
        
        # Assertions
        assert result is True
        mock_post.assert_called_once_with("https://api.emailservice.com/send", {
            "to": "test@example.com",
            "subject": "Test", 
            "body": "Hello"
        })
    
    @patch('requests.post')
    def test_send_email_failure(self, mock_post):
        """Test email sending failure."""
        # Setup mock to return error
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        # Test
        service = EmailService()
        result = service.send_email("test@example.com", "Test", "Hello")
        
        # Assertions
        assert result is False
    
    @patch('requests.get')
    def test_get_email_count(self, mock_get):
        """Test getting email count."""
        # Setup mock
        mock_response = Mock()
        mock_response.json.return_value = {"count": 25}
        mock_get.return_value = mock_response
        
        # Test
        service = EmailService()
        count = service.get_email_count(123)
        
        # Assertions
        assert count == 25
        mock_get.assert_called_once_with("https://api.emailservice.com/count/123")


# Mocking with dependency injection

class TestUserManager:
    """Test class demonstrating dependency injection mocking."""
    
    def test_create_user_with_mock_service(self):
        """Test user creation with mocked email service."""
        # Create mock email service
        mock_email_service = Mock()
        mock_email_service.send_email.return_value = True
        
        # Create user manager with mock
        manager = UserManager(email_service=mock_email_service)
        
        # Test user creation
        user = manager.create_user("testuser", "test@example.com")
        
        # Assertions
        assert user["username"] == "testuser"
        assert user["email"] == "test@example.com"
        assert user["welcome_sent"] is True
        
        # Verify mock was called correctly
        mock_email_service.send_email.assert_called_once_with(
            to="test@example.com",
            subject="Welcome!",
            body="Welcome testuser!"
        )
    
    def test_create_user_email_failure(self):
        """Test user creation when email sending fails."""
        # Mock email service that fails
        mock_email_service = Mock()
        mock_email_service.send_email.return_value = False
        
        # Test
        manager = UserManager(email_service=mock_email_service)
        user = manager.create_user("testuser", "test@example.com")
        
        # Assertions
        assert user["welcome_sent"] is False
    
    def test_get_user_stats(self):
        """Test getting user statistics with mocked dependencies."""
        # Setup mock
        mock_email_service = Mock()
        mock_email_service.send_email.return_value = True
        mock_email_service.get_email_count.return_value = 42
        
        # Create manager and user
        manager = UserManager(email_service=mock_email_service)
        manager.create_user("testuser", "test@example.com")
        
        # Test stats
        stats = manager.get_user_stats("testuser")
        
        # Assertions
        assert stats["username"] == "testuser"
        assert stats["email_count"] == 42
        mock_email_service.get_email_count.assert_called_with(1)  # First user gets ID 1


# Context manager mocking

def test_fetch_user_data_with_context_manager():
    """Test using patch as context manager."""
    with patch('requests.get') as mock_get:
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Alice", "id": 2}
        mock_get.return_value = mock_response
        
        # Test
        result = fetch_user_data(2)
        
        # Assertions
        assert result["name"] == "Alice"
        mock_get.assert_called_once()


# File operations mocking

@patch("builtins.open", new_callable=mock_open)
@patch("json.dump")
def test_save_to_file(mock_json_dump, mock_file):
    """Test file saving with mocked file operations."""
    data = {"test": "data"}
    
    result = save_to_file("test.json", data)
    
    assert result is True
    mock_file.assert_called_once_with("test.json", 'w')
    mock_json_dump.assert_called_once_with(data, mock_file.return_value.__enter__.return_value)


@patch("builtins.open", new_callable=mock_open, read_data='{"config": "value"}')
@patch("json.load")
def test_read_config_file(mock_json_load, mock_file):
    """Test config file reading with mocked file operations."""
    mock_json_load.return_value = {"config": "value"}
    
    result = read_config_file("config.json")
    
    assert result["config"] == "value"
    mock_file.assert_called_once_with("config.json", 'r')


# Advanced mocking patterns

def test_mock_with_side_effect():
    """Test mock with side effect function."""
    def custom_side_effect(user_id):
        if user_id == 1:
            return {"name": "Alice"}
        elif user_id == 2:
            return {"name": "Bob"}
        else:
            raise ValueError("User not found")
    
    with patch('test_mocking.fetch_user_data') as mock_fetch:
        mock_fetch.side_effect = custom_side_effect
        
        # Test successful cases
        result1 = fetch_user_data(1)
        result2 = fetch_user_data(2)
        assert result1["name"] == "Alice"
        assert result2["name"] == "Bob"
        
        # Test exception case
        with pytest.raises(ValueError, match="User not found"):
            fetch_user_data(3)


def test_mock_with_multiple_return_values():
    """Test mock that returns different values on successive calls."""
    mock_service = Mock()
    
    # Configure mock to return different values
    mock_service.get_data.side_effect = ["first", "second", "third"]
    
    # Test multiple calls
    assert mock_service.get_data() == "first"
    assert mock_service.get_data() == "second" 
    assert mock_service.get_data() == "third"
    
    # Verify call count
    assert mock_service.get_data.call_count == 3


def test_mock_with_exception_side_effect():
    """Test mock that raises exceptions."""
    mock_service = Mock()
    mock_service.risky_operation.side_effect = ConnectionError("Network error")
    
    with pytest.raises(ConnectionError, match="Network error"):
        mock_service.risky_operation()


# Spy pattern - partial mocking

class TestSpyPattern:
    """Test class demonstrating spy patterns."""
    
    def test_spy_on_real_object(self):
        """Test spying on real object to verify calls while keeping functionality."""
        real_service = EmailService()
        
        with patch.object(real_service, 'send_email', wraps=real_service.send_email) as spy:
            # Configure the underlying requests.post to avoid real network calls
            with patch('requests.post') as mock_post:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_post.return_value = mock_response
                
                # Call the method - it executes real code but we can spy on it
                result = real_service.send_email("test@example.com", "Subject", "Body")
                
                # Verify the spy recorded the call
                spy.assert_called_once_with("test@example.com", "Subject", "Body")
                assert result is True


# Property and attribute mocking

def test_mock_object_attributes():
    """Test mocking object attributes and properties."""
    # Create mock object
    mock_user = Mock()
    
    # Set attributes
    mock_user.name = "Alice"
    mock_user.email = "alice@example.com"
    mock_user.is_active = True
    
    # Configure method return values
    mock_user.get_permissions.return_value = ["read", "write"]
    
    # Test
    assert mock_user.name == "Alice"
    assert mock_user.is_active is True
    permissions = mock_user.get_permissions()
    assert "read" in permissions
    
    # Verify method was called
    mock_user.get_permissions.assert_called_once()


# MagicMock for magic methods

def test_magic_mock_usage():
    """Test MagicMock for objects with magic methods."""
    mock_dict = MagicMock()
    
    # Configure magic methods
    mock_dict.__len__.return_value = 3
    mock_dict.__getitem__.side_effect = lambda key: f"value_for_{key}"
    mock_dict.__contains__.return_value = True
    
    # Test magic method behavior
    assert len(mock_dict) == 3
    assert mock_dict["key1"] == "value_for_key1"
    assert "anything" in mock_dict
    
    # Verify calls
    mock_dict.__getitem__.assert_called_with("key1")
    mock_dict.__contains__.assert_called_with("anything")


# Mock call verification

def test_mock_call_verification():
    """Test various ways to verify mock calls."""
    mock_service = Mock()
    
    # Make some calls
    mock_service.method_a("arg1", "arg2")
    mock_service.method_a("arg3", keyword="value")
    mock_service.method_b()
    
    # Basic call verification
    mock_service.method_a.assert_called()  # Called at least once
    mock_service.method_b.assert_called_once()  # Called exactly once
    
    # Verify specific call
    mock_service.method_a.assert_any_call("arg1", "arg2")
    mock_service.method_a.assert_any_call("arg3", keyword="value")
    
    # Verify call count
    assert mock_service.method_a.call_count == 2
    assert mock_service.method_b.call_count == 1
    
    # Verify all calls
    expected_calls = [
        call("arg1", "arg2"),
        call("arg3", keyword="value")
    ]
    mock_service.method_a.assert_has_calls(expected_calls)


# Environment variable mocking

@patch.dict(os.environ, {"TEST_ENV_VAR": "test_value", "DEBUG": "true"})
def test_environment_variables():
    """Test with mocked environment variables."""
    assert os.environ["TEST_ENV_VAR"] == "test_value"
    assert os.environ["DEBUG"] == "true"
    
    # Test code that depends on environment variables
    debug_mode = os.environ.get("DEBUG", "false").lower() == "true"
    assert debug_mode is True


# Fixture-based mocking

@pytest.fixture
def mock_requests():
    """Fixture that provides mocked requests."""
    with patch('requests.get') as mock_get, patch('requests.post') as mock_post:
        yield {"get": mock_get, "post": mock_post}


def test_with_mock_fixture(mock_requests):
    """Test using mocked requests fixture."""
    # Configure mocks through fixture
    mock_requests["get"].return_value.status_code = 200
    mock_requests["get"].return_value.json.return_value = {"data": "test"}
    
    # Use in test
    result = fetch_user_data(1)
    
    # Verify
    mock_requests["get"].assert_called_once()