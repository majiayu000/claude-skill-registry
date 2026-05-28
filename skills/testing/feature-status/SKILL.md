---
name: feature-status
description: Count features marked as @failing and write to status JSON file. Used to determine when the autonomous coding loop should end.
allowed-tools: Glob, Read, Write
---

# Feature Status Skill

## Purpose

This skill counts the number of features marked as `@failing` and writes the count to a JSON file. This is used by the autonomous coding harness to determine when the implementation loop should end (when `failing_count` reaches 0).

## Output File

**File**: `feature-status.json`

**Format**:
```json
{
  "failing_count": 3
}
```

**Loop Termination Logic**:
- If `failing_count > 0` → Continue coding sessions
- If `failing_count == 0` → All features implemented, end loop

## How It Works

### Step 1: Find Feature Files

Use Glob to find all Gherkin feature files:
```
Pattern: gherkin.feature_*.feature
```

### Step 2: Count @failing Tags

For each feature file:
1. Read the first few lines
2. Look for `@failing` tag
3. If found, increment the failing counter

**Tag Detection**:
```
@failing
Feature: Some Feature Name
  ...
```

Read lines until you find either:
- `@failing` → Count this feature as failing
- `@passing` → Skip (not failing)
- `Feature:` line → Stop searching (assume no tag = passing)

### Step 3: Write JSON

Write `feature-status.json` with just the failing count:
```json
{
  "failing_count": <count>
}
```

## Usage

Simply invoke the skill:
```
/feature-status
```

This will:
1. Scan all `gherkin.feature_*.feature` files in the current directory
2. Count how many have `@failing` tags
3. Write the count to `feature-status.json`

## Example Implementation

```python
# Pseudocode for reference
def count_failing_features(directory):
    failing_count = 0

    # Find all feature files
    feature_files = glob("gherkin.feature_*.feature")

    for file in feature_files:
        with open(file) as f:
            for line in f:
                line = line.strip()

                if line.startswith("@failing"):
                    failing_count += 1
                    break
                elif line.startswith("@passing"):
                    break
                elif line.startswith("Feature:"):
                    # No tag found, assume passing
                    break

    return failing_count
```

## Integration with Autonomous Coding Harness

The harness can check the status file to decide whether to continue:

```python
import json

def should_continue_loop():
    with open("feature-status.json") as f:
        status = json.load(f)
    return status["failing_count"] > 0
```

## Best Practices

1. **Run after each coding session** to update the failing count
2. **Commit the status file** to track progress over time
3. **Check before starting a new session** to avoid unnecessary runs
4. **Use as a termination condition** in automation scripts
