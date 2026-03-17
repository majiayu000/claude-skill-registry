---
name: theme-handler
description: Manage and update application themes using shadcn and tweakcn.
tools: Run, terminal_cmd
model: inherit
---

# Theme Handler

## Instructions

### 1. Updating the Theme
To update the application theme, choose a theme from the [Available Themes](reference.md) list and run the installation command.

1.  **Select a Theme**: Pick a theme URL from the reference list.
2.  **Install Command**: Run the following command, replacing `<theme-url>` with your choice:
    ```bash
    pnpm dlx shadcn@latest add <theme-url>
    ```

### 2. Example Usage
> "Update the theme to 'Modern Minimal'."

Command to run:
```bash
pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/modern-minimal.json
```

## Reference
See [reference.md](reference.md) for a complete list of available themes and their installation URLs.

