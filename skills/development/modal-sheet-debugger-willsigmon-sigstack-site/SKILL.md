---
name: Modal Sheet Debugger
description: Fix SwiftUI sheet presentation issues in Leavn - competing sheets, dismissal patterns, binding synchronization, enum-based consolidation
allowed-tools: Read, Edit, Grep
---

# Modal Sheet Debugger

Fix sheet presentation issues:

1. **Find competing sheets**: Multiple `.sheet()` modifiers on same view
2. **Consolidate pattern**:
   ```swift
   enum SheetType: Identifiable {
       case optionA, optionB
       var id: String { ... }
   }
   @State var activeSheet: SheetType?
   .sheet(item: $activeSheet) { type in
       switch type { ... }
   }
   ```

3. **Fix dismissal**: Update binding before dismiss()
4. **Check bindings**: Ensure parent and environment in sync

Use when: Multiple sheets conflict, dismissal bugs, sheet state issues
