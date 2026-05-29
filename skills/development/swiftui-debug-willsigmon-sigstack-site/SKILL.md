---
name: swiftui-debug
description: Debug SwiftUI view issues (state, bindings, rendering)
model: sonnet
---

# SwiftUI Debugging Guide

Debug common SwiftUI issues in the Leavn app:

## Common Issues

### 1. View Not Updating
**Check:**
- Is ViewModel using `@Observable` macro?
- Are properties marked `@MainActor` if needed?
- Is view observing the right object?

**Fix:**
```swift
// Ensure ViewModel is @Observable
@Observable
class MyViewModel {
    var state: String = ""  // Auto-tracked
}

// Ensure view observes it
@State var viewModel = MyViewModel()  // Not @StateObject
```

### 2. Binding Not Working
**Check:**
- Is the binding two-way?
- Is the source value actually mutable?
- Is there a `@Binding` vs `@State` mismatch?

**Fix:**
```swift
// Correct binding chain
@State var value: String
TextField("", text: $value)  // $ creates Binding
```

### 3. Modal/Sheet Won't Dismiss
**Check:**
- Is `@Environment(\.dismiss)` being called?
- Is `isPresented` binding being set to false?
- Are there multiple presentation modifiers conflicting?

**Fix:**
```swift
@Environment(\.dismiss) var dismiss

Button("Close") {
    isPresented = false  // Update binding
    dismiss()  // Call environment dismiss
}
```

### 4. Performance Issues
**Check:**
- Are views too complex? (use `Self._printChanges()`)
- Unnecessary re-renders?
- Heavy computations in body?

**Fix:**
- Extract subviews
- Use `@State` sparingly
- Move logic to ViewModel

**Return specific fixes for the reported SwiftUI issue.**
