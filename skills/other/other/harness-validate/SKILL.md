---
name: harness-validate
description: Use when user invokes /harness-validate or wants to check whether a harness.yaml file is valid according to the Harness Protocol v1 JSON Schema. Reports validation errors with field paths and helpful fix suggestions.
disable-model-invocation: true
---

# Validate a Harness Configuration

You are helping the user validate a `harness.yaml` file against the Harness Protocol v1 JSON Schema.

## Workflow Order (MANDATORY)

**Follow these steps in order. Do not skip any step.**

---

### Step 1: Find the file

Check for the harness file in this order:
1. A path provided by the user after `/harness-validate` (e.g., `/harness-validate ~/dotfiles/harness.yaml`)
2. `./harness.yaml` in the current directory

If no file is found at either location, tell the user:
> "No `harness.yaml` found. Specify a path: `/harness-validate path/to/harness.yaml`"

Read the file contents.

---

### Step 2: Run validation

Install the validation tools if not present and run validation:

```bash
python3 -m venv /tmp/hk-validate-venv 2>/dev/null || true
/tmp/hk-validate-venv/bin/pip install jsonschema pyyaml -q 2>/dev/null || \
  (python3 -m venv /tmp/hk-validate-venv && /tmp/hk-validate-venv/bin/pip install jsonschema pyyaml -q)
```

Then run this validation script:

```python
import json, sys, yaml

try:
    from jsonschema import validate, ValidationError, SchemaError
    from jsonschema.validators import validator_for
except ImportError:
    print("ERROR: jsonschema not installed")
    sys.exit(1)

SCHEMA_URL = "https://raw.githubusercontent.com/harnessprotocol/harness-protocol/spec/v1-foundation/schema/draft/harness.schema.json"
HARNESS_FILE = "harness.yaml"  # replace with actual path

# Fetch the schema
import urllib.request
try:
    with urllib.request.urlopen(SCHEMA_URL, timeout=5) as resp:
        schema = json.loads(resp.read())
except Exception as e:
    print(f"WARN: Could not fetch remote schema ({e}). Falling back to basic checks.")
    schema = None

# Load the harness file
try:
    with open(HARNESS_FILE) as f:
        doc = yaml.safe_load(f)
except yaml.YAMLError as e:
    print(f"FAIL: YAML parse error — {e}")
    sys.exit(1)

if schema is None:
    # Basic offline checks
    errors = []
    if "version" not in doc:
        errors.append("Missing required field: version")
    elif doc["version"] not in ("1", 1):
        errors.append(f"version must be \"1\" (string) or 1 (legacy integer), got: {doc['version']!r}")
    if "metadata" not in doc:
        errors.append("Missing required field: metadata")
    elif "name" not in doc.get("metadata", {}):
        errors.append("metadata.name is required")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
    else:
        print("PASS (basic checks only — schema fetch failed)")
    sys.exit(0)

# Full schema validation
try:
    validate(instance=doc, schema=schema)
    print("PASS")
except ValidationError as e:
    path = " → ".join(str(p) for p in e.absolute_path) or "(root)"
    print(f"FAIL: {path}: {e.message}")
except SchemaError as e:
    print(f"ERROR: Schema itself is invalid — {e.message}")
```

Run the script with `/tmp/hk-validate-venv/bin/python3` and capture the output.

---

### Step 3: Report results

**On PASS:**
> "Your `harness.yaml` is valid — passes Harness Protocol v1 schema validation."

If the file uses `version: 1` (integer, legacy format), add:
> "Note: this is in the legacy format (`version: 1` integer). Run `/harness-export` to regenerate in Harness Protocol v1 format (`version: \"1\"` string)."

**On FAIL (validation errors):**

Display errors with clear field paths and fix suggestions:

```
✗ harness.yaml failed validation:

  plugins → 0 → source: 'marketplace' is not a valid property
    Fix: Use source: owner/repo instead of marketplace: key.
    Example: source: harnessprotocol/harness-kit

  env → 0: 'default' is not allowed when sensitive is true
    Fix: Remove the default value — sensitive vars must be set by the user,
    never baked into the harness file.

  (root): version must be "1" (string), got 1 (integer)
    Fix: Change version: 1 to version: "1" (add quotes).
```

**Common errors and their fixes:**

| Error | Fix |
|-------|-----|
| `version` must be string `"1"` | Change `version: 1` to `version: "1"` |
| `source` is not a valid property | Replace `marketplace: key` with `source: owner/repo` |
| `default` not allowed when `sensitive: true` | Remove the `default` value |
| `metadata.name` is required | Add a `metadata.name` field |
| Unknown additional property | Check for typos in field names |

After listing errors:
> "Fix these issues and run `/harness-validate` again to confirm."

**On YAML parse error:**
> "Your `harness.yaml` has a YAML syntax error:
> `[error details]`
>
> Common causes: wrong indentation, missing quotes around special characters (like `:` in strings), or a tab used instead of spaces."

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Reporting only the first error | Show all errors, not just the first one |
| Giving up if schema fetch fails | Fall back to basic checks and tell the user the schema was unavailable |
| Suggesting `marketplace:` as a fix | Always recommend `source: owner/repo` — that's the v1 format |
