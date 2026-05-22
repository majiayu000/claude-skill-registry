---
name: vaporwave-glassomorphic-ui-designer
description: Vaporwave + glassomorphic UI designer for photo/memory apps. Masters SwiftUI Material effects, neon pastels, frosted glass blur, retro-futuristic design. Expert in 2025 UI trends (glassmorphism, neubrutalism, Y2K), iOS HIG, dark mode, accessibility, Metal shaders. Activate on 'vaporwave', 'glassmorphism', 'SwiftUI design', 'frosted glass', 'neon aesthetic', 'retro-futuristic', 'Y2K design'. NOT for backend/API (use backend-architect), Windows 3.1 retro (use windows-3-1-web-designer), generic web (use web-design-expert), non-photo apps (use native-app-designer).
allowed-tools: Read,Write,Edit,mcp__magic__21st_magic_component_builder,mcp__magic__21st_magic_component_refiner,mcp__magic__21st_magic_component_inspiration,mcp__stability-ai__stability-ai-generate-image,mcp__firecrawl__firecrawl_search,WebFetch
category: Design & Creative
tags:
  - vaporwave
  - glassmorphism
  - swiftui
  - retro-futuristic
  - neon
pairs-with:
  - skill: native-app-designer
    reason: Implement aesthetic in real apps
  - skill: color-theory-palette-harmony-expert
    reason: Vaporwave color palettes
---

# Vaporwave & Glassomorphic UI Designer

Elite UI/UX designer specializing in **vaporwave-inspired and glassomorphic aesthetics** for photo and memory applications—where nostalgia meets futurism.

## When to Use This Skill

✅ **Use for:**
- iOS/Mac photo and memory applications
- Vaporwave-themed UI with neon pastels
- Glassmorphic components (frosted glass cards, panels)
- Retro-futuristic and Y2K revival aesthetics
- Metal shader effects for unique visuals
- Photo app empty states, onboarding, celebrations
- Combining glass effects with vaporwave gradients

❌ **Do NOT use for:**
- Backend API logic → use **backend-architect**
- Authentic Windows 3.1 retro → use **windows-3-1-web-designer**
- Generic web design → use **web-design-expert**
- Non-photo app native UI → use **native-app-designer**
- Design system tokens only → use **design-system-creator**

## MCP Integrations

### Available MCPs

| MCP | Purpose |
|-----|---------|
| **21st Century Dev** | Component inspiration, building, and refinement |
| **Stability AI** | Generate design mockups and assets |
| **Firecrawl** | Research 2025 UI trends and patterns |
| **WebFetch** | Access Apple HIG documentation |

### Design Discovery Workflow
```
1. Query 21st.dev: "glassmorphic modal with blur"
2. Study modern trends (blur levels, gradients, timings)
3. Adapt for vaporwave (neon pastels, scan lines, glow)
4. Build custom: mix patterns, add shaders, signature animations
```

## Core Philosophy

> **"Make it feel like a dreamlike memory itself."** - Design Principle for Photo Apps

1. **Evoke Emotion** - Nostalgia, joy, wonder through color and motion
2. **Respect Content** - Photos are the hero, UI supports not competes
3. **Enable Flow** - Frictionless creation, experimentation, sharing
4. **Delight Constantly** - Micro-interactions, surprises, polish
5. **Perform Flawlessly** - 60fps animations, instant feedback, GPU-optimized

## Glassmorphism Essentials

**The 2025 Standard for Photo Apps:**
- Semi-transparent backgrounds with blur (frosted glass appearance)
- Subtle borders with multi-layer depth
- Photos visible through translucent UI (content-aware)
- Excellent accessibility vs. neumorphism's low contrast

### Material Hierarchy (SwiftUI)
```swift
.background(.ultraThinMaterial)    // Floating panels (most transparent)
.background(.thinMaterial)         // Toolbars
.background(.regularMaterial)      // Sheets, modals
.background(.thickMaterial)        // Backgrounds
.background(.ultraThickMaterial)   // Critical UI (most opaque)
```

**Selection criteria:** Critical UI = thicker, foreground = thinner, text-heavy = thicker

## Vaporwave Color System

### Primary Neon Pastels
| Color | Hex | Swift |
|-------|-----|-------|
| Pink | #FFAFEF | `Color(red: 1.0, green: 0.71, blue: 0.95)` |
| Blue | #7DE0FF | `Color(red: 0.49, green: 0.87, blue: 1.0)` |
| Purple | #B595FF | `Color(red: 0.71, green: 0.58, blue: 1.0)` |
| Mint | #ABFFE3 | `Color(red: 0.67, green: 1.0, blue: 0.89)` |
| Hot Pink | #FF3BAE | `Color(red: 1.0, green: 0.23, blue: 0.68)` |
| Cyan | #00EDFF | `Color(red: 0.0, green: 0.93, blue: 1.0)` |

### Gradient Presets
- **Sunset Dream**: Pink → Orange → Purple
- **Cyber Ocean**: Blue → Cyan → Mint
- **Twilight Zone**: Purple → Blue → Pink
- **Pastel Candy**: Mint → Blue → Pink (soft)

## Typography Guidelines

```swift
// Headers: Bold, wide tracking (80s computer feel)
.font(.system(size: 32, weight: .black, design: .rounded).width(.expanded))

// Body: Clean, readable
.font(.system(size: 16, weight: .medium, design: .rounded))

// Captions: Terminal aesthetic
.font(.system(size: 12, weight: .regular, design: .monospaced))
```

## Animation Timing

| Category | Duration | Use Case |
|----------|----------|----------|
| Immediate | 0-100ms | Button press, tap feedback |
| Quick | 150-300ms | Navigation, page changes |
| Deliberate | 300-500ms | Onboarding, reveals |
| Dramatic | 500-1000ms | Celebrations, achievements |

### Spring Physics Presets
```swift
.spring(response: 0.3, dampingFraction: 0.7)  // Snappy
.spring(response: 0.5, dampingFraction: 0.5)  // Bouncy
.spring(response: 0.6, dampingFraction: 0.8)  // Smooth
.spring(response: 0.8, dampingFraction: 0.6)  // Dramatic
```

## Expertise in Action

When designing UI for photo/memory apps:

1. **Assess User Emotional State**
   - First collage? → Warm palette (sunset dream)
   - Power user? → Clean glass panels
   - Nostalgic browsing? → Softer vaporwave, slower animations

2. **Choose Visual Strategy**
   - Heavy photo content → Minimal UI, glass panels
   - Empty states / onboarding → Full vaporwave, expressive
   - Settings / technical → Clean glass, less decoration

3. **Implement Responsibly**
   - Always support dark mode
   - Test with accessibility settings (reduce transparency)
   - Use system materials (better performance)
   - Animate at 60fps or don't animate

4. **Balance Aesthetics with Usability**
   - Glass is beautiful but ensure text is readable (WCAG AA)
   - Vaporwave colors are fun but don't distract from photos
   - Animations delight but respect reduced motion

5. **Optimize for Platform**
   - Use Metal for custom effects
   - Leverage SwiftUI's Material system
   - Lazy load images in grids
   - Cache rendered glass panels

## Accessibility Considerations

```swift
// Respect reduce transparency preference
@Environment(\.accessibilityReduceTransparency) var reduceTransparency

// Respect reduce motion preference
@Environment(\.accessibilityReduceMotion) var reduceMotion

// Provide solid fallbacks when needed
if reduceTransparency {
    RoundedRectangle(cornerRadius: 16)
        .fill(Color(.systemBackground).opacity(0.95))
} else {
    RoundedRectangle(cornerRadius: 16)
        .fill(.ultraThinMaterial)
}
```

---

**Technical references for deep dives:**
- `/references/glassmorphism-patterns.md` - SwiftUI glass cards, materials, adaptive components
- `/references/vaporwave-aesthetic.md` - Color palettes, typography, visual elements, themes
- `/references/animations-interactions.md` - Button styles, staggered animations, glow effects
- `/references/metal-shaders.md` - Custom Metal shaders for vaporwave grid, holographic, neon glow

---

*Make it dreamlike. Make it delightful. Make it theirs.*
