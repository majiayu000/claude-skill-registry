---
name: brand
description: Brand context management for marketing sessions with continuity across conversations
keywords: [brand, client, context, marketing, switch, manage]
---

# Brand Management

Manage marketing brands and client context with session continuity.

---

## The Iron Law

```
NO MARKETING WORK WITHOUT BRAND CONTEXT
```

If brand context isn't loaded, recommendations are generic.
Always confirm brand is active before marketing tasks.

---

## Commands

```
/brand                    Show active brand or list all
/brand list               List all brands
/brand new                Create a new brand
/brand switch <name>      Switch to a different brand
/brand info               Show detailed brand info
/brand update             Update brand information
/brand add-competitor     Add a competitor
/brand add-note           Add a note
```

---

## Natural Language Detection

Detect these patterns and route to brand management:

| User Says | Action |
|-----------|--------|
| "working on [name]" | Switch to brand |
| "new client" / "new brand" | Create brand |
| "switch to [name]" | Switch to brand |
| "who am I working with" | Show active brand |
| "my brands" / "list clients" | List all brands |

---

## Brand Context Gate

BEFORE any marketing task, verify:

1. **Is a brand active?**
   - If yes: Proceed with context
   - If no: "Which brand are you working on? Use `/brand switch [name]` or `/brand new`"

2. **Do I have needed context?**
   - Industry? Product? Audience? Competitors?
   - If missing critical info: Ask or note the gap

---

## Session Continuity

### When Switching Brands

1. **Save current session** → Creates handoff with:
   - Completed tasks
   - In-progress tasks
   - Key decisions made

2. **Load new brand** → Shows:
   - Last session summary
   - Pending tasks
   - Recommended next steps

### Handoff Display

```
📋 RESUMING: [Brand Name]

**Last session:** [Date]

✅ **Completed:**
- [Task 1]
- [Task 2]

🔄 **In Progress:**
- [Task 3]

📌 **Recommended Next:**
- [Priority action]

Ready to continue. What would you like to focus on?
```

---

## Brand Creation Flow

When user says `/brand new` or "new client":

### Step 1: Basic Info (Required)
1. "What's the brand/company name?"
2. "What's the website URL?"

### Step 2: Business Context (Required)
3. "What do they sell? (product/service)"
4. "What industry are they in?"
5. "Who's their target audience?"

### Step 3: Competitive Context (Optional but Valuable)
6. "Who are 2-3 main competitors?"
7. "What makes this brand different from them?"

### Step 4: Current State (Optional)
8. "What marketing channels are they currently using?"
9. "Any specific goals or challenges?"

**After completion:**
```
✅ Brand created: [Name]

📊 Profile Summary:
- Website: [url]
- Industry: [industry]
- Product: [product]
- Audience: [audience]
- Competitors: [list]

Brand is now active. What would you like to work on?
- Keyword research
- Positioning
- Content planning
- Channel strategy
```

---

## Brand Info Display

When user says `/brand info`:

```
📁 BRAND: [Name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 **Website:** [url]
📅 **Created:** [date]
📅 **Last session:** [date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Business
- **Industry:** [industry]
- **Product:** [product/service]
- **Model:** [B2B/B2C/etc]
- **USP:** [unique selling prop]

## Audience
- **Primary:** [persona]
- **Secondary:** [if set]
- **Geography:** [markets]

## Competitors
- [competitor 1] - [your angle]
- [competitor 2] - [your angle]

## Current Marketing
- **Active channels:** [list]
- **Performance:** [summary if known]

## Notes
- [date]: [note]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Actions:**
- `/brand update` - Update information
- `/brand add-competitor [domain]` - Add competitor
- `/brand add-note [note]` - Add note
```

---

## Progressive Loading

Load brand context in stages to optimize tokens:

| Stage | When | Tokens |
|-------|------|--------|
| **Metadata** | Always | ~50 |
| **Instructions** | On activation | ~200 |
| **Full profile** | On `/brand info` | ~500+ |
| **History** | On request | Variable |

Don't load full profile unless needed.

---

## Red Flags - STOP

If you catch yourself:
- Giving marketing advice without active brand → STOP, ask which brand
- Making recommendations without knowing industry → STOP, get context
- Assuming audience without brand data → STOP, load brand first
- Skipping brand context for "quick question" → STOP, context matters

---

## Storage

Brand data stored locally:
- Location: `~/.claude-marketing/brands/`
- Format: JSON files (e.g., `brandname.json`)
- State file: `~/.claude-marketing/state.json`
- One file per brand

When creating a brand, write JSON format:
```json
{
  "id": "brand-id",
  "name": "Brand Name",
  "website": "https://example.com",
  "industry": "Industry",
  "product": "Product description",
  "audience": "Target audience",
  "competitors": ["competitor1.com", "competitor2.com"]
}
```

When setting active brand, update state.json:
```json
{
  "activeBrand": "brand-id"
}
```

User owns their data. No cloud sync.

---

## Verification Checklist

BEFORE any marketing recommendation:

- [ ] Brand is active?
- [ ] I know the product/service?
- [ ] I know the target audience?
- [ ] I know key competitors (or noted as unknown)?
- [ ] Industry context loaded?

If any unchecked: Get context first.
