# Skill Reviewer Guidelines

Review and improve skills for maximum effectiveness and reliability.

## Review Process

### 1. Locate and Read Skill

- Find SKILL.md file
- Read frontmatter and body content
- Check for supporting directories (references/, scripts/, assets/)

### 2. Validate Structure

- Frontmatter format (YAML between `---`)
- Required fields: `name`, `description`
- Body content exists and is substantial

### 3. Evaluate Description (Most Critical)

- **Trigger Phrases**: Does description include specific phrases users would say?
- **Third Person**: Avoids first/second person ("I can help you", "You can use this"). Imperative form ("Use when...") is fine.
- **Specificity**: Concrete scenarios, not vague
- **Length**: Appropriate (not too short <50 chars, not too long >1024 chars for description)
- **Example Triggers**: Lists specific user queries that should trigger skill

### 4. Assess Content Quality

- **Line Count**: SKILL.md body should be under 500 lines (lean, focused)
- **Writing Style**: Imperative/infinitive form ("To do X, do Y" not "You should do X")
- **Instructions vs documentation**: Every paragraph should tell the agent what to do. Flag prose that only describes, frames, or contextualizes the skill for a human reader — it is drift, not instruction.
- **Lean baseline comparison**: Pick the simplest existing skills in the same collection (ones that open with a one-line purpose and jump straight into Task Tracking or Step 1) and compare the reviewed skill against that baseline. If the reviewed skill has multiple paragraphs of context before the first instruction while its neighbors do not, flag the excess as narrator prose.
- **Organization**: Clear sections, logical flow
- **Specificity**: Concrete guidance, not vague advice

### 5. Check Progressive Disclosure

- **Core SKILL.md**: Essential information only
- **references/**: Detailed docs moved out of core
- **scripts/**: Utility scripts if needed
- **assets/**: Output resources separate from documentation
- **Pointers**: SKILL.md references these resources clearly

### 6. Review Supporting Files (if present)

- **references/**: Check quality, relevance, organization
- **scripts/**: Check scripts are executable and documented
- **assets/**: Verify assets are used and referenced

### 7. Identify Issues

Categorize by severity (critical/major/minor).

Anti-patterns to watch for:
- Vague trigger descriptions
- Too much content in SKILL.md (should be in references/)
- First/second person in description ("I can help you", "You can use this")
- Missing key triggers
- No references when they'd be valuable
- **Narrator prose**: meta-framing that explains the file to its own reader ("This SKILL.md is the router..."), cross-skill commentary ("This is the sibling of /other-skill"), marketing copy ("X is the structured alternative to Y"), architecture commentary that restates what the instructions already convey, historical rationale, and tautological boundary statements ("X is Y's job; this skill only does Z")
- **"Step 0" as mode detection**: a numbered step that only inspects caller input or picks a mode. Should be folded into the opening prose, not given a step heading

## Quality Standards

- Description must have strong, specific trigger phrases
- SKILL.md should be lean (under 500 lines)
- Writing style must be imperative/infinitive form
- Progressive disclosure properly implemented
- All file references work correctly

## Output Format

When reviewing a skill, produce a report with:

### Summary
Overall assessment and word counts.

### Description Analysis
- Current description
- Issues found
- Recommended improvements (with suggested text)

### Content Quality
- Line count assessment
- Writing style assessment
- Organization assessment

### Progressive Disclosure
- Current structure (file counts, word counts)
- Assessment of whether disclosure is effective
- Recommendations for better organization

### Issues by Severity

#### Critical
Issues that prevent the skill from working correctly.

#### Major
Issues that significantly reduce skill effectiveness.

#### Minor
Polish and optimization suggestions.

### Positive Aspects
What the skill does well.

### Overall Rating
Pass / Needs Improvement / Needs Major Revision

### Priority Recommendations
Top 3 fixes ordered by impact.
