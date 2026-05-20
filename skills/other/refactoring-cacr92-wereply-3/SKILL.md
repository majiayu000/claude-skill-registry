---
name: refactoring
description: 当用户要求"重构代码"、"改进代码结构"、"清理代码"、"降低复杂度"、"提取方法"，或者提到"重构"、"refactoring"、"代码异味"、"技术债"、"遗留代码"时使用此技能。用于在不改变功能的前提下提高代码质量、可维护性或设计。
version: 2.0.0
---

# Refactoring Skill

Systematic code refactoring guidance for improving code quality, maintainability, and design without changing functionality.

## Overview

This skill provides refactoring strategies for:
- **Extracting methods/functions** for better organization
- **Removing code duplication** (DRY principle)
- **Simplifying complex logic** and reducing cyclomatic complexity
- **Improving naming** and readability
- **Applying design patterns** appropriately
- **Reducing technical debt** while maintaining functionality

## When This Skill Applies

This skill activates when:
- Code is difficult to understand or maintain
- Functions/methods are too long or complex
- Similar code appears in multiple places
- Naming is unclear or inconsistent
- Design patterns could improve structure
- Technical debt needs to be reduced
- Performance optimizations are needed

## Refactoring Principles

### Core Rules

1. **Preserve Functionality**: Refactoring should NOT change behavior
2. **Small Steps**: Make incremental changes with tests between each
3. **Test Coverage**: Ensure tests pass before and after refactoring
4. **Commit Often**: Save working state frequently
5. **Document Why**: Explain reasons for significant changes

### Red, Green, Refactor

```bash
# 1. Ensure tests pass (GREEN)
cargo test
npm test

# 2. Make small refactoring change
# 3. Run tests again (still GREEN)
cargo test
npm test

# 4. Commit if tests pass
git commit -m "refactor: extract material validation logic"

# Repeat
```

## Common Code Smells & Refactorings

### 1. Long Method/Function

**Smell:**
```rust
// ❌ 200+ line function doing multiple things
pub async fn create_formula_with_materials(
    &self,
    dto: CreateFormulaDto,
) -> Result<Formula> {
    // Validate name
    if dto.name.is_empty() {
        return Err(anyhow!("Name cannot be empty"));
    }
    if dto.name.len() > 100 {
        return Err(anyhow!("Name too long"));
    }
    // ... 50 more validation lines

    // Check duplicate name
    let exists = sqlx::query_scalar!(
        "SELECT COUNT(*) FROM formulas WHERE name = ?",
        dto.name
    )
    .fetch_one(&self.pool)
    .await?;
    if exists > 0 {
        return Err(anyhow!("Formula already exists"));
    }

    // Validate materials
    for material in &dto.materials {
        if material.proportion < 0.0 || material.proportion > 100.0 {
            return Err(anyhow!("Invalid proportion"));
        }
        // ... 30 more validation lines
    }

    // Insert formula
    // ... 100 more lines
}
```

**Refactor - Extract Methods:**
```rust
// ✅ Broken into focused functions
pub async fn create_formula_with_materials(
    &self,
    dto: CreateFormulaDto,
) -> Result<Formula> {
    self.validate_formula_dto(&dto)?;
    self.check_duplicate_formula(&dto.name).await?;
    self.validate_materials(&dto.materials)?;
    self.insert_formula_with_materials(dto).await
}

// Extracted: Name validation
fn validate_formula_dto(&self, dto: &CreateFormulaDto) -> Result<()> {
    validate_non_empty(&dto.name, "配方名称")?;
    validate_max_length(&dto.name, 100, "配方名称")?;
    validate_species_code(&dto.species_code)?;
    Ok(())
}

// Extracted: Duplicate check
async fn check_duplicate_formula(&self, name: &str) -> Result<()> {
    let exists = sqlx::query_scalar!(
        "SELECT COUNT(*) FROM formulas WHERE name = ?",
        name
    )
    .fetch_one(&self.pool)
    .await?;

    if exists > 0 {
        return Err(anyhow!("配方名称已存在"));
    }
    Ok(())
}

// Extracted: Material validation
fn validate_materials(&self, materials: &[FormulaMaterialDto]) -> Result<()> {
    let total: f64 = materials.iter().map(|m| m.proportion).sum();

    if (total - 100.0).abs() > 0.01 {
        return Err(anyhow!("原料总比例必须为100%"));
    }

    for material in materials {
        validate_proportion(material.proportion)?;
    }
    Ok(())
}
```

### 2. Code Duplication (DRY Violation)

**Smell:**
```typescript
// ❌ Same validation logic repeated
function validateFormulaName(name: string): void {
  if (!name || name.length < 2) {
    message.error('名称至少2个字符');
    return;
  }
  if (name.length > 100) {
    message.error('名称最多100个字符');
    return;
  }
}

function validateMaterialName(name: string): void {
  if (!name || name.length < 2) {
    message.error('名称至少2个字符');
    return;
  }
  if (name.length > 100) {
    message.error('名称最多100个字符');
    return;
  }
}
```

**Refactor - Extract Common Function:**
```typescript
// ✅ Reusable validation function
interface ValidationRule {
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  fieldName: string;
}

function validateName(name: string, rule: ValidationRule): boolean {
  if (!name) {
    message.error(`${rule.fieldName}不能为空`);
    return false;
  }

  if (rule.minLength && name.length < rule.minLength) {
    message.error(`${rule.fieldName}至少${rule.minLength}个字符`);
    return false;
  }

  if (rule.maxLength && name.length > rule.maxLength) {
    message.error(`${rule.fieldName}最多${rule.maxLength}个字符`);
    return false;
  }

  if (rule.pattern && !rule.pattern.test(name)) {
    message.error(`${rule.fieldName}格式不正确`);
    return false;
  }

  return true;
}

// Usage
validateFormulaName(name, {
  minLength: 2,
  maxLength: 100,
  fieldName: '配方名称'
});

validateMaterialName(name, {
  minLength: 2,
  maxLength: 100,
  pattern: /^[A-Z0-9_]+$/,
  fieldName: '原料代码'
});
```

### 3. Complex Conditional Logic

**Smell:**
```rust
// ❌ Nested conditionals (Arrow Code)
pub async fn get_formula_materials(&self, formula_id: i64) -> Result<Vec<Material>> {
    if formula_id > 0 {
        let formula = self.get_by_id(formula_id).await?;
        if formula.is_active {
            if formula.materials.len() > 0 {
                return Ok(formula.materials);
            } else {
                return Err(anyhow!("配方没有原料"));
            }
        } else {
            return Err(anyhow!("配方未激活"));
        }
    } else {
        return Err(anyhow!("无效的ID"));
    }
}
```

**Refactor - Early Returns (Guard Clauses):**
```rust
// ✅ Flat structure with guard clauses
pub async fn get_formula_materials(&self, formula_id: i64) -> Result<Vec<Material>> {
    // Guard clauses
    if formula_id <= 0 {
        return Err(anyhow!("无效的ID"));
    }

    let formula = self.get_by_id(formula_id).await?;

    if !formula.is_active {
        return Err(anyhow!("配方未激活"));
    }

    if formula.materials.is_empty() {
        return Err(anyhow!("配方没有原料"));
    }

    Ok(formula.materials)
}
```

### 4. Magic Numbers/Strings

**Smell:**
```rust
// ❌ Magic numbers
pub fn calculate_discount(price: f64) -> f64 {
    if price > 1000 {
        price * 0.85  // What is 0.85?
    } else if price > 500 {
        price * 0.90
    } else {
        price
    }
}
```

**Refactor - Named Constants:**
```rust
// ✅ Self-documenting constants
pub const DISCOUNT_THRESHOLD_HIGH: f64 = 1000.0;
pub const DISCOUNT_THRESHOLD_MEDIUM: f64 = 500.0;
pub const DISCOUNT_RATE_HIGH: f64 = 0.85;   // 15% off
pub const DISCOUNT_RATE_MEDIUM: f64 = 0.90; // 10% off

pub fn calculate_discount(price: f64) -> f64 {
    if price > DISCOUNT_THRESHOLD_HIGH {
        price * DISCOUNT_RATE_HIGH
    } else if price > DISCOUNT_THRESHOLD_MEDIUM {
        price * DISCOUNT_RATE_MEDIUM
    } else {
        price
    }
}
```

### 5. Large Interface/Class

**Smell:**
```rust
// ❌ God object doing too much
pub struct FormulaService {
    db: SqlitePool,
    material_service: MaterialService,
    species_service: SpeciesService,
    optimization_service: OptimizationService,
    calculation_service: CalculationService,
    validation_service: ValidationService,
    export_service: ExportService,
    notification_service: NotificationService,
    // ... 20 more fields
}
```

**Refactor - Single Responsibility:**
```rust
// ✅ Focused services with clear responsibilities
pub struct FormulaService {
    db: SqlitePool,
}

impl FormulaService {
    pub async fn create(&self, dto: CreateDto) -> Result<Formula> { }
    pub async fn get(&self, id: i64) -> Result<Formula> { }
    pub async fn update(&self, id: i64, dto: UpdateDto) -> Result<Formula> { }
    pub async fn delete(&self, id: i64) -> Result<()> { }
    pub async fn list(&self, params: ListParams) -> Result<Vec<Formula>> { }
}

pub struct FormulaOptimizer {
    highs_solver: HighsSolver,
}

impl FormulaOptimizer {
    pub async fn optimize(&self, request: OptimizationRequest) -> Result<OptimizationResult> { }
}
```

### 6. Feature Envy

**Smell:**
```rust
// ❌ Method that should be on another object
impl Formula {
    pub fn calculate_material_nutrition(&self, material: &Material) -> f64 {
        // Lots of logic about materials, not formulas
        let protein = material.nutrition.get("protein").unwrap_or(&0.0);
        let energy = material.nutrition.get("energy").unwrap_or(&0.0);
        // ... 20 more lines dealing with material internals
    }
}
```

**Refactor - Move Method:**
```rust
// ✅ Method belongs on Material
impl Material {
    pub fn get_nutrition(&self, nutrient_code: &str) -> f64 {
        self.nutrition.get(nutrient_code).copied().unwrap_or(0.0)
    }
}

impl Formula {
    pub fn calculate_total_nutrition(&self, nutrient_code: &str) -> f64 {
        self.materials.iter()
            .map(|m| m.get_nutrition(nutrient_code) * m.proportion / 100.0)
            .sum()
    }
}
```

## React-Specific Refactorings

### Extract Custom Hooks

**Before:**
```typescript
// ❌ Component with mixed concerns
export const FormulaList: React.FC = () => {
  const [formulas, setFormulas] = useState<Formula[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    commands.getFormulas()
      .then(result => {
        if (result.success) {
          setFormulas(result.data);
        } else {
          setError(result.message);
        }
      })
      .finally(() => setLoading(false));
  }, []);

  // 50 more lines of data fetching and state management
  // plus rendering logic mixed in
};
```

**After:**
```typescript
// ✅ Extracted custom hook
export function useFormulas() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['formulas'],
    queryFn: async () => {
      const result = await commands.getFormulas();
      if (!result.success) throw new Error(result.message);
      return result.data;
    },
  });

  return {
    formulas: data ?? [],
    isLoading,
    error: error?.message,
  };
}

// ✅ Simplified component
export const FormulaList: React.FC = () => {
  const { formulas, isLoading, error } = useFormulas();

  if (isLoading) return <Spin />;
  if (error) return <Alert message={error} type="error" />;

  return <FormulaTable formulas={formulas} />;
};
```

### Extract Components

**Before:**
```typescript
// ❌ 200+ line component
export const FormulaEditor: React.FC = () => {
  return (
    <div>
      {/* 50 lines for name input */}
      <Input label="配方名称" ... />
      <Input label="品种代码" ... />
      <Input label="描述" ... />

      {/* 100 lines for material table */}
      <Table columns={[...]} dataSource={...} />

      {/* 50 lines for nutrition display */}
      <div>蛋白质: {nutrition.protein}</div>
      <div>能量: {nutrition.energy}</div>
      {/* ... more nutrition fields */}
    </div>
  );
};
```

**After:**
```typescript
// ✅ Focused components
export const FormulaEditor: React.FC = () => {
  const [formulas, setFormulas] = useState<Formulas>(emptyFormulas);

  return (
    <div>
      <FormulaBasicInfoForm value={formulas} onChange={setFormulas} />
      <MaterialTable materials={formulas.materials} onChange={setFormulas} />
      <NutritionDisplay nutrition={formulas.nutrition} />
    </div>
  );
};

// Each component is focused and testable
```

## Refactoring Workflow

### Step 1: Identify the Smell

Ask yourself:
- What makes this code hard to understand?
- What would make it easier to maintain?
- Is there duplication?
- Are there too many responsibilities?
- Is the naming unclear?

### Step 2: Write Tests (If None Exist)

```rust
#[test]
fn test_current_behavior() {
    let input = create_test_input();
    let result = function_to_refactor(input);
    assert_eq!(result, expected_output);
}
```

### Step 3: Apply Refactoring (Small Steps)

1. Make one small change
2. Run tests: `cargo test` or `npm test`
3. If tests pass, commit
4. Repeat

### Step 4: Verify Behavior

```bash
# Run all tests
cargo test --all
npm test

# If available, run integration tests
cargo test --test integration

# Manual testing if needed
cargo run
npm run dev
```

### Step 5: Update Documentation

```markdown
## Refactoring Notes

### 2025-12-25: Extract Formula Validation

**Problem**: `create_formula` function was 200+ lines with mixed concerns

**Solution**:
- Extracted `validate_formula_dto()`
- Extracted `check_duplicate_formula()`
- Extracted `validate_materials()`

**Files Changed**:
- `src/formula/service.rs` (main changes)
- `src/formula/validation.rs` (new module)

**Tests**: All existing tests pass, no behavior changed
```

## Refactoring Checklist

### Before Refactoring
- [ ] Tests exist and pass
- [ ] Git working directory is clean
- [ ] Understand current behavior
- [ ] Have identified specific improvement

### During Refactoring
- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Commit often
- [ ] Don't change behavior yet (that's a feature change)

### After Refactoring
- [ ] All tests pass
- [ ] Code is more readable
- [ ] Duplication reduced
- [ ] Complexity reduced
- [ ] Documentation updated
- [ ] No unintended side effects

## Quick Reference

### Common Extract Refactorings

| Refactoring | Description | Shortcut |
|-------------|-------------|----------|
| Extract Method | Move code to new method/function | IDE: Extract function |
| Extract Variable | Complex expression → named variable | IDE: Introduce variable |
| Extract Constant | Magic value → named constant | Find/Replace |
| Inline Method | Simple method → inline it | IDE: Inline function |
| Rename | Better name for clarity | IDE: Rename symbol |
| Extract Interface | Common methods → interface | IDE: Extract interface |

### Rust-Specific Refactorings

```rust
// Use ? instead of match
// Before
match result {
    Ok(data) => data,
    Err(e) => return Err(e),
}

// After
result?
```

```rust
// Use iterators instead of loops
// Before
let mut result = Vec::new();
for item in items {
    if item.is_active {
        result.push(item);
    }
}

// After
let result: Vec<_> = items.iter()
    .filter(|item| item.is_active)
    .collect();
```

### React-Specific Refactorings

```typescript
// Use custom hooks for state logic
// Use React.memo for expensive components
// Use useMemo for expensive calculations
// Use useCallback for stable function references
// Extract components to reduce prop drilling
```

## When to Use This Skill

Activate this skill when:
- Code is difficult to understand
- Functions are too long or complex
- Similar code appears in multiple places
- Naming is unclear
- Design needs improvement
- Performance needs optimization
- Technical debt should be reduced
