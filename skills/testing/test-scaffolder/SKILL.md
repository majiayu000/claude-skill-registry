---
name: test-scaffolder
description: Generate test boilerplate from code or specs. Use for creating new tests, setting up test files, pytest fixtures, vitest tests, page objects, and E2E test scaffolding.
---

# Test Scaffolder Skill

**Activation:** create test, new test file, test boilerplate, scaffold test, generate test, page object

## Overview

Generate test boilerplate for pytest (backend), vitest (frontend), and Playwright E2E tests. Follows project patterns from the `testing` skill.

> **CRITICAL: Container-First Execution**
>
> All test commands run in Docker (except Playwright E2E which runs on host):
> ```bash
> docker compose exec backend pytest /tests/unit/backend/
> docker compose exec frontend pnpm test
> cd tests/e2e/playwright && pnpm test
> ```

## Pytest Unit Test Template

```python
# tests/unit/backend/services/test_{module}.py
"""Unit tests for {Module}Service."""
import pytest
from unittest.mock import Mock, AsyncMock

from app.services.{module} import {Module}Service


class Test{Module}Service:
    """Test cases for {Module}Service."""

    @pytest.fixture
    def service(self) -> {Module}Service:
        """Create service instance with mocked dependencies."""
        mock_repo = Mock()
        return {Module}Service(repository=mock_repo)

    def test_validate_input_success(self, service: {Module}Service) -> None:
        """Test input validation with valid data."""
        result = service.validate({"name": "test", "value": 42})
        assert result.is_valid is True

    def test_validate_input_failure(self, service: {Module}Service) -> None:
        """Test input validation with invalid data."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            service.validate({"name": "", "value": 42})

    @pytest.mark.parametrize("platform,expected", [
        ("nam", True),
        ("aida_x", True),
        ("invalid", False),
    ])
    def test_platform_validation(
        self,
        service: {Module}Service,
        platform: str,
        expected: bool,
    ) -> None:
        """Test platform validation against allowed values."""
        result = service.is_valid_platform(platform)
        assert result is expected
```

## Pytest Integration Test Template

```python
# tests/integration/backend/api/test_{endpoint}.py
"""Integration tests for {Endpoint} API."""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
@pytest.mark.integration
class Test{Endpoint}API:
    """Integration tests for {endpoint} endpoints."""

    async def test_create_success(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        test_user,
    ) -> None:
        """Test successful creation via POST."""
        response = await client.post(
            "/api/v1/{endpoint}",
            json={"name": "Test Item", "description": "Test"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Test Item"
        assert data["user_id"] == str(test_user.id)

    async def test_get_by_id(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        make_{entity},
    ) -> None:
        """Test GET by ID returns correct entity."""
        entity = await make_{entity}(name="Existing Item")

        response = await client.get(
            f"/api/v1/{endpoint}/{entity.id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Existing Item"

    async def test_get_not_found(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Test GET with non-existent ID returns 404."""
        response = await client.get(
            f"/api/v1/{endpoint}/{uuid4()}",
            headers=auth_headers,
        )

        assert response.status_code == 404

    async def test_list_with_pagination(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        make_{entity},
    ) -> None:
        """Test list endpoint with pagination."""
        for i in range(5):
            await make_{entity}(name=f"Item {i}")

        response = await client.get(
            "/api/v1/{endpoint}?limit=2&offset=0",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["{entities}"]) == 2
        assert data["total"] >= 5

    async def test_unauthorized_access(
        self,
        client: AsyncClient,
    ) -> None:
        """Test endpoint returns 401 without auth."""
        response = await client.get("/api/v1/{endpoint}")
        assert response.status_code == 401
```

## Pytest Factory Fixture Template

```python
# tests/integration/backend/conftest.py (add to existing)
@pytest.fixture(scope="function")
def make_{entity}(db_session: AsyncSession, test_user):
    """Factory fixture for creating {Entity} instances."""
    from app.models.{entity} import {Entity}

    async def _make_{entity}(
        name: str = "Test {Entity}",
        user=None,
        **kwargs,
    ) -> {Entity}:
        entity = {Entity}(
            id=uuid4(),
            user_id=(user or test_user).id,
            name=name,
            **kwargs,
        )
        db_session.add(entity)
        await db_session.flush()
        await db_session.refresh(entity)
        return entity

    return _make_{entity}
```

## Vitest Frontend Test Template

```typescript
// frontend/src/components/{Component}.test.tsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { {Component} } from './{Component}';

// Mock API calls
vi.mock('../lib/api', () => ({
  fetchJSON: vi.fn(),
}));

describe('{Component}', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
      },
    });
    vi.clearAllMocks();
  });

  const renderComponent = (props = {}) => {
    return render(
      <QueryClientProvider client={queryClient}>
        <{Component} {...props} />
      </QueryClientProvider>
    );
  };

  it('renders correctly', () => {
    renderComponent();
    expect(screen.getByRole('heading')).toBeInTheDocument();
  });

  it('displays loading state', () => {
    renderComponent();
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    const user = userEvent.setup();
    renderComponent();

    await user.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(screen.getByText(/success/i)).toBeInTheDocument();
    });
  });

  it('displays error state', async () => {
    const { fetchJSON } = await import('../lib/api');
    vi.mocked(fetchJSON).mockRejectedValue(new Error('API Error'));

    renderComponent();

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
```

## Playwright Page Object Template

```typescript
// tests/e2e/playwright/pages/{Page}Page.ts
import { Page, Locator, expect } from '@playwright/test';

export class {Page}Page {
  readonly page: Page;

  // Locators
  readonly heading: Locator;
  readonly nameInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly successMessage: Locator;
  readonly itemList: Locator;

  constructor(page: Page) {
    this.page = page;

    // Define locators (prefer test-id or role-based)
    this.heading = page.getByRole('heading', { name: /{Page}/i });
    this.nameInput = page.getByLabel('Name');
    this.submitButton = page.getByRole('button', { name: /submit/i });
    this.errorMessage = page.getByTestId('error-message');
    this.successMessage = page.getByTestId('success-message');
    this.itemList = page.getByTestId('{entity}-list');
  }

  // Navigation
  async goto(): Promise<void> {
    await this.page.goto('/{path}');
    await expect(this.heading).toBeVisible();
  }

  // Actions
  async fillForm(data: { name: string }): Promise<void> {
    await this.nameInput.fill(data.name);
  }

  async submit(): Promise<void> {
    await this.submitButton.click();
  }

  async createItem(name: string): Promise<void> {
    await this.fillForm({ name });
    await this.submit();
    await this.waitForSuccess();
  }

  // Assertions
  async expectError(message: string): Promise<void> {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toContainText(message);
  }

  async expectSuccess(): Promise<void> {
    await expect(this.successMessage).toBeVisible();
  }

  async waitForSuccess(): Promise<void> {
    await this.page.waitForResponse(
      resp => resp.url().includes('/api/v1/{endpoint}') && resp.ok()
    );
  }

  async expectItemCount(count: number): Promise<void> {
    await expect(this.itemList.getByRole('listitem')).toHaveCount(count);
  }

  async expectItemVisible(name: string): Promise<void> {
    await expect(this.itemList.getByText(name)).toBeVisible();
  }
}
```

## Playwright E2E Test Template

```typescript
// tests/e2e/playwright/tests/{feature}.spec.ts
import { test, expect } from '@playwright/test';
import { {Page}Page } from '../pages/{Page}Page';

test.describe('{Feature} E2E', () => {
  let {page}Page: {Page}Page;

  test.beforeEach(async ({ page }) => {
    {page}Page = new {Page}Page(page);
    await {page}Page.goto();
  });

  test('should display page correctly', async () => {
    await expect({page}Page.heading).toBeVisible();
    await expect({page}Page.submitButton).toBeEnabled();
  });

  test('should create item successfully', async ({ page }) => {
    const itemName = `E2E-Test-Item-${Date.now()}`;

    await {page}Page.createItem(itemName);

    // Verify in database via API
    const response = await page.request.get('/api/v1/{endpoint}');
    const data = await response.json();
    expect(data.{entities}.some(i => i.name === itemName)).toBe(true);
  });

  test('should show validation error for empty name', async () => {
    await {page}Page.fillForm({ name: '' });
    await {page}Page.submit();
    await {page}Page.expectError('Name is required');
  });

  test('should display items in list', async ({ page }) => {
    // Create test data
    const itemName = `E2E-Test-List-${Date.now()}`;
    await page.request.post('/api/v1/{endpoint}', {
      data: { name: itemName },
    });

    await page.reload();
    await {page}Page.expectItemVisible(itemName);
  });

  test.afterEach(async ({ page }) => {
    // Cleanup test data
    const response = await page.request.get('/api/v1/{endpoint}?search=E2E-Test');
    const data = await response.json();
    for (const item of data.{entities}) {
      await page.request.delete(`/api/v1/{endpoint}/${item.id}`);
    }
  });
});
```

## Quick Reference

| Test Type | Location | Template |
|-----------|----------|----------|
| Unit (backend) | `tests/unit/backend/` | Pytest class with fixtures |
| Integration (backend) | `tests/integration/backend/` | Pytest with real DB |
| Frontend (vitest) | `frontend/src/**/*.test.tsx` | Vitest + RTL |
| E2E (Playwright) | `tests/e2e/playwright/tests/` | TypeScript specs |
| Page Objects | `tests/e2e/playwright/pages/` | Page class pattern |

## Example Invocations

### Create Unit Test for Service
```
"Create unit tests for the AudioProcessingService"
-> Use Pytest Unit Test Template
-> Place in tests/unit/backend/services/test_audio_processing.py
```

### Create Integration Tests for API
```
"Scaffold integration tests for the /api/v1/shootouts endpoint"
-> Use Pytest Integration Test Template
-> Create factory fixture for shootout
-> Place in tests/integration/backend/api/test_shootouts.py
```

### Create Page Object for E2E
```
"Create a page object for the Signal Chain Builder page"
-> Use Page Object Template
-> Place in tests/e2e/playwright/pages/BuilderPage.ts
-> Create matching spec in tests/e2e/playwright/tests/builder.spec.ts
```

### Create Frontend Component Test
```
"Add vitest tests for the ShootoutCard component"
-> Use Vitest Frontend Test Template
-> Place in frontend/src/components/ShootoutCard.test.tsx
```

## Test Naming Conventions

| Convention | Example |
|------------|---------|
| Test file | `test_{module}.py` or `{Component}.test.tsx` |
| Test class | `Test{Feature}` |
| Test method | `test_{action}_{expected_result}` |
| Page object | `{Page}Page.ts` |
| E2E spec | `{feature}.spec.ts` |
