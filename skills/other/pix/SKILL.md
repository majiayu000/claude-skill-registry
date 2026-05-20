---
name: pix
description: Launches an autonomous, pixel-perfect UI implementation loop using Figma MCP and Chrome.
allowed-tools: [Bash, Read, Glob, Grep, Edit, Write]
---

# /pix: The Pixel-Perfect Autonomous Loop

User provides a Figma link. You implement it pixel-perfect. That's it.

> Tool names may vary based on your MCP configuration (e.g., `figma__get_screenshot` or `mcp__figma__get_screenshot`). Run `/mcp` to see available tools.

## Resource Strategy

### Tool Costs

| Tool | Cost | Use For |
|------|------|---------|
| `get_metadata` | **Cheap** | Node tree with child IDs, positions, sizes. No styling. |
| `get_variable_defs` | **Cheap** | All design tokens (colors, spacing, radii) as name→value. |
| `get_code_connect_map` | **Cheap** | Check which Figma nodes map to existing code components. |
| `get_screenshot` | **Medium** | Visual image of a specific node. Target a `nodeId` to crop/zoom. |
| `get_design_context` | **Expensive** | Full code + styling + assets. NEVER call on a large parent — call on individual sections. |

**Core rule**: Cheap calls first to build a map, then expensive calls only on the smallest necessary nodes.

### Image Budget

Claude API limits images to 2000px per dimension when >20 images are in a conversation. Old images cannot be individually removed.

- **~20 screenshots per conversation** before the resolution limit kicks in
- **3-image working set**: Figma layout (overview), Figma detail (current section), Chrome state (rendered result)
- **Never re-screenshot a static Figma node** — designs don't change mid-session
- **Use `getComputedStyle` for numerical properties** — zero image cost
- **Recovery**: `/compact` drops old images from context (see Recovery section)

---

## Phase 1: Reconnaissance

When the user provides a Figma link, extract `fileKey` and `nodeId` from the URL and immediately start working. If any MCP call or Chrome interaction fails, run the [Doctor Check](#doctor-check) to diagnose and fix, then resume.

### Step 1: Get the Node Tree

Call `get_metadata(nodeId, fileKey)`:

```xml
<Frame id="45:1" name="Header" type="FRAME" x="0" y="0" width="1440" height="80">
  <Component id="45:10" name="Logo" x="20" y="16" width="120" height="48"/>
  <Frame id="45:15" name="NavLinks" x="400" y="20" width="600" height="40">
    <Text id="45:16" name="Home" x="0" y="0" width="60" height="40"/>
  </Frame>
</Frame>
```

Build a **mental map**:
- Identify every major section and note each `nodeId`
- Note positions and sizes to understand the layout grid
- Identify components vs frames vs text vs icons

### Step 2: Extract All Design Tokens (Once)

Call `get_variable_defs(nodeId, fileKey)`. Save the result — do NOT call this again.

### Step 3: Check Existing Components

Call `get_code_connect_map(nodeId, fileKey)`. For matched components, follow this priority:
1. **Reuse as-is** — if it covers the Figma design exactly
2. **Extend minimally** — add a prop or variant if close but not exact
3. **Compose** — combine existing components
4. **Create new** — only if nothing existing fits

### Step 4: Visual Overview

Call `get_screenshot(nodeId, fileKey)` on the root selection. This is Image 1 of your budget — your layout reference. Do NOT retake it.

**At this point you have NOT called `get_design_context` at all.** You have a complete structural map, all tokens, reusable component info, and a visual reference — all from cheap calls.

---

## Phase 2: Study & Implement (Code in the Dark)

Study the design deeply, memorize every detail, then code from memory.

### Step 1: Layout Shell

Using the metadata tree, implement the outer layout:
- Container dimensions and positioning (flex, grid)
- Major section placement
- Background colors from tokens
- Borders and dividers

The metadata + visual overview are usually sufficient. Only call `get_design_context` if you need specific properties you can't infer.

### Step 2: Study Every Section

For each major section:

1. **Figma Detail**: `get_screenshot(sectionNodeId, fileKey)` — zoomed-in visual reference.

2. **Design Context**: `get_design_context(sectionNodeId, fileKey)` — text only, no image cost. If truncated, use child node IDs from `get_metadata` and fetch children individually.

3. **Absorb every detail**: fonts, sizes, weights, colors, spacing, borders, shadows, icon shapes. Burn it into memory.

4. **Color sanity check**: Compare `get_design_context` colors against the Figma screenshot. If the screenshot reveals opacity layering, overlapping fills, or gradients — the raw token values will be wrong. Use the visual truth, not the raw token.

**No Chrome screenshots during this phase.** You are studying, not checking.

**Key rule**: NEVER call `get_design_context` on the root selection. Always target the smallest meaningful node.

### Step 3: Code from Memory

Implement everything using what you memorized:
- Design context output for exact properties
- Tokens from Phase 1 (do not re-extract)
- Reusable components from Phase 1
- **Respect project rules**: Check for `.claude/rules`, `CLAUDE.md`, and project instruction files. Follow established patterns for component structure, file placement, naming, and styling. Figma MCP output is a design representation — translate it into your project's conventions, don't paste it verbatim.

**Frontend only.** Don't touch backend, API routes, or database unless the user explicitly asks. Use mock/placeholder data if APIs don't exist yet.

**Minimize screenshots during coding.** You studied the design — use what you memorized. But if you're missing crucial data for a specific element (exact icon shape, a nested layout you didn't drill into, a subtle gradient), take a targeted `get_screenshot` on that Figma node rather than guessing. Getting it right the first time is cheaper than a refinement round.

### Step 4: Design System Sync

NEVER hardcode values. Sync to the project's design system:

- **Tailwind**: Update `tailwind.config.*` if a token is missing. Never `text-[#f3f3f3]`.
- **CSS-in-JS**: Add tokens to the theme object. Never inline hex.
- **Component Library**: Map to existing theme tokens. Never bypass the theme.
- **CSS/SCSS**: Add custom properties to `:root`. Never scatter magic values.

### Step 5: Icons & Assets

**Icons**: Find a match in the project's existing icon library first — by name, then by visual shape. Match `stroke-width` and `size` exactly.

**Fallback**: If the layer name doesn't map, `get_screenshot(iconNodeId)` and identify visually. Match by shape, not name.

**Images/illustrations**: Download from the Figma MCP assets endpoint and save to the project's public/static folder. Don't create inline SVG blobs for complex illustrations. Don't import new icon packages without asking.

### Property Checklist

Before writing code for ANY element, verify ALL applicable properties:

- **Text**: font-family, font-size, font-weight, line-height, letter-spacing, color, opacity, text-align, text-decoration, text-transform
- **Container**: width, height, min/max-width, padding (all 4), margin, background-color, border-radius, border-width/color/style, box-shadow, opacity, overflow
- **Icon**: size, fill, stroke, stroke-width, color (independent from parent text)
- **Button/Link**: All text + container props + cursor, hover/active/disabled states
- **Image**: width, height, object-fit, border-radius, border, aspect-ratio
- **Spacing**: gap, row-gap, column-gap

**Layout Principle**: Avoid hardcoded sizes. With correct font-size, line-height, padding, and parent width, elements render correctly. Hardcoded dimensions are a symptom of wrong upstream layout.

**Responsive**: Consider how the component adapts to different screen sizes. Use the project's responsive approach (Tailwind breakpoints, media queries, container queries).

**Never use approximate Tailwind classes** (like `text-zinc-500`) when exact hex values are available from tokens.

---

## Phase 3: Refinement Loop

You think you're done. Now prove it. Keep cycling until the result is perfect.

### The Loop

**Step 1: Chrome screenshot (1 image)**

First look at what you built. Compare against Figma screenshots in context. Be extremely picky:
- Visual alignment issues
- Missing elements or wrong proportions
- Layout shifts, spacing that looks off
- Wrong icon shapes
- Color or weight mismatches
- **Color comparison**: Sample dominant colors from Figma vs Chrome. Flag anything that looks off — opacity/layering can cause perceived differences even when hex values match.

**Step 2: Numerical audit (zero images)**

Run `getComputedStyle` on every element and compare against Figma values:

```js
const el = document.querySelector('.target-element');
const s = getComputedStyle(el);
JSON.stringify({
  padding: s.padding, margin: s.margin, gap: s.gap,
  backgroundColor: s.backgroundColor, color: s.color,
  fontSize: s.fontSize, fontWeight: s.fontWeight,
  lineHeight: s.lineHeight, letterSpacing: s.letterSpacing,
  borderRadius: s.borderRadius, borderWidth: s.borderWidth,
  borderColor: s.borderColor, boxShadow: s.boxShadow
});
```

12px is not 10px. #f97316 is not #ff611c.

**CSS specificity check**: Icons inside wrapper components (Button, Link) often get wrong colors from parent overrides. Run `getComputedStyle` on the SVG itself. If the computed color doesn't match, use the Tailwind important modifier (prefix with !) to force it.

**Step 3: Picky mismatch list**

Combine visual + numerical issues into one list. No issue is too small. 2px off? List it.

**Step 4: Fix everything**

Batch all fixes. No screenshots between individual fixes.

**Step 5: Repeat from Step 1**

**Exit condition**: Retake `get_screenshot` on the Figma root node. Place side-by-side with your latest Chrome screenshot. Compare colors directly. Only move on when both screenshots match AND numerical audit shows zero mismatches.

### Icon & Shape Verification

If an icon looks wrong during any loop iteration:
- `get_screenshot(iconNodeId, fileKey)` on the Figma icon
- Screenshot Chrome icon at 3x zoom
- Compare the SILHOUETTE — stroke count, shape, proportions

Common mismatches:
- "filter" → often lines-with-circles, NOT a funnel
- "calendar" → many variants (with/without dots)
- "mail" → open vs closed envelope

If it doesn't match: try another icon from the library, or use the Figma SVG inline.

### Anti-Pattern: "Looks Good Enough"

This ALWAYS misses: 2-4px spacing differences, wrong icon variant, slightly wrong color, missing shadow, font weight mismatch.

**RULE**: Not done until zero visual mismatches AND zero numerical mismatches.

---

## Recovery: Compact & Resume

If you hit the image limit (or proactively after ~15 screenshots):

1. **Run `/compact`** — summarizes conversation, drops old images. Notes and progress are preserved.
2. **Retake 3 reference images**: Figma overview, Figma detail (current section), Chrome state.
3. **Continue the refinement loop** — you still know everything from the compacted history. ~17 more image slots available.

Repeatable: compact → retake 3 → continue → compact again if needed.

---

## Phase 4: User Review

**Stop and ask**:
- "Here's the final result. Are you happy with it?"
- "If something looks off, paste a Figma 'Link to Selection' for the specific area."

If the user provides a new link, re-run Phases 1-3 scoped to that selection.

---

## Doctor Check

Run this ONLY when something fails. Not at startup.

**Figma MCP not working?**
- Call `whoami` to check authentication
- Not connected → alert user to configure Figma MCP
- Not authenticated → guide through Figma OAuth

**Chrome not responding?**
- Ensure Claude Chrome extension is active
- Navigate to the correct localhost page

**Dev server not running?**
- Check lockfile: `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm), `bun.lockb` (bun)
- Read `package.json` for dev command and port
- Default ports: 5173 (Vite), 3000 (Next/CRA), 8080 (Vue CLI)
- `lsof -i :<PORT>` — if not running, start in background

**Unknown design system or icon library?**
- Scan `package.json`: `tailwindcss`, `styled-components`, `@emotion/*`, `@chakra-ui/*`, `@mui/*`, `@mantine/*`
- Icon libraries: `lucide-react`, `@heroicons/react`, `react-icons`, `@radix-ui/react-icons`, `@fortawesome/*`, `@phosphor-icons/react`, `@tabler/icons-react`

---

## Examples

**Invocation:**
```
/pix
> Paste Figma link: https://figma.com/design/abc123/MyApp?node-id=42-100
```

**What happens:**
1. Recon: `get_metadata` + `get_variable_defs` + `get_code_connect_map` (0 images)
2. Figma overview: `get_screenshot` on root (image 1)
3. Study section 1: `get_screenshot` (image 2) + `get_design_context` (text). Memorize.
4. Study section 2: `get_screenshot` (image 3) + `get_design_context` (text). Memorize.
5. Code everything from memory (0 images)
6. **Loop round 1**: Chrome screenshot (image 4) + audit → 4 mismatches + 1 bad icon
7. Fix mismatches. Icon check: `get_screenshot` on Figma icon (image 5) — swap it.
8. **Loop round 2**: Chrome screenshot (image 6) + audit → 1 spacing issue
9. Fix spacing.
10. **Loop round 3**: Chrome screenshot (image 7) + audit → zero mismatches.
11. **Final check**: Retake Figma `get_screenshot` (image 8) side-by-side with Chrome → match.
12. Done. Total: 8 images.

**Bad patterns:**
- Screenshotting every element individually (budget killer)
- Re-screenshotting the same Figma node (it's static)
- Chrome screenshots after every small CSS tweak
- Using screenshots to verify what `getComputedStyle` gives for free
- Not running `/compact` when approaching image limit
- `get_design_context` on root (token waste)
- `get_variable_defs` more than once (redundant)
- Hardcoded hex in Tailwind (`text-[#f3f3f3]`)
- Magic width numbers (`w-[247px]`)
- Saying "looks close" without numerical verification
