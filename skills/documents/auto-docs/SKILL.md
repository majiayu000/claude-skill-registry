---
name: auto-docs
description: Generate comprehensive documentation from codebase analysis - creates README sections, API docs, migration guides, and examples from code
---

# Auto-Documentation Generator

Analyzes codebase and generates/updates comprehensive documentation automatically.

## When to Use

- User runs `/popkit:plugin docs --generate`
- After major feature additions
- Before release to ensure complete documentation
- When creating new plugin packages

## Arguments

| Argument          | Description                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------------- |
| (target)          | Documentation to generate: `readme`, `api`, `migration`, `examples`, `all` (default: readme) |
| `--output=<path>` | Custom output path                                                                           |
| `--json`          | Output results as JSON                                                                       |
| `--verbose`       | Show detailed generation process                                                             |

## Process

### Step 1: Analyze Codebase

```python
import os
from pathlib import Path
from popkit_shared.utils.plugin_validator import validate_plugin_structure
from popkit_shared.utils.skill_validator import get_skill_statistics
from popkit_shared.utils.agent_router_test import get_routing_statistics

# Get plugin root
plugin_root = Path(os.environ.get('CLAUDE_PLUGIN_ROOT', '.'))

print("Analyzing codebase...")

# Get structure
structure = validate_plugin_structure(plugin_root)

# Get skill stats
skill_stats = get_skill_statistics(plugin_root / "skills")

# Get routing stats
routing_stats = get_routing_statistics(plugin_root / "agents" / "config.json")

# Load plugin.json
plugin_json = json.loads((plugin_root / ".claude-plugin" / "plugin.json").read_text())

analysis = {
    'name': plugin_json.get('name', 'Unknown'),
    'version': plugin_json.get('version', '0.0.0'),
    'description': plugin_json.get('description', ''),
    'skills': skill_stats,
    'routing': routing_stats,
    'structure': structure
}
```

### Step 2: Generate Documentation

Based on target, generate appropriate documentation:

#### README Generation

```python
def generate_readme(analysis: Dict) -> str:
    """Generate README.md from codebase analysis."""

    sections = []

    # Header
    sections.append(f"# {analysis['name']}")
    sections.append(f"\\n{analysis['description']}\\n")

    # Version badge
    sections.append(f"**Version:** {analysis['version']}\\n")

    # Installation
    sections.append("## Installation\\n")
    sections.append(f"/plugin install {analysis['name']}@{get_marketplace_name(analysis['name'])}\\n")

    # Features (from skills)
    sections.append("## Features\\n")

    skill_dirs = list((plugin_root / "skills").iterdir())
    if skill_dirs:
        for skill_dir in skill_dirs:
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                # Extract description from frontmatter
                validation = validate_skill_format(skill_file)
                desc = validation['frontmatter'].get('description', '')

                if desc:
                    sections.append(f"- **{skill_dir.name}**: {desc}")

    sections.append("")

    # Commands (from commands/)
    sections.append("## Commands\\n")

    command_files = list((plugin_root / "commands").glob("*.md"))
    if command_files:
        for cmd_file in sorted(command_files):
            cmd_name = cmd_file.stem
            # Extract description from frontmatter
            content = cmd_file.read_text()
            fm_match = re.match(r'^---\\s*\\n(.*?)\\n---', content, re.DOTALL)

            if fm_match:
                fm = yaml.safe_load(fm_match.group(1))
                desc = fm.get('description', '')
                sections.append(f"- `/popkit:{cmd_name}` - {desc}")

    sections.append("")

    # Configuration
    sections.append("## Configuration\\n")
    sections.append("This plugin requires no additional configuration.\\n")

    # Contributing
    sections.append("## Contributing\\n")
    sections.append("See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.\\n")

    # License
    license_name = plugin_json.get('license', 'MIT')
    sections.append(f"## License\\n")
    sections.append(f"{license_name}\\n")

    return "\\n".join(sections)
```

#### API Documentation

```python
def generate_api_docs(analysis: Dict) -> str:
    """Generate API.md documenting skills, commands, and hooks."""

    sections = []

    sections.append("# API Documentation\\n")
    sections.append(f"**Plugin:** {analysis['name']} v{analysis['version']}\\n")

    # Skills API
    sections.append("## Skills\\n")
    sections.append("Skills are invoked via the `Skill` tool.\\n")

    for skill_dir in sorted((plugin_root / "skills").iterdir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        validation = validate_skill_format(skill_file)
        name = validation['frontmatter'].get('name', skill_dir.name)
        desc = validation['frontmatter'].get('description', '')

        sections.append(f"### {name}\\n")
        sections.append(f"{desc}\\n")

        # Extract arguments from skill content
        content = skill_file.read_text()
        args_section = extract_section(content, "Arguments")

        if args_section:
            sections.append("**Arguments:**\\n")
            sections.append(args_section)

        sections.append("")

    # Commands API
    sections.append("## Commands\\n")
    sections.append("Commands are slash commands available in the UI.\\n")

    for cmd_file in sorted((plugin_root / "commands").glob("*.md")):
        content = cmd_file.read_text()
        fm_match = re.match(r'^---\\s*\\n(.*?)\\n---', content, re.DOTALL)

        if fm_match:
            fm = yaml.safe_load(fm_match.group(1))
            name = cmd_file.stem
            desc = fm.get('description', '')

            sections.append(f"### /popkit:{name}\\n")
            sections.append(f"{desc}\\n")

    # Hooks API
    sections.append("## Hooks\\n")
    sections.append("Hooks are automatically triggered by Claude Code events.\\n")

    hooks_json = json.loads((plugin_root / "hooks" / "hooks.json").read_text())

    for hook_type, matchers in hooks_json.get('hooks', {}).items():
        sections.append(f"### {hook_type}\\n")

        hook_count = sum(len(m.get('hooks', [])) for m in matchers)
        sections.append(f"**Registered hooks:** {hook_count}\\n")

    return "\\n".join(sections)
```

#### Migration Guide

```python
def generate_migration_guide(from_version: str, to_version: str) -> str:
    """Generate migration guide from git history."""

    sections = []

    sections.append(f"# Migration Guide: {from_version} → {to_version}\\n")

    # Get commits between versions
    import subprocess
    commits = subprocess.run(
        ['git', 'log', f'v{from_version}..v{to_version}', '--oneline'],
        capture_output=True,
        text=True
    ).stdout.strip().split('\\n')

    # Analyze commits for breaking changes
    breaking_changes = []
    new_features = []

    for commit in commits:
        if 'BREAKING' in commit or '!' in commit:
            breaking_changes.append(commit)
        elif 'feat:' in commit or 'feature:' in commit:
            new_features.append(commit)

    # Breaking changes
    if breaking_changes:
        sections.append("## Breaking Changes\\n")
        for change in breaking_changes:
            sections.append(f"- {change}")
        sections.append("")

    # New features
    if new_features:
        sections.append("## New Features\\n")
        for feature in new_features:
            sections.append(f"- {feature}")
        sections.append("")

    # Migration steps
    sections.append("## Migration Steps\\n")
    sections.append("1. Update plugin: `/plugin update popkit`")
    sections.append("2. Restart Claude Code")
    sections.append("3. Review breaking changes above")
    sections.append("4. Test critical workflows\\n")

    return "\\n".join(sections)
```

### Step 3: Write Documentation Files

```python
def write_documentation(target: str, content: str, output_path: Path = None):
    """Write generated documentation to file."""

    if output_path is None:
        # Default output paths
        output_paths = {
            'readme': plugin_root / "README.md",
            'api': plugin_root / "API.md",
            'migration': plugin_root / "MIGRATION.md",
            'examples': plugin_root / "EXAMPLES.md"
        }
        output_path = output_paths.get(target, plugin_root / f"{target.upper()}.md")

    # Ask user for confirmation before overwriting
    if output_path.exists():
        print(f"\\nFile exists: {output_path}")
        print("Overwrite? (y/n): ", end="")
        confirm = input().lower()

        if confirm != 'y':
            print("Skipped")
            return False

    output_path.write_text(content)
    print(f"✓ Generated: {output_path}")
    return True
```

## Documentation Templates

### README Template

```markdown
# {name}

{description}

**Version:** {version}

## Installation

/plugin install {name}@{marketplace}

## Features

- **skill-1**: Description
- **skill-2**: Description

## Commands

- /popkit:command-1 - Description
- /popkit:command-2 - Description

## Configuration

Configuration details...

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

{license}
```

### API Template

```markdown
# API Documentation

**Plugin:** {name} v{version}

## Skills

### skill-name

Description...

**Arguments:**

- arg1: Description
- arg2: Description

## Commands

### /popkit:command

Description...

## Hooks

### PreToolUse

**Registered hooks:** N
```

## Output Examples

### README Generation

```
Analyzing codebase...

Generating README.md...
  - Extracting plugin metadata
  - Analyzing 68 skills
  - Analyzing 24 commands
  - Generating features section
  - Generating commands section

✓ Generated: README.md

README.md statistics:
  - Sections: 7
  - Features: 68
  - Commands: 24
  - Words: 1,234
```

### API Documentation

```
Generating API.md...
  - Documenting 68 skills
  - Documenting 24 commands
  - Documenting 8 hook types

✓ Generated: API.md

API.md statistics:
  - Skills: 68
  - Commands: 24
  - Hook types: 8
  - Total endpoints: 100
```

### Migration Guide

```
Generating MIGRATION.md (v0.1.0 → v0.2.0)...
  - Analyzing git history
  - Found 3 breaking changes
  - Found 12 new features
  - Generating migration steps

✓ Generated: MIGRATION.md

Migration guide includes:
  - Breaking changes: 3
  - New features: 12
  - Migration steps: 4
```

## Integration

### Command Integration

Invoked by `/popkit:plugin docs --generate [target]`

### Dependencies

**Required utilities**:

- `popkit_shared.utils.plugin_validator`
- `popkit_shared.utils.skill_validator`
- `popkit_shared.utils.agent_router_test`

### Related Skills

- `pop-doc-sync` - Synchronize AUTO-GEN sections
- `pop-validation-engine` - Validate plugin integrity
- `pop-plugin-test` - Test plugin components

## Notes

- Always reviews generated docs before committing
- Templates can be customized per project
- Git history analysis requires git repository
- API docs are generated from code annotations
- Migration guides require tagged versions
- Examples can be extracted from test files
