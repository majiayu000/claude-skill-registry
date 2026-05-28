---
name: infographic-generator
description: Generate world-class medical infographics using carousel-level visual language. Templates include hero stats, multi-section layouts, comparisons, myth-busters, process flows, and patient checklists. Default 1080x1350 for Instagram.
---

# Infographic Generator

Generate publication-grade infographics that match your carousel visual quality. Uses mesh gradients, bold typography, icons, and branded footers.

## World-Class Templates

| Template | Use Case | Visual Style |
|----------|----------|--------------|
| `infographic-hero` | Single key stat | Giant gradient stat badge, icon, branded footer |
| `infographic-dense` | Multi-section content | Grid of styled cards with icons |
| `infographic-comparison` | Drug vs drug, treatment options | Split layout with contrast colors |
| `infographic-myth` | Debunking misconceptions | Red/Green split with icons |
| `infographic-process` | Workflows, algorithms | Numbered steps with connectors |
| `infographic-checklist` | Patient prep, guides | Styled checkbox items |

## Quick Start

### Single Infographic

```bash
# Hero stat infographic
python skills/cardiology/infographic-generator/scripts/infographic_cli.py \
  --template infographic-hero \
  --data '{"stat":"26%","label":"Mortality Reduction","context":"HR 0.74 (95% CI 0.65-0.85)","source":"PARADIGM-HF","icon":"chart-down","tag":"CLINICAL TRIAL"}' \
  --output outputs/hero-paradigm.png

# Dense multi-section
python skills/cardiology/infographic-generator/scripts/infographic_cli.py \
  --template infographic-dense \
  --data '{"tag":"PATIENT GUIDE","title":"GLP-1 Roll-Off","icon":"pill","sections":[{"title":"Who this is for","bullets":["Stable HF patients","No recent decompensation"],"icon":"people"},{"title":"Red flags","bullets":["Weight gain >2kg/week","New edema"],"icon":"warning","accent":"danger"}],"callout":{"label":"Key","text":"Monitor weekly during taper"}}' \
  --output outputs/dense-glp1.png

# Comparison
python skills/cardiology/infographic-generator/scripts/infographic_cli.py \
  --template infographic-comparison \
  --data '{"tag":"TREATMENT CHOICE","title":"ACE-I vs ARB","left":{"label":"ACE Inhibitors","stat":"22%","statLabel":"Mortality Reduction","icon":"pill","bullets":["First-line","More cough"],"theme":"primary"},"right":{"label":"ARBs","stat":"18%","statLabel":"Mortality Reduction","icon":"shield","bullets":["ACE-I intolerant","Better tolerated"],"theme":"accent"}}' \
  --output outputs/comparison-acei-arb.png

# Myth buster
python skills/cardiology/infographic-generator/scripts/infographic_cli.py \
  --template infographic-myth \
  --data '{"tag":"MYTH BUSTED","title":"Statins cause muscle damage","myth":{"text":"Taking statins will definitely give you muscle pain"},"truth":{"text":"Only 5-10% experience symptoms, most can continue therapy"},"evidence":"Meta-analysis of 19 RCTs","source":"Lancet 2022"}' \
  --output outputs/myth-statins.png

# Process flow
python skills/cardiology/infographic-generator/scripts/infographic_cli.py \
  --template infographic-process \
  --data '{"tag":"ALGORITHM","title":"Starting SGLT2 Inhibitors","steps":[{"title":"Screen","description":"Confirm HFrEF, check eGFR","icon":"magnify"},{"title":"Initiate","description":"Start at recommended dose","icon":"pill"},{"title":"Monitor","description":"Check creatinine at 1-2 weeks","icon":"chart-up"}],"note":"eGFR ≥20 for most agents"}' \
  --output outputs/process-sglt2.png

# Checklist
python skills/cardiology/infographic-generator/scripts/infographic_cli.py \
  --template infographic-checklist \
  --data '{"tag":"PATIENT CHECKLIST","title":"Before Your Stress Test","icon":"heart","categories":[{"title":"24 Hours Before","items":[{"text":"Avoid caffeine"},{"text":"Continue medications"}]},{"title":"Day of Test","items":[{"text":"Wear comfortable shoes"},{"text":"Bring medication list"}]}],"callout":{"icon":"warning","text":"Tell staff about chest pain"}}' \
  --output outputs/checklist-stress.png
```

### Batch Generation

Generate multiple infographics from a config file (perfect for content campaigns):

```bash
# From JSON config
python skills/cardiology/infographic-generator/scripts/batch_generate.py \
  --config examples/batch_demo.json

# Parallel generation (faster)
python skills/cardiology/infographic-generator/scripts/batch_generate.py \
  --config examples/batch_demo.json \
  --parallel 4

# Validate config without generating
python skills/cardiology/infographic-generator/scripts/batch_generate.py \
  --config my_config.json \
  --dry-run
```

**Example batch config** (`examples/batch_demo.json`):
```json
[
  {
    "template": "infographic-hero",
    "data": {
      "stat": "26%",
      "label": "Mortality Reduction",
      "source": "PARADIGM-HF",
      "icon": "chart-down",
      "tag": "CLINICAL TRIAL"
    },
    "output": "outputs/hero-paradigm.png"
  },
  {
    "template": "infographic-myth",
    "data": {
      "tag": "MYTH BUSTED",
      "title": "Statins cause muscle damage",
      "myth": {"text": "Taking statins will give you pain"},
      "truth": {"text": "Only 5-10% experience symptoms"}
    },
    "output": "outputs/myth-statins.png"
  }
]
```

**Batch Features:**
- ✅ Validate all configs before generating
- ✅ Parallel generation (1-8 workers)
- ✅ Stop on first error (optional)
- ✅ JSON or YAML config formats
- ✅ Progress tracking

## Template Data Schemas

### infographic-hero
```json
{
  "stat": "26%",
  "label": "Mortality Reduction",
  "context": "HR 0.74, 95% CI 0.65-0.85",
  "source": "PARADIGM-HF Trial",
  "icon": "chart-down",
  "tag": "CLINICAL TRIAL",
  "theme": "primary|success|accent|dark",
  "showFooter": true,
  "footerName": "Dr. Shailesh Singh",
  "footerHandle": "@heartdocshailesh"
}
```

### infographic-dense
```json
{
  "tag": "PATIENT GUIDE",
  "title": "GLP-1 Roll-Off in Heart Patients",
  "subtitle": "A practical tapering guide",
  "icon": "pill",
  "sections": [
    {
      "title": "Who this is for",
      "bullets": ["Stable HF patients", "No recent decompensation"],
      "icon": "people",
      "accent": "teal|danger|success|accent"
    }
  ],
  "callout": { "label": "Bottom line", "text": "..." },
  "footer": "Educational infographic. Not medical advice.",
  "showBrandFooter": true
}
```

### infographic-comparison
```json
{
  "tag": "TREATMENT COMPARISON",
  "title": "ACE-I vs ARB in HFrEF",
  "left": {
    "label": "ACE Inhibitors",
    "stat": "22%",
    "statLabel": "Mortality Reduction",
    "icon": "pill",
    "bullets": ["First-line therapy", "More cough"],
    "theme": "primary|success|accent|danger"
  },
  "right": {
    "label": "ARBs",
    "stat": "18%",
    "statLabel": "Mortality Reduction",
    "icon": "shield",
    "bullets": ["ACE-I intolerant", "Better tolerated"],
    "theme": "accent"
  },
  "source": "Meta-analysis, Circulation 2022"
}
```

### infographic-myth
```json
{
  "tag": "MYTH BUSTED",
  "title": "Statins cause muscle damage in everyone",
  "myth": {
    "text": "Taking statins will definitely give you muscle pain",
    "icon": "cross"
  },
  "truth": {
    "text": "Only 5-10% experience symptoms, most can continue",
    "icon": "check"
  },
  "evidence": "Meta-analysis of 19 RCTs (n=71,000)",
  "source": "Lancet 2022"
}
```

### infographic-process
```json
{
  "tag": "TREATMENT ALGORITHM",
  "title": "Starting SGLT2 Inhibitors",
  "subtitle": "Step-by-step for clinicians",
  "steps": [
    { "title": "Screen", "description": "Confirm HFrEF", "icon": "magnify" },
    { "title": "Initiate", "description": "Start at dose", "icon": "pill" },
    { "title": "Monitor", "description": "Check creatinine", "icon": "chart-up" }
  ],
  "note": "eGFR ≥20 for most agents"
}
```

### infographic-checklist
```json
{
  "tag": "PATIENT CHECKLIST",
  "title": "Before Your Stress Test",
  "subtitle": "Complete preparation guide",
  "icon": "heart",
  "categories": [
    {
      "title": "24 Hours Before",
      "items": [
        { "text": "Avoid caffeine", "checked": false },
        { "text": "Continue medications", "checked": false }
      ]
    }
  ],
  "callout": { "icon": "warning", "text": "Tell staff about chest pain" }
}
```

## Available Icons

**Medical:** pill, heart, heart-pulse, stethoscope, syringe, blood-drop, dna, microscope, brain, lungs, bone, hospital, ambulance, doctor

**Charts:** chart-up, chart-down, graph

**Status:** check, cross, warning, stop, star, fire, lightning, target, bulb, trophy, shield, clock, magnify, books, people

**Arrows:** arrow-up, arrow-down, arrow-right

## Visual Design System

All templates use:
- **Mesh gradients** (layered radials, not flat colors)
- **Font weights:** 900 for headlines, 300 for subtitles
- **3x+ size jumps** for hierarchy
- **Icon containers** with styled backgrounds
- **Gradient stat badges** with shadows
- **Branded footer** with handle

## Defaults

- **Size:** 1080x1350 (Instagram portrait, 4:5)
- **Font:** Helvetica/Arial
- **Brand colors:** Teal (#16697A), Coral (#EF5350), Success (#27AE60)

## Output Location

Default: `skills/cardiology/visual-design-system/outputs/infographics/`

## Python API

```python
from skills.cardiology.visual_design_system.scripts.generate_infographic import generate

result = generate(
    "infographic-hero",
    {
        "stat": "26%",
        "label": "Mortality Reduction",
        "source": "PARADIGM-HF",
        "icon": "chart-down",
        "tag": "LANDMARK TRIAL"
    },
    "output.png",
    width=1080,
    height=1350
)

if result["success"]:
    print(f"Generated: {result['output']}")
```
