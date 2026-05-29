---
name: mobile-patterns
description: Generic mobile patterns for navigation, gestures, and offline. Use when building any mobile application.
---

# Mobile Patterns

Framework-agnostic mobile best practices. These rules apply regardless of your platform (iOS, Android, React Native).

## When This Applies

- Building mobile applications
- Implementing navigation
- Handling offline scenarios
- Mobile performance optimization

## Extends

This is a **generic platform plugin**. Framework-specific plugins extend these rules:
- `ios` - Swift/SwiftUI specifics
- `android` - Kotlin/Compose specifics
- `react-native` - React Native/Expo specifics

## Quick Reference

| Section | Impact | Prefix |
|---------|--------|--------|
| Navigation | HIGH | `nav-` |
| Gestures | MEDIUM | `gesture-` |
| Offline | MEDIUM | `offline-` |
| Performance | MEDIUM | `perf-` |

## Status

**Scaffold** - Sections defined, rules to be added.

## Rules

See `rules/` directory for individual rules organized by section prefix.
