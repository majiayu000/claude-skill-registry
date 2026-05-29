---
name: validation-history-integration
description: Auto-store validation results using store_validation_result() integration utility
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T22:58:59.652Z"
  updated_at: "2026-01-29T22:58:59.652Z"
  version: "1"
  tags: "validation,history,integration"
  compatibility: "2.1.0+"
  difficulty: "intermediate"
---
<!-- BEGIN:compound:skill-managed -->
# Validation History Integration
This skill provides guidance on automatically storing validation results in history.

## When To Use
- User asks about auto-storing validation results
- Implementing validation framework with history persistence
- Need to integrate ValidationSuite with ValidationHistoryStore

## Procedure
1. Import from vibe_piper.validation.integration: `store_validation_result`
2. Create ValidationHistoryStore (PostgreSQLValidationHistoryStore)
3. Call `store.initialize_schema()` before first use
4. Run validation suite on data
5. Call `store_validation_result()` with:
   - SuiteValidationResult from suite.validate()
   - Asset name (string)
   - History store instance
   - Optional pipeline_id for tracking
6. Returns validation_run_id for querying history later

## Example
```python
from vibe_piper.validation import ValidationSuite, expect_column_values_to_be_unique
from vibe_piper.validation.integration import store_validation_result
from vibe_piper.connectors.postgres import PostgreSQLConnector, PostgreSQLConfig

suite = ValidationSuite(name='data_quality')
suite.add_check('unique_ids', expect_column_values_to_be_unique('user_id'))

config = PostgreSQLConfig(host='localhost', port=5432, database='vp', user='u', password='p')
connector = PostgreSQLConnector(config)
connector.connect()

store = PostgreSQLValidationHistoryStore(connector)
store.initialize_schema()

result = suite.validate(data)
run_id = store_validation_result(result, asset_name='users', history_store=store, pipeline_id='daily')
print(f'Stored as: {run_id}')
```

## Integration Points
- Works with existing ValidationSuite API
- Works with all validation check functions
- Integrates with asset metadata (pipeline_id, suite_name)
- Stores comprehensive metrics for trend analysis

## Notes
- Requires PostgreSQL database initialized with validation history schema
- Call `store.initialize_schema()` before first use
- Metrics are automatically extracted: pass_rate, duration_ms, total_records
- Validation run ID can be used for tracking and querying history
- See src/vibe_piper/validation/history.py for full API
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
