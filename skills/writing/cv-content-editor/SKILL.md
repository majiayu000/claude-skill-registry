---
name: cv-content-editor
description: Edit and update existing CV content using the knowledge base as source of truth. Use when user wants to modify case studies, update experience, refine variants, or improve existing content.
---

# CV Content Editor

<purpose>
Edit existing portfolio content by cross-referencing the knowledge base to ensure consistency and accuracy. Maintains the source of truth in `content/knowledge/` while updating presentation-layer files.
</purpose>

<when_to_activate>
Activate when the user:
- Wants to update an existing case study
- Needs to modify experience highlights
- Wants to refine a variant's messaging
- Asks to improve or expand existing content
- Needs to sync content with knowledge base updates

**Trigger phrases:** "update", "edit", "modify", "change", "improve", "fix [content]"
</when_to_activate>

## Two-Way Sync Philosophy

```
Knowledge Base (Source of Truth)     Presentation Layer (Output)
─────────────────────────────────    ──────────────────────────
content/knowledge/                   content/case-studies/
├── achievements/                    content/experience/
├── stories/                         content/variants/
└── metrics/                         content/blog/
         ↓ generates                         ↑ informs
         ↓                                   ↑
    [EDITING FLOW: Update knowledge → Regenerate presentation]
```

## Content Editing Workflow

### Step 1: Identify What to Edit
1. Read the target file user wants to modify
2. Identify which knowledge base entities it draws from
3. Query `content/knowledge/index.yaml` for relationships

### Step 2: Determine Edit Scope

| Edit Type | Scope | Files to Update |
|-----------|-------|-----------------|
| Factual correction | Knowledge base | Achievement/story → regenerate presentation |
| Messaging refinement | Presentation only | Case study/variant directly |
| New achievement | Knowledge base first | New achievement → update case study |
| Metric update | Knowledge base | Achievement metric → sync to presentation |

### Step 3: Execute Edit

#### For Knowledge Base Updates
1. Edit the source file in `content/knowledge/achievements/` or `stories/`
2. Update `content/knowledge/index.yaml` if relationships changed
3. Regenerate affected presentation files

#### For Presentation-Only Updates
1. Read current file
2. Apply targeted edits (preserve structure)
3. Validate against schema

### Step 4: Validate Consistency
- Knowledge base and presentation should not contradict
- Metrics should match across files
- Tags/themes should align with index

## Edit Patterns

### Pattern 1: Update Achievement Metric
**User**: "Update the Ankr revenue to $2.5M ARR"

**Workflow**:
```
1. Edit: content/knowledge/achievements/ankr-15x-revenue.yaml
   - Update metric.value and result section

2. Sync: content/case-studies/04-ankr-rpc.md
   - Update hook.impactMetric
   - Update Results section

3. Sync: content/experience/index.yaml
   - Update Ankr highlights if affected
```

### Pattern 2: Improve Case Study Narrative
**User**: "Make the ETH staking case study more compelling"

**Workflow**:
```
1. Read: content/knowledge/stories/galaxy-compliance-win.yaml
   - Understand the core narrative

2. Read: content/case-studies/01-eth-staking.md
   - Identify weak sections

3. Edit: Case study directly
   - Strengthen hook
   - Add concrete details from story
   - Improve key quote

4. Consider: Backport improvements to story if substantial
```

### Pattern 3: Update Variant for New Role
**User**: "Update the Bloomberg variant with new achievements"

**Workflow**:
```
1. Read: content/knowledge/achievements/*.yaml
   - Find new relevant achievements

2. Read: content/variants/bloomberg-technical-product-manager.yaml
   - Understand current positioning

3. Edit: Variant YAML
   - Add new achievements to relevant sections
   - Update relevance scores
   - Regenerate JSON

4. Validate: Test variant URL still works
```

### Pattern 4: Add New Experience Highlight
**User**: "Add a highlight about shipping 3 protocols in parallel"

**Workflow**:
```
1. Check: Does achievement exist?
   - If not, create in content/knowledge/achievements/

2. Edit: content/experience/index.yaml
   - Add highlight to appropriate company

3. Consider: Update related case study if relevant
```

## Content Validation

After any edit, verify:

### Schema Validation
```bash
npm run validate
```

### Cross-Reference Check
- [ ] Achievement metrics match case study metrics
- [ ] Experience highlights reflect achievements
- [ ] Variant relevance scores are justified
- [ ] Index relationships are current

### Consistency Check
- [ ] Same achievement = same numbers everywhere
- [ ] Company names consistent
- [ ] Dates/periods consistent
- [ ] Tags match knowledge base themes

## Common Edit Commands

| User Says | Action |
|-----------|--------|
| "Update the numbers" | Edit achievement → sync presentation |
| "Make it more compelling" | Edit presentation narrative |
| "Add this achievement" | Create achievement → update presentation |
| "Fix inconsistency" | Identify source of truth → sync all |
| "Improve this section" | Targeted presentation edit |

## Output Format

When editing, always:
1. Show the diff (what changed)
2. List all files updated
3. Note if knowledge base was modified
4. Suggest running validation

Example output:
```
Updated files:
- content/knowledge/achievements/ankr-15x-revenue.yaml (metric update)
- content/case-studies/04-ankr-rpc.md (synced metric)

Knowledge base updated: Yes
Run validation: npm run validate
```
