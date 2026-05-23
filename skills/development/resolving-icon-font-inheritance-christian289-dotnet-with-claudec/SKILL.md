---
name: resolving-icon-font-inheritance
description: "Resolves text font inheritance issues when using Segoe Fluent Icons in WPF CustomControl. Use when TextBlocks inherit icon fonts unexpectedly within ControlTemplate."
---

# WPF CustomControl Icon Font Inheritance Issue Resolution

## Problem Scenario

When using Segoe Fluent Icons font in WPF CustomControl, **TextBlocks within the same ControlTemplate inherit the icon font, causing text to render incorrectly**.

### Symptoms
- Button text displays as square boxes (□) or strange symbols
- Icons display correctly but regular text doesn't render

### Cause
WPF's `FontFamily` is inherited to child elements following the Visual Tree. When `FontFamily="Segoe Fluent Icons"` is set on a TextBlock for icons within a ControlTemplate, other TextBlocks in the same container may inherit this font.

---

## Solution

### Explicitly Specify FontFamily on Text-Displaying Elements

```xml
<!-- IconButton ControlTemplate Example -->
<ControlTemplate TargetType="{x:Type local:IconButton}">
    <Border Background="{TemplateBinding Background}"
            BorderBrush="{TemplateBinding BorderBrush}"
            BorderThickness="{TemplateBinding BorderThickness}">
        <StackPanel Orientation="{TemplateBinding Orientation}"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Center">

            <!-- Icon: Use Segoe Fluent Icons -->
            <TextBlock x:Name="PART_Icon"
                       Text="{TemplateBinding Icon}"
                       FontFamily="Segoe Fluent Icons, Segoe MDL2 Assets"
                       FontSize="{TemplateBinding IconSize}"
                       Foreground="{TemplateBinding Foreground}" />

            <!-- Text: Explicitly specify Segoe UI (Important!) -->
            <TextBlock x:Name="PART_Text"
                       Text="{TemplateBinding Text}"
                       FontFamily="Segoe UI"
                       FontSize="12"
                       Foreground="{TemplateBinding Foreground}"
                       VerticalAlignment="Center" />
        </StackPanel>
    </Border>
</ControlTemplate>
```

---

## Key Points

1. **Apply icon font only to specific element**: Specify `Segoe Fluent Icons` only on `PART_Icon`
2. **Explicitly specify FontFamily on text elements**: `FontFamily="Segoe UI"` is required on `PART_Text`
3. **Don't set FontFamily on parent containers**: Setting FontFamily on Border or StackPanel inherits to all children

---

## Applicable Controls

- IconButton (icon + text button)
- IconToggleButton (toggleable icon button)
- NavigationButton (navigation menu item)
- Any other CustomControl using icons and text together

---

## Related Icon Fonts

| Font Name | Windows Version | Purpose |
|-----------|-----------------|---------|
| `Segoe Fluent Icons` | Windows 11+ | Latest Fluent Design icons |
| `Segoe MDL2 Assets` | Windows 10+ | Default system icons |

### Fallback Pattern
```xml
FontFamily="Segoe Fluent Icons, Segoe MDL2 Assets"
```
Specify fallback font for Windows 10 compatibility
