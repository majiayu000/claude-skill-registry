---
name: schema-validate-resume
description: Validate resume payloads using strict Pydantic models. Ensures that the resume JSON conforms to the required structure before processing.
---

# Schema Validate Resume

## Overview

This skill enforces strict type checking on resume data using Pydantic. It verifies that required fields exist and types are correct.

## Prerequisites

*   `pydantic` library (`pip install pydantic`).

## Usage

### Validate Script

**Syntax:**

```bash
python3 .agent/skills/schema-validate-resume/scripts/validate.py <resume.json>
```

**Output:**
Exit code 0 if valid, 1 if invalid (with error message).

**Example:**

```bash
if python3 .agent/skills/schema-validate-resume/scripts/validate.py resume.json; then
    echo "Valid"
else
    echo "Invalid"
fi
```
