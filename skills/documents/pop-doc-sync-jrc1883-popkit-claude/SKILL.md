---
name: doc-sync
description: Synchronize documentation with codebase - updates AUTO-GEN sections in CLAUDE.md, validates cross-references, and reports stale documentation
---

# Documentation Synchronization

Automatically update documentation sections based on codebase analysis.

## When to Use

- User runs `/popkit:plugin docs`
- After adding/removing agents, skills, or commands
- Before release to ensure docs are current
- During CI/CD to detect documentation drift

## Arguments

| Argument            | Description                        |
| ------------------- | ---------------------------------- |
| (none) or `--check` | Report what would change (default) |
| `--sync`            | Apply documentation updates        |
| `--json`            | Output results as JSON             |
| `--verbose`         | Show detailed changes              |

## Process

### Step 1: Analyze Codebase

```python
import os
from pathlib import Path
from popkit_shared.utils.doc_sync import (
    analyze_plugin_structure,
    find_auto_gen_sections,
    generate_tier_counts,
    generate_repo_structure,
    generate_key_files
)

# Get plugin root
plugin_root = Path(os.environ.get('CLAUDE_PLUGIN_ROOT', '.'))

# Analyze current structure
analysis = analyze_plugin_structure(plugin_root)

print(f"Analyzing {analysis['total_skills']} skills, {analysis['total_agents']} agents, {analysis['total_commands']} commands...")
```

### Step 2: Find AUTO-GEN Sections

```python
# Find CLAUDE.md
claude_md = plugin_root / "CLAUDE.md"

if not claude_md.exists():
    print("Warning: CLAUDE.md not found", file=sys.stderr)
    sys.exit(1)

content = claude_md.read_text()

# Find AUTO-GEN markers
auto_gen_sections = find_auto_gen_sections(content)

print(f"\\nFound {len(auto_gen_sections)} AUTO-GEN sections:")
for section_name in auto_gen_sections.keys():
    print(f"  - {section_name}")
```

### Step 3: Generate New Content

```python
updates = {}

# Generate tier counts
if 'TIER-COUNTS' in auto_gen_sections:
    new_tier_counts = generate_tier_counts(plugin_root)
    current_tier_counts = auto_gen_sections['TIER-COUNTS']['content']

    if new_tier_counts != current_tier_counts:
        updates['TIER-COUNTS'] = {
            'old': current_tier_counts,
            'new': new_tier_counts,
            'changed': True
        }
    else:
        updates['TIER-COUNTS'] = {'changed': False}

# Generate repo structure
if 'REPO-STRUCTURE' in auto_gen_sections:
    new_repo_structure = generate_repo_structure(plugin_root)
    current_repo_structure = auto_gen_sections['REPO-STRUCTURE']['content']

    if new_repo_structure != current_repo_structure:
        updates['REPO-STRUCTURE'] = {
            'old': current_repo_structure,
            'new': new_repo_structure,
            'changed': True
        }
    else:
        updates['REPO-STRUCTURE'] = {'changed': False}

# Generate key files
if 'KEY-FILES' in auto_gen_sections:
    new_key_files = generate_key_files(plugin_root)
    current_key_files = auto_gen_sections['KEY-FILES']['content']

    if new_key_files != current_key_files:
        updates['KEY-FILES'] = {
            'old': current_key_files,
            'new': new_key_files,
            'changed': True
        }
    else:
        updates['KEY-FILES'] = {'changed': False}
```

### Step 4: Report or Apply Changes

#### Check Mode (default)

```python
if args.check or not args.sync:
    changed_sections = [name for name, update in updates.items() if update.get('changed')]

    if not changed_sections:
        print("\\n✓ All AUTO-GEN sections are up to date")
        sys.exit(0)

    print(f"\\n{len(changed_sections)} sections need updating:")

    for section_name in changed_sections:
        update = updates[section_name]
        print(f"\\n{'='*60}")
        print(f"{section_name} (changed)")
        print(f"{'='*60}")

        if args.verbose:
            print("\\nCurrent:")
            print(update['old'])
            print("\\nNew:")
            print(update['new'])
        else:
            print("Run with --verbose to see diff")

    print(f"\\nRun with --sync to apply these changes")
    sys.exit(1)  # Exit 1 to indicate changes needed
```

#### Sync Mode (--sync)

```python
if args.sync:
    from popkit_shared.utils.doc_sync import apply_auto_gen_updates

    print("\\nApplying documentation updates...")

    result = apply_auto_gen_updates(claude_md, updates)

    for section_name, applied in result['applied'].items():
        if applied:
            print(f"  ✓ Updated {section_name}")
        else:
            print(f"  - {section_name} (no change)")

    if result['success']:
        print(f"\\n✓ Documentation synchronized successfully")
        sys.exit(0)
    else:
        print(f"\\n✗ Failed to synchronize: {result.get('error')}")
        sys.exit(1)
```

## AUTO-GEN Section Generators

### TIER-COUNTS

Generates agent and skill counts by tier:

```markdown
<!-- AUTO-GEN:TIER-COUNTS START -->

- Tier 1: Always-active core agents (11)
- Tier 2: On-demand specialists activated by triggers (17)
- Feature Workflow: 7-phase development agents (3)
- Skills: 68 reusable skills
- Commands: 24 slash commands
<!-- AUTO-GEN:TIER-COUNTS END -->
```

Implementation:

```python
def generate_tier_counts(plugin_root: Path) -> str:
    """Generate tier counts section."""

    # Count agents by tier
    tier_1_count = len(list((plugin_root / "agents" / "tier-1-always-active").glob("*.md")))
    tier_2_count = len(list((plugin_root / "agents" / "tier-2-on-demand").glob("*.md")))
    feature_count = len(list((plugin_root / "agents" / "feature-workflow").glob("*.md")))

    # Count skills and commands
    skills_count = len(list((plugin_root / "skills").glob("*/SKILL.md")))
    commands_count = len(list((plugin_root / "commands").glob("*.md")))

    return f"""- Tier 1: Always-active core agents ({tier_1_count})
- Tier 2: On-demand specialists activated by triggers ({tier_2_count})
- Feature Workflow: 7-phase development agents ({feature_count})
- Skills: {skills_count} reusable skills
- Commands: {commands_count} slash commands"""
```

### REPO-STRUCTURE

Generates directory tree structure:

```markdown
<!-- AUTO-GEN:REPO-STRUCTURE START -->
```

packages/
plugin/ Claude Code plugin (main package)
.claude-plugin/ Plugin manifest
agents/ 31 agent definitions
skills/ 68 reusable skills
commands/ 24 slash commands
hooks/ 23 Python hooks

```
<!-- AUTO-GEN:REPO-STRUCTURE END -->
```

Implementation:

```python
def generate_repo_structure(plugin_root: Path) -> str:
    """Generate repository structure tree."""

    tree_lines = []

    def add_dir(path: Path, indent: int = 0):
        """Recursively build tree."""
        indent_str = "  " * indent

        # Add directory name with count
        dir_name = path.name if indent > 0 else "packages/"
        tree_lines.append(f"{indent_str}{dir_name}")

        # Add description for key directories
        descriptions = {
            'plugin': 'Claude Code plugin (main package)',
            '.claude-plugin': 'Plugin manifest',
            'agents': f'{count_agents(path)} agent definitions',
            'skills': f'{count_skills(path)} reusable skills',
            'commands': f'{count_commands(path)} slash commands',
            'hooks': f'{count_hooks(path)} Python hooks'
        }

        if path.name in descriptions:
            tree_lines.append(f"{indent_str}  {descriptions[path.name]}")

        # Recurse for important subdirectories only
        if indent < 2:
            for subdir in sorted(path.iterdir()):
                if subdir.is_dir() and not subdir.name.startswith('.'):
                    add_dir(subdir, indent + 1)

    add_dir(plugin_root)
    return "\\n".join(tree_lines)
```

### KEY-FILES

Generates table of key configuration files:

```markdown
<!-- AUTO-GEN:KEY-FILES START -->

| File                                 | Purpose                         |
| ------------------------------------ | ------------------------------- |
| `packages/plugin/agents/config.json` | Agent routing and configuration |
| `packages/plugin/hooks/hooks.json`   | Hook event configuration        |
| `packages/cloud/wrangler.toml`       | Cloudflare Workers config       |

<!-- AUTO-GEN:KEY-FILES END -->
```

Implementation:

```python
def generate_key_files(plugin_root: Path) -> str:
    """Generate key files table."""

    key_files = [
        (".claude-plugin/plugin.json", "Plugin manifest"),
        ("agents/config.json", "Agent routing and configuration"),
        ("hooks/hooks.json", "Hook event configuration"),
        ("README.md", "Plugin documentation")
    ]

    # Filter to existing files
    existing_files = [
        (str(plugin_root / file), desc)
        for file, desc in key_files
        if (plugin_root / file).exists()
    ]

    # Generate table
    lines = ["| File | Purpose |", "|------|---------|"]

    for file_path, description in existing_files:
        # Make path relative to repo root
        rel_path = file_path.replace(str(plugin_root), "packages/plugin")
        lines.append(f"| `{rel_path}` | {description} |")

    return "\\n".join(lines)
```

## Validation

### Cross-Reference Validation

Check that references in documentation are valid:

```python
def validate_cross_references(content: str, plugin_root: Path) -> List[Dict]:
    """Find broken references in documentation."""

    issues = []

    # Find markdown links [text](path)
    links = re.findall(r'\\[([^\\]]+)\\]\\(([^)]+)\\)', content)

    for text, path in links:
        # Skip external URLs
        if path.startswith('http'):
            continue

        # Check if file exists
        file_path = plugin_root / path
        if not file_path.exists():
            issues.append({
                'type': 'broken_link',
                'text': text,
                'path': path,
                'line': content[:content.find(path)].count('\\n') + 1
            })

    return issues
```

### Stale Documentation Detection

Find documentation that may be outdated:

```python
def detect_stale_documentation(plugin_root: Path) -> List[Dict]:
    """Detect potentially stale documentation."""

    stale = []

    # Check if CHANGELOG.md mentions latest version
    plugin_json = json.loads((plugin_root / ".claude-plugin" / "plugin.json").read_text())
    current_version = plugin_json['version']

    changelog = (plugin_root / "CHANGELOG.md").read_text()
    if current_version not in changelog:
        stale.append({
            'file': 'CHANGELOG.md',
            'issue': f'Missing entry for version {current_version}'
        })

    # Check if AUTO-GEN sections are out of sync
    # (already handled by main sync logic)

    return stale
```

## Output Examples

### Check Mode

```
Analyzing 68 skills, 31 agents, 24 commands...

Found 3 AUTO-GEN sections:
  - TIER-COUNTS
  - REPO-STRUCTURE
  - KEY-FILES

2 sections need updating:

============================================================
TIER-COUNTS (changed)
============================================================
Run with --verbose to see diff

============================================================
REPO-STRUCTURE (changed)
============================================================
Run with --verbose to see diff

Run with --sync to apply these changes
```

### Sync Mode

```
Analyzing 68 skills, 31 agents, 24 commands...

Found 3 AUTO-GEN sections:
  - TIER-COUNTS
  - REPO-STRUCTURE
  - KEY-FILES

Applying documentation updates...
  ✓ Updated TIER-COUNTS
  ✓ Updated REPO-STRUCTURE
  - KEY-FILES (no change)

✓ Documentation synchronized successfully
```

### JSON Output (--json)

```json
{
  "analysis": {
    "total_skills": 68,
    "total_agents": 31,
    "total_commands": 24
  },
  "sections": {
    "TIER-COUNTS": {
      "changed": true
    },
    "REPO-STRUCTURE": {
      "changed": true
    },
    "KEY-FILES": {
      "changed": false
    }
  },
  "changes_needed": 2,
  "up_to_date": 1
}
```

## Integration

### Command Integration

Invoked by `/popkit:plugin docs [--check|--sync] [--json]`

### Dependencies

**Required utilities**:

- `popkit_shared.utils.doc_sync`

### Related Skills

- `pop-validation-engine` - Validate plugin integrity
- `pop-auto-docs` - Generate comprehensive documentation
- `pop-plugin-test` - Test plugin components

## Notes

- Always run --check before --sync to preview changes
- AUTO-GEN sections are preserved exactly as marked
- Manual changes outside AUTO-GEN sections are preserved
- Cross-reference validation helps prevent broken links
- Stale documentation detection prevents version drift
- JSON output enables CI/CD integration
