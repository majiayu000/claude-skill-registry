---
name: anti-slop
description: Comprehensive toolkit for detecting and eliminating "AI slop" - generic, low-quality AI-generated patterns in natural language, code, and design. Use when reviewing or improving content quality, preventing generic AI patterns, cleaning up existing content, or enforcing quality standards in writing, code, or design work.
---

# Anti-Slop Skill

Detect and eliminate generic AI-generated patterns ("slop") across natural language, code, and design.

## What is AI Slop?

AI slop refers to telltale patterns that signal low-quality, generic AI-generated content:
- **Text**: Overused phrases like "delve into," excessive buzzwords, meta-commentary
- **Code**: Generic variable names, obvious comments, unnecessary abstraction
- **Design**: Cookie-cutter layouts, generic gradients, overused visual patterns

This skill helps identify and remove these patterns to create authentic, high-quality content.

## When to Use This Skill

Apply anti-slop techniques when:
- Reviewing AI-generated content before delivery
- Creating original content and want to avoid generic patterns
- Cleaning up existing content that feels generic
- Establishing quality standards for a project
- User explicitly requests slop detection or cleanup
- Content has telltale signs of generic AI generation

## Core Workflow

### 1. Detect Slop

**For text files:**
```bash
python scripts/detect_slop.py <file> [--verbose]
```

This analyzes text and provides:
- Slop score (0-100, higher is worse)
- Specific pattern findings
- Actionable recommendations

**Manual detection:**
Read the appropriate reference file for detailed patterns:
- `references/text-patterns.md` - Natural language slop patterns
- `references/code-patterns.md` - Programming slop patterns  
- `references/design-patterns.md` - Visual/UX design slop patterns

### 2. Clean Slop

**Automated cleanup (text only):**
```bash
# Preview changes
python scripts/clean_slop.py <file>

# Apply changes (creates backup)
python scripts/clean_slop.py <file> --save

# Aggressive mode (may slightly change meaning)
python scripts/clean_slop.py <file> --save --aggressive
```

**Manual cleanup:**
Apply strategies from the reference files based on detected patterns.

## Text Slop Detection & Cleanup

### High-Priority Targets

**Remove immediately:**
- "delve into" → delete or replace with "examine"
- "navigate the complexities" → "handle" or delete
- "in today's fast-paced world" → delete
- "it's important to note that" → delete
- Meta-commentary about the document itself

**Simplify wordy phrases:**
- "in order to" → "to"
- "due to the fact that" → "because"
- "has the ability to" → "can"

**Replace buzzwords:**
- "leverage" → "use"
- "synergistic" → "cooperative"
- "paradigm shift" → "major change"

### Quality Principles

**Be direct:**
- Skip preambles and meta-commentary
- Lead with the actual point
- Cut transition words that don't add meaning

**Be specific:**
- Replace generic terms with concrete examples
- Name specific things instead of "items," "things," "data"
- Use precise verbs instead of vague action words

**Be authentic:**
- Vary sentence structure and length
- Use active voice predominantly
- Write in a voice appropriate to context, not corporate-generic

## Code Slop Detection & Cleanup

### High-Priority Targets

**Rename generic variables:**
- `data` → name what data it represents
- `result` → name what the result contains
- `temp` → name what you're temporarily storing
- `item` → name what kind of item

**Remove obvious comments:**
```python
# Bad
# Create a user
user = User()

# Better - let code speak
user = User()
```

**Simplify over-engineered code:**
- Remove unnecessary abstraction layers
- Replace design patterns used without purpose
- Simplify complex implementations of simple tasks

**Improve function names:**
- `handleData()` → what are you doing with data?
- `processItems()` → what processing specifically?
- `manageUsers()` → what management action?

### Quality Principles

**Clarity over cleverness:**
- Write code that's easy to understand
- Optimize only when profiling shows need
- Prefer simple solutions to complex ones

**Meaningful names:**
- Variable names should describe content
- Function names should describe action + object
- Class names should describe responsibility

**Appropriate documentation:**
- Document why, not what
- Skip documentation for self-evident code
- Focus documentation on public APIs and complex logic

## Design Slop Detection & Cleanup

### High-Priority Targets

**Visual slop:**
- Generic gradient backgrounds (purple/pink/cyan)
- Overuse of glassmorphism or neumorphism
- Floating 3D shapes without purpose
- Every element using same design treatment

**Layout slop:**
- Template-driven layouts ignoring content needs
- Everything in cards regardless of content type
- Excessive whitespace without hierarchy
- Center-alignment of all elements

**Copy slop:**
- "Empower your business" type headlines
- Generic CTAs like "Get Started" without context
- Buzzword-heavy descriptions
- Stock photo aesthetics

### Quality Principles

**Content-first design:**
- Design around actual content needs
- Create hierarchy based on importance
- Let content determine layout, not templates

**Intentional choices:**
- Every design decision should be justifiable
- Use patterns because they serve users, not because they're trendy
- Vary visual treatment based on element importance

**Authentic voice:**
- Copy should reflect brand personality
- Avoid generic marketing speak
- Be specific about value proposition

## Reference Files

Consult these comprehensive guides when working on specific domains:

- **[text-patterns.md](references/text-patterns.md)** - Complete catalog of natural language slop patterns with detection rules and cleanup strategies

- **[code-patterns.md](references/code-patterns.md)** - Programming antipatterns across languages with refactoring guidance

- **[design-patterns.md](references/design-patterns.md)** - Visual and UX design slop patterns with improvement strategies

Each reference includes:
- Pattern definitions and examples
- Detection signals (high/medium confidence)
- Context where patterns are acceptable
- Specific cleanup strategies

## Scripts

### detect_slop.py

Analyzes text files for AI slop patterns.

**Usage:**
```bash
python scripts/detect_slop.py <file> [--verbose]
```

**Output:**
- Overall slop score (0-100)
- Category-specific findings
- Line numbers and examples
- Actionable recommendations

**Scoring:**
- 0-20: Low slop (authentic writing)
- 20-40: Moderate slop (some patterns)
- 40-60: High slop (many patterns)
- 60+: Severe slop (heavily generic)

### clean_slop.py

Automatically removes common slop patterns from text files.

**Usage:**
```bash
# Preview changes
python scripts/clean_slop.py <file>

# Save changes (creates backup)
python scripts/clean_slop.py <file> --save

# Save to different file
python scripts/clean_slop.py <file> --output clean_file.txt

# Aggressive mode
python scripts/clean_slop.py <file> --save --aggressive
```

**What it cleans:**
- High-risk phrases
- Wordy constructions
- Meta-commentary
- Excessive hedging
- Buzzwords
- Redundant qualifiers
- Empty intensifiers

**Safety:**
- Always creates `.backup` file when overwriting
- Preview mode shows changes before applying
- Preserves content meaning (non-aggressive mode)

## Best Practices

### Prevention Over Cure

**When creating content:**
1. Write with specific audience in mind
2. Use concrete examples over abstractions
3. Lead with the point, skip preambles
4. Choose words for precision, not impression
5. Review before considering it complete

### Context-Aware Cleanup

Not all patterns are always slop:

**Acceptable contexts:**
- Academic writing may need more hedging
- Legal documents require specific phrasing
- Internal documentation can use shortcuts
- Technical docs have domain-specific conventions

**Always consider:**
- Who is the audience?
- What is the purpose?
- Does this pattern serve a function?
- Is there a better alternative?

### Iterative Improvement

1. **Detect** - Run detection scripts or manual review
2. **Analyze** - Understand which patterns are truly problems
3. **Clean** - Apply automated cleanup where safe
4. **Review** - Manually verify changes maintain meaning
5. **Refine** - Fix remaining issues by hand

### Quality Over Automation

The scripts are tools, not replacements for judgment:
- Use automated detection to find candidates
- Apply automated cleanup to obvious patterns
- Manually review anything that changes meaning
- Exercise discretion based on context

## Integration Patterns

### Code Review

```bash
# Check files before committing
python scripts/detect_slop.py src/documentation.md --verbose

# Clean up automatically
python scripts/clean_slop.py src/documentation.md --save
```

### Content Pipeline

1. Create initial content
2. Run slop detection
3. Apply automated cleanup
4. Manual review and refinement
5. Final quality check

### Standards Enforcement

Create project-specific thresholds:
- Max acceptable slop score: 30
- Required manual review for scores > 20
- Auto-reject submissions with scores > 50

## Limitations

**Scripts only handle text:**
- Code slop detection is manual (use code-patterns.md)
- Design slop detection is manual (use design-patterns.md)

**Context sensitivity:**
- Scripts can't understand all contexts
- Some "slop" may be appropriate in certain domains
- Always review automated changes

**Language coverage:**
- Detection patterns optimized for English
- Code patterns focus on common languages (Python, JS, Java)
- Design patterns are platform-agnostic

## Common Scenarios

### Scenario 1: Review AI-Generated Content

```bash
# User asks: "Can you review this article for AI slop?"
1. Read references/text-patterns.md for patterns to watch
2. Run: python scripts/detect_slop.py article.txt --verbose
3. Review findings and apply manual cleanup
4. Optionally run: python scripts/clean_slop.py article.txt --save
5. Do final manual review of cleaned content
```

### Scenario 2: Clean Up Codebase

```bash
# User asks: "Help me clean up generic AI patterns in my code"
1. Read references/code-patterns.md
2. Review code files manually for patterns
3. Create list of generic names to rename
4. Refactor following principles in code-patterns.md
5. Remove obvious comments and over-abstractions
```

### Scenario 3: Design Review

```bash
# User asks: "Does this design look too generic?"
1. Read references/design-patterns.md
2. Check against high-confidence slop indicators
3. Identify specific issues (gradients, layouts, copy)
4. Provide specific recommendations from design-patterns.md
5. Suggest concrete alternatives
```

### Scenario 4: Establish Quality Standards

```bash
# User asks: "Help me create quality standards for our team"
1. Review all three reference files
2. Identify patterns most relevant to user's domain
3. Create project-specific guidelines
4. Set up detection scripts in development pipeline
5. Document acceptable exceptions
```

## Tips for Success

**For text cleanup:**
- Run detection first to understand scope
- Use non-aggressive mode for important content
- Always review automated changes
- Focus on high-risk patterns first

**For code cleanup:**
- Start with renaming generic variables
- Remove obvious comments next
- Refactor over-engineered code last
- Test after each significant change

**For design cleanup:**
- Audit visual elements against patterns
- Prioritize structural issues over aesthetic ones
- Ensure changes serve user needs
- Maintain brand consistency

**General principles:**
- Quality > uniformity
- Context > rules
- Clarity > cleverness
- Specificity > generality
