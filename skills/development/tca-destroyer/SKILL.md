---
name: TCA Destroyer
description: Remove TCA (Composable Architecture) code from Leavn - delete reducers, migrate to @Observable ViewModels, remove dependencies
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# TCA Destroyer

Eliminate TCA from codebase:

1. **Find TCA code**:
   - *Feature.swift files
   - Reducer protocols
   - Store/ViewStore
   - Dependencies from TCA

2. **Migration path**:
   - Extract business logic
   - Create @Observable ViewModel
   - Replace Store with ViewModel
   - Update views

3. **Delete**:
   - Remove TCA imports
   - Delete Feature files
   - Clean Dependencies

Use when: TCA removal, modernizing architecture, deprecating legacy patterns
