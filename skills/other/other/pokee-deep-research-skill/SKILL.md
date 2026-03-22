---
name: pokee-deep-research
description: Conduct deep research using Pokee AI's Deep Research API. Generates comprehensive, structured research reports with outlines and detailed writeups. Use when the user needs thorough research, competitive analysis, market research, academic research, or any topic requiring detailed investigation. Takes 7-25 minutes per query and produces publication-quality reports.
---

# Pokee Deep Research

Deep research for when surface-level answers aren't enough. Powered by Pokee's academic-grade research engine.

---

## Quick Start (3 Steps)

**Install:**
```bash
mkdir -p ~/.openclaw/skills && cd ~/.openclaw/skills
git clone https://github.com/Niraven/pokee-deep-research-skill.git pokee-deep-research
cd pokee-deep-research
```

**Configure:**
```bash
python3 scripts/setup.py
```
*Get your free token at https://pokee.ai*

**Research:**
```bash
./scripts/pokee-research.sh "Your research question"
```

---

## When to Use This

✓ Competitive intelligence  
✓ Market landscape analysis  
✓ Pre-meeting deep dives  
✓ Technology evaluations  
✓ Any question where "I searched it" isn't enough  

---

## Output

Results in `~/.openclaw/workspace/research-output/`:

- **`*_outline.md`** — Structured overview (read this first)
- **`*_writeup.md`** — Full report with analysis (~50-70 KB)
- **`*_response.json`** — Raw API response

---

## Requirements

- Python 3.7+
- `pip3 install requests`
- Pokee API token (free tier available)

---

## About the Engine

Pokee Deep Research doesn't just find information — it synthesizes it. The 7-25 minute runtime reflects genuine analysis: building outlines, comparing sources, structuring findings into actionable intelligence.

[Learn more at pokee.ai](https://pokee.ai)
