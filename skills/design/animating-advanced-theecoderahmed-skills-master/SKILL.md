---
name: animating-advanced
description: Creates Awwwards-level, high-performance animations using industry-standard tools like GSAP, Three.js/R3F, and Lenis. Specializes in "Hero Sections", 3D interactions, and scroll-linked storytelling.
---

# Cinematic Interaction Designer

## When to use this skill
- When the user asks for "Awwwards specific" or "Google Flow/Whisk" level animations.
- When creating a **Hero Section** that needs to wow the user.
- When implementing **Smooth Scrolling**, **Parallax**, or **3D Objects**.

## Workflow
1.  **Vibe Check**: Is this "Playful Bounce" (Framer Motion) or "Media Art" (GenAI + WebGL)?
2.  **Stack Selection**:
    - **GSAP**: For timelines and scroll triggers.
    - **R3F (Three.js)**: For 3D models and shaders.
    - **Lenis**: For smooth, momentum-based scrolling.
    - **Google Labs (Flow/Whisk)**: For generating the *assets* (textures, video loops) to be animated.
3.  **Performance Check**:
    - Usage of `will-change`.
    - Offloading heavy 3D to generic GPU shaders.
    - Loading states (Preloaders).

## Instructions

### 1. The "Labs.Google" Pipeline (GenAI Assets)
To achieve the specific "Google Labs" aesthetic:
1.  **Asset Gen**: Use **Google Whisk** to generate consistent textures/styles and **Google Flow** to create seamless video loops.
2.  **Implementation**:
    - Use these assets as *textures* on 3D objects in R3F.
    - Or use them as full-screen background video layers with `mix-blend-mode`.
3.  **Interaction**: Use GSAP to distort/scale these assets on scroll.

### 2. Awwwards Recipe
To achieve that specific "premium" feel:
- **Smooth Scroll**: Install `@studio-freight/lenis`.
- **Typography**: Big, massive fonts that move slightly slower than the scroll (Parallax).
- **Images**: Reveal effects (clip-path) upon scrolling into view.

### 3. GSAP Patterns
Always use `useGSAP` hook in React (safe cleanup).
```javascript
useGSAP(() => {
  gsap.from(".hero-text", {
    y: 100,
    opacity: 0,
    stagger: 0.1,
    duration: 1.5,
    ease: "power4.out"
  });
}, { scope: containerRef });
```

### 4. Three.js / WebGL
- Use `drei` for helpers (OrbitControls, Environment).
- **Optimization**: Always compress .glb files using `gltfjsx` + `modifiers`.

## Self-Correction Checklist
- "Is this accessible?" -> Don't animate `width/height` (causes reflow). Animate `transform`.
- "Does it lag on mobile?" -> Disable heavy WebGL on low-end devices.
