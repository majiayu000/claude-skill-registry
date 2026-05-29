---
name: contacts-management
description: |
  Manage contact information by adding, updating, or validating entries.
  Use when adding new contacts or updating existing contact details.
  Triggers: "add contact", "new contact", "update contact", "contacts".
license: MIT
metadata:
  author: KemingHe
  version: "2.0.0"
---

# Contact Management

Add, update, and validate contact information by extracting details from various sources and ensuring completeness.

**Temporary persona**: Senior engineering manager with expertise in team coordination and professional networking.

## When to Use This Skill

- Adding a new contact from LinkedIn, email signature, or conversation
- Updating existing contact with new information
- Validating contact completeness before meetings
- Organizing contacts by domain or team

## Asset Resolution

1. Check `./assets/contacts-template.md` for contact entry format
2. Search `**/contacts.md` for existing contacts file in repository
3. If no contacts file exists, offer to create one using template

## Process

### Step 1: Identify Source and Extract

When user wants to add/update a contact, gather from available sources:

- LinkedIn profile URL (extract title, company, specializations)
- Email signature (extract phone, email, title)
- Meeting notes or conversation history
- User-provided information directly

**Extract these fields**:

| Field | Required | Source Hints |
| :--- | :--- | :--- |
| Full Name | Yes | LinkedIn headline, email signature |
| Title | Yes | LinkedIn current position |
| Company | Yes | LinkedIn experience, email domain |
| Email | Yes | Email signature, LinkedIn contact |
| Phone | No | Email signature, user-provided |
| LinkedIn | No | Profile URL |
| GitHub | No | Profile URL, user-provided |
| Timezone | No | LinkedIn location, user-provided |
| Specializations | No | LinkedIn about/skills, conversation context |

### Step 2: Validate and Request Missing

Check extracted information:

- **Email format**: Valid structure ([name@domain.tld](mailto:name@domain.tld))
- **Required fields**: Name, title, company, email present
- **Consistency**: Title matches company context

**Actively request missing info**:

```markdown
I found: [extracted fields]

Missing: [list of missing fields]

Can you provide: [specific questions for missing required fields]
```

### Step 3: Add or Update Entry

- Search existing contacts.md for duplicate entries
- If updating: show diff of changes, confirm with user
- If adding: format entry per template, confirm placement (domain section)
- Present final entry for approval before writing

## Output Format

Present contact entry in markdown following template structure:

```markdown
### First Name Last Name

- **Title**: [Job Title], [Company/Organization]
- **Email**: [email@domain.com](mailto:email@domain.com) or ???
- **Phone**: [+0 000-000-0000] or ???
- **LinkedIn**: [username](https://www.linkedin.com/in/username/) or N/A or ???
- **GitHub**: [username](https://github.com/username) or N/A or ???
- **Timezone**: [Timezone Name (Abbreviation, UTC+X)] or ???
- **Specializations**:
  - [Area 1]
  - [Area 2]
- **Notes**:
  - [Important context]
```

**Field status markers**:

- `???` = Missing/unknown - should be requested from user or researched
- `N/A` = Not applicable/not relevant for this contact (e.g., no GitHub for non-developer)

## General Doc Constraints

Apply to all generated output. If a discovered template deviates from any rule (e.g., uses emojis semantically, uses a different bullet convention), note the deviation explicitly and confirm with the user before treating it as a permitted exception.

- **Characters**: QWERTY keyboard typeable only - no smart quotes, emojis, or special Unicode anywhere. In prose, do not use em-dashes or em-dash substitutes (`--`, ` -- `); use ` - ` (space-dash-space) for clause separation instead. Exception: `↑` for ToC navigation.
- **Inline formatting**: Use `_underscore_` for italics, not `*single-star*`. Place colons after bold inline labels outside the markers: `**Topic**:` not `**Topic:**`.
- **Bullets**: Use `-` for all unordered lists; one bullet per complete thought; never wrap a bullet's content mid-sentence onto a continuation line - split into separate bullets if too long or multi-thought. Nested sub-bullets for component grouping are permitted. End with a period only when the item is a full sentence; omit the period for concise fragment items (preferred).
- **Prose**: Never break a sentence across lines with a hard newline; multi-sentence paragraphs belong on one continuous line since editors and viewers handle visual wrapping. Exception: commit message bodies use one sentence per line for `git log` readability.
- **Template hygiene**: Delete `(optional)` and any parenthetical conditional label (e.g., `(if operational)`) from a section header the moment the section is populated - treat it as a `.gitkeep`-style placeholder that exists only until first use, then is removed. Omit the entire section (header and body) when unused. Populate all bracketed placeholders with actual content; never leave `[TODO]`, `[TBD]`, or any `[placeholder]` in generated output.
- **Consistency**: Use the same term for the same concept throughout; match the voice and tense of the template; do not mix header levels for parallel sections.
- **KISS and DRY**: Each section and bullet conveys unique information - no redundancy or overlap.

> General Doc Constraints v1.1.0 - KemingHe/common-devx

## Skill Constraints

- **Template as scaffold**: Use discovered templates as minimum structure
- **Validation first**: Always validate email format and required fields before adding
- **Duplicate check**: Search existing contacts before adding new entry
- **User confirmation**: Always confirm before writing changes
- **Privacy awareness**: Only include information user has permission to store
