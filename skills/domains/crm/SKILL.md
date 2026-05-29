---
name: crm
description: Research people and companies, add to CRM database with smart linking
---

# CRM Skill

**Telegram Skill** - Invoke with `/crm` (no parameters)

This is a Telegram skill. When invoked with `/crm`, the skill will prompt you for the query to research and add people or companies to the Database with intelligent linking and relationship discovery.

## Input Detection

The skill auto-detects entity type from query:

| Input Type | Example | Action |
|------------|---------|--------|
| Email | `john@anthropic.com` | Research person + company from domain |
| Person name | `John Doe` | Research person only |
| Person + company | `John Doe at Anthropic` | Research both, link them |
| Company name | `Anthropic` | Research company |
| Company domain | `anthropic.com` | Research company |
| LinkedIn URL (person) | `linkedin.com/in/username` | Research person |
| LinkedIn URL (company) | `linkedin.com/company/name` | Research company |

## Execution Flow

### Phase 1: Entity Detection & Duplicate Check

1. **Parse Input**: Determine if query is person, company, or both
2. **Check Duplicates**:
   - **People**: Match by email > LinkedIn URL > name (case-insensitive)
   - **Companies**: Match by domain > LinkedIn > name
   - If fuzzy match found, ask user to confirm
   - If multiple matches, show differentiators and let user decide

### Phase 2: Research

#### For Person:
Use web search to find:
- LinkedIn profile (priority)
- Current company and role
- Email address (if not provided)
- Twitter/X profile
- Location
- Professional background and achievements
- Recent news or notable projects

#### For Company:
Use web search to find:
- Company website
- LinkedIn company page
- Industry and description
- Company stage (seed/series-a/public/etc)
- Company size (employee count)
- Location (headquarters)
- Twitter/X handle
- Recent news or funding announcements

**Research Best Practices:**
- Verify information from multiple sources
- Focus on publicly available professional information only
- Clearly indicate uncertain/unavailable information
- Add research date and sources for reference

### Phase 3: Smart Linking

#### Person → Company Linking:
1. If person's company is found during research
2. Check if company exists in `Database/Companies/`
3. If company doesn't exist:
   - Ask user: "Would you like me to create a company entry for [Company Name]?"
   - If yes, research and create company entry
4. Link person to company via `company: "[[Database/Companies/Company-Name]]"` field

#### Company → People Discovery:
When researching a company, offer to find key people:
- Ask user: "Would you like me to research key people at [Company Name] (founders, executives, decision-makers)?"
- If yes:
  - Search for 3-5 key people (founders, C-suite, VPs)
  - Show list of found people with roles
  - Ask: "Which of these people should I add to the database?"
  - Create entries for selected people with company links

#### Person → Coworkers Discovery:
When researching a person, offer to find coworkers:
- Ask user: "Would you like me to search for [Person]'s coworkers at [Company]?"
- If yes:
  - Search for people at the same company (LinkedIn, team pages)
  - Show list of found coworkers with roles
  - Ask: "Which coworkers should I add to the database?"
  - Create entries for selected people with company links

### Phase 4: Create or Update Entry

#### If Updating Existing Entry:
- Read current file completely
- Merge new information with existing data
- **PRESERVE** all user-added content:
  - Notes section
  - Interaction history
  - Custom tags
  - Relationship info
  - Next actions
- Add update note with date at bottom
- Only update fields with new/better information

#### If Creating New Entry:

**Person Entry:**
- Filename: `First-Last.md` (e.g., `John-Doe.md`)
- Use `Database/People/Person-Template.md` structure
- Include all found information
- Link to company if identified
- Set relationship type (contact by default)
- Add research date and sources

**Company Entry:**
- Filename: `Company-Name.md` (e.g., `Anthropic.md`)
- Use `Database/Companies/Company-Template.md` structure
- Include all found information
- Set relationship type (prospect by default)
- Add research date and sources
- Include Contacts Base query for dynamic people list

## File Structure Templates

### Person Entry:
```markdown
---
type: person
company: "[[Database/Companies/Company-Name]]"
role: VP Engineering
email: person@company.com
linkedin: https://linkedin.com/in/username
twitter: https://twitter.com/username
location: San Francisco, CA
relationship: contact
last_contact:
next_action:
created: 2026-01-21
tags:
  - person
  - contact
---

# Full Name

## Role & Background

Current role and background information.

## Contact Information

- Email: [[email]]
- LinkedIn: [[linkedin]]
- Twitter: [[twitter]]
- Location: [[location]]
- Company: [[company]]

## Relationship

Type: [[relationship]]
How we know each other, context of relationship.

## Interaction History

### YYYY-MM-DD
Notes from meeting/interaction...

## Tasks & Projects

Related tasks or projects involving this person.

```base
filters:
  and:
    - file.inFolder("Database/Tasks")
    - assignee == link(this.file)
views:
  - type: table
    name: Tasks
    order:
      - status
      - priority
```

## Notes

Additional context, interests, preferences, etc.

---
*Research Date: [current date]*
*Sources: [list sources]*
```

### Company Entry:
```markdown
---
type: company
industry: Industry Name
stage: startup
size: 1-10
location: City, Country
website: https://example.com
linkedin: https://linkedin.com/company/name
twitter: https://twitter.com/company
relationship: prospect
last_interaction:
next_action:
tags:
  - company
  - prospect
---

# Company Name

## Overview

Brief description of what the company does.

## Details

- **Industry**: [[industry]]
- **Stage**: [[stage]] (seed/series-a/series-b/public/etc)
- **Size**: [[size]] employees
- **Location**: [[location]]
- **Website**: [[website]]

## Relationship

Type: [[relationship]] (prospect/partner/client/vendor/investor/etc)
Context of relationship.

## Contacts

People we know at this company:

```base
filters:
  and:
    - file.inFolder("Database/People")
    - company == link(this.file)
views:
  - type: table
    name: Contacts
    order:
      - role
      - file.name
```

## Interaction History

### YYYY-MM-DD
Notes from meeting/interaction...

## Projects & Opportunities

Related projects or business opportunities.

## Notes

Additional context, competitive intel, etc.

---
*Research Date: [current date]*
*Sources: [list sources]*
```

## Response Format

**IMPORTANT**: Never mention file paths (Database/People/, Database/Companies/) or file extensions (.md) in responses. Only mention entity names (person names, company names).

### New Person Entry:
```
✅ Research completed for [Person Name]
📍 Person profile created

Key Info:
• Role: [Job Title] at [Company]
• Location: [Location]
• Email: [Yes/No]
• LinkedIn: [Yes/No]

[2-3 sentence summary of background]

Company: [Created/Linked to existing] [Company Name]
Sources: [N] reviewed
```

### New Company Entry:
```
✅ Research completed for [Company Name]
📍 Company profile created

Key Info:
• Industry: [Industry]
• Stage: [Stage]
• Size: [Size]
• Location: [Location]

[2-3 sentence summary of what they do]

Sources: [N] reviewed
```

### Updated Entry:
```
✅ Research completed for [Person/Company Name]
📍 [Person/Company] profile updated

Updates:
• [What changed]
• [What changed]

Sources: [N] reviewed
```

### With Related Entities Added:
```
✅ Added [N] people from [Company Name]

📍 [Person Name]
→ [Role] | [Key background points]

📍 [Person Name]
→ [Role] | [Key background points]

All linked to [Company Name].
```

## User Interaction Examples

### Example 1: Email Input with Company Creation
```
User: /crm
Assistant: Please provide the person or company you'd like to research.
User: john@anthropic.com
Assistant: [Searches for John and Anthropic]
Assistant: Found John Doe, VP of Engineering at Anthropic.
Anthropic doesn't exist in the database yet.
Would you like me to create a company entry for Anthropic?
User: yes
Assistant: [Creates both entries, links them]
✅ Research completed for John Doe
📍 Person profile created
📍 Company profile created: Anthropic
```

### Example 2: Company with People Discovery
```
User: /crm
Assistant: Please provide the person or company you'd like to research.
User: Anthropic
Assistant: [Researches Anthropic]
Would you like me to research key people at Anthropic (founders, executives)?
User: yes
Assistant: [Searches for key people]
Found the following key people at Anthropic:
1. Dario Amodei - CEO & Co-founder
2. Daniela Amodei - President & Co-founder
3. Tom Brown - Co-founder

Which of these people should I add to the database? (You can select multiple or say "all")
User: 1 and 2
Assistant: [Creates entries for Dario and Daniela]
✅ Added 2 people from Anthropic

📍 Dario Amodei
→ CEO & Co-founder

📍 Daniela Amodei
→ President & Co-founder

All linked to Anthropic.
```

### Example 3: Person with Coworkers Discovery
```
User: /crm
Assistant: Please provide the person or company you'd like to research.
User: Jane Smith at Example Corp
Assistant: [Researches Jane Smith]
Would you like me to search for Jane's coworkers at Example Corp?
User: yes
Assistant: [Searches for coworkers]
Found the following coworkers:
1. Bob Johnson - VP Sales
2. Alice Chen - Director of Engineering
3. Mike Davis - Product Manager

Which coworkers should I add? (You can select multiple or say "all")
User: skip
Assistant: [Creates only Jane's entry]
✅ Research completed for Jane Smith
📍 Person profile created
```

## Best Practices

### Duplicate Prevention:
- Always check duplicates BEFORE researching
- Match by email (highest priority), then LinkedIn, then name
- For names, check variations (John vs J., Smith vs Smyth)
- If uncertain, ask user to confirm

### Information Quality:
- Verify from multiple sources when possible
- Mark uncertain information clearly
- Don't invent information if not found
- Save partial information rather than nothing

### User Experience:
- Always ask before adding related entities
- Show clear options for user selection
- Provide context (roles, differentiators) in choices
- Allow "skip" or "none" as valid responses

### File Management:
- Use consistent filename conventions
- Preserve all user-added content when updating
- Document what changed and when
- Include research date and sources

### Relationship Context:
- Default to "contact" for people, "prospect" for companies
- If context suggests different relationship, use appropriate type
- Document how/why entity was added in Relationship section

## Relationship Types

### For People:
- `contact` - General external contact (default)
- `colleague` - Team member or coworker
- `client` - Customer or client contact
- `partner` - Partnership or collaboration contact
- `investor` - Investor or VC contact

### For Companies:
- `prospect` - Potential client or partner (default)
- `partner` - Active partnership
- `client` - Paying customer
- `vendor` - Service provider to us
- `investor` - Current or potential investor
- `competitor` - Competitive intelligence

## Tone

Professional, factual, organized, efficient. Focus on actionable information without fluff.
