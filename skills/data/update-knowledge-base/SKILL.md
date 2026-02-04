---
name: update-knowledge-base
description: Analyze code changes and update KNOWLEDGE_BASE.md with architectural and feature changes.
---

# Update Knowledge Base

## Purpose

Automatically analyze recent code changes and update the project's knowledge base documentation to reflect current architecture, features, and conventions.

## Instructions

1. **Analyze Recent Changes**
   - Review git diff or recent commits
   - Identify new adapters, commands, or features
   - Note architectural changes or new patterns

2. **Read Current Knowledge Base**
   - Check if KNOWLEDGE_BASE.md exists
   - If not, create it with proper structure
   - If exists, identify sections needing updates

3. **Update Sections**
   - **Architecture**: Update if new adapters or core components added
   - **Features**: Document new CLI commands or options
   - **Conventions**: Note any new coding patterns established
   - **API Changes**: Document breaking changes or deprecations

4. **Verify Accuracy**
   - Cross-reference with actual source code
   - Ensure examples are runnable
   - Check that all documented features exist

5. **Format Consistently**
   - Use consistent markdown formatting
   - Include code examples where helpful
   - Maintain table format for command references

## Knowledge Base Structure

```markdown
# AI Rules Sync - Knowledge Base

## Architecture Overview
- Adapter system description
- CLI layer structure
- Config management

## Supported Tools
| Tool | Types | Source Dir | Target Dir |

## Commands Reference
| Command | Description | Example |

## Adapter Implementation
- How to add new adapters
- Required interfaces

## Configuration
- ai-rules-sync.json structure
- Local/private rules

## Changelog
- Recent significant changes
```

## Output

After running this skill:
- KNOWLEDGE_BASE.md is created or updated
- Changes reflect current codebase state
- Documentation is accurate and complete
