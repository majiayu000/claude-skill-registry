---
name: Widget Extension Builder
description: Create and maintain iOS widgets for Leavn - VOTD widget, reading plan widget, prayer widget with proper data sharing and refresh
allowed-tools: Read, Write, Edit
---

# Widget Extension Builder

Build iOS widgets:

1. **Widget types**:
   - VerseOfDayWidget
   - ReadingPlanWidget
   - CommunityPrayerWidget
   - ReadingLiveActivity

2. **Data sharing**:
   - Use SharedWidgetStore
   - App group: `group.com.leavn.app`
   - Write from main app, read from widget

3. **Localization**:
   - Use WidgetI18n (separate from main app)
   - All 6 languages supported

4. **Refresh**:
   - Timeline provider
   - Background refresh
   - User-triggered reload

Use when: Creating widgets, updating widget data, widget refresh issues
