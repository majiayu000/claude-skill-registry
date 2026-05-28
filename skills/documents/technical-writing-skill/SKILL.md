---
document_name: "technical-writing.skill.md"
location: ".claude/skills/technical-writing.skill.md"
codebook_id: "CB-SKILL-TECHWRITE-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for technical writing"
skill_metadata:
  category: "documentation"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Subject matter understanding"
    - "Markdown proficiency"
category: "skills"
status: "active"
tags:
  - "skill"
  - "documentation"
  - "technical-writing"
ai_parser_instructions: |
  This skill defines procedures for technical writing.
  Used by Doc Chef agent.
---

# Technical Writing Skill

=== PURPOSE ===

Procedures for creating clear, accurate technical documentation.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(doc-chef) @ref(CB-AGENT-DOC-001) | Primary skill for docs |

=== PROCEDURE: Document Planning ===

**Before Writing:**
1. Identify the audience
2. Define the purpose
3. Outline the structure
4. Gather source material
5. Identify prerequisites

**Audience Analysis:**
| Audience | Knowledge | Needs |
|----------|-----------|-------|
| Beginner | Minimal | Step-by-step, context |
| Intermediate | Working knowledge | How-to, best practices |
| Advanced | Expert | Reference, edge cases |

=== PROCEDURE: Writing Guidelines ===

**Clarity:**
- Use simple, direct language
- One idea per sentence
- Active voice preferred
- Avoid jargon (or define it)
- Be specific, not vague

**Examples:**
```
✗ "The system processes the data."
✓ "The API validates the request body against the schema."

✗ "You should configure the settings properly."
✓ "Set the API_KEY environment variable to your key."
```

**Structure:**
- Lead with the most important information
- Use headings to organize
- Keep paragraphs short (3-5 sentences)
- Use lists for sequential or parallel items
- Include code examples

=== PROCEDURE: Document Types ===

**Conceptual (What/Why):**
- Explains concepts and architecture
- Provides context and background
- Answers "what is this?" and "why use it?"

**Procedural (How):**
- Step-by-step instructions
- Numbered steps
- Expected outcomes for each step

**Reference (Details):**
- Complete, accurate information
- Organized for scanning
- API endpoints, config options, etc.

=== PROCEDURE: Code Examples ===

**Best Practices:**
```markdown
<!-- Show the language for syntax highlighting -->
```javascript
// Include comments explaining key parts
const result = api.getData({ limit: 10 });
```

**Example Guidelines:**
- Keep examples minimal but complete
- Use realistic values, not "foo/bar"
- Show expected output when helpful
- Test all code examples

=== PROCEDURE: Style Consistency ===

**Headings:**
- Use sentence case: "Getting started"
- Not title case: "Getting Started"
- Be descriptive, not clever

**Lists:**
- Parallel structure
- Consistent punctuation
- Complete thoughts or fragments (not mixed)

**Formatting:**
| Element | Format |
|---------|--------|
| Code inline | `backticks` |
| File paths | `path/to/file` |
| Commands | `npm install` |
| Variables | `VARIABLE_NAME` |
| UI elements | **Bold** |
| First use of term | *Italics* |

=== PROCEDURE: Review Checklist ===

**Technical Accuracy:**
- [ ] Code examples work
- [ ] Commands are correct
- [ ] Links are valid
- [ ] Information is current

**Clarity:**
- [ ] Purpose is clear
- [ ] Steps are complete
- [ ] Prerequisites stated
- [ ] Audience appropriate

**Completeness:**
- [ ] Edge cases covered
- [ ] Errors/troubleshooting included
- [ ] Related docs linked
- [ ] Next steps provided

=== PROCEDURE: Maintenance ===

**When to Update:**
- API/feature changes
- User feedback received
- Errors discovered
- Related docs changed

**Update Process:**
1. Identify what changed
2. Find all affected docs
3. Update content
4. Update related cross-refs
5. Update "last edited" date
6. Review for consistency

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(api-documentation) | API-specific writing |
| @skill(voice-tone) | Tone consistency |
