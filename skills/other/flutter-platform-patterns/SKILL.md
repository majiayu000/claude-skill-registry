---
name: flutter-platform-patterns
description: Guide platform-adaptive UI and native integration patterns when the user asks about Flutter platform differences, responsive layouts, or platform channels
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep
argument-hint: "[platform concern, widget, or integration need]"
read-only: true
destructive: false
idempotent: true
open-world: false
user-invocable: true
tags: flutter, mobile, patterns
---

# Flutter Platform Patterns

## Overview

Guide Flutter development for platform-adaptive UI, responsive layouts, and native platform integration. Covers Material vs. Cupertino patterns, adaptive widgets, responsive layout strategies, and platform channels. Stack-specific Tier 3 reference skill.

## Workflow

1. **Read project setup** — Check `.chalk/docs/engineering/` for architecture docs. Determine the target platforms (iOS, Android, web, desktop), minimum SDK versions, and any platform-specific requirements or design guidelines.

2. **Identify the scope** — Parse `$ARGUMENTS` for the specific platform pattern or concern. Categories include: adaptive UI, responsive layout, platform channels, or platform-specific behavior.

3. **Audit platform-adaptive UI** — Check for:
   - Hardcoded Material widgets where Cupertino equivalents are expected on iOS (e.g., `Switch` vs. `CupertinoSwitch`)
   - Missing platform checks (`Platform.isIOS`, `Theme.of(context).platform`) for platform-specific behavior
   - Navigation patterns that feel wrong on the target platform (e.g., bottom tabs on Android vs. iOS conventions)
   - Adaptive widget usage: prefer `Switch.adaptive`, `Slider.adaptive`, and similar when available

4. **Audit responsive layouts** — Check for:
   - Hardcoded widths/heights that break on different screen sizes
   - Missing `LayoutBuilder` or `MediaQuery` usage for responsive breakpoints
   - Single-column layouts that waste space on tablets and desktop
   - `ListView` without `shrinkWrap: true` consideration inside `Column` (common layout bug)
   - Missing `SafeArea` wrapping for notches and system UI

5. **Audit platform channels** — If native integration is needed, check for:
   - Method channel naming conventions (reverse domain: `com.example.app/channel`)
   - Missing error handling on both Dart and native sides
   - Missing null safety in channel communication
   - Heavy computation on the platform channel that should use an `Isolate` or background thread instead
   - Pigeon or `flutter_rust_bridge` usage where manual channels add unnecessary boilerplate

6. **Audit platform-specific concerns** — Check for:
   - iOS: proper `Info.plist` permissions, App Transport Security, keyboard handling
   - Android: proper `AndroidManifest.xml` permissions, back button handling, deep linking
   - Web: missing `kIsWeb` checks, unsupported plugins, SEO considerations
   - Desktop: window management, menu bar integration, keyboard shortcuts

7. **Report findings** — Present findings with specific file references, the current approach, the recommended pattern, and platform-specific rationale.

## Output

- **Format**: Audit report delivered in the conversation
- **Key sections**: Platform-Adaptive UI Findings, Responsive Layout Assessment, Platform Channel Review (if applicable), Platform-Specific Concerns, Recommended Patterns with Code Examples

## Anti-patterns

- **Platform-agnostic everything** — Not all UI should look the same on every platform. Users expect iOS apps to feel like iOS and Android apps to feel like Android. Use adaptive widgets and platform checks where conventions differ.
- **Overusing platform checks** — Conversely, wrapping every widget in `Platform.isIOS ? CupertinoX : MaterialX` is unmaintainable. Use adaptive variants where available and only add explicit checks for behaviors that genuinely differ.
- **Ignoring responsive design until tablet** — Phones come in many sizes. A layout that works on a Pixel 7 may break on an iPhone SE. Test with `LayoutBuilder` from the start.
- **Synchronous platform channels** — Platform channel calls are async. Blocking the UI thread while waiting for a native response causes jank. Always handle loading and error states.
- **Skipping error handling on channels** — Native code can throw exceptions that crash the app if not caught on the Dart side. Always wrap channel calls in try/catch and handle `MissingPluginException` for platforms that do not implement the channel.
