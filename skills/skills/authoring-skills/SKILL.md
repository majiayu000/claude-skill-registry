---
name: authoring-skills
description: Use when creating new skills, improving existing skills, or when the user requests help with skill authoring. Creates optimized Claude Code skills (SKILL.md files) following official best practices for descriptions, structure, content patterns, and validation.
---

# Skill Authoring

For foundational instruction authoring principles (token economics, imperative language, formatting, anti-patterns), invoke the `authoring-prompts` skill first. This skill focuses on skill-specific requirements.

Create Claude Code skills that produce consistent, deterministic agent behavior. Optimize for LLM execution efficiency, not human aesthetics.

## Metadata Requirements

### Name Field

Requirements:
- Maximum 64 characters
- Lowercase letters, numbers, and hyphens only
- Cannot contain XML tags
- Cannot contain reserved words: "anthropic", "claude"

Naming convention: Use gerund form (verb + -ing) for clarity.

Good: `processing-pdfs`, `analyzing-spreadsheets`, `writing-tests`
Avoid: `helper`, `utils`, `tools`

### Description Field

Requirements:
- Maximum 1024 characters
- Must be non-empty
- Cannot contain XML tags
- Include BOTH what the skill does AND when to use it

**The description determines skill invocation.** Claude Code selects skills based on description relevance. Frontload invocation triggers with clear, action-oriented language.

#### Effective Description Structure

**Pattern 1: Imperative invocation trigger first**

Frontload with directive action when the skill should be invoked proactively:

```yaml
# Strong - imperative trigger first
description: Use when working with .cs files, .NET projects, implementing C# features, advising on C#/.NET architecture and patterns, or answering questions about C#/.NET development. Covers async patterns, dependency injection, LINQ, and testing conventions.

# Weak - buried trigger
description: C# and .NET patterns for async, DI, LINQ, and testing. Use when working with .cs files or .NET projects.
```

**Pattern 2: Descriptive capability with explicit triggers**

For skills invoked based on context, state capabilities then enumerate clear trigger conditions:

```yaml
# Strong - clear domain and triggers
description: Ruby on Rails conventions for models, controllers, routes, and testing. Use when working with Rails projects, ActiveRecord models, or Rails-specific patterns.

# Weak - vague triggers
description: Helps with Ruby on Rails development tasks.
```

**Pattern 3: "Invoke when" for foundational skills**

For skills that should be loaded before other operations, make invocation mandatory:

```yaml
# Strong - explicit invocation requirement
description: Invoke this skill first when authoring any AI agent instructions. Foundational principles for writing LLM instructions (skills, CLAUDE.md, rules, commands). Covers token economics, imperative language, formatting, emphasis modifiers, and anti-patterns.

# Weak - passive suggestion
description: Foundational principles for writing instructions. Reference when creating skills or documentation.
```

#### Common Anti-Patterns

Vague scope:
- ❌ `description: Helps with documents`
- ✓ `description: Extract text and tables from PDF files. Use when working with PDFs, forms, or document extraction.`

Buried triggers:
- ❌ `description: C# patterns including async and LINQ. Use when writing C# code.`
- ✓ `description: Use when working with .cs files or C# projects. Covers async patterns, LINQ, DI, and testing.`

Generic verbs without specificity:
- ❌ `description: Assists with testing activities`
- ✓ `description: Write xUnit tests with Moq and Bogus. Use when creating unit tests or integration tests in C#.`

Multiple trigger conditions without clear enumeration:
- ❌ `description: Use for various Rails tasks`
- ✓ `description: Use when working with Rails projects, ActiveRecord models, controllers, routes, or Rails testing.`

## Structure and Organization

### Keep SKILL.md Concise

Target: Under 500 lines for optimal performance

When approaching this limit:
- Split content into separate reference files
- Use progressive disclosure patterns
- Move detailed reference material to bundled files

### Progressive Disclosure Patterns

SKILL.md serves as an overview that points Claude to detailed materials as needed.

**Pattern 1: Reference files for advanced features**

```markdown
## Quick start
[Basic instructions inline]

## Advanced features
**Form filling**: See [references/forms.md](references/forms.md)
**API reference**: See [references/api.md](references/api.md)
```

**Pattern 2: Domain-specific organization**

When skills cover multiple domains, organize content by domain to avoid loading irrelevant context.

```
skill-name/
├── SKILL.md (overview and navigation)
└── references/
    ├── domain-a.md
    ├── domain-b.md
    └── domain-c.md
```

**Critical rules:**
- Keep references one level deep from SKILL.md (no nested references)
- For reference files longer than 100 lines, include table of contents at top
- Make clear in SKILL.md when to read each reference file

### Directory Structure

```
skill-name/
├── SKILL.md              # Required: overview and core instructions
├── scripts/              # Executable code (executed, not loaded into context)
├── references/           # Documentation (loaded as needed)
└── templates/            # Templates and examples
```

## Content Patterns

### Template Pattern

Provide templates for output format. Match strictness to requirements.

For strict requirements (API responses, data formats):
```markdown
ALWAYS use this exact template structure:
[template here]
```

For flexible guidance:
```markdown
Here is a sensible default format, adjust as needed:
[template here]
```

### Examples Pattern

Provide concrete input/output pairs for tasks where output quality depends on seeing examples.

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation
```

**Example 2:**
Input: Fixed date display bug
Output:
```
fix(reports): correct date formatting

Use UTC timestamps consistently
```
```

Include 3-5 diverse examples covering different scenarios and edge cases.

### Workflow Pattern

Break complex operations into clear sequential steps. For particularly complex workflows, provide a checklist.

```markdown
## Multi-step workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Analyze input (run analyze.py)
- [ ] Step 2: Create mapping (edit config.json)
- [ ] Step 3: Validate (run validate.py)
- [ ] Step 4: Execute (run process.py)
- [ ] Step 5: Verify output
```

**Step 1: Analyze input**
[Detailed instructions for step 1]

**Step 2: Create mapping**
[Detailed instructions for step 2]
```

### Feedback Loop Pattern

For quality-critical operations, implement validation cycles:

```markdown
1. Perform action
2. **Validate immediately**: Run validation script
3. If validation fails:
   - Review error messages
   - Fix issues
   - Run validation again
4. **Only proceed when validation passes**
5. Continue to next step
```

### Conditional Workflow Pattern

Guide through decision points:

```markdown
1. Determine the task type:
   **Creating new?** → Follow "Creation workflow"
   **Editing existing?** → Follow "Editing workflow"

2. Creation workflow:
   [Steps for creation]

3. Editing workflow:
   [Steps for editing]
```

## Quality Requirements

### No Time-Sensitive Information

Avoid information that will become outdated.

Bad: "If doing this before August 2025, use old API"

Good: Use "old patterns" section with details/summary tags:
```markdown
## Current method
[Current approach]

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
[Historical context]
</details>
```

### Grounding and Verification

Use techniques from prompt engineering to reduce hallucinations:

- Allow Claude to say "I don't know" explicitly
- Ask for direct quotes from documents before analysis
- Request citations for claims
- Use validation scripts for verifiable operations

### Consistency Techniques

For consistent outputs:
- Specify exact output format (JSON, XML, templates)
- Provide multiple examples showing desired format
- Use prefill patterns where applicable
- Define success criteria explicitly

## Executable Scripts

When including scripts in skills:

### Script Purpose

Include scripts for operations requiring consistent results. Scripts are more reliable than generated code and save tokens.

Make execution intent clear:
- "Run scripts/analyze.py" (execute the script)
- "See scripts/analyze.py for the algorithm" (read as reference)

### Script Quality

Scripts should:
- Handle errors explicitly, not punt to Claude
- Document all configuration values (no magic numbers)
- Use forward slashes in all paths
- List required packages explicitly

Example with clear error handling:
```python
def process_file(path):
    """Process file, creating if missing."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
```

### Package Dependencies

List required packages in SKILL.md. Verify they're available in the code execution environment.

Note runtime environment constraints:
- Claude API: No network access, no runtime package installation
- Claude.ai: Variable network access depending on settings

## Validation Checklist

Before completing a skill, verify:

**Metadata:**
- [ ] Name follows conventions (lowercase-hyphens, gerund form, under 64 chars)
- [ ] Description frontloads invocation triggers, includes what AND when (under 1024 chars)

**Content:**
- [ ] SKILL.md body under 500 lines
- [ ] Instructions are imperative and specific
- [ ] Examples are concrete and diverse (3-5 examples)
- [ ] No time-sensitive information (or in "old patterns" section)
- [ ] Consistent terminology throughout
- [ ] No deeply nested file references (one level from SKILL.md)

**Structure:**
- [ ] Clear headings establish scope
- [ ] Progressive disclosure used for detailed content
- [ ] Long reference files have table of contents
- [ ] Scripts have clear execution intent
- [ ] Workflows include validation steps

**Quality:**
- [ ] Assumes Claude's intelligence (no obvious explanations)
- [ ] Every sentence changes agent behavior (no fluff)
- [ ] Specific constraints, not vague guidance
- [ ] Success criteria are explicit and testable

**Execution:**
- [ ] All file paths use forward slashes
- [ ] Required packages listed explicitly
- [ ] Error handling is explicit in scripts
- [ ] No assumptions about installed tools
