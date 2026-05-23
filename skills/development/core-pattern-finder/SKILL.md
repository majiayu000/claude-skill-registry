---
name: core-pattern-finder
description: Use when needing Drupal core implementation examples - searches core modules for specific patterns and returns file path references
version: 1.1.0
user-invocable: false
---

# Core Pattern Finder

Search Drupal core for implementation patterns and return file references.

## Activation

Activate when you detect:
- "How does core do X?"
- "Find core example of X"
- "Show me core's implementation of X"
- Need a reference implementation for a Drupal pattern

## Quick Reference

Check these common patterns first before searching:

### Forms
| Pattern | Path |
|---------|------|
| ConfigFormBase | `core/modules/system/src/Form/SiteInformationForm.php` |
| FormBase | `core/modules/node/src/Form/NodeForm.php` |
| ConfirmFormBase | `core/modules/node/src/Form/NodeDeleteForm.php` |
| EntityForm | `core/modules/user/src/ProfileForm.php` |

### Entities
| Pattern | Path |
|---------|------|
| Content Entity | `core/modules/node/src/Entity/Node.php` |
| Config Entity | `core/modules/field/src/Entity/FieldConfig.php` |
| Entity List Builder | `core/modules/node/src/NodeListBuilder.php` |

### Services
| Pattern | Path |
|---------|------|
| Entity Type Manager | `core/lib/Drupal/Core/Entity/EntityTypeManager.php` |
| Plugin Manager | `core/lib/Drupal/Core/Block/BlockManager.php` |
| Event Subscriber | `core/modules/system/src/EventSubscriber/ConfigCacheTag.php` |

### Plugins
| Pattern | Path |
|---------|------|
| Block Plugin | `core/modules/system/src/Plugin/Block/SystemBrandingBlock.php` |
| Field Formatter | `core/modules/text/src/Plugin/Field/FieldFormatter/TextDefaultFormatter.php` |
| Field Widget | `core/modules/text/src/Plugin/Field/FieldWidget/TextareaWidget.php` |
| Condition Plugin | `core/modules/system/src/Plugin/Condition/RequestPath.php` |

### Controllers
| Pattern | Path |
|---------|------|
| ControllerBase | `core/modules/system/src/Controller/SystemController.php` |
| Entity Controller | `core/modules/node/src/Controller/NodeController.php` |

## Workflow

### 1. Check Quick Reference

If pattern matches table above, return that path immediately.

### 2. Search Core

If not in quick reference, search using these strategies:

**For class/interface patterns:**
```
Use Grep with pattern: "class {PatternName}" or "interface {PatternName}"
Path: core/
```

**For specific implementations:**
```
Use Grep with pattern: "extends {BaseClass}" or "implements {Interface}"
Path: core/modules/
```

**For service patterns:**
```
Use Glob with pattern: core/modules/*/src/*Manager.php
or: core/lib/Drupal/Core/*/*.php
```

### 3. Read and Extract Key Sections

Once file found, use `Read` tool and identify:
- Key methods to study
- Relevant line numbers
- Dependencies injected

### 4. Return Structured Response

Format your response as:

```
## Core Pattern: {Pattern Name}

### Primary Example
`{file_path}`

**Key methods:**
- `{method1}()` (line {X}): {what it does}
- `{method2}()` (line {Y}): {what it does}

**Dependencies:**
- {service_name}: {purpose}

### Additional Examples
- `{path2}` - {variation description}
- `{path3}` - {variation description}

### Usage Notes
{Any gotchas or important considerations}
```

## Stop Points

STOP and ask user:
- If pattern is ambiguous (multiple interpretations)
- If no matching pattern found in core
- Before reading more than 3 files (ask which to prioritize)
