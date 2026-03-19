---
name: requirement-lock
description: Once requirements are confirmed, lock them. Prevent scope creep during building.
---

# Requirement Lock

After the user confirms what they want:
1. Internally record the confirmed requirements
2. If the user adds new requirements during building, acknowledge them but ask: "这个功能我先记下来，等现在这个做完再加，好不好？"
3. Never silently change direction mid-build
4. If requirements conflict with what was confirmed, point it out gently

The goal: finish what was agreed on FIRST, then iterate. Don't let the project spiral.
