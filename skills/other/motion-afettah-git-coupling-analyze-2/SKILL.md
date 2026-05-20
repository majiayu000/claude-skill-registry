---
name: motion
description: Animation patterns using Framer Motion.
---

# Motion & Animations

## Import

```tsx
import { motion, AnimatePresence } from 'framer-motion';
```

## Common Patterns

### Fade + Scale (modals, cards)
```tsx
<motion.div
  initial={{ opacity: 0, scale: 0.95 }}
  animate={{ opacity: 1, scale: 1 }}
  exit={{ opacity: 0, scale: 0.95 }}
  transition={{ duration: 0.2 }}
/>
```

### Slide In (panels, drawers)
```tsx
<motion.div
  initial={{ x: -20, opacity: 0 }}
  animate={{ x: 0, opacity: 1 }}
  transition={{ duration: 0.15 }}
/>
```

### List Stagger
```tsx
<motion.ul initial="hidden" animate="visible" variants={{
  visible: { transition: { staggerChildren: 0.05 } }
}}>
  {items.map(item => (
    <motion.li key={item.id} variants={{
      hidden: { opacity: 0, y: 10 },
      visible: { opacity: 1, y: 0 }
    }} />
  ))}
</motion.ul>
```

### Exit Animation (wrap parent)
```tsx
<AnimatePresence mode="wait">
  {isOpen && <motion.div key="modal" exit={{ opacity: 0 }} />}
</AnimatePresence>
```

## Timing Reference

| Use Case | Duration |
|----------|----------|
| Micro (hover, focus) | 100-150ms |
| UI feedback | 200ms |
| Panels/modals | 200-300ms |
| Page transitions | 300-500ms |
