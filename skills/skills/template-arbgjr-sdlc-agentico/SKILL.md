---
name: skill-name
description: |
  What this skill does AND when to use it.
  Include key terms that help Claude discover this skill (e.g., "PDF processing", "database queries", "system design").
  Use third person: "Processes X and generates Y" (NOT "I can help you...").
allowed-tools:
  - Read
  - Bash
  # Add other tools ONLY if truly necessary
user-invocable: true  # false if only called by other agents
version: "1.0.0"
---

# Skill Name

> **Philosophy**: Default to natural language. Use scripts ONLY for deterministic operations, complex I/O, or external API integration.

## Quick Start

[Concise example showing the most common use case - assume Claude is smart]

**Example**:
```bash
# Process document
python3 scripts/process.py input.pdf --output result.txt
```

## When to Use This Skill

Use this skill when:
- [Specific scenario 1]
- [Specific scenario 2]
- [Keyword trigger mentioned by user]

DO NOT use when:
- [Alternative approach is better]

## Core Workflows

### Workflow 1: [Name]

**Use when**: [Specific trigger or scenario]

**Steps**:
1. [Natural language instruction - be specific]
2. [Conditional logic: If X, then Y; else Z]
3. [Verification step]

**Example**:
```markdown
1. Check if document exists: `ls docs/*.pdf`
2. If PDF found: Extract text using `scripts/extract.py`
3. If no PDF: Search for DOCX alternatives
4. Validate output has non-zero size
```

**Common Issues**:
- **Problem**: [What goes wrong]
- **Solution**: [How to fix it]

---

### Workflow 2: [Name]

[Follow same pattern as Workflow 1]

---

## Reference Documentation

For detailed information, see:
- [Topic A Details](reference/topic-a.md) - When working with X
- [Topic B Details](reference/topic-b.md) - For advanced Y usage
- [API Reference](reference/api.md) - All available functions

> **Note**: Claude loads these files ONLY when needed (progressive disclosure).

---

## Scripts (ONLY when justified)

### script-name.py

**Why this script is needed**: [ONE of these justifications]:
- ✅ Deterministic validation (e.g., schema validation, syntax checking)
- ✅ External API integration (e.g., GitHub API, third-party service)
- ✅ Complex I/O operation (e.g., scanning thousands of files, binary parsing)
- ✅ Safety-critical operation (e.g., git worktree, database migrations)
- ❌ **NOT for**: Pattern matching, text analysis, conditional logic (Claude is better)

**Usage**:
```bash
python3 scripts/script-name.py --arg value
```

**Arguments**:
- `--arg`: Description

**Output**:
```
Expected output format
```

**Error Handling**:
Script handles these errors explicitly (doesn't punt to Claude):
- Missing input file → Creates default
- Permission denied → Uses alternative path
- Network timeout → Retries with backoff

---

### validation-script.sh

**Why needed**: [Justification - e.g., "Bash validation faster than Python for simple checks"]

**Usage**:
```bash
./scripts/validation-script.sh file.txt
```

**Returns**:
- Exit code 0: Valid
- Exit code 1: Invalid (with error message)

---

## Testing

### Run Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Specific test
pytest tests/test_specific.py::test_function -v
```

### Test Coverage

Current coverage: XX%

```bash
pytest --cov=scripts --cov-report=html
open htmlcov/index.html
```

---

## Examples

### Example 1: [Common Use Case]

**Scenario**: [Describe the situation]

**Input**:
```
[What user provides]
```

**Process**:
```markdown
1. Claude reads input
2. Validates format
3. Calls script if needed: `python3 scripts/process.py`
4. Formats output
```

**Output**:
```
[What user gets]
```

---

### Example 2: [Edge Case]

[Same structure as Example 1]

---

## Integration

### With Other Skills

This skill integrates with:
- **skill-a**: Use after this skill for [purpose]
- **skill-b**: Call this skill if [condition]

### With Agents

Agents that use this skill:
- **agent-x** (Phase Y): Uses for [specific task]
- **agent-z** (Phase W): Calls during [workflow step]

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VAR_NAME` | No | `default` | What this controls |

### Settings File

Create `~/.config/skill-name/settings.yml`:

```yaml
option1: value1
option2: value2
```

---

## Troubleshooting

### Common Issues

**Issue**: Script fails with "Module not found"

**Solution**:
```bash
pip install required-package
```

---

**Issue**: Permission denied

**Solution**:
```bash
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

---

**Issue**: Output is empty

**Solution**:
Check input file format. Expected: [format description]

---

## Development

### Adding New Features

1. Create feature branch
2. Add tests FIRST (TDD)
3. Implement in natural language if possible
4. Add script ONLY if justified
5. Update SKILL.md
6. Run tests: `pytest -v`

### Code Style

- **Natural language**: Clear, concise, assume Claude is smart
- **Python**: PEP 8, type hints, docstrings
- **Bash**: ShellCheck compliant

---

## Changelog

### v1.0.0 (YYYY-MM-DD)
- Initial release
- Core workflows implemented
- [Feature X] added

---

## References

- [External Documentation](https://example.com)
- [Related Pattern](../../corpus/nodes/patterns/PATTERN-*.yml)
- [ADR](../../corpus/nodes/decisions/ADR-*.yml)

---

## Anti-Patterns to Avoid

❌ **DON'T**:
- Create scripts for pattern matching (Claude is better)
- Write Python for simple Bash operations
- Add dependencies without justification
- Create "utils" or "helpers" (be specific)

✅ **DO**:
- Default to natural language instructions
- Use progressive disclosure for > 500 lines
- Document why each script is needed
- Test with Claude before assuming script is needed

---

**Skill maintained by**: [Team/Person]
**Last updated**: YYYY-MM-DD
**Questions**: Contact [channel/person]
