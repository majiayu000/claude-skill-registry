---
name: create-config
description: Creates timestamped configuration files for sports poetry multi-agent workflows. Invoked when users request to 'create config', 'set up configuration', 'configure sports poetry', provide sports lists for generation, or need help understanding configuration options. Validates sports count (3-5), checks API keys for LLM mode, and generates both JSON config and reproducible generator script (project)
---

Create timestamped configuration files for the sports poetry multi-agent workflow using interactive conversation and pre-built utility functions.

## Table of Contents

- [When to Use This Skill](#when-to-use-this-skill)
- [Quick Start Example](#quick-start-example)
- [Available Utilities](#available-utilities)
- [Conversation Flow](#conversation-flow)
- [CRITICAL: Always Create Both Files](#critical-always-create-both-files)
- [Common Usage Patterns](#common-usage-patterns)
- [Validation & Error Handling](#validation--error-handling)
- [Troubleshooting](#troubleshooting)
- [Configuration Parameters Reference](#configuration-parameters-reference)
- [File Structure](#file-structure)
- [Testing](#testing)
- [See Also](#see-also)
- [Dependencies](#dependencies)

## When to Use This Skill

Use this skill when the user:
- Asks to "create a config" or "set up configuration"
- Wants to configure sports poetry generation
- Provides a list of sports and generation preferences
- Needs help understanding configuration options

## Quick Start Example

```
User: "Create a config for basketball, soccer, and tennis"

You: I'll create a configuration for you.
     [Use skill_helpers.py utilities to create both files]

     ✓ Created output/configs/config_20251115_120000.json
     ✓ Created output/configs/generate_config_20251115_120000.py

     Ready to run: python3 orchestrator.py --config output/configs/config_20251115_120000.json
```

## Available Utilities

This skill uses pre-built functions from `skill_helpers.py`. Import and USE these directly rather than reimplementing:

```python
from skill_helpers import (
    check_api_key,           # Check env vars + .claude/claude.local.md
    create_generator_script, # Generate executable Python script
    get_setup_instructions   # Get API key setup help
)
```

**Key principle:** Use these utilities to save tokens and ensure consistency. Don't reimplement their logic.

## Conversation Flow

### High-Level Steps

1. **Collect sports** (3-5 required)
   - Validate count using `config_builder.with_sports()`
   - Normalize to lowercase, check for duplicates
   - config_builder handles validation automatically

2. **Ask for generation mode** (template or llm)
   - Default: `template` (fast, no API key needed)
   - If user wants LLM: proceed to step 3
   - If template mode: skip to step 5

3. **Check API key** (LLM mode only)
   - Use `check_api_key(provider)` from skill_helpers
   - If found: proceed to step 4
   - If not found: use `get_setup_instructions(provider)` and offer to switch to template mode

4. **Confirm LLM settings** (LLM mode only)
   - Provider: "together" or "huggingface" (default: together)
   - Model: Use provider-specific defaults unless user specifies
   - Together.ai default: `meta-llama/Llama-3.3-70B-Instruct-Turbo-Free`
   - HuggingFace default: `meta-llama/Meta-Llama-3-8B-Instruct`

5. **Ask about retry behavior** (optional)
   - Default: `true` (recommended)
   - Accept: yes/no, true/false, enable/disable

6. **Show configuration summary**
   - Display all settings before creating files
   - Ask for confirmation: "Proceed? [yes/no]"

7. **Create BOTH files** (CRITICAL - see below)
   - Config JSON: `output/configs/config_{timestamp}.json`
   - Generator script: `output/configs/generate_config_{timestamp}.py`
   - Make generator script executable: `chmod +x`

## CRITICAL: Always Create Both Files

Every successful skill execution MUST create TWO files:

**File 1: Configuration JSON**
```
output/configs/config_{timestamp}.json
```
Created by: `config_builder.save(config_path)`

**File 2: Generator Script**
```
output/configs/generate_config_{timestamp}.py
```
Created by: `create_generator_script()` from skill_helpers
Made executable with: `chmod +x`

**Failure to create BOTH files is incomplete execution of this skill.**

The generator script provides:
- Reproducibility (re-run to create same config with new timestamp)
- Auditability (shows exactly how config was created)
- Self-documentation (includes all parameters in header)

## Common Usage Pattern

This example shows both template mode (fast, no API key) and LLM mode (requires API key):

```python
from skill_helpers import check_api_key, get_setup_instructions, create_generator_script
from config_builder import ConfigBuilder
from pathlib import Path
from datetime import datetime
import os, stat

# Configuration
sports_list = ["basketball", "soccer", "tennis"]
use_llm_mode = False  # Set to True for LLM-generated poems
provider = "together"
model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

# Initialize builder
builder = ConfigBuilder.load_default()
builder.with_sports(sports_list)

# Configure mode-specific settings
if use_llm_mode:
    # Check for API key
    api_key = check_api_key(provider)
    if not api_key:
        print(get_setup_instructions(provider))
        print("\nFalling back to template mode...")
        use_llm_mode = False
    else:
        builder.with_generation_mode("llm")
        builder.with_llm_provider(provider)
        builder.with_llm_model(model)

# Create timestamped config file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
config_path = Path(f"output/configs/config_{timestamp}.json")
config_path.parent.mkdir(parents=True, exist_ok=True)
builder.save(str(config_path))

# Create generator script (required for reproducibility)
mode = "llm" if use_llm_mode else "template"
script = create_generator_script(
    sports=sports_list,
    mode=mode,
    provider=provider,
    model=model,
    retry=True,
    timestamp=timestamp
)

script_path = Path(f"output/configs/generate_config_{timestamp}.py")
script_path.write_text(script)
os.chmod(script_path, os.stat(script_path).st_mode | stat.S_IEXEC)

print(f"✓ Created {config_path}")
print(f"✓ Created {script_path}")
print(f"\nNext: python3 orchestrator.py --config {config_path}")
```

## Validation & Error Handling

**config_builder.py handles all validation automatically:**

- Sports count (3-5): Error raised immediately in `with_sports()`
- Duplicates: Detected and rejected
- Empty strings: Not allowed
- Generation mode: Must be "template" or "llm"
- LLM settings: Required if mode="llm"

**You don't need to duplicate validation logic.** Just call the builder methods and let them validate.

**Error message example:**
```
ConfigValidationError: Must specify at least 3 sports (got 2)
```

These messages are already helpful - just pass them to the user.

## Troubleshooting

### Sports Count Validation Error

When config_builder raises a sports count error, provide friendly suggestions:
```
You provided 2 sports, but we need 3-5.
Suggestions: tennis, volleyball, baseball, hockey, swimming
```

### API Key Issues

For LLM mode API key problems, use `check_api_key(provider)` and `get_setup_instructions(provider)` from skill_helpers (see Pattern 2 example), or offer to switch to template mode.

## Configuration Parameters Reference

### Required
- **sports** (list, 3-5 items): Sport names for poem generation
- **generation_mode** (string): "template" or "llm"

### Conditional (LLM mode only)
- **llm.provider** (string): "together" or "huggingface"
- **llm.model** (string): Model identifier

### Optional
- **retry_enabled** (boolean, default: true): Retry failed agents

### Auto-Generated (by orchestrator at runtime)
- **session_id**: Unique session identifier
- **timestamp**: ISO 8601 timestamp

## File Structure

```
.claude/skills/create_config/
├── SKILL.md                    # This file
└── skill_helpers.py            # Pre-built utility functions
```

## Testing

After using this skill, verify:

✅ Both files exist:
   - `output/configs/config_{timestamp}.json`
   - `output/configs/generate_config_{timestamp}.py`

✅ Config is valid JSON with required fields

✅ Generator script is executable:
   ```bash
   ls -l output/configs/generate_config_*.py
   # Should show -rwxr-xr-x (executable)
   ```

✅ Generator script can be run:
   ```bash
   ./output/configs/generate_config_{timestamp}.py
   # Should create new config with new timestamp
   ```

### Multi-Model Validation

This skill has been validated across all Claude models:
- **Claude Opus**: Full testing with complex configurations
- **Claude Sonnet**: Primary development and testing model
- **Claude Haiku**: Lightweight execution validation

All models successfully execute the skill with consistent behavior across template and LLM modes.

## See Also

- **skill_helpers.py** - Utility functions (check API keys, create scripts, etc.)
- **tests/test_create_config_skill.py** - Evaluation tests and acceptance criteria
- **config_builder.py** - Python API for config creation and validation
- **config.default.json** - Default configuration template
- **README.md** - Project overview and quick start guide

## Dependencies

- `config_builder.py` - Configuration builder with validation
- `skill_helpers.py` - Utility functions for this skill
- Python 3.7+ - For f-strings and pathlib
