---
name: figma-to-page
description: "Generates React code for a full page based on pasted Figma 'Inspect' details. Uses the page scaffolder."
---

# Figma to Page Workflow

1.  Ask for the page name in `PascalCase` (e.g., `UserProfile`).
2.  Ask the user to paste all details from the Figma 'Inspect' panel for the _entire page_.
3.  **Execute scaffolder:**
    - Run `chmod +x .claude/skills/react-page-scaffolder/scripts/create-page.sh`
    - Run `.claude/skills/react-page-scaffolder/scripts/create-page.sh {{PAGE_NAME}}`
    - Report the output (the new file paths). Let `{{PAGE_DIR}}` be the new directory (e.g., `src/pages/userprofile`).
4.  **Generate Code:**
    - Read the user-pasted Figma details.
    - Generate the TSX code for `{{PAGE_DIR}}/{{PAGE_NAME}}.tsx`.
    - Generate the corresponding CSS for `{{PAGE_DIR}}/{{PAGE_NAME}}.module.css`.
5.  **Write Files:**
    - Write the new TSX content, overwriting the template.
    - Write the new CSS content, overwriting the template.
6.  **Lint:** Run `yarn lint:fix {{PAGE_DIR}}` to clean up the new files.
7.  Report that the page has been created and populated from Figma details.
