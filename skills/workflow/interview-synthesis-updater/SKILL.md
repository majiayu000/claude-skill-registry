---
name: interview-synthesis-updater
description: Auto-update synthesis documents after interview analysis. Use after video-transcript-analyzer creates a new interview analysis file.
version: 1.0.0
allowed-tools: [Read, Write, Glob, Bash]
---

# Interview Synthesis Updater

## Overview
This skill automatically updates synthesis documents and the master index after a new customer interview analysis is created. It extracts themes, products, and personas from the interview analysis, updates relevant synthesis documents with new quotes and insights, creates new synthesis documents when needed, and keeps index.md current.

## When to Apply
Use this skill:
- **Automatically** after the video-transcript-analyzer skill completes
- When a new interview analysis file is created in `interview-analysis/`
- When you need to sync synthesis documents with recent interviews
- After manually creating or editing an interview analysis

Do NOT use this skill for:
- Creating initial interview analyses (use video-transcript-analyzer instead)
- General document editing
- Non-interview content

## Inputs
1. **Interview analysis file path** (required) - Path to the newly created interview analysis markdown file
2. **Base directory** (optional) - Root directory of the customer interviews project (defaults to current directory)

## Outputs
A report of all changes made:
- List of synthesis documents updated (by-theme, by-product, by-persona)
- List of new synthesis documents created
- Confirmation that index.md was updated
- Summary statistics (total interviews, themes, etc.)

## Setup Instructions

### First Time Setup
1. **Install dependencies**:
   ```bash
   cd ~/.claude/skills/interview-synthesis-updater
   npm install
   ```

2. **Verify directory structure**:
   The skill expects this structure in your project:
   ```
   customer interviews/
   ├── interview-analysis/          # Interview analysis files
   ├── syntheses/
   │   ├── _SYNTHESIS_TEMPLATE.md
   │   ├── by-theme/
   │   ├── by-product/
   │   └── by-persona/
   └── index.md
   ```

## Instructions for Claude

### Step 1: Validate Inputs
- Verify the interview analysis file path exists and is readable
- Check that it has valid YAML frontmatter with required fields:
  - `date`, `customer_first`, `company`, `role`, `call_type`
  - `themes`, `pain_points`, `hubspot_products`
- Verify the base directory structure exists (syntheses/, index.md, etc.)
- If validation fails, report the error and stop

### Step 2: Extract Metadata and Content
Parse the interview analysis file to extract:
- **From YAML frontmatter**:
  - `themes`: Array of theme tags
  - `hubspot_products`: Array of product names
  - `role`: Persona/role (for by-persona syntheses)
  - `pain_points`: Array of pain points
  - `pain_point_severity`: P0-P3 severity ratings
  - `date`, `customer_first`, `customer_last`, `company`
- **From markdown content**:
  - Key quotes from the "Key Quotes" section
  - Topical breakdown summaries
  - Business impact statements

### Step 3: Update By-Theme Syntheses
For each theme in the `themes` array:
1. Convert theme to filename: lowercase, replace spaces with hyphens (e.g., "Data Management" -> "data-management.md")
2. Check if `syntheses/by-theme/{theme-filename}` exists
3. **If exists**: Update the existing synthesis document
   - Add representative quotes to the "Representative Quotes" section
   - Increment frequency count in intro
   - Add interview to "Source Interviews" list at bottom
   - Update "Last Updated" date
4. **If doesn't exist**: Create new synthesis from template
   - Copy `syntheses/_SYNTHESIS_TEMPLATE.md`
   - Fill in theme name, description, initial quote
   - Add first source interview
   - Set frequency to 1
   - Save to `syntheses/by-theme/{theme-filename}`

### Step 4: Update By-Product Syntheses
For each product in the `hubspot_products` array:
1. Convert product to filename: lowercase, replace spaces/slashes with hyphens (e.g., "Lists/Views" -> "lists-views.md")
2. Check if `syntheses/by-product/{product-filename}` exists
3. **If exists**: Update the existing synthesis
   - Add product-specific pain points to relevant sections
   - Add quotes related to this product
   - Update pain points list
   - Add interview to source list
   - Update "Last Updated" date
4. **If doesn't exist**: Create new synthesis from template
   - Customize for product name
   - Add initial pain points and quotes
   - Add first source interview
   - Save to `syntheses/by-product/{product-filename}`

### Step 5: Update By-Persona Syntheses
Based on the `role` field:
1. Convert role to filename: lowercase, pluralize if needed (e.g., "HubSpot Admin" -> "hubspot-administrators.md")
2. Check if `syntheses/by-persona/{persona-filename}` exists
3. **If exists**: Update the existing synthesis
   - Add to persona profile patterns
   - Add representative quotes
   - Update common pain points
   - Add interview to source list
   - Update "Last Updated" date
4. **If doesn't exist**: Create new synthesis from template
   - Customize for persona
   - Add initial profile information
   - Add first quotes and patterns
   - Save to `syntheses/by-persona/{persona-filename}`

### Step 6: Update index.md
1. **Update quick stats**:
   - Count total files in `interview-analysis/` directory
   - Update date range (earliest to latest interview)
   - Count total synthesis documents
2. **Add to "Recent Interviews" section**:
   - Add new entry at the top (most recent first)
   - Format: `- **[Date]**: [First Last, Company] - [Brief description from summary]`
   - Keep only the 10 most recent
3. **Add to "All Interviews by Date" table**:
   - Add new row with: Date | Name | Company | Role | Key Topics | Link
4. **Update "Search by Theme" categories**:
   - For each theme, add interview to that theme's list
   - Create new theme category if it doesn't exist

### Step 7: Generate Report
Create a summary of all changes:
```markdown
## Synthesis Update Complete

### Updated Synthesis Documents
**By Theme:**
- data-management-lists.md (added 3 quotes, updated patterns)
- admin-workflow-productivity.md (added 2 quotes)

**By Product:**
- index-pages.md (added pain points, 4 quotes)
- custom-objects.md (added 2 quotes)

**By Persona:**
- hubspot-administrators.md (updated profile, 5 quotes)

### New Synthesis Documents Created
- syntheses/by-theme/accidental-admins.md
- syntheses/by-product/leads-object.md

### Index Updated
- Added interview: 2025-11-15 Matthew Ruxton, Ignite Reading
- Total interviews: 23
- Total syntheses: 18 (5 themes, 8 products, 5 personas)

### Recommendations
- Consider reviewing "accidental-admins" theme (now has 3 interviews)
- "Leads object" synthesis newly created - may need refinement
```

Return this report to the user.

## Quality Checks
- [ ] All YAML frontmatter fields properly extracted
- [ ] Quotes are verbatim from the source (not paraphrased)
- [ ] Synthesis documents follow the template structure
- [ ] No duplicate entries in source interview lists
- [ ] index.md table is properly formatted (markdown)
- [ ] All links are valid relative paths
- [ ] Frequency counts are accurate
- [ ] "Last Updated" dates are current (YYYY-MM-DD format)

## Error Handling
If errors occur:
- **Missing frontmatter**: Report which fields are missing, skip that synthesis type
- **File read/write errors**: Report the error, continue with other updates
- **Invalid markdown**: Report formatting issues, attempt to fix or skip
- **Missing template**: Report error and stop (template is required)

Always complete as many updates as possible even if some fail.

## Examples

### Example 1: After Video Transcript Analysis
**User completes video-transcript-analyzer skill**, which creates:
`interview-analysis/2025-11-15_Matthew_Ruxton_IgniteReading.md`

**Claude automatically invokes this skill** with:
- Input: Path to the newly created interview analysis file

**Skill executes**:
1. Extracts themes: ["Behavioral Data", "Accidental Admins", "Data Architecture"]
2. Extracts products: ["Index Pages", "Custom Objects", "Workspaces", "Leads"]
3. Extracts persona: "HubSpot Administrator"
4. Updates 6 existing syntheses, creates 2 new ones
5. Updates index.md
6. Reports results

### Example 2: Manual Invocation
**User says**: "Update the syntheses for the Matthew Ruxton interview"

**Claude does**:
1. Finds the most recent interview analysis file
2. Invokes the skill with that file path
3. Reports results

### Example 3: Batch Update
**User says**: "Re-sync all syntheses from scratch"

**Claude does**:
1. Clears existing syntheses (after user confirmation)
2. Loops through all interview analysis files
3. Invokes skill for each one
4. Reports cumulative results

## Notes
- This skill should be invoked automatically via a post-tool hook after video-transcript-analyzer
- The skill is idempotent - running it multiple times on the same interview is safe
- Synthesis documents use a consistent structure from _SYNTHESIS_TEMPLATE.md
- All dates use YYYY-MM-DD format
- Quotes should be verbatim from the source interview (preserve customer voice)
