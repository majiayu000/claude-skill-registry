---
name: mermaid-generator
description: This skill generates interactive workflow diagrams using the Mermaid
  JavaScript library
---

---
name: mermaid-generator
description: This skill generates interactive workflow diagrams using the Mermaid JavaScript library
for placement in a narrow region of a textbook using an iframe. Use this skill when users request creating flowcharts, process diagrams, workflow visualizations, or decision trees for educational textbooks. The skill creates MicroSim packages with standalone HTML files featuring colorful backgrounds, 16-point fonts, and top-down rendering by default, saved to /docs/sims/ following the MicroSim pattern.
---

# Mermaid Diagram Generator

## Overview

Generate simple minimalist but colorful interactive workflow diagrams using Mermaid.js for intelligent textbooks. Creates complete MicroSim packages with standalone HTML files, MkDocs integration, and Dublin Core metadata. Each diagram features colorful node backgrounds, 16-point fonts for optimal readability, and follows the educational MicroSim pattern.

Because this skill is part of the workflow for creation of textbooks using mkdocs, the design goal
is to create simple unadorned diagrams without any complex padding, borders or decoration.  This is
because our focus is to educate, not entertain and show off our ability to do rounded corners and gradient shading.

## When to Use This Skill

Use the mermaid-generator skill when users request:

- Workflow diagrams or process flows
- Decision trees with branching logic
- Algorithm visualizations
- System architecture flows
- Educational process diagrams
- Step-by-step procedure illustrations
- State transition diagrams
- Any flowchart-style visualization

**Example user requests:**
- "Create a flowchart showing the software development lifecycle"
- "Generate a workflow diagram for the scientific method"
- "Make a decision tree for troubleshooting network issues"
- "Visualize the process of photosynthesis as a diagram"

## Workflow

### Step 1: Gather Diagram Requirements

Analyze the user's description to extract:

1. **Diagram Purpose**: What process or workflow is being illustrated?
2. **Key Steps**: What are the main nodes/steps in the workflow?
3. **Decision Points**: Are there branching decisions (if/then)?
4. **Flow Direction**: Should it be top-down (TD), left-right (LR), or other?
5. **Start/End Points**: Where does the process begin and end?

**If the description is incomplete or unclear**, prompt the user for additional information:

```
To create an accurate workflow diagram, I need more information:

1. What are the main steps in this process?
2. Are there any decision points where the flow branches?
3. What happens in success vs. error scenarios?
4. Should this flow top-down or left-right?
```

**Required information before proceeding:**

- At least 3-5 distinct steps/nodes
- Clear start and end points
- Understanding of the flow sequence

### Step 2: Design the Mermaid Flowchart

Consult `references/mermaid-flowchart-syntax.md` for detailed syntax guidance.

**Design decisions:**

1. **Choose node shapes** based on purpose:
   - Rounded rectangles `("Label")` for start/end
   - Rectangles `["Label"]` for process steps
   - Diamonds `{"Decision?"}` for decision points
   - Circles `(("Label"))` for connectors

2. **Select color palette** from reference guide:
   - Vibrant (purple/blue/pink) for engaging diagrams
   - Professional (turquoise/mint/coral) for formal content
   - Ocean (blue spectrum) for technical content
   - Or create custom palette matching textbook theme

3. **Define style classes** for consistent theming:
   ```
   classDef startNode fill:#667eea,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
   classDef processNode fill:#764ba2,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
   classDef decisionNode fill:#f093fb,stroke:#333,stroke-width:2px,color:#333,font-size:16px
   ```

4. **Ensure 16pt fonts** for all nodes and edge labels:
   - Set `font-size:16px` in all classDef declarations
   - Apply to edge labels: `linkStyle default font-size:16px`

5. **Use top-down direction** unless user specifies otherwise:
   ```
   flowchart TD
   ```

**Example Mermaid code structure:**

```mermaid
flowchart TD
    Start("Start Process"):::startNode
    Step1["Gather Input"]:::processNode
    Decision{"Valid Input?"}:::decisionNode
    Step2["Process Data"]:::processNode
    Success("Success"):::successNode
    Error("Error - Retry"):::errorNode

    Start --> Step1 --> Decision
    Decision -->|Yes| Step2 --> Success
    Decision -->|No| Error --> Step1

    classDef startNode fill:#667eea,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
    classDef processNode fill:#764ba2,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
    classDef decisionNode fill:#f093fb,stroke:#333,stroke-width:2px,color:#333,font-size:16px
    classDef successNode fill:#4facfe,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
    classDef errorNode fill:#fa709a,stroke:#333,stroke-width:2px,color:#fff,font-size:16px

    linkStyle default stroke:#999,stroke-width:2px,font-size:16px
```

### Step 3: Create the MicroSim Directory Structure

Create the diagram directory following the MicroSim pattern:

```bash
mkdir -p /docs/sims/[diagram-name]
```

**Naming convention:**
- Use kebab-case (lowercase with hyphens)
- Descriptive and concise
- Examples: `software-lifecycle`, `scientific-method`, `network-troubleshooting`

### Step 4: Generate Files from Templates

Use the template files in `assets/template/` as a starting point. Replace placeholders with actual content:

#### 4.1 Create main.html

Copy `assets/template/main.html` and replace these placeholders:

- `{{TITLE}}`: Diagram title (e.g., "Software Development Lifecycle")
- `{{SUBTITLE}}`: Brief subtitle (e.g., "Interactive Workflow Diagram")
- `{{MERMAID_CODE}}`: The complete Mermaid flowchart code (from Step 2)
- `{{DESCRIPTION}}`: 2-3 sentence explanation of the diagram

**Important:** Ensure proper indentation of the Mermaid code within the `<div class="mermaid">` tag.

#### 4.2 Create style.css

Copy `assets/template/style.css` directly - no modifications needed unless custom styling is requested.

The default stylesheet ensures:
- 16px font size for diagram elements
- Responsive design for mobile devices
- Clean, professional appearance
- Print-friendly styling

#### 4.3 Create script.js

Copy `assets/template/script.js` directly. This provides:
- Zoom controls for large diagrams
- Export to SVG functionality
- Node interaction tracking
- Accessibility features

#### 4.4 Create index.md

Copy `assets/template/index.md` and replace placeholders:

- `{{TITLE}}`: Same as main.html title
- `{{OVERVIEW}}`: 1-paragraph overview of the workflow
- `{{DESCRIPTION}}`: Detailed description of the process
- `{{WORKFLOW_STEPS}}`: Bulleted list of main steps:
  ```markdown
  1. **Step Name** - Description of what happens
  2. **Decision Point** - What decision is being made
  3. **Final Step** - How the process concludes
  ```
- `{{KEY_CONCEPTS}}`: Bulleted list of educational concepts illustrated
- `{{RELATED_CONCEPTS}}`: Links to related textbook sections or concepts

#### 4.5 Create metadata.json

Copy `assets/template/metadata.json` and replace placeholders:

- `{{TITLE}}`: Diagram title
- `{{DESCRIPTION}}`: Brief description
- `{{SUBJECT}}`: Educational subject area (e.g., "Computer Science", "Biology")
- `{{DATE}}`: Current date in ISO format (YYYY-MM-DD)
- `{{COVERAGE}}`: Scope of content (e.g., "Introductory", "Advanced")
- `{{AUDIENCE}}`: Target audience (e.g., "High School", "Undergraduate")
- `{{NODE_COUNT}}`: Number of nodes in diagram
- `{{EDGE_COUNT}}`: Number of edges/arrows in diagram
- `{{CONCEPTS_LIST}}`: JSON array of concept labels (e.g., `"Algorithm Design", "Data Validation"`)
- `{{BLOOM_LEVEL}}`: Highest Bloom's Taxonomy level addressed (e.g., "Understand", "Apply", "Analyze")

**Example metadata.json:**

```json
{
  "title": "Software Development Lifecycle",
  "description": "Interactive workflow diagram showing the phases of software development from planning through deployment",
  "subject": "Computer Science",
  "creator": "Claude AI with Mermaid Generator Skill",
  "date": "2025-11-06",
  "type": "Interactive Workflow Diagram",
  "format": "text/html",
  "language": "en-US",
  "coverage": "Introductory",
  "rights": "Educational Use",
  "audience": "Undergraduate",
  "diagram_type": "flowchart",
  "direction": "TD",
  "node_count": "8",
  "edge_count": "10",
  "concepts": [
    "Requirements Analysis",
    "System Design",
    "Implementation",
    "Testing",
    "Deployment",
    "Maintenance"
  ],
  "bloom_taxonomy": "Understand",
  "version": "1.0"
}
```

### Step 5: Update MkDocs Navigation

Add the new diagram to the textbook's navigation in `mkdocs.yml`:

```yaml
nav:
  - Visualizations:
    - Software Lifecycle: sims/software-lifecycle/index.md
```

Or integrate into relevant chapter navigation:

```yaml
nav:
  - Chapter 3 - Software Engineering:
    - Introduction: chapters/03/index.md
    - Lifecycle Diagram: sims/software-lifecycle/index.md
```

### Step 6: Validate and Test

Perform quality checks:

1. **Syntax validation**: Ensure Mermaid code renders without errors
2. **File structure**: Verify all 5 files are present (index.md, metadata.json, style.css, main.html, script.js)
3. **Placeholder replacement**: Check that no `{{PLACEHOLDERS}}` remain
4. **Font size verification**: Confirm 16px fonts in Mermaid code and CSS
5. **Color contrast**: Ensure text is readable on colored backgrounds
6. **Responsive design**: Test that diagram works on different screen sizes

**Test the diagram:**

```bash
cd /docs
mkdocs serve
# Navigate to http://localhost:8000/sims/[diagram-name]/
```

Open main.html directly in browser to test standalone functionality.

### Step 7: Inform the User

Provide a summary of what was created:

```
Created interactive Mermaid workflow diagram: [Diagram Name]

Location: /docs/sims/[diagram-name]/

Files generated:
✓ main.html - Standalone interactive diagram
✓ index.md - MkDocs integration page
✓ style.css - Responsive styling
✓ script.js - Interactive features (zoom, export)
✓ metadata.json - Dublin Core metadata

Features:
• Top-down flowchart layout
• Colorful node backgrounds for visual clarity
• 16-point fonts for optimal readability
• [X] nodes and [Y] edges
• Zoom controls and SVG export

The diagram illustrates: [brief description]

To view:
1. Standalone: Open /docs/sims/[diagram-name]/main.html
2. In textbook: Run `mkdocs serve` and navigate to the page

Next steps:
- Add navigation link in mkdocs.yml
- Reference from relevant chapter content
- Consider creating related diagrams for connected concepts
```

## Best Practices

### Design Principles

1. **Clarity over Complexity**: Keep diagrams focused on core workflow - if too complex, consider breaking into multiple diagrams
2. **Consistent Styling**: Use the same color palette across related diagrams in a textbook
3. **Meaningful Labels**: Use clear, concise labels (2-5 words max per node)
4. **Logical Flow**: Ensure arrows flow in expected reading direction (top-down or left-right)
5. **Color Semantics**: Use colors consistently (e.g., green for success, red for errors)

### Accessibility

1. **Font Size**: Always use 16px minimum for readability
2. **Color Contrast**: Ensure WCAG AA contrast ratios (4.5:1 minimum)
3. **Text Alternatives**: Provide descriptive text in index.md
4. **Semantic HTML**: Use proper heading structure in documentation

### Educational Integration

1. **Align with Learning Goals**: Map diagram to specific learning objectives
2. **Bloom's Taxonomy**: Tag with appropriate cognitive level
3. **Concept Dependencies**: Link to prerequisite concepts in learning graph
4. **Practice Exercises**: Consider adding comprehension questions in index.md

### Common Patterns

**Linear Process Flow:**
```
Start → Step 1 → Step 2 → Step 3 → End
```

**Decision Tree:**
```
Start → Decision 1 (Yes/No)
  ├─ Yes → Action A → End
  └─ No → Decision 2 (Yes/No)
      ├─ Yes → Action B → End
      └─ No → Action C → End
```

**Loop/Iteration:**
```
Start → Initialize → Process → Check Complete?
  ├─ No → Process (loop back)
  └─ Yes → End
```

**Error Handling:**
```
Start → Try Action → Success?
  ├─ Yes → Continue → End
  └─ No → Error Handler → Retry or Exit
```

## Troubleshooting

### Common Issues

**Issue: Mermaid code doesn't render**
- Check for syntax errors (missing quotes, brackets)
- Ensure `flowchart TD` directive is first line
- Verify no reserved keywords used as IDs (like "end" in lowercase)

**Issue: Fonts not 16px**
- Verify `font-size:16px` in all classDef declarations
- Check `linkStyle default font-size:16px` is present
- Ensure style.css includes `.mermaid .node text` styling

**Issue: Colors not showing**
- Confirm classDef declarations come after flowchart code
- Verify `:::className` syntax on nodes
- Check hex color codes are valid

**Issue: Diagram too large/small**
- Adjust node count (split into multiple diagrams if >15 nodes)
- Use zoom controls in script.js
- Modify CSS max-width settings

**Issue: Labels cut off or truncated**
- Shorten label text
- Use markdown strings for auto-wrapping: `A["Text **bold**"]`
- Increase diagram container width in CSS

## Resources

### Bundled References

- **`references/mermaid-flowchart-syntax.md`**: Comprehensive Mermaid syntax guide with examples, node shapes, styling options, and color palettes

### Bundled Templates

- **`assets/template/main.html`**: Standalone HTML diagram template
- **`assets/template/style.css`**: Responsive stylesheet with 16px fonts
- **`assets/template/script.js`**: Interactive features (zoom, export, tracking)
- **`assets/template/index.md`**: MkDocs integration template
- **`assets/template/metadata.json`**: Dublin Core metadata template

### External Resources

- Mermaid.js Documentation: https://mermaid.js.org/
- MkDocs Material Theme: https://squidfunk.github.io/mkdocs-material/
- Dublin Core Metadata: https://www.dublincore.org/specifications/dublin-core/

## Examples

### Example 1: Simple Linear Workflow

**User Request:** "Create a diagram showing the steps of making coffee"

**Generated Mermaid Code:**

```mermaid
flowchart TD
    Start("Start"):::startNode
    Step1["Boil Water"]:::processNode
    Step2["Grind Coffee Beans"]:::processNode
    Step3["Add Coffee to Filter"]:::processNode
    Step4["Pour Hot Water"]:::processNode
    Step5["Wait 4 Minutes"]:::processNode
    End("Enjoy Coffee!"):::endNode

    Start --> Step1 --> Step2 --> Step3 --> Step4 --> Step5 --> End

    classDef startNode fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
    classDef processNode fill:#95e1d3,stroke:#333,stroke-width:2px,color:#333,font-size:16px
    classDef endNode fill:#6c5ce7,stroke:#333,stroke-width:2px,color:#fff,font-size:16px

    linkStyle default stroke:#999,stroke-width:2px,font-size:16px
```

### Example 2: Decision-Based Workflow

**User Request:** "Create a flowchart for troubleshooting a computer that won't start"

**Generated Mermaid Code:**

```mermaid
flowchart TD
    Start("Computer Won't Start"):::startNode
    Check1{"Is it plugged in?"}:::decisionNode
    Fix1["Plug in power cable"]:::processNode
    Check2{"Does it have power?"}:::decisionNode
    Check3{"Do you hear beeps?"}:::decisionNode
    Fix2["Check power supply"]:::processNode
    Fix3["Check RAM seating"]:::processNode
    Fix4["Call technician"]:::processNode
    Success("Computer Started!"):::successNode

    Start --> Check1
    Check1 -->|No| Fix1 --> Check2
    Check1 -->|Yes| Check2
    Check2 -->|No| Fix2 --> Success
    Check2 -->|Yes| Check3
    Check3 -->|Yes| Fix3 --> Success
    Check3 -->|No| Fix4

    classDef startNode fill:#667eea,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
    classDef processNode fill:#764ba2,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
    classDef decisionNode fill:#f093fb,stroke:#333,stroke-width:2px,color:#333,font-size:16px
    classDef successNode fill:#4facfe,stroke:#333,stroke-width:2px,color:#fff,font-size:16px

    linkStyle default stroke:#999,stroke-width:2px,font-size:16px
```

### Example 3: Loop-Based Algorithm

**User Request:** "Visualize a simple search algorithm"

**Generated Mermaid Code:**

```mermaid
flowchart TD
    Start("Start Search"):::startNode
    Input["Get search target"]:::processNode
    Init["Set index = 0"]:::processNode
    Loop["Check array[index]"]:::processNode
    Match{"Match found?"}:::decisionNode
    End{"More items?"}:::decisionNode
    Increment["index = index + 1"]:::processNode
    Success("Return index"):::successNode
    Fail("Return -1"):::errorNode

    Start --> Input --> Init --> Loop --> Match
    Match -->|Yes| Success
    Match -->|No| End
    End -->|Yes| Increment --> Loop
    End -->|No| Fail

    classDef startNode fill:#0083b0,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
    classDef processNode fill:#00b4d8,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
    classDef decisionNode fill:#90e0ef,stroke:#333,stroke-width:2px,color:#333,font-size:16px
    classDef successNode fill:#48cae4,stroke:#333,stroke-width:2px,color:#fff,font-size:16px
    classDef errorNode fill:#0077b6,stroke:#333,stroke-width:2px,color:#fff,font-size:16px

    linkStyle default stroke:#999,stroke-width:2px,font-size:16px
```

## Integration with Other Skills

This skill works well with other intelligent textbook skills:

- **learning-graph-generator**: Create diagrams for concepts in the learning graph
- **chapter-content-generator**: Embed diagrams in chapter content
- **microsim-p5**: Use Mermaid for static workflow diagrams, p5.js for dynamic simulations
- **quiz-generator**: Create questions about workflow understanding
- **glossary-generator**: Define terms used in diagram labels

## Version History

**v1.0** - Initial release
- Flowchart diagram generation
- MicroSim package creation
- 16pt fonts and colorful styling
- Top-down rendering default
- Dublin Core metadata support
