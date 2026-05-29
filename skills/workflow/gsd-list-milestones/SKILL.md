---
name: gsd-list-milestones
description: Display completed milestones from the MILESTONES.md registry
allowed-tools: Read, Bash
---


<objective>
Display completed milestones from the MILESTONES.md registry.

Purpose: Show milestone history without scanning filesystem.
Output: Formatted list of completed milestones with key accomplishments.
</objective>

<execution_context>
@.github/get-shit-done/references/ui-brand.md
</execution_context>

<context>
Registry file:
- `.planning/MILESTONES.md` — Milestone completion registry
</context>

<process>

<step name="check_registry_exists">
Check if milestone registry exists using bash:

```bash
if [ ! -f .planning/MILESTONES.md ]; then
    echo ""
    echo "No milestones completed yet."
    echo ""
    echo "Complete your first milestone with:"
    echo "  /gsd-complete-milestone"
    echo ""
    exit 0
fi
```

If registry doesn't exist: Show friendly message and exit.
If registry exists: Continue to display step.
</step>

<step name="display_milestones">
Display milestone history from registry:

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " GSD ► MILESTONE HISTORY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Display registry content
cat .planning/MILESTONES.md

echo ""
echo "───────────────────────────────────────────────────────────────"
echo ""
echo "Archived milestones are in: .planning/history/"
echo ""
echo "To view archived files:"
echo "  ls .planning/history/v1.0/"
echo "  cat .planning/history/v1.0/ROADMAP.md"
echo ""
echo "To start new milestone:"
echo "  /gsd-new-milestone"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```
</step>

</process>

<success_criteria>
- [ ] Registry existence checked before display
- [ ] Friendly message if no milestones completed yet
- [ ] MILESTONES.md content displayed directly (no parsing)
- [ ] Helpful bash commands shown for accessing archives
- [ ] User knows next command (complete-milestone or new-milestone)
- [ ] Template variables (/gsd-) used for cross-platform support
</success_criteria>
