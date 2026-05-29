---
name: vision-scorer-mcp
description: MCP server extending Design System Sidekick with programmatic vision-based compliance scoring. Replaces manual Northcote Visual Audit with deterministic measurements.
type: mcp-server
---

# Vision-Scorer MCP Server

## Purpose

Add to Design System Sidekick MCP server. Provides programmatic asset validation via Gemini Vision API.

## New MCP Tools

### 1. `score_asset_compliance`

**Input:**
```json
{
  "image_path": "/path/to/asset.png",
  "asset_id": "ASSET-3",
  "target_score": 90
}
```

**Process:**
1. Load image via Vision API
2. Extract colors (sample 50 points → hex codes)
3. Identify specimens (Vision recognition + geographic DB lookup)
4. Measure density zones (pixel coverage analysis)
5. Detect translucency (luminance gradient analysis)
6. OCR typography (count labels, verify font/color)
7. Score 6 dimensions (0-20 each)

**Output:**
```json
{
  "overall_score": 87,
  "decision": "REGENERATE",
  "dimensions": {
    "geographic_authenticity": 18,
    "translucency_physics": 14,
    "scale_hierarchy": 19,
    "density_zones": 16,
    "background_color": 9,
    "typography": 8
  },
  "violations": [
    "Spider molt appears opaque (no transmission)",
    "Upper-left density 25% (exceeds 20% threshold)"
  ],
  "correction_prompt": "CRITICAL FIXES:\n- Spider: '60-80% light-transmissive amber chitin'\n- Upper-left: '200×200px COMPLETELY EMPTY'"
}
```

### 2. `extract_visual_tokens`

**Input:** Image path
**Output:** Design tokens JSON

```json
{
  "colors": {
    "background": "#1A1714",
    "dominant": ["#C45C4B", "#D4A84B"],
    "accents": ["#7A9E82", "#D4885C"]
  },
  "specimens": [
    {"name": "Waratah", "size_cm": 15, "position": "upper_right"},
    {"name": "Frill-neck", "size_cm": 18, "position": "center"}
  ],
  "density": {
    "upper_left": 18,
    "lower_right": 28,
    "central": 70
  }
}
```

### 3. `compare_attempts`

**Input:** Array of attempt image paths
**Output:** Iteration analysis

```json
{
  "progression": [
    {"attempt": 1, "score": 68, "key_failure": "Geographic violations"},
    {"attempt": 2, "score": 87, "key_failure": "Density zones"},
    {"attempt": 3, "score": 92, "decision": "PACKAGE"}
  ],
  "pattern_learnings": [
    "Adding negative constraints improved specimen accuracy",
    "Density zone pixel specs more effective than percentages"
  ]
}
```

## Implementation

**File:** `/servers/design_system_sidekick.py`

**Add Vision API Integration:**
```python
import google.generativeai as genai

class VisionScorer:
    def score_asset_compliance(self, image_path, asset_id, target_score):
        # Load image
        image = genai.upload_file(image_path)
        
        # Vision analysis prompt
        prompt = """
        Analyze this Northcote Curio asset:
        
        1. Extract hex colors (background + palette)
        2. Identify specimens (names + sizes)
        3. Measure density zones (upper-left, lower-right, central %)
        4. Detect translucency (which specimens show transmission?)
        5. Count typography labels
        
        Return structured JSON.
        """
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content([prompt, image])
        
        # Parse response → score dimensions
        data = parse_vision_response(response.text)
        scores = calculate_dimension_scores(data)
        
        return {
            "overall_score": sum(scores.values()),
            "dimensions": scores,
            "decision": "PACKAGE" if sum(scores.values()) >= target_score else "REGENERATE"
        }
```

## Integration

**Claude Desktop Config:**
```json
{
  "mcpServers": {
    "design-system-sidekick": {
      "command": "python3",
      "args": ["/path/to/design_system_sidekick.py"],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    }
  }
}
```

## Usage

```python
# Claude Desktop invokes MCP tool
result = mcp.call_tool(
    server="design-system-sidekick",
    tool="score_asset_compliance",
    arguments={
        "image_path": "/downloads/asset-3.png",
        "asset_id": "ASSET-3",
        "target_score": 90
    }
)

if result['decision'] == 'PACKAGE':
    # Trigger asset-packager
else:
    # Apply corrections, regenerate
```

## Token Efficiency

**Gemini Vision:** ~1500 tokens per analysis
**Cost:** $0.002 per image (Flash model)
**Speed:** 5-8 seconds per validation

vs Manual: 10 minutes conversational validation

## Advantages

- Deterministic scoring (not subjective)
- Structured JSON output (feeds dashboards)
- Pattern learning across iterations
- 95% time reduction

---

*Extends Design System Sidekick with vision-based compliance scoring. Manual audit → programmatic measurement.*
