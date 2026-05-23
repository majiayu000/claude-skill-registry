---
name: writing-skill-md
description: Defines how to create, structure, and document agent skills, including required metadata, directory layout, and best practices. Use this skill when designing, validating, or reviewing agent skills.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

# Writing SKILL.md

## When to use this skill
This skill teaches agents how to author compliant Agent Skills. Use it whenever you need to create a new skill, review an existing one, or ensure a skill follows the official Agent Skills format and conventions.

## Skill structure
A skill is a directory that contains at minimum a SKILL.md file. Expected structure:
```
skill-name/
└── SKILL.md
```

Optional supporting directories may be added when helpful:
- scripts
- references
- assets

## SKILL.md requirements
Each SKILL.md file consists of two parts:
1. YAML frontmatter
2. Markdown body with instructions

The frontmatter is mandatory. The body content is flexible but should be optimized for agent use.

## Frontmatter fields

### Required fields
_name_
- Length: 1 to 64 characters
- Characters: lowercase letters, numbers, hyphens
- Must not start or end with a hyphen
- Must not contain consecutive hyphens
- Must exactly match the parent directory name

_description_
- Length: 1 to 1024 characters
- Must be non-empty
- Must explain what the skill does and when it should be used
- Should include keywords that help agents recognize relevant tasks

### Optional fields
_license_
- Short license name or reference to a bundled license file

_compatibility_
- Length: 1 to 500 characters
- Only include if the skill has specific environment requirements
- May describe intended product, required system packages, or network access

_metadata_
- Key-value mapping of strings
- Used for additional properties such as author, version, or internal tags
- Prefer unique and descriptive keys

_allowed-tools_
- Space-delimited list of pre-approved tools
- This field is not part of the core specification and experimental, it should only be used in controlled environments

## Valid name examples
Valid:
- pdf-processing
- data-analysis
- code-review

Invalid:
- PDF-Processing (uppercase not allowed)
- -pdf (cannot start with hyphen)
- pdf--processing (consecutive hyphens not allowed)

## Writing the description
A good description explains both capability and context.
Good example: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
Poor example: Helps with PDFs.

## Body content guidelines
The Markdown body contains the actual skill instructions. There are no strict format requirements, but clarity and efficiency are critical. Recommended sections:
- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases and failure modes
- Decision rules for when the skill should or should not be used

Assume the agent will load the full SKILL.md only after deciding to activate the skill based on only the name and description.

## Progressive disclosure principles
Design skills to minimize unnecessary context usage:
1. Frontmatter metadata
  - Name and description are always loaded
  - Keep them concise and precise
2. Markdown body instructions
  - Loaded only when the skill is activated
  - Recommended size is under 5000 tokens
  - Move detailed material into separate files
3. Resources
  - Loaded only when explicitly referenced
  - Includes scripts, references, and assets

## Optional directories

### scripts
Executable code that agents may run.
Guidelines:
- Clearly document dependencies
- Fail gracefully with helpful error messages
- Handle edge cases explicitly

Common languages include Python, Bash, and JavaScript, depending on the agent environment.

### references
Additional documentation loaded only when needed.
Common files:
- REFERENCE.md for deep technical detail
- FORMS.md for structured formats or templates
- Domain-specific documentation such as finance.md or legal.md

Keep each reference file focused and small.

### assets
Static resources such as:
- Document or configuration templates
- Diagrams or example images
- Data files like schemas or lookup tables

## File references
When referring to other files, always use relative paths from the skill root.
Examples:
- references/REFERENCE.md
- scripts/extract.py

Avoid deep nesting. References should generally be only one level away from SKILL.md.

## Review checklist
Before finalizing a skill, verify:
- The directory name matches the name field
- Required frontmatter fields are present and valid
- The description clearly states what and when
- Instructions are actionable and unambiguous
- Supporting files are referenced correctly
- The skill follows progressive disclosure principles
