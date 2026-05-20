# Drafting template and authoring rules

## Canonical file skeleton

Use one Markdown file with this fixed order:

1. `# Full Name - positioning descriptor`
2. `## QUICK REFERENCE`
3. scope declaration paragraph
4. education
5. professional experience if any
6. research and publications if any
7. skills index
8. certifications and achievements if any
9. languages
10. extracurricular and leadership if any

Do not reorder sections for stylistic reasons. Stable order helps both human maintenance and agent retrieval.

## QUICK REFERENCE template

Write the section as YAML in a fenced block directly under the `QUICK REFERENCE` heading. Keep values flat. Omit empty fields.

```yaml
name: Full Name
current_location: City, Country
target_roles: [Role A, Role B]
open_to_relocation: true

education:
  - "[DEGREE] Degree Name | Institution | Grade | Month Year"

gpa_summary: "Course A: grade, Course B: grade"

professional:
  - "[ROLE] Job Title | Company | Period"

top_skills: [skill1, skill2, skill3]
tools: [tool1, tool2, tool3]

competitions:
  - "Result - Competition Name (Year)"

certifications:
  - "Cert Name | Issuer | Date | ID: XXXXX"

languages:
  - "Language: Level (Certificate if applicable)"

github: https://github.com/username
linkedin: https://linkedin.com/in/username
portfolio: https://example.com
```

## Scope declaration template

Write one short third-person paragraph explaining what the file is for, then close it with a `VERIFIED FACTS` HTML comment.

```markdown
This file is a personal knowledge base documenting Full Name's academic and
professional record. It is not intended for direct distribution to third
parties. Its purpose is to serve as a structured source of truth from which
career outputs can be generated. Hard factual claims should be verified or
marked as needing evidence before reuse.

<!-- VERIFIED FACTS: graduation=YYYY-MM, final_grade=x/y, cert_id=XXXX -->
```

## Section authoring rules

- Degrees: use `## [DEGREE] ...` headings and one sentence on relevance.
- Courses: use `#### [COURSE] ...` plus one flat `Topics:` line.
- Projects under courses: use `##### [PROJECT] ...` and include a required `**TL;DR:**` line under 30 words.
- Thesis: use `### [THESIS] ...` with `Full title`, `Supervisors`, `Research area`, and `TL;DR`.
- Roles: use `### [ROLE] ...` with `TL;DR` and quantified bullets, not prose paragraphs.
- Papers and preprints: use `### [PAPER] ...` or `### [PREPRINT] ...` with authorship, venue or status, and `TL;DR`.
- Skills index: use bold category labels with comma-separated terms on one line; every skill must be evidenced elsewhere in the file.
- Languages: use a table, not prose.

## Drafting discipline

- Prefer omission over guessing.
- Keep descriptors specific to the user's actual positioning, not generic aspirational branding.
- Use exact dates, grades, rankings, IDs, and scores when known.
- If the user provides raw material that lacks a needed field, mark the gap and ask for that fact rather than inventing a filler value.
