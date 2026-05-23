---
name: effective-commenting-strategies
description: Use this skill when writing, reviewing, or maintaining code comments. Apply these strategies to ensure comments explain intent rather than repeat code, use maintainable styles, and follow density guidelines. This skill covers comment types, style best practices, and performance considerations.
---

# Effective Commenting Strategies

Good comments explain the "why" behind code, not the "what." Use these strategies to write comments that enhance code maintainability without creating maintenance burden.

## When to Use

- Adding comments to new code
- Reviewing existing comments for quality
- Establishing team commenting standards
- Optimizing comment density for readability
- Handling performance-sensitive code with comments

## Core Principle: Intent Over Repetition

Good comments should:
- **Not repeat code** or explain what the code does
- **Clarify intent** at a higher abstraction level than the code
- **Act as navigation** like book headings or table of contents
- **Help maintenance** by explaining the original programmer's intent
- **Be efficient"—reading one English comment is faster than parsing 20 lines of code

**Rule**: If the code already explains everything, a comment that repeats it provides no value.

## Comment Types

### Marker Comments

**Purpose**: Remind developers of incomplete work (not intended for production)

**Requirements**:
- Use standardized markers (e.g., `***`, `TBD`, `TODO`)
- Make markers mechanically searchable
- Include in release checklist to prevent shipping known defects

**Action**: Search for all markers before release to ensure no incomplete code ships.

### Explanatory Comments

**Purpose**: Explain complex, tricky, or sensitive code

**Strategy**:
- If code is complex enough to need explanation, **refactor the code** first
- Make the code itself clearer
- Then use summary or intent comments if still needed

### Summary Comments

**Purpose**: Condense several lines of code into one or two sentences

**Value**: More valuable than code-repeating comments because readers can scan them faster than reading code

**When to use**: Particularly helpful when non-original authors need to modify code

### Intent Comments

**Purpose**: Explain the purpose of a code section at the intent/problem level

**Level**: Operates more at the problem level than the solution level

**Example**:
- Intent: "Get current employee information"
- Solution/Summary: "Update employeeRecord object"

### Metadata Comments

**Purpose**: Record information that cannot be expressed in code

**Includes**:
- Copyright notices
- Confidentiality statements
- Version numbers
- Design notes
- Requirement references
- Online reference pointers
- Optimization notes
- Tool-required comments (e.g., Javadoc)

## Maintainable Comment Style

### Avoid High-Maintenance Styles

Do not use styles that require manual alignment:

- ❌ **Leader dots** (`...`) connecting variables and descriptions
- ❌ **Asterisk boxes** (`*`) surrounding paragraphs—requires adjusting both sides
- ❌ **Plus-sign underlines** (`+---+`)—requires precise positioning when text length changes

**Principle**: Prefer accurate comments over pretty comments. If maintaining aesthetics requires tedious work, abandon that style.

### Syntax Guidelines

**For Java and C++**:
- **Single-line comments**: Use `//` syntax, keep comments short
- **Multi-line comments**: Use `/* ... */` syntax—easier to maintain than manually wrapped `//` lines

**For emphasis**: Use standard-length lines (via editor macros), not lines that vary with comment length

## Comment Density Guidelines

### Optimal Density

**IBM Research Finding**: Approximately **1 comment per 10 statements** maximizes code clarity

- **Below this density**: Code becomes difficult to understand
- **Above this density**: Readability decreases

### Avoid Quotas

**Do not** enforce rigid standards like "at least 1 comment per 5 lines"

**Reason**: This addresses the symptom (lack of comments) without solving the root cause (unclear code)

### Performance Considerations

**Principle**: Do not avoid comments due to performance concerns (e.g., interpreted environments, network transmission overhead)

**Solution**: Create a separate release build

**Implementation**: Run a tool during the build process to automatically strip comments from the production version

## Pseudocode Programming Process (PPP) Comment Efficiency

When using the Pseudocode Programming Process:

1. **Recognize the pattern**: Effective PPP naturally results in "a comment every few lines"
2. **Understand the nature**: Comment quantity is a side effect of the process, not a goal
3. **Focus on efficiency**: Don't count comments—evaluate whether each comment is effective
4. **Assess sufficiency**: Comments are sufficient if they:
   - Describe **why** the code was written
   - Meet the other standards in this skill

**Conclusion**: If comments explain "why" and meet quality standards, the quantity is adequate—don't worry about the number.