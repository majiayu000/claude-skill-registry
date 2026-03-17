---
name: macos-scrollbar
description: Custom themed scrollbars for macOS WKWebView apps. Use when styling scrollbars in the native macOS app, fixing scrollbar theming issues, implementing custom scroll containers that work in WKWebView, or debugging scroll position persistence issues with tabs.
---

# MacOS WKWebView Custom Scrollbars

## The Problem

WKWebView on macOS does **not** support standard CSS scrollbar styling:
- `::-webkit-scrollbar` pseudo-elements are ignored
- `scrollbar-color` and `scrollbar-width` CSS properties don't work reliably
- Native scrollbars always render with system appearance

This means CSS-based scrollbar theming that works in browsers will NOT work in the native macOS app.

## The Solution: Negative Margin Technique

Hide the native scrollbar using pure CSS layout (not pseudo-elements):

1. **Outer wrapper**: `overflow: hidden` clips the native scrollbar
2. **Inner scrollable div**: `overflow-y: scroll` + `marginRight: -20px` pushes scrollbar outside
3. **Padding compensation**: `paddingRight: 20px` ensures content isn't cut off
4. **Custom overlay**: Render a themed scrollbar as a positioned DOM element

## Usage

Use the `OverlayScrollbar` component from `@/components/OverlayScrollbar`:

```tsx
import { OverlayScrollbar } from "@/components/OverlayScrollbar";

// Basic usage
<OverlayScrollbar className="h-full">
    <div>Your scrollable content here</div>
</OverlayScrollbar>

// With scroll position persistence
const scrollRef = useTabScrollPersistence(tabId);

<OverlayScrollbar
    scrollRef={scrollRef}
    className="flex-1 h-full"
    style={{ backgroundColor: currentTheme.styles.surfacePrimary }}
>
    <div>Content with scroll position saved</div>
</OverlayScrollbar>
```

## Component Props

| Prop | Type | Description |
|------|------|-------------|
| `children` | `ReactNode` | Scrollable content |
| `className` | `string` | CSS classes for outer wrapper |
| `style` | `CSSProperties` | Inline styles for outer wrapper |
| `scrollRef` | `RefObject<HTMLDivElement>` | Optional ref for scroll position access |

## Features

- **Theme-aware**: Uses `currentTheme.styles.borderDefault` for scrollbar color
- **Auto-hide**: Scrollbar fades out after 1 second of inactivity
- **Hover to show**: Scrollbar appears when hovering the container
- **Drag support**: Click and drag the thumb to scroll
- **Track click**: Click the track to jump to position
- **Resize-aware**: Updates when content or container size changes

## When to Use

Use `OverlayScrollbar` instead of native `overflow-y-auto` when:
- The scroll container needs themed scrollbars
- The component renders in the macOS WKWebView app
- You want consistent scrollbar appearance across web and native

## When NOT to Use

- Very small scroll areas (the overlay adds complexity)
- Performance-critical lists with thousands of items (consider virtualization)
- Areas where native scrollbar behavior is preferred

## Implementation Details

See the full component at: `src/components/OverlayScrollbar.tsx`

Key constants:
- `SCROLLBAR_WIDTH = 20` - Margin to hide native scrollbar (macOS scrollbar is ~15-17px)
- Thumb minimum height: 30px
- Hide delay: 1000ms after scroll stops
- Fade transition: 150ms

## Scroll Position Persistence for Tabs

When implementing scroll persistence for workspace tabs, use `useTabScrollPersistence` with `OverlayScrollbar`.

### How It Works

1. `useTabScrollPersistence(tabId)` returns a ref and:
   - Saves scroll position to a module-level Map on every scroll event
   - Restores position when the component mounts (using ResizeObserver/MutationObserver for async content)

2. Pass the ref to `OverlayScrollbar`:
   ```tsx
   const scrollRef = useTabScrollPersistence(tabId);

   <OverlayScrollbar scrollRef={scrollRef} className="flex-1">
       {/* content */}
   </OverlayScrollbar>
   ```

### Critical Rule: Keep OverlayScrollbar Mounted

**The ref must be attached to a mounted element when `useTabScrollPersistence`'s effect runs.**

If you conditionally render a different tree during loading, the ref won't be set and restoration will fail:

```tsx
// BAD - OverlayScrollbar unmounts during loading, ref is null when effect runs
if (isLoading) {
    return <Loader />;  // Different tree, no OverlayScrollbar!
}

return (
    <OverlayScrollbar scrollRef={scrollRef}>
        {/* content */}
    </OverlayScrollbar>
);
```

```tsx
// GOOD - OverlayScrollbar stays mounted, ref is always set
return (
    <OverlayScrollbar scrollRef={scrollRef} className="flex-1">
        {isLoading ? (
            <div className="flex h-full items-center justify-center">
                <Loader />
            </div>
        ) : (
            {/* actual content */}
        )}
    </OverlayScrollbar>
);
```

### Why This Matters

The `useTabScrollPersistence` hook runs its effect on mount with `[tabId]` dependency:

```tsx
useEffect(() => {
    const element = scrollRef.current;
    if (!element) return;  // Early return if ref not set!

    // Set up observers and attempt restoration...
}, [tabId]);
```

If the element isn't mounted when the effect runs:
1. `scrollRef.current` is `null`
2. Effect returns early without setting up observers
3. When content loads and OverlayScrollbar mounts, the effect doesn't re-run
4. No scroll restoration happens

### Checklist for Scroll Persistence

- [ ] Use `OverlayScrollbar` (not native `overflow-y-auto`) for the scroll container
- [ ] Pass `scrollRef` from `useTabScrollPersistence` to `OverlayScrollbar`
- [ ] Keep `OverlayScrollbar` in the component tree during ALL render states (loading, error, etc.)
- [ ] Render loading/error states as CHILDREN of `OverlayScrollbar`, not as alternative returns

### Key Files

| File | Purpose |
|------|---------|
| `src/hooks/useTabScrollPersistence.ts` | Hook that saves/restores scroll position per tab |
| `src/components/OverlayScrollbar.tsx` | Custom scrollbar with `scrollRef` prop |
| `src/features/notes/note-view.tsx` | Reference implementation (lines 1370-1457) |
| `src/features/chat/chat-view.tsx` | Chat implementation with loading state handling |

## References

- [CSS Negative Margin Technique](https://www.codestudy.net/blog/hide-scroll-bar-but-while-still-being-able-to-scroll/)
- [WKWebView Scrollbar Limitations - Apache JIRA](https://issues.apache.org/jira/browse/CB-10123)
- [Apple Developer Forums - WKWebView Scroll](https://developer.apple.com/forums/thread/134112)
