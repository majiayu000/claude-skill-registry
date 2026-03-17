---
name: testing-strategy
description: 当用户要求"编写测试"、"创建测试用例"、"添加单元测试"、"添加集成测试"、"测试覆盖率"、"模拟命令"，或者提到"测试"、"TDD"、"测试夹具"时使用此技能。用于测试策略、测试模式、mocking 或 Rust 后端和 React 前端的质量保证。
version: 2.0.0
---

# Testing Strategy Skill

Comprehensive testing guidance for Tauri applications with Rust backend and React frontend.

## Overview

This skill provides testing strategies for:
- Rust unit and integration tests
- React component and hook tests
- Tauri command mocking
- Database testing with fixtures
- Test coverage and quality gates
- TDD (Test-Driven Development) workflows

## When This Skill Applies

This skill activates when:
- Writing new tests for Rust or TypeScript code
- Implementing test doubles and mocks
- Setting up test infrastructure
- Debugging test failures
- Improving test coverage
- Planning testing strategy for features

## Rust Testing

### Unit Tests

**Location**: In the same module as the code being tested

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_formula_cost_calculation() {
        let materials = vec![
            FormulaMaterial {
                material_code: "corn".to_string(),
                proportion: 50.0,
                price: 2.5,
            },
            FormulaMaterial {
                material_code: "soybean".to_string(),
                proportion: 50.0,
                price: 3.0,
            },
        ];

        let cost = calculate_total_cost(&materials);
        assert!((cost - 2.75).abs() < 0.01); // Average of 2.5 and 3.0
    }

    #[test]
    fn test_empty_materials() {
        let materials = vec![];
        let cost = calculate_total_cost(&materials);
        assert_eq!(cost, 0.0);
    }

    #[test]
    #[should_panic(expected = "Proportion cannot be negative")]
    fn test_negative_proportion_panics() {
        let material = FormulaMaterial {
            material_code: "test".to_string(),
            proportion: -10.0,
            price: 1.0,
        };
        validate_material(&material);
    }
}
```

### Integration Tests

**Location**: `tests/` directory at project root

```rust
// tests/formula_integration_tests.rs
use ca_cr_feed_formula::database::create_pool;
use ca_cr_feed_formula::formula::FormulaService;

#[tokio::test]
async fn test_create_and_retrieve_formula() {
    // Use test database
    let pool = create_pool(":memory:").await.expect("Failed to create pool");
    let service = FormulaService::new(pool);

    // Create formula
    let create_dto = CreateFormulaDto {
        name: "Test Formula".to_string(),
        species_code: "pig".to_string(),
        description: None,
    };

    let formula_id = service.create_formula(create_dto)
        .await
        .expect("Failed to create formula");

    // Retrieve formula
    let formula = service.get_formula(formula_id)
        .await
        .expect("Failed to retrieve formula");

    assert_eq!(formula.name, "Test Formula");
    assert_eq!(formula.species_code, "pig");
}

#[tokio::test]
async fn test_formula_not_found() {
    let pool = create_pool(":memory:").await.expect("Failed to create pool");
    let service = FormulaService::new(pool);

    let result = service.get_formula(99999).await;
    assert!(result.is_err());
}
```

### Database Fixtures

```rust
pub struct TestFixture {
    pub pool: SqlitePool,
    pub material_service: MaterialService,
    pub formula_service: FormulaService,
}

impl TestFixture {
    pub async fn setup() -> Self {
        let pool = create_pool(":memory:").await.unwrap();

        // Run migrations
        sqlx::migrate!("./migrations")
            .run(&pool)
            .await
            .unwrap();

        // Insert test data
        Self::seed_test_data(&pool).await;

        Self {
            pool: pool.clone(),
            material_service: MaterialService::new(pool.clone()),
            formula_service: FormulaService::new(pool),
        }
    }

    async fn seed_test_data(pool: &SqlitePool) {
        // Insert test materials
        sqlx::query!(
            "INSERT INTO materials (code, name, price, category) VALUES (?, ?, ?, ?)",
            "corn", "Corn", 2.5, "energy"
        )
        .execute(pool)
        .await
        .unwrap();

        sqlx::query!(
            "INSERT INTO materials (code, name, price, category) VALUES (?, ?, ?, ?)",
            "soybean", "Soybean Meal", 3.0, "protein"
        )
        .execute(pool)
        .await
        .unwrap();
    }

    pub async fn teardown(self) {
        self.pool.close().await;
    }
}

#[tokio::test]
async fn test_with_fixture() {
    let fixture = TestFixture::setup().await;

    let corn = fixture.material_service.get_material("corn")
        .await
        .unwrap();

    assert_eq!(corn.name, "Corn");

    fixture.teardown().await;
}
```

## React Testing

### Component Tests

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FormulaForm } from './FormulaForm';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { message } from 'antd';

// Mock Tauri commands
vi.mock('../bindings', () => ({
  commands: {
    createFormula: vi.fn(),
    updateFormula: vi.fn(),
  },
}));

// Mock message
vi.mock('antd', async () => ({
  ...((await vi.importActual('antd')) as any),
  message: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));

describe('FormulaForm', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render form fields', () => {
    render(<FormulaForm />, { wrapper });

    expect(screen.getByLabelText(/配方名称/)).toBeInTheDocument();
    expect(screen.getByLabelText(/品种代码/)).toBeInTheDocument();
  });

  it('should show validation errors for empty name', async () => {
    const user = userEvent.setup();
    render(<FormulaForm />, { wrapper });

    const submitButton = screen.getByText(/保存/);
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/请输入配方名称/)).toBeInTheDocument();
    });
  });

  it('should submit form with valid data', async () => {
    const mockCreate = vi.mocked(commands.createFormula);
    mockCreate.mockResolvedValueOnce({
      success: true,
      data: { id: 1, name: '测试配方' },
    });

    const user = userEvent.setup();
    render(<FormulaForm />, { wrapper });

    await user.type(screen.getByLabelText(/配方名称/), '测试配方');
    await user.click(screen.getByText(/保存/));

    await waitFor(() => {
      expect(mockCreate).toHaveBeenCalledWith({
        name: '测试配方',
        species_code: 'pig',
      });
      expect(message.success).toHaveBeenCalledWith('保存成功');
    });
  });

  it('should handle API errors', async () => {
    const mockCreate = vi.mocked(commands.createFormula);
    mockCreate.mockResolvedValueOnce({
      success: false,
      message: '创建失败：配方已存在',
    });

    const user = userEvent.setup();
    render(<FormulaForm />, { wrapper });

    await user.type(screen.getByLabelText(/配方名称/), '测试配方');
    await user.click(screen.getByText(/保存/));

    await waitFor(() => {
      expect(message.error).toHaveBeenCalledWith('创建失败：配方已存在');
    });
  });
});
```

### Hook Tests

```typescript
import { renderHook, act, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useMaterials } from './useMaterials';

vi.mock('../bindings', () => ({
  commands: {
    getMaterials: vi.fn(),
  },
}));

describe('useMaterials', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
      },
    });
  });

  it('should fetch materials successfully', async () => {
    const mockData = [
      { code: 'corn', name: 'Corn', price: 2.5 },
      { code: 'soybean', name: 'Soybean', price: 3.0 },
    ];

    vi.mocked(commands.getMaterials).mockResolvedValueOnce({
      success: true,
      data: mockData,
    });

    const { result } = renderHook(() => useMaterials(), {
      wrapper: ({ children }) => (
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
      ),
    });

    expect(result.current.isLoading).toBe(true);

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
      expect(result.current.materials).toEqual(mockData);
    });
  });

  it('should handle fetch errors', async () => {
    vi.mocked(commands.getMaterials).mockResolvedValueOnce({
      success: false,
      message: 'Failed to load materials',
    });

    const { result } = renderHook(() => useMaterials(), {
      wrapper: ({ children }) => (
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
      ),
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
      expect(result.current.materials).toBeNull();
    });
  });
});
```

## TDD Workflow

### Red-Green-Refactor Cycle

```bash
# 1. RED: Write failing test
# 2. GREEN: Write minimum code to pass
# 3. REFACTOR: Improve code while tests pass
```

**Example: TDD for Nutrition Calculation**

```rust
// Step 1: Write failing test (RED)
#[test]
fn test_calculate_protein_content() {
    let materials = vec![
        create_material("corn", 8.5),  // 8.5% protein
        create_material("soybean", 44.0),  // 44% protein
    ];
    let proportions = vec![50.0, 50.0];  // 50% each

    let protein = calculate_nutrient(&materials, &proportions, "protein");
    assert!((protein - 26.25).abs() < 0.01);  // Weighted average
}

// Step 2: Write minimum implementation (GREEN)
fn calculate_nutrient(
    materials: &[Material],
    proportions: &[f64],
    nutrient_code: &str,
) -> f64 {
    materials
        .iter()
        .zip(proportions.iter())
        .map(|(m, prop)| {
            let value = m.nutrients.get(nutrient_code).copied().unwrap_or(0.0);
            value * (prop / 100.0)
        })
        .sum()
}

// Step 3: Refactor (REFACTOR)
// Improve code structure, add validation, optimize performance
```

## Test Coverage

### Setting Up Coverage

**Rust (tarpaulin):**

```bash
cargo install tarpaulin

# Generate coverage report
cargo tarpaulin --out Html --output-dir coverage

# View report
open coverage/index.html
```

**TypeScript (vitest):**

```bash
# Add to package.json
{
  "scripts": {
    "test": "vitest",
    "test:coverage": "vitest --coverage"
  }
}

# Run coverage
npm run test:coverage
```

### Coverage Goals

| Component Type | Target Coverage |
|----------------|-----------------|
| Business logic (Rust) | > 90% |
| UI Components | > 80% |
| Utilities/Helpers | > 95% |
| Integration tests | Key workflows only |

## Testing Best Practices

### DO's ✅

- Write tests before implementation (TDD)
- Use descriptive test names (`test_calculate_cost_with_discount`)
- Test edge cases and error conditions
- Mock external dependencies (database, API)
- Keep tests independent and isolated
- Use fixtures for complex test data
- Test behavior, not implementation

### DON'Ts ❌

- Don't test trivial getters/setters
- Don't write tests that are tightly coupled to implementation
- Don't use shared state between tests
- Don't ignore failing tests
- Don't mock code you own (only external deps)
- Don't write tests that are too complex to understand

## Quick Reference

### Test Structure Template

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_descriptive_name() {
        // Arrange
        let input = setup_test_data();

        // Act
        let result = function_under_test(input);

        // Assert
        assert_eq!(result, expected);
    }
}
```

### React Test Template

```typescript
describe('ComponentName', () => {
  it('should do something when condition', () => {
    // Arrange
    render(<ComponentName prop="value" />);

    // Act
    fireEvent.click(screen.getByText('Button'));

    // Assert
    expect(screen.getByText('Result')).toBeInTheDocument();
  });
});
```

### Common Test Commands

```bash
# Rust tests
cargo test                      # Run all tests
cargo test test_name            # Run specific test
cargo test -- --nocapture       # Show print output
cargo nextest run              # Faster test runner

# TypeScript tests
npm test                       # Run all tests
npm test -- FormulaForm        # Run specific file
npm run test:coverage          # With coverage
```

## When to Use This Skill

Activate this skill when:
- Writing new tests for Rust or TypeScript
- Setting up test infrastructure
- Debugging test failures
- Improving test coverage
- Planning testing strategy
- Implementing TDD workflow
- Creating mocks and fixtures
