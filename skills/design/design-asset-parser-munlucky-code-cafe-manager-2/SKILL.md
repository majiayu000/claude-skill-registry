---
name: design-asset-parser
description: Parses design assets (PDF, CSS) to generate a draft design spec.
---

# Design Asset Parser Skill

> **Purpose**: Parse design deliverables (Figma export images/CSS/HTML, screen-spec PDF) to produce a draft dev spec
> **Outputs**: `{tasksRoot}/{feature-name}/design-spec.md`, `pending-questions.md`
> **When to use**: Before implementing a new feature when design assets are provided

---

## Role

Automatically extract UI/feature requirements from design assets and generate a structured spec that developers can implement immediately.

### Input file types
1. **Screen-spec PDF**: `.claude/docs/design-assets/*.pdf`
2. **Figma export**: images (PNG/JPG), CSS/HTML export
3. **Design guide**: color/font/spacing tokens

### Key capabilities
- Extract text/images from PDF (OCR supported)
- Extract components/style tokens from CSS/HTML export
- Structure UI elements, validation, states, edge cases
- Auto-detect unclear requirements and generate questions

---

## Triggers

Call automatically or manually in these cases:

### Automatic triggers
1. PDF added under `.claude/docs/design-assets/`
2. Figma export zip added
3. Moonshot Agent classifies as new feature and finds design asset paths

### Manual triggers
```bash
# Example user requests
"Parse the screen-spec PDF and create a dev spec"
"Analyze Figma export CSS and organize style tokens"
```

---

## Flow

### Step 1: Verify input files (1m)
```markdown
Input file list:
- Screen spec: .claude/docs/design-assets/batch-management_v3.pdf
- Figma export: .claude/docs/design-assets/batch-management-export.zip
- Feature name: batch-management
```

### Step 2: Parse PDF (3-5m)
**Work**:
- Extract PDF text (read PDF with Read tool)
- Extract images and run OCR (if needed)
- Identify section structure (screen layout, field definitions, feature requirements)

**Extract items**:
- Page/modal/tab structure
- Form fields: name, type, required, default, validation
- Table/Grid: columns, sort/filter, paging, empty state
- Buttons/actions: label, action, enable/disable conditions
- State/error/loading: message rules

### Step 3: Parse CSS/HTML (2-3m)
**Work**:
- Extract CSS variables (color, font, spacing)
- Extract component classes and variants (Primary/Secondary/Disabled)
- Identify HTML structure (layout, component hierarchy)

**Extract items**:
```css
/* Style tokens */
--color-primary: #1a73e8;
--font-size-base: 14px;
--spacing-md: 16px;
```

### Step 4: Draft spec (5-10m)
**Output file**: `{tasksRoot}/{feature-name}/design-spec.md`

Base structure:
```markdown
# Design-based Development Spec

## Screen Overview
- Page structure
- Main flow

## UI Elements and Behavior
### Form Fields
| Field | Type | Required | Default | Validation |
|--------|------|---------|--------|------------|

### Table Columns
| Column | Sort | Filter | Notes |
|--------|------|--------|------|

### Buttons/Actions
- Button: action description

### State/Error/Loading
- Loading: spinner location
- Success/Error: message rules

## Style Tokens
- Colors, fonts, spacing

## Asset Manifest
- Image/icon list

## Extraction Evidence
- Source files, page numbers

## Open Questions
- List of unclear requirements
```

### Step 5: Record open questions (1-2m)
**Output file**: `{tasksRoot}/{feature-name}/pending-questions.md`

```markdown
# Pending Questions

## Date: {YYYY-MM-DD}

### Priority: HIGH
1. **Question title**
   - Source: design-spec.md section
   - Question: specific question
   - Impact: impact on implementation/design
```

### Step 6: Summarize results and next steps
```markdown
OK Design Asset Parser Skill complete

## Outputs
- design-spec.md: N UI elements, N style tokens
- pending-questions.md: N open questions

## Next steps
1. Resolve HIGH priority questions in pending-questions.md
2. Call Requirements Analyzer Agent
3. Call Context Builder Agent
```

---

## Prompt Template

```markdown
You are the Design Asset Parser Skill.
Read design assets and structure a dev spec.

## Input
- Design file paths: {designPaths}
- Target feature name: {featureName}
- Existing design-spec.md: {hasSpec}

## Tasks
1. Read PDF/Figma export files (use Read tool)
2. Extract UI elements (Form/Table/Button/State)
3. Specify validation/edge cases
4. Extract style tokens (if CSS exists)
5. Build asset manifest
6. Organize open questions

## Output
- `{tasksRoot}/{feature-name}/design-spec.md`: structured dev spec
- `{tasksRoot}/{feature-name}/pending-questions.md`: open questions list

## Quality bar
- UI elements in table format
- Validation rules clearly specified (length/pattern/range)
- Convert ambiguous requirements into questions
- Priority included (HIGH/MEDIUM/LOW)
```

---

## Usage Examples

### Example 1: Parse screen-spec PDF
```
User: "Parse the screen-spec PDF and create a dev spec.
       Path: .claude/docs/design-assets/batch-management_v3.pdf
       Feature: batch-management"

Design Asset Parser Skill ->
1. Read PDF (Read tool)
2. Parse by section (layout, field definitions, requirements)
3. Create design-spec.md
4. Create pending-questions.md (unclear parts)

Outputs:
- {tasksRoot}/batch-management/design-spec.md
- {tasksRoot}/batch-management/pending-questions.md
```

### Example 2: Parse Figma CSS export
```
User: "Analyze Figma CSS export and organize style tokens.
       Path: .claude/docs/design-assets/batch-ui-export.css
       Feature: batch-management"

Design Asset Parser Skill ->
1. Read CSS file
2. Extract CSS variables (--color-*, --font-*, --spacing-*)
3. Extract component classes (.button--primary, .button--disabled)
4. Update the "Style Tokens" section in design-spec.md

Outputs:
- design-spec.md (style tokens updated)
```

### Example 3: Parse PDF + CSS together
```
User: "Parse the screen-spec PDF and Figma CSS together.
       PDF: .claude/docs/design-assets/batch-management_v3.pdf
       CSS: .claude/docs/design-assets/batch-ui-export.css
       Feature: batch-management"

Design Asset Parser Skill ->
1. Parse PDF -> UI elements, feature requirements
2. Parse CSS -> style tokens
3. Merge results -> design-spec.md
4. Conflicts -> pending-questions.md

Outputs:
- design-spec.md (UI + styles merged)
- pending-questions.md (conflict questions)
```

---

## Integrated Workflow

### Design Asset Parser -> Design Spec Extractor Agent
```
1. Design Asset Parser Skill:
   - Input: PDF/CSS files
   - Output: design-spec.md (draft), pending-questions.md

2. User:
   - Review pending-questions.md
   - Answer HIGH priority questions

3. Design Spec Extractor Agent:
   - Review design-spec.md
   - Compare with CLAUDE.md rules
   - Apply project patterns
   - Generate final design-spec.md

4. Requirements Analyzer Agent:
   - Create preliminary agreement based on design-spec.md
```

---

## Reference Info

### Project design asset paths
- **Example product**: `.claude/docs/design-assets/*.pdf`
- **Figma export**: `.claude/docs/design-assets/*.zip`, `*.css`, `*.html`

### Existing project patterns (follow CLAUDE.md)
- Entity-Request separation
- API proxy pattern
- Activity log header rules
- fp-ts Either pattern
- TypeScript strict mode

### Notes
1. **PDF parsing limits**: image-heavy PDFs need OCR
2. **CSS parsing limits**: inline styles cannot be extracted
3. **Automation limits**: ambiguous requirements should become questions
4. **Versioning**: record version history when design-spec.md changes
