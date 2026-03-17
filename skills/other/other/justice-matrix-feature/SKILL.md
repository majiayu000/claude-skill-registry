---
name: justice-matrix-feature
description: Feature Justice Matrix items for storytelling and content creation
---

# Justice Matrix Feature Skill

## When to Use
- Highlighting a case or campaign for storytelling
- Creating content angles for Ralph Stories
- Generating interview questions
- Creating Australian context reflections
- Cross-jurisdiction analysis

## Commands

| Command | Purpose |
|---------|---------|
| `/ralph-matrix-feature [id]` | Feature a case/campaign for storytelling |
| `/ralph-matrix-interview [id]` | Generate interview questions for case/campaign |
| `/ralph-matrix-reflect [id]` | Create Australian context reflection |
| `/ralph-matrix-compare [id1] [id2]` | Cross-jurisdiction comparison |

## Feature Workflow

When an item is featured:

```
1. Mark featured=true in database
2. Set featured_at timestamp
3. Generate story brief for Ralph Stories
4. Identify interview subjects
5. Create content angles
```

## Content Types

| Type | Purpose | Output |
|------|---------|--------|
| **Case Analysis** | Legal breakdown, precedent impact | Technical article |
| **Campaign Spotlight** | Advocacy deep-dive, tactics | Feature story |
| **Interview** | Q&A with lawyers, advocates | Interview script |
| **Reflection** | What this means for Australia | Opinion piece |
| **Comparison** | Cross-jurisdiction analysis | Comparative article |

## Story Brief Generation

### For Cases

```json
{
  "type": "case_analysis",
  "title": "[Case citation] - [Issue Summary]",
  "hook": "Why this matters for youth justice",
  "legal_breakdown": {
    "court": "...",
    "issue": "...",
    "holding": "...",
    "precedent_value": "..."
  },
  "australian_relevance": "...",
  "interview_targets": ["type of expert"],
  "content_angles": ["angle 1", "angle 2"]
}
```

### For Campaigns

```json
{
  "type": "campaign_spotlight",
  "title": "[Campaign name] - [Goal Summary]",
  "hook": "Why this campaign matters",
  "campaign_breakdown": {
    "organizations": "...",
    "goals": "...",
    "tactics": "...",
    "status": "..."
  },
  "lessons_for_australia": "...",
  "interview_targets": ["organizer type"],
  "content_angles": ["angle 1", "angle 2"]
}
```

## Interview Question Templates

### Case - Legal Expert
1. What makes [case] significant for youth justice?
2. How does this precedent apply to other jurisdictions?
3. What were the key legal arguments?
4. What impact has this had since the decision?
5. How might this apply to Australian cases?

### Campaign - Advocate
1. What inspired this campaign?
2. What tactics proved most effective?
3. What challenges did you face?
4. What advice would you give to other advocates?
5. What's next for the campaign?

## Australian Reflection Framework

For each featured item, consider:

1. **Parallels**: What similar issues exist in Australia?
2. **Differences**: What contextual differences matter?
3. **Opportunities**: How could Australian advocates apply this?
4. **Challenges**: What barriers exist to applying this here?
5. **Partners**: Who in Australia should know about this?

## Integration with Ralph Stories

Featured items automatically generate briefs for the Ralph Stories pipeline:

```typescript
// When featuring an item
await supabase.from('ralph_story_briefs').insert({
  source_type: 'justice_matrix',
  source_id: item.id,
  brief_type: contentType,
  brief_data: generatedBrief,
  status: 'pending'
});
```

## Database Updates

When featuring:

```sql
UPDATE justice_matrix_cases
SET featured = true, featured_at = NOW()
WHERE id = $1;
```

## Example Usage

```bash
# Feature a landmark case
/ralph-matrix-feature uk-rwanda-2023

# Generate interview questions
/ralph-matrix-interview au-malaysia-2011

# Create Australian reflection
/ralph-matrix-reflect ecthr-hirsi-2012

# Compare two cases
/ralph-matrix-compare uk-rwanda-2023 au-malaysia-2011
```
