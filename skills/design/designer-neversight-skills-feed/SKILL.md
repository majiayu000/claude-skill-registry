---
name: designer
description: Design assistant for UI mockups/wireframes, responsive HTML/CSS builds, brand kits, and presentation decks. Trigger when Codex needs to propose visual direction, lay out screens, draft or refine HTML/CSS for pages/components, assemble brand kits (palette, typography, voice, logo directions), or outline slide decks with visual guidance and speaker notes.
---

# Designer

Use this skill to quickly collect inputs, pick a deliverable type, and ship concise design outputs. Default to fast, lightweight artifacts (textual mockups, single-file HTML/CSS, structured brand kits, slide outlines) unless the user asks for higher fidelity.

## Inputs to gather (ask only what is missing)
- Product/goal, audience, platform (web/mobile), primary actions or KPIs
- Brand assets: palette, fonts, logos, design tokens, sample links; if repo has a design system, load its tokens first
- Constraints: breakpoints, accessibility targets (>= AA), performance, banned colors/fonts, delivery format
- Voice/tone keywords and mood (modern, playful, enterprise, minimal, editorial)

## Output menu
- UI mockup / wireframe plan
- Responsive HTML/CSS page or component
- Brand kit
- Presentation deck outline

## UI mockups and wireframes
1) Define the flow and primary user goals; list key screens and states.
2) Choose layout: grid (e.g., 12-col web, 4-col mobile), spacing scale, container widths, breakpoint behaviors.
3) Specify sections with hierarchy, placement, and density; call out above-the-fold priorities.
4) List components with states (default/hover/active/empty/error/loading/success) and content samples.
5) Provide visual direction: palette, typography scale, imagery style, iconography, motion hints.
6) Accessibility: contrast targets, tap targets, focus order, keyboard paths.

Output format (text first, then optional ASCII layout if helpful):
- Goal and audience
- Layout (desktop + mobile): grid, container widths, section ordering
- Components and states with sample copy/data
- Visual direction: palette (names + hex), type scale (font families, weights, sizes), imagery style
- Interaction notes: hover/focus, transitions, empty/error/loading behavior
- Accessibility notes

## HTML/CSS builds
1) Confirm scope: page vs component, interactions allowed (prefer no JS unless requested), breakpoints.
2) Define tokens: CSS custom properties for colors, spacing, radii, shadows, type scale.
3) Outline sections and semantic structure before coding.
4) Ship a single HTML file with embedded `<style>`; keep CSS small and readable.
5) Responsiveness: fluid widths, stack/reorder on narrow viewports, maintain readable line lengths.
6) Accessibility: semantic tags, proper headings, labels, `aria-*` where needed, `alt` text, focus styles.

Preferred HTML skeleton:
```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root {
      --bg: #0b1021;
      --surface: #111837;
      --text: #e6ecff;
      --muted: #9fb0d6;
      --accent: #7dd3fc;
      --accent-strong: #38bdf8;
      --radius: 14px;
      --shadow: 0 12px 40px rgba(0,0,0,0.35);
      --space: 18px;
      --max-width: 1080px;
    }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: "Inter", system-ui, -apple-system, sans-serif; background: radial-gradient(circle at 20% 20%, rgba(125,211,252,0.06), transparent 35%), #060916; color: var(--text); }
    .page { max-width: var(--max-width); margin: 0 auto; padding: calc(var(--space) * 2) calc(var(--space) * 1.5); }
    header, main, section { display: block; }
    .hero { display: grid; gap: calc(var(--space) * 1.5); grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); align-items: center; }
    .card { background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(255,255,255,0.02)); border: 1px solid rgba(255,255,255,0.07); border-radius: var(--radius); padding: calc(var(--space) * 1.2); box-shadow: var(--shadow); }
    .btn { display: inline-flex; align-items: center; gap: 10px; background: linear-gradient(135deg, var(--accent), var(--accent-strong)); color: #05101c; border: none; border-radius: 999px; padding: 12px 18px; font-weight: 700; text-decoration: none; box-shadow: 0 10px 24px rgba(56,189,248,0.3); }
    .btn.secondary { background: transparent; color: var(--text); border: 1px solid rgba(255,255,255,0.18); box-shadow: none; }
    @media (max-width: 720px) { .page { padding: calc(var(--space) * 1.5) var(--space); } }
  </style>
</head>
<body>
  <div class="page">
    <header class="hero">
      <div>
        <p style="color: var(--muted); letter-spacing: 0.12em;">AI CRM DESIGN</p>
        <h1 style="margin: 10px 0 16px; font-size: 40px; line-height: 1.05;">Design sharper experiences, faster.</h1>
        <p style="color: var(--muted); font-size: 17px; line-height: 1.6;">Pair clear structure with bold gradients and ample breathing room. Swap palette/type to match brand.</p>
        <div style="display: flex; gap: 10px; margin-top: 18px;">
          <a class="btn" href="#">Primary action</a>
          <a class="btn secondary" href="#">Secondary</a>
        </div>
      </div>
      <div class="card">
        <p style="margin: 0; color: var(--muted); font-size: 15px;">Live preview</p>
        <h3 style="margin: 6px 0 14px;">Key metric panel</h3>
        <div style="display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));">
          <div class="card" style="padding: 14px; box-shadow: none; border-radius: 10px;">
            <p style="margin: 0; color: var(--muted); font-size: 13px;">Conversion</p>
            <p style="margin: 6px 0 0; font-size: 26px; font-weight: 700;">42.3%</p>
          </div>
          <div class="card" style="padding: 14px; box-shadow: none; border-radius: 10px;">
            <p style="margin: 0; color: var(--muted); font-size: 13px;">Active deals</p>
            <p style="margin: 6px 0 0; font-size: 26px; font-weight: 700;">187</p>
          </div>
        </div>
      </div>
    </header>
  </div>
</body>
</html>
```

HTML/CSS checklist:
- Semantic tags, ordered headings, label every input, include focus states
- Avoid heavy libraries; prefer pure CSS; Tailwind/utility allowed only if requested
- Provide copy and sample data; avoid lorem ipsum unless unavoidable
- Keep gradients subtle, spacing generous, line length 60-80 chars

## Brand kits
1) Brand core: mission, audience, personality traits (3-5), tone words, no-go areas.
2) Palette: 1 primary, 1-2 secondary, neutrals, surface/backgrounds, states; include hex and suggested usage; ensure accessible text pairings.
3) Typography: heading and body pairs (weights, sizes, line heights, tracking), usage rules, substitutions if unavailable.
4) Imagery and iconography: style, stroke weight, color usage, photo guidelines, illustration motifs.
5) UI tokens: radii, shadows, border widths, spacing scale, button styles, form states, chip/badge patterns.
6) Logo directions: shapes/constraints if no logo exists; placement, clear space, sizing if a logo exists.

Output format:
- Brand story: mission, voice, do/dont
- Palette table with hex + accessibility notes
- Type stack: headings/body/code with usage rules
- Tokens: spacing, radius, shadows, button styles, form states
- Imagery/icon/illustration guidance
- Sample application: navbar, hero block, CTA, card, notification

## Presentation decks
1) Confirm audience, objective, CTA, and time/slide budget.
2) Define narrative spine: hook -> problem -> insight -> solution -> proof -> roadmap -> CTA.
3) Set theme: palette, type, layout rhythm, image style; align to brand kit when present.
4) Produce slide-by-slide outline: title, key point(s), visuals per slide, speaker notes or script, time allocation.
5) Include consistency cues: grid, margin/padding, hierarchy patterns, icon/photo rules.

Output format:
- Deck goal and audience
- Theme (palette, typography, layout rules, image style)
- Slide list with: title, bullet content, visual directions (charts/diagrams/photos), speaker notes, timing
- Closing slide CTA and backup/appendix ideas

## Quality checks (all deliverables)
- Does the output reflect the goal, audience, and constraints?
- Readability: contrast AA+ for text, line length, font sizes; touch targets >= 44px; focus states visible.
- Responsiveness: define breakpoints and how sections/components adapt.
- Consistency: spacing scale, radii, shadows, icon stroke weights, copy tone.
- Clarity: avoid lorem ipsum; keep actionable next steps or code ready to drop in.
