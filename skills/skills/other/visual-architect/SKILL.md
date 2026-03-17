---
name: paper-visualizer
description: Transform research papers into professional visual schemas. Analyzes paper logic, selects optimal layout patterns, and generates detailed prompts for AI image generation.
---


# Paper Visualizer Skill

Top-tier Scientific Visual Architect. Transforms text into geometric, structural visual instructions.

## 1. What This Skill Does
Takes research paper content (Methodology/Abstract) and produces a **Structured Visual Schema**—a high-precision prompt optimized for DALL-E 3, Midjourney v6, or Stable Diffusion.

## 2. Execution Logic (The Brain)

### Phase 1: Layout Pattern Recognition
You must analyze the text and enforce one of these strictly:
1. **Linear Pipeline**: Left→Right flow (Data Processing, Encoding-Decoding).
2. **Cyclic/Iterative**: Center loop (Optimization, RL, Feedback Loops).
3. **Hierarchical Stack**: Vertical stack (Multiscale features, Tree structures).
4. **Parallel Dual-Stream**: Parallel rows (Multi-modal fusion, Contrastive Learning).
5. **Central Hub**: Core connecting peripherals (Agent-Environment).
6. **Matrix Grid**: Comparison studies or ablation components.

### Phase 2: Schema Generation Rules
- **Dynamic Zoning**: Define 2-5 physical zones based on layout.
- **Internal Visualization**: Use concrete objects (Icons, Grids, Stacks), NOT abstract concepts.
- **Explicit Connections**: Describe physics of flow (e.g., "Curved arrow looping back").

## 3. Output Format (The Golden Schema)

You MUST respond strictly using this Markdown template. Use the examples in brackets `[...]` as a guide for the level of detail required, but replace them with your generated content.

```markdown
---BEGIN PROMPT---

[Style & Meta-Instructions]
High-fidelity scientific schematic, technical vector illustration, clean white background, distinct boundaries, academic textbook style. High resolution 4k, strictly 2D flat design with subtle isometric elements.

**[TEXT RENDERING RULES]**
* **Typography**: Use bold, sans-serif font (e.g., Helvetica/Roboto style) for maximum legibility.
* **Hierarchy**: Prioritize correct spelling for MAIN HEADERS (Zone Titles). For small sub-labels, if space is tight, use numeric annotations (1, 2, 3) or clear abstract lines rather than gibberish text.
* **Contrast**: Text must be dark grey/black on light backgrounds. Avoid overlapping text on complex textures.

[LAYOUT CONFIGURATION]
* **Selected Layout**: [e.g., Cyclic Iterative Process with 3 Nodes]
* **Composition Logic**: [e.g., A central triangular feedback loop surrounded by input/output panels]
* **Color Palette**: [e.g., Professional Pastel (Azure Blue, Slate Grey, Coral Orange, Mint Green)]

[ZONE 1: LOCATION - LABEL]
* **Container**: [Shape description, e.g., Top-Left Rectangular Panel]
* **Visual Structure**: [Concrete objects, e.g., A stack of 3 layered documents with binary code patterns]
* **Key Text Labels**: "[Text 1]"

[ZONE 2: LOCATION - LABEL]
* **Container**: [Shape description, e.g., Central Circular Engine]
* **Visual Structure**: [Concrete objects, e.g., A clockwise loop connecting 3 internal modules: A (Gear), B (Graph), C (Filter)]
* **Key Text Labels**: "[Text 2]", "[Text 3]"

[ZONE 3: LOCATION - LABEL]
... (Add Zone 4 or 5 if necessary based on the selected layout)

[CONNECTIONS]
1. [Connection description, e.g., A curved dotted arrow looping from Zone 2 back to Zone 1 labeled "Feedback"]
2. [Connection description, e.g., A wide flow arrow branching from Zone 2 to Zone 3]

---END PROMPT---

```

## 4. Usage Guide for User

**Input:** Upload your paper PDF and say:
> "Generate a visual schema for this paper's methodology section"

**Pro Tips for Best Results:**
* **Text Correction**: AI image generators often misspell complex scientific terms. Use the generated image as a *base layer*, then overlay correct text in PowerPoint/Canva/Illustrator.
* **Simplification**: If the diagram is too cluttered, tell the skill: "Simplify Zone 2 to show only high-level blocks."

**Advanced Constraints:**

* Add `--svg` to request a Mermaid/SVG code block representation (Experimental).
* Add `--style "poster"` for simplified, bold layouts.

## 5. Technical Limitations

* SVG output is an approximation; prioritize the Text Schema for Image Generation models.
* Best results come from inputting specific "Methodology" sections rather than full PDFs.