---
name: macos-scrollbar
description: Custom themed scrollbars for macOS WKWebView apps. Use when styling scrollbars in the native macOS app, fixing scrollbar theming issues, or implementing custom scroll containers that work in WKWebView.
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

## References

- [CSS Negative Margin Technique](https://www.codestudy.net/blog/hide-scroll-bar-but-while-still-being-able-to-scroll/)
- [WKWebView Scrollbar Limitations - Apache JIRA](https://issues.apache.org/jira/browse/CB-10123)
- [Apple Developer Forums - WKWebView Scroll](https://developer.apple.com/forums/thread/134112)
