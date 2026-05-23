---
name: managing-global-state
description: Defines when and how to manage shared state using React Context or Zustand. Use for global persistent data like the "Booking Cart".
---

# Global State Management

## When to use this skill
- Managing a "Booking Cart" or "Wishlist".
- Storing temporary user preferences during a session.
- Avoid prop-drilling more than 3 levels deep.

## Tools
- **Zustand**: Preferred for its simplicity and performance in Next.js.
- **React Context**: Use for simple theme or auth state.

## Implementation (Zustand)
```typescript
import { create } from 'zustand';
import { Tour } from '@/types';

interface CartState {
    items: Tour[];
    addItem: (tour: Tour) => void;
    removeItem: (id: string) => void;
    clearCart: () => void;
}

export const useCartStore = create<CartState>((set) => ({
    items: [],
    addItem: (tour) => set((state) => ({ items: [...state.items, tour] })),
    removeItem: (id) => set((state) => ({ items: state.items.filter(i => i.$id !== id) })),
    clearCart: () => set({ items: [] }),
}));
```

## Instructions
- **Persistence**: Use Zustand's middleware for `localStorage` if the cart needs to survive refresh.
- **Context Boundaries**: Keep Context Providers high up in `layout.tsx`.
