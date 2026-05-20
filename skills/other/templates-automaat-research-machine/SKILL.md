# Research Skill Template

For skills that aggregate information from multiple sources.

---

```yaml
---
name: {skill-name}
description: {Research X from multiple sources with synthesis}
argument-hint: "[topic] [--focus area] [--since date]"
allowed-tools: WebSearch, WebFetch, Read, Write
user-invocable: true
---
```

# {Skill Name}

{Description of research domain and purpose.}

## Arguments

Parse from `$ARGUMENTS`:

- **topic:** Required — What to research
- **--focus:** Optional — Narrow scope (default: all)
- **--since:** Optional — Date range (default: past 7 days)

## State Files

### Last Run

```text
./findings/{skill-name}/.last-run
```

Format: `YYYY-MM-DD`

### Covered Items

```text
./findings/{skill-name}/.covered-items
```

Format: One URL/ID per line. Keep last 500.

## Workflow

### Phase 1: Setup

1. Read `sources.md` for search patterns
2. Read `output-template.md` for format
3. Parse arguments
4. Read `.last-run` — set date range
5. Read `.covered-items` — for deduplication

### Phase 2: Research

Search patterns from `sources.md`:

```text
{topic} {date_range}
site:{source1} {topic}
site:{source2} {topic}
"{topic}" best OR latest
```

Collect:
- {Data point 1}
- {Data point 2}
- {Data point 3}

### Phase 3: Synthesis

1. Deduplicate within session
2. Filter against `.covered-items`
3. Rank by {criteria}
4. Categorize into sections

### Phase 4: Generate Output

1. Load `output-template.md`
2. Fill sections with findings
3. Format per template

### Phase 5: Save

**Write output:**
```text
./findings/{skill-name}/{topic}-{date}.md
```

**Update state:**
```text
./findings/{skill-name}/.last-run → today's date
./findings/{skill-name}/.covered-items → append new URLs
```

## Output Requirements

- Source URLs for all items
- {Domain-specific format}
- Emojis for section headers
- Bullet points over paragraphs

## Error Handling

- **No results:** Broaden search, try alternative terms
- **Source unavailable:** Log and continue with others
- **Minimum not met:** Expand date range, retry

## Quality Checklist

- [ ] At least {N} sources cited
- [ ] No duplicate items
- [ ] All items have URLs
- [ ] State files updated
