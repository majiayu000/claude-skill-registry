---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: MIT
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## Common Design Issues

### Typography Problems
**Issue**: Generic font choices (Inter, Arial, Roboto)
**Solution**: Use distinctive font pairings from Google Fonts or custom fonts. Examples: display fonts (Playfair Display, Bebas Neue, Archivo Black) paired with refined body fonts (Source Serif, Crimson Text, Work Sans).

**Issue**: Poor hierarchy and readability
**Solution**: Establish clear type scale with CSS variables. Use size, weight, and spacing to create visual hierarchy.

### Color & Theme Issues
**Issue**: Clichéd color schemes (purple gradients on white)
**Solution**: Commit to bold, contextual color choices. Use CSS variables for consistency. Consider: monochromatic with one accent, high-contrast brutalism, muted earth tones, vibrant complementary pairs.

**Issue**: Low contrast affecting accessibility
**Solution**: Verify color contrast ratios meet WCAG AA (4.5:1 for text, 3:1 for large text). Use tools like WebAIM Contrast Checker.

### Layout Issues
**Issue**: Predictable, cookie-cutter layouts
**Solution**: Experiment with asymmetry, overlapping elements, diagonal flow, grid-breaking components. Use CSS Grid and Flexbox creatively.

**Issue**: Responsive breakpoints failing
**Solution**: Test at 320px, 768px, 1024px, 1440px. Use fluid typography (clamp()) and container queries.

### Animation Issues
**Issue**: Excessive or jarring animations
**Solution**: Use subtle, purposeful animations. Respect `prefers-reduced-motion`. Focus on one well-orchestrated page load rather than scattered micro-interactions.

**Issue**: Performance problems from animations
**Solution**: Prefer CSS animations over JavaScript. Use `transform` and `opacity` (GPU-accelerated). Avoid animating `width`, `height`, `top`, `left`.

### Accessibility Violations
**Issue**: Missing keyboard navigation
**Solution**: Ensure all interactive elements are keyboard accessible. Add visible focus states.

**Issue**: Poor semantic HTML
**Solution**: Use semantic tags (`<nav>`, `<main>`, `<article>`, `<section>`). Add ARIA labels where needed.

**Issue**: Missing alt text on images
**Solution**: Add descriptive alt text for images. Use empty alt (`alt=""`) for decorative images.

## Design Validation Checklist

After creating a design, verify:

### Visual Quality
- [ ] Color contrast meets WCAG AA standards (4.5:1 for text)
- [ ] Typography is distinctive and readable
- [ ] Visual hierarchy is clear (headings, body, accents)
- [ ] Design has a clear aesthetic direction (not generic)
- [ ] Spacing and alignment are consistent
- [ ] No overused AI patterns (purple gradients, Inter font, etc.)

### Responsive Design
- [ ] Tested at mobile breakpoint (320px-480px)
- [ ] Tested at tablet breakpoint (768px-1024px)
- [ ] Tested at desktop breakpoint (1440px+)
- [ ] Text remains readable at all sizes
- [ ] Images and media scale appropriately
- [ ] No horizontal scrolling on small screens

### Accessibility
- [ ] All interactive elements keyboard accessible
- [ ] Focus states visible and clear
- [ ] Semantic HTML used throughout
- [ ] Alt text present for images
- [ ] Color is not the only indicator (for colorblind users)
- [ ] Animations respect `prefers-reduced-motion`

### Performance
- [ ] Animations use GPU-accelerated properties (`transform`, `opacity`)
- [ ] No layout thrashing from animations
- [ ] Images optimized (WebP, proper dimensions)
- [ ] Fonts loaded efficiently (font-display: swap)
- [ ] Critical CSS inlined for faster first paint

### Code Quality
- [ ] CSS variables used for theming consistency
- [ ] Clean, semantic class names
- [ ] No hardcoded magic numbers
- [ ] Comments explain complex decisions
- [ ] Works without JavaScript (progressive enhancement)

### Browser Compatibility
- [ ] Tested in Chrome/Edge (Chromium)
- [ ] Tested in Firefox
- [ ] Tested in Safari (WebKit)
- [ ] Fallbacks for modern CSS features (Grid, clamp, etc.)

## Testing Your Design

### Visual Testing
```bash
# Test responsive breakpoints
# Open browser DevTools → Toggle device toolbar
# Test at: 320px, 768px, 1024px, 1440px, 1920px
```

### Accessibility Testing
```bash
# Check color contrast
# Use WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/

# Test keyboard navigation
# Tab through all interactive elements
# Verify visible focus states
# Test with screen reader (VoiceOver on Mac, NVDA on Windows)
```

### Performance Testing
```bash
# Open browser DevTools → Performance tab
# Record page load and interactions
# Look for layout shifts (CLS)
# Verify animations run at 60fps
# Check for memory leaks with long animations
```

### Cross-Browser Testing
- Chrome/Edge: Primary testing
- Firefox: Verify CSS Grid/Flexbox behavior
- Safari: Test WebKit-specific issues
- Mobile browsers: Test touch interactions and viewport
