---
name: kotlin-composable-preview
description: Generate comprehensive @Preview functions for Jetpack Compose composables. Analyzes component parameters, states, and dependencies to create previews covering all visual states, edge cases, and configurations.
---

# Kotlin Composable Preview Generator

Skill for generating production-quality @Preview functions for Jetpack Compose UI components.

## When to Use

- Adding previews to new Composable functions
- Enhancing existing previews with more state coverage
- Creating previews for components with sealed class states
- Generating multi-configuration previews (light/dark, device sizes)

## Preview Categories

1. **Simple Preview** - Basic single-state preview
2. **Multi-State Preview** - Separate @Preview for each state (sealed class, enum)
3. **Variant Preview** - Column/Row showing all variants in one preview
4. **Interactive Preview** - Using PreviewParameter for data-driven previews
5. **Configuration Preview** - Device, font scale, UI mode configurations

## Generation Workflow

1. **Analyze Composable signature**
   - Extract parameters (required/optional)
   - Identify state classes (data class, sealed class, enum)
   - Find callback parameters (lambdas)

2. **Identify preview requirements**
   - Check for HazeState dependency → needs hazeSource setup
   - Check for modifier patterns → use appropriate sizing
   - Check for sealed class states → generate preview for each subtype

3. **Generate previews**
   - Follow naming: `{ComposableName}Preview`, `{ComposableName}{State}Preview`
   - Use `private` modifier for preview functions
   - Add dark background wrapper when needed
   - Provide realistic sample data

## Preview Patterns Reference

See `references/preview-patterns.md` for detailed examples.

## Output Guidelines

| Aspect | Guideline |
|--------|-----------|
| Naming | `{ComposableName}Preview`, `{ComposableName}{State}Preview` |
| Visibility | `private` for preview functions |
| Background | Use `Box(Modifier.background(Black))` for dark-themed components |
| HazeState | Use `rememberHazeState()` + `hazeSource()` setup |
| Callbacks | Use empty lambdas `{}` for onClick, onDismiss |
| Sample Data | Use realistic Vietnamese text when appropriate |

## Quality Checklist

- [ ] All sealed class/enum states have dedicated previews
- [ ] Required parameters have realistic sample values
- [ ] Preview renders correctly in Android Studio
- [ ] Dark backgrounds used for dark-themed components
- [ ] HazeState properly configured when needed
- [ ] Proper imports added
