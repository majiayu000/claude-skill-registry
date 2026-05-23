---
name: skill-writing
description: Create new Claude Code skills following best practices including optimal descriptions, progressive disclosure, proper structure, and testing guidelines. Use when creating new skills or skill templates.
version: 1.0.0
---

# Skill Writing

## Purpose

Guide the creation of new Claude Code skills following official best practices to ensure optimal performance, discoverability, and maintainability.

## Quick Start Workflow

### Step 1: Identify the Gap

**Ask:** Does Claude really need this skill?

```bash
# Test Claude's baseline performance WITHOUT the skill
# - Can Claude already do this task reasonably well?
# - What specific knowledge/capability is missing?
# - Will a skill genuinely improve results?
```

**Only create a skill if:**

- ✅ Claude lacks specific domain knowledge
- ✅ Task requires exact procedures or formats
- ✅ Performance improvement is measurable
- ❌ Claude can already handle it well
- ❌ Only saves a few minutes
- ❌ Task is too variable/creative

### Step 2: Create Evaluations First

**Before writing extensive documentation:**

```python
# Create 3+ test scenarios
evaluations = [
    {
        "input": "Process this PDF with forms",
        "expected": "Extracted form data in JSON format",
        "baseline_performance": "fails to extract structured data"
    },
    {
        "input": "Generate chart from spreadsheet",
        "expected": "Bar chart with proper labels",
        "baseline_performance": "creates chart but missing labels"
    },
    # Add more scenarios...
]
```

**Test baseline:** Run scenarios without skill, measure gaps

### Step 3: Write Minimal SKILL.md

**Keep under 500 lines**

```bash
# Create skill directory
mkdir -p ~/.claude/skills/my-skill

# Create SKILL.md
touch ~/.claude/skills/my-skill/Skill.md
```

**Start with this template:**

```markdown
---
name: processing-pdfs
description: Extract text, tables, and forms from PDF files including scanned documents. Use when working with PDFs or document extraction tasks.
version: 1.0.0
---

# PDF Processing

## Purpose

[One sentence: what this skill does]

## Workflow

### Step 1: [Action]

\`\`\`bash

# Concrete command

\`\`\`

### Step 2: [Action]

[Clear instructions]

## Examples

[2-3 input/output examples]
```

### Step 4: Test with Fresh Instances

```bash
# Open new Claude Code session
# Test skill by triggering scenarios
# Observe where Claude struggles
# Note which files get accessed
```

### Step 5: Iterate Based on Usage

```markdown
# Refinement cycle:

1. Observe real usage patterns
2. Identify missing information
3. Add only what's needed
4. Test again
5. Repeat until evaluations pass
```

## Skill Structure Requirements

### Directory Structure

```
skill-name/                    # Use gerund: verb + -ing
├── Skill.md                   # Required (capital S)
├── REFERENCE.md               # Optional (large reference material)
├── TEMPLATE.md                # Optional (output templates)
└── scripts/                   # Optional (executables)
    └── helper.py
```

### YAML Frontmatter (Required)

```yaml
---
name: processing-pdfs # Gerund form, lowercase-with-hyphens, max 64 chars
description: Extract text, tables, and forms from PDF files including scanned documents. Use when working with PDFs or document extraction tasks. # Max 1024 chars, third person, specific
version: 1.0.0 # SemVer format
dependencies: python>=3.8, pdfplumber>=0.9.0 # Optional, list required packages
---
```

**Naming Rules:**

- ✅ Use gerund form (verb + -ing): `processing-pdfs`, `analyzing-spreadsheets`
- ✅ Max 64 characters
- ✅ Lowercase letters, numbers, hyphens only
- ❌ Avoid vague names: `helper`, `utils`, `tool`

**Description Rules:**

- ✅ Third person: "Extracts text from PDFs"
- ❌ First/second person: "I can extract" or "You can use"
- ✅ Specific: "Extract text, tables, and forms from PDF files"
- ❌ Vague: "Helps with documents"
- ✅ Include WHAT it does: "Extracts text, tables, forms"
- ✅ Include WHEN to use: "Use when working with PDFs"
- ✅ Include key terms: "PDF", "document extraction", "tables"

### Good vs Bad Descriptions

```yaml
# ❌ Bad - Vague, first person, no triggers
description: I help you process different types of files and documents.

# ❌ Bad - Too generic, missing context
description: Processes data efficiently.

# ❌ Bad - Second person, unclear
description: You can use this to work with files.

# ✅ Good - Specific, third person, clear triggers
description: Extract text, tables, and forms from PDF files including scanned documents. Use when working with PDFs or document extraction tasks.

# ✅ Good - Clear capability and context
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing tabular data or Excel files.
```

## Content Organization

### Progressive Disclosure Pattern

**Keep SKILL.md under 500 lines for optimal performance (target: under 300 lines for complex skills)**

#### Directory Structure

```
skill-name/
├── SKILL.md                      # Main file (always loaded, <500 lines)
└── references/                   # On-demand detailed content
    ├── WORKFLOW-STEPS.md         # Detailed step-by-step procedures
    ├── TROUBLESHOOTING.md        # Error handling and edge cases
    ├── TEMPLATE-EXAMPLES.md      # Templates and code examples
    └── [DOMAIN-SPECIFIC].md      # Skill-specific detailed content
```

#### SKILL.md Structure (Always Loaded)

```markdown
## Workflow (Quick Summary)

### Core Steps

1. **Step Name**: Brief description of what to do
2. **Step Name**: Brief description of what to do
   [...concise steps...]

**For detailed step-by-step workflow with commands and examples:**

\`\`\`
Read `~/.claude/skills/[skill-name]/references/WORKFLOW-STEPS.md`
\`\`\`

Use when: Performing the task, need specific commands, or understanding each step
```

#### Loading Guidance Format

Always include explicit loading instructions with "Use when" context:

```markdown
**For [detailed topic]:**

\`\`\`
Read `~/.claude/skills/[skill-name]/references/[FILENAME].md`
\`\`\`

Use when: [specific scenario requiring this content]
```

#### What to Extract to references/

| Content Type       | Reference File         | Extract When                   |
| ------------------ | ---------------------- | ------------------------------ |
| Detailed workflows | WORKFLOW-STEPS.md      | Steps exceed 20 lines          |
| Troubleshooting    | TROUBLESHOOTING.md     | >5 error scenarios             |
| Templates/examples | TEMPLATE-EXAMPLES.md   | Complex output formats         |
| Domain checks      | [DOMAIN]-CHECKS.md     | Language/tool-specific details |
| Validation rules   | VERIFICATION-CHECKS.md | Detailed verification criteria |

#### Example: Before and After

**Before (680 lines - too long):**

```markdown
## Workflow

### Step 1: Discovery

[50 lines of detailed commands and examples]

### Step 2: Extraction

[80 lines of detailed procedures]
...
```

**After (200 lines - optimal):**

```markdown
## Workflow (Quick Summary)

### Core Steps

1. **Discovery**: Identify files using grep/glob patterns
2. **Extraction**: Read source, copy exact signatures
3. **Documentation**: Use templates, follow patterns
4. **Verification**: Check accuracy against source

**For detailed workflow with commands and verification checklists:**
\`\`\`
Read `~/.claude/skills/my-skill/references/WORKFLOW-STEPS.md`
\`\`\`
```

#### Reference File Guidelines

- ✅ Keep references ONE level deep (SKILL.md → references/FILE.md)
- ✅ Use ALL CAPS for reference filenames
- ✅ Include complete, standalone content (don't reference other references)
- ✅ Start each reference with brief context of what it contains
- ❌ Don't nest references (references/A.md → references/B.md)
- ❌ Don't duplicate content between SKILL.md and references

### File Naming Conventions

```
✅ Good:
- Skill.md (capital S, required)
- REFERENCE.md (all caps for supporting docs)
- TEMPLATE.md (all caps)
- FORMS.md (all caps)

❌ Bad:
- skill.md (lowercase s)
- reference.txt (wrong extension)
- my_template.md (underscores)
```

## Instruction Clarity

### Sequential Workflows

```markdown
## Workflow

### Step 1: Validate Input

\`\`\`bash

# Check file exists

test -f document.pdf || echo "File not found"
\`\`\`

### Step 2: Extract Text

\`\`\`python
import pdfplumber
with pdfplumber.open('document.pdf') as pdf:
text = pdf.pages[0].extract_text()
\`\`\`

### Step 3: Verify Output

Expected format:
\`\`\`json
{
"pages": 5,
"text": "extracted content..."
}
\`\`\`
```

### Concrete Examples Pattern

**Provide 2-3 examples minimum:**

```markdown
## Examples

### Example 1: Simple Text Extraction

**Input:**
\`\`\`
document.pdf (invoice)
\`\`\`

**Output:**
\`\`\`json
{
"invoice_number": "INV-001",
"amount": "$100.00",
"date": "2024-01-01"
}
\`\`\`

### Example 2: Table Extraction

**Input:**
\`\`\`
spreadsheet.pdf (financial data)
\`\`\`

**Output:**
\`\`\`json
[
{"month": "Jan", "revenue": 1000},
{"month": "Feb", "revenue": 1200}
]
\`\`\`
```

### Template Patterns

**When output format matters:**

```markdown
## Output Template

\`\`\`json
{
"field1": "value", // Required
"field2": 123, // Optional, number
"field3": ["array"], // Optional, array of strings
"metadata": { // Required
"timestamp": "ISO8601",
"version": "1.0"
}
}
\`\`\`
```

### Validation Steps

```markdown
## Validation Checklist

After extraction:

- [ ] All required fields present
- [ ] Data types correct
- [ ] Values within expected ranges
- [ ] No parsing errors in logs
```

## Common Pitfalls to Avoid

**Key anti-patterns to watch for:**

- ❌ Offering too many options (pick ONE default approach)
- ❌ Vague descriptions (be specific about what skill does)
- ❌ Deeply nested references (max one level: Skill.md → REFERENCE.md)
- ❌ Inconsistent terminology (choose one term per concept)
- ❌ First/second person (use third person in descriptions)
- ❌ Too much context (Claude knows programming basics)
- ❌ Missing "When NOT to Use" section
- ❌ No concrete examples (need 2-3 minimum)
- ❌ Placeholder values in examples (use realistic values)

**See REFERENCE.md Section 1 for detailed anti-patterns with examples.**

## Code and Script Guidance

**Best practices for code in skills:**

- ✅ Explicit error handling (catch specific exceptions)
- ✅ Configuration comments explain WHY, not WHAT
- ✅ Forward slashes in all paths (cross-platform)
- ✅ Input validation (fail fast with clear errors)
- ✅ Resource cleanup (use context managers)

**See REFERENCE.md Section 2 for detailed code guidance with examples.**

## Testing Guidelines

**Required testing before releasing a skill:**

- ✅ Create 3+ evaluation scenarios first (test-driven approach)
- ✅ Test across models (Haiku, Sonnet, Opus)
- ✅ Fresh instance testing (no prior context)
- ✅ Baseline comparison (prove skill adds value)
- ✅ Real-world validation (actual user tasks)
- ✅ Continuous improvement (iterate based on usage)

**See REFERENCE.md Section 3 for comprehensive testing guidelines.**

## Quality Checklist

Before sharing a skill, verify:

### Core Quality

- [ ] Description includes specific key terms and usage triggers
- [ ] Description written in third person
- [ ] SKILL.md body under 500 lines
- [ ] Additional details in separate reference files
- [ ] Reference files one level deep from SKILL.md
- [ ] Consistent terminology throughout
- [ ] Concrete examples provided (2-3 minimum)
- [ ] Clear workflow steps with verification points

### Naming & Structure

- [ ] Name uses gerund form (verb + -ing)
- [ ] Name max 64 characters, lowercase-with-hyphens
- [ ] Directory named correctly (matches skill name)
- [ ] Skill.md with capital S
- [ ] YAML frontmatter complete (name, description, version)

### Content Quality

- [ ] Only includes info Claude doesn't already know
- [ ] Progressive disclosure pattern used
- [ ] One default approach (not too many options)
- [ ] No time-sensitive information
- [ ] No deeply nested references
- [ ] No vague confidence language

### Code Quality (if applicable)

- [ ] Scripts handle errors explicitly
- [ ] All constants justified in comments
- [ ] Required packages listed and verified available
- [ ] Validation steps for critical operations
- [ ] Forward slashes in all file paths

### Testing

- [ ] At least 3 evaluations created
- [ ] Tested with Haiku, Sonnet, and Opus
- [ ] Real-world usage scenarios validated
- [ ] Fresh instance testing completed
- [ ] Team feedback incorporated

## Resources

- [Official Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skill Template](TEMPLATE.md)
- [Example Skills](EXAMPLES.md)
- [Claude Documentation](https://platform.claude.com/docs)

## Quick Reference

```bash
# Create new skill
mkdir -p ~/.claude/skills/my-skill-name
cd ~/.claude/skills/my-skill-name

# Copy template
cp ~/.claude/skills/skill-writing/TEMPLATE.md ./Skill.md

# Edit frontmatter and content
# Test with fresh Claude instance
# Iterate based on usage
```
