---
name: "ascii-art-alignment"
description: "Create perfectly aligned ASCII diagrams using the hybrid character strategy."
---

# ASCII Art Alignment Skill

> Create perfectly aligned ASCII diagrams using the hybrid character strategy.

## Format Selection: Mermaid-First Principle

**Default to Mermaid** for all architecture, flow, and relationship diagrams. ASCII art is a **last resort** for specific use cases. SVG is preferred for polished, brand-ready illustrations.

| Use Case | Format | Reason |
|----------|--------|--------|
| Architecture diagrams | **Mermaid** | Auto-layout, renderable, LLM-readable |
| Flowcharts / sequences | **Mermaid** | Native tooling (`renderMermaidDiagram`) |
| Relationship maps | **Mermaid** | ER, class, graph diagrams |
| Branded visuals / logos | **SVG** | Scalable, animatable, platform-specific |
| Infographics / illustrations | **SVG** | Full design control, dark/light mode |
| UI mockups / wireframes | ASCII | Embedded in code comments |
| Terminal output examples | ASCII | Literal reproduction |
| Inline feature lists in boxes | ASCII | README decorations |
| Conversation mockups | ASCII | Chat-style formatting |

**Decision rule**: If a diagram shows *structure or flow*, use Mermaid. If it shows *a visual design*, use SVG. If it's *embedded in code or terminal context*, use ASCII.

## The Problem

ASCII art diagrams render with misaligned lines due to inconsistent character widths across fonts and rendering contexts.

## The Solution: Hybrid Character Strategy

> Unicode boxes + ASCII arrows + obsessive line counting = perfect alignment

---

## Character Reference

### Use These (Consistent Width)

**Box Drawing (Unicode):**

```text
┌ ─ ┐    Top corners and horizontal
│        Vertical lines
└ ┘      Bottom corners
├ ┤      T-junctions (left/right)
┬ ┴      T-junctions (top/bottom)
┼        Cross junction
```

**Arrows (Plain ASCII):**

```text
v    Down arrow (lowercase v)
^    Up arrow (caret)
<    Left arrow
>    Right arrow
<--> Bidirectional
---> Flow direction
```

### Avoid These (Break Alignment)

| Bad | Problem | Good Alternative |
| --- | ------- | ---------------- |
| `▼ ▲ ◄ ►` | Triangle arrows render as 2 chars | `v ^ < >` |
| `→ ← ↑ ↓` | Arrow symbols inconsistent width | `> < ^ v` |
| `◄──►` | Mixed arrows = guaranteed misalign | `<-->` |

**Note**: `→` in prose is fine (e.g., "A → B means..."). Only avoid inside ASCII box diagrams.

### Emojis in ASCII Boxes

**Principle**: Emojis add personality and visual scanning. Don't sacrifice them for perfect alignment.

| Approach | When to Use |
| -------- | ----------- |
| Emojis with calibration | Default — emojis are worth the effort |
| ASCII markers `[!] [*]` | Only if emoji causes severe rendering issues |

**Calibration Guide**:

| Emoji Type | Visual Width | Adjustment |
| ---------- | ------------ | ---------- |
| 🛡️ (with variation selector) | ~2 chars | Remove 2 spaces after |
| 📚 🧪 📦 👥 (standard) | ~2 chars | Remove 1 space after |

**Process**: Add emoji → check line length → adjust spaces → verify visually.

**Accept**: Minor alignment imperfections are OK. Emojis > perfect alignment.

---

## Validation Checklist

1. ☐ Count characters in EVERY line of outer box
2. ☐ All lines must have identical character count
3. ☐ Use `v` not `▼` for down arrows
4. ☐ Use `<-->` not `◄──►` for bidirectional
5. ☐ Never put emojis inside ASCII boxes
6. ☐ Test in VS Code preview AND GitHub rendering
7. ☐ After fixing inner content, re-count total width
8. ☐ Center text within inner boxes (visual balance)

---

## Real-Time Validation Tip

When editing ASCII art in VS Code:

1. **Select** the entire code block
2. **Status bar** shows character count per line (bottom right)
3. **Each line** inside box should match outer border width
4. **Monospace font** is mandatory - non-monospace breaks everything

**Quick mental math**: If outer box is 43 chars, inner content line = `│` + 41 spaces/content + `│` = 43

---

## Debugging Method

### Step 1: Identify Symptom

- Right border looks jagged
- Inner boxes don't align with outer border
- User reports "lines are misaligned"

### Step 2: Count Characters

```text
Line X: │  ┌─────────┐    ┌─────────┐    │  = ?? chars
        ^                              ^
        Count from here                To here
```

### Step 3: Compare to Border

Outer border (top `┌───┐` line) sets the standard width. Every line must match EXACTLY.

### Step 4: Fix Off-by-One

The most common bug:

```text
┌───────────────────────────────────────┐  <- 41 chars
│  ┌─────────┐    ┌─────────┐    │      <- 40 chars (WRONG!)
└───────────────────────────────────────┘  <- 41 chars
```

Fix: Add one space before closing `│`.

---

## PowerShell Validation

### Find All Misaligned Lines

```powershell
$content = Get-Content "file.md"
$target = 67  # Your expected width
$content | ForEach-Object -Begin {$i=0} -Process {
    $i++
    if ($_ -match '^\│' -and $_.Length -ne $target) {
        "{0,4}: [{1}] {2}" -f $i, $_.Length, $_
    }
}
```

### Quick Stats

```powershell
$content | Where-Object { $_ -match '^\│' } |
    Group-Object Length | Sort-Object Name |
    ForEach-Object { "{0} chars: {1} lines" -f $_.Name, $_.Count }
```

### Multi-Width Documents

```powershell
$valid = @(67, 75, 91)  # Multiple valid widths
$content | Where-Object { $_ -match '^\│' } | ForEach-Object {
    if ($_.Length -notin $valid) { "[$($_.Length)] $_" }
}
```

### Find Problematic Unicode Characters

Scan multiple files for Unicode arrows that should be ASCII:

```powershell
Select-String -Path "*.md" -Pattern '[▼▲◄►]' |
    Select-Object Filename, LineNumber, Line
```

---

## Example Templates

### Basic Architecture

```text
┌─────────────────────────────────────────┐
│             ARCHITECTURE                │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────┐       ┌───────────┐      │
│  │ Component │ ----> │ Component │      │
│  │     A     │       │     B     │      │
│  └───────────┘       └───────────┘      │
│        │                   │            │
│        v                   v            │
│  ┌─────────────────────────────────┐    │
│  │          Shared Layer           │    │
│  └─────────────────────────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

### Side-by-Side Comparison

```text
┌─────────────────────────────┐    ┌─────────────────────────────┐
│          BEFORE             │    │           AFTER             │
├─────────────────────────────┤    ├─────────────────────────────┤
│                             │    │                             │
│  - Manual process           │    │  - Automated workflow       │
│  - Error prone              │    │  - Validated inputs         │
│  - Slow feedback            │    │  - Real-time feedback       │
│                             │    │                             │
└─────────────────────────────┘    └─────────────────────────────┘
```

### Status Checklist

```text
┌─────────────────────────────────────────┐
│           PROJECT STATUS                │
├─────────────────────────────────────────┤
│                                         │
│  [x] Phase 1: Planning         DONE     │
│  [x] Phase 2: Design           DONE     │
│  [~] Phase 3: Development      75%      │
│  [ ] Phase 4: Testing          PENDING  │
│                                         │
│  Legend: [x]=Done [~]=Progress [ ]=Todo │
│                                         │
└─────────────────────────────────────────┘
```

### Pipeline Flow

```text
┌───────────────────────────────────────────────────────────────┐
│                   DATA PROCESSING PIPELINE                    │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │  INPUT  │--->│ VALIDATE│--->│ PROCESS │--->│ OUTPUT  │     │
│  └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘     │
│       │              │              │              │          │
│       v              v              v              v          │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │   Raw   │    │  Clean  │    │ Enriched│    │  Final  │     │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## Mermaid vs ASCII Decision

> **Default**: Use Mermaid unless you have a specific reason for ASCII. Mermaid auto-layouts, renders interactively, and supports theming via the **markdown-mermaid** skill.

| Diagram Type | Use | Reason |
| ------------ | --- | ------ |
| Flow charts | **Mermaid** | Auto-layout, interactive, GitHub-native |
| Gantt/Timeline | **Mermaid** | Native support, date handling |
| Sequence diagrams | **Mermaid** | Lifelines, activation bars |
| State machines | **Mermaid** | Standard notation, auto-routing |
| ER diagrams | **Mermaid** | Relationship cardinality notation |
| UI Mockups | **ASCII** | Precise pixel-level layout control |
| Conversation mockups | **ASCII** | Text-heavy, spacing matters per-character |
| Feature lists in boxes | **ASCII** | Better for bullet lists inside boxes |
| Simple architecture | **Either** | Mermaid for auto-layout, ASCII for exact control |
| Inline code comments | **ASCII** | Can't embed Mermaid in source code |
| Terminal output | **ASCII** | Rendered in monospace, no Mermaid support |

**When ASCII excels**: Content with precise character-level alignment, mixed bullet lists inside boxes, or rendering contexts without Mermaid support (terminals, code comments, plain text files).

---

## Anti-Patterns

### Emojis Inside Boxes

```text
❌ WRONG:
│ ✅ Complete │  <- Misaligned (emoji width varies)

✅ CORRECT:
│ [x] Complete │  <- Aligned
```

### Unicode Arrows

```text
❌ WRONG:
│     ▼        │  <- Misaligned (arrow width varies)

✅ CORRECT:
│     v        │  <- Aligned
```

### Visual-Only Validation

❌ **Wrong**: "It looks fine to me"

✅ **Correct**: Run PowerShell validation, confirm line counts match

---

## Synapses

See [synapses.json](synapses.json) for connection mapping.
