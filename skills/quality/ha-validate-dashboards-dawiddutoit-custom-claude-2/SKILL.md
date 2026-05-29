---
name: ha-validate-dashboards
description: |
  Provides 3-tier validation approach for Home Assistant dashboards including pre-publish
  validation (entity checks, config structure), post-publish verification (log analysis),
  and visual validation (browser console, rendering). Use when validating HA dashboards,
  checking dashboard configs, verifying entity IDs, debugging rendering issues, or before
  deploying dashboard changes. Triggers on "validate dashboard", "check HA config", "dashboard
  errors", "entity not found", or "test dashboard". Works with Home Assistant WebSocket/REST APIs,
  Chrome extension MCP tools, Python dashboard builders, and YAML dashboard configurations.
---
# Home Assistant Dashboard Validation

Validates Home Assistant dashboard and configuration changes using a comprehensive 3-tier validation approach to catch errors before they impact users.

## Quick Start

Run a complete validation before deploying a dashboard:

```bash
# 1. Validate config structure and entities (pre-publish)
python3 << 'EOF'
import json
with open('climate_dashboard.json') as f:
    config = json.load(f)

from validation_helpers import validate_dashboard_config, verify_entities_exist, extract_all_entity_ids

is_valid, errors = validate_dashboard_config(config)
if not is_valid:
    print("Config errors:", errors)
    exit(1)

entities = extract_all_entity_ids(config)
existence = verify_entities_exist(entities)
missing = [e for e, exists in existence.items() if not exists]
if missing:
    print("Missing entities:", missing)
    exit(1)
print("✅ Pre-publish validation passed")
EOF

# 2. Publish dashboard
./run.sh dashboard_builder.py

# 3. Check HA logs (post-publish)
curl -s "http://192.168.68.123:8123/api/error_log" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | \
  grep -i "lovelace" | tail -5

# 4. Visual validation (browser)
mcp-cli call claude-in-chrome/navigate '{"url": "http://192.168.68.123:8123/climate-dashboard"}'
sleep 2
mcp-cli call claude-in-chrome/read_console_messages '{}'
```

## Table of Contents

1. When to Use This Skill
2. The 3-Tier Validation Approach
3. Validation Workflows
4. Common Failure Modes
5. Supporting Files
6. Integration with Project
7. Requirements
8. Red Flags to Avoid

## When to Use This Skill

**Explicit Triggers:**
- "validate my dashboard"
- "check HA dashboard config"
- "verify dashboard entities"
- "validate before publish"

**Implicit Triggers:**
- Before deploying dashboard changes
- After modifying dashboard builder scripts
- Before committing dashboard code changes

**Debugging Triggers:**
- Dashboard shows "Entity not available"
- Cards fail to render or show error states
- Console shows JavaScript errors
- HACS card doesn't appear after installation

## Usage

Use this skill to validate Home Assistant dashboards before deployment. Run the Quick Start workflow for a complete validation, or use individual tiers (pre-publish, post-publish, visual) for specific validation needs. Always run pre-publish validation first to catch config errors before they reach production.

## The 3-Tier Validation Approach

### Tier 1: Pre-Publish Validation (API-Based)

Validate configuration and entities BEFORE publishing to Home Assistant.

**Config Structure Validation:**

```python
def validate_dashboard_config(config: dict) -> tuple[bool, list[str]]:
    """Validate dashboard configuration structure."""
    errors = []

    if "views" not in config:
        errors.append("Missing required 'views' key")
        return False, errors

    if not isinstance(config["views"], list):
        errors.append("'views' must be a list")
        return False, errors

    for idx, view in enumerate(config["views"]):
        if "title" not in view:
            errors.append(f"View {idx}: Missing required 'title'")
        if "cards" in view and not isinstance(view["cards"], list):
            errors.append(f"View {idx}: 'cards' must be a list")

    return len(errors) == 0, errors
```

**Entity Existence Check:**

```python
def verify_entities_exist(entity_ids: list[str]) -> dict[str, bool]:
    """Check if entities exist via REST API."""
    url = "http://192.168.68.123:8123/api/states"
    headers = {"Authorization": f"Bearer {os.environ['HA_LONG_LIVED_TOKEN']}"}

    response = requests.get(url, headers=headers, timeout=10)
    existing_entities = {state["entity_id"] for state in response.json()}

    return {
        entity_id: entity_id in existing_entities
        for entity_id in entity_ids
    }
```

**Extract All Entity IDs:**

```python
def extract_all_entity_ids(config: dict) -> list[str]:
    """Recursively extract all entity IDs from dashboard config."""
    entity_ids = []

    def extract_from_dict(d):
        if isinstance(d, dict):
            if "entity" in d and isinstance(d["entity"], str):
                entity_ids.append(d["entity"])
            if "entities" in d and isinstance(d["entities"], list):
                for item in d["entities"]:
                    if isinstance(item, str):
                        entity_ids.append(item)
                    elif isinstance(item, dict) and "entity" in item:
                        entity_ids.append(item["entity"])
            for value in d.values():
                if isinstance(value, (dict, list)):
                    extract_from_dict(value)
        elif isinstance(d, list):
            for item in d:
                extract_from_dict(item)

    extract_from_dict(config)
    return list(set(entity_ids))
```

**Why Pre-Publish Validation Matters:**
- Catches config errors before they reach HA
- Prevents "Entity not available" errors in production
- Verifies HACS cards are installed
- Fast feedback loop (API calls only)

### Tier 2: Post-Publish Verification (Log Analysis)

Monitor Home Assistant logs for errors after publishing dashboard changes.

**Log Comparison Workflow:**

```bash
# 1. Capture baseline errors before change
curl -s "http://192.168.68.123:8123/api/error_log" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" > pre-change-errors.log

# 2. Make dashboard changes via WebSocket/API

# 3. Wait for errors to propagate
sleep 5

# 4. Capture post-change errors
curl -s "http://192.168.68.123:8123/api/error_log" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" > post-change-errors.log

# 5. Compare for new errors
diff pre-change-errors.log post-change-errors.log
```

**Key Error Patterns:**

| Error Pattern | Meaning | Fix |
|---------------|---------|-----|
| `Custom element doesn't exist: custom:*-card` | HACS card not installed/loaded | Install via HACS, clear cache |
| `Entity not available: sensor.*` | Entity doesn't exist or offline | Check entity ID, verify device |
| `Error while loading page lovelace` | Dashboard config syntax error | Check config structure |
| `Invalid configuration for card` | Card validation failed | Review card schema |

**Why Log Analysis Matters:**
- Detects runtime errors that pre-publish checks miss
- Catches integration-specific issues
- Provides detailed error messages for debugging
- Confirms changes didn't break existing functionality

### Tier 3: Visual Validation (Browser Automation)

Use Chrome extension MCP tools to verify rendering and check browser console.

**Browser Validation Workflow:**

```bash
# 1. Navigate to dashboard
mcp-cli call claude-in-chrome/navigate '{
  "url": "http://192.168.68.123:8123/climate-dashboard"
}'

# 2. Wait for page load
sleep 2

# 3. Check console for JavaScript errors
mcp-cli call claude-in-chrome/read_console_messages '{}'

# 4. Take screenshot for visual verification
mcp-cli call claude-in-chrome/computer '{
  "action": "screenshot"
}'

# 5. Read page content to verify cards rendered
mcp-cli call claude-in-chrome/read_page '{}'
```

**Console Error Interpretation:**

| Console Error | Root Cause | Fix |
|---------------|------------|-----|
| `Custom element doesn't exist: custom:*` | HACS card not loaded | Hard refresh (Ctrl+Shift+R) |
| `Uncaught TypeError: Cannot read property 'state'` | Entity ID mismatch | Check entity via API |
| `Failed to fetch` | Network/API connectivity | Check HA availability |
| `SyntaxError: Unexpected token` | JSON config syntax error | Validate JSON structure |

**When to Use Visual Testing:**

Always use for:
- Major dashboard restructuring
- New custom cards from HACS
- card_mod CSS customizations
- After updating HACS cards

Skip for:
- Simple entity ID changes
- Backend configuration
- Non-frontend changes

**Why Visual Validation Matters:**
- Catches rendering issues that API checks miss
- Verifies card styling and layout
- Confirms HACS cards loaded correctly
- Provides visual proof of correctness

## Validation Workflows

### Quick Validation (Minor Changes)

Fast validation for simple entity ID updates:

```bash
#!/bin/bash
# quick_validate.sh

DASHBOARD="climate-dashboard"

# Rebuild dashboard
./run.sh dashboard_builder.py

# Check logs for errors
if curl -s "http://192.168.68.123:8123/api/error_log" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | \
  grep -i "error.*lovelace"; then
    echo "❌ Errors in logs"
    exit 1
fi

# Quick browser check
mcp-cli call claude-in-chrome/navigate "{\"url\": \"http://192.168.68.123:8123/$DASHBOARD\"}" > /dev/null
sleep 2
mcp-cli call claude-in-chrome/read_console_messages '{}' | grep -q '"level": "error"'

if [ $? -eq 0 ]; then
    echo "❌ Console errors detected"
    exit 1
fi

echo "✅ Quick validation passed"
```

### Full Validation (Major Changes)

Comprehensive validation for major dashboard updates. See `references/workflows.md` for the complete full validation script (full_validate.sh).

Key steps:
1. Pre-publish validation (config + entities)
2. Publish to production
3. Check HA logs for new errors
4. Automated browser validation
5. Take screenshot for visual confirmation

### Incremental Testing

Build complex dashboards section by section with validation:

```python
def build_dashboard_incrementally():
    """Build dashboard section by section with validation."""
    cards = []

    # Section 1: Temperature
    temp_cards = create_temperature_section()
    test_partial_dashboard("test-temp", temp_cards)
    cards.extend(temp_cards)

    # Section 2: Humidity
    humidity_cards = create_humidity_section()
    test_partial_dashboard("test-humidity", cards + humidity_cards)
    cards.extend(humidity_cards)

    # Final publish
    publish_dashboard("climate-dashboard", {
        "views": [{"title": "Climate", "cards": cards}]
    })
```

## Common Failure Modes

### Configuration Errors

| Failure Mode | Detection | Fix |
|--------------|-----------|-----|
| Missing entity ID | API entity check | Fix entity ID typo |
| Invalid card type | Console error | Check spelling, verify HACS |
| Malformed JSON | WebSocket error | Validate JSON syntax |
| Missing required field | Pre-publish validation | Add required field |

### HACS Card Issues

| Failure Mode | Detection | Fix |
|--------------|-----------|-----|
| Card not installed | Console, HACS check | Install via HACS |
| Card not loaded | Console, network tab | Hard refresh |
| Version incompatibility | Check versions | Update card or HA |

### Entity Issues

| Failure Mode | Detection | Fix |
|--------------|-----------|-----|
| Entity unavailable | API state check | Check device connection |
| Entity renamed | API 404 | Update entity ID |
| Entity removed | Pre-publish check | Remove/update card |

## Supporting Files

### references/validation-reference.md

Comprehensive reference documentation including:
- REST API endpoint reference (full request/response examples)
- WebSocket API command reference (auth flow, dashboard operations)
- MCP Chrome extension tool details (all available tools)
- Complete validation function implementations
- Entity state validation patterns
- Log analysis techniques and Python helpers

**When to read:** Need API details, complete code examples, or advanced validation patterns.

### references/workflows.md

Detailed workflow documentation including:
- Pre-commit validation checklist
- Rollback strategy and procedures (backup/restore)
- Complete end-to-end deployment workflow
- CI/CD integration patterns (GitHub Actions, pre-commit hooks)
- Automated testing scripts (validate_all.py, check_entities.py)

**When to read:** Setting up automation, implementing CI/CD, or need complete deployment scripts.

## Integration with Project

This skill integrates with the Home Assistant dashboard management workflow:

**Integration Points:**

1. **Dashboard Builder Scripts** (`dashboard_builder.py`)
   - Add validation calls before publishing
   - Use `publish_dashboard_safely()` wrapper

2. **Card Utilities** (`ha_card_utils.py`)
   - Validation helpers can be added here
   - Keep utilities project-specific

3. **Chrome Extension** (MCP tools)
   - Use for visual validation
   - Check console errors, take screenshots

4. **CLAUDE.md Documentation**
   - Update validation checklist
   - Document validation commands

**Example Integration:**

```python
# In dashboard_builder.py
from validation_helpers import validate_dashboard_config, verify_entities_exist

def build_climate_dashboard():
    """Build climate dashboard with validation."""
    cards = create_climate_cards()
    config = {"views": [{"title": "Climate", "cards": cards}]}

    # Validate before publish
    is_valid, errors = validate_dashboard_config(config)
    if not is_valid:
        print("❌ Validation failed:", errors)
        return False

    # Verify entities
    entities = extract_all_entity_ids(config)
    existence = verify_entities_exist(entities)
    missing = [e for e, exists in existence.items() if not exists]

    if missing:
        print("❌ Missing entities:", missing)
        return False

    # Safe publish
    success, msg = publish_dashboard_safely("climate-dashboard", config)
    return success
```

## Requirements

### Environment

- Home Assistant 2025.12.3+ (WebSocket/REST API)
- Python 3.11+ (validation scripts)
- Chrome browser with Claude extension (visual testing)
- MCP CLI installed and configured

### Dependencies

```bash
pip install requests websocket-client
export HA_LONG_LIVED_TOKEN="your-token"
```

### Knowledge Required

- Basic Python programming
- Home Assistant entity ID format
- Dashboard config structure (views, cards)
- curl and bash scripting basics

## Red Flags to Avoid

- [ ] Skipping pre-publish validation - Always validate BEFORE deploying
- [ ] Ignoring entity existence checks - Missing entities cause runtime errors
- [ ] Not checking HACS cards - Custom cards must be installed first
- [ ] Skipping log analysis - New errors won't be detected
- [ ] Publishing without backup - Always save current config before changes
- [ ] Ignoring console errors - Browser console shows critical rendering issues
- [ ] Testing only in code - Visual validation catches real rendering problems
- [ ] Not using incremental testing - Build dashboards section by section
- [ ] Publishing to production first - Test on test-dashboard first
- [ ] Ignoring rollback strategy - Know how to revert if deployment fails

## Notes

- **Integration Priority**: Pre-publish validation is most critical - it prevents bad configs from reaching HA
- **Visual Testing Cost**: Browser automation is slower but catches rendering issues that API checks miss
- **Log Monitoring**: Post-publish log checks detect issues that only appear at runtime
- **Incremental Testing**: Build complex dashboards section by section to isolate issues quickly
- **Rollback Safety**: Always capture current config before making changes for easy rollback
