---
name: output-style-audit
description: Validates output-style persona definitions, behavior specifications, and keep-coding-instructions decisions. Use when auditing, reviewing, or improving output-styles, checking persona clarity, validating behavior concreteness, or verifying scope alignment (user vs project). Triggers when user asks about output-style best practices or needs help with persona definition.
allowed-tools: [Read, Grep, Glob, Bash]
# model: inherit
---

## Reference Files

Advanced output-style validation guidance:

- [persona-definition.md](persona-definition.md) - Persona clarity assessment and role definition quality
- [behavior-specification.md](behavior-specification.md) - Behavior concreteness and actionability validation
- [coding-instructions-decision.md](coding-instructions-decision.md) - Decision matrix for keep-coding-instructions field
- [scope-alignment.md](scope-alignment.md) - User vs project scope selection guidance
- [examples.md](examples.md) - Good vs poor output-style comparisons and full audit reports

---

# Output-Style Auditor

Validates output-style configurations for persona clarity, behavior concreteness, and scope appropriateness.

## Quick Start

**Basic audit workflow**:

1. Read output-style file
2. Assess persona definition clarity
3. Validate behavior specification concreteness
4. Check keep-coding-instructions decision
5. Verify scope alignment (user vs project)
6. Generate audit report

**Example usage**:

```text
User: "Audit my content-editor style"
→ Reads output-styles/content-editor.md
→ Validates persona, behaviors, coding-instructions, scope
→ Generates report with findings and recommendations
```

## Output-Style Audit Checklist

### Critical Issues

Must be fixed for style to function correctly:

- [ ] **Valid markdown file** - Proper frontmatter and structure
- [ ] **name field present** - Style name defined
- [ ] **Persona defined** - Clear WHO Claude becomes
- [ ] **At least 3 concrete behaviors** - Actionable instructions
- [ ] **keep-coding-instructions decision** - Explicit true/false or omitted
- [ ] **Description contains trigger phrases** - Discoverability optimized

### Important Issues

Should be fixed for optimal style performance:

- [ ] **Persona is specific** - Clear role, not vague
- [ ] **Behaviors are actionable** - Concrete, not abstract
- [ ] **keep-coding-instructions matches role** - Engineering=true, other=false
- [ ] **Scope is appropriate** - User (personal) or project (team)
- [ ] **5-10 behaviors** - Not too few (vague) or too many (overwhelming)
- [ ] **Description is comprehensive** - 200-400 chars with use cases

### Nice-to-Have Improvements

Polish for excellent style quality:

- [ ] **Persona has examples** - Sample scenarios or tone indicators
- [ ] **Behaviors have if/then logic** - Conditional instructions
- [ ] **Description has keywords** - Optimized for discovery
- [ ] **File size reasonable** - <200 lines focused persona
- [ ] **Context economy** - Concise without sacrificing clarity

## Audit Workflow

### Step 1: Read Output-Style File

Identify the output-style file to audit:

```bash
# Single style (user scope)
Read ~/.claude/output-styles/content-editor.md

# Single style (project scope)
Read .claude/output-styles/qa-tester.md

# Find all styles
Glob ~/.claude/output-styles/*.md
Glob .claude/output-styles/*.md
```

### Step 2: Assess Persona Definition

**Check persona section**:

```markdown
## Persona

You are a professional content editor with expertise in clarity and readability.
```

**Quality criteria**:

- **Specific vs Vague**: "content editor" (specific) vs "helper" (vague)
- **Clear role**: Defines WHO Claude becomes
- **Concrete identity**: Professional/expert/specialist (not abstract)
- **Scope boundaries**: What this persona does/doesn't do

**Common issues**:

- Vague persona: "You are helpful and knowledgeable"
- Missing persona: No persona section
- Too abstract: "You embody excellence"

See [persona-definition.md](persona-definition.md) for assessment methodology.

### Step 3: Validate Behavior Specification

**Check behaviors/instructions**:

```markdown
## Behaviors

1. Prioritize clarity over cleverness in all writing
2. Use active voice unless passive is necessary
3. Break long sentences into shorter ones
4. Remove jargon and explain technical terms
5. Add section headers for readability
```

**Quality criteria**:

- **Concrete vs Abstract**: "Use active voice" (concrete) vs "Be clear" (abstract)
- **Actionable**: Can be implemented directly
- **Numbered steps**: Sequential or prioritized
- **If/then logic** (optional): Conditional instructions

**Common issues**:

- Abstract behaviors: "Be helpful and friendly"
- Too few (<3): Insufficient guidance
- Too many (>15): Overwhelming, unfocused
- No behaviors: Missing section

See [behavior-specification.md](behavior-specification.md) for concreteness validation.

### Step 4: Check keep-coding-instructions Decision

**Field presence**:

```yaml
---
name: content-editor
keep-coding-instructions: false # Explicit decision
---
```

**Decision criteria**:

- **Engineering roles** (QA, DevOps, security): `keep-coding-instructions: true`
- **Non-engineering roles** (writer, analyst, teacher): `keep-coding-instructions: false`
- **Omitted**: Defaults to `false` (removes coding instructions)

**Common issues**:

- Engineering role with false: QA tester can't review code
- Non-engineering role with true: Content editor gets coding instructions
- Inconsistent with persona: Mismatch between role and decision

See [coding-instructions-decision.md](coding-instructions-decision.md) for decision matrix.

### Step 5: Verify Scope Alignment

**File location**:

- **User scope**: `~/.claude/output-styles/` (personal styles)
- **Project scope**: `.claude/output-styles/` (team styles)

**Alignment criteria**:

- **Personal use**: User scope, not tracked in git
- **Team use**: Project scope, tracked in git
- **Audience**: Single user vs entire team

**Common issues**:

- Personal style in project scope (pollutes team config)
- Team style in user scope (not shared with team)
- No clear audience definition

See [scope-alignment.md](scope-alignment.md) for selection guidance.

### Step 6: Generate Audit Report

Compile findings into standardized report format (see Report Format section below).

## Style-Specific Validation

### Persona Clarity

**Assessment criteria**:

1. **Role specificity**: Specific profession/role (not generic "helper")
2. **Expertise indication**: Professional/expert/specialist qualifier
3. **Domain clarity**: Area of expertise clearly defined
4. **Identity statement**: Complete "You are X" sentence

**Scoring** (1-10):

- 9-10: Specific role with clear expertise and domain
- 7-8: Clear role with some specificity
- 5-6: Generic role with vague expertise
- 3-4: Very vague role
- 1-2: No clear role or missing persona

### Behavior Concreteness

**Assessment criteria**:

1. **Actionability**: Can be implemented directly
2. **Specificity**: Concrete actions (not "be good")
3. **Count**: 5-10 behaviors (not too few/many)
4. **Structure**: Numbered or bulleted list
5. **Conditional logic** (optional): If/then instructions

**Scoring** (1-10):

- 9-10: All behaviors concrete, actionable, well-structured
- 7-8: Most behaviors concrete, minor vague statements
- 5-6: Mix of concrete and abstract
- 3-4: Mostly abstract behaviors
- 1-2: All abstract or missing

### keep-coding-instructions Appropriateness

**Decision validation**:

**Engineering roles** (should be `true` or omitted for default):

- QA engineer / tester
- DevOps engineer / SRE
- Security analyst / pentester
- Code reviewer
- Technical architect

**Non-engineering roles** (should be `false`):

- Content editor / writer
- Business analyst
- Teacher / tutor
- Project manager
- Data analyst (non-coding)

**Verdict**:

- ✓ Appropriate: Matches role type
- ✗ Inappropriate: Engineering role with false, or non-engineering with true

### Scope Alignment

**Location validation**:

- **User scope** (`~/.claude/output-styles/`): Personal, not in git
- **Project scope** (`.claude/output-styles/`): Team-wide, in git

**Audience assessment**:

- **Personal**: Single user's preference
- **Team**: Shared standard across project

**Verdict**:

- ✓ Aligned: Location matches audience
- ✗ Misaligned: Personal in project or team in user

## Common Issues

### Issue 1: Vague Persona

**Problem**: Generic or abstract persona definition

**Example**:

```markdown
## Persona

You are helpful, knowledgeable, and friendly.
```

**Fix**:

```markdown
## Persona

You are a professional content editor specializing in technical documentation. You prioritize clarity, conciseness, and readability. You have expertise in plain language principles and audience-appropriate communication.
```

### Issue 2: Abstract Behaviors

**Problem**: Behaviors that aren't actionable

**Example**:

```markdown
## Behaviors

- Be helpful
- Provide quality responses
- Use best practices
```

**Fix**:

```markdown
## Behaviors

1. Use active voice unless passive is grammatically necessary
2. Break sentences longer than 25 words into shorter ones
3. Replace jargon with plain language or define technical terms
4. Add section headers every 3-4 paragraphs for scannability
5. Use bullet points for lists of 3+ items
6. Limit paragraphs to 3-5 sentences maximum
```

### Issue 3: Incorrect keep-coding-instructions

**Problem**: Engineering role with `keep-coding-instructions: false`

**Example**:

```yaml
---
name: qa-tester
keep-coding-instructions: false
---
## Persona

You are a QA engineer who reviews code for quality and bugs.
```

**Fix**:

```yaml
---
name: qa-tester
keep-coding-instructions: true
---
## Persona

You are a QA engineer who reviews code for quality, bugs, and test coverage.
```

### Issue 4: Scope Misalignment

**Problem**: Personal style in project scope

**Location**: `.claude/output-styles/my-personal-style.md` (project directory)

**Impact**: Team members get someone's personal preferences

**Fix**: Move to `~/.claude/output-styles/my-personal-style.md` (user directory)

### Issue 5: Missing Trigger Phrases

**Problem**: Description lacks use case triggers

**Example**:

```yaml
---
name: content-editor
description: Edits content
---
```

**Fix**:

```yaml
---
name: content-editor
description: Professional content editor for clarity and readability. Use when editing documentation, improving writing quality, simplifying technical content, or enhancing readability. Triggers on "edit", "improve writing", "make clearer", "simplify content".
---
```

## Report Format

Use this standardized structure for all output-style audit reports:

```markdown
# Output-Style Audit Report: {name}

**Style**: {name}
**File**: {path to style file}
**Scope**: {user/project}
**Audited**: {YYYY-MM-DD HH:MM}

## Summary

{1-2 sentence overview of style and assessment}

## Compliance Status

**Overall**: PASS | NEEDS WORK | FAIL

- **Persona**: ✓/✗ {specific/vague}
- **Behaviors**: ✓/✗ {count} behaviors - {concrete/abstract}
- **keep-coding-instructions**: ✓/✗ {appropriate/inappropriate for role}
- **Scope**: ✓/✗ {aligned/misaligned with audience}
- **Description**: ✓/✗ {comprehensive/insufficient}

## Critical Issues

{Must-fix issues that prevent proper functioning}

### {Issue Title}

- **Severity**: CRITICAL
- **Location**: {section}:{line}
- **Issue**: {description}
- **Fix**: {specific remediation}

## Important Issues

{Should-fix issues that impact quality}

## Nice-to-Have Improvements

{Polish items for excellence}

## Recommendations

1. **Critical**: {must-fix for correctness}
2. **Important**: {should-fix for quality}
3. **Nice-to-Have**: {polish for excellence}

## Next Steps

{Specific actions to improve style quality}
```

## Integration with audit-coordinator

**Invocation pattern**:

```text
User: "Audit my output-style"
→ audit-coordinator invokes audit-output-styleor
→ audit-output-styleor performs specialized validation
→ Results returned to audit-coordinator
→ Consolidated with evaluator findings
```

**Sequence**:

1. audit-output-styleor (primary) - Style-specific validation
2. evaluator (secondary) - General structure validation
3. test-runner (optional) - Effectiveness testing

**Report compilation**:

- audit-output-styleor findings (persona, behaviors, coding-instructions, scope)
- evaluator findings (markdown, frontmatter, structure)
- Unified report with reconciled priorities

## Examples

### Example 1: Good Style (content-editor)

**Status**: PASS

**Strengths**:

- Persona: Specific role (content editor) with clear expertise
- Behaviors: 8 concrete, actionable behaviors
- keep-coding-instructions: false (appropriate for non-engineering role)
- Scope: User scope (personal preference)

**Score**: 9/10 - Excellent style design

### Example 2: Style Needs Work

**Status**: NEEDS WORK

**Issues**:

- Persona: Vague ("helpful assistant")
- Behaviors: 2 abstract behaviors ("be clear", "be helpful")
- keep-coding-instructions: true (inappropriate for content editing role)
- Scope: Project scope (should be user scope for personal style)

**Critical fixes**:

1. Define specific persona with clear role
2. Add 6-8 concrete behaviors
3. Change keep-coding-instructions to false
4. Move to user scope

**Score**: 4/10 - Requires significant improvement

See [examples.md](examples.md) for complete audit reports.

---

For detailed guidance on each validation area, consult the reference files linked at the top of this document.
