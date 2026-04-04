---
name: gitbook-assistant
description: Validates GitBook markdown syntax, helps create properly formatted blocks, and ensures documentation quality
---

# GitBook Assistant Skill

## When to Use

This skill automatically assists when:
- Editing or creating markdown documentation files in this repository
- User asks about GitBook syntax or block types
- Validation of GitBook-specific blocks is needed
- Creating new documentation content with GitBook features
- Reviewing documentation for syntax errors or improvements

## Core Capabilities

### 1. Syntax Validation

Check documentation for proper GitBook syntax:
- Block opening/closing: `{% blockType %}...{% endblockType %}`
- Block type validity against official GitBook spec
- Required parameters for each block type
- Proper nesting rules
- LaTeX/KaTeX math syntax
- OpenAPI block configuration

### 2. Block Assistance

Help create and insert properly formatted blocks:
- Suggest appropriate block types for user intent
- Generate correctly formatted block syntax
- Provide examples from templates
- Explain block parameters and options

### 3. Content Enhancement

Improve documentation quality:
- Check for missing code examples
- Verify consistent terminology usage
- Suggest appropriate block types for content
- Validate accessibility considerations
- Ensure proper heading hierarchy

### 4. Reference Lookup

Access comprehensive GitBook format documentation:
- Full block type reference
- Syntax examples for all blocks
- Advanced features (variables, expressions, conditional content)
- OpenAPI extensions and configuration
- Best practices and limitations

## Validation Process

When validating GitBook content:

1. **Block Syntax Check**
   - Verify all blocks have proper opening/closing tags
   - Check block type names match official GitBook blocks
   - Validate no orphaned tags

2. **Parameter Validation**
   - Check required parameters are present
   - Verify parameter syntax and values
   - Validate URL formats for embedded content

3. **Nesting Rules**
   - Ensure blocks are nested according to GitBook rules
   - Check that content blocks don't violate nesting restrictions

4. **Special Syntax**
   - LaTeX: Verify proper `$...$` or `$$...$$` wrapping and valid LaTeX commands
   - OpenAPI: Check valid paths and methods
   - Variables: Validate `{{ }}` syntax and variable names
   - Expressions: Check JavaScript expression syntax

5. **Accessibility**
   - Images have alt text
   - Tables have appropriate column types
   - Headings follow proper hierarchy

## Common Block Types Quick Reference

**Content Blocks:**
- `{% hint style="info|warning|danger|success" %}` - Callout boxes
- `{% tabs %}` / `{% tab title="..." %}` - Tabbed content
- `{% code %}` - Code blocks with syntax highlighting
- `{% embed url="..." %}` - Embedded content

**Structural Blocks:**
- `{% swagger %}` / `{% openapi %}` - API documentation
- `{% stepper %}` / `{% step %}` - Step-by-step guides ⚠️ **CRITICAL: No indentation inside steps**
- `{% cards %}` / `{% card %}` - Card layouts
- `{% columns %}` - Multi-column layouts

**Interactive Blocks:**
- `{% expand title="..." %}` - Collapsible content (or HTML `<details>`)
- `{% file src="..." %}` - File attachments

**Nesting Restrictions:**
- ⚠️ `{% tabs %}` **cannot** be nested inside `<details>` - GitBook does not support this

**Advanced Features:**
- Variables: `{{ space.vars.variableName }}`
- Expressions: `{{ user.email || "guest" }}`
- Conditional: `{% if condition %}...{% endif %}`
- Reusable: `{% content ref="..." %}`

## Resources Available

### Full Reference Documentation
`resources/gitbook-format-reference.md` - Comprehensive reference for all GitBook blocks, syntax, and advanced features (~8k tokens, load only when detailed lookup needed)

### Block Templates
`resources/templates/` - Pre-formatted templates for common blocks:
- hint.md - Callout boxes
- tabs.md - Tabbed content
- code-block.md - Code examples
- openapi.md - API documentation
- stepper.md - Step-by-step guides
- expand.md - Collapsible sections

## Usage Examples

### Example 1: User asks "How do I add a warning callout?"

Response approach:
1. Recognize this needs a hint block with warning style
2. Access template from `resources/templates/hint.md`
3. Provide formatted syntax with example:

```markdown
{% hint style="warning" %}
Your warning message here
{% endhint %}
```

### Example 2: Validating existing documentation

When reviewing a file:
1. Scan for all `{% %}` blocks
2. Check each block type is valid
3. Verify all blocks are properly closed
4. Check parameters match requirements
5. Report any issues with line numbers and suggested fixes

### Example 3: Creating new guide

When user wants to create a new guide:
1. Suggest appropriate block types for content structure
2. Provide templates for common patterns
3. Ensure proper heading hierarchy
4. Add code examples with syntax highlighting
5. Include hints for important information

## Error Detection

Common errors to catch:
- Unclosed blocks: `{% hint %}` without `{% endhint %}`
- Invalid block types: `{% note %}` (should be `{% hint %}`)
- Missing required parameters: `{% tab %}` without `title="..."`
- Invalid LaTeX: `$x * y$` (should be `$x \cdot y$`)
- Broken nesting: code blocks inside other code blocks, `{% tabs %}` inside `<details>`
- **Indentation inside stepper steps** - causes unwanted code block rendering
- Missing alt text on images
- Invalid OpenAPI paths or methods
- Missing or malformed frontmatter

## Critical Formatting Rules

**MUST follow these rules to prevent GitBook rendering errors:**

1. **No indentation inside stepper steps** - GitBook creates unwanted code blocks from indented content
2. **Always close tags** - `{% endstep %}`, `{% endhint %}`, `{% endtab %}`, `</details>`
3. **Use proper frontmatter** - YAML frontmatter at top of file with `---` delimiters, including `title` and `description` fields
4. **Code blocks need wrapper** - Use `{% code title="..." %}` for titles, not just triple backticks
5. **No tabs in details** - `{% tabs %}` cannot be nested inside `<details>` elements

## Frontmatter Format

**REQUIRED: All documentation files must use frontmatter for titles, NOT H1 headers**

Proper frontmatter format:
```yaml
---
title: Page Title Here
description: Brief description of the page content
---
```

Example:
```yaml
---
title: How to Create Compressed Accounts
description: Guide to create compressed accounts in Solana programs with full code examples.
---
```

**Do NOT use H1 headers (`#`) for page titles.** The `title` field in frontmatter sets the page title in GitBook.

## Best Practices

When working with GitBook documentation:
1. **Page titles**: Always use frontmatter `title` field, never H1 for page titles
2. **Frontmatter**: Include both `title` and `description` fields in YAML frontmatter
3. **Heading hierarchy**: H1 for major sections (Overview, Next Steps), H2 in steppers and subsections, H3-H4 for subsections of H2
4. **Code blocks**: Always specify language for syntax highlighting
5. **Hints**: Use appropriate style (info/warning/danger/success)
6. **Links**: Use relative paths for internal docs
7. **Math**: Use proper LaTeX syntax with `\cdot`, `\pi`, etc.
8. **Accessibility**: Always include alt text for images
9. **Consistency**: Match existing documentation style

## Integration with Repository

This skill works alongside:
- [CLAUDE.md](../../CLAUDE.md) - Local writing standards
- [index.md](../../index.md) - Documentation index
- Writing guidelines in repository

When invoked, prioritize:
1. Technical accuracy over style
2. GitBook syntax correctness
3. Consistency with existing documentation
4. Accessibility and usability
5. Clear, concise explanations

## Progressive Resource Loading

To optimize context usage:
1. **First invoke**: Load this SKILL.md file only (~2k tokens)
2. **If validation needed**: Scan file with regex patterns (minimal context)
3. **If specific block lookup needed**: Load relevant template (~100 tokens)
4. **If comprehensive reference needed**: Load full format reference (~8k tokens)

Only load the full reference when user asks specific questions about advanced features or when detailed syntax lookup is required.
