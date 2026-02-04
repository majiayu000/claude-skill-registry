---
name: elegant-design
description: Create world-class, accessible, responsive interfaces with sophisticated interactive elements including chat, terminals, code display, and streaming content. Use when building user interfaces that need professional polish and developer-focused features.
---

# Designing Elegant Interfaces

## Philosophy

World-class design is intentional, accessible, and delightful. Every element serves a purpose, every interaction feels natural, and the experience adapts gracefully across contexts.

**Core Principles:**
- **Clarity over cleverness** - Users should never wonder what to do next
- **Consistency over novelty** - Patterns should repeat predictably
- **Performance over features** - Fast, smooth interactions trump visual complexity
- **Accessibility always** - Design for all users from the start
- **Progressive disclosure** - Reveal complexity only when needed
- **Intentional friction** - Make destructive actions harder, constructive actions effortless

## When to Use This Skill

Use this skill when:
- Building web applications with React/Next.js/similar frameworks
- Creating developer tools or technical interfaces
- Designing interfaces with chat, terminals, or code display
- Implementing real-time or streaming features
- Ensuring accessibility and responsive design
- Working with shadcn/ui, daisyUI, or HeroUI design systems

## Design Process Workflow

Follow this workflow for optimal results:

### 1. Discovery & Planning (15-30 min)

**Map User Experience:**
```bash
# Create flow diagrams with Graphviz
cat > user-flow.dot << 'EOF'
digraph UserFlow {
  Start -> "Observe State"
  "Observe State" -> "Orient Understanding"
  "Orient Understanding" -> "Decide Action"
  "Decide Action" -> "Act Execute"
  "Act Execute" -> "Observe State" [label="OODA loop"]
}
EOF

dot -Tpng user-flow.dot -o user-flow.png
```

**OODA Loop Mapping:**
For each major user goal, optimize the cycle:
1. **Observe** - What information does the user need?
2. **Orient** - How do they make sense of it?
3. **Decide** - What choices are available?
4. **Act** - How do they execute?

**Document States:**
- Entry points (how users arrive)
- Core loops (repeated actions)
- Success states (goals achieved)
- Failure states (errors, recovery paths)
- Edge cases (empty, loading, error, extreme data)

**List Affordances:**
Identify every UI element needed:
- Navigation (movement between sections)
- Actions (buttons, links, controls)
- Inputs (forms, editors, pickers)
- Feedback (success, error, loading)
- Content (text, images, data)
- Wayfinding (breadcrumbs, progress)

**Before Building Custom Components:**
1. Search shadcn/ui first (https://ui.shadcn.com)
2. Check daisyUI (https://daisyui.com)
3. Explore HeroUI (https://heroui.com)
4. Build custom only when necessary

### 2. Design Foundation (20-40 min)

**Establish Visual System:**

Read the detailed foundation guides:
- `foundation/typography.md` - Font selection (Geist, JetBrains Mono), scales, loading
- `foundation/colors-and-spacing.md` - Color palettes, spacing systems, dark mode
- `foundation/layout-patterns.md` - Grids, containers, white space, responsive breakpoints

**Quick Reference:**
- **Typography**: Geist for UI, JetBrains Mono for code (14px minimum)
- **Spacing**: 8px base system (0.5rem, 1rem, 1.5rem, 2rem, 3rem, 4rem, 6rem, 8rem)
- **Colors**: Semantic tokens (--color-background, --color-primary, --color-error, etc.)
- **Layout**: Mobile-first, 12-column grid, generous white space

### 3. Interactive Elements (30-60 min)

For sophisticated interactive features, reference the specialized guides:

**Chat & Messaging:**
- Read `interactive/chat-and-messaging.md` when building conversational interfaces
- Covers message states, streaming, auto-scrolling, markdown rendering

**Terminals & Code Display:**
- Read `interactive/terminals-and-code.md` for terminal emulators, syntax highlighting, semantic highlighting
- Covers ANSI colors, Shiki integration, copy buttons, line highlighting

**Streaming & Loading:**
- Read `interactive/streaming-and-loading.md` for progressive loading, streaming text, optimistic updates
- Covers skeleton screens, progress indicators, loading hierarchies

**Diffs & Logs:**
- Read `interactive/diffs-and-logs.md` for version control UIs, log viewers
- Covers split/unified diffs, character-level changes, virtual scrolling

### 4. Implementation (1-3 hours)

**Build Components:**
- Read `implementation/components-and-accessibility.md` for component architecture and WCAG compliance
- Use atomic design: atoms → molecules → organisms → templates → pages
- Ensure keyboard navigation and screen reader support

**Optimize Performance:**
- Read `implementation/performance.md` for Core Web Vitals optimization
- Lazy load, code split, optimize images, measure with Lighthouse

**Test & Refine:**
- Read `implementation/testing-and-qa.md` for comprehensive testing approach
- Test on multiple devices, screen sizes, and with accessibility tools

### 5. Validation & Refinement

**Pre-Launch Checklist:**
- [ ] User flows tested and OODA loops optimized
- [ ] All states handled (empty, loading, error, success)
- [ ] Mobile responsive (tested on real devices)
- [ ] Accessibility compliant (WCAG AA)
- [ ] Performance measured (Lighthouse score > 90)
- [ ] Geist used for UI, JetBrains Mono for code
- [ ] Design system components used where possible
- [ ] Consistent spacing and typography
- [ ] Both light and dark modes work
- [ ] Keyboard navigation complete
- [ ] Interactive elements polished (see interactive guides)

## Quick Decision Tree

**Need to understand the basics?**
→ Read `foundation/` files first

**Building chat or messaging?**
→ Read `interactive/chat-and-messaging.md`

**Building terminal or code editor?**
→ Read `interactive/terminals-and-code.md`

**Need streaming or loading states?**
→ Read `interactive/streaming-and-loading.md`

**Building diffs or log viewers?**
→ Read `interactive/diffs-and-logs.md`

**Ready to implement?**
→ Read `implementation/` files

**Need tools or want to avoid mistakes?**
→ Read `reference/` files

## Design Systems Priority

1. **shadcn/ui** (https://ui.shadcn.com) - PRIMARY CHOICE
   - Excellent accessibility defaults
   - Radix UI primitives
   - Tailwind-based, customizable
   - Copy-paste into project

2. **daisyUI** (https://daisyui.com)
   - Semantic component names
   - Tailwind plugin
   - Rapid prototyping

3. **HeroUI** (https://heroui.com)
   - Modern, polished
   - Strong design language
   - Product interfaces

See `reference/design-systems.md` for detailed comparison and usage patterns.

## Typography Standards

**Use these fonts exclusively:**

- **Geist** (https://vercel.com/font) - For ALL interface text
  - UI labels, body text, headings
  - 95% of your typography
  
- **JetBrains Mono** (https://jetbrains.com/mono) - For ALL code/technical content
  - Code blocks, terminals, logs, diffs
  - 14px minimum size
  - Enable ligatures

Never mix multiple sans-serif or multiple monospace fonts.

See `foundation/typography.md` for complete guidance.

## Inspiration Sites

Study these for design patterns:
- **Vercel** (https://vercel.com) - Generous white space, clear typography
- **Hex** (https://hex.tech) - Data-dense but organized
- **Baseten** (https://docs.baseten.co) - Clear documentation structure
- **Weather Underground** (https://wunderground.com) - Complex data, clean presentation
- **Ghostty** (https://ghostty.org) - Modern terminal, elegant design

## Common Anti-Patterns

**Avoid these mistakes:**
- ❌ Building custom components when design system has them
- ❌ Using absolute positioning for layout
- ❌ Animating expensive properties (width, height)
- ❌ Skipping mobile testing
- ❌ Ignoring accessibility
- ❌ Using `<div>` for everything
- ❌ Mixing multiple monospace fonts
- ❌ Auto-scrolling when user is reading
- ❌ Showing raw ANSI codes in terminals
- ❌ Forgetting empty/loading/error states

See `reference/anti-patterns.md` for complete list with explanations.

## Iterative Development

**For simple interfaces (single page, few components):**
1. Start with foundation (read foundation files)
2. Use design system components
3. Test and refine

**For complex interfaces (multiple features, interactive elements):**
1. Map flows and create diagrams
2. Establish foundation (read foundation files)
3. Build one feature at a time (read relevant interactive files)
4. Test each feature before moving to next
5. Optimize and polish (read implementation files)

**For developer tools or technical interfaces:**
1. Map OODA loops carefully
2. Read ALL interactive files (chat, terminals, code, streaming, diffs, logs)
3. Focus on keyboard navigation and performance
4. Test with actual technical content

## Getting Help

**If unsure where to start:**
1. Read the philosophy section above
2. Follow the Design Process Workflow
3. Reference specific guides as needed

**If design feels off:**
1. Check against principles (clarity, consistency, performance)
2. Review anti-patterns list
3. Study inspiration sites
4. Test with real users

**If implementation is slow:**
1. Use design system components first
2. Don't build what exists
3. Focus on one feature at a time
4. Test early and often

## File Organization

```
elegant-design/
├── SKILL.md (you are here)
├── foundation/
│   ├── typography.md (fonts, scales, loading)
│   ├── colors-and-spacing.md (palettes, spacing system, dark mode)
│   └── layout-patterns.md (grids, containers, responsive)
├── interactive/
│   ├── chat-and-messaging.md (chat UIs, streaming messages)
│   ├── terminals-and-code.md (terminals, syntax highlighting)
│   ├── streaming-and-loading.md (progressive loading, skeletons)
│   └── diffs-and-logs.md (version control UI, log viewers)
├── implementation/
│   ├── components-and-accessibility.md (architecture, WCAG)
│   ├── performance.md (Core Web Vitals, optimization)
│   └── testing-and-qa.md (testing checklist, tools)
└── reference/
    ├── design-systems.md (shadcn, daisyUI, HeroUI details)
    ├── tools-and-libraries.md (complete tool list)
    └── anti-patterns.md (what not to do, with explanations)
```

## Remember

**World-class design is invisible.** Users shouldn't notice your clever solutions - they should simply accomplish their goals effortlessly and maybe smile along the way.

**Start simple, iterate based on real use.** Don't build everything at once. Build what's needed, test it, refine it, then move to the next feature.

**Accessibility is not optional.** Design for keyboard navigation, screen readers, and sufficient contrast from the start. Retrofitting is much harder.

**Performance matters.** A beautiful interface that's slow is a bad interface. Measure performance early and often.
