---
name: validation-engine
description: Validate plugin integrity and offer safe auto-fixes for common issues - checks agents, skills, hooks, routing config, and plugin structure
---

# Validation Engine

Comprehensive plugin integrity validation with safe automatic fixes for common issues.

## When to Use

- User runs `/popkit:plugin sync`
- Pre-release validation
- After adding new agents/skills
- Debugging plugin structure issues
- Automated CI/CD checks

## Arguments

| Argument             | Description                          |
| -------------------- | ------------------------------------ |
| (none)               | Run validation checks only (default) |
| `apply`              | Apply safe auto-fixes                |
| `--component=<name>` | Validate specific component only     |
| `--json`             | Output results as JSON               |
| `--verbose`          | Show detailed validation output      |

## Process

### Step 1: Run Validation Checks

```python
import os
from pathlib import Path
from popkit_shared.utils.plugin_validator import validate_plugin_structure
from popkit_shared.utils.skill_validator import (
    validate_all_skills,
    check_skill_naming_consistency,
    find_duplicate_skill_names
)
from popkit_shared.utils.agent_router_test import (
    test_agent_definitions_exist,
    get_routing_statistics
)

# Get plugin root
plugin_root = Path(os.environ.get('CLAUDE_PLUGIN_ROOT', '.'))

# Validate overall structure
print("Validating plugin structure...")
structure_result = validate_plugin_structure(plugin_root)

# Validate skills
print("Validating skills...")
skill_files = list((plugin_root / "skills").glob("*/SKILL.md"))
skill_results = validate_all_skills(skill_files)
skill_naming = check_skill_naming_consistency(plugin_root / "skills")
duplicate_skills = find_duplicate_skill_names(plugin_root / "skills")

# Validate agents
print("Validating agents...")
agent_result = test_agent_definitions_exist(
    plugin_root / "agents" / "config.json",
    plugin_root / "agents"
)
routing_stats = get_routing_statistics(plugin_root / "agents" / "config.json")
```

### Step 2: Categorize Issues

```python
issues = {
    'critical': [],  # Must fix before release
    'high': [],      # Should fix, failure requires explanation
    'medium': [],    # Nice to have
    'low': [],       # Informational
    'auto_fixable': []  # Can be safely auto-fixed
}

# Critical: Missing required files
for file_path, file_info in structure_result['required_files'].items():
    if not file_info['exists']:
        issues['critical'].append({
            'type': 'missing_required_file',
            'file': file_path,
            'description': file_info['description'],
            'auto_fixable': False
        })

# High: Invalid configurations
for error in structure_result.get('errors', []):
    issues['high'].append({
        'type': 'structure_error',
        'error': error,
        'auto_fixable': False
    })

# Medium: Skill format issues
for skill_result in skill_results:
    if not skill_result['valid']:
        for error in skill_result['errors']:
            issues['medium'].append({
                'type': 'skill_format_error',
                'skill': skill_result['file'],
                'error': error,
                'auto_fixable': 'missing' in error.lower()  # Missing frontmatter fields can be auto-fixed
            })

# Medium: Orphaned agents
for orphaned in agent_result.get('orphaned_definitions', []):
    issues['medium'].append({
        'type': 'orphaned_agent',
        'agent': orphaned,
        'auto_fixable': True,  # Can be registered in config.json
        'fix_action': f"Add '{orphaned}' to agents/config.json"
    })

# Low: Naming inconsistencies
for naming_issue in skill_naming.get('issues', []):
    issues['low'].append({
        'type': 'naming_inconsistency',
        'directory': naming_issue['directory'],
        'issue': naming_issue['issue'],
        'auto_fixable': False  # Require manual decision
    })

# Count auto-fixable issues
auto_fixable_count = sum(1 for severity_issues in issues.values() for issue in severity_issues if issue.get('auto_fixable'))
```

### Step 3: Generate Report

```python
def generate_report(issues, structure_result, verbose=False):
    """Generate validation report."""

    print("\\nPopKit Plugin Validation Report")
    print("=" * 60)
    print()

    # Summary
    total_issues = sum(len(severity_issues) for severity_issues in issues.values())
    auto_fixable = sum(1 for severity_issues in issues.values() for issue in severity_issues if issue.get('auto_fixable'))

    print(f"Total Issues: {total_issues}")
    print(f"Auto-fixable: {auto_fixable}")
    print()

    # Health score
    from popkit_shared.utils.plugin_validator import get_plugin_health_score
    health = get_plugin_health_score(plugin_root)

    print(f"Plugin Health Score: {health['score']}/100 (Grade: {health['grade']})")
    if health['deductions']:
        print("\\nDeductions:")
        for deduction in health['deductions']:
            print(f"  - {deduction}")
    print()

    # Issues by severity
    for severity in ['critical', 'high', 'medium', 'low']:
        if issues[severity]:
            symbol = "✗" if severity in ['critical', 'high'] else "⚠"
            print(f"{symbol} {severity.upper()}: {len(issues[severity])} issues")

            for issue in issues[severity]:
                auto_fix = " [AUTO-FIXABLE]" if issue.get('auto_fixable') else ""
                print(f"  - {issue['type']}: {issue.get('error', issue.get('issue', 'unknown'))}{auto_fix}")

                if verbose and 'fix_action' in issue:
                    print(f"    Fix: {issue['fix_action']}")

            print()

    # Auto-fix suggestion
    if auto_fixable > 0:
        print(f"\\n{auto_fixable} issues can be automatically fixed.")
        print("Run: /popkit:plugin sync apply")
```

### Step 4: Apply Auto-Fixes (if requested)

```python
if args.apply:
    print("\\nApplying auto-fixes...")

    fixes_applied = 0

    for severity_issues in issues.values():
        for issue in severity_issues:
            if not issue.get('auto_fixable'):
                continue

            try:
                if issue['type'] == 'orphaned_agent':
                    # Register orphaned agent
                    fix_orphaned_agent(plugin_root, issue['agent'])
                    print(f"  ✓ Registered agent: {issue['agent']}")
                    fixes_applied += 1

                elif issue['type'] == 'skill_format_error' and 'missing' in issue['error'].lower():
                    # Add missing frontmatter fields
                    fix_missing_frontmatter(issue['skill'])
                    print(f"  ✓ Added frontmatter: {issue['skill']}")
                    fixes_applied += 1

                # Add more auto-fixes as needed

            except Exception as e:
                print(f"  ✗ Failed to fix {issue['type']}: {e}")

    print(f"\\nApplied {fixes_applied} auto-fixes")
```

## Safe Auto-Fixes

### What Can Be Auto-Fixed

1. **Missing Frontmatter Fields**
   - Add `name` and `description` with defaults
   - Extract name from directory
   - Generate placeholder description

2. **Orphaned Agents**
   - Register in `agents/config.json`
   - Add to appropriate tier based on directory
   - Add basic routing keywords

3. **Missing Output Style Schemas**
   - Create schema file with basic structure
   - Add required fields from template

4. **Missing Test Case Placeholders**
   - Create test definition with basic structure
   - Add to appropriate test category

### What's NEVER Auto-Fixed

- Code changes in hooks or utilities
- Agent prompts or instructions
- Skill process descriptions
- Configuration values (thresholds, API keys)
- File deletions or renames

## Auto-Fix Implementations

### Register Orphaned Agent

```python
def fix_orphaned_agent(plugin_root: Path, agent_name: str):
    """Add orphaned agent to config.json."""
    config_path = plugin_root / "agents" / "config.json"
    config = json.loads(config_path.read_text())

    # Determine tier from directory structure
    tier = 2  # Default to Tier 2 (on-demand)
    agent_file = None

    for tier_dir in (plugin_root / "agents").iterdir():
        if tier_dir.is_dir() and (tier_dir / f"{agent_name}.md").exists():
            if "tier-1" in tier_dir.name:
                tier = 1
            agent_file = tier_dir / f"{agent_name}.md"
            break

    # Add to agents section
    if 'agents' not in config:
        config['agents'] = {}

    config['agents'][agent_name] = {
        'tier': tier,
        'enabled': True
    }

    # Add basic routing keyword
    if 'routing' not in config:
        config['routing'] = {'keywords': {}}
    if 'keywords' not in config['routing']:
        config['routing']['keywords'] = {}

    # Use agent name as initial keyword
    config['routing']['keywords'][agent_name] = [agent_name.replace('-', ' ')]

    # Write back
    config_path.write_text(json.dumps(config, indent=2))
```

### Fix Missing Frontmatter

```python
def fix_missing_frontmatter(skill_file_path: str):
    """Add missing frontmatter fields to skill."""
    skill_file = Path(skill_file_path)
    content = skill_file.read_text()

    # Extract existing frontmatter
    frontmatter_match = re.match(r'^---\\s*\\n(.*?)\\n---\\s*\\n', content, re.DOTALL)

    if frontmatter_match:
        # Has frontmatter, add missing fields
        frontmatter_text = frontmatter_match.group(1)
        frontmatter = yaml.safe_load(frontmatter_text)

        # Add missing name
        if 'name' not in frontmatter:
            frontmatter['name'] = skill_file.parent.name

        # Add missing description
        if 'description' not in frontmatter:
            frontmatter['description'] = f"Skill for {skill_file.parent.name} (add description)"

        # Reconstruct file
        new_frontmatter = yaml.dump(frontmatter, default_flow_style=False)
        content_after = content[frontmatter_match.end():]
        new_content = f"---\\n{new_frontmatter}---\\n{content_after}"

    else:
        # No frontmatter, add it
        name = skill_file.parent.name
        frontmatter = {
            'name': name,
            'description': f"Skill for {name} (add description)"
        }

        new_frontmatter = yaml.dump(frontmatter, default_flow_style=False)
        new_content = f"---\\n{new_frontmatter}---\\n\\n{content}"

    skill_file.write_text(new_content)
```

## Output Examples

### Check Mode (default)

```
PopKit Plugin Validation Report
============================================================

Total Issues: 8
Auto-fixable: 3

Plugin Health Score: 85/100 (Grade: B+)

Deductions:
  - hooks.json errors (-10)
  - 5 warnings (-5)

✗ HIGH: 2 issues
  - structure_error: Hook files not found: deprecated-hook.py
  - structure_error: Invalid JSON in agents/config.json

⚠ MEDIUM: 3 issues
  - orphaned_agent: new-feature-agent [AUTO-FIXABLE]
    Fix: Add 'new-feature-agent' to agents/config.json
  - skill_format_error: Missing frontmatter field: description [AUTO-FIXABLE]
  - skill_format_error: Description contains placeholder text

⚠ LOW: 3 issues
  - naming_inconsistency: Directory 'old-name' doesn't match skill name

3 issues can be automatically fixed.
Run: /popkit:plugin sync apply
```

### Apply Mode

```
PopKit Plugin Validation Report
============================================================

[... same report as above ...]

Applying auto-fixes...
  ✓ Registered agent: new-feature-agent
  ✓ Added frontmatter: skills/example/SKILL.md
  ✓ Added frontmatter: skills/another/SKILL.md

Applied 3 auto-fixes

Re-run validation to verify fixes.
```

### JSON Output (--json)

```json
{
  "summary": {
    "total_issues": 8,
    "auto_fixable": 3,
    "health_score": 85,
    "grade": "B+"
  },
  "issues": {
    "critical": [],
    "high": [
      {
        "type": "structure_error",
        "error": "Hook files not found: deprecated-hook.py"
      }
    ],
    "medium": [
      {
        "type": "orphaned_agent",
        "agent": "new-feature-agent",
        "auto_fixable": true
      }
    ]
  }
}
```

## Integration

### Command Integration

Invoked by `/popkit:plugin sync [apply] [--component=<name>]`

### Dependencies

**Required utilities**:

- `popkit_shared.utils.plugin_validator`
- `popkit_shared.utils.skill_validator`
- `popkit_shared.utils.agent_router_test`

### Related Skills

- `pop-plugin-test` - Run automated tests
- `pop-doc-sync` - Synchronize documentation
- `pop-auto-docs` - Generate documentation

## Notes

- Only safe, reversible changes are auto-fixed
- All auto-fixes are logged for review
- Manual fixes required for structural changes
- JSON output enables CI/CD integration
- Health score helps track plugin quality over time
