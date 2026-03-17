---
name: newsletter-events-add-source
description: Add Instagram accounts or web aggregators to sources.yaml configuration
---

<required_reading>
STOP. Before doing ANYTHING else, you MUST read this entire file.

This skill uses a dispatcher pattern with separate workflows:
- For web URLs → Read `workflows/add-web-aggregator.md` (HAS MANDATORY PROFILING)
- For Instagram → Read `workflows/add-instagram.md`

DO NOT just edit sources.yaml directly. Follow the workflows.
</required_reading>

<essential_principles>
## Configuration Location

All sources are stored in `~/.config/local-media-tools/sources.yaml`.

## Source Types & Routing

| Type | Detection | Workflow |
|------|-----------|----------|
| Instagram | `@handle` or alphanumeric handle | `workflows/add-instagram.md` |
| Web Aggregator | `http://` or `https://` URL | `workflows/add-web-aggregator.md` |
| Facebook | `facebook.com/events/*` | Not stored - use `/research` directly |

## Key Differences

- **Instagram**: Simple add - no profiling needed
- **Web Aggregator**: Requires profiling to discover optimal scraping strategy
</essential_principles>

<intake>
What sources do you want to add?

**Examples:**
- `@localvenue @musicbar` - Add Instagram accounts
- `https://hudsonvalleyevents.com` - Add web aggregator (will be profiled)
- `@venue1 and https://events.com` - Mix of sources

**Note:** For Facebook events, use `/research https://facebook.com/events/123456` instead.

Provide the source(s):
</intake>

<process>
## Step 1: Parse and Classify Input

Analyze user input and classify each source:

```python
import re

sources = {"instagram": [], "web": [], "facebook": []}

for token in user_input.replace(",", " ").replace(" and ", " ").split():
    token = token.strip()
    if not token:
        continue

    if "facebook.com/events/" in token:
        sources["facebook"].append(token)
    elif token.startswith("@") or re.match(r"^[a-zA-Z][a-zA-Z0-9_.]+$", token):
        sources["instagram"].append(token.lstrip("@").lower())
    elif token.startswith("http://") or token.startswith("https://"):
        sources["web"].append(token)
```

## Step 2: Handle Facebook URLs

If any Facebook URLs detected, inform user:

```
Facebook events are not stored in configuration.
Pass URLs directly to /research instead:

  /research https://facebook.com/events/123456
```

Continue processing other sources.

## Step 3: Route to Workflows

### For Instagram handles:
If `sources["instagram"]` is not empty:
1. Read `workflows/add-instagram.md`
2. Follow that workflow for all Instagram handles
3. Collect results

### For Web URLs:
If `sources["web"]` is not empty:
1. Read `workflows/add-web-aggregator.md`
2. Follow that workflow for EACH web URL (profiling is per-source)
3. Collect results

**IMPORTANT:** Process web sources one at a time since each requires interactive profiling.

## Step 4: Report Combined Results

After both workflows complete, display combined summary:

| Type | Source | Name | Status |
|------|--------|------|--------|
| Instagram | @localvenue | Local Venue | Added |
| Instagram | @musicbar | Music Bar | Already exists |
| Web | greatnortherncatskills.com | Great Northern Catskills | Added (profiled) |

```
Config saved to ~/.config/local-media-tools/sources.yaml
Run /newsletter-events:research to scrape these sources.
```
</process>

<success_criteria>
- [ ] All sources parsed and classified by type
- [ ] Facebook URLs identified with redirect message
- [ ] Instagram sources processed via `workflows/add-instagram.md`
- [ ] Web sources processed via `workflows/add-web-aggregator.md` (with profiling)
- [ ] Combined results displayed to user
</success_criteria>
