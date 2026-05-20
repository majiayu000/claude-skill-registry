---
name: "desktop-shell-maximized-content-inset"
description: "Prevent maximize-only clipping in a custom WPF shell by insetting hosted content at the native boundary"
domain: "desktop-hosting"
confidence: "high"
source: "bishop-maximize-clipping-fix"
---

## Context

Use this when a WPF desktop shell owns custom chrome (`WindowStyle=None` / `WindowChrome`) and hosted content such as WebView2 looks correct in restored mode but loses accents or edge content when maximized.

## Pattern

1. Treat maximize-only edge clipping as a host-boundary issue first, not a web-layout bug.
2. Name the hosted content container separately from the native titlebar/container chrome.
3. On maximize, inset that hosted content container by `SystemParameters.WindowResizeBorderThickness` on the clipped edges.
4. If the native titlebar already owns the top chrome, keep the top inset at zero so you do not create a second gap under the separator.
5. On restore, return the inset to zero so restored spacing stays identical.
6. Keep the titlebar row independent if you want maximize padding only for hosted content.

## Why

The maximized resize frame can overlap the client area in custom-chrome shells. A host-side inset respects the native boundary without forcing the web app to carry maximize-state CSS hacks.

## Example

- `ShellContentHost.Margin = WindowState == WindowState.Maximized ? new Thickness(left, 0, right, bottom) : new Thickness(0);`

## Anti-Patterns

- Fixing a maximize-only host clipping bug by changing only the active-tab CSS
- Adding permanent padding that alters restored-mode spacing
- Insetting the whole window blindly when only the hosted content needs protection
