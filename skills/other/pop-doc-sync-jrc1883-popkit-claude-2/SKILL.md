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
from popkit_shared.utils.doc_sync import analyze_plugin_structure

plugin_root = Path(os.environ.get('CLAUDE_PLUGIN_ROOT', '.'))
analysis = analyze_plugin_structure(plugin_root)

print(f"Analyzing {analysis['total_skills']} skills, {analysis['total_agents']} agents, {analysis['total_commands']} commands...")
```

### Step 2: Find AUTO-GEN Sections

```python
from popkit_shared.utils.doc_sync import find_auto_gen_sections

claude_md = plugin_root / "CLAUDE.md"
content = claude_md.read_text()
auto_gen_sections = find_auto_gen_sections(content)

print(f"\nFound {len(auto_gen_sections)} AUTO-GEN sections:")
for section_name in auto_gen_sections.keys():
    print(f"  - {section_name}")
```

### Step 3: Generate New Content

```python
from popkit_shared.utils.doc_sync import (
    generate_tier_counts,
    generate_repo_structure,
    generate_key_files
)

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

# Similar for REPO-STRUCTURE and KEY-FILES
```

### Step 4: Report or Apply Changes

#### Check Mode (default)

```python
if args.check or not args.sync:
    changed_sections = [name for name, update in updates.items() if update.get('changed')]

    if not changed_sections:
        print("\n✓ All AUTO-GEN sections are up to date")
        sys.exit(0)

    print(f"\n{len(changed_sections)} sections need updating:")
    for section_name in changed_sections:
        print(f"\n{'='*60}")
        print(f"{section_name} (changed)")
        print(f"{'='*60}")

        if args.verbose:
            update = updates[section_name]
            print("\nCurrent:")
            print(update['old'])
            print("\nNew:")
            print(update['new'])
        else:
            print("Run with --verbose to see diff")

    print(f"\nRun with --sync to apply these changes")
    sys.exit(1)  # Exit 1 to indicate changes needed
```

#### Sync Mode (--sync)

```python
if args.sync:
    from popkit_shared.utils.doc_sync import apply_auto_gen_updates

    print("\nApplying documentation updates...")
    result = apply_auto_gen_updates(claude_md, updates)

    for section_name, applied in result['applied'].items():
        if applied:
            print(f"  ✓ Updated {section_name}")
        else:
            print(f"  - {section_name} (no change)")

    if result['success']:
        print(f"\n✓ Documentation synchronized successfully")
        sys.exit(0)
    else:
        print(f"\n✗ Failed to synchronize: {result.get('error')}")
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

### REPO-STRUCTURE

Generates directory tree structure:

```markdown
<!-- AUTO-GEN:REPO-STRUCTURE START -->

packages/
plugin/ Claude Code plugin (main package)
.claude-plugin/ Plugin manifest
agents/ 31 agent definitions
skills/ 68 reusable skills
commands/ 24 slash commands
hooks/ 23 Python hooks

<!-- AUTO-GEN:REPO-STRUCTURE END -->
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
