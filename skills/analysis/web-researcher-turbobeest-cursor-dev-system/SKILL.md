# Web Researcher Skill

## Metadata
- skill_name: web-researcher
- activation_code: WEB_RESEARCHER_V1
- version: 2.0.0
- category: research
- phase: 1, 2 (Ideation and Discovery only)

## Description

Web research capability using Claude Code's built-in WebSearch and WebFetch tools. Helps gather external context during early pipeline phases - competitor analysis, market research, technical patterns, and design inspiration. Results feed into PRD context sections, not core requirements.

**Key principle:** This skill enriches understanding, it does not define requirements. The user's vision remains primary; external research provides supporting context only.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     WEB RESEARCHER SKILL                        │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │COMPETITOR│          │TECHNICAL│          │ MARKET  │
   │ RESEARCH │          │PATTERNS │          │RESEARCH │
   └────┬────┘          └────┬────┘          └────┬────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌─────────────────┐
                    │   BUILT-IN      │
                    │   WebSearch +   │
                    │   WebFetch      │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  .research/     │
                    │  findings.json  │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ PRD Section 3   │
                    │ (Market Context)│
                    └─────────────────┘
```

## Tools Available

This skill uses Claude Code's **built-in tools** - no external API keys or MCP configuration required:

| Tool | Purpose | Example |
|------|---------|---------|
| **WebSearch** | Search the web for information | Find competitors, market data, trends |
| **WebFetch** | Fetch and analyze specific URLs | Get API docs, read product pages |

## Activation

**User-triggered only.** This skill never activates automatically.

**Trigger phrases:**
- `research competitors`
- `find similar products`
- `market research`
- `what else exists`
- `competitor analysis`
- `technical research`
- `how do others solve this`

**Explicit activation:**
```
> research competitors for scheduling apps
> research technical patterns for real-time collaboration
```

## Research Modes

### 1. Competitor Research

**Process:**
1. Use WebSearch to find competitors: `"[product type] competitors 2025"`
2. Use WebFetch to analyze top results
3. Extract: name, pricing, features, differentiators

**Example prompt to Claude:**
```
Research 5 competitors for scheduling apps. For each:
- Product name and URL
- Pricing (free tier, paid plans)
- Key features (top 5)
- Target audience
- Main differentiator

Also synthesize:
- Common features across all
- Gaps/opportunities
- Pricing range
```

**Output:**
```json
{
  "research_type": "competitor",
  "query": "scheduling apps",
  "findings": [
    {
      "name": "Calendly",
      "url": "https://calendly.com",
      "pricing": {"free": true, "paid_from": "$10/mo"},
      "key_features": ["calendar sync", "team scheduling", "integrations"],
      "target_audience": "professionals, sales teams",
      "differentiator": "simplicity, brand recognition"
    }
  ],
  "synthesis": {
    "common_features": ["calendar sync", "notifications"],
    "gaps": ["AI scheduling", "group consensus"],
    "pricing_range": "$0-50/mo"
  }
}
```

### 2. Technical Patterns Research

**Process:**
1. Use WebSearch: `"[capability] implementation patterns best practices"`
2. Use WebFetch on technical blogs, docs, GitHub repos
3. Extract: patterns, libraries, trade-offs

**Example prompt to Claude:**
```
Research technical approaches for real-time collaboration.
For each approach:
- Pattern/approach name
- Who uses it (real examples)
- Pros and cons
- Implementation complexity
- Recommended libraries/tools

Provide a recommendation for a new project.
```

**Output:**
```json
{
  "research_type": "technical",
  "query": "real-time collaboration",
  "findings": [
    {
      "pattern": "Operational Transformation",
      "used_by": ["Google Docs"],
      "pros": ["proven at scale", "handles conflicts"],
      "cons": ["complex to implement"]
    },
    {
      "pattern": "CRDTs",
      "used_by": ["Figma", "Linear"],
      "pros": ["simpler conflict resolution", "offline-first"],
      "cons": ["memory overhead"]
    }
  ],
  "recommendation": "CRDTs for new projects, OT if Google Docs-level scale needed"
}
```

### 3. Market Research

**Process:**
1. Use WebSearch: `"[domain] market size trends 2025"`
2. Use WebFetch on industry reports, news articles
3. Extract: market size, trends, players

**Example prompt to Claude:**
```
Research market data for project management software.
Extract:
- Market size (current and projected)
- Growth rate
- Key players
- Current trends
- Underserved segments or opportunities

Focus on actionable insights for a new entrant.
```

**Output:**
```json
{
  "research_type": "market",
  "query": "project management software",
  "findings": {
    "market_size": "$6.7B (2024)",
    "growth_rate": "13.7% CAGR",
    "key_players": ["Asana", "Monday", "Notion", "ClickUp"],
    "trends": ["AI automation", "all-in-one platforms", "async-first"],
    "underserved_segments": ["solo developers", "creative agencies"]
  }
}
```

## Output Files

Research results should be saved to:
```
.research/
├── findings.json           # Structured research data
├── competitor-analysis.md  # Human-readable competitor summary
├── technical-patterns.md   # Technical approaches summary
└── market-context.md       # Market research summary
```

### findings.json Schema
```json
{
  "version": "1.0",
  "created_at": "2025-12-19T10:00:00Z",
  "research_sessions": [
    {
      "id": "r-001",
      "type": "competitor",
      "query": "scheduling apps",
      "timestamp": "2025-12-19T10:00:00Z",
      "sources_checked": 5,
      "findings": [...],
      "synthesis": {...}
    }
  ],
  "prd_integration": {
    "section_3_market": "...",
    "section_5_competitors": "...",
    "section_8_technical": "..."
  }
}
```

## PRD Integration

Research findings map to specific PRD sections:

| Research Type | PRD Section | Integration |
|---------------|-------------|-------------|
| Competitor | Section 3 (Market Context) | Competitive landscape summary |
| Competitor | Section 5 (Anti-Requirements) | "Unlike X, we will NOT..." |
| Technical | Section 8 (Architecture) | Pattern recommendations |
| Market | Section 3 (Market Context) | Market size, trends |
| Market | Section 4 (Success Criteria) | Market-informed metrics |

### Integration Example

**Research finding:**
```json
{
  "type": "competitor",
  "name": "Calendly",
  "gap": "No AI-powered optimal time suggestion"
}
```

**PRD Section 3 addition:**
```markdown
### Competitive Landscape
- Calendly: Market leader, simple UX, lacks AI scheduling
- Cal.com: Open source alternative, developer-focused
- **Our differentiation:** AI-powered optimal time suggestion
```

**PRD Section 5 addition:**
```markdown
### Anti-Requirements (What We Won't Build)
- Unlike Calendly, we will NOT require manual availability setting
```

## Plan Guardian Integration

Research-sourced additions are flagged for Plan Guardian:

```json
{
  "source": "web_research",
  "research_id": "r-001",
  "confidence": "external",
  "added_to_prd": true
}
```

Plan Guardian treats externally-sourced content with **higher scrutiny**:
- Default confidence penalty: -0.15
- Requires explicit user acknowledgment to include in core requirements
- Logged separately in guardian audit trail

## Usage Examples

### Example 1: Competitor Research During Ideation
```
User: I want to build a better note-taking app

Claude: Before we dive into specifics, would you like me to
research existing note-taking apps to understand the landscape?

User: yes, research competitors

[Claude uses WebSearch to find "note-taking app competitors 2025"]
[Claude uses WebFetch to analyze top results]

Claude: I found 5 major competitors:
1. Notion - All-in-one workspace, $8-15/mo
2. Obsidian - Local-first, plugin ecosystem, free/$8/mo
3. Roam - Bidirectional linking pioneer, $15/mo
4. Logseq - Open source Roam alternative
5. Apple Notes - Simple, free, Apple ecosystem

Common gaps I noticed:
- AI-powered organization (emerging)
- Cross-device sync without cloud (privacy)
- Collaborative editing + local-first (hard problem)

Would you like to differentiate in any of these areas?
```

### Example 2: Technical Research During Discovery
```
User: The app needs real-time collaboration. Research technical patterns.

[Claude uses WebSearch for "real-time collaboration patterns CRDT OT"]
[Claude uses WebFetch on technical articles]

Claude: I researched real-time collaboration patterns:

1. **CRDTs** (Conflict-free Replicated Data Types)
   - Used by: Figma, Linear
   - Pros: Offline-first, automatic conflict resolution
   - Cons: Memory overhead, complex for rich text

2. **Operational Transformation**
   - Used by: Google Docs
   - Pros: Proven at scale, precise cursor tracking
   - Cons: Requires central server, complex algorithm

3. **Yjs** (CRDT Library)
   - Open source, TypeScript, active community
   - Powers: BlockSuite, Tiptap collaboration

Recommendation for your use case: Yjs with WebRTC for
peer-to-peer sync, falls back to WebSocket server.

Want me to add this to the Architecture section of the PRD?
```

### Example 3: Market Research
```
User: What's the market like for project management tools?

[Claude uses WebSearch for "project management software market 2025"]
[Claude uses WebFetch on market reports]

Claude: Market research findings:

**Market Size:** $6.7B (2024), growing 13.7% CAGR
**Key Players:** Asana, Monday.com, Notion, ClickUp, Linear

**Trends:**
- AI automation (task creation, prioritization)
- All-in-one platforms (docs + tasks + wiki)
- Async-first workflows (remote work)

**Underserved Segments:**
- Solo developers (too complex)
- Creative agencies (need visual workflows)
- Hardware teams (need physical + digital)

This context could help position your product.
Which segment interests you?
```

## Configuration

### .claude/research-config.json (Optional)
```json
{
  "enabled": true,
  "max_sources_per_query": 5,
  "research_modes": ["competitor", "technical", "market"],
  "auto_integrate_to_prd": false,
  "require_user_confirmation": true,
  "cache_duration_hours": 24
}
```

## Limitations

1. **Web access required:** Research uses live web search
2. **Accuracy:** AI-extracted data should be verified for critical decisions
3. **Freshness:** Check publication dates on sources
4. **Scope:** Only activates in Phase 1-2; disabled after PRD approval

## Signals

| Signal | Trigger |
|--------|---------|
| RESEARCH_STARTED | Skill activates |
| RESEARCH_COMPLETE | Findings returned |
| RESEARCH_INTEGRATED | Findings added to PRD |
| RESEARCH_SKIPPED | User declined research |

## See Also

- Ideation skill (Phase 1 - triggers research option)
- Discovery skill (Phase 2 - can request research)
- Plan Guardian (monitors research-sourced additions)
- PRD Template (sections that receive research data)
