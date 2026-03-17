---
name: Unity Template Generator
description: Generates production-ready C# script templates (MonoBehaviour, ScriptableObject, Editor, tests). Use when creating new scripts or setting up project structure.
allowed-tools: Write, Read, Glob
---

# Unity Template Generator

Assists with generating production-ready Unity C# script templates that follow best practices and Unity conventions.

## Available Templates

**MonoBehaviour** - GameObject components with lifecycle methods, serialized fields, component caching, and Gizmo helpers.

**ScriptableObject** - Data assets with `[CreateAssetMenu]`, validation, encapsulation, and clone methods.

**Editor Script** - Custom inspectors or windows. Asks for UGUI vs UI Toolkit preference (see [unity-ui-selector](../unity-ui-selector/SKILL.md)).

**Test Script** - NUnit/PlayMode tests with Setup/TearDown, `[UnityTest]`, performance tests, and Arrange-Act-Assert pattern.

## Template Features

All templates include:
- Unity coding conventions (`[SerializeField]`, PascalCase, XML docs)
- Performance patterns (component caching, no GetComponent in Update)
- Code organization (#region directives, consistent ordering)
- Safety features (null checks, OnValidate, Gizmos)

Placeholders: `{{CLASS_NAME}}`, `{{NAMESPACE}}`, `{{DESCRIPTION}}`, `{{MENU_PATH}}`, `{{FILE_NAME}}`

See [template-reference.md](template-reference.md) for detailed customization options.

## When to Use vs Other Components

**Use this Skill when**: Discussing template options, understanding template features, or getting guidance on script structure

**Use @unity-scripter agent when**: Writing custom scripts with specific requirements or implementing complex Unity features

**Use @unity-refactor agent when**: Improving existing scripts or restructuring code for better maintainability

**Use /unity:new-script command when**: Actually generating script files from templates with specific parameters

**Use /unity:setup-test command when**: Setting up complete test environments with test scripts

## Related Skills

- **unity-script-validator**: Validates generated scripts
- **unity-ui-selector**: Helps choose UI system for Editor scripts
- **unity-uitoolkit**: Assists with UI Toolkit implementation when generating Editor scripts
