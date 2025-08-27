"""
Pytest class-based testing examples.

This module demonstrates intermediate pytest patterns using classes:
- Basic test classes
- Class-level fixtures and setup/teardown
- Shared state between tests
- Inheritance in test classes
- Class-specific markers
- Nested test organization
"""

import pytest


class TestBasicCalculator:
    """Basic test class for calculator functionality."""
    
    def test_addition(self):
        """Test addition operation."""
        result = 2 + 3
        assert result == 5
    
    def test_subtraction(self):
        """Test subtraction operation."""
        result = 10 - 3
        assert result == 7
    
    def test_multiplication(self):
        """Test multiplication operation."""
        result = 4 * 5
        assert result == 20
    
    def test_division(self):
        """Test division operation."""
        result = 15 / 3
        assert result == 5
    
    def test_division_by_zero(self):
        """Test that division by zero raises exception."""
        with pytest.raises(ZeroDivisionError):
            10 / 0


class TestStringOperations:
    """Test class for string operations with class-level setup."""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method that runs before each test method."""
        self.test_string = "Hello, pytest!"
        self.empty_string = ""
        self.numeric_string = "12345"
    
    def test_string_length(self):
        """Test string length calculation."""
        assert len(self.test_string) == 14
        assert len(self.empty_string) == 0
        assert len(self.numeric_string) == 5
    
    def test_string_contains(self):
        """Test string containment."""
        assert "pytest" in self.test_string
        assert "Hello" in self.test_string
        assert "goodbye" not in self.test_string
    
    def test_string_case_conversion(self):
        """Test string case conversion methods."""
        assert self.test_string.upper() == "HELLO, PYTEST!"
        assert self.test_string.lower() == "hello, pytest!"
        assert self.test_string.title() == "Hello, Pytest!"
    
    def test_string_split(self):
        """Test string splitting."""
        words = self.test_string.split()
        assert len(words) == 2
        assert words[0] == "Hello,"
        assert words[1] == "pytest!"
    
    def test_numeric_string_operations(self):
        """Test operations on numeric strings."""
        assert self.numeric_string.isdigit()
        assert int(self.numeric_string) == 12345
        assert not self.test_string.isdigit()


class TestListOperations:
    """Test class for list operations with class-level fixtures."""
    
    @classmethod
    def setup_class(cls):
        """Class-level setup - runs once per test class."""
        cls.base_list = [1, 2, 3, 4, 5]
        cls.empty_list = []
        cls.string_list = ["apple", "banana", "cherry"]
        print(f"\nSetting up {cls.__name__}")
    
    @classmethod
    def teardown_class(cls):
        """Class-level teardown - runs once after all tests in class."""
        print(f"\nTearing down {cls.__name__}")
    
    def setup_method(self):
        """Instance-level setup - runs before each test method."""
        # Create fresh copies for each test to avoid side effects
        self.numbers = self.base_list.copy()
        self.fruits = self.string_list.copy()
        self.temp_list = []
    
    def test_list_append(self):
        """Test list append operation."""
        original_length = len(self.numbers)
        self.numbers.append(6)
        assert len(self.numbers) == original_length + 1
        assert self.numbers[-1] == 6
    
    def test_list_remove(self):
        """Test list remove operation."""
        original_length = len(self.numbers)
        self.numbers.remove(3)
        assert len(self.numbers) == original_length - 1
        assert 3 not in self.numbers
    
    def test_list_extend(self):
        """Test list extend operation."""
        original_length = len(self.numbers)
        self.numbers.extend([6, 7, 8])
        assert len(self.numbers) == original_length + 3
        assert self.numbers[-3:] == [6, 7, 8]
    
    def test_list_sorting(self):
        """Test list sorting."""
        unsorted_list = [3, 1, 4, 1, 5, 9, 2, 6]
        unsorted_list.sort()
        assert unsorted_list == [1, 1, 2, 3, 4, 5, 6, 9]
        
        # Test sorted() function (doesn't modify original)
        original = [3, 1, 4, 1, 5]
        sorted_copy = sorted(original)
        assert original == [3, 1, 4, 1, 5]  # Original unchanged
        assert sorted_copy == [1, 1, 3, 4, 5]
    
    def test_list_comprehension(self):
        """Test list comprehensions."""
        squares = [x**2 for x in self.numbers]
        expected_squares = [1, 4, 9, 16, 25]
        assert squares == expected_squares
        
        # Filter even numbers
        evens = [x for x in self.numbers if x % 2 == 0]
        assert evens == [2, 4]


@pytest.mark.database
class TestDatabaseOperations:
    """Test class marked for database operations."""
    
    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Mock database setup."""
        self.db_connection = {"status": "connected", "data": {}}
        yield
        # Cleanup
        self.db_connection = None
    
    def test_database_connection(self):
        """Test database connection."""
        assert self.db_connection["status"] == "connected"
    
    def test_database_insert(self):
        """Test database insert operation."""
        self.db_connection["data"]["user_1"] = {"name": "Alice", "age": 30}
        assert "user_1" in self.db_connection["data"]
        assert self.db_connection["data"]["user_1"]["name"] == "Alice"
    
    def test_database_update(self):
        """Test database update operation."""
        # Insert first
        self.db_connection["data"]["user_2"] = {"name": "Bob", "age": 25}
        
        # Update
        self.db_connection["data"]["user_2"]["age"] = 26
        assert self.db_connection["data"]["user_2"]["age"] == 26
    
    def test_database_delete(self):
        """Test database delete operation."""
        # Insert first
        self.db_connection["data"]["user_3"] = {"name": "Charlie", "age": 35}
        assert "user_3" in self.db_connection["data"]
        
        # Delete
        del self.db_connection["data"]["user_3"]
        assert "user_3" not in self.db_connection["data"]


class TestUserAccount:
    """Test class demonstrating object state management."""
    
    @pytest.fixture
    def user_account(self):
        """Fixture that creates a user account for testing."""
        return UserAccount("testuser", "test@example.com", balance=100.0)
    
    def test_account_creation(self, user_account):
        """Test user account creation."""
        assert user_account.username == "testuser"
        assert user_account.email == "test@example.com"
        assert user_account.balance == 100.0
    
    def test_deposit(self, user_account):
        """Test deposit operation."""
        initial_balance = user_account.balance
        user_account.deposit(50.0)
        assert user_account.balance == initial_balance + 50.0
    
    def test_withdrawal(self, user_account):
        """Test withdrawal operation."""
        initial_balance = user_account.balance
        user_account.withdraw(30.0)
        assert user_account.balance == initial_balance - 30.0
    
    def test_insufficient_funds(self, user_account):
        """Test withdrawal with insufficient funds."""
        with pytest.raises(ValueError, match="Insufficient funds"):
            user_account.withdraw(200.0)
    
    def test_negative_deposit(self, user_account):
        """Test deposit with negative amount."""
        with pytest.raises(ValueError, match="Amount must be positive"):
            user_account.deposit(-10.0)


class UserAccount:
    """Simple user account class for testing."""
    
    def __init__(self, username, email, balance=0.0):
        self.username = username
        self.email = email
        self.balance = balance
    
    def deposit(self, amount):
        """Deposit money to account."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount):
        """Withdraw money from account."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount


class TestInheritance:
    """Base test class to demonstrate inheritance."""
    
    @pytest.fixture(autouse=True)
    def base_setup(self):
        """Base setup method."""
        self.base_value = "base"
    
    def test_base_functionality(self):
        """Test base functionality."""
        assert self.base_value == "base"


class TestInheritanceChild(TestInheritance):
    """Child test class that inherits from TestInheritance."""
    
    @pytest.fixture(autouse=True) 
    def child_setup(self):
        """Child setup method."""
        self.child_value = "child"
    
    def test_inherited_functionality(self):
        """Test that child class inherits base functionality."""
        assert self.base_value == "base"  # From parent
        assert self.child_value == "child"  # From child
    
    def test_child_specific_functionality(self):
        """Test child-specific functionality."""
        combined = f"{self.base_value}_{self.child_value}"
        assert combined == "base_child"


@pytest.mark.parametrize("operation,a,b,expected", [
    ("add", 2, 3, 5),
    ("subtract", 10, 3, 7),
    ("multiply", 4, 5, 20),
    ("divide", 15, 3, 5),
])
class TestParametrizedClass:
    """Test class that uses parametrization."""
    
    def test_calculator_operation(self, operation, a, b, expected):
        """Test calculator operations with parametrized inputs."""
        calculator = SimpleCalculator()
        
        if operation == "add":
            result = calculator.add(a, b)
        elif operation == "subtract":
            result = calculator.subtract(a, b)
        elif operation == "multiply":
            result = calculator.multiply(a, b)
        elif operation == "divide":
            result = calculator.divide(a, b)
        else:
            pytest.fail(f"Unknown operation: {operation}")
        
        assert result == expected


class SimpleCalculator:
    """Simple calculator class for testing."""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b