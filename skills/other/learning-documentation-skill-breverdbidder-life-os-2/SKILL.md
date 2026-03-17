---
name: learning-documentation-skill
description: Document learning insights and activities to Supabase with proper categorization, formatting, and retrieval patterns
---

# Learning Documentation Skill

Systematically documents learning activities, insights, and knowledge to Life OS Supabase database.

## When to Use This Skill

- After completing learning activity (video, article, course)
- Documenting insights from experiments
- Storing reference material for future use
- Building knowledge base over time
- Creating searchable learning archive

## Supabase Structure

**Table:** `insights`  
**Location:** mocerqjnksmhcjzxrewo.supabase.co

**Required Fields:**
- `category`: Primary classification
- `subcategory`: Secondary classification  
- `title`: Brief descriptive title
- `content`: Main content (JSON for structured data)
- `metadata`: Additional context (optional)

## Category Taxonomy

### Primary Categories

**learning:**
- Subcategories: youtube_transcript, article, book, course, experiment
- Use: General knowledge acquisition

**michael_swim:**
- Subcategories: recruiting, meet_results, training, nutrition
- Use: Michael's swimming-related activities

**mcp_reference:**
- Subcategories: architecture, claude_skills, integration_patterns
- Use: MCP and Claude technical documentation

**business:**
- Subcategories: biddeed_ai, everest_capital, strategy
- Use: Business insights and decisions

**adhd:**
- Subcategories: task_patterns, interventions, productivity
- Use: ADHD management insights

**family:**
- Subcategories: shabbat, holidays, events
- Use: Family activities and observances

## YouTube Transcript Documentation

**When:** After youtube_transcript.yml workflow completes

**Format:**
```json
{
  "category": "learning",
  "subcategory": "youtube_transcript",
  "title": "Claude Skills Tutorial - 6 Essential Skills",
  "content": {
    "video_id": "thxXGxYIwUI",
    "video_url": "https://youtu.be/thxXGxYIwUI",
    "transcript_summary": "Tutorial on 6 Claude skills: frontend-design, domain-brainstormer, stripe-integration, content-writer, lead-research, skill-creator",
    "key_takeaways": [
      "Skills only load when needed (memory efficient)",
      "Progressive disclosure: ~100 tokens metadata, <5k when active",
      "Can build custom skills using skill-creator"
    ],
    "action_items": [
      "Deploy 6 base skills to both repos",
      "Build custom foreclosure-analysis-skill",
      "Create ADHD task management skill"
    ],
    "source": "apify"
  },
  "metadata": {
    "duration_minutes": 15,
    "watched_date": "2025-12-25",
    "relevance": "high"
  }
}
```

## Article/Blog Documentation

**Format:**
```json
{
  "category": "learning",
  "subcategory": "article",
  "title": "MCP Architecture Deep Dive",
  "content": {
    "url": "https://example.com/mcp-architecture",
    "author": "Anthropic",
    "published_date": "2025-01-15",
    "key_concepts": [
      "Tool-based architecture",
      "Progressive disclosure",
      "Context injection patterns"
    ],
    "quotes": [
      "Skills are prompt templates that inject domain-specific instructions"
    ],
    "personal_notes": "This explains why skills are more efficient than rules"
  }
}
```

## Experiment/Test Documentation

**Format:**
```json
{
  "category": "business",
  "subcategory": "biddeed_ai",
  "title": "Smart Router V5 Performance Test",
  "content": {
    "experiment_date": "2025-12-24",
    "hypothesis": "Gemini 2.5 Flash can handle 40-55% of requests",
    "methodology": "Run 100 auction analyses, track FREE vs PAID tier usage",
    "results": {
      "free_tier_percentage": 52,
      "paid_tier_percentage": 48,
      "cost_savings": "$28/month"
    },
    "conclusion": "Target achieved, deploying to production",
    "next_steps": [
      "Monitor for 1 week",
      "Adjust thresholds if needed"
    ]
  }
}
```

## Michael Swimming Documentation

**Meet Results:**
```json
{
  "category": "michael_swim",
  "subcategory": "meet_results",
  "title": "Harry Meisel Meet - December 2025",
  "content": {
    "meet_name": "Harry Meisel Invitational",
    "date": "2025-12-13",
    "location": "Orlando, FL",
    "results": [
      {
        "event": "50 Free",
        "time": "21.85",
        "place": 3,
        "improvement": "-0.15 from previous"
      },
      {
        "event": "100 Free", 
        "time": "47.92",
        "place": 5,
        "improvement": "-0.32 from previous"
      }
    ],
    "notes": "Strong performance, time drops across all events",
    "coach_notifications": ["UF", "FSU", "NC State"]
  }
}
```

**Recruiting Activity:**
```json
{
  "category": "michael_swim",
  "subcategory": "recruiting",
  "title": "Coach Outreach - University of Florida",
  "content": {
    "university": "University of Florida",
    "coach_name": "Anthony Nesty",
    "contact_date": "2025-12-20",
    "type": "initial_email",
    "response_received": false,
    "follow_up_date": "2026-01-03"
  }
}
```

## Markdown Formatting Standards

**For content field (when storing markdown):**

```markdown
# Title

## Key Points
- Point 1
- Point 2

## Takeaways
1. First takeaway
2. Second takeaway

## Action Items
- [ ] Action 1
- [ ] Action 2

## References
- [Source 1](url)
- [Source 2](url)
```

**Keep it clean:**
- Use headers (##) for sections
- Use bullet points for lists
- Use checkboxes for action items
- Include URLs for references
- NO excessive formatting

## Insertion Workflow

### Via GitHub Actions (Recommended)

**BidDeed.AI repo:**
```yaml
workflow: .github/workflows/insert_insight.yml
inputs:
  category: "mcp_reference"
  subcategory: "claude_skills"
  title: "Phase 1 Skills Deployed"
  content: "{json_content}"
```

**Life OS repo:**
```yaml
workflow: .github/workflows/insert_insight.yml
inputs:
  category: "learning"
  subcategory: "youtube_transcript"
  title: "Video Title"
  content: "{json_content}"
```

### Direct Supabase Insert (Use Sparingly)

Only when GitHub Actions not available:
```python
import requests

response = requests.post(
    "https://mocerqjnksmhcjzxrewo.supabase.co/rest/v1/insights",
    headers={
        "apikey": "YOUR_ANON_KEY",
        "Content-Type": "application/json"
    },
    json={
        "category": "learning",
        "subcategory": "article",
        "title": "Example Title",
        "content": {"key": "value"}
    }
)
```

## Retrieval Patterns

**Search by category:**
```sql
SELECT * FROM insights 
WHERE category = 'learning' 
ORDER BY created_at DESC 
LIMIT 10
```

**Search by keywords:**
```sql
SELECT * FROM insights
WHERE title ILIKE '%claude skills%'
OR content::text ILIKE '%claude skills%'
```

**Recent activity:**
```sql
SELECT category, subcategory, title, created_at
FROM insights
WHERE created_at > NOW() - INTERVAL '7 days'
ORDER BY created_at DESC
```

## Best Practices

### DO:
- ✓ Use consistent category/subcategory
- ✓ Write descriptive titles
- ✓ Structure content as JSON when possible
- ✓ Include action items when relevant
- ✓ Tag for future searchability

### DON'T:
- ✗ Duplicate entries (check before inserting)
- ✗ Use vague titles ("Notes", "Misc")
- ✗ Store sensitive data (API keys, passwords)
- ✗ Overwrite existing valuable entries
- ✗ Insert empty or placeholder content

## Example Usage

```
"Use learning-documentation-skill to log the Claude skills video transcript"

"Document experiment results for Smart Router V5"

"Log Michael's meet results from Harry Meisel"
```

## Integration with Other Skills

**After youtube_transcript workflow:**
```
1. Transcript generated
2. Use learning-documentation-skill
3. Log to Supabase insights table
4. Category: learning, subcategory: youtube_transcript
```

**After task completion:**
```
1. Task marked COMPLETED
2. Use learning-documentation-skill
3. Log patterns/insights discovered
4. Category: adhd, subcategory: task_patterns
```

## Critical Reminders

1. **Consistent Taxonomy:** Always use standard categories
2. **JSON Structure:** Structured data > plain text
3. **Action Items:** Extract and track actionable insights
4. **No Duplicates:** Search before inserting
5. **Future Self:** Write for searchability later
