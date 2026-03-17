---
name: gemini-research
description: Use Gemini CLI for research with Google Search grounding and 1M token context
allowed-tools: Bash, Read, Write, TodoWrite, WebFetch, Glob, Grep
---

# Gemini Research Skill



---

## LIBRARY-FIRST PROTOCOL (MANDATORY)

**Before writing ANY code, you MUST check:**

### Step 1: Library Catalog
- Location: `.claude/library/catalog.json`
- If match >70%: REUSE or ADAPT

### Step 2: Patterns Guide
- Location: `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md`
- If pattern exists: FOLLOW documented approach

### Step 3: Existing Projects
- Location: `D:\Projects\*`
- If found: EXTRACT and adapt

### Decision Matrix
| Match | Action |
|-------|--------|
| Library >90% | REUSE directly |
| Library 70-90% | ADAPT minimally |
| Pattern exists | FOLLOW pattern |
| In project | EXTRACT |
| No match | BUILD (add to library after) |

---

## Purpose

Route research tasks to Gemini CLI when:
- Real-time information is needed (Google Search grounding)
- Context exceeds Claude's 200k limit (Gemini has 1M)
- Need web-grounded factual answers

## Unique Capability

**What Gemini Does Better**:
- Google Search grounding for current information
- 1M token context for massive document analysis
- 70+ extensions (Figma, Stripe, Shopify, etc.)
- Web content analysis with source attribution

## When to Use

### Perfect For:
- Current events, recent documentation
- Large codebase analysis (>150k tokens)
- Literature reviews with many papers
- Real-time API documentation lookup
- Market research, competitor analysis

### Don't Use When:
- Offline/airgapped environments
- Complex multi-step reasoning (use Claude)
- Code generation requiring iteration (use Codex)

## Usage

### Basic Research
```bash
/gemini-research "What are the latest React 19 best practices?"
```

### With Context Files
```bash
/gemini-research "Analyze architecture" --context @src/
```

### Large Document Analysis
```bash
/gemini-research "Summarize all papers" --context papers/*.pdf
```

## Command Pattern

```bash
bash scripts/multi-model/gemini-research.sh "<query>" "<task_id>" "json"
```

## Memory Integration

Results stored to Memory-MCP:
- Key: `multi-model/gemini/research/{task_id}`
- Tags: WHO=gemini-cli, WHY=research

## Output Format

```json
{
  "content": "Research findings...",
  "sources": ["url1", "url2"],
  "model": "gemini-2.5-pro",
  "timestamp": "2025-12-28T..."
}
```

## Handoff to Claude

After Gemini research completes:
1. Results stored in Memory-MCP
2. Claude agents read from memory key
3. Use research to inform implementation

```javascript
// Claude agent reads Gemini research
const research = memory_retrieve("multi-model/gemini/research/{task_id}");
Task("Coder", `Implement using: ${research.content}`, "coder");
```

## Configuration

- Retries: 3 attempts on failure
- Timeout: 60 seconds per query
- Fallback: Claude researcher agent if Gemini unavailable
