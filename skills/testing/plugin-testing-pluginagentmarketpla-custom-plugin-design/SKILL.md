---
name: plugin-testing
description: Master plugin testing, quality assurance, and validation. Learn unit testing, integration testing, and how to ensure plugin quality.
sasmp_version: "1.3.0"
bonded_agent: 04-plugin-tester
bond_type: PRIMARY_BOND
---

# Plugin Testing

## Quick Start

Test your plugin:

```bash
# Validate structure
/test-plugin my-plugin

# Run all tests
/test-plugin my-plugin --all

# Detailed report
/test-plugin my-plugin --report
```

## Testing Levels

### Unit Tests

Test individual components:

```markdown
Agent:
  ✅ Description present and valid
  ✅ Capabilities list complete
  ✅ Content properly formatted
  ✅ Status and date included

Skill:
  ✅ Name lowercase-hyphens
  ✅ Quick Start code runs
  ✅ 3+ concepts documented
  ✅ Real projects included

Command:
  ✅ Executes without error
  ✅ Options documented
  ✅ Example output provided
```

### Integration Tests

Test component interactions:

```markdown
Agent → Agent:
  ✅ Agent A links to Agent B
  ✅ Both agents available
  ✅ Integration documented

Agent → Skill:
  ✅ Agent recommends skill
  ✅ Skill accessible
  ✅ Connection clear

Command → Agent:
  ✅ Command invokes agent
  ✅ Agent responds appropriately
  ✅ Workflow makes sense
```

## Test Checklist

### Structure Tests

```json
{
  "manifest_valid": {
    "description": "plugin.json valid JSON",
    "check": "JSON.parse(plugin.json)"
  },
  "files_exist": {
    "description": "All referenced files exist",
    "check": "For each agent/skill/command file"
  },
  "naming_correct": {
    "description": "Files follow naming conventions",
    "check": "lowercase-hyphens pattern"
  },
  "references_valid": {
    "description": "All manifested references valid",
    "check": "Check each file path"
  }
}
```

### Content Tests

```markdown
Agent:
  ✅ YAML frontmatter valid
  ✅ Description < 1024 chars
  ✅ Capabilities 5-10 items
  ✅ Content 250-400 lines
  ✅ Markdown properly formatted

Skill:
  ✅ YAML frontmatter valid
  ✅ Name < 64 chars, lowercase
  ✅ Quick Start code works
  ✅ Core concepts explained
  ✅ Real projects included

Command:
  ✅ Markdown valid
  ✅ Usage clear
  ✅ Options documented
  ✅ Example provided
  ✅ Next steps suggested
```

### Functionality Tests

```markdown
Agent Invocation:
  ✅ Agent loads without error
  ✅ Content renders correctly
  ✅ Integrations accessible
  ✅ No broken links

Skill Loading:
  ✅ Skill accessible from agent
  ✅ Code examples accurate
  ✅ Links functional
  ✅ Metadata correct

Command Execution:
  ✅ Command recognized
  ✅ Options work as documented
  ✅ Output as expected
  ✅ Next steps provided
```

## Test Report Example

### Full Test Report

```markdown
PLUGIN TEST REPORT
═══════════════════════════════════════
Plugin: my-plugin
Version: 1.0.0
Date: 2025-01-18

STRUCTURE TESTS
  ✅ Manifest valid (5/5)
  ✅ Files exist (8/8)
  ✅ Naming correct (6/6)
  ├─ Result: PASS

CONTENT TESTS
  ✅ Agents valid (3/3)
  ✅ Skills valid (5/5)
  ✅ Commands valid (4/4)
  ├─ Result: PASS

FUNCTIONALITY TESTS
  ✅ Agents invoke (3/3)
  ✅ Skills load (5/5)
  ✅ Commands execute (4/4)
  ├─ Result: PASS

QUALITY SCORE: 98% ✅
READY FOR PRODUCTION: YES ✅
═══════════════════════════════════════
```

## Common Test Failures

### JSON Syntax Error

```
❌ Error in plugin.json line 15
  Missing comma after "name": "value"

Fix:
  "name": "value",  ← Add comma
  "version": "1.0.0"
```

### File Not Found

```
❌ Agent agents/missing.md referenced but not found

Fix:
  1. Create the file, OR
  2. Remove reference from plugin.json
```

### Invalid YAML

```
❌ Invalid YAML in agents/agent.md

Fix:
  - Check indentation (use spaces, not tabs)
  - Ensure quotes around values with special chars
  - Verify array syntax with dashes
```

### Content Too Short

```
⚠️  Warning: Skill content only 150 lines
   Recommended: 200-300 lines

Fix:
  - Add more examples
  - Expand core concepts
  - Include more projects
```

## Performance Testing

### Load Time Baseline

```
Agent initialization:   < 500ms ✅
Skill loading:         < 300ms ✅
Command execution:     < 2s   ✅
Overall workflow:      < 5s   ✅
```

### Size Limits

```
Agent files:    < 400 lines ✅
Skill files:    < 300 lines ✅
Command files:  < 150 lines ✅
Manifest:       < 50KB      ✅
```

## Automated Testing

### Test Command

```bash
# Quick test (5 min)
/test-plugin my-plugin

# Full test (10 min)
/test-plugin my-plugin --full

# Continuous monitoring
/test-plugin my-plugin --watch
```

### Test Categories

```
✅ Structure tests
✅ Content validation
✅ Format checking
✅ Reference validation
✅ Performance baseline
✅ Integration tests
```

## Pre-Deployment Testing

### Checklist

```markdown
[ ] All structure tests pass
[ ] All content validation passes
[ ] No broken references
[ ] Performance acceptable
[ ] Documentation complete
[ ] Examples working
[ ] Error messages helpful
[ ] Integration smooth
[ ] User acceptance tested
[ ] Ready for marketplace
```

### Release Testing

```
Before release:
  ✅ Version bumped
  ✅ CHANGELOG updated
  ✅ All tests passing
  ✅ Documentation updated
  ✅ Examples verified
  ✅ Performance baseline met
  ✅ Code reviewed
```

---

**Use this skill when:**
- Testing plugin components
- Validating structure
- Checking quality
- Before deployment
- Finding and fixing issues

---

**Status**: ✅ Production Ready | **SASMP**: v1.3.0 | **Bonded Agent**: 04-plugin-tester
