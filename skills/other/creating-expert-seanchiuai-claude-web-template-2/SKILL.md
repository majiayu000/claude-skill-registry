---
name: "Creating Expert"
description: "Create new domain expert with expertise file and workflows. Use when adding new technology or domain area."
tools: Read, Grep, Glob, Write, Edit
model: inherit
---

# Skill: Creating Expert

Generate complete expert structure for a new domain. This is a meta-skill - a tool that builds tools.

## When to Use

- Adding new tech to stack (e.g., "postgres-expert" for Postgres database)
- Creating domain specialist (e.g., "auth-expert" for authentication patterns)
- Splitting existing expert into sub-domains
- Expanding beyond the 4 core experts (convex, nextjs, shadcn, vercel)

## Workflow

### 1. Interview User

Ask clarifying questions:
- **Expert name:** What domain? (kebab-case, e.g., "postgres-expert")
- **Domain description:** One-line summary
- **Initial knowledge sources:** Docs? Agent files? Existing code?
- **Related existing agents:** Build on existing agents?

### 2. Create Directory Structure

```bash
mkdir -p .claude/experts/{expert-name}-expert
```

Create three files:
- `expertise.yaml` - Mental model (initially low confidence)
- `question.md` - Question workflow
- `self-improve.md` - Self-improvement workflow

### 3. Generate Expertise File

Use template from `.claude/experts/_shared/expertise-schema.yaml`:

```yaml
---
expert: "{name}-expert"
domain: "{Domain Description}"
last_updated: "{current-date}"
version: "0.1.0"
confidence: "low"
---

{domain}_patterns:
  - pattern: "{initial pattern from docs/agent}"
    context: "{when this applies}"
    evidence: "{source}"
    learned_from: "Initial setup"
    importance: "medium"
    confidence: "low"

common_issues: []  # To be discovered

key_files:
  primary: "{main config/entry file}"
  common_patterns: []

codebase_conventions: []  # To be discovered

evolution_log:
  - date: "{current-date}"
    change: "Expert created"
    confidence_before: "none"
    confidence_after: "low"
    trigger: "manual creation"

metadata:
  created: "{current-date}"
  self_improve_runs: 0
  last_self_improve: "never"
  questions_answered: 0
```

**Fill with initial patterns** from:
- Existing agent documentation (if exists)
- Official tech docs
- Common best practices
- User-provided knowledge

### 4. Generate Question Prompt

Adapt from existing experts (use convex-expert/question.md as template):

```markdown
---
name: Question {Name} Expert
description: Ask questions about {domain} patterns
argument-hint: [Your question about {domain}]
tools: Read, Grep, Glob
model: inherit
---

# Question: {Name} Expert

Answer questions using accumulated expertise validated against codebase.

## Workflow

### 1. Read Expertise
```
Read: .claude/experts/{name}-expert/expertise.yaml
```

### 2. Validate Against Codebase
```bash
# Domain-specific search patterns
Glob: {domain-files}/*
Grep: {domain-keywords}
Read: {key-files}
```

### 3. Provide Structured Answer
- Direct answer
- Evidence from codebase (file:line)
- Related patterns from expertise
- Confidence level
- Recommendations
```

**Customize:**
- Search patterns for domain (Glob/Grep targets)
- Key files to check
- Domain-specific validation steps

### 5. Generate Self-Improve Prompt

Adapt from convex-expert/self-improve.md:

```markdown
---
name: Self-Improve {Name} Expert
description: Sync {domain} expertise with current codebase
tools: Read, Grep, Glob, Edit
model: inherit
---

# Self-Improve: {Name} Expert

## Workflow

### 1. Read Current Expertise
```
Read: .claude/experts/{name}-expert/expertise.yaml
```

### 2. Explore Codebase
```bash
Glob: {domain-files}/**/*
Read: {key-files}
Grep: {domain-patterns}
```

### 3. Validate Patterns
- Count occurrences (3+ = add/keep)
- Update confidence levels
- Discover new patterns
- Remove obsolete patterns

### 4. Update Expertise
Edit expertise.yaml:
- Add new patterns found
- Update confidence based on validation
- Update file locations
- Add codebase conventions discovered
- Increment version
- Add evolution log entry
```

**Customize:**
- File patterns to explore
- Keywords to search for
- Pattern detection criteria

### 6. Update Dispatcher

Add new expert to `.claude/commands/ask-expert.md`:

```markdown
### {name}
**Domain:** {Domain Description}
**Expertise:** {key areas}
**Use for:** {when to use this expert}
```

Also update `expertMap` in implementation section.

### 7. Run Initial Self-Improvement

Execute the self-improve prompt to populate initial expertise:

```bash
# This will explore codebase and populate expertise.yaml
# with real patterns discovered
```

### 8. Create Agent Reference (Optional)

If there's a corresponding agent, enhance it:

```markdown
---
expertise_file: .claude/experts/{name}-expert/expertise.yaml
---

## Before Starting Any Task
1. Read expertise file
2. Apply patterns
3. Validate & extend
```

## Success Criteria

New expert should have:
- [ ] Directory: `.claude/experts/{name}-expert/`
- [ ] File: `expertise.yaml` with initial patterns
- [ ] File: `question.md` with domain-specific workflow
- [ ] File: `self-improve.md` with exploration logic
- [ ] Updated: `ask-expert.md` dispatcher
- [ ] Tested: Can answer basic questions
- [ ] Populated: Initial self-improve run completed

## Example: Creating "testing-expert"

```bash
# User request: "Create expert for testing patterns"

# 1. Interview
Expert name: testing-expert
Domain: Test automation and quality assurance
Sources: Existing test files, Jest/Vitest docs
Related: Quality checks, CI/CD

# 2. Create structure
mkdir -p .claude/experts/testing-expert

# 3. Generate expertise.yaml
testing_patterns:
  - pattern: "Use describe/it for test structure"
    confidence: "low"
  - pattern: "Mock external dependencies"
    confidence: "low"

key_files:
  config: "vitest.config.ts"
  test_utils: "test/utils.ts"

# 4. Generate question.md
# Customize for test file patterns (Glob: **/*.test.ts)

# 5. Generate self-improve.md
# Customize for test discovery (Grep: "describe(", "test(")

# 6. Update ask-expert.md
Add "testing" to expert map

# 7. Run self-improvement
Execute: testing-expert/self-improve.md
Result: Discovers actual test patterns in codebase

# 8. Test
/ask-expert testing "How should I structure unit tests?"
Returns: Answer based on discovered patterns
```

## Tips

**Start Simple:**
- Begin with 3-5 initial patterns
- Low confidence initially
- Let self-improvement discover rest

**Use Templates:**
- Copy structure from similar expert
- Customize domain-specific parts
- Keep workflow patterns consistent

**Test Early:**
- Run self-improve immediately after creation
- Ask test question to verify it works
- Iterate on search patterns if needed

**Documentation:**
- Add expert to project documentation
- Update CLAUDE.md if significant
- Note what domain it covers

## Common Issues

**Expert doesn't find patterns:**
- Check Glob/Grep patterns in self-improve
- Verify file paths are correct
- Adjust pattern detection thresholds

**Questions return low confidence:**
- Normal for new experts
- Improve with self-improvement runs
- Add more initial patterns if needed

**Duplicate coverage with existing expert:**
- Consider if new expert needed
- Or enhance existing expert instead
- Or split existing expert's domain

## Output Template

After creating expert, provide summary:

```markdown
## Created: {Name} Expert

**Domain:** {description}
**Location:** `.claude/experts/{name}-expert/`

**Files Created:**
- expertise.yaml (version 0.1.0, {N} initial patterns)
- question.md (customized for {domain})
- self-improve.md (explores {file-patterns})

**Initial Self-Improvement:**
- Explored {N} files
- Discovered {M} patterns
- Confidence: low → {updated}

**Usage:**
- Ask questions: `/ask-expert {name} "your question"`
- Update expertise: `/sync-expertise {name}`

**Next Steps:**
- Test with sample questions
- Run self-improvement after domain changes
- Enhance patterns as they're validated
```
