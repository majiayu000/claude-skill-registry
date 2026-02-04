---
name: timeline
description: Create interactive 10-10-10 timeline simulator with parallel tracks and regret markers. Use when user wants temporal analysis, project forward, see consequences over time, or run regret minimization.
---

# Timeline Playground

Creates an interactive HTML canvas for visualizing decisions across time horizons with probability and regret analysis.

## When to Use

- "show me over time"
- "project forward"
- "10-10-10 this"
- "what will I regret"
- Temporal decision analysis
- Comparing options across time horizons

## What It Creates

A single HTML file with:
- Parallel horizontal tracks (one per decision option)
- Three time zones: 10 minutes, 10 months, 10 years
- Draggable event cards with probability
- Regret markers for flagging future regret points
- Prompt output for extracting insights

## Skill Protocol

### 1. Understand the Decision

Before generating, clarify:
- What decision is being analyzed?
- What are the options (2-4)?
- What events/outcomes matter at each time horizon?
- What would cause regret?

### 2. Generate the Playground

Create a single self-contained HTML file following the structure in [references/probability-cones.md](references/probability-cones.md).

**Core requirements:**
- Single HTML file, all CSS/JS inline
- No external dependencies
- Dark theme, system font for UI
- Live preview on every change
- Copy button with "Copied!" feedback

### 3. State Shape

```javascript
const state = {
  options: [
    { id: 'optA', label: 'Option A', color: '#3b82f6' },
    { id: 'optB', label: 'Option B', color: '#10b981' }
  ],
  events: [
    { id: 1, optionId: 'optA', timeZone: '10min', x: 50, label: 'Immediate relief', probability: 95 },
    { id: 2, optionId: 'optA', timeZone: '10mo', x: 150, label: 'Skills atrophy', probability: 70 }
  ],
  regretMarkers: [
    { optionId: 'optA', timeZone: '10yr', note: 'Missed growth opportunity' }
  ],
  focusedTimeZone: 'all'
};
```

### 4. Layout

```
+-------------------+----------------------------------+
|  Controls:        |  Timeline Canvas                 |
|  • Options list   |  10 min | 10 months | 10 years  |
|  • Add event      |  -------|-----------|----------  |
|  • Probability    |  [Option A track: events...]    |
|    slider         |  [Option B track: events...]    |
|                   +----------------------------------+
|  Regret markers:  |  Prompt output                   |
|  • Listed by      |  [ Copy Prompt ]                 |
|    option         |                                  |
+-------------------+----------------------------------+
```

### 5. Unique Features

**Parallel Tracks:**
- Each decision option gets its own horizontal track
- Tracks stack vertically, labeled with option name and color
- Time flows left-to-right across three zones
- Zone dividers at 10min/10mo/10yr boundaries

**Probability Visualization:**
- Events display as cards on tracks
- Opacity reflects probability (100% = solid, 20% = faded)
- Events in distant future naturally fade (uncertainty cone)
- User can adjust probability via slider on each event

**Regret Markers:**
- Click any point on a track to add a regret flag
- Flag prompts: "At this moment, would I wish I'd chosen differently?"
- Flags include note field for context
- Red markers aggregate in sidebar for comparison

**Time Zone Focus:**
- Toggle to focus on single time zone
- Hides other zones for detailed analysis
- Useful for deep-diving specific horizons

### 6. Canvas Rendering

Use `<canvas>` or SVG with:
- Horizontal bands per option (track height ~80px)
- Vertical dividers for time zones
- Event cards as rounded rectangles
- Drag behavior for repositioning within zone
- Regret flags as triangular markers

```javascript
function draw() {
  ctx.clearRect(0, 0, W, H);
  drawTimeZones();
  state.options.forEach((opt, i) => drawTrack(opt, i));
  state.events.forEach(e => drawEvent(e));
  state.regretMarkers.forEach(r => drawRegretMarker(r));
}

function drawEvent(event) {
  ctx.globalAlpha = event.probability / 100;
  ctx.fillStyle = getOptionColor(event.optionId);
  ctx.fillRect(event.x, getTrackY(event.optionId), 120, 40);
  ctx.globalAlpha = 1;
  ctx.fillStyle = '#fff';
  ctx.fillText(event.label, event.x + 8, getTrackY(event.optionId) + 24);
}
```

### 7. Prompt Output

Generate natural language analysis:

```
10-10-10 Analysis for [DECISION]:

**Option A: [Label]**
- 10 minutes: [event] (95% likely)
- 10 months: [event] (70% likely), [event] (50% likely)
- 10 years: [event] (40% likely)
- Regret risk: Low at 10min, Medium at 10mo, High at 10yr

**Option B: [Label]**
- 10 minutes: [event] (80% likely)
- 10 months: [event] (75% likely)
- 10 years: [event] (60% likely)
- Regret risk: Medium at 10min, Low at 10mo, Low at 10yr

**Comparison:**
- Short-term winner: Option A (immediate relief)
- Long-term winner: Option B (sustainable growth)
- Reversal point: Around month 6, Option B overtakes if [condition]

**Regret Analysis:**
- Option A: "Missed growth opportunity" flagged at 10yr
- Option B: No regret markers

**Recommendation:**
If short-term relief is critical, choose A with exit plan at 6 months.
If long-term matters more, choose B and accept short-term discomfort.
```

### 8. After Browser Interaction

When user returns from the playground:
1. Ask what patterns they noticed
2. Parse their description or pasted state
3. Generate recommendation based on regret markers
4. Identify reversal points and decision triggers

## Anti-Patterns

- More than 4 options (overwhelming)
- No probability decay over time (false precision)
- Missing regret markers (core feature unused)
- Static image without drag/edit (not a playground)
- External dependencies (breaks if CDN down)

## Integration

- Feeds into `hope:future` for regret minimization
- Uses `hope:soul` 10-10-10 tool patterns
- Can inform Quality Footer reversibility assessment
