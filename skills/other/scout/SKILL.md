---
name: scout
description: Explore codebase or research a question. Delegates to Scout agent for fast, thorough exploration.
user-invocable: true
arguments:
  - name: question
    description: What to explore or find out (optional - will ask if not provided)
    required: false
---

# Scout - Quick Exploration

Delegate exploration tasks to the Scout agent (haiku model - fast & cheap).

## Usage

```
/scout how does authentication work here?
/scout where is the database schema defined?
/scout what options do we have for caching?
/scout                    # will ask what to explore
```

## Process

1. If no question provided, ask: "What do you want to explore?"

2. Delegate to Scout agent:
```
"Scout, explore: [question]

Context:
- Project: [current directory/project name]
- Relevant area: [if obvious from question]

Return:
- What you found
- How it works
- Options (if applicable)
- Unknowns or questions for Tako"
```

3. Present Scout's findings to Tako

4. Ask: "Want me to dig deeper on anything?"

## When to Use

- "How does X work in this codebase?"
- "Where is Y implemented?"
- "What are our options for Z?"
- "Find all places that do X"
- Before starting work on unfamiliar area
- Quick research on approaches

## Scout's Strengths

- Fast (haiku model)
- Systematic (follows code paths, checks tests, looks at git history)
- Evidence-based (cites files and line numbers)
- Surfaces unknowns (doesn't hide gaps)

## Examples

**Exploring a feature:**
```
/scout how does the scraper handle rate limiting?
```

**Finding implementations:**
```
/scout where are all the API endpoints defined?
```

**Researching options:**
```
/scout what libraries could we use for PDF generation?
```

**Understanding patterns:**
```
/scout what's the error handling pattern in this codebase?
```
