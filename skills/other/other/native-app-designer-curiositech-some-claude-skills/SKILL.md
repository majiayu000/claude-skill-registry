---
name: native-app-designer
description: Creates breathtaking iOS/Mac and web apps with organic, non-AI aesthetic. Expert in SwiftUI, React animations, physics-based motion, and human-crafted design. Use for iOS/Mac app UI, React/Vue animations, native-feel web apps, physics-based motion design. Activate on "SwiftUI", "iOS app", "native app", "React animation", "motion design", "UIKit", "physics animation". NOT for backend logic, API design (use backend-architect), simple static sites (use web-design-expert), or pure graphic design (use design-system-creator).
allowed-tools: Read,Write,Edit,Bash,mcp__magic__21st_magic_component_builder,mcp__magic__21st_magic_component_refiner,mcp__stability-ai__stability-ai-generate-image,mcp__firecrawl__firecrawl_search
category: Design & Creative
tags:
  - ios
  - swiftui
  - react
  - animations
  - motion
pairs-with:
  - skill: metal-shader-expert
    reason: GPU-accelerated visual effects
  - skill: vaporwave-glassomorphic-ui-designer
    reason: Aesthetic iOS design
---

# Native App Designer

Elite native app designer specializing in breathtaking, human-centered applications that feel organic and alive—never generic or AI-generated.

## When to Use This Skill

✅ **Use for:**
- iOS/Mac app UI design with SwiftUI or UIKit
- React/Vue/Svelte apps with delightful animations
- Physics-based motion design and micro-interactions
- Native-feel Progressive Web Apps (PWAs)
- App onboarding flows with personality
- Custom shader effects (Metal/WebGL)
- Component library design with character

❌ **Do NOT use for:**
- Backend API logic → use **backend-architect**
- Simple static websites → use **web-design-expert**
- Design system tokens only → use **design-system-creator**
- Graphic design/brand identity → use **design-system-creator**
- Accessibility-first ADHD apps → use **adhd-design-expert**
- Retro/vaporwave aesthetics → use **vaporwave-glassomorphic-ui-designer**

## MCP Integrations

### Available MCPs

| MCP | Purpose |
|-----|---------|
| **21st Century Dev** | Component inspiration and building |
| **Stability AI** | Generate design assets and mockups |
| **Firecrawl** | Research design patterns |
| **Figma MCP** (if configured) | Import designs from Figma |
| **Apple Developer Docs MCP** (community) | Access SwiftUI/UIKit documentation |

### Component Inspiration Workflow
```
1. Search 21st.dev for modern patterns
2. Analyze animation timing, color usage, hierarchy
3. Adapt (don't copy) - add your personality
4. Use mcp__magic__21st_magic_component_builder to scaffold
5. Refine with mcp__magic__21st_magic_component_refiner
```

## Common Anti-Patterns

### Anti-Pattern: Generic Card Syndrome
**What it looks like**: Every component is a white card with shadow
**Why it's wrong**: Creates monotonous, AI-generated aesthetic
**What to do instead**: Mix layouts—cards, lists, grids, overlays, inline elements

### Anti-Pattern: Linear Animation Death
**What it looks like**: `.animation(.linear(duration: 0.3))`
**Why it's wrong**: Feels robotic, lifeless, unnatural
**What to do instead**: Use spring physics with response/damping parameters

### Anti-Pattern: Rainbow Vomit
**What it looks like**: Using every color in the palette everywhere
**Why it's wrong**: No visual hierarchy, overwhelming
**What to do instead**: Restrained palette with purposeful color usage

### Anti-Pattern: Animation Overload
**What it looks like**: Everything bounces, slides, and fades constantly
**Why it's wrong**: Distracting, overwhelming, hides content
**What to do instead**: Animate intentionally—guide attention, provide feedback

### Anti-Pattern: Inconsistent Spacing
**What it looks like**: Random margins (8px, 14px, 23px...)
**Why it's wrong**: Feels unpolished, chaotic
**What to do instead**: 4pt or 8pt grid system with consistent rhythm

## Design Philosophy: Beyond Generic

### What Makes Apps Look "AI-Generated" (AVOID)
- ❌ Perfectly centered everything with no visual rhythm
- ❌ Generic gradients (linear purple-to-blue everywhere)
- ❌ Oversized, ultra-rounded corners on everything
- ❌ Stock illustrations with same flat art style
- ❌ Over-reliance on cards with identical spacing
- ❌ Soulless animations (generic slide-in-from-bottom)

### What Makes Apps Feel Human-Crafted (DO THIS)
- ✅ **Asymmetry with purpose**: Break the grid intentionally
- ✅ **Unexpected details**: Easter eggs, playful copy, personality
- ✅ **Organic motion**: Physics-based animations, spring dynamics
- ✅ **Textural elements**: Subtle noise, gradients with character
- ✅ **Thoughtful hierarchy**: Visual weight that guides naturally
- ✅ **Emotional color**: Palettes that evoke feeling
- ✅ **Contextual adaptation**: UI that responds to content and state

## App Personality Types

Choose a personality and commit to it:

| Personality | Animation | Color | Typography |
|------------|-----------|-------|------------|
| **Playful** | Bouncy springs, overshoots | Warm, saturated | Rounded, friendly |
| **Professional** | Crisp, confident | Sophisticated, muted | Clean, weighted |
| **Minimal** | Subtle, restrained | Limited palette | Perfect spacing |
| **Vibrant** | Energetic, expressive | Bold, unexpected | Dynamic contrast |
| **Natural** | Organic, flowing | Earthy, warm | Soft, approachable |

## Motion Design Principles

### Spring Physics Cheat Sheet
```swift
// Snappy, responsive
.spring(response: 0.3, dampingFraction: 0.7)

// Bouncy, playful
.spring(response: 0.5, dampingFraction: 0.5)

// Smooth, elegant
.spring(response: 0.6, dampingFraction: 0.8)

// Dramatic, slow
.spring(response: 0.8, dampingFraction: 0.6)
```

### Animation Timing
- **Immediate feedback**: 0-100ms (button press)
- **Quick transitions**: 150-300ms (page change)
- **Deliberate animations**: 300-500ms (onboarding)
- **Dramatic moments**: 500-1000ms (celebrations)

## Details That Delight

Small touches that make users smile:
- Pull-to-refresh with personality (not just a spinner)
- Empty states with character and guidance
- Loading states that entertain
- Success states that celebrate
- Error states that empathize
- Haptic feedback on key interactions

## Platform-Specific Best Practices

### iOS Native
- Use system materials (.ultraThinMaterial, .regularMaterial)
- Respect safe areas and Dynamic Island
- Support Dynamic Type (accessibility)
- Implement haptic feedback strategically
- Use SF Symbols with weight matching
- Support dark mode with semantic colors

### Web Native Feel
- 60fps animations using transform/opacity
- CSS containment for performance
- Pull-to-refresh implementation
- PWA install prompt
- Reduced motion support
- Touch-friendly targets (44px minimum)

## Tools & Libraries

### iOS
- **SwiftUI**: Declarative UI framework
- **UIKit**: When SwiftUI isn't enough
- **Lottie**: After Effects animations
- **SF Symbols**: Apple's icon system

### Web
- **Framer Motion**: React animation library
- **GSAP**: JavaScript animation powerhouse
- **react-spring**: Physics-based React animations
- **Lottie Web**: Cross-platform animations

### Design
- **Figma**: Primary design tool
- **Principle**: Advanced prototyping
- **21st.dev**: Component inspiration

---

**Technical references for deep dives:**
- `/references/swiftui-patterns.md` - SwiftUI components, animations, color palettes
- `/references/react-patterns.md` - React/Vue patterns, Framer Motion, responsive design
- `/references/custom-shaders.md` - Metal and WebGL shaders for unique effects

---

**Philosophy**: The difference between good and breathtaking is soul. Every pixel should have purpose. Every animation should feel inevitable. Every interaction should delight.
