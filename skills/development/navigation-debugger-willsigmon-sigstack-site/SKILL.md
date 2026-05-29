---
name: Navigation Debugger
description: Debug Leavn navigation issues - NotificationCenter routing, deep links, tab selection, AppCoordinator, modal presentations
allowed-tools: Read, Edit, Grep
---

# Navigation Debugger

Fix navigation bugs in Leavn:

1. **Check notification handling**:
   - Search for notification name in ContentView
   - Verify .onReceive() handlers exist
   - Check AppCoordinator navigation methods

2. **Common Leavn patterns**:
   ```swift
   // Post navigation
   NotificationCenter.default.post(
       name: .OpenBibleReference,
       userInfo: ["book": "Genesis", "chapter": 1]
   )

   // Handle in ContentView
   .onReceive(NotificationCenter.default.publisher(for: .OpenBibleReference)) {
       // Navigate to Bible
   }
   ```

3. **Debug steps**:
   - Add AppLog in notification handlers
   - Verify userInfo parsing
   - Check tab selection works
   - Test deep link URLs

Use when: Navigation broken, wrong screen, deep links fail, tab routing issues
