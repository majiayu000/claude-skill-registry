---
name: dendron-tree
description: Show the dendron note hierarchy as a visual tree. Accepts optional -L depth and prefix filter.
---

Run the dendron tree script with any arguments the user provides:

```bash
bash scripts/dendron-tree.sh $ARGUMENTS
```

- `-L N` limits tree depth
- A prefix (e.g., `swanki.processing`) filters to that subtree
- No args shows the full hierarchy

Show the output directly to the user.
