---
name: agentic-vision
description: |
  Gemini 3 Flash Agentic Vision - The Sandwich Architecture for pixel-perfect UI generation.
  Phase 1: SURVEYOR measures layout BEFORE generation (grids, spacing, colors).
  Phase 2: QA TESTER verifies AFTER render (SSIM, diff regions, auto-fix).
  "Measure twice, cut once" - generator gets hard data, not guesses.

  Use when: video-to-code, image-to-code, UI verification, layout measurement, 
  pixel-perfect generation, SSIM comparison, auto-fix suggestions.
user-invocable: true
---

# Agentic Vision - The Sandwich Architecture

**Version**: 1.0.0
**Last Updated**: 2026-01-30

---

## What is Agentic Vision?

Agentic Vision in Gemini 3 Flash converts image understanding from a **static act** into an **agentic process**. It combines visual reasoning with **Code Execution**.

```
Think → Act → Observe loop:
1. THINK: Analyze image, formulate plan
2. ACT: Generate and execute Python code (crop, measure, annotate)
3. OBSERVE: Process results, refine understanding
```

**Key capability**: Instead of "guessing" padding is `p-4`, it MEASURES and returns `24px`.

---

## The Sandwich Architecture

```
                  REPLAY "SANDWICH" ARCHITECTURE
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│  ┌──────────┐                                                     │
│  │  Video   │──────────────────────────────┐                      │
│  │  Input   │                              │                      │
│  └────┬─────┘                              │                      │
│       │                                    ▼                      │
│       │                       ┌─────────────────────────┐         │
│       │                       │  PHASE 1: THE SURVEYOR  │         │
│       │                       │ (Agentic Vision Flash)  │         │
│       │                       ├─────────────────────────┤         │
│       │                       │ 1. Measure Grids (px)   │         │
│       │                       │ 2. Extract Colors (hex) │         │
│       │                       │ 3. Map Layout (JSON)    │ ◄─── KEY
│       │                       └────────────┬────────────┘         │
│       │                                    │                      │
│       ▼                                    ▼                      │
│  ┌──────────────┐             ┌─────────────────────────┐         │
│  │ Gemini 3 Pro │◄────────────│  Architecture Specs     │         │
│  │ (Code Gen)   │             │   (Hard Data JSON)      │         │
│  └──────┬───────┘             └─────────────────────────┘         │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐    ┌──────────────────────────────────┐         │
│  │ Render View  │───▶│      PHASE 2: THE QA TESTER      │         │
│  └──────────────┘    │     (Agentic Vision Flash)       │         │
│                      ├──────────────────────────────────┤         │
│                      │ 1. Compare Original vs Render    │         │
│                      │ 2. "Spot the difference" (SSIM)  │         │
│                      │ 3. Auto-fix suggestions          │         │
│                      └─────────────────┬────────────────┘         │
│                                        │                          │
│                                        ▼                          │
│                              ┌──────────────────┐                 │
│                              │ FINAL PIXEL-PERFECT │              │
│                              │      COMPONENT      │              │
│                              └──────────────────┘                 │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: THE SURVEYOR

Measures layout **BEFORE** code generation.

### API Endpoint

```typescript
POST /api/survey/measure
{
  imageBase64: string,      // Base64 encoded frame
  mimeType?: string,        // default: 'image/png'
  useParallel?: boolean,    // default: true (faster)
  includePromptFormat?: boolean  // Include formatted prompt for generator
}
```

### Response

```typescript
{
  success: true,
  measurements: {
    imageDimensions: { width: 1920, height: 1080 },
    grid: { columns: 12, gap: "24px" },
    spacing: {
      sidebarWidth: "256px",
      navHeight: "64px",
      cardPadding: "24px",
      sectionGap: "48px",
      containerPadding: "32px"
    },
    colors: {
      background: "#0f172a",
      surface: "#1e293b",
      primary: "#6366f1",
      text: "#ffffff",
      textMuted: "#94a3b8",
      border: "#334155"
    },
    typography: {
      h1: "48px",
      h2: "32px",
      body: "16px",
      small: "14px"
    },
    components: [
      { type: "sidebar", bbox: {...}, confidence: 0.95 }
    ],
    confidence: 0.91
  },
  promptFormat: "... formatted for code generator ..."
}
```

### Code Usage

```typescript
import { runParallelSurveyor, formatSurveyorDataForPrompt } from '@/lib/agentic-vision';

// 1. Run Surveyor on video frame
const { measurements } = await runParallelSurveyor(frameBase64, 'image/png');

// 2. Inject into code generator prompt
const prompt = `
${SYSTEM_PROMPT}

${formatSurveyorDataForPrompt(measurements)}

Generate code based on the video above.
`;

// 3. Generator uses EXACT values: p-[24px] not p-4
```

---

## Phase 2: THE QA TESTER

Verifies generated UI **AFTER** render.

### API Endpoint

```typescript
POST /api/verify/diff
{
  originalImageBase64: string,    // Original frame from video
  generatedImageBase64: string,   // Screenshot of generated code
  mimeType?: string,              // default: 'image/png'
  quickCheck?: boolean,           // Only SSIM, skip full analysis
  includeReport?: boolean         // Include formatted text report
}
```

### Response

```typescript
{
  success: true,
  verification: {
    ssimScore: 0.94,
    overallAccuracy: "94%",
    verdict: "needs_fixes",  // "pass" | "needs_fixes" | "major_issues"
    issues: [
      {
        type: "spacing",
        severity: "medium",
        location: "card padding",
        description: "Card padding is 16px, should be 24px",
        expected: "24px",
        actual: "16px"
      }
    ],
    autoFixSuggestions: [
      {
        selector: ".card",
        property: "padding",
        suggestedValue: "24px",
        confidence: 0.85
      }
    ]
  },
  report: "✅ QA VERIFICATION REPORT..."
}
```

### Verdict Rules

| Verdict | Condition |
|---------|-----------|
| `pass` | SSIM >= 0.95 AND no high severity issues |
| `needs_fixes` | SSIM >= 0.85 AND <= 3 high severity issues |
| `major_issues` | SSIM < 0.85 OR > 3 high severity issues |

---

## Enabling Code Execution

Agentic Vision requires `codeExecution` tool in Gemini API:

```typescript
import { GoogleGenAI } from '@google/genai';

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const response = await ai.models.generateContent({
  model: 'gemini-3-flash',
  contents: [
    { text: prompt },
    { inlineData: { data: imageBase64, mimeType: 'image/png' } }
  ],
  config: {
    tools: [{ codeExecution: {} }]  // <-- CRITICAL
  }
});

// Response contains:
// - executableCode: { code: "Python code..." }
// - codeExecutionResult: { outcome: "OUTCOME_OK", output: "JSON result" }
```

---

## Available Python Libraries in Sandbox

```python
# Data Science
import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn import preprocessing

# Image Processing
from PIL import Image
from skimage import filters, measure, transform
from skimage.metrics import structural_similarity as ssim

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Utilities
import io
import json
```

---

## Technical Considerations

### 1. Coordinate Normalization

Gemini may rescale images internally. Always request BOTH:
- Normalized coordinates (0.0-1.0)
- Image dimensions for backend rescaling

```python
def normalize_bbox(x, y, w, h, img_width, img_height):
    return {
        "x": x / img_width,
        "y": y / img_height,
        "width": w / img_width,
        "height": h / img_height
    }
```

### 2. Parallel Execution for Speed

Run color sampling and spacing measurement in parallel:

```typescript
const [colors, spacing] = await Promise.all([
  surveyColors(frame),      // Fast
  surveySpacing(frame)      // Heavier CV
]);
// Time reduced by ~50%
```

### 3. SSIM with scikit-image

Use industry-standard SSIM calculation:

```python
from skimage.metrics import structural_similarity as ssim

score, diff_image = ssim(img1, img2, full=True)
# score: 0.0 (different) to 1.0 (identical)
# diff_image: per-pixel difference map
```

---

## Integration with Replay Pipeline

### Before (Without Surveyor)

```
Video → Gemini Pro "guesses" → p-4 or p-6? → 3-5 iterations
```

### After (With Sandwich Architecture)

```
Video → Surveyor MEASURES → padding: 24px → Generator EXECUTES → 1-2 iterations
```

**Result**: First generation is 80% better!

---

## File Structure

```
lib/agentic-vision/
├── index.ts          # Main exports
├── types.ts          # TypeScript interfaces
├── prompts.ts        # Surveyor & QA prompts
├── surveyor.ts       # Phase 1 implementation
└── qa-tester.ts      # Phase 2 implementation

app/api/
├── survey/measure/route.ts    # Surveyor endpoint
└── verify/diff/route.ts       # QA Tester endpoint
```

---

## Quick Start

```typescript
// Full pipeline with Agentic Vision

// 1. PHASE 1: Measure before generation
const surveyResult = await fetch('/api/survey/measure', {
  method: 'POST',
  body: JSON.stringify({ 
    imageBase64: videoFrame,
    includePromptFormat: true 
  })
});
const { measurements, promptFormat } = await surveyResult.json();

// 2. Generate code with HARD DATA
const codeResult = await generateWithConstraints(video, promptFormat);

// 3. Render and screenshot
const screenshot = await renderAndCapture(codeResult.code);

// 4. PHASE 2: Verify
const qaResult = await fetch('/api/verify/diff', {
  method: 'POST',
  body: JSON.stringify({
    originalImageBase64: videoFrame,
    generatedImageBase64: screenshot
  })
});
const { verification } = await qaResult.json();

// 5. Check result
if (verification.verdict === 'pass') {
  console.log('✅ Pixel-perfect!');
} else {
  console.log('⚠️ Apply fixes:', verification.autoFixSuggestions);
}
```

---

## References

- [Google Blog: Agentic Vision in Gemini 3 Flash](https://blog.google/technology/developers/agentic-vision-gemini-3-flash/)
- [Gemini API Code Execution Docs](https://ai.google.dev/gemini-api/docs/code-execution)
- [scikit-image SSIM](https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.structural_similarity)
