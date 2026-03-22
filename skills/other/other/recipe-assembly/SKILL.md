---
name: recipe-assembly
description: Recipe-based context assembly and deployment using slice architecture. Use when building compilation pipelines, extracting documentation slices, or deploying context to multiple targets.
---

# Recipe Assembly

*A context workshop for recipe-based assembly and deployment. Write once, deploy everywhere via slice architecture.*

## Overview

Recipe Assembly documents the patterns for assembling context from distributed sources and deploying to multiple targets. This is not a complex build system—it's "make for context" with Obsidian integration.

This skill provides:

- **Recipe structure** for context assembly instructions
- **Slice architecture** for targeted content extraction
- **Assembly pipeline** (extract → template → output)
- **Synchronization patterns** for multi-target deployment
- **Template processing** for context transformation

The core insight: Context compilation should be deterministic, testable, and version-controlled. Recipes make implicit assembly explicit.

## The Architecture

```
Obsidian Context Vault → Recipes → assemble.py → Output → sync.py → Targets
```

| Component | Purpose | Location |
|-----------|---------|----------|
| **Recipes** | Assembly instructions | `workshop/*.md` |
| **Sources** | Content with slice markers | Vault files |
| **Output** | Assembled artifacts | `workshop/output/` |
| **Targets** | Deployment destinations | Config, steering files |
| **Manifest** | Deployment tracking | `workshop/recipe-manifest.md` |

## Recipe Structure

### Recipe Schema

Recipes combine Obsidian frontmatter with YAML configuration:

```yaml
---
# Obsidian frontmatter
id: recipe-identifier
type: recipe
status: active
---

# Recipe Title

## Description
[What this recipe produces]

## Configuration
```yaml
name: recipe-identifier
target_locations:
  - path: /deployment/target/file.md
sources:
  - slice: slice-identifier
    file: source/file/path.md
template: |
  Template with {content} substitution
```
```

### Recipe Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Unique recipe identifier |
| `target_locations` | Yes | Where to deploy output |
| `sources` | Yes | What content to extract |
| `template` | Optional | How to transform content |

### Recipe Types

| Type | Purpose | Example |
|------|---------|---------|
| **Agent** | System prompts | `recipe-agent-kiro.md` |
| **Steering** | Context guidance | `recipe-steering-workspace.md` |
| **Skill** | Skill documentation | `recipe-skill-bundle.md` |
| **Power** | Kiro power packages | `recipe-power-covenant.md` |

## Slice Architecture

### Slice Markers

HTML comment markers enable targeted extraction:

```markdown
<!-- slice:identifier -->
Content to extract
<!-- /slice -->
```

### Slice Patterns

**Simple Slice**:
```markdown
<!-- slice:agent=kiro -->
Kiro-specific agent configuration
<!-- /slice -->
```

**Namespaced Slice**:
```markdown
<!-- slice:agent=kiro:section=identity -->
Identity section only
<!-- /slice -->

<!-- slice:agent=kiro:section=constraints -->
Constraints section only
<!-- /slice -->
```

**Multi-Value Slice**:
```markdown
<!-- slice:skill=covenant-patterns -->
Full skill content
<!-- /slice -->
```

### Slice Resolution

```python
def resolve_slice(slice_spec, source_file):
    """Extract content matching slice specification."""

    content = read_file(source_file)

    # Parse slice spec: "agent=kiro" or "agent=kiro:section=identity"
    parts = parse_slice_spec(slice_spec)

    # Build marker pattern
    start_marker = f"<!-- slice:{slice_spec} -->"
    end_marker = "<!-- /slice -->"

    # Extract content between markers
    return extract_between(content, start_marker, end_marker)
```

## Assembly Pipeline

### Phase 1: Discovery

```python
def discover_recipes(workshop_path):
    """Find all recipe files in workshop directory."""

    recipes = []

    for file in glob(workshop_path / "*.md"):
        if file.name.startswith("recipe-"):
            recipe = parse_recipe(file)
            recipes.append(recipe)

    return recipes
```

### Phase 2: Extraction

```python
def extract_sources(recipe):
    """Extract content from all source slices."""

    contents = []

    for source in recipe.sources:
        slice_content = resolve_slice(
            slice_spec=source.slice,
            source_file=source.file
        )
        contents.append(slice_content)

    return join_contents(contents)
```

### Phase 3: Templating

```python
def apply_template(recipe, content):
    """Apply template substitution."""

    if recipe.template:
        return recipe.template.format(content=content)
    else:
        return content
```

### Phase 4: Output

```python
def write_output(recipe, assembled_content):
    """Write assembled content to output directory."""

    output_path = workshop_path / "output" / f"{recipe.name}.md"
    write_file(output_path, assembled_content)

    return output_path
```

### Full Assembly

```python
def assemble_recipe(recipe):
    """Complete assembly pipeline."""

    # Extract
    content = extract_sources(recipe)

    # Template
    assembled = apply_template(recipe, content)

    # Output
    output_path = write_output(recipe, assembled)

    return AssemblyResult(
        recipe=recipe.name,
        output=output_path,
        timestamp=now()
    )
```

## Synchronization

### Sync Pipeline

```python
def sync_recipe(recipe, output_path):
    """Deploy output to target locations."""

    results = []

    for target in recipe.target_locations:
        # Expand path (handle ~ and env vars)
        expanded_path = expand_path(target.path)

        # Copy output to target
        copy_file(output_path, expanded_path)

        results.append(SyncResult(
            target=expanded_path,
            timestamp=now()
        ))

    return results
```

### Orphan Cleanup

```python
def cleanup_orphans(manifest, current_outputs):
    """Remove files from previous deployments no longer produced."""

    previous_outputs = manifest.get_previous_outputs()
    orphans = previous_outputs - current_outputs

    for orphan in orphans:
        if orphan.exists():
            remove_file(orphan)
            log(f"Removed orphan: {orphan}")
```

### Manifest Tracking

```markdown
# Recipe Manifest

## Last Run
- Timestamp: 2024-01-15T10:30:00Z
- Recipes processed: 5
- Files deployed: 8

## Deployment History

### recipe-agent-kiro
- Output: workshop/output/recipe-agent-kiro.md
- Targets:
  - ~/.kiro/steering/agent.md (deployed)
- Status: success

### recipe-skill-bundle
- Output: workshop/output/recipe-skill-bundle.md
- Targets:
  - ~/.claude/skills/bundle.md (deployed)
- Status: success
```

## Covenant Integration

### Final-State Surgery

Recipe changes apply final-state surgery:
- New output replaces old completely
- Orphan cleanup removes abandoned targets
- No legacy artifacts preserved

```python
def apply_final_state(recipe, output):
    """Final-state deployment (no transition period)."""

    # Remove old deployment if exists
    for target in recipe.target_locations:
        if target.exists():
            remove_file(target)

    # Deploy new
    sync_recipe(recipe, output)

    # Clean orphans
    cleanup_orphans(manifest, current_outputs)
```

### Fast-Fail

Assembly fails immediately on missing slices:

```python
def extract_sources(recipe):
    """Extract with fast-fail on missing slices."""

    for source in recipe.sources:
        slice_content = resolve_slice(source.slice, source.file)

        if slice_content is None:
            raise SliceNotFoundError(
                f"Slice '{source.slice}' not found in '{source.file}'. "
                "Cannot proceed with partial assembly."
            )

    return contents
```

### Determinism

Assembly is deterministic given same inputs:

```python
def verify_determinism(recipe, run1_output, run2_output):
    """Verify deterministic assembly."""

    assert run1_output == run2_output, (
        f"Non-deterministic assembly detected for '{recipe.name}'. "
        "Check for time-based or random content."
    )
```

## Recipe Examples

### Agent Steering Recipe

```yaml
name: recipe-agent-kiro
target_locations:
  - path: ~/.kiro/steering/agent.md
sources:
  - slice: agent=kiro
    file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-principles.md
template: |
  # Kiro Agent Configuration

  ## Identity
  {content}

  ## Covenant Integration
  See covenant-patterns skill for principle enforcement.
```

### Skill Bundle Recipe

```yaml
name: recipe-skill-bundle
target_locations:
  - path: ~/.claude/skills/context-bundle.md
sources:
  - slice: skill=covenant-patterns
    file: skills/covenant-patterns/SKILL.md
  - slice: skill=agent-steering
    file: skills/agent-steering/SKILL.md
template: |
  # Context Skills Bundle

  Assembled from vault skills for Claude Code deployment.

  {content}
```

### Power Package Recipe

```yaml
name: recipe-power-epistemic
target_locations:
  - path: ~/.kiro/powers/epistemic-rendering/POWER.md
  - path: ~/.kiro/powers/epistemic-rendering/power.json
sources:
  - slice: power=epistemic-rendering
    file: skills/epistemic-rendering/POWER.md
template: |
  {content}
```

## VSCode Integration

### Task Configuration

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Workshop: Full Workflow",
      "type": "shell",
      "command": "python",
      "args": ["${workspaceFolder}/.dev/.scripts/assemble.py", "&&", "python", "${workspaceFolder}/.dev/.scripts/sync.py"],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    },
    {
      "label": "Workshop: Assemble Only",
      "type": "shell",
      "command": "python",
      "args": ["${workspaceFolder}/.dev/.scripts/assemble.py"]
    },
    {
      "label": "Workshop: Sync Only",
      "type": "shell",
      "command": "python",
      "args": ["${workspaceFolder}/.dev/.scripts/sync.py"]
    },
    {
      "label": "Workshop: Dry Run",
      "type": "shell",
      "command": "python",
      "args": ["${workspaceFolder}/.dev/.scripts/assemble.py", "--dry-run"]
    }
  ]
}
```

### Keyboard Shortcuts

- **Ctrl+Shift+B** — Full workflow (assemble + sync)
- **Ctrl+Shift+P** → "Tasks: Run Task" — Individual operations

## Quality Gates

### Pre-Assembly

- [ ] Recipe syntax valid (YAML parseable)
- [ ] Source files exist
- [ ] Slice markers present in sources
- [ ] Target paths valid

### Post-Assembly

- [ ] Output produced for all recipes
- [ ] Template substitution complete
- [ ] No missing slice warnings
- [ ] Determinism verified

### Post-Sync

- [ ] All targets deployed
- [ ] Orphans cleaned
- [ ] Manifest updated
- [ ] No permission errors

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| Slice not found | Marker missing or typo | Check slice spec matches marker exactly |
| Partial output | Template substitution failed | Verify `{content}` placeholder present |
| Permission denied | Target path not writable | Check file permissions, expand ~ correctly |
| Orphan not cleaned | Manifest out of sync | Delete manifest, rebuild |
| Non-deterministic | Time-based content | Remove timestamps from template |

## Related Skills

- **[covenant-patterns](../covenant-patterns/SKILL.md)** — Final-state surgery, determinism principles
- **[agent-steering](../agent-steering/SKILL.md)** — Steering recipes and deployment
- **[epistemic-rendering](../epistemic-rendering/SKILL.md)** — Lens template deployment
- **[multi-agent-coordination](../multi-agent-coordination/SKILL.md)** — Agent role slice architecture

---

*"Recipes make implicit assembly explicit. Write once, deploy everywhere."* 🔧
