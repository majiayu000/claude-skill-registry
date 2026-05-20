---
name: Testing Anti-Patterns
description: This skill should be used when encountering "flaky tests", "test maintenance issues", "slow test suites", "brittle tests", "test code smells", "test debugging problems", or when tests are hard to understand, maintain, or debug.
version: 1.0.0
---

# Testing Anti-Patterns: Prevention and Detection

## Overview

This skill identifies and prevents common testing anti-patterns that make test suites unreliable, slow, and difficult to maintain. It provides detection strategies and refactoring solutions for healthier test codebases.

## When to Use This Skill

Use this skill when encountering:
- **Flaky tests** that pass/fail inconsistently
- **Slow test suites** that take too long to run
- **Brittle tests** that break on minor code changes
- **Hard-to-debug test failures**
- **Test maintenance nightmares**
- **Test code duplication and complexity**
- **Poor test organization and naming**

## Common Anti-Patterns and Solutions

### 1. The Mystery Guest Anti-Pattern
**Problem**: Tests depend on external data that's not visible in the test.

```python
# ❌ BAD: Mystery Guest
def test_user_login():
    """What user data exists? What are the credentials?"""
    user = User.objects.get(email="test@example.com")  # Where did this come from?
    response = client.post('/login', {
        'email': user.email,
        'password': 'secret123'  # How do we know this password?
    })
    assert response.status_code == 200

# ✅ GOOD: Explicit setup
def test_user_login():
    """Clear test with explicit data creation."""
    # Arrange: Create test data explicitly
    user = User.objects.create_user(
        email="test@example.com",
        password="secret123",
        first_name="Test",
        last_name="User"
    )

    # Act: Perform the action
    response = client.post('/login', {
        'email': user.email,
        'password': 'secret123'
    })

    # Assert: Verify the result
    assert response.status_code == 200
    assert response.json()['user_id'] == user.id
```

### 2. The Slow Poke Anti-Pattern
**Problem**: Tests take unnecessarily long to run.

```python
# ❌ BAD: Slow Poke
import time

def test_api_response():
    """This test is unnecessarily slow."""
    time.sleep(5)  # Why?
    response = api_client.get('/slow-endpoint')
    time.sleep(2)  # More unnecessary waiting
    assert response.status_code == 200

# ✅ GOOD: Fast and focused
def test_api_response_fast():
    """Fast test with mocked delays."""
    with patch('slow_service.time_consuming_operation') as mock_op:
        mock_op.return_value = "mocked_result"

        response = api_client.get('/fast-endpoint')
        assert response.status_code == 200

        # Verify the operation was called correctly
        mock_op.assert_called_once()
```

### 3. The Eager Test Anti-Pattern
**Problem**: One test tries to verify too many things.

```python
# ❌ BAD: Eager Test
def test_user_management_everything():
    """This test does too much."""
    # Create user
    user = create_user("test@example.com")
    assert user.id is not None

    # Update user
    user.update(first_name="Updated")
    assert user.first_name == "Updated"

    # User permissions
    assign_permission(user, "read")
    assert user.has_permission("read")

    # User posts
    post = create_post(user, "Test post")
    assert post.author == user

    # Delete user
    user.delete()
    assert User.objects.filter(id=user.id).count() == 0

    # This test is hard to debug when it fails!

# ✅ GOOD: Focused tests
def test_user_creation():
    """Test only user creation."""
    user = create_user("test@example.com")
    assert user.id is not None
    assert user.email == "test@example.com"

def test_user_update():
    """Test only user updates."""
    user = create_user("test@example.com")
    user.update(first_name="Updated")
    assert user.first_name == "Updated"

def test_user_permissions():
    """Test only permission assignment."""
    user = create_user("test@example.com")
    assign_permission(user, "read")
    assert user.has_permission("read")
```

### 4. The Fragile Fixture Anti-Pattern
**Problem**: Fixtures that break easily and affect multiple tests.

```python
# ❌ BAD: Fragile Fixture
@pytest.fixture(scope="session")  # Dangerous: shared state
def database_with_data():
    """This fixture is fragile and affects all tests."""
    db.create_all()

    # Create a bunch of interconnected data
    user1 = User.objects.create(email="user1@test.com")
    user2 = User.objects.create(email="user2@test.com")

    post1 = Post.objects.create(author=user1, title="Post 1")
    post2 = Post.objects.create(author=user2, title="Post 2")

    # Any test that modifies this data breaks other tests!
    yield

    db.drop_all()

# ✅ GOOD: Isolated fixtures
@pytest.fixture
def clean_database():
    """Clean database for each test."""
    db.create_all()
    yield
    db.drop_all()

@pytest.fixture
def sample_user(clean_database):
    """Create a fresh user for each test."""
    return User.objects.create(
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )

@pytest.fixture
def sample_post(sample_user):
    """Create a fresh post for each test."""
    return Post.objects.create(
        author=sample_user,
        title="Test Post",
        content="Test content"
    )
```

### 5. The Assertion Roulette Anti-Pattern
**Problem**: Multiple assertions without clear failure messages.

```python
# ❌ BAD: Assertion Roulette
def test_user_api_response():
    """Which assertion failed? Who knows!"""
    response = api_client.get('/users/1')
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == 1
    assert data['email'] == 'test@example.com'
    assert data['first_name'] == 'Test'
    assert data['last_name'] == 'User'
    assert data['is_active'] is True
    assert data['created_at'] is not None
    # If any of these fail, we don't know which or why

# ✅ GOOD: Clear assertions with messages
def test_user_api_response_clear():
    """Each assertion has a clear purpose and message."""
    response = api_client.get('/users/1')

    assert response.status_code == 200, f"API request failed: {response.text}"

    data = response.json()
    assert data['id'] == 1, f"Wrong user ID: expected 1, got {data.get('id')}"
    assert data['email'] == 'test@example.com', f"Wrong email: {data.get('email')}"
    assert data['first_name'] == 'Test', f"Wrong first name: {data.get('first_name')}"
    assert data['last_name'] == 'User', f"Wrong last name: {data.get('last_name')}"
    assert data['is_active'] is True, f"User should be active: {data.get('is_active')}"

    # Or use a helper for complex object validation
    assert_user_data_valid(data, expected_id=1, expected_email='test@example.com')

def assert_user_data_valid(data, expected_id, expected_email):
    """Helper for user data validation with detailed error messages."""
    errors = []

    if data.get('id') != expected_id:
        errors.append(f"ID mismatch: expected {expected_id}, got {data.get('id')}")

    if data.get('email') != expected_email:
        errors.append(f"Email mismatch: expected {expected_email}, got {data.get('email')}")

    if not data.get('created_at'):
        errors.append("Missing created_at field")

    if errors:
        pytest.fail(f"User data validation failed:\n" + "\n".join(errors))
```

### 6. The Test Code Duplication Anti-Pattern
**Problem**: Copy-paste test code that's hard to maintain.

```python
# ❌ BAD: Test Code Duplication
def test_admin_can_create_post():
    admin = User.objects.create(email="admin@test.com", role="admin")
    auth_token = generate_token(admin)
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post('/posts', {
        'title': 'Admin Post',
        'content': 'Admin content'
    }, headers=headers)

    assert response.status_code == 201

def test_admin_can_update_post():
    admin = User.objects.create(email="admin@test.com", role="admin")
    auth_token = generate_token(admin)
    headers = {"Authorization": f"Bearer {auth_token}"}

    post = Post.objects.create(title="Test", content="Test", author=admin)

    response = client.put(f'/posts/{post.id}', {
        'title': 'Updated Post',
        'content': 'Updated content'
    }, headers=headers)

    assert response.status_code == 200

def test_admin_can_delete_post():
    admin = User.objects.create(email="admin@test.com", role="admin")
    auth_token = generate_token(admin)
    headers = {"Authorization": f"Bearer {auth_token}"}

    post = Post.objects.create(title="Test", content="Test", author=admin)

    response = client.delete(f'/posts/{post.id}', headers=headers)

    assert response.status_code == 204

# ✅ GOOD: DRY test code with helpers
class TestPostAPI:
    @pytest.fixture
    def admin_user(self):
        """Create admin user for tests."""
        return User.objects.create(email="admin@test.com", role="admin")

    @pytest.fixture
    def auth_headers(self, admin_user):
        """Create authenticated headers."""
        token = generate_token(admin_user)
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def sample_post(self, admin_user):
        """Create a sample post for tests."""
        return Post.objects.create(
            title="Test Post",
            content="Test content",
            author=admin_user
        )

    def test_admin_can_create_post(self, auth_headers):
        """Test admin post creation."""
        response = client.post('/posts', {
            'title': 'Admin Post',
            'content': 'Admin content'
        }, headers=auth_headers)

        assert response.status_code == 201

    def test_admin_can_update_post(self, auth_headers, sample_post):
        """Test admin post update."""
        response = client.put(f'/posts/{sample_post.id}', {
            'title': 'Updated Post',
            'content': 'Updated content'
        }, headers=auth_headers)

        assert response.status_code == 200

    def test_admin_can_delete_post(self, auth_headers, sample_post):
        """Test admin post deletion."""
        response = client.delete(f'/posts/{sample_post.id}', headers=auth_headers)
        assert response.status_code == 204
```

### 7. The Secret Dependency Anti-Pattern
**Problem**: Tests that depend on execution order or hidden state.

```python
# ❌ BAD: Secret Dependencies
class TestUserWorkflow:
    # These tests secretly depend on execution order!
    def test_01_create_user(self):
        """Must run first!"""
        self.user = User.objects.create(email="test@example.com")
        assert self.user.id is not None

    def test_02_update_user(self):
        """Depends on test_01_create_user!"""
        self.user.update(first_name="Updated")
        assert self.user.first_name == "Updated"

    def test_03_delete_user(self):
        """Depends on previous tests!"""
        self.user.delete()
        assert User.objects.filter(id=self.user.id).count() == 0

# ✅ GOOD: Independent tests
class TestUserWorkflow:
    def test_user_creation(self):
        """Independent test for user creation."""
        user = User.objects.create(email="test@example.com")
        assert user.id is not None
        assert user.email == "test@example.com"

    def test_user_update(self):
        """Independent test for user update."""
        # Arrange: Create necessary data
        user = User.objects.create(email="test@example.com")

        # Act: Perform update
        user.update(first_name="Updated")

        # Assert: Verify result
        assert user.first_name == "Updated"

    def test_user_deletion(self):
        """Independent test for user deletion."""
        # Arrange: Create user to delete
        user = User.objects.create(email="test@example.com")
        user_id = user.id

        # Act: Delete user
        user.delete()

        # Assert: Verify deletion
        assert User.objects.filter(id=user_id).count() == 0
```

## Anti-Pattern Detection Tools

### 1. Test Smell Detector
```python
"""
Tool to detect common test anti-patterns in the codebase.
"""

import ast
import os
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class TestSmell:
    """Represents a detected test anti-pattern."""
    file_path: str
    line_number: int
    smell_type: str
    description: str
    severity: str  # 'low', 'medium', 'high'
    suggestion: str


class TestSmellDetector:
    """Detects common anti-patterns in test files."""

    def __init__(self):
        self.smells: List[TestSmell] = []

    def analyze_test_file(self, file_path: Path) -> List[TestSmell]:
        """Analyze a test file for anti-patterns."""
        self.smells = []

        with open(file_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)
        self._analyze_ast(tree, str(file_path))

        return self.smells

    def _analyze_ast(self, tree: ast.AST, file_path: str):
        """Analyze AST for test smells."""
        for node in ast.walk(tree):
            self._check_long_test_methods(node, file_path)
            self._check_mystery_guest(node, file_path)
            self._check_assertion_roulette(node, file_path)
            self._check_slow_poke(node, file_path)
            self._check_fragile_fixture(node, file_path)

    def _check_long_test_methods(self, node: ast.AST, file_path: str):
        """Detect overly long test methods (Eager Test)."""
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            # Count lines of code (excluding comments and docstrings)
            loc = len([n for n in ast.walk(node) if isinstance(n, ast.stmt)])

            if loc > 15:  # Threshold for "too long"
                self.smells.append(TestSmell(
                    file_path=file_path,
                    line_number=node.lineno,
                    smell_type="Eager Test",
                    description=f"Test method '{node.name}' is too long ({loc} statements)",
                    severity="medium",
                    suggestion="Break this test into smaller, focused tests"
                ))

    def _check_mystery_guest(self, node: ast.AST, file_path: str):
        """Detect Mystery Guest pattern."""
        if isinstance(node, ast.Call):
            # Look for database queries without clear setup
            if (hasattr(node.func, 'attr') and
                node.func.attr in ['get', 'filter', 'first'] and
                hasattr(node.func.value, 'attr') and
                node.func.value.attr == 'objects'):

                # Check if this is in a test method
                parent = node
                while parent and not (isinstance(parent, ast.FunctionDef) and
                                    parent.name.startswith('test_')):
                    parent = getattr(parent, 'parent', None)

                if parent:
                    self.smells.append(TestSmell(
                        file_path=file_path,
                        line_number=node.lineno,
                        smell_type="Mystery Guest",
                        description="Database query in test without explicit setup",
                        severity="medium",
                        suggestion="Create test data explicitly in the test or use fixtures"
                    ))

    def _check_assertion_roulette(self, node: ast.AST, file_path: str):
        """Detect Assertion Roulette pattern."""
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            # Count assert statements
            assert_count = len([n for n in ast.walk(node)
                              if isinstance(n, ast.Assert)])

            if assert_count > 5:
                self.smells.append(TestSmell(
                    file_path=file_path,
                    line_number=node.lineno,
                    smell_type="Assertion Roulette",
                    description=f"Test has {assert_count} assertions without clear messages",
                    severity="medium",
                    suggestion="Add descriptive messages to assertions or split into multiple tests"
                ))

    def _check_slow_poke(self, node: ast.AST, file_path: str):
        """Detect Slow Poke pattern."""
        if isinstance(node, ast.Call):
            # Look for sleep calls in tests
            if (hasattr(node.func, 'attr') and node.func.attr == 'sleep' or
                isinstance(node.func, ast.Name) and node.func.id == 'sleep'):

                self.smells.append(TestSmell(
                    file_path=file_path,
                    line_number=node.lineno,
                    smell_type="Slow Poke",
                    description="Test uses sleep() - potential timing issue",
                    severity="high",
                    suggestion="Replace sleep with condition waiting or use mocks"
                ))

    def _check_fragile_fixture(self, node: ast.AST, file_path: str):
        """Detect Fragile Fixture pattern."""
        if (isinstance(node, ast.FunctionDef) and
            any(d.id == 'pytest.fixture' for d in node.decorator_list
                if hasattr(d, 'id'))):

            # Look for session-scoped fixtures
            for decorator in node.decorator_list:
                if (isinstance(decorator, ast.Call) and
                    hasattr(decorator.func, 'attr') and
                    decorator.func.attr == 'fixture'):

                    for keyword in decorator.keywords:
                        if (keyword.arg == 'scope' and
                            isinstance(keyword.value, ast.Str) and
                            keyword.value.s == 'session'):

                            self.smells.append(TestSmell(
                                file_path=file_path,
                                line_number=node.lineno,
                                smell_type="Fragile Fixture",
                                description="Session-scoped fixture can cause test interdependencies",
                                severity="medium",
                                suggestion="Consider using function-scoped fixtures for better isolation"
                            ))

    def generate_report(self, test_directory: Path) -> str:
        """Generate a comprehensive report of test smells."""
        all_smells = []

        # Analyze all test files
        for test_file in test_directory.rglob("test_*.py"):
            smells = self.analyze_test_file(test_file)
            all_smells.extend(smells)

        # Group by smell type
        smell_groups = {}
        for smell in all_smells:
            smell_type = smell.smell_type
            if smell_type not in smell_groups:
                smell_groups[smell_type] = []
            smell_groups[smell_type].append(smell)

        # Generate report
        report = "# Test Anti-Pattern Detection Report\n\n"
        report += f"Total smells detected: {len(all_smells)}\n\n"

        for smell_type, smells in smell_groups.items():
            report += f"## {smell_type} ({len(smells)} occurrences)\n\n"

            for smell in smells:
                report += f"- **{smell.file_path}:{smell.line_number}** - {smell.description}\n"
                report += f"  *Suggestion: {smell.suggestion}*\n\n"

        return report


# Usage example:
def check_project_test_smells():
    """Check the entire project for test anti-patterns."""
    detector = TestSmellDetector()
    test_dir = Path("tests")

    report = detector.generate_report(test_dir)

    with open("test_smell_report.md", "w") as f:
        f.write(report)

    print("Test smell analysis complete. See test_smell_report.md")
```

### 2. Test Performance Analyzer
```python
"""
Tool to analyze test suite performance and identify slow tests.
"""

import pytest
import time
import json
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict


@dataclass
class TestMetrics:
    """Metrics for a single test."""
    name: str
    duration: float
    status: str  # 'PASSED', 'FAILED', 'SKIPPED'
    file_path: str
    line_number: int


class TestPerformanceAnalyzer:
    """Analyzes test suite performance."""

    def __init__(self):
        self.test_metrics: List[TestMetrics] = []

    def pytest_runtest_protocol(self, item, nextitem):
        """Pytest hook to collect test metrics."""
        start_time = time.time()

        # Run the test
        result = yield

        end_time = time.time()
        duration = end_time - start_time

        # Collect metrics
        metrics = TestMetrics(
            name=item.name,
            duration=duration,
            status=result.outcome if hasattr(result, 'outcome') else 'UNKNOWN',
            file_path=str(item.fspath),
            line_number=item.function.__code__.co_firstlineno
        )

        self.test_metrics.append(metrics)

    def generate_performance_report(self) -> Dict:
        """Generate detailed performance analysis."""
        if not self.test_metrics:
            return {"error": "No test metrics collected"}

        total_duration = sum(m.duration for m in self.test_metrics)
        avg_duration = total_duration / len(self.test_metrics)

        # Find slow tests (>2x average duration)
        slow_threshold = avg_duration * 2
        slow_tests = [m for m in self.test_metrics if m.duration > slow_threshold]

        # Group by file
        by_file = {}
        for metric in self.test_metrics:
            file_path = metric.file_path
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(metric)

        # Find slowest files
        file_durations = {
            path: sum(m.duration for m in metrics)
            for path, metrics in by_file.items()
        }

        slowest_files = sorted(file_durations.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "summary": {
                "total_tests": len(self.test_metrics),
                "total_duration": round(total_duration, 2),
                "average_duration": round(avg_duration, 2),
                "slow_test_count": len(slow_tests),
                "slow_test_threshold": round(slow_threshold, 2)
            },
            "slow_tests": [
                {
                    "name": m.name,
                    "duration": round(m.duration, 2),
                    "file": m.file_path,
                    "line": m.line_number
                }
                for m in sorted(slow_tests, key=lambda x: x.duration, reverse=True)[:20]
            ],
            "slowest_files": [
                {
                    "file": path,
                    "duration": round(duration, 2),
                    "test_count": len(by_file[path])
                }
                for path, duration in slowest_files
            ]
        }

    def save_metrics(self, output_path: Path):
        """Save collected metrics to JSON file."""
        data = {
            "metrics": [asdict(m) for m in self.test_metrics],
            "report": self.generate_performance_report()
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

# pytest plugin configuration
def pytest_configure(config):
    """Configure the performance analyzer plugin."""
    config.analyzer = TestPerformanceAnalyzer()
    config.pluginmanager.register(config.analyzer, "performance_analyzer")

def pytest_unconfigure(config):
    """Save metrics when tests complete."""
    if hasattr(config, 'analyzer'):
        config.analyzer.save_metrics(Path("test_performance_metrics.json"))
        print("Test performance metrics saved to test_performance_metrics.json")
```

## Project-Specific Patterns for EnterpriseHub

### For GHL Real Estate AI Components

```python
# ✅ Good patterns for Streamlit component testing
class TestStreamlitComponents:
    """Test patterns for Streamlit components."""

    @pytest.fixture
    def mock_streamlit_session(self):
        """Mock Streamlit session state."""
        with patch('streamlit.session_state') as mock_session:
            mock_session._state = {}
            yield mock_session

    def test_property_matcher_component(self, mock_streamlit_session):
        """Test property matcher with proper mocking."""
        from components.property_matcher_ai import PropertyMatcherComponent

        # Arrange: Set up component with test data
        component = PropertyMatcherComponent()
        test_preferences = {
            "budget_max": 500000,
            "bedrooms": 3,
            "location": "Rancho Cucamonga, CA"
        }

        # Act: Render component with test data
        with patch('streamlit.selectbox') as mock_selectbox:
            mock_selectbox.return_value = "Rancho Cucamonga, CA"

            result = component.render_preferences_form()

        # Assert: Verify component behavior
        assert result is not None
        mock_selectbox.assert_called_once()

    def test_ai_training_sandbox_isolation(self):
        """Test AI training with proper isolation."""
        from components.ai_training_sandbox import AITrainingSandbox

        # Arrange: Create isolated training environment
        with patch('services.ai_service.AIService') as mock_ai_service:
            mock_ai_service.return_value.train_model.return_value = {
                "accuracy": 0.95,
                "loss": 0.05
            }

            sandbox = AITrainingSandbox()

            # Act: Train model with test data
            result = sandbox.train_with_sample_data()

            # Assert: Verify training results
            assert result["accuracy"] > 0.9
            mock_ai_service.return_value.train_model.assert_called_once()
```

## Best Practices Summary

1. **Explicit Test Data**: Create all test data explicitly within tests
2. **Independent Tests**: Each test should run independently
3. **Clear Assertions**: Use descriptive assertion messages
4. **Fast Tests**: Mock external dependencies and avoid unnecessary delays
5. **Focused Tests**: Test one concept per test method
6. **Clean Fixtures**: Use function-scoped fixtures when possible
7. **DRY Principles**: Extract common test code into reusable helpers

## Integration with Other Skills

This skill enhances:
- **test-driven-development**: By preventing common TDD pitfalls
- **verification-before-completion**: By ensuring test quality before completion
- **systematic-debugging**: By making test failures easier to debug

Use the detection tools regularly to maintain test suite health and prevent anti-pattern accumulation.