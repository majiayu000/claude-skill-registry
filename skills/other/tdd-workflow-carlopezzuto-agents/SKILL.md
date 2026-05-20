---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.
---

# Test-Driven Development Workflow

This skill ensures all code development follows TDD principles with comprehensive test coverage.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new services or classes

## Core Principles

### 1. Tests BEFORE Code

ALWAYS write tests first, then implement code to make tests pass.

### 2. Coverage Requirements

- Changed-lines coverage: >= 90%
- Global coverage: >= 85%
- Critical paths: 100%
- Error paths: >= 95%

### 3. Test Types

#### Unit Tests (~70%)

- Individual functions and utilities
- Class methods
- Pure functions
- Helpers and utilities

#### Integration Tests (~20%)

- API endpoints
- Database operations
- Service interactions
- External API calls

#### E2E Tests (~10% - Playwright)

- Critical user flows
- Complete workflows
- Browser automation
- UI interactions

## TDD Workflow Steps

### Step 1: Write User Stories

```
As a [role], I want to [action], so that [benefit]

Example:
As a recruiter, I want to match candidates to jobs semantically,
so that I can find relevant candidates even without exact skill matches.
```

### Step 2: Generate Test Cases

For each user story, create comprehensive test cases:

```python
import pytest
from unittest.mock import Mock, patch


class TestSemanticSearch:
    """Tests for semantic search functionality."""

    def test_returns_relevant_candidates_for_query(self, search_service):
        """Search returns candidates matching semantic query."""
        results = search_service.search("Python developer")

        assert len(results) > 0
        assert all(r.relevance_score > 0.7 for r in results)

    def test_handles_empty_query_gracefully(self, search_service):
        """Empty query returns empty results without error."""
        results = search_service.search("")

        assert results == []

    def test_falls_back_to_keyword_search_when_embedding_unavailable(
        self, search_service, mock_embedding_service
    ):
        """Falls back to keyword search when embedding fails."""
        mock_embedding_service.generate.side_effect = ConnectionError()

        results = search_service.search("Python")

        assert len(results) > 0  # Fallback worked

    def test_sorts_results_by_similarity_score(self, search_service):
        """Results are sorted by descending similarity score."""
        results = search_service.search("data scientist")

        scores = [r.relevance_score for r in results]
        assert scores == sorted(scores, reverse=True)
```

### Step 3: Run Tests (They Should Fail)

```bash
pytest tests/ -v
# Tests should fail - we haven't implemented yet
```

### Step 4: Implement Code

Write minimal code to make tests pass:

```python
class SemanticSearchService:
    """Service for semantic candidate search."""

    def __init__(self, embedding_service: EmbeddingService, repository: CandidateRepository):
        self._embedding_service = embedding_service
        self._repository = repository

    def search(self, query: str) -> list[SearchResult]:
        """Search candidates semantically."""
        if not query.strip():
            return []

        try:
            embedding = self._embedding_service.generate(query)
            candidates = self._repository.find_by_embedding(embedding)
        except ConnectionError:
            candidates = self._repository.find_by_keyword(query)

        return sorted(candidates, key=lambda c: c.relevance_score, reverse=True)
```

### Step 5: Run Tests Again

```bash
pytest tests/ -v
# Tests should now pass
```

### Step 6: Refactor

Improve code quality while keeping tests green:

- Remove duplication
- Improve naming
- Optimize performance
- Enhance readability

### Step 7: Verify Coverage

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=85
# Verify coverage thresholds achieved
```

## Testing Patterns

### Unit Test Pattern (pytest)

```python
import pytest
from src.services.candidate_scorer import CandidateScorer


class TestCandidateScorer:
    """Unit tests for CandidateScorer."""

    @pytest.fixture
    def scorer(self):
        """Create scorer instance for tests."""
        return CandidateScorer()

    def test_scores_perfect_match_as_1(self, scorer):
        """Perfect skill match scores 1.0."""
        candidate_skills = {"Python", "FastAPI", "PostgreSQL"}
        job_skills = {"Python", "FastAPI", "PostgreSQL"}

        score = scorer.calculate_skill_match(candidate_skills, job_skills)

        assert score == 1.0

    def test_scores_no_match_as_0(self, scorer):
        """No skill overlap scores 0.0."""
        candidate_skills = {"Java", "Spring"}
        job_skills = {"Python", "FastAPI"}

        score = scorer.calculate_skill_match(candidate_skills, job_skills)

        assert score == 0.0

    def test_scores_partial_match_proportionally(self, scorer):
        """Partial match scores proportionally."""
        candidate_skills = {"Python", "Java"}
        job_skills = {"Python", "FastAPI", "PostgreSQL"}

        score = scorer.calculate_skill_match(candidate_skills, job_skills)

        assert 0.3 <= score <= 0.4  # 1/3 match
```

### API Integration Test Pattern (FastAPI)

```python
import pytest
from httpx import AsyncClient
from fastapi import status

from src.main import app


@pytest.mark.asyncio
class TestCandidatesAPI:
    """Integration tests for candidates API."""

    async def test_search_candidates_returns_results(self, client: AsyncClient):
        """GET /api/candidates/search returns matching candidates."""
        response = await client.get("/api/candidates/search", params={"q": "Python"})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)

    async def test_search_validates_query_parameter(self, client: AsyncClient):
        """GET /api/candidates/search validates query params."""
        response = await client.get("/api/candidates/search", params={"limit": "invalid"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_search_handles_database_errors_gracefully(
        self, client: AsyncClient, mock_db_failure
    ):
        """Database errors return 500 with generic message."""
        response = await client.get("/api/candidates/search", params={"q": "test"})

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "detail" in data
        assert "database" not in data["detail"].lower()  # No leak
```

### E2E Test Pattern (Playwright)

```python
import pytest
from playwright.sync_api import Page, expect


class TestCandidateSearchFlow:
    """E2E tests for candidate search user flow."""

    def test_user_can_search_and_view_candidate(self, page: Page):
        """Complete user journey: search -> view candidate."""
        # Navigate to candidates page
        page.goto("/candidates")

        # Verify page loaded
        expect(page.locator("h1")).to_contain_text("Candidates")

        # Search for candidates
        page.fill('input[placeholder="Search candidates"]', "Python developer")

        # Wait for debounce and results
        page.wait_for_response(
            lambda resp: "/api/candidates/search" in resp.url and resp.status == 200
        )

        # Verify search results displayed
        results = page.locator('[data-testid="candidate-card"]')
        expect(results.first).to_be_visible()

        # Click on first result
        results.first.click()

        # Verify candidate details page loads
        expect(page).to_have_url(r"/candidates/[a-z0-9-]+")
        expect(page.locator('[data-testid="candidate-name"]')).to_be_visible()

    def test_search_with_no_results_shows_empty_state(self, page: Page):
        """Empty search results show appropriate message."""
        page.goto("/candidates")

        page.fill('input[placeholder="Search candidates"]', "xyznonexistent123456")

        page.wait_for_load_state("networkidle")

        no_results = page.locator('[data-testid="no-results"]')
        expect(no_results).to_be_visible()
        expect(no_results).to_contain_text("No candidates found")
```

## Test File Organization

```
tests/
├── unit/
│   ├── services/
│   │   ├── test_candidate_scorer.py
│   │   └── test_embedding_service.py
│   ├── repositories/
│   │   └── test_candidate_repository.py
│   └── utils/
│       └── test_skill_normalizer.py
├── integration/
│   ├── api/
│   │   ├── test_candidates_api.py
│   │   └── test_jobs_api.py
│   └── database/
│       └── test_candidate_queries.py
├── e2e/
│   ├── test_candidate_search.py
│   ├── test_job_matching.py
│   └── test_export_results.py
├── fixtures/
│   ├── candidates.py
│   └── jobs.py
└── conftest.py
```

## Mocking External Services

### Database Mock

```python
import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def mock_db_session():
    """Mock database session."""
    session = AsyncMock()
    session.execute.return_value.scalars.return_value.all.return_value = [
        Candidate(id=1, name="John Doe", skills=["Python", "FastAPI"])
    ]
    return session
```

### Embedding Service Mock

```python
import pytest
from unittest.mock import Mock
import numpy as np


@pytest.fixture
def mock_embedding_service():
    """Mock embedding service."""
    service = Mock()
    service.generate.return_value = np.random.rand(1536).tolist()
    return service
```

### External API Mock

```python
import pytest
from unittest.mock import patch


@pytest.fixture
def mock_esco_api():
    """Mock ESCO API responses."""
    with patch("src.integrations.esco_client.ESCOClient") as mock:
        mock.return_value.get_skills.return_value = [
            {"uri": "http://esco/skill/1", "label": "Python programming"}
        ]
        yield mock
```

## Test Coverage Configuration

### pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = [
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=85",
]

[tool.coverage.run]
branch = true
source = ["src"]
omit = ["*/__init__.py", "*/migrations/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

## Common Testing Mistakes to Avoid

### Testing Implementation Details

```python
# BAD - Testing private methods
def test_private_method(self):
    assert obj._internal_state == expected

# GOOD - Testing public behavior
def test_public_behavior(self):
    assert obj.get_result() == expected
```

### Multiple Behaviors Per Test

```python
# BAD - Testing multiple behaviors
def test_everything(self):
    assert validator.is_valid(data1)
    assert not validator.is_valid(data2)
    assert validator.errors == expected

# GOOD - Separate tests
def test_accepts_valid_data(self):
    assert validator.is_valid(valid_data)

def test_rejects_invalid_data(self):
    assert not validator.is_valid(invalid_data)
```

### Excessive Mocking

```python
# BAD - Mocking everything
def test_with_all_mocks(self):
    mock_db = Mock()
    mock_cache = Mock()
    mock_validator = Mock()
    service = Service(mock_db, mock_cache, mock_validator)

# GOOD - Mock only external dependencies
def test_with_minimal_mocks(self):
    real_validator = Validator()
    real_cache = InMemoryCache()
    mock_db = Mock()  # Only mock external dependency
    service = Service(mock_db, real_cache, real_validator)
```

### Brittle Selectors (E2E)

```python
# BAD - Breaks easily
await page.click(".css-class-xyz")

# GOOD - Resilient to changes
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

### No Test Isolation

```python
# BAD - Tests depend on each other
def test_creates_user(self):
    self.user = create_user()

def test_updates_same_user(self):
    update_user(self.user)  # Depends on previous test!

# GOOD - Independent tests
def test_creates_user(self):
    user = create_test_user()
    # Test logic

def test_updates_user(self):
    user = create_test_user()
    update_user(user)
```

## Continuous Testing

### Watch Mode During Development

```bash
pytest-watch
# Tests run automatically on file changes
```

### Pre-Commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest tests/unit -q
        language: system
        pass_filenames: false
        always_run: true
```

### CI/CD Integration

```yaml
# GitHub Actions
- name: Run Tests
  run: pytest --cov=src --cov-report=xml

- name: Upload Coverage
  uses: codecov/codecov-action@v4
  with:
    files: coverage.xml
```

## Best Practices

1. **Write Tests First** - Always TDD
2. **One Assert Per Test** - Focus on single behavior
3. **Descriptive Test Names** - Explain what's tested
4. **Arrange-Act-Assert** - Clear test structure
5. **Mock External Dependencies** - Isolate unit tests
6. **Test Edge Cases** - None, empty, boundary values
7. **Test Error Paths** - Not just happy paths
8. **Keep Tests Fast** - Unit tests < 100ms each
9. **Clean Up After Tests** - No side effects
10. **Review Coverage Reports** - Identify gaps

## Success Metrics

- Changed-lines coverage >= 90%
- Global coverage >= 85%
- All tests passing (green)
- No skipped or disabled tests
- Fast test execution (unit < 100ms, integration < 1s, E2E < 10s)
- E2E tests cover critical user flows
- Tests catch bugs before production

---

**Remember**: Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability. One vulnerability can compromise the entire platform.
