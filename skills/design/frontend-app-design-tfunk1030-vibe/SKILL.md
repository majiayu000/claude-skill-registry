---
name: frontend-app-design
description: Create distinctive, production-grade React Native Expo interfaces following iOS Human Interface Guidelines and liquid glass design principles. Use when building mobile screens, components, or styling any React Native UI.
---

This skill guides creation of distinctive, production-grade React Native Expo interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a screen, component, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Mobile-first. Design for touch, thumb zones, glanceability, and varying screen sizes.
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working React Native Expo code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## iOS Human Interface Guidelines

- **Clarity**: Text is legible at every size. Icons are precise. Adornments are subtle.
- **Deference**: Content is primary. UI recedes, letting content shine.
- **Depth**: Visual layers and motion convey hierarchy and enable navigation.

## Liquid Glass Design (iOS 26)

Create depth through translucency and layering:
- **Translucent Surfaces**: Use `expo-blur` BlurView for frosted glass effects on overlays, cards, and navigation. Layer content over blurred backgrounds.
- **Depth & Layering**: Stack translucent layers to create visual hierarchy. Background → blurred surface → content.
- **Subtle Shadows**: Soft, diffused shadows rather than hard drops. Use low opacity with larger radius.
- **Refined Borders**: Thin, semi-transparent borders to define glass edges.

## Mobile Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic system fonts; use `@expo-google-fonts` for distinctive choices that elevate the interface. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use Tailwind theme colors for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use `react-native-reanimated` for fluid, 60fps animations. Focus on high-impact moments: screen transitions with staggered reveals, gesture-driven interactions, spring physics on state changes. Add `expo-haptics` feedback on meaningful interactions.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Generous negative space OR controlled density. Design for comfortable touch targets (minimum 44pt) and thumb-reachable primary actions.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Use `expo-linear-gradient` for gradient meshes, layered transparencies, dramatic shadows, and depth. Leverage blur effects for the liquid glass aesthetic.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, system fonts), clichéd color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
