---
name: todo
description: Add items to TODO.md
disable-model-invocation: true
argument-hint: [item description]
---

# Add Todo Item

Add this item to TODO.md in the project root:

$ARGUMENTS

## Instructions

1. Read TODO.md first to understand current structure
2. Determine the appropriate section based on the item:
   - Quick fixes, small UI tweaks → **Quick Add** (top of file)
   - New features → **Features**
   - Bug reports → **Bugs**
   - UI/UX issues → **Fixes**
   - If related to an existing Plan (In-App Chat, Case Page Redesign, Omni Bar, Proceedings Table), add to that plan's **Implementation** checklist
   - Code quality items → **Technical Debt**
3. Use checkbox format: `- [ ] Item description`
4. Keep descriptions concise but clear
5. Confirm what was added and where
