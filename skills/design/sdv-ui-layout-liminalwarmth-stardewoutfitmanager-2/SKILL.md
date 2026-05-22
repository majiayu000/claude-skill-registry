---
name: sdv-ui-layout
description: This skill should be used when the user asks to "create a menu layout", "fix UI spacing", "adjust positioning", "design a menu", or discusses UI alignment, element placement, or visual layout. Also use when working on files in the Menus/ directory or when the user mentions layout, positioning, spacing, or menu design.
version: 1.0.0
---

# SDV UI Layout Designer

Design and validate Stardew Valley menu layouts with confidence. This skill provides a systematic approach to UI development that reduces trial-and-error iteration.

## Design Workflow

### 1. Conceptual Design First

Before writing any positioning code, create a text diagram of the intended layout:

```
+------------------------------------------+
|  [Tab1] [Tab2] [Tab3]      [X Close]     |  <- Tab bar (64px height)
+------------------------------------------+
|                                          |
|  +------------+   +------------------+   |
|  |            |   | Hat:    [<] [>]  |   |  <- Item selectors
|  |  Portrait  |   | Shirt:  [<] [>]  |   |
|  |   Box      |   | Pants:  [<] [>]  |   |
|  |  (256x384) |   | Boots:  [<] [>]  |   |
|  |            |   +------------------+   |
|  +------------+                          |
|                                          |
|  [Spring][Summer][Fall][Winter][Special] |  <- Categories
|                                          |
|              [Save Outfit]               |  <- Action buttons
+------------------------------------------+
```

### 2. Use Semantic Positioning

Replace magic numbers with named relationships:

```csharp
// BAD: Magic numbers
int buttonX = 324;
int buttonY = yPositionOnScreen + 88;

// GOOD: Semantic relationships
int buttonX = _portraitBox.Right + Spacing.ElementGap;
int buttonY = _portraitBox.Y;
```

### 3. Define Layout Constants

Create named constants for consistent spacing:

```csharp
private static class Layout
{
    // Standard SDV spacing
    public const int BorderWidth = IClickableMenu.borderWidth;           // 16
    public const int SpaceToClearSideBorder = IClickableMenu.spaceToClearSideBorder;  // 16

    // Custom spacing for this menu
    public const int ElementGap = 16;        // Between sibling elements
    public const int SectionGap = 32;        // Between major sections
    public const int ButtonSize = 64;        // Standard button dimensions
    public const int ArrowButtonSize = 48;   // Arrow/selector buttons
    public const int TabHeight = 64;         // Tab bar height
    public const int PortraitWidth = 256;    // 4x farmer sprite
    public const int PortraitHeight = 384;   // 4x farmer sprite
}
```

### 4. Use Anchor-Based Positioning

Position elements relative to anchors, not absolute coordinates:

```csharp
// Portrait anchored to menu left
_portraitBox = new Rectangle(
    xPositionOnScreen + Layout.BorderWidth + Layout.SpaceToClearSideBorder,
    yPositionOnScreen + Layout.TabHeight + Layout.SectionGap,
    Layout.PortraitWidth,
    Layout.PortraitHeight
);

// Selector buttons anchored to portrait right
int selectorX = _portraitBox.Right + Layout.SectionGap;
int selectorY = _portraitBox.Y;

// Categories anchored to portrait bottom
int categoryY = _portraitBox.Bottom + Layout.ElementGap;
```

### 5. Validate Before Testing

Run these static checks before manual testing:

1. **Bounds Check**: Verify all elements fit within menu bounds
2. **Overlap Check**: Detect potentially overlapping clickable regions
3. **Gamepad Navigation**: Verify all ClickableComponents have myID and neighborIDs
4. **Resolution Check**: Test positions at 1280x720, 1920x1080, 2560x1440

## SDV UI Conventions

### Standard Dimensions
- `IClickableMenu.borderWidth` = 16 pixels
- `IClickableMenu.spaceToClearSideBorder` = 16 pixels
- Standard button: 64x64 pixels
- Arrow buttons: 48x48 pixels (scale 1f) or 60x60 (scale 1.25f)
- Tab buttons: varies, typically 64px height

### Common Source Rectangles (Game1.mouseCursors)
```csharp
// Arrows (from Game1.getSourceRectForStandardTileSheet)
Game1.getSourceRectForStandardTileSheet(Game1.mouseCursors, 44)  // Left arrow
Game1.getSourceRectForStandardTileSheet(Game1.mouseCursors, 33)  // Right arrow

// Icons
new Rectangle(352, 495, 12, 11)   // Small left arrow
new Rectangle(365, 495, 12, 11)   // Small right arrow
new Rectangle(128, 256, 64, 64)   // OK/checkmark button
new Rectangle(322, 498, 12, 12)   // X/close icon
new Rectangle(310, 392, 16, 16)   // Star icon
new Rectangle(323, 433, 9, 10)    // Trash can
```

### Centering Pattern
```csharp
Vector2 topLeft = Utility.getTopLeftPositionForCenteringOnScreen(width, height);
xPositionOnScreen = (int)topLeft.X;
yPositionOnScreen = (int)topLeft.Y;
```

### Window Resize Handling
```csharp
public override void gameWindowSizeChanged(Rectangle oldBounds, Rectangle newBounds)
{
    base.gameWindowSizeChanged(oldBounds, newBounds);

    // Recenter menu
    Vector2 topLeft = Utility.getTopLeftPositionForCenteringOnScreen(width, height);
    xPositionOnScreen = (int)topLeft.X;
    yPositionOnScreen = (int)topLeft.Y;

    // Recalculate all element positions...
    RecalculateLayout();

    // CRITICAL: Propagate to child menus
    GetChildMenu()?.gameWindowSizeChanged(oldBounds, newBounds);
}
```

### Gamepad Navigation Requirements
```csharp
// Every clickable element needs:
component.myID = uniqueId;
component.leftNeighborID = leftId;    // or -99999 for none
component.rightNeighborID = rightId;
component.upNeighborID = upId;
component.downNeighborID = downId;

// Call after adding all components:
populateClickableComponentList();
snapToDefaultClickableComponent();
```

## Debug Overlay

When SMAPI debug mode is enabled, consider rendering element bounds for verification:

```csharp
#if DEBUG
private void DrawDebugOverlay(SpriteBatch b)
{
    // Draw clickable component bounds
    foreach (var component in allClickableComponents)
    {
        DrawBorder(b, component.bounds, Color.Red * 0.5f);
        // Draw component name/ID
        b.DrawString(Game1.tinyFont, $"{component.name}:{component.myID}",
            new Vector2(component.bounds.X, component.bounds.Y - 12), Color.White);
    }
}

private void DrawBorder(SpriteBatch b, Rectangle rect, Color color)
{
    b.Draw(Game1.staminaRect, new Rectangle(rect.X, rect.Y, rect.Width, 1), color);
    b.Draw(Game1.staminaRect, new Rectangle(rect.X, rect.Y + rect.Height - 1, rect.Width, 1), color);
    b.Draw(Game1.staminaRect, new Rectangle(rect.X, rect.Y, 1, rect.Height), color);
    b.Draw(Game1.staminaRect, new Rectangle(rect.X + rect.Width - 1, rect.Y, 1, rect.Height), color);
}
#endif
```

## Static Analysis Checklist

Before requesting manual testing, verify:

- [ ] All elements have explicit width/height (no implicit sizing)
- [ ] No hardcoded x/y positions without semantic meaning
- [ ] All ClickableComponents have myID assigned
- [ ] All ClickableComponents have neighborIDs for gamepad navigation
- [ ] Menu recalculates positions in gameWindowSizeChanged()
- [ ] Child menus receive gameWindowSizeChanged() propagation
- [ ] Text doesn't overflow element bounds at common resolutions
- [ ] Clickable regions don't overlap
- [ ] All elements fit within menu bounds with 16px margin

## References

See `references/` for detailed patterns from this codebase and SDV conventions.
