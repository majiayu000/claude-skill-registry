---
name: apple-guidelines
description: Apple Human Interface Guidelines and App Store requirements. Use when designing UI, handling app review requirements, privacy policies, or platform-specific UX patterns.
---

# Apple Guidelines for Finance App

## App Store Requirements for Finance Apps
- Privacy policy required (handles financial data)
- Data encryption at rest and in transit
- Biometric auth option for accessing financial data
- No third-party analytics tracking financial data without consent
- Clear data deletion option (GDPR, App Privacy)

## iOS HIG Key Points
- Tab bar: max 5 tabs, most important features
- Suggested tabs: Dashboard, Transactions, Budget, Accounts, Settings
- Use SF Symbols for icons (consistent with system)
- Sheets for creation flows, push for detail views
- Swipe actions: Delete (destructive, red), Archive, etc.
- Pull to refresh for synced data

## macOS HIG Key Points
- Sidebar navigation (NavigationSplitView)
- Keyboard shortcuts for common actions (⌘N new, ⌘S save)
- Menu bar integration
- Toolbar for contextual actions
- Support standard macOS window behaviors (resize, full screen)

## Accessibility Checklist
- VoiceOver labels on all interactive elements
- Dynamic Type support (no fixed font sizes)
- Sufficient color contrast (4.5:1 minimum)
- Don't use color alone to convey information
- Support Bold Text setting
- Reduce Motion support
