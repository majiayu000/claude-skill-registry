---
name: modal-patterns
description: React Portal modal implementation patterns for Dr. Sophia AI. Covers createPortal usage, AnimatePresence integration, z-index hierarchy (header always visible), dark mode styling, backdrop opacity. Use when creating modals, fixing header overlap issues, implementing React Portal components, or debugging modal stacking problems.
---

# React Modal Implementation Patterns

## Overview

Complete guide for implementing modals using React Portal to prevent stacking context violations and ensure proper z-index hierarchy. This skill provides the correct pattern to keep headers always visible above modals.

**Keywords**: React Portal, createPortal, modal, AnimatePresence, framer-motion, z-index, stacking context, dark mode, backdrop

## When to Use This Skill

- Creating new modal dialogs
- Fixing header blackout issues
- Implementing React Portal components
- Debugging modal stacking problems
- Adding animations to modals
- Ensuring dark mode compatibility

## Critical Rule

🚨 **ALWAYS use React Portal for modals** to render at `document.body` level!

**Problem**: Modals inside parent components violate stacking context
**Solution**: Use `createPortal` to escape parent's stacking context

## Correct Modal Pattern

```jsx
import { createPortal } from 'react-dom';
import { AnimatePresence, motion } from 'framer-motion';

const ModalComponent = () => {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      {/* Button stays in parent */}
      <button onClick={() => setShowModal(true)}>
        Open Modal
      </button>

      {/* Modal renders at document.body */}
      {showModal && createPortal(
        <AnimatePresence>
          <motion.div
            key="modal-unique-key"  // Required for AnimatePresence tracking
            className="fixed inset-0 bg-black/70 z-[105] flex items-start justify-center p-4 pt-44"
            onClick={() => setShowModal(false)}
          >
            <motion.div
              className="bg-[#EBE5DC] dark:bg-[#1a1a2e] rounded-2xl p-6 max-w-2xl"
              onClick={(e) => e.stopPropagation()}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
            >
              <ModalContent onClose={() => setShowModal(false)} />
            </motion.div>
          </motion.div>
        </AnimatePresence>,
        document.body
      )}
    </>
  );
};
```

## Z-Index Hierarchy

**CRITICAL**: Maintain this exact z-index order:

```
z-[120] - Header (HIGHEST - always visible)
z-[110] - User management modals
z-[105] - Wearables/data modals
z-[100] - Theme toggle (fixed position)
z-[99]  - Combat mode banner
z-[50]  - Regular content
```

**Header must ALWAYS be z-[120]** to stay above all modals!

## Backdrop Opacity

Use **70% opacity** for backdrop (allows page visibility):

```jsx
// ✅ CORRECT - Semi-transparent backdrop
className="bg-black/70"

// ❌ WRONG - Fully opaque (can't see page)
className="bg-black"
```

**Modal content should be 100% opaque** (solid backgrounds):

```jsx
// ✅ CORRECT - Solid modal content
className="bg-[#EBE5DC] dark:bg-[#1a1a2e]"

// ❌ WRONG - Transparent content (hard to read)
className="bg-white/10 dark:bg-black/10"
```

## AnimatePresence Placement

**CRITICAL**: AnimatePresence goes INSIDE createPortal!

```jsx
// ✅ CORRECT
{showModal && createPortal(
  <AnimatePresence>
    <motion.div key="modal">...</motion.div>
  </AnimatePresence>,
  document.body
)}

// ❌ WRONG - AnimatePresence wrapping createPortal breaks tracking
<AnimatePresence>
  {showModal && createPortal(
    <motion.div>...</motion.div>,
    document.body
  )}
</AnimatePresence>
```

**Add unique `key` prop** to motion.div for Framer Motion tracking!

## Positioning

Use **`pt-44` (176px)** for modal content start:

```jsx
className="fixed inset-0 ... pt-44"
```

**Why**:
- Header ends at ~160px (including padding)
- 16px clearance ensures no overlap
- Modals start below header

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Header goes black | Modal in header's DOM tree | Use createPortal |
| Button doesn't work | AnimatePresence wrapping Portal | Move AnimatePresence inside |
| Content transparent | Using glass effects on content | Use solid backgrounds |
| Can't see page | Backdrop 100% opaque | Use `bg-black/70` |
| Animation broken | Missing key prop | Add `key="modal-unique-key"` |

## Detailed Examples

For complete working examples, see:

- **Modal Examples**: [references/modal-examples.md](references/modal-examples.md)

## Dark Mode Implementation

```jsx
<motion.div className="bg-[#EBE5DC] dark:bg-[#1a1a2e] ...">
  {/* Light mode: Cream #EBE5DC */}
  {/* Dark mode: Deep navy #1a1a2e */}
  {/* Both 100% opaque (solid) */}
</motion.div>
```

**Never use transparency on modal content** - only on backdrop!

## Working Examples

**WearablesQuickView.jsx** - Correct Portal usage
**HealthUserManager.jsx** - Called from modal (nested Portal)

---

**Pattern**: React Portal + AnimatePresence
**Z-Index**: Header 120 > Modals 105-110
**Opacity**: Backdrop 70%, Content 100%
**Last Updated**: October 8, 2025
