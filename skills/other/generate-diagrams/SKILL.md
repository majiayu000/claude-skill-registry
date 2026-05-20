---
name: generate-diagrams
description: "Generate all diagrams for a blog post using PaperBanana. Creates .txt description files, runs PaperBanana to produce diagrams, then VISUALLY VERIFIES each image. Use when the article plan exists and diagrams need to be created."
allowed-tools: Bash, Read, Write, Glob
---

# Diagram Generation Skill

## Input
$ARGUMENTS = topic name (must have plan/<topic-slug>_outline.md)

## Process

### Step 1: Read the Plan
Read plan/<topic-slug>_outline.md
Extract the complete Diagram Master List.

### Step 2: Write ALL Description Files First
For EACH diagram in the master list, create a .txt file at:
  figures/descriptions/<fig_id>.txt

Each .txt file MUST follow this exact format (matching the style from
the DeepSeek chapter figures):

```
<Diagram Title>

IMPORTANT: Pure white background (#FFFFFF). No gray tint, no colored
background, no gradient. The diagram must have a clean white background
suitable for an academic paper/blog post.

<Detailed description follows...>

[Describe the layout: top-to-bottom, left-to-right, etc.]

[List every component in order:]
1. Component Name (shape, color, label)
   - Sub-details
   - Connections to other components

[Describe the flow arrows:]
- Solid black arrows for main data flow
- Thin gray arrows for skip/residual connections
- Dashed arrows for shared/tied weights

[Describe matrix shapes if applicable:]
- Input: (4, 8) blue rounded box
- Output: (4, 4) green rounded box

Style: Clean academic illustration with sans-serif labels, pastel color
palette (blue, green, lavender, pink, gray, peach/orange), solid black
arrows for data flow. White background throughout.
```

### Step 3: Generate Diagrams One by One
For each .txt file, run PaperBanana:

```bash
paperbanana generate \
  -i figures/descriptions/<fig_id>.txt \
  -c "<caption from the plan>" \
  -o figures/output/<fig_id>.png \
  -n 3 \
  --optimize
```

If PaperBanana MCP is available, use the generate_diagram tool instead.

### Step 4: VISUALLY VERIFY Each Generated Diagram (CRITICAL)
THIS IS THE MOST IMPORTANT STEP. Do NOT just check if the file exists.

After EACH diagram is generated, you MUST:

1. **Open and LOOK at the generated .png image** using the Read tool
   on the image file path. Claude Code has vision and can see images.

2. **Compare what you see against the .txt description.** Check for:
   - Are ALL components from the description present?
   - Are labels readable and correctly spelled?
   - Is the layout correct (top-to-bottom, left-to-right as specified)?
   - Are matrix shapes shown correctly?
   - Are arrows pointing the right direction?
   - Is the background white (not gray or colored)?
   - Are colors roughly matching the pastel palette specified?
   - Is any text cut off or overlapping?
   - Are there any garbled, nonsensical, or hallucinated labels?

3. **Rate the diagram: PASS, FIXABLE, or FAIL**
   - PASS: Diagram is good. All components present, labels readable,
     layout correct. Minor imperfections are acceptable.
   - FIXABLE: Most components are right but something specific is wrong
     (e.g., a label is misspelled, one arrow is missing, colors are off).
     Identify exactly what is wrong for targeted regeneration.
   - FAIL: Diagram is fundamentally wrong, garbled, or unusable.
     Major components missing, layout completely different from description,
     or unreadable text throughout.

### Step 5: Handle Verification Results

**For PASS diagrams:**
Move on to the next diagram.

**For FIXABLE diagrams:**
1. Identify the specific issue (e.g., "Expert 3 label says 'Epert 3'")
2. Update the .txt description to be MORE EXPLICIT about the problem area
   (e.g., add "CRITICAL: The label must say exactly 'Expert 3' not 'Epert'")
3. Regenerate ONLY this diagram
4. Visually verify again
5. Maximum 3 retry attempts, then flag for user

**For FAIL diagrams:**
1. Analyze why it failed (too complex? unclear description? wrong layout type?)
2. REWRITE the .txt description significantly:
   - Simplify if the diagram was too complex
   - Add more explicit spatial instructions
   - Break into multiple simpler diagrams if needed
3. Regenerate
4. Visually verify again
5. Maximum 3 retry attempts, then flag for user

### Step 6: Generate Final Report
After ALL diagrams have been generated and verified, create a report:

```
Diagram Generation and Verification Report
============================================
Total planned: X
PASSED on first try: Y
PASSED after fixes: Z
FAILED (needs user attention): W

Detailed Status:
[PASS]  fig_roadmap.png - All components present, labels clear
[PASS]  fig_architecture.png - Clean layout, good colors
[FIXED] fig_comparison.png - Regenerated 2x, fixed label overlap
[FAIL]  fig_math_derivation.png - Could not get readable equations
        after 3 attempts. Recommend creating this one manually.

Quality Notes:
- fig_roadmap.png: Excellent quality, matches description well
- fig_architecture.png: Good but arrow from block 3 to block 4
  is slightly misaligned (acceptable)
- fig_comparison.png: Usable after fixes but colors are slightly
  different from other diagrams
```

Show this report to the user. For any FAIL diagrams, show what the
current best attempt looks like so the user can decide whether to
keep it, manually edit it, or create it from scratch.

## Important Rules
- Write EVERY .txt description file BEFORE running any generation
- ALWAYS visually inspect EVERY generated image. NEVER skip this.
- Never just check file existence. You MUST look at the actual image.
- Maximum 3 regeneration attempts per diagram before flagging for user
- Keep a running count of API calls to avoid excessive Gemini usage
- Generate 3 variants (-n 3) and the system picks the best
- All descriptions must specify white background
- Use consistent pastel color palette across all diagrams
- Matrix shapes must be clearly labeled in every diagram

## Output
Show the full verification report to the user.
For FAIL diagrams, display the best attempt so user can see it.
Ask user if they want to regenerate any specific diagrams or proceed.