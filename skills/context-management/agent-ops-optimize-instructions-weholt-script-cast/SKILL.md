---
name: agent-ops-optimize-instructions
description: "Optimize agent instruction files by extracting sections into separate files and referencing them. Reduces context size while preserving information."
category: utility
invokes: [agent-ops-project-sections, agent-ops-interview]
invoked_by: [User request]
state_files:
  read: [focus.md, constitution.md]
  write: [focus.md]
---

# Instruction File Optimization Workflow

## Purpose

Optimize agent or instruction files (AGENTS.md, copilot-instructions.md, SKILL.md, etc.) by:

1. Identifying logical sections that can be extracted
2. Moving verbose content to separate reference files
3. Replacing with concise summaries and links
4. Reducing total context size while preserving information

This helps keep prompt context within token limits while maintaining comprehensive guidance.

## When to Use

- Instruction file exceeds recommended size (~2000 lines)
- File contains large code examples or detailed procedures
- Multiple sections could be shared across files
- Agent consistently runs out of context
- Preparing instructions for smaller context models

## Optimization Strategies

### Strategy 1: Section Extraction

Extract large, self-contained sections into reference files.

**Before:**
```markdown
# AGENTS.md

## API Guidelines
{500 lines of detailed API guidelines}

## Testing Patterns
{300 lines of testing examples}
```

**After:**
```markdown
# AGENTS.md

## API Guidelines
See: [api-guidelines.md](.github/reference/api-guidelines.md)
Key points: REST conventions, error handling, versioning.

## Testing Patterns  
See: [testing-patterns.md](.github/reference/testing-patterns.md)
Key points: pytest fixtures, mocking, coverage targets.
```

### Strategy 2: Example Consolidation

Move detailed examples to reference files, keep summaries inline.

**Before:**
```markdown
### Example: Complex Query
```python
def complex_query(db, filters, pagination, sorting):
    # 50 lines of example code
    ...
```
```

**After:**
```markdown
### Example: Complex Query
See: [examples/complex-query.py](.github/reference/examples/complex-query.py)
Pattern: Filter → Paginate → Sort → Execute
```

### Strategy 3: Conditional Loading

Mark sections as "load on demand" for agents that support it.

```markdown
## Advanced Configuration
<!-- LOAD_ON_DEMAND: Only load when user asks about configuration -->
See: [advanced-config.md](.github/reference/advanced-config.md)
```

### Strategy 4: Tiered Detail

Keep high-level summary inline, link to detailed version.

```markdown
## Error Handling

**Quick reference:** Try/catch, log, return Result type.

**Full guide:** [error-handling.md](.github/reference/error-handling.md)
```

## Procedure

### Phase 1: Analysis

1. **Measure current size**: Count lines, estimate tokens
2. **Identify section boundaries**: Headers, code blocks, tables
3. **Classify sections** by extraction potential:
   - ✅ **Extract**: Large (>50 lines), self-contained, reference-style
   - ⚠️ **Consider**: Medium (20-50 lines), may need context
   - ❌ **Keep**: Small (<20 lines), critical, frequently referenced
4. **Check for duplication**: Same content in multiple files?

### Phase 2: Extraction Planning

For each section marked "Extract":

1. **Choose target location**:
   - `.github/reference/` — General reference docs
   - `.github/reference/examples/` — Code examples
   - `.github/reference/lang-{language}.md` — Language-specific
2. **Draft summary** (2-5 lines) to replace full content
3. **Identify key points** that must stay inline
4. **Plan cross-references** if content is shared

### Phase 3: User Confirmation

Present optimization plan:

```
## Instruction Optimization Plan: AGENTS.md

Current size: 2,450 lines (~98,000 tokens)
Target size: ~800 lines (~32,000 tokens)
Reduction: 67%

### Proposed Extractions

| Section | Lines | Target File | Summary |
|---------|-------|-------------|---------|
| API Guidelines | 520 | reference/api-guidelines.md | REST conventions, errors |
| Python Patterns | 380 | reference/lang-python.md | pytest, typing, logging |
| Code Examples | 450 | reference/examples/ | 12 example files |

### Sections to Keep Inline
- Core workflow (critical path)
- Quick reference tables
- Navigation links

Proceed? [Y]es / [E]dit plan / [C]ancel
```

### Phase 4: Execution

1. **Create reference directory** if needed
2. **Extract sections** to target files:
   - Copy full content
   - Add header with source reference
   - Format as standalone document
3. **Update source file**:
   - Replace with summary + link
   - Preserve header structure
   - Add "See: [file](path)" references
4. **Validate links**: Ensure all references resolve

### Phase 5: Verification

1. **Check file sizes**: Source reduced, references created
2. **Validate markdown**: No broken links, proper formatting
3. **Test with agent**: Verify instructions still work
4. **Report results**:

```
✅ Optimization Complete

Before: 2,450 lines (98k tokens)
After: 812 lines (32k tokens)
Reduction: 67%

Created reference files:
- .github/reference/api-guidelines.md (520 lines)
- .github/reference/lang-python.md (380 lines)
- .github/reference/examples/ (12 files)

The instruction file now fits comfortably in standard context windows.
```

## Reference File Template

When creating extracted reference files:

```markdown
---
title: {Section Title}
extracted_from: {source file path}
extracted_date: {YYYY-MM-DD}
---

# {Section Title}

{Full content from original section}

---

*This file was extracted from [{source}]({path}) to optimize context size.*
```

## Size Guidelines

| File Type | Recommended Max | Action if Exceeded |
|-----------|-----------------|-------------------|
| AGENTS.md | 1,000 lines | Extract to references |
| SKILL.md | 500 lines | Extract examples |
| copilot-instructions.md | 500 lines | Use skill references |
| Prompt files | 100 lines | Keep focused |

## Integration with Project Sections

Use `agent-ops-project-sections` to:
- Identify which instruction sections map to which code sections
- Extract language-specific guidance to appropriate reference files
- Scope instructions to relevant project areas

## Completion Criteria

- [ ] Source file size reduced to target
- [ ] All extracted content preserved in reference files
- [ ] Links validate (no 404s)
- [ ] Summaries capture key points
- [ ] Agent tested with optimized instructions
- [ ] Size reduction reported

## Anti-patterns (avoid)

- ❌ Extracting critical workflow steps (keep inline)
- ❌ Creating too many tiny files (consolidate related content)
- ❌ Losing context between extracted sections
- ❌ Breaking cross-references
- ❌ Removing all examples (keep 1-2 inline for quick reference)

## Examples

### Example: Optimizing copilot-instructions.md

**Before analysis:**
- 1,847 lines
- Contains: Python guide (400 lines), TypeScript guide (350 lines), C# guide (380 lines)

**After optimization:**
- 412 lines (main file)
- Created: `lang-python.md`, `lang-typescript.md`, `lang-csharp.md`
- Main file contains summaries + links to language guides

**User benefit:** Instructions now fit in 16k context window instead of requiring 64k+.
