---
name: react-page-scaffolder
description: "Creates a complete React page directory (page.tsx, index.ts, styles.css) with routing integration. Use when asked to create a new page, view, or route handler that combines components and layouts."
---

# React Page Scaffolder Workflow

1.  Ask the user for the new page name in `PascalCase` (e.g., `UserProfile`).
2.  Make the helper script executable: `chmod +x .claude/skills/react-page-scaffolder/scripts/create-page.sh`
3.  Execute the scaffolding script: `.claude/skills/react-page-scaffolder/scripts/create-page.sh {{PAGE_NAME}}`
4.  Report the full output of the script to the user.
