---
name: enhance-design
description: Comprehensive design enhancement that chains all design skills in phases - analyze, mobile optimize, conversion optimize, and polish. Transforms any interface into a professional, high-converting, mobile-friendly experience.
hooks:
  SubagentStart:
    - matcher: ".*"
      hooks:
        - type: command
          command: |
            case "$AGENT_TYPE" in
              "conversion-audit") echo "📊 Auditing conversion opportunities..." ;;
              "mobile-patterns") echo "📱 Applying mobile navigation patterns..." ;;
              "touch-interactions") echo "👆 Implementing touch interactions..." ;;
              "mobile-accessibility") echo "♿ Adding accessibility support..." ;;
              "copywriting-guide") echo "✍️  Optimizing copy and messaging..." ;;
              "cta-optimizer") echo "🎯 Enhancing CTAs..." ;;
              "social-proof") echo "⭐ Adding social proof elements..." ;;
              "color-palette") echo "🎨 Refining color palette..." ;;
              "typography-system") echo "📝 Establishing typography system..." ;;
              "spacing-system") echo "📏 Creating spacing rhythm..." ;;
              "component-states") echo "🔄 Adding interactive states..." ;;
              "micro-interactions") echo "✨ Implementing micro-interactions..." ;;
              "component-polish") echo "💎 Final polish pass..." ;;
              *) echo "🔧 Running $AGENT_TYPE..." ;;
            esac
  SubagentStop:
    - hooks:
        - type: command
          command: "echo '   ✓ Complete'"
  Stop:
    - hooks:
        - type: agent
          prompt: |
            Verify that /enhance-design completed all required phases.

            Check the conversation transcript for evidence that these phases ran:

            Phase 1 - ANALYZE:
            - [ ] /conversion-audit was invoked

            Phase 2 - MOBILE OPTIMIZE (should run in parallel):
            - [ ] /mobile-patterns was invoked
            - [ ] /touch-interactions was invoked
            - [ ] /mobile-accessibility was invoked

            Phase 3 - CONVERSION OPTIMIZE (should run in parallel):
            - [ ] /copywriting-guide was invoked
            - [ ] /cta-optimizer was invoked
            - [ ] /social-proof was invoked

            Phase 4 - VISUAL POLISH (should run in batches):
            - [ ] /color-palette was invoked
            - [ ] /typography-system was invoked
            - [ ] /spacing-system was invoked
            - [ ] /component-states was invoked
            - [ ] /micro-interactions was invoked
            - [ ] /component-polish was invoked

            Context: $ARGUMENTS

            Return {"ok": true} if ALL phases completed successfully.
            Return {"ok": false, "reason": "Missing: [list skills that didn't run]"} if any skills were skipped.
          timeout: 120
---

# Enhance Design Skill

## Instructions

**IMPORTANT: Execute immediately. Do NOT explore the codebase first or propose a plan. Start Phase 1 right now.**

Default mode is **Full Enhancement** (all 4 phases). If the user passed an argument, select the matching mode:
- `quick` → Phase 1 + Phase 4 only
- `mobile` → Phase 1 + Phase 2 only
- `conversion` → Phase 1 + Phase 3 only
- No argument or `all` → Full Enhancement (Phase 1 → 2 → 3 → 4)

---

### Phase 1: Analyze & Audit

1. **Quick project scan** (30 seconds max): Use Glob to find page files and Read the main layout to understand project structure. Do NOT launch an Explore agent - just do a quick Glob + Read.

2. **Invoke `/conversion-audit`** immediately using the Skill tool. This skill will assess:
   - Page structure and information hierarchy
   - Copy effectiveness and messaging
   - Trust signals and social proof
   - Friction points and obstacles
   - Mobile conversion readiness

3. **Present audit results** to the user as a prioritized list:

```markdown
## Design Audit Results

### Critical Issues (Fix First)
1. [Issue] - [Impact] - [Recommended fix]

### High Priority
2. [Issue] - [Impact] - [Recommended fix]

### Medium Priority
...

### Strengths (Don't Change)
- [What's working well]
```

4. **Ask the user** to confirm before proceeding to the next phase.

---

### Phase 2: Mobile Optimization

**Invoke all three skills in parallel** using the Skill tool in a single message:
- `/mobile-patterns` - Navigation patterns (bottom nav, drawer, tabs), responsive grid, component adaptations (tables → lists, modals → sheets), safe area handling
- `/touch-interactions` - Touch targets ≥ 48x48px, swipe gestures, touch feedback (scale, ripple), pull-to-refresh
- `/mobile-accessibility` - Screen reader labels (VoiceOver/TalkBack), focus management, live regions, reduced motion support

**Wait for all three to complete.**

**VERIFY**: After all three skills complete, run `git diff --stat` to check if files were actually modified. If NO files changed (agents completed without writing), the sub-skills' tool calls were likely blocked by permissions. In that case:
1. Review the analysis/recommendations returned by each sub-skill
2. Implement the changes yourself directly using Edit/Write tools
3. Apply mobile patterns, touch interaction fixes, and accessibility improvements based on the sub-skills' guidance

Verify these outputs before proceeding to Phase 3:
- [ ] Bottom-heavy layout (thumb zone friendly)
- [ ] All touch targets ≥ 48px
- [ ] Platform-appropriate patterns
- [ ] Safe area handling
- [ ] Screen reader support

---

### Phase 3: Conversion Optimization

**Invoke all three skills in parallel** using the Skill tool in a single message:
- `/copywriting-guide` - Rewrite headlines using PAS/AIDA/BAB frameworks, transform features into benefits, optimize microcopy, apply power words
- `/cta-optimizer` - CTA copy (action verb + value + friction reducer), visual design (contrast, size, spacing), placement strategy, primary/secondary/tertiary hierarchy
- `/social-proof` - Testimonials (photos, names, results), logo trust bar, stats/usage numbers, trust signals near CTAs and forms

**Wait for all three to complete.**

**VERIFY**: Run `git diff --stat` to check if files were actually modified. If NO files changed, implement the changes yourself directly based on the sub-skills' recommendations.

Verify these outputs before proceeding to Phase 4:
- [ ] Benefit-driven headlines
- [ ] Prominent, action-oriented CTAs
- [ ] Strategic social proof placement
- [ ] Trust signals near decision points
- [ ] No dark patterns

---

### Phase 4: Visual Polish (3 Batches)

**Batch 1 - Invoke all three in parallel** using the Skill tool in a single message:
- `/color-palette` - Replace generic colors with sophisticated palette, create color scales (50-900), ensure WCAG contrast ratios, define semantic usage
- `/typography-system` - Type scale with clear hierarchy, font pairing, weight/line-height definitions, responsive sizing
- `/spacing-system` - Intentional spacing rhythm, content-relationship-based spacing, break mechanical uniformity, consistent scale

**Wait for Batch 1 to complete.**

**VERIFY**: Run `git diff --stat`. If no files changed, implement the design system changes yourself directly.

**Batch 2 - Invoke both in parallel** using the Skill tool in a single message:
- `/component-states` - Complete interactive states (hover, focus, active, disabled, loading), smooth transitions, keyboard focus indicators, error/success states
- `/micro-interactions` - Subtle hover effects, entrance animations, meaningful loading states, polished state transitions

**Wait for Batch 2 to complete.**

**VERIFY**: Run `git diff --stat`. If no files changed, implement states and interactions yourself directly.

**Batch 3 - Invoke sequentially:**
- `/component-polish` - Final detail pass, perfect alignment and spacing, subtle shadows and depth, pixel-perfect implementation

**VERIFY**: Run `git diff --stat`. If no files changed, implement the polish yourself directly.

Verify these outputs:
- [ ] Sophisticated color palette
- [ ] Clear typography hierarchy
- [ ] Intentional spacing rhythm
- [ ] Complete interactive states
- [ ] Delightful micro-interactions
- [ ] Production-ready quality

---

### Final Report

After all phases complete, present a summary:

```markdown
# Design Enhancement Report

## Summary
- **Mode**: [Full/Quick/Mobile/Conversion]
- **Components Enhanced**: [number]
- **Issues Fixed**: [number]

## Phase 1: Audit Results
[Summary of findings]

## Phase 2: Mobile Optimization
[Summary: navigation changes, touch target fixes, accessibility additions]

## Phase 3: Conversion Optimization
[Summary: copy changes, CTA updates, social proof added]

## Phase 4: Visual Polish
[Summary: color palette, typography, spacing, states, interactions]

## Files Modified
- `[filepath]` - [Changes made]

## Verification Checklist
- [x] All touch targets ≥ 48px
- [x] Color contrast ≥ 4.5:1
- [x] Screen reader tested
- [x] CTA copy is action-oriented
- [x] Social proof placed strategically
- [x] No dark patterns present
- [x] Component states complete
- [x] Micro-interactions added
```

---

## Skill Chain Reference

| Phase | Skill | Purpose |
|-------|-------|---------|
| 1 | `/conversion-audit` | Identify all design issues |
| 2a | `/mobile-patterns` | Mobile navigation and layout |
| 2b | `/touch-interactions` | Touch targets and gestures |
| 2c | `/mobile-accessibility` | Screen reader support |
| 3a | `/copywriting-guide` | Headlines and copy |
| 3b | `/cta-optimizer` | CTA design and placement |
| 3c | `/social-proof` | Testimonials and trust |
| 4a | `/color-palette` | Professional colors |
| 4b | `/typography-system` | Type hierarchy |
| 4c | `/spacing-system` | Visual rhythm |
| 4d | `/component-states` | Interactive states |
| 4e | `/micro-interactions` | Animations |
| 4f | `/component-polish` | Final details |

## Integration with Agents

This skill works well when invoked by:
- **ui-ux-designer** - For complete design transformations
- **mobile-designer** - When mobile-first approach is needed
- **conversion-optimizer** - When revenue optimization is primary goal

## Notes

- Each phase can be run independently if needed
- User approval checkpoint after Phase 1 (audit) is recommended
- For very large projects, consider running one phase per session
- Individual skills can be re-run if specific improvements needed
- All changes follow ethical design principles (no dark patterns)
- Accessibility is baked into every phase, not an afterthought