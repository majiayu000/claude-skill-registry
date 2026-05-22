---
name: material-design
description: Guide for implementing Material Design 3 (Material You). Use when designing Android apps, implementing dynamic theming, or following Material component patterns.
---

# Material Design 3 (Material You)

Apply Google's Material Design 3 principles when designing and developing user interfaces with emphasis on personalization, accessibility, and cross-platform consistency.

## When to Activate

Use this skill when:
- Designing or implementing Android applications
- Building web applications following Material Design
- Working with Flutter or Jetpack Compose
- Implementing dynamic theming and color systems
- Creating Material components
- Reviewing designs for Material Design compliance

## What is Material Design 3?

Material Design 3 (Material You) represents Google's latest design system with:

- **Personalization**: Dynamic color extraction from user preferences
- **Expressiveness**: Softer, rounded components with visual hierarchy
- **Adaptability**: Responsive across devices and platforms
- **Accessibility**: Built-in inclusive design features

## Key Differences from Material Design 2

| Aspect | MD2 | MD3 |
|--------|-----|-----|
| **Colors** | Fixed brand palettes | Dynamic, user-generated schemes |
| **Customization** | Limited theming | Highly personalized |
| **Components** | Flat, rigid shapes | Rounded, expressive |
| **Accessibility** | Basic support | Priority built-in |

## Core Foundations

### 1. Dynamic Color System

Material Design 3 uses HCT (Hue, Chroma, Tone) color space for perceptually accurate color generation.

**Key concepts:**
- Color roles (primary, secondary, tertiary, error, neutral)
- Tonal palettes (50-99 tones per color)
- Automatic light/dark theme generation
- User-driven personalization from wallpaper/system

For detailed color system implementation, see `references/color-system.md`.

### 2. Typography

Type scale with 5 display sizes and 9 text sizes:

**Quick example:**
- Display Large: 57sp
- Headline Large: 32sp
- Body Large: 16sp
- Label Small: 11sp

For complete typography system and responsive scaling, see `references/typography.md`.

### 3. Layout

Responsive breakpoints and grid system:

- **Compact**: 0-599dp (phones)
- **Medium**: 600-839dp (tablets, folded phones)
- **Expanded**: 840dp+ (desktops, large tablets)

For layout guidelines and examples, see `references/layout.md`.

## Component Guidelines

Material Design 3 provides specifications for:

- **Common Buttons**: Elevated, Filled, Tonal, Outlined, Text
- **Cards**: Elevated, Filled, Outlined variants
- **Text Fields**: Filled, Outlined with labels and helper text
- **Navigation**: Navigation bar, rail, drawer
- **Chips**: Assist, Filter, Input, Suggestion chips
- **Dialogs**: Basic, Full-screen dialogs

For detailed component specifications, consult `references/components.md`.

## Quick Component Examples

### Buttons

```kotlin
// Jetpack Compose
Button(onClick = { }) {
    Text("Filled Button")
}

OutlinedButton(onClick = { }) {
    Text("Outlined Button")
}
```

### Cards

```kotlin
Card(
    modifier = Modifier.fillMaxWidth(),
    elevation = CardDefaults.cardElevation(defaultElevation = 6.dp)
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Card Title", style = MaterialTheme.typography.headlineSmall)
        Text("Card content", style = MaterialTheme.typography.bodyMedium)
    }
}
```

### Text Fields

```kotlin
OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("Label") },
    supportingText = { Text("Helper text") }
)
```

For more component examples and patterns, see `references/components.md`.

## Implementing Dynamic Color

### Android (Jetpack Compose)

```kotlin
val dynamicColor = Build.VERSION.SDK_INT >= Build.VERSION_CODES.S

val colorScheme = when {
    dynamicColor && darkTheme -> dynamicDarkColorScheme(LocalContext.current)
    dynamicColor && !darkTheme -> dynamicLightColorScheme(LocalContext.current)
    darkTheme -> darkColorScheme()
    else -> lightColorScheme()
}

MaterialTheme(
    colorScheme = colorScheme,
    typography = Typography,
    content = content
)
```

### Web

For web implementation with Material Web Components, see `references/web-implementation.md`.

## Motion and Animation

Material Design 3 motion principles:
- **Easing**: Standard, emphasized, decelerated curves
- **Duration**: Based on travel distance and complexity
- **Choreography**: Coordinated element movements

For motion specifications, see `references/motion.md`.

## Accessibility

Material Design 3 prioritizes accessibility:
- Minimum 4.5:1 contrast ratio (text)
- 3:1 contrast ratio (UI components)
- Touch targets minimum 48dp × 48dp
- Screen reader support
- Semantic color usage (not color-only indicators)

For accessibility implementation details, see `references/accessibility.md`.

## When to Consult References

- **Color system implementation**: Read `references/color-system.md`
- **Typography scales and usage**: Read `references/typography.md`
- **Layout and responsive design**: Read `references/layout.md`
- **Component specifications**: Read `references/components.md`
- **Web implementation**: Read `references/web-implementation.md`
- **Motion and animation**: Read `references/motion.md`
- **Accessibility guidelines**: Read `references/accessibility.md`

## Key Principles

- **User-driven personalization**: Colors adapt to user preferences
- **Expressive and flexible**: Rounded corners, dynamic elevation
- **Accessible by default**: Built-in contrast, touch targets, semantics
- **Cross-platform consistency**: Same principles across Android, web, iOS
- **Design tokens**: Use semantic tokens, not hardcoded values
- **Responsive**: Adapt to device size and orientation

## Resources

- **Material Design 3**: https://m3.material.io/
- **Material Theme Builder**: https://m3.material.io/theme-builder
- **Jetpack Compose**: https://developer.android.com/jetpack/compose/designsystems/material3
- **Material Web Components**: https://github.com/material-components/material-web
- **Flutter Material 3**: https://flutter.dev/docs/development/ui/material
