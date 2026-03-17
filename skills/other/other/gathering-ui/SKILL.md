---
name: gathering-ui
description: The drum sounds. Chameleon and Deer gather for complete UI work. Use when designing interfaces that must be both beautiful and accessible.
---

# Gathering UI 🌲🦎🦌

The drum echoes through the glade. The Chameleon shifts its colors, painting the forest with glass and light. The Deer senses what others cannot see, ensuring every path is clear. Together they create spaces that welcome all wanderers—beautiful to behold, accessible to all.

## When to Summon

- Designing new pages or interfaces
- Implementing complete UI features
- Ensuring visual design meets accessibility standards
- Creating Grove-themed experiences
- When beauty and inclusion must coexist

---

## Grove Tools for This Gathering

Use `gw` and `gf` throughout. Quick reference for UI work:

```bash
# Find existing UI patterns and components
gf --agent search "GlassCard|GlassButton"  # Find glass component usage
gf --agent glass                    # Find glassmorphism patterns
gf --agent store                    # Find store usage (season, theme)
gf --agent routes                   # Understand route structure

# Test UI changes
gw ci --affected                    # Run CI on affected packages
```

---

## The Gathering

```
SUMMON → ORGANIZE → EXECUTE → VALIDATE → COMPLETE
   ↓         ↲          ↲          ↲          ↓
Receive  Dispatch   Animals    Verify   UI
Request  Animals    Work       Design   Complete
```

### Animals Mobilized

1. **🦎 Chameleon** — Design the UI with glassmorphism and seasonal themes
2. **🦌 Deer** — Audit accessibility and ensure inclusive design

---

### Phase 1: SUMMON

_The drum sounds. The glade awaits..._

Receive and parse the request:

**Clarify the UI Work:**

- What page/component are we designing?
- What's the emotional tone?
- Which season should it reflect?
- What's the content structure?

**Scope Check:**

> "I'll mobilize a UI gathering for: **[UI description]**
>
> This will involve:
>
> - 🦎 Chameleon designing with Grove aesthetics
>   - Glassmorphism containers
>   - Seasonal colors and themes
>   - Randomized forests if appropriate
>   - Lucide icons (no emojis)
> - 🦌 Deer auditing for accessibility
>   - Keyboard navigation
>   - Screen reader compatibility
>   - Color contrast
>   - Reduced motion support
>
> Proceed with the gathering?"

---

### Phase 2: ORGANIZE

_The animals take their positions..._

Dispatch in sequence:

**Dispatch Order:**

```
Chameleon ──→ Deer
     │            │
     │            │
Design         Audit
UI             Accessibility
```

**Dependencies:**

- Chameleon must complete before Deer (needs UI to audit)
- May iterate: Deer findings → Chameleon fixes → Deer re-audit

---

### Phase 3: EXECUTE

_The glade transforms..._

Execute each phase:

**🦎 CHAMELEON — ADAPT**

```
"Reading the light, sketching the form..."

Phase: READ
- Determine season and emotional tone
- Choose decoration level (minimal/moderate/full)

Phase: SKETCH
- Build glassmorphism structure
- Layer: Background → Decorations → Glass → Content

Phase: COLOR
- Apply seasonal palette
- Import from @autumnsgrove/groveengine/ui/nature

Phase: TEXTURE
- Add randomized forests if appropriate
- Weather effects (snow, petals, leaves)
- Seasonal birds
- Lucide icons

Phase: ADAPT
- Mobile responsive
- Reduced motion support
- Touch targets 44px minimum
- Dark mode variants
- GroveTerm components for all Grove terminology
  (never hardcode — use GroveTerm, GroveSwap, GroveText)
  ([[term]] syntax for data-driven content strings)

Output:
- Complete Svelte components
- Styled with Tailwind
- Glass variants applied
- Seasonal decorations
- Grove terminology uses GroveTerm V2 components
```

**🦌 DEER — SENSE**

```
"Listening for barriers, scanning the path..."

Phase: LISTEN
- Understand user needs
- WCAG AA standard

Phase: SCAN
- Automated scan with axe-core
- Lighthouse accessibility audit

Phase: TEST
- Keyboard navigation test
- Screen reader test (VoiceOver/NVDA)
- Zoom to 200%
- Reduced motion check

Phase: GUIDE
- Fix any issues found
- Add ARIA labels where needed
- Ensure focus management
- Proper heading structure

Phase: PROTECT
- ESLint jsx-a11y plugin
- axe-core in CI

Output:
- Accessibility audit report
- Issues fixed
- Documentation of a11y features
```

---

### Phase 4: VALIDATE

_The design stands. Both animals verify..._

**Validation Checklist:**

- [ ] Chameleon: UI matches Grove aesthetic
- [ ] Chameleon: Seasonal theme appropriate
- [ ] Chameleon: Glassmorphism readable
- [ ] Chameleon: Mobile responsive
- [ ] Deer: Keyboard navigation works
- [ ] Deer: Screen reader compatible
- [ ] Deer: Color contrast passes (4.5:1)
- [ ] Deer: Reduced motion respected
- [ ] Deer: Touch targets adequate (44px)
- [ ] Both: Grove terminology uses GroveTerm components (not hardcoded)
- [ ] Both: `[[term]]` syntax used in data-driven content strings

**Quality Gates:**

```
Chameleon completes → Deer audits
                         ↓
               Issues found?
                  /        \
               Yes          No
                |            |
         Chameleon fixes     ↓
                |         Proceed
         Deer re-audit
                |
            Complete
```

---

### Phase 5: COMPLETE

_The gathering ends. A welcoming space awaits..._

**Completion Report:**

```markdown
## 🌲 GATHERING UI COMPLETE

### UI: [Name]

### Animals Mobilized

🦎 Chameleon → 🦌 Deer

### Design Decisions

- **Season:** [spring/summer/autumn/winter/midnight]
- **Decoration Level:** [minimal/moderate/full]
- **Glass Variants Used:** [surface/tint/card/accent]

### Visual Elements

- Randomized forests: [count] trees
- Weather effects: [snow/petals/leaves/none]
- Seasonal birds: [species]
- Icons: Lucide ([list])

### Accessibility Features

- Keyboard navigation: ✅
- Screen reader tested: [VoiceOver/NVDA]
- Color contrast: ✅ [ratios]
- Reduced motion: ✅
- Touch targets: ✅ [44px minimum]

### Files Created

- [Component files]
- [Style files]
- [Accessibility documentation]

### Time Elapsed

[Duration]

_The glade welcomes all wanderers._ 🌲
```

---

## Example Gathering

**User:** "/gathering-ui Create the user profile page"

**Gathering execution:**

1. 🌲 **SUMMON** — "Mobilizing for: User profile page. Personal settings, avatar, bio. Emotional: reflection."

2. 🌲 **ORGANIZE** — "Chameleon designs → Deer audits"

3. 🌲 **EXECUTE** —
   - 🦎 Chameleon: "Autumn theme, glass cards for settings, randomized birch trees, cardinals perched, Lucide icons"
   - 🦌 Deer: "Tab order logical, form labels associated, contrast passes, screen reader announces changes"

4. 🌲 **VALIDATE** — "Visual design matches Grove, all accessibility checks pass"

5. 🌲 **COMPLETE** — "Profile page complete, beautiful and accessible"

---

_Beautiful and accessible—the forest welcomes all._ 🌲
