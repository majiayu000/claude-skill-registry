---
name: data-analysis
description: AI-powered data analysis for Empathy Ledger - themes, quotes, story suggestions, transcript analysis.
---

# Data Analysis

Patterns for AI-powered analysis: themes, quotes, summaries, and story suggestions.

## When to Use
- Adding quotes to story cards
- Implementing story suggestions/related content
- Building theme-based filtering or search
- Creating analytics dashboards
- Integrating AI analysis results

## Quick Reference

### Analysis Pipeline
```
Transcript → AI Analysis → themes[], key_quotes[], ai_summary
Story → Connections → Related Stories, Suggested Content
```

### Key Tables
| Table | Analysis Fields |
|-------|-----------------|
| `transcripts` | `themes`, `key_quotes`, `ai_summary`, `ai_processing_status` |
| `stories` | `themes`, `cultural_tags`, `featured_quote` |
| `storytellers` | `expertise_themes`, `connection_strength` |

### Theme Categories
- **cultural**: identity, heritage, tradition, language, ceremony
- **family**: kinship, elders, children, ancestors, community
- **land**: country, connection, seasons, wildlife, sacred-sites
- **resilience**: survival, adaptation, strength, healing, hope
- **knowledge**: wisdom, teaching, learning, stories, dreams

### Common Queries
```sql
-- Stories with matching theme
SELECT * FROM stories WHERE themes && ARRAY['identity', 'heritage'];

-- Theme frequency
SELECT unnest(themes) as theme, count(*) FROM stories GROUP BY theme ORDER BY count DESC;
```

### API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `POST /api/transcripts/{id}/analyze` | Trigger AI analysis |
| `GET /api/stories/{id}/suggestions` | Get related stories |
| `GET /api/themes` | List themes with counts |

## Reference Files
| Topic | File |
|-------|------|
| Code patterns | `refs/analysis-patterns.md` |
| SQL queries | `refs/supabase-queries.md` |
| Theme hierarchy | `refs/theme-taxonomy.md` |
| Sync status | `refs/sync-status.md` |

## Related Skills
- `database-navigator` - Database exploration
- `supabase-connection` - Database clients
- `design-component` - UI patterns for analysis display
