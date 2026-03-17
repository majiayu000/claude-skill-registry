## <!-- markdownlint-disable MD041 -->

name: frontend-design
description: Create distinctive, production-grade Quickshell (QML) widgets and interfaces for the user's desktop environment. Specialized for the @quickshell configuration, using existing components, theme tokens, and services. Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt

---

# Frontend Design Skill

This skill guides the creation of high-quality QML interfaces for Quickshell, specifically tailored to the `@quickshell/.config/quickshell/` configuration. It combines technical Quickshell expertise with high-end aesthetic design thinking.

## Design Thinking

Before coding, commit to a BOLD aesthetic direction that fits the "Obelisk" shell but pushes it further:

- **Tone**: Pick a flavor: brutally minimal, retro-futuristic, refined luxury, industrial/utilitarian, or organic.
- **Differentiation**: What is the one thing that makes this widget UNFORGETTABLE?
- **Intentionality**: Bold maximalism and refined minimalism both work; the key is executing with precision.

## Quickshell Design Principles

- **Native Integration**: Widgets must look and feel like part of the existing "Obelisk" shell.
- **Theming**: Rigorously use the `Theme` singleton (`qs.Config`) for all colors, sizes, radii, and fonts.
- **Reusability**: Use existing components from `qs.Components` (`OText`, `OButton`, `IconButton`, `OPanel`) whenever possible.
- **Reactive**: Bind properties to Services (`qs.Services`) for live data.

## Technical Foundation

Always include necessary imports:

```qml
import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Wayland
import qs.Config      // Theme, Settings
import qs.Components  // OText, OButton, OPanel, etc.
import qs.Services    // Core, SystemInfo, WM
```

### Theming Guidelines (`Theme.qml`)

- **Backgrounds**: `Theme.bgColor`, `Theme.bgElevated`, `Theme.bgElevatedAlt`
- **Accents**: `Theme.activeColor`, `Theme.onHoverColor`, `Theme.critical` (red), `Theme.warning` (orange)
- **Text**: `Theme.textActiveColor`, `Theme.textInactiveColor`
- **Spacing**: `Theme.spacingXs` to `Theme.spacingXl`
- **Radii**: `Theme.itemRadius`, `Theme.radiusMd`, `Theme.radiusLg`

## Aesthetics & Polish

- **Typography**: Stick to `Theme.fontFamily` (CaskaydiaCove) and `Theme.iconFontFamily`. Use `OText` variants for hierarchy.
- **Motion**: Use `Behavior on <property>` with `Theme.animationDuration` and `Easing.InOutQuad` for all transitions. Focus on staggered reveals and smooth width/opacity changes.
- **Visual Details**: Create depth. Use `RectangularShadow` or `MultiEffect` for subtle shadows. Use `Canvas` for custom gradient borders (see `CardStyling.qml`).
- **Avoid "AI Slop"**: No predictable layouts or generic "purple on white" color schemes. Stay true to the project's Catppuccin/Dracula/Obelisk color palettes.

## Component Usage

- **OText**: `OText { text: "Label"; bold: true; muted: true }`
- **IconButton**: For circular icon-only buttons.
- **OPanel**: For dropdowns/menus. Always provide a unique `panelNamespace`.
- **ExpandingPill**: Use for collapsible groups of buttons (like PowerMenu or Workspaces).

## New Modules

When creating a new widget:

1. Place it in `Modules/<Category>/<Name>.qml`.
2. Use `pragma ComponentBehavior: Bound`.
3. **Example Pattern**:

```qml
pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Layouts
import qs.Config
import qs.Components

Rectangle {
    color: Theme.bgElevated
    radius: Theme.itemRadius
    border.color: Theme.borderLight
    border.width: 1

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Theme.spacingMd
        spacing: Theme.spacingSm

        OText {
            text: "Widget Title"
            bold: true
            size: "lg"
        }
        // ... content
    }
}
```
