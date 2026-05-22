---
name: Swift Binding Fixer
description: Fix SwiftUI binding errors ($var issues) by adding @Bindable to @Observable ViewModels in Leavn app
allowed-tools: Read, Edit, Grep
---

# Swift Binding Fixer

## Instructions

Fix "cannot find '$viewModel'" errors:

1. **Find the error**:
   ```bash
   grep "cannot find '\$viewModel'" build_output.txt
   ```

2. **Read the view file**:
   - Check if viewModel is @Observable type
   - Look for `@State var viewModel` or `var viewModel`
   - Find all `$viewModel.property` usages

3. **Apply fix**:
   ```swift
   // BEFORE
   @State var viewModel: MyViewModel
   // OR
   var viewModel: MyViewModel

   // AFTER (if using $viewModel)
   @Bindable var viewModel: MyViewModel
   ```

4. **Common Leavn patterns**:
   - HomeViewModel: Use @Bindable for sheet bindings
   - CommunityViewModel: Use @Bindable for showCreate* bindings
   - SettingsViewModel: Use @Bindable for alert bindings
   - SermonAIView: Use @Bindable for showing* bindings

Use this skill when: $viewModel errors, @Observable binding issues, sheet presentation errors
