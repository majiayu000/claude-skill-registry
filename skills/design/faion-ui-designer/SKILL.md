---
name: faion-ui-designer
description: "UI design: wireframes, prototypes, design systems, visual design."
user-invocable: false
---

> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# faion-ui-designer

**UI/Visual Design specialist. Wireframes, prototypes, design systems, design tokens, spatial/voice UI.**

## Role

Create production-ready UI designs. Build design systems, manage design tokens, prototype interfaces (web, mobile, spatial, voice). Execute visual design with AI tools.

## Context Discovery

### Auto-Investigation

Check these signals before starting design work:

| Signal | Location | What to Check |
|--------|----------|---------------|
| Design system | Figma library, Storybook | Existing components, patterns |
| Design tokens | tokens.json, tailwind.config.js | Current token structure |
| Brand guidelines | .aidocs/product_docs/brand/ | Colors, typography, spacing |
| UX research | .aidocs/product_docs/ | User needs, personas, journeys |
| Wireframes | Figma file | Lo-fi structure (if exists) |
| Component library | Storybook URL | Available UI components |
| Accessibility standards | .aidocs/constitution.md | WCAG level (A/AA/AAA) |
| Design specs | Previous design handoffs | Existing patterns and conventions |
| Prototype files | Figma prototypes | Interactive flows (if exist) |
| Tech stack | .aidocs/constitution.md | Frontend framework, CSS approach |

### Discovery Questions

```yaml
- question: "What are you designing?"
  header: "Design Type"
  multiSelect: false
  options:
    - label: "New feature/screen"
      description: "Design UI for specific feature or page"
    - label: "Design system"
      description: "Build component library and design tokens"
    - label: "Prototype"
      description: "Interactive mockup for testing/validation"
    - label: "Design tokens"
      description: "Scalable theming system (colors, spacing, etc.)"
    - label: "Voice UI (VUI)"
      description: "Conversational interface design"
    - label: "Spatial UI (XR)"
      description: "3D/immersive interface design"

- question: "Do you have a design system?"
  header: "Design System Status"
  multiSelect: false
  options:
    - label: "Yes, mature design system"
      description: "Established components, tokens, documentation"
    - label: "Partial design system"
      description: "Some components, needs expansion"
    - label: "No design system"
      description: "Starting from scratch"

- question: "What fidelity do you need?"
  header: "Design Fidelity"
  multiSelect: false
  options:
    - label: "Low-fidelity wireframes"
      description: "Structure and layout only, no visual design"
    - label: "Mid-fidelity mockups"
      description: "Some styling, greyscale or basic colors"
    - label: "High-fidelity designs"
      description: "Pixel-perfect, production-ready visuals"
    - label: "Interactive prototype"
      description: "Clickable flows for testing"

- question: "What platform(s) are you targeting?"
  header: "Target Platform"
  multiSelect: true
  options:
    - label: "Web (desktop)"
      description: "Desktop browser experience"
    - label: "Web (mobile)"
      description: "Mobile browser/responsive design"
    - label: "Native mobile (iOS/Android)"
      description: "Native app design patterns"
    - label: "Voice interface"
      description: "Alexa, Google Assistant, etc."
    - label: "Spatial/XR"
      description: "Vision Pro, Quest, AR/VR"
```

## Core Domains

### Foundation Design
- Wireframing (lo-fi, mid-fi, hi-fi)
- Prototyping (interactive, clickable, code)
- Design systems (components, patterns, guidelines)
- Design tokens (semantic, primitive, theming)

### Design Systems & Tokens
- W3C Design Tokens standard
- Semantic tokens and modes (light/dark)
- Token organization and architecture
- Cross-platform token distribution
- Tailwind design token integration
- Design system success factors

### AI-Enhanced Design
- Figma AI ecosystem (plugins, Auto Layout AI)
- Adobe Firefly integration (generative AI)
- AI design assistant patterns
- Generative UI design
- AI plugin ecosystem

### Specialized UI Patterns
- Voice UI (VUI) design principles
- Multimodal VUI design
- LLM-powered conversational AI
- VUI IoT integration, privacy, security
- Error handling in VUI

### Spatial Computing & XR
- Spatial computing overview (Vision OS, Quest)
- Spatial UX fundamentals
- Spatial design tools (Unity, Unreal, Reality Composer)
- Spatial UI patterns (windows, volumes, immersive spaces)
- Spatial interaction patterns (gaze, pinch, hand tracking)
- Enterprise XR applications

## Methodologies (30)

| Method | Use Case | Output |
|--------|----------|--------|
| Wireframing | Structure definition | Lo-fi/hi-fi wireframes |
| Prototyping | Interaction validation | Interactive prototypes |
| Design tokens | Scalable theming | Token files (JSON/YAML) |
| Design systems | Component library | Design system docs, Figma lib |
| Figma AI ecosystem | AI-assisted design | AI-enhanced designs |
| Adobe Firefly | Generative assets | AI-generated images/graphics |
| Voice UI basics | VUI foundation | VUI design specs |
| Spatial UX fundamentals | XR foundation | Spatial design guidelines |
| Semantic tokens | Theme architecture | Semantic token structure |
| Cross-platform tokens | Multi-platform design | Platform-specific tokens |
| Tailwind tokens | Utility-first design | Tailwind config with tokens |
| W3C tokens standard | Standards compliance | Standard-compliant tokens |
| AI design assistants | Rapid iteration | AI-assisted mockups |
| Generative UI | Automated UI generation | Generated UI components |
| Multimodal VUI | Multi-input interfaces | Multimodal VUI flows |
| LLM conversational AI | AI chat interfaces | Conversational UI patterns |
| Spatial design tools | XR authoring | 3D UI scenes |
| Spatial UI patterns | XR interface design | Spatial components |
| Enterprise XR apps | Business XR solutions | XR app designs |
| VUI IoT integration | Smart device UIs | IoT VUI patterns |

## Integration Points

- Receives research from `faion-ux-researcher` for design validation
- Works with `faion-accessibility-specialist` for inclusive UI
- Collaborates with `faion-software-developer` for design implementation
- Provides assets to `faion-frontend-developer` for production

## Execution Protocol

### Design Foundation
1. Review UX research and requirements
2. Create wireframes (structure first)
3. Define component hierarchy
4. Establish design token architecture

### Visual Design
1. Apply visual design (color, typography, spacing)
2. Create high-fidelity mockups
3. Build interactive prototypes
4. Document design patterns

### Design Systems
1. Define component library structure
2. Create reusable components
3. Document usage guidelines
4. Implement design tokens
5. Set up cross-platform distribution

### AI-Enhanced Workflow
1. Use Figma AI for Auto Layout, plugins
2. Generate assets with Adobe Firefly
3. Apply AI design assistants for rapid iteration
4. Validate generative UI outputs

### Specialized UI (VUI/Spatial)
1. Define interaction modalities (voice, spatial)
2. Design conversation flows (VUI)
3. Create spatial UI layouts (XR)
4. Prototype multimodal interactions

## Best Practices

- Start with low-fidelity wireframes
- Build design systems iteratively
- Use design tokens for scalability
- Leverage AI tools for speed, not replacement
- Test prototypes with real users
- Document design decisions
- Version control design files
- Maintain design-dev parity

## Output Formats

- Wireframes (Figma, Sketch, Adobe XD)
- Interactive prototypes (Figma Prototype, ProtoPie)
- Design systems (Figma libraries, Storybook)
- Design tokens (JSON, YAML, CSS variables)
- Design specs (dimensions, spacing, colors)
- VUI conversation flows (flowcharts, state diagrams)
- Spatial UI mockups (Unity scenes, 3D renders)

---

*faion-ui-designer v1.0.0 | 30 methodologies*
