---
name: faion-product-research
description: "Product research: market, competitors, personas, validation, pricing. Triggers: market research, competitor analysis."
user-invocable: false
allowed-tools: Read, Write, Glob, Task, AskUserQuestion, TodoWrite
---

# Product Research Orchestrator

**Communication: User's language. Docs: English.**

## Agents

| Agent | Output |
|-------|--------|
| faion-market-researcher-agent | market-research.md |
| faion-competitor-analyzer-agent | competitive-analysis.md |
| faion-persona-builder-agent | user-personas.md |
| faion-problem-validator-agent | problem-validation.md |
| faion-pricing-researcher-agent | pricing-research.md |

## Workflow

```
1. Parse project from ARGUMENTS
2. Read: constitution.md, roadmap.md
3. AskUserQuestion: modules + mode (quick/deep)
4. Run agents SEQUENTIALLY (not parallel)
5. Write executive-summary.md
```

## Execution

```python
AGENTS = {
    "market": "faion-market-researcher-agent",
    "competitors": "faion-competitor-analyzer-agent",
    "personas": "faion-persona-builder-agent",
    "validation": "faion-problem-validator-agent",
    "pricing": "faion-pricing-researcher-agent"
}

for module in selected_modules:
    Task(
        subagent_type=AGENTS[module],
        prompt=f"""
PROJECT: {project}
PRODUCT: {product_description}
MODE: {quick|deep}
OUTPUT: aidocs/sdd/{project}/product_docs/{output_file}
"""
    )
```

## Module Selection

```python
AskUserQuestion(
    questions=[{
        "question": "Які модулі запустити?",
        "multiSelect": True,
        "options": [
            {"label": "Market Research", "description": "TAM/SAM/SOM, trends"},
            {"label": "Competitors", "description": "Features, pricing"},
            {"label": "Personas", "description": "Pain points, JTBD"},
            {"label": "Validation", "description": "Problem evidence"},
            {"label": "Pricing", "description": "Benchmarks"}
        ]
    }]
)
```

## Output

```
aidocs/sdd/{project}/product_docs/
├── market-research.md
├── competitive-analysis.md
├── user-personas.md
├── problem-validation.md
├── pricing-research.md
├── executive-summary.md
└── gtm-manifest/              # Optional, after research complete
    └── gtm-manifest-full.md
```

## Next Step

After research complete, offer:
→ "Створити GTM Manifest?" → Call `faion-gtm-manifest` skill

## Rules

- Run agents ONE BY ONE
- Agents cite sources with URLs
- If data not found → "Data not available"
- Quick: 3-5 searches, Deep: 8-12 searches
