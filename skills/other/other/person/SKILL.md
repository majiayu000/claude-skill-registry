---
context: fork
model: haiku
---

# /person

Quick-create a person note.

## Usage

```
/person <name>
/person <name> from <organisation>
/person <name> role <job title>
```

## Examples

```
/person John Smith
/person Sarah Jones from VendorA
/person Mike Chen role Solutions Architect from SAP
```

## Instructions

1. Parse the command for:
   - **name**: Person's full name (required)
   - **organisation**: Company/org (after "from")
   - **role**: Job title (after "role")

2. Check if person already exists:
   - Search for `{{name}}.md` (no prefix)
   - Also check legacy `Person - {{name}}.md` format
   - If exists, show existing note instead of creating duplicate

3. Generate filename: `{{name}}.md` (no prefix - type is in frontmatter)

4. Create person note in vault root:

```markdown
---
type: Person
title: {{name}}
created: {{DATE}}
modified: {{DATE}}
role: {{role or null}}
organisation: {{org_link or null}}
emailAddress: null
tags: []
---

# {{name}}

## Contact Information

- **Role**: {{role}}
- **Organisation**: {{org_link}}
- **Email**:

## Notes


## Interactions

```dataview
TABLE date as "Date", title as "Meeting"
FROM ""
WHERE type = "Meeting" AND contains(attendees, this.file.link)
SORT date DESC
LIMIT 10
```

## Related Projects

```dataview
LIST
FROM ""
WHERE type = "Project" AND contains(file.outlinks, this.file.link)
```
```

5. For organisation:
   - Check if `Organisation - {{org}}.md` exists
   - If yes, link: `"[[Organisation - VendorA]]"`
   - If no, just use the name (offer to create org note)

6. After creating:
   - Confirm creation with file path
   - Suggest linking from relevant meetings
   - If from known org, load context about that org

## Note on Naming Convention

Person notes no longer require the "Person - " prefix. The note type is determined by the `type: Person` frontmatter field, not the filename. This allows for cleaner wiki-links like `[[John Smith]]` instead of `[[John Smith]]`.

Legacy files with the "Person - " prefix will still work but can be renamed using `/rename`.
