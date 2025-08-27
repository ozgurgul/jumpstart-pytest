"""
Advanced pytest fixture examples.

This module demonstrates advanced fixture patterns:
- Fixture factories and parameterized fixtures
- Fixture dependency injection
- Dynamic fixture generation
- Fixture scopes and lifecycle management
- Fixture cleanup and error handling
- Custom fixture implementations
"""

import pytest
import tempfile
import shutil
import os
import sqlite3
from contextlib import contextmanager


# Fixture factory pattern
@pytest.fixture
def user_factory():
    """Factory fixture that creates user objects with different configurations."""
    created_users = []
    
    def _create_user(name="Default User", email=None, role="user", active=True):
        if email is None:
            email = f"{name.lower().replace(' ', '.')}@example.com"
        
        user = {
            "id": len(created_users) + 1,
            "name": name,
            "email": email,
            "role": role,
            "active": active,
            "created_at": "2024-01-01T00:00:00Z"
        }
        created_users.append(user)
        return user
    
    yield _create_user
    
    # Cleanup: log all created users (in real scenario, might clean up database)
    print(f"\nCreated {len(created_users)} users during test session")


# Parameterized fixture
@pytest.fixture(params=["sqlite", "memory", "file"])
def database_type(request):
    """Parameterized fixture that provides different database types."""
    return request.param


@pytest.fixture
def database_connection(database_type):
    """Fixture that creates different types of database connections."""
    if database_type == "sqlite":
        conn = sqlite3.connect(":memory:")
        conn.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
    elif database_type == "memory":
        conn = {"type": "memory", "data": {}}
    else:  # file
        temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        conn = sqlite3.connect(temp_db.name)
        conn.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
    
    yield conn
    
    # Cleanup
    if hasattr(conn, 'close'):
        conn.close()
    if database_type == "file" and hasattr(temp_db, 'name'):
        os.unlink(temp_db.name)


# Fixture with complex dependency chain
@pytest.fixture(scope="session")
def application_config():
    """Session-scoped fixture providing application configuration."""
    return {
        "debug": True,
        "testing": True,
        "database_url": "sqlite:///:memory:",
        "secret_key": "test-secret-key"
    }


@pytest.fixture(scope="module")
def application(application_config):
    """Module-scoped fixture that creates application instance."""
    app = MockApplication(application_config)
    app.initialize()
    yield app
    app.cleanup()


@pytest.fixture
def authenticated_client(application, user_factory):
    """Fixture that provides authenticated client with dependencies."""
    user = user_factory(name="Test User", role="admin")
    client = application.create_client()
    client.authenticate(user)
    return client


# Fixture with error handling
@pytest.fixture
def risky_resource():
    """Fixture that demonstrates error handling during setup/teardown."""
    resource = None
    try:
        resource = create_risky_resource()
        yield resource
    except Exception as e:
        print(f"Error creating resource: {e}")
        yield None
    finally:
        if resource:
            try:
                cleanup_risky_resource(resource)
            except Exception as e:
                print(f"Error cleaning up resource: {e}")


# Dynamic fixture based on test request
@pytest.fixture
def dynamic_data(request):
    """Fixture that adapts based on test requirements."""
    # Check if test has specific markers
    if request.node.get_closest_marker("large_dataset"):
        data_size = 1000
    elif request.node.get_closest_marker("small_dataset"):
        data_size = 10
    else:
        data_size = 100
    
    # Generate data based on test name
    test_name = request.node.name
    if "user" in test_name.lower():
        data_type = "users"
    elif "product" in test_name.lower():
        data_type = "products"
    else:
        data_type = "generic"
    
    return generate_test_data(data_type, data_size)


# Fixture that yields multiple values
@pytest.fixture
def multi_environment():
    """Fixture that provides multiple environment configurations."""
    environments = [
        {"name": "development", "debug": True, "testing": False},
        {"name": "testing", "debug": True, "testing": True},
        {"name": "production", "debug": False, "testing": False}
    ]
    
    for env in environments:
        yield env


# Advanced temporary directory fixture
@pytest.fixture
def temp_workspace():
    """Advanced temporary directory fixture with predefined structure."""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="pytest_workspace_")
    
    # Create subdirectories
    subdirs = ["input", "output", "temp", "logs"]
    for subdir in subdirs:
        os.makedirs(os.path.join(temp_dir, subdir))
    
    # Create some sample files
    sample_files = {
        "input/data.txt": "Sample input data",
        "input/config.json": '{"setting": "value"}',
        "temp/placeholder.txt": "Temporary file"
    }
    
    for file_path, content in sample_files.items():
        full_path = os.path.join(temp_dir, file_path)
        with open(full_path, 'w') as f:
            f.write(content)
    
    workspace = {
        "root": temp_dir,
        "input": os.path.join(temp_dir, "input"),
        "output": os.path.join(temp_dir, "output"),
        "temp": os.path.join(temp_dir, "temp"),
        "logs": os.path.join(temp_dir, "logs")
    }
    
    yield workspace
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


# Fixture with context manager
@pytest.fixture
def managed_resource():
    """Fixture that uses context manager for resource management."""
    with resource_manager() as resource:
        yield resource


@contextmanager
def resource_manager():
    """Context manager for resource handling."""
    print("Acquiring resource...")
    resource = {"id": "resource_123", "status": "active"}
    try:
        yield resource
    finally:
        print("Releasing resource...")
        resource["status"] = "released"


# Fixture composition pattern
@pytest.fixture
def basic_user():
    """Basic user fixture."""
    return {"id": 1, "name": "Basic User", "role": "user"}


@pytest.fixture
def admin_user():
    """Admin user fixture."""
    return {"id": 2, "name": "Admin User", "role": "admin"}


@pytest.fixture
def user_permissions(request):
    """Fixture that provides permissions based on user type."""
    # Get the user fixture from the test
    if hasattr(request, 'getfixturevalue'):
        try:
            user = request.getfixturevalue('admin_user')
        except:
            user = request.getfixturevalue('basic_user')
    else:
        user = {"role": "user"}  # Default
    
    if user["role"] == "admin":
        return {"read": True, "write": True, "delete": True, "admin": True}
    else:
        return {"read": True, "write": False, "delete": False, "admin": False}


# Fixture with caching mechanism
@pytest.fixture(scope="session")
def cached_expensive_data():
    """Session-scoped fixture that caches expensive computation."""
    print("Computing expensive data...")
    # Simulate expensive computation
    import time
    time.sleep(0.1)  # Simulate delay
    
    data = {
        "computation_result": sum(range(10000)),
        "timestamp": time.time(),
        "cached": True
    }
    
    return data


# Helper classes and functions for fixtures
class MockApplication:
    """Mock application class for testing."""
    
    def __init__(self, config):
        self.config = config
        self.initialized = False
    
    def initialize(self):
        """Initialize the application."""
        self.initialized = True
        print("Application initialized")
    
    def cleanup(self):
        """Cleanup the application."""
        self.initialized = False
        print("Application cleaned up")
    
    def create_client(self):
        """Create a client for the application."""
        return MockClient(self)


class MockClient:
    """Mock client class for testing."""
    
    def __init__(self, app):
        self.app = app
        self.authenticated = False
        self.user = None
    
    def authenticate(self, user):
        """Authenticate the client with a user."""
        self.user = user
        self.authenticated = True


def create_risky_resource():
    """Create a resource that might fail."""
    # Simulate potential failure
    import random
    if random.random() < 0.1:  # 10% chance of failure
        raise Exception("Failed to create risky resource")
    return {"id": "risky_123", "status": "created"}


def cleanup_risky_resource(resource):
    """Cleanup risky resource."""
    resource["status"] = "cleaned_up"


def generate_test_data(data_type, size):
    """Generate test data based on type and size."""
    if data_type == "users":
        return [
            {"id": i, "name": f"User{i}", "email": f"user{i}@example.com"}
            for i in range(1, size + 1)
        ]
    elif data_type == "products":
        return [
            {"id": i, "name": f"Product{i}", "price": i * 10.0}
            for i in range(1, size + 1)
        ]
    else:
        return [{"id": i, "value": f"item_{i}"} for i in range(1, size + 1)]


# Tests using the advanced fixtures

def test_user_factory(user_factory):
    """Test the user factory fixture."""
    user1 = user_factory("Alice")
    user2 = user_factory("Bob", role="admin")
    
    assert user1["name"] == "Alice"
    assert user1["role"] == "user"
    assert user2["name"] == "Bob"
    assert user2["role"] == "admin"
    assert user1["id"] != user2["id"]


def test_database_operations(database_connection, database_type):
    """Test database operations with different database types."""
    if database_type in ["sqlite"]:
        # Test SQLite operations
        cursor = database_connection.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                      ("Test User", "test@example.com"))
        database_connection.commit()
        
        cursor.execute("SELECT * FROM users WHERE name = ?", ("Test User",))
        result = cursor.fetchone()
        assert result[1] == "Test User"  # name column
        assert result[2] == "test@example.com"  # email column
    
    elif database_type == "memory":
        # Test memory database operations
        database_connection["data"]["user1"] = {"name": "Test User", "email": "test@example.com"}
        assert "user1" in database_connection["data"]


def test_authenticated_client(authenticated_client):
    """Test authenticated client fixture."""
    assert authenticated_client.authenticated is True
    assert authenticated_client.user["role"] == "admin"
    assert authenticated_client.app.initialized is True


def test_temp_workspace(temp_workspace):
    """Test temporary workspace fixture."""
    # Check directory structure
    assert os.path.exists(temp_workspace["root"])
    assert os.path.exists(temp_workspace["input"])
    assert os.path.exists(temp_workspace["output"])
    
    # Check sample files
    data_file = os.path.join(temp_workspace["input"], "data.txt")
    assert os.path.exists(data_file)
    
    with open(data_file, 'r') as f:
        content = f.read()
    assert content == "Sample input data"


@pytest.mark.small_dataset
def test_dynamic_data_small(dynamic_data):
    """Test with small dataset marker."""
    assert len(dynamic_data) == 10


@pytest.mark.large_dataset 
def test_dynamic_data_large(dynamic_data):
    """Test with large dataset marker."""
    assert len(dynamic_data) == 1000


def test_user_dynamic_data(dynamic_data):
    """Test dynamic data generation for user-related test."""
    # Should generate user data based on test name
    assert len(dynamic_data) == 100  # Default size
    if dynamic_data:  # Check if data was generated
        assert "name" in dynamic_data[0] or "id" in dynamic_data[0]


def test_managed_resource(managed_resource):
    """Test managed resource fixture."""
    assert managed_resource["id"] == "resource_123"
    assert managed_resource["status"] == "active"


def test_admin_permissions(admin_user, user_permissions):
    """Test admin user permissions."""
    assert user_permissions["admin"] is True
    assert user_permissions["write"] is True
    assert user_permissions["delete"] is True


def test_basic_permissions(basic_user, user_permissions):
    """Test basic user permissions."""
    assert user_permissions["admin"] is False
    assert user_permissions["write"] is False
    assert user_permissions["delete"] is False
    assert user_permissions["read"] is True


def test_cached_data_consistency(cached_expensive_data):
    """Test that cached data is consistent across multiple accesses."""
    # This test will reuse the same data from session scope
    assert cached_expensive_data["cached"] is True
    assert cached_expensive_data["computation_result"] == sum(range(10000))


def test_cached_data_reuse(cached_expensive_data):
    """Another test using the same cached data."""
    # This should use the exact same data instance
    assert cached_expensive_data["cached"] is True