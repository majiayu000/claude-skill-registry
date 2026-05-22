---
description: Use this skill when the user asks to "generate stories for components", "parse component props", "detect component variants", "analyze components", "create stories automatically", mentions "component parser", "story automation", or wants to generate Storybook stories from existing component files. This skill provides intelligent component analysis and CSF 3.0 story generation with interaction tests and accessibility checks.
---

# Story Generation Skill

## Overview

Generate Storybook stories automatically from existing components by parsing prop types, detecting variants, and creating comprehensive CSF 3.0 stories with interaction tests and accessibility validation.

This skill provides a complete component analysis and story generation pipeline for React, Vue, and Svelte components.

## What This Skill Provides

### Component Analysis
Parse component files to extract:
- Component name and type classification
- Props with TypeScript types
- Required vs optional props
- Default values
- Children/slots detection

### Intelligent Variant Detection
Automatically detect story variants from:
- Enum/union types: `'primary' | 'secondary' | 'outline'`
- Size props: `small`, `medium`, `large`
- Boolean states: `disabled`, `loading`, `error`
- Component-type specific patterns

### Story Generation
Create complete story files with:
- **CSF 3.0 format** (`satisfies Meta<typeof Component>`)
- **ArgTypes** with inferred controls (select, boolean, action)
- **Variant stories** for all detected variations
- **Interaction tests** with play functions (Testing Library)
- **Accessibility tests** with axe-core rules
- **Component-specific test patterns** (button clicks, input validation, modal focus)

### Multi-Framework Support
- **React/TypeScript**: Parse interfaces, types, function components
- **Vue 3**: Parse `defineProps<T>` and runtime props
- **Svelte**: Parse `export let` statements

## Core Scripts

The skill provides four main scripts in `scripts/`:

### 1. parse_component.py
Parse component files to extract metadata.

**Usage:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/story-generation/scripts/parse_component.py \
  path/to/Component.tsx \
  --json
```

**Output:** Component metadata (name, framework, props, type classification)

### 2. detect_variants.py
Detect story variants from component props.

**Usage:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/story-generation/scripts/detect_variants.py \
  path/to/Component.tsx \
  --json
```

**Output:** List of variants with args and priorities

### 3. generate_story.py
Generate complete story file with tests.

**Usage:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/story-generation/scripts/generate_story.py \
  path/to/Component.tsx \
  --level full \
  --output path/to/Component.stories.tsx
```

**Testing levels:**
- `full`: All features (variants + interaction tests + a11y tests)
- `standard`: Variants + interaction tests
- `basic`: Variants with args/controls only
- `minimal`: Single default story

### 4. scan_components.py
Scan project directories for components.

**Usage:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/story-generation/scripts/scan_components.py \
  src \
  --json
```

**Output:** JSON array of discovered components with metadata

## Story Templates

Templates are located in `templates/` directory:

- `react-full.template` - React with full testing
- `react-basic.template` - React basic stories
- `vue-full.template` - Vue 3 with full testing
- `svelte-full.template` - Svelte with full testing

Templates use variable replacement:
- `{{COMPONENT_NAME}}` - Component name
- `{{VARIANT_STORIES}}` - Generated variant exports
- `{{INTERACTION_TEST_CODE}}` - Test code
- `{{A11Y_RULES}}` - Accessibility rules

## Workflow Integration

This skill integrates with the `/generate-stories` command:

1. **Scan**: Discover components with `scan_components.py`
2. **Parse**: Extract metadata with `parse_component.py`
3. **Detect**: Find variants with `detect_variants.py`
4. **Generate**: Create story with `generate_story.py`

## Component Type Support

The parser automatically detects and generates appropriate tests for:

| Type | Example | Special Handling |
|------|---------|------------------|
| button | Button, SubmitButton | Click tests, disabled check |
| input | TextField, Input | Type tests, value validation |
| checkbox | Checkbox | Click, checked state |
| select | Dropdown, Select | Option selection |
| card | Card, ProductCard | Render tests |
| modal | Dialog, Modal | Focus trap, ESC handler |
| table | DataTable, Table | Row/column tests |

15+ component types supported with custom test patterns.

## Example Usage

### Parse a Button Component

```bash
# Parse component
python3 scripts/parse_component.py src/components/Button.tsx

# Output:
# Component: Button
# Framework: react
# Type: button
# Props (6):
#   - variant: 'primary' | 'secondary' | 'outline' | 'ghost' (required)
#   - size: 'small' | 'medium' | 'large' (optional)
#   - disabled: boolean (optional)
#   - loading: boolean (optional)
#   - onClick: () => void (optional)
#   - children: React.ReactNode (required)
```

### Detect Variants

```bash
# Detect variants
python3 scripts/detect_variants.py src/components/Button.tsx

# Output:
# Detected 11 variants:
# 1. Primary (variant: primary)
# 2. Secondary (variant: secondary)
# 3. Outline (variant: outline)
# 4. Ghost (variant: ghost)
# 5-7. Small/Medium/Large (size variants)
# 8. Disabled (boolean state)
# 9. Loading (boolean state)
```

### Generate Complete Story

```bash
# Generate story with full testing
python3 scripts/generate_story.py \
  src/components/Button.tsx \
  --level full \
  --output src/components/Button.stories.tsx
```

**Generated story includes:**
- Meta configuration with argTypes
- 11 variant stories (Primary, Secondary, Outline, Ghost, Small, Large, Disabled, Loading, etc.)
- Interaction test with play function
- Accessibility test with axe-core rules

## Performance

- Component parsing: ~10ms per component
- Variant detection: ~1ms per component
- Story generation: ~15ms per component
- **Total**: ~26ms per component

Can process 100+ components in 2-3 seconds.

## Error Handling

The scripts handle common errors gracefully:
- **Parse failures**: Skip component, continue with others
- **Unknown types**: Fall back to generic component template
- **Missing files**: Clear error messages
- **Invalid syntax**: Report parsing errors with line numbers

## Best Practices

When using this skill:

1. **Parse first**: Always parse component before generating story to ensure it's supported
2. **Check variants**: Review detected variants to ensure they match expectations
3. **Choose testing level**: Use `full` for comprehensive testing, `basic` for simple stories
4. **Review output**: Generated stories are production-ready but may need customization

## References

- **README.md**: Complete usage guide with examples
- **scripts/**: All parser and generator scripts
- **templates/**: Story templates for each framework
- **test_samples/**: Sample components for testing

## Related Commands

- `/generate-stories` - Interactive workflow using this skill
- `/create-component` - Creates components with auto-generated stories

## Technical Details

**Parser Implementation:**
- Regex-based parsing (no AST dependencies)
- TypeScript interface extraction
- Vue Composition API support
- Svelte reactive declarations

**Variant Detection:**
- Pattern matching on type unions
- Heuristic-based classification
- Priority sorting (high-priority variants first)
- Component-type specific detection

**Story Generation:**
- Template-based with variable replacement
- CSF 3.0 format compliance
- Testing Library integration
- axe-core accessibility rules

All scripts use Python 3.8+ standard library only (no external dependencies).
