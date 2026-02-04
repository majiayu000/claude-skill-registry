---
name: architect
description: Expert guidance for GabeDA v2.1 architecture (34 modules) - implementing models, features, debugging 4-case logic, and maintaining the /src codebase.
version: 2.1.0
---

# GabeDA Architecture Expert

## Purpose

This skill provides expert guidance for the GabeDA v2.1 refactored architecture. It focuses on implementing models, adding features, debugging execution logic, and maintaining architectural principles across the 34-module `/src` codebase.

**Core Expertise:**
- `/src` architecture (34 modules in 6 packages)
- 4-case logic execution engine
- Feature implementation (filters, attributes, aggregations)
- Dependency resolution and data flow
- External data integration patterns
- Frontend development (React + TypeScript + Vite)
- Testing strategies and validation

## When to Use This Skill

Invoke this skill when:
- Working with the `/src` refactored codebase (v2.1)
- Implementing new aggregation models (daily, weekly, monthly, customer, product)
- Adding filters, attributes, or computed features
- Debugging 4-case logic execution issues
- Configuring external data joins
- **Developing frontend features (React + TypeScript + Vite)**
- **Troubleshooting blank pages or HMR issues**
- Understanding data flow and persistence strategies
- Troubleshooting column naming or dependency resolution
- Ensuring architectural principles are maintained
- Creating tests in `/test` folder

**NOT for:** Business strategy, marketing content, data analysis notebooks (delegate to business, marketing, insights skills)

## Quick Start

**Essential Documents:**
- 📚 **[Feature Implementation Guide](../../../ai/architect/feature_implementation_guide.md)** - **PRIMARY GUIDE** for implementation
- 📖 **[Documentation Master Index](../../../ai/README.md)** - Central hub for all documentation
- 🧪 **[Test Manifest](../../../ai/testing/TEST_MANIFEST.md)** - Complete test catalog (197 tests)
- 📝 **[Documentation Guidelines](../../../ai/standards/DOCUMENTATION_STANDARD.md)** - Before creating any docs

**Key References:**
- [references/module_reference.md](references/module_reference.md) - 34 modules structure
- [references/4_case_logic.md](references/4_case_logic.md) - Critical execution engine
- [references/external_data_integration.md](references/external_data_integration.md) - Column naming rules

## Core Architecture Overview

### Module Structure (v2.1)

**34 modules in 6 packages** following Single Responsibility Principle:

```
src/
├── utils/         # Utilities (7 modules) - 88 tests, 92% coverage
├── core/          # Core infrastructure (5 modules)
├── preprocessing/ # Data preparation (5 modules)
├── features/      # Feature management (4 modules)
├── execution/     # Feature computation (5 modules) - Includes 4-case logic
└── export/        # Output generation (2 modules)
```

**For complete module details:** See [references/module_reference.md](references/module_reference.md)

### Data Flow Pipeline

```
CSV → DataLoader → SchemaProcessor → SyntheticEnricher →
FeatureStore → DependencyResolver → ModelExecutor → ExcelExporter
```

**For detailed flow stages:** See [references/data_flow_pipeline.md](references/data_flow_pipeline.md)

### Critical: 4-Case Logic

The **GroupByProcessor** (`src/execution/groupby.py`) implements single-loop execution with 4 cases:

- **Case 1**: Standard filter (reads data_in only)
- **Case 2**: Filter using attributes (reads data_in + agg_results) **KEY INNOVATION**
- **Case 3**: Attribute with aggregation
- **Case 4**: Attribute composition (uses only other attributes)

**Case 2 Example:**
```python
def price_above_avg(price_total: float, prod_price_avg: float) -> bool:
    """Filter that uses an attribute as input"""
    return price_total > prod_price_avg
```

**For deep dive:** See [references/4_case_logic.md](references/4_case_logic.md)

## Core Workflows

### Workflow 1: Implementing a New Model

When creating daily, weekly, monthly, customer, or product aggregation models:

1. **Read primary guide** - [Feature Implementation Guide](../../../ai/architect/feature_implementation_guide.md)
2. **Define features** - Create filter and attribute functions with type hints
3. **Create features dictionary** - Register all features
4. **Configure model** - Set group_by, external_data, output_cols
5. **Verify naming** - Check external column prefixes (join keys NOT prefixed, others ARE)
6. **Test execution** - Verify output shapes and values
7. **Create tests** - Add repeatable tests in `/test` folder

**Detailed guide:** [assets/examples/implementing_new_model.md](assets/examples/implementing_new_model.md)

**Working examples:**
- [02_1_week.ipynb](../../../02_1_week.ipynb) - Weekly model with external data
- [01_1_1_day.ipynb](../../../01_1_1_day.ipynb) - Daily aggregation
- [03_consolidated_all_models.ipynb](../../../notebooks/from_store/03_consolidated_all_models.ipynb) - 9-model pipeline

### Workflow 2: Adding a New Feature

When adding filters (row-level) or attributes (aggregated):

1. **Define function** - Include type hints and docstring
2. **Determine type** - Filter (vectorized) or attribute (aggregated)?
3. **Register in dictionary** - Add to features dict
4. **Check dependencies** - Ensure resolvable via DFS
5. **Verify external data** - If using, check column naming
6. **Update model config** - Add to output_cols
7. **Create tests** - Add to `/test` folder with sample data

**Detailed guide:** [assets/examples/adding_new_feature.md](assets/examples/adding_new_feature.md)

**For feature type details:** See [references/feature_types.md](references/feature_types.md)

### Workflow 3: Configuring External Data

When joining external datasets (daily → weekly, customer → product):

1. **Verify dataset exists** - Check `ctx.list_datasets()`
2. **Configure in model** - Add external_data section with source, join_on, columns
3. **Remember naming rules:**
   - **Join keys:** NOT prefixed (e.g., `dt_date` stays `dt_date`)
   - **Regular columns:** ARE prefixed (e.g., `price_total_sum` → `daily_attrs_price_total_sum`)
4. **Write feature functions** - Use correct prefixed names
5. **Test join** - Verify merged data has expected columns

**Critical naming table:**

| Column Type | Original | After Merge | Prefixed? |
|-------------|----------|-------------|-----------|
| Join key | `dt_date` | `dt_date` | ❌ NO |
| Regular column | `price_total_sum` | `daily_attrs_price_total_sum` | ✅ YES |

**Detailed guide:** [assets/examples/configuring_external_data.md](assets/examples/configuring_external_data.md)

**For complete naming rules:** See [references/external_data_integration.md](references/external_data_integration.md)

### Workflow 4: Debugging Execution Issues

When encountering errors during model execution:

1. **Check error message** - "Argument 'X' not found" most common
2. **Verify column naming** - Join keys vs regular columns prefixes
3. **Validate external data** - Check dataset exists and join_on matches
4. **Print available columns** - Use `ctx.get_dataset('name').columns.tolist()`
5. **Test incrementally** - Add features one at a time
6. **Check dependencies** - Ensure DFS can resolve order

**Common error: "Argument not found"**

**Causes:**
1. External column wrong prefix (join key vs regular)
2. Missing external data config
3. Typo in column name

**Solution:**
```python
# 1. Check input dataset
print(ctx.get_dataset('transactions_filters').columns.tolist())

# 2. Check external dataset
print(ctx.get_dataset('daily_attrs').columns.tolist())

# 3. Remember: Join keys NO prefix, others WITH prefix
```

**For complete troubleshooting:** See [references/troubleshooting.md](references/troubleshooting.md)

### Workflow 5: Frontend Development (React/Vite)

**CRITICAL: Always clean dev environment BEFORE starting new features**

When working on frontend features (GabeDA Dashboard - React + TypeScript + Vite):

**Step 0: Clean Dev Environment (MANDATORY)**
```bash
# Kill all node processes to avoid port conflicts and HMR corruption
cd C:/Projects/play/gabeda_frontend
taskkill //F //IM node.exe

# Clear Vite cache
rm -rf node_modules/.vite

# Start fresh dev server
npm run dev
```

**Why This Matters:**
- **Problem**: Multiple Vite HMR instances can run simultaneously on different ports (5173, 5174, 5175...)
- **Symptom**: Blank pages, "module does not provide export" errors, stuck/corrupted state
- **Root Cause**: Old dev servers hold corrupted module cache, new changes start on different port
- **Solution**: Kill ALL node processes before starting work

**Quick Fix Script:** Use `restart-dev.bat` in frontend folder:
```batch
@echo off
taskkill //F //IM node.exe 2>nul
if exist node_modules\.vite rmdir /s /q node_modules\.vite
npm run dev
```

**Development Workflow:**
1. **CLEAN** - Run `restart-dev.bat` or kill node processes manually
2. **BRANCH** - Create feature branch (`git checkout -b feature/feature-name`)
3. **IMPLEMENT** - Make code changes
4. **BUILD** - Run `npm run build` to check for TypeScript errors
5. **TEST** - Test locally on http://localhost:5173 (verify correct port!)
6. **E2E** - Use Playwright skill for automated testing
7. **COMMIT** - Only after local verification passes
8. **DEPLOY** - Merge to main → auto-deploy to Render

**Common Issues:**
- **Blank pages on all routes** → Multiple Vite instances running, kill all node processes
- **"Module does not provide export" errors** → HMR cache corruption, clear `.vite` cache
- **Wrong port (5174, 5175 instead of 5173)** → Old servers still running, kill and restart
- **Changes not appearing** → Browser accessing old port, hard refresh (Ctrl+Shift+R) or use incognito

**Port Detection:**
```bash
# Check which port Vite started on (look for "Local: http://localhost:XXXX")
npm run dev

# If not 5173, there are stuck processes - kill and restart
```

**Best Practices:**
- **Always** kill node processes before starting new feature work
- **Always** verify you're accessing the correct port (check terminal output)
- **Always** use incognito/private browsing for testing to avoid browser cache issues
- **Always** build (`npm run build`) before committing to catch TypeScript errors
- **Never** commit without local testing on the correct port

## Core Principles (DO NOT BREAK)

✅ **Single Responsibility** - Each module does ONE thing
✅ **Single Input** - Each model gets exactly 1 dataframe
✅ **DFS Resolution** - Features auto-ordered by dependencies
✅ **4-Case Logic** - Filters can use attributes as inputs
✅ **Immutable Context** - User config never changes during execution
✅ **Save Checkpoints** - Save after every major transformation
✅ **Type Annotations** - All functions have type hints
✅ **Logging** - Every module uses get_logger(__name__)
✅ **Testing** - All tests MUST be in `/test` folder and be repeatable

**For detailed principles:** See [references/core_principles.md](references/core_principles.md)

## Testing Requirements

**Current Statistics:**
- **Total Tests:** 197 tests (6 integration, 108 unit, 69 validation, 14 notebook)
- **Code Coverage:** 85% (target: ≥85%)
- **Test Manifest:** [ai/testing/TEST_MANIFEST.md](../../../ai/testing/TEST_MANIFEST.md) **⭐ Living Document**

**Test Rules:**
1. **Location:** All tests MUST be in `/test` folder
2. **Repeatability:** Tests MUST be idempotent (run multiple times, same result)
3. **Cleanup:** Tests MUST delete temp files/folders
4. **Independence:** No external state dependencies
5. **Naming:** Use `test_{module_name}.py` or `test_{feature_name}.py`
6. **Documentation:** ALWAYS append to [Test Manifest](../../../ai/testing/TEST_MANIFEST.md)

**Running Tests:**
```bash
pytest test/              # All tests
pytest test/unit/         # Unit tests only
pytest test/integration/  # Integration tests only
pytest test/ -v           # With verbose output
```

**For complete testing guidelines:** See [references/testing_guidelines.md](references/testing_guidelines.md)

## Configuration Patterns

**Base Config:**
```python
base_cfg = {
    'input_file': 'path/to/data.csv',
    'client': 'project_name',
    'analysis_dt': 'YYYY-MM-DD',
    'data_schema': {
        'in_dt': {'source_column': 'Fecha venta', 'dtype': 'date'},
        'in_product_id': {'source_column': 'SKU', 'dtype': 'str'},
        'in_price_total': {'source_column': 'Total', 'dtype': 'float'}
    }
}
```

**Model Config (With External Data):**
```python
cfg_model = {
    'model_name': 'weekly',
    'group_by': ['dt_year', 'dt_weekofyear'],
    'row_id': 'in_trans_id',
    'output_cols': list(features.keys()),
    'features': features,
    'external_data': {
        'daily_attrs': {
            'source': 'daily_attrs',
            'join_on': ['dt_date'],
            'columns': None  # None = ALL, or ['col1', 'col2']
        }
    }
}
```

**For complete patterns:** See [references/configuration_patterns.md](references/configuration_patterns.md)

## Additional Resources

### Reference Documentation
- [module_reference.md](references/module_reference.md) - 34 modules structure with coverage stats
- [data_flow_pipeline.md](references/data_flow_pipeline.md) - 7-stage pipeline flow
- [4_case_logic.md](references/4_case_logic.md) - Critical execution engine **⭐ KEY INNOVATION**
- [feature_types.md](references/feature_types.md) - Filters vs attributes
- [dependency_resolution.md](references/dependency_resolution.md) - DFS traversal
- [configuration_patterns.md](references/configuration_patterns.md) - Config templates
- [external_data_integration.md](references/external_data_integration.md) - Column naming rules
- [synthetic_enrichment.md](references/synthetic_enrichment.md) - Auto-infer 17 columns
- [testing_guidelines.md](references/testing_guidelines.md) - Test requirements (197 tests)
- [troubleshooting.md](references/troubleshooting.md) - Common error patterns
- [core_principles.md](references/core_principles.md) - 9 DO NOT BREAK rules

### Implementation Examples
- [implementing_new_model.md](assets/examples/implementing_new_model.md) - Step-by-step model creation
- [adding_new_feature.md](assets/examples/adding_new_feature.md) - Filter and attribute addition
- [configuring_external_data.md](assets/examples/configuring_external_data.md) - External joins
- [adding_aggregation_level.md](assets/examples/adding_aggregation_level.md) - New aggregation levels

### External Documentation
- **[Feature Implementation Guide](../../../ai/architect/feature_implementation_guide.md)** - **PRIMARY REFERENCE**
- [Documentation Master Index](../../../ai/README.md) - All guides
- [Module Reference](../../../ai/specs/src/README.md) - Technical module docs
- [Model Specifications](../../../ai/specs/model/) - Tech specs, aggregation architecture

## Integration with Other Skills

### From Business Skill
- **Receive:** User stories, acceptance criteria, priority rankings, business requirements
- **Provide:** Technical feasibility assessment, effort estimates, architecture proposals
- **Example:** Business defines "VIP customer retention" → Architect implements RFM model

### From Executive Skill
- **Receive:** Feature requirements, quality standards, timeline constraints
- **Provide:** Implementation plans, trade-off analysis, technical specs
- **Example:** Executive prioritizes Chilean launch → Architect implements CLP currency support

### To Insights Skill
- **Provide:** Available features, data schema, execution capabilities
- **Receive:** Notebook requirements, visualization needs, metric definitions
- **Example:** Architect adds RFM model → Insights creates VIP retention notebook

### To Marketing Skill
- **Provide:** Technical capabilities, feature descriptions, performance metrics
- **Receive:** Feature positioning requirements, technical content needs
- **Example:** Architect implements 4-case logic → Marketing positions as "KEY INNOVATION"

## Living Documents (Append Only)

**When making changes, ALWAYS append to these 9 living documents:**

| Document | When to Use |
|----------|-------------|
| [CHANGELOG.md](../../../ai/CHANGELOG.md) | After modifying any `.py` file |
| [ISSUES.md](../../../ai/ISSUES.md) | After fixing bugs or errors |
| [PROJECT_STATUS.md](../../../ai/PROJECT_STATUS.md) | Weekly updates |
| [FEATURE_IMPLEMENTATIONS.md](../../../ai/FEATURE_IMPLEMENTATIONS.md) | After implementing features |
| [TESTING_RESULTS.md](../../../ai/TESTING_RESULTS.md) | After running tests |
| [TEST_MANIFEST.md](../../../ai/testing/TEST_MANIFEST.md) | **When adding/modifying tests** ⭐ |
| [ARCHITECTURE_DECISIONS.md](../../../ai/architect/ARCHITECTURE_DECISIONS.md) | When making architectural choices |
| [NOTEBOOK_IMPROVEMENTS.md](../../../ai/guides/NOTEBOOK_IMPROVEMENTS.md) | When improving notebooks |
| [FUTURE_ENHANCEMENTS.md](../../../ai/planning/FUTURE_ENHANCEMENTS.md) | When proposing enhancements |

**Documentation Workflow:**
1. Check if change fits into one of these 9 living documents
2. If YES → **APPEND** to that document (do NOT create new file)
3. If NO → Check [Documentation Guidelines](../../../ai/standards/DOCUMENTATION_STANDARD.md)
4. **NEVER create documentation files without checking guidelines first**

## Working Directory

**Architect Workspace:** `.claude/skills/architect/`

**Bundled Resources:**
- `references/` - 11 technical reference documents (module structure, 4-case logic, external data, testing, troubleshooting, core principles)
- `assets/examples/` - 4 implementation guides (new model, new feature, external data, aggregation level)

**Technical Documents (Create Here):**
- `/ai/architect/` - Architecture proposals, spike results, design documents
- Use descriptive names: `integration_analysis.md`, `feature_implementation_guide.md`

**Context Folders (Reference as Needed):**
- `/ai/backend/` - Django backend context
- `/ai/frontend/` - React frontend context
- `/ai/specs/` - Technical specifications (context, edge cases, feature store, model specs)

## When Suggesting Changes

Always explain:
- **Why** - Maintains architectural integrity
- **Which modules** - Affected components
- **How** - Fits into data flow
- **Where** - Data persistence location
- **What testing** - Required in `/test` folder
- **How repeatable** - Test idempotency strategy

**For every change:**
1. Identify implementation files
2. Create corresponding test in `/test` folder
3. Ensure tests are repeatable and self-contained
4. Use sample data from `data/tests/` when needed
5. Document test execution in code comments
6. **Append to Test Manifest** when adding tests

**Think like an architect:** Prioritize maintainability, testability, and adherence to established patterns.

## Version History

**v2.1.0** (2025-10-30)
- Refactored to use progressive disclosure pattern
- Extracted detailed content to `references/` (11 files) and `assets/examples/` (4 files)
- Converted to imperative form (removed second-person voice)
- Reduced from 576 lines to ~295 lines
- Enhanced with v2.1 utils package details (7 utility modules)
- Added clear workflow sections with examples

**v2.0.0** (2025-10-28)
- Updated for v2.1 architecture (34 modules, 6 packages)
- Added comprehensive testing guidelines
- Enhanced external data integration documentation

---

**Last Updated:** 2025-10-30
**Architecture Version:** v2.1 (34 modules in 6 packages)
**Test Coverage:** 197 tests, 85% coverage
**Core Innovation:** 4-case logic engine (filters can use attributes as inputs)
