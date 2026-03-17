---
name: pptx-generation
description: Enterprise-grade PowerPoint deck generation system using evidence-based prompting techniques, workflow enforcement, and constraint-based design. Use when creating professional presentations (board decks, reports, analyses) requiring consistent visual quality, accessibility compliance, and integration of complex data from multiple sources. Implements html2pptx workflow with spatial layout optimization, validation gates, and multi-chat architecture for 30+ slide decks.
---

# PowerPoint Generation Skill

## Overview

This skill implements a systematic framework for generating professional-quality PowerPoint presentations using AI. It addresses the unique challenges of PowerPoint as a medium that combines data analysis, narrative structure, visual design, and spatial layout—making it one of the most complex AI generation tasks in corporate knowledge work.

The skill applies evidence-based prompting techniques (plan-and-solve, program-of-thought, self-consistency), structural optimization principles (workflow enforcement, constraint-based design, validation gates), and proven spatial layout patterns to ensure consistent, high-quality outputs.

## Core Principles

### 1. Workflow Enforcement

AI systems exhibit tool degradation—silently switching to suboptimal alternatives when primary tools encounter difficulties. For spatial/visual tasks, this creates unreliable outputs.

**Implementation**: Explicitly specify the html2pptx technical workflow and prohibit alternative approaches. Require documentation review before execution.

**Rationale**: PowerPoint generation requires precise spatial calculations. The html2pptx skill provides reliable pixel-level control. Preventing tool switching eliminates the primary source of layout inconsistencies.

### 2. Constraint-Based Design Over Decorative Specification

Simple visual rules scale reliably; complex decorative elements create brittleness in AI generation.

**Implementation**: Define what NOT to do (negative constraints) before specifying positive behaviors. Prohibit border boxes, outline shapes, and rounded rectangles. Emphasize spacing, typography, and subtle color blocks.

**Rationale**: Visual design has exponentially more failure modes than success modes. Eliminating known problematic patterns focuses generative capacity within reliable boundaries. Clean design enables AI to prioritize content synthesis over visual parsing.

### 3. Pre-Execution Design Planning

Separating planning from execution prevents premature commitment to suboptimal visual approaches.

**Implementation**: Require written design plan specifying layout approach, color palette, typography hierarchy, and visual emphasis strategy before code generation.

**Rationale**: Mimics human design process. Creates audit trail for review. Establishes coherent visual system before implementation begins. Dramatically improves consistency across multi-slide decks.

### 4. Quantified Visual Specifications

Vague instructions ("clean margins") force the AI to guess intent. Precise specifications eliminate ambiguity.

**Implementation**: Convert qualitative requirements to measurable parameters (contrast ratios, font sizes, margin measurements, element counts).

**Rationale**: Spatial relationships are inherently quantitative. Explicit measurements create reproducible results and enable automated validation.

### 5. Multi-Chat Architecture for Complex Decks

Visual elements consume tokens faster than text or data. Single-context generation becomes unreliable beyond ~15 slides.

**Implementation**: Separate architect (narrative structure), generator (slide production), and assembly (consistency validation) into distinct conversations for 30+ slide decks.

**Rationale**: Manages context window limitations. Allows focused expertise in each phase. Enables section-level iteration without full deck regeneration.

## When to Use This Skill

**Primary Use Cases**:
- Board decks and executive presentations requiring professional polish
- Financial reports integrating data from multiple sources
- Strategic analyses combining quantitative and qualitative content
- Project updates demanding consistent visual language
- Any presentation where visual quality impacts stakeholder perception

**Skill Triggers**:
- User requests "create a presentation," "make slides," "build a deck"
- User asks to "analyze [data] and present findings"
- User mentions specific output formats: .pptx, PowerPoint, slides
- User provides business data (CSV, financial reports, memos) requesting visualization
- Task requires integrating analysis with narrative in visual format

**When NOT to Use**:
- Simple 1-3 slide requests (use default PowerPoint generation without full workflow)
- Requests for slide content only without visual implementation
- Non-presentation visualization tasks (use charts, graphs, or documents instead)

## PowerPoint Generation Workflow

### Phase 1: Requirements Analysis

**Objective**: Establish scope, constraints, and success criteria before design.

**Process**:
1. Identify data sources and required analyses
2. Determine slide count and narrative structure  
3. Establish visual constraints (brand guidelines, accessibility requirements, template restrictions)
4. Clarify audience expertise level and presentation context
5. Define output quality standards

**Decision Point**: Simple deck (≤15 slides, single context) vs. Complex deck (30+ slides, multi-chat architecture)?

### Phase 2: Pre-Execution Design Plan

**Objective**: Establish coherent visual system before implementation.

**Required Elements**:
- **Layout Philosophy**: Describe approach to spacing, element positioning, visual hierarchy
- **Color Palette**: Specify exact hex values, contrast ratios, usage rules
- **Typography System**: Font families, size hierarchy (titles, headers, body, captions), line spacing
- **Visual Emphasis Strategy**: How information priority translates to visual weight (color blocks, spacing, sizing)

**Format**: Written description in structured format. Must be completed before any code generation begins.

**Validation**: Design plan must explicitly address all items in Design Restrictions (see below).

### Phase 3: Implementation

**For Simple Decks (≤15 slides)**:
Execute in single conversation following the prompt template in `references/simple-deck-template.md`.

**For Complex Decks (30+ slides)**:
Follow multi-chat architecture in `references/complex-deck-architecture.md`:
1. Architect Chat: Generate narrative structure and slide-level outline
2. Generator Chat(s): Produce sections of 10-15 slides each
3. Assembly Chat: Ensure consistency, validate against design plan

**Technical Requirements**:
- Always use html2pptx workflow
- Generate slides iteratively (never all at once for complex decks)
- Validate after each section before proceeding
- Maintain state document tracking completed slides and remaining work

### Phase 4: Validation

**Automated Checks**:
- Contrast ratio verification (minimum 4.5:1 for all text)
- Font size validation (18pt minimum, 24pt titles)
- Margin measurements (0.5" minimum all sides)
- Element overlap detection
- Bullet count per slide (maximum 3)

**Manual Review Points**:
- Thumbnail readability test
- Visual consistency across slides
- Narrative flow and logical progression
- Data accuracy and source attribution

**Failure Response**: If validation fails, identify root cause, adjust design plan or implementation approach, and regenerate affected sections. Never apply band-aid fixes.

## Design Restrictions

These constraints are absolute and apply to every slide in every deck. They eliminate known failure modes and ensure reliable spatial layout.

### Prohibited Elements

**NEVER include these in any slide**:
- Border boxes around text elements
- Outline shapes containing text content
- Rounded rectangles with text inside
- Text containers or frames
- Decorative borders or dividing lines as separate elements
- Overlapping text elements
- Dark text on dark backgrounds

### Required Patterns

**ALWAYS implement these in every deck**:
- Text directly on slide background or solid color areas
- Visual separation through spacing and typography (not containers)
- Colored accent bars or background sections (not outlined boxes)
- Subtle background color zones for emphasis (not bordered elements)
- Clean white or light-colored backgrounds
- High-contrast text (4.5:1 minimum ratio)
- Single visual element per slide (maximum)

### Layout Constraints

**Quantified requirements for every slide**:
- Maximum 3 bullets per slide
- 18pt minimum font size (body text)
- 24pt minimum font size (titles)
- 0.5" minimum margins on all sides
- No overlapping text elements
- Light backgrounds with dark text (preferred)

### Accessibility Requirements

**Non-negotiable standards**:
- All text must have minimum 4.5:1 contrast ratio
- Test readability at thumbnail size
- No dark text on dark backgrounds
- Color should not be sole means of conveying information
- Alt text for all visual elements

## Common Failure Modes and Solutions

### Symptom: Inconsistent visual styling across slides

**Root Cause**: Design plan not established before implementation, or not referenced during generation.

**Solution**: Always complete pre-execution design plan. Include design plan in context for each generator chat. Explicitly validate against design plan after each section.

### Symptom: Text overlapping or extending beyond slide boundaries

**Root Cause**: AI switched from html2pptx to alternative tool without notification (tool degradation).

**Solution**: Enforce html2pptx workflow explicitly in prompt. Include statement: "Debug any installation issues; do not switch to alternative approaches." If problem persists, confirm tool is actually being used.

### Symptom: Border boxes or outline shapes appearing despite restrictions

**Root Cause**: Positive instructions ("use clean design") given without corresponding negative constraints.

**Solution**: Lead with negative constraints in CAPITAL LETTERS at top of prompt. Repeat critical prohibitions in multiple sections. Make restrictions more prominent than positive instructions.

### Symptom: Low contrast or readability issues

**Root Cause**: Validation gates not implemented or skipped.

**Solution**: Require explicit contrast ratio verification (show calculations). Test at thumbnail size before considering deck complete. Make accessibility validation non-optional.

### Symptom: Context window exhaustion mid-generation

**Root Cause**: Attempting complex deck in single conversation without multi-chat architecture.

**Solution**: Implement multi-chat architecture for decks >15 slides. Separate planning, generation, and assembly phases. Generate slides in sections of 10-15, not all at once.

## Integration with Other Skills

This skill works synergistically with:

- **Data Analysis Skills**: Generate analysis outputs in structured format suitable for slide generation
- **Brand Guidelines Skill**: Automatically apply organizational visual standards  
- **DOCX Skill**: Generate complementary written reports alongside presentations
- **Chart Generation**: Create data visualizations for inclusion in slides

When used together, these skills enable complete board package generation (deck + memo + analysis) from raw data sources.

## References

This skill includes comprehensive reference documentation:

- `references/simple-deck-template.md` - Complete prompt template for ≤15 slide decks
- `references/complex-deck-architecture.md` - Multi-chat architecture for 30+ slide decks  
- `references/design-principles.md` - Deep dive on constraint-based design philosophy
- `references/validation-checklist.md` - Detailed validation procedures
- `references/brand-integration.md` - Process for applying brand guidelines
- `references/workflow-diagram.dot` - Visual process flow (GraphViz format)

Load relevant references as needed during implementation.

## Conclusion

PowerPoint generation represents the intersection of data analysis, narrative structure, visual design, and spatial layout. This skill addresses the unique challenges through systematic workflow enforcement, evidence-based prompting techniques, and constraint-based design principles.

The key insight: **Make constraints more explicit, not more complex.**

**Simple visual rules + Clear prohibitions + Forced planning = Reliable professional outputs**

Success metrics:
- Consistent visual quality across all slides
- Zero layout failures (overlaps, boundary violations, contrast issues)
- Reduced iteration cycles (get it right in first generation)
- Scalability to complex 30+ slide decks
- Accessibility compliance as default, not afterthought
