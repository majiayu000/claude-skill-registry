---
name: webflow-page-transitions
description: Manage and implement client-side page transitions using Taxi.js. Use when creating transition animations, handling cross-page state, or debugging navigation.
---

# Webflow Page Transitions

This skill covers how to work with the Taxi.js transition system and how it triggers module lifecycles.

## Implementation Pattern

```typescript
import { onPageIn, onPageOut } from "@/modules/_";
import gsap from "@lib/gsap";

export default function(element: HTMLElement) {
  onPageIn(async () => {
    await gsap.from(element, { opacity: 0, duration: 1 });
  });

  onPageOut(async () => {
    await gsap.to(element, { opacity: 0, duration: 0.5 });
  }, { element });
}
```
