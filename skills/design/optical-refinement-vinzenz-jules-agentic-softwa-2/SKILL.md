---
name: optical-refinement
description: Reviews designs for optical balance issues that mathematical precision misses. Covers typography kerning, visual alignment, spacing rhythm, color weight, and the human touch that distinguishes professional design from AI-generated output.
---

# Optical Refinement Skill

You are operating with optical refinement capabilities. This skill addresses the fundamental difference between mathematically correct and visually correct design.

## Core Philosophy

> "The way humans see and process images isn't always going in pair with what the numbers say. What may seem perfectly aligned and balanced for a computer may not seem the same way for your eyes." — Rafal Tomal

Professional designers trust their eyes over rulers. AI uses mathematical precision — which often looks wrong to human eyes. This skill teaches how to identify and correct optical issues.

## Why This Matters

**Mathematical precision fails because:**
- Human vision is not a camera
- We perceive some shapes as "heavier" than others
- Optical illusions affect all viewers consistently
- Context changes how we perceive elements

**Examples:**
- A mathematically centered circle in a square looks too low
- Letters A and V need tighter kerning than H and I
- A 10px gap after text looks smaller than a 10px gap after an icon
- Warm colors appear to advance; cool colors recede

## Category 1: Typography Optical Issues

### Kerning and Letter Spacing

<typography_kerning>
**Common Problems:**
- "AV", "AT", "LT", "Ty" combinations need tighter spacing
- Round letters (O, C, G) need visual compensation
- The eye judges spacing by AREA, not distance

**How to Check:**
1. Flip the text upside down (removes semantic reading)
2. Squint to blur the letterforms
3. Look for "rivers" of white space
4. Check if any letter pairs feel disconnected

**Correction Approach:**
- Space by optical area, not mathematical distance
- Tighten pairs with diagonal/round edges
- Loosen pairs with vertical stems

```xml
<kerning_issue>
  <location>Element containing the text</location>
  <problem_pair>AV, LT, etc.</problem_pair>
  <current_spacing>Mathematical spacing</current_spacing>
  <recommended_action>Tighten by X units or percentage</recommended_action>
</kerning_issue>
```
</typography_kerning>

### Vertical Rhythm and Line Height

<typography_rhythm>
**Common Problems:**
- Line height that works for body text is wrong for headings
- All-caps text needs tighter line height than mixed case
- Descenders (g, j, p, q, y) affect perceived line spacing

**How to Check:**
1. Measure paragraph "color" — should be even gray when squinted
2. Check for "stacking" — lines that feel too tight
3. Check for "floating" — lines that feel disconnected
4. Compare line spacing to paragraph spacing ratios

**Correction Approach:**
- Body text: 1.4-1.6x font size
- Headings: 1.1-1.3x font size
- All-caps: 1.0-1.2x font size
- Maintain proportional paragraph spacing (usually 1.5-2x line height)

```xml
<rhythm_issue>
  <location>Text block or section</location>
  <current_line_height>Current value</current_line_height>
  <problem>Lines feel too tight/loose because...</problem>
  <recommended_line_height>Adjusted value</recommended_line_height>
</rhythm_issue>
```
</typography_rhythm>

### Type Size Relationships

<typography_scale>
**Common Problems:**
- Too many type sizes (more than 5-6 creates chaos)
- Size jumps too small (hard to establish hierarchy)
- Size jumps inconsistent (no mathematical relationship)

**How to Check:**
1. List all font sizes used — are they intentional?
2. Do size jumps create clear hierarchy?
3. Can you identify the importance of text by size alone?

**Correction Approach:**
- Use a type scale (1.25, 1.333, 1.5, or 1.618 ratio)
- Larger jumps for clearer hierarchy (don't be timid)
- Fewer sizes, more consistent use

```xml
<scale_issue>
  <sizes_in_use>12, 14, 16, 18, 20, 24, 32, 48</sizes_in_use>
  <problem>Too many sizes / No clear ratio / Hierarchy unclear</problem>
  <recommended_scale>base: 16, ratio: 1.25 = 16, 20, 25, 31, 39</recommended_scale>
</scale_issue>
```
</typography_scale>

## Category 2: Spatial Optical Issues

### Visual Centering

<spatial_centering>
**The Problem:**
Mathematical center looks wrong because:
- Shapes with points (triangles, play icons) have visual weight offset from geometric center
- Text has a visual center different from its bounding box center
- Elements with descenders or ascenders shift perceived center

**How to Check:**
1. Cover half the container — does the element look centered?
2. Squint — where does your eye land?
3. Compare to similar elements — is centering consistent?

**Common Fixes:**
- Play icons: shift right ~5-10% of their width
- Triangles pointing up: shift down slightly
- Text: align to cap-height or x-height, not bounding box
- Icons in circles: adjust per icon shape

```xml
<centering_issue>
  <element>Play button icon</element>
  <container>Circular button</container>
  <mathematical_center>50%, 50%</mathematical_center>
  <visual_adjustment>Shift right 2px, no vertical change</visual_adjustment>
  <reason>Triangle visual weight is left of geometric center</reason>
</centering_issue>
```
</spatial_centering>

### Spacing Consistency

<spatial_spacing>
**The Problem:**
Same pixel value feels different depending on:
- What's being separated (text vs icon vs image)
- The "weight" of adjacent elements
- Background color/contrast

**How to Check:**
1. Do all similar elements feel equally spaced?
2. Does spacing create clear groupings?
3. Are there any "awkward gaps" or "crowded areas"?

**Correction Approach:**
- Space by visual separation, not pixels
- Heavier elements need more space
- Group related items with tighter spacing
- Separate unrelated items with more space

```xml
<spacing_issue>
  <location>Card header area</location>
  <elements>Icon, title, subtitle</elements>
  <current_spacing>All 8px gaps</current_spacing>
  <problem>Icon-to-title gap feels larger than title-to-subtitle</problem>
  <recommended_adjustment>Icon-title: 6px, Title-subtitle: 10px</recommended_adjustment>
  <reason>Icon has inherent padding; text lines relate more closely</reason>
</spacing_issue>
```
</spatial_spacing>

### Edge Alignment

<spatial_alignment>
**The Problem:**
Visually aligned edges may not be pixel-aligned because:
- Text has optical margins built into fonts
- Icons have visual weight offset from bounding box
- Rounded corners start their curve before the mathematical edge

**How to Check:**
1. Turn on alignment guides — do "aligned" elements actually align?
2. Does the page feel structured or chaotic?
3. Are there hidden alignment lines creating order?

**Correction Approach:**
- Align to optical edge, not bounding box
- Text should "hang" slightly into margins (optical margin alignment)
- Icons may need individual offsets
- Create consistent alignment zones, then optically adjust

```xml
<alignment_issue>
  <elements>Paragraph text and bullet icon</elements>
  <current_state>Mathematically left-aligned</current_state>
  <problem>Bullet feels indented compared to text</problem>
  <recommended_adjustment>Shift bullet left 2px to align visually</recommended_adjustment>
</alignment_issue>
```
</spatial_alignment>

## Category 3: Color Optical Issues

### Perceived Weight

<color_weight>
**The Problem:**
Different colors have different visual "weight":
- Saturated colors feel heavier than desaturated
- Dark colors feel heavier than light
- Warm colors advance; cool colors recede
- Some hues (red, yellow) grab attention more than others (blue, green)

**How to Check:**
1. Does the visual hierarchy match the importance hierarchy?
2. Are accent colors being used for the right elements?
3. Do any colors "jump out" inappropriately?

**Correction Approach:**
- Reduce saturation for background elements
- Increase saturation for focal points
- Balance warm/cool to create depth
- Use color weight to reinforce hierarchy

```xml
<color_weight_issue>
  <element>Secondary action button</element>
  <current_color>#FF5733 (saturated orange)</current_color>
  <problem>Competes with primary action despite lower importance</problem>
  <recommended_adjustment>Desaturate to #D4A57B or switch to neutral</recommended_adjustment>
</color_weight_issue>
```
</color_weight>

### Contrast Perception

<color_contrast>
**The Problem:**
WCAG contrast ratios measure mathematical contrast, but perceived contrast varies:
- Small text needs more contrast than large text
- Thin fonts need more contrast than bold fonts
- Colored backgrounds shift perceived text color
- Adjacent colors influence each other (simultaneous contrast)

**How to Check:**
1. Pass WCAG is minimum — does it FEEL readable?
2. Check on multiple devices/lighting conditions
3. Look for "vibrating" color combinations

**Correction Approach:**
- Exceed WCAG minimums for body text
- Test with actual content, not placeholder
- Avoid pure black on pure white (too harsh)
- Adjust for adjacent color influence

```xml
<contrast_issue>
  <element>Body text on colored card</element>
  <wcag_ratio>4.8:1 (passes AA)</wcag_ratio>
  <problem>Thin font weight makes text feel hard to read</problem>
  <recommended_adjustment>Increase font weight OR darken text to 7:1</recommended_adjustment>
</contrast_issue>
```
</color_contrast>

## Category 4: Component Optical Issues

### Icon Consistency

<icon_optical>
**The Problem:**
Icons from different sources/styles have inconsistent visual weight even at same pixel size:
- Stroke-based vs filled icons
- Different stroke weights
- Different levels of detail
- Different optical sizes within bounding box

**How to Check:**
1. Line up icons — do they feel the same size?
2. Do some icons feel "bolder" than others?
3. Is there consistent visual density?

**Correction Approach:**
- Standardize on one icon set/style
- Adjust individual icons to match visual weight
- Simpler icons may need slight size increase
- Complex icons may need slight size decrease

```xml
<icon_issue>
  <icons>Menu (3 lines), Search (magnifier), User (person)</icons>
  <problem>Search icon feels smaller than others</problem>
  <current_size>All 24px</current_size>
  <recommended_adjustment>Search icon: 26px to match visual weight</recommended_adjustment>
</icon_issue>
```
</icon_optical>

### Button and Touch Targets

<button_optical>
**The Problem:**
Buttons with same padding can look different depending on:
- Label length (short labels feel cramped)
- Icon presence (icons add visual weight)
- Border/shadow presence

**How to Check:**
1. Do all buttons feel equally "clickable"?
2. Do icon buttons feel balanced?
3. Is there enough touch target area? (44px minimum)

**Correction Approach:**
- Minimum width for short labels
- Optical padding adjustment for icons
- Consider visual padding vs actual padding

```xml
<button_issue>
  <buttons>"OK" button vs "Cancel Changes" button</buttons>
  <current_padding>12px 24px for both</current_padding>
  <problem>"OK" feels too narrow despite same padding</problem>
  <recommended_adjustment>Add min-width: 80px for short labels</recommended_adjustment>
</button_issue>
```
</button_optical>

## Refinement Process

<refinement_workflow>
1. **First Pass — Squint Test**
   - View design at 50% zoom
   - Squint to blur details
   - Note areas that feel "off"

2. **Second Pass — Component Audit**
   - Check each component category
   - Apply category-specific checks
   - Document issues found

3. **Third Pass — Context Check**
   - View in realistic context
   - Check responsive breakpoints
   - Test on actual devices if possible

4. **Fourth Pass — Fresh Eyes**
   - Step away, return later
   - View as a user would
   - Note any remaining friction
</refinement_workflow>

## Output Format

<refinement_output>
```xml
<optical_refinement_report>
  <summary>
    <issues_found count="N"/>
    <critical_issues count="N">Issues that significantly harm perception</critical_issues>
    <minor_issues count="N">Polish items</minor_issues>
  </summary>

  <typography_issues>
    <!-- Issues from Category 1 -->
  </typography_issues>

  <spatial_issues>
    <!-- Issues from Category 2 -->
  </spatial_issues>

  <color_issues>
    <!-- Issues from Category 3 -->
  </color_issues>

  <component_issues>
    <!-- Issues from Category 4 -->
  </component_issues>

  <before_after_recommendations>
    <recommendation priority="1">
      <element>What to change</element>
      <before>Current state</before>
      <after>Recommended state</after>
      <impact>Why this matters</impact>
    </recommendation>
  </before_after_recommendations>

  <overall_assessment>
    <craft_level>novice/developing/professional/exceptional</craft_level>
    <most_impactful_change>The single change that would help most</most_impactful_change>
  </overall_assessment>
</optical_refinement_report>
```
</refinement_output>

## Key Principle

> "Font design is all about minute adjustments to create optically pleasing letterforms."

The same applies to all design. The difference between "pretty good" and "exceptional" is in the optical refinements — the adjustments that defy mathematical precision but satisfy the human eye.
