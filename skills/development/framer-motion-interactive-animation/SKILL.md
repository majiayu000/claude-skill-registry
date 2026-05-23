---
name: framer-motion-interactive-animation
description: |
  Framer Motion animations: motion components, gestures (hover/tap), entrance/exit, scroll triggers, and performance.
  Keywords: "animate", "animation", "framer motion", "hover", "scroll", "whileHover", "AnimatePresence"
---

# Framer Motion Interactive Animation

## motion Component

Convert any element to animatable:

\`\`\`tsx
'use client';

import { motion } from 'framer-motion';

<motion.div
  animate={{ x: 100 }}
  transition={{ duration: 0.5 }}
/>
\`\`\`

## Gesture Animations

### Hover/Tap Effects

\`\`\`tsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ duration: 0.2 }}
>
  Click Me
</motion.button>
\`\`\`

## Entrance Animations

\`\`\`tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Fades in and slides up
</motion.div>
\`\`\`

## Exit Animations

**CRITICAL**: Must wrap in \`<AnimatePresence>\`

\`\`\`tsx
import { motion, AnimatePresence } from 'framer-motion';

<AnimatePresence>
  {isVisible && (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      Content with exit animation
    </motion.div>
  )}
</AnimatePresence>
\`\`\`

## Scroll-Triggered Animations

\`\`\`tsx
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}  // Only animate once
  transition={{ duration: 0.6 }}
>
  Appears when scrolled into view
</motion.div>
\`\`\`

## Transition Options

\`\`\`tsx
// Spring (physics-based)
transition={{ type: "spring", stiffness: 300, damping: 30 }}

// Tween (duration-based)
transition={{ duration: 0.3, ease: "easeInOut" }}
\`\`\`

## Performance Best Practices

✅ **Animate**: \`transform\` (x, y, scale, rotate), \`opacity\`
❌ **Don't animate**: width, height, margin, padding (causes reflow)

✅ Use \`viewport={{ once: true }}\` for scroll animations
❌ Forget \`<AnimatePresence>\` for exit animations

---

**Token Estimate**: ~2,200 tokens
