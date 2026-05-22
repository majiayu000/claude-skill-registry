---
name: tailwind-setup
description: Configure Tailwind CSS and shadcn/ui for React frontends with Django backends, including dark mode support and theme tokens. This skill should be used when setting up a new React project or adding Tailwind to an existing one.
allowed-tools: Bash, Write, Edit, Read, Glob, Grep, TodoWrite, mcp__shadcn__get_project_registries, mcp__shadcn__search_items_in_registries, mcp__shadcn__view_items_in_registries, mcp__shadcn__get_item_examples_from_registries, mcp__shadcn__get_add_command_for_items, mcp__shadcn__get_audit_checklist
---

## Purpose

Configure Tailwind CSS with shadcn/ui for React frontends connecting to Django backends. This setup includes dark mode support, theme tokens, and shadcn/ui component integration. The configuration enables automatic dark mode switching and provides a foundation for building consistent, themeable user interfaces.

## Setup Process Overview

Follow these steps in order:
1. Install Dependencies
2. Configure Vite for Django Backend
3. Setup Tailwind in CSS
4. Apply Base Theme (Required for dark mode support)
5. Setup shadcn/ui
6. Implement Dark Mode with Toggle
7. Verify Setup and Check for Errors

---

## Step 1: Install Dependencies

Install Tailwind CSS and the Vite plugin:

```bash
npm --prefix ./frontend tailwindcss @tailwindcss/vite
```

## Step 2: Configure Vite for Django Backend

Configure `vite.config.js` to enable Tailwind and path aliases:

1. Read existing `vite.config.js`
2. Add the required imports at the top (keep the existing React import):
   ```javascript
   import path from 'node:path'
   import tailwindcss from '@tailwindcss/vite'
   ```
3. Update the plugins array so Tailwind runs alongside React:
   ```javascript
   plugins: [
     react(),
     tailwindcss(),
   ]
   ```
4. Define the alias block in the same file so `@/` resolves to `src` (this relies on the `path` import above):
   ```javascript
   resolve: {
     alias: {
       '@': path.resolve(__dirname, './src'),
     },
   }
   ```

## Step 3: Setup Tailwind in CSS

Configure the main CSS file to import Tailwind:

1. Read existing `src/index.css`
2. Replace the entire contents with the Tailwind import:
   ```css
   @import "tailwindcss";
   ```

## Step 4: Apply Base Theme

Apply the base theme by running the bundled script from the project root directory at: `scripts/apply-theme.sh`

Apply the base theme by running the script from the skill's bundled resources at:`scripts/apply-theme.sh` within this skill's directory.

The script requires requires the frontend directory path (relative to project
  root) as an argument.

3. **Run the theme script from project root**:
   ```bash
   bash <path-to-skill>/scripts/apply-theme.sh frontend
   ```

The script appends shadcn/ui's design tokens (from `assets/tailwind-theme.css`, in the skill's bundled resources) to `src/index.css`, adding support for typography, colors, and automatic dark mode.


## Step 5: Setup shadcn/ui

### 5a. Install shadcn/ui Dependencies

Install the required packages for shadcn/ui component functionality:

```bash
npm --prefix ./frontend install class-variance-authority clsx tailwind-merge lucide-react
```

### 5b. Create jsconfig.json for Path Aliases

Create `jsconfig.json` in the frontend root directory:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### 5c. Create Utility Helper Function

Create `src/lib/utils.js`:

```javascript
import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}
```

### 5d. Create components.json Configuration

Create `components.json` in the frontend root directory:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": false,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/index.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
```

### 5e. Install shadcn/ui Components

**PREREQUISITE:** Before installing components, verify their availability and review usage patterns using the shadcn MCP server. This ensures compatibility with the current registry and helps understand proper implementation patterns.

**MCP Verification:**

Use the shadcn MCP tools to search for each component and confirm it exists in the registry:

- `mcp__shadcn__search_items_in_registries` with `registries=["@shadcn"]` and `query="card"`
- `mcp__shadcn__search_items_in_registries` with `registries=["@shadcn"]` and `query="button"`
- `mcp__shadcn__search_items_in_registries` with `registries=["@shadcn"]` and `query="navigation-menu"`
- `mcp__shadcn__search_items_in_registries` with `registries=["@shadcn"]` and `query="alert"`

**Install Required Components:**

Once verified, install the components using the shadcn CLI:

```bash
npx --prefix ./frontend shadcn@latest add card
npx --prefix ./frontend shadcn@latest add field
npx --prefix ./frontend shadcn@latest add input
npx --prefix ./frontend shadcn@latest add button
npx --prefix ./frontend shadcn@latest add table
npx --prefix ./frontend shadcn@latest add navigation-menu
npx --prefix ./frontend shadcn@latest add label
npx --prefix ./frontend shadcn@latest add separator
npx --prefix ./frontend shadcn@latest add alert
```

## Step 6: Implement Dark Mode with Toggle

### 6a. Configure Tailwind for Class-based Dark Mode

Create or update `tailwind.config.js` in the frontend root directory, to enable class-based dark mode:

```js
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
}
```

### 6b. Create Theme Context

Create `src/contexts/ThemeContext.jsx`:

```js
import { createContext, useContext, useEffect, useState } from "react";

const ThemeContext = createContext({
  theme: "system",
  setTheme: () => null,
});

export function ThemeProvider({ children, defaultTheme = "system", storageKey = "theme" }) {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem(storageKey) || defaultTheme;
  });

  useEffect(() => {
    const root = document.documentElement;

    root.classList.remove("dark");

    if (theme === "system") {
      const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
      if (systemTheme) {
        root.classList.add("dark");
      }
      return;
    }

    if (theme === "dark") {
      root.classList.add("dark");
    }
  }, [theme]);

  const value = {
    theme,
    setTheme: (newTheme) => {
      localStorage.setItem(storageKey, newTheme);
      setTheme(newTheme);
    },
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const context = useContext(ThemeContext);

  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }

  return context;
}
```

### 6c. Create Theme Toggle Button Component

Create `src/components/ThemeToggle.jsx`:

```js
import { Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useTheme } from "@/contexts/ThemeContext";

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    // If currently system or light, switch to dark
    // If currently dark, switch to light
    if (theme === "dark") {
      setTheme("light");
    } else {
      setTheme("dark");
    }
  };

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggleTheme}
      aria-label="Toggle theme"
      className="cursor-pointer"
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
    </Button>
  );
}
```

### 6d. Wrap App with ThemeProvider

Update `src/App.jsx` to include the ThemeProvider:

```js
import Router from "./router";
import { ThemeProvider } from "@/contexts/ThemeContext";

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="theme">
      <Router />
    </ThemeProvider>
  );
}

export default App;
```

### 6e. Add Theme Toggle to Navbar

Integrate the ThemeToggle component into the navigation bar:

1. **Locate the navbar component**: Find the main navigation component (commonly in `src/components/Navbar.jsx` or similar)
2. **Import the ThemeToggle component**:
   ```js
   import ThemeToggle from "@/components/ThemeToggle";
   ```
3. **Add the toggle to the navbar**: Place the `<ThemeToggle />` component in an appropriate location within the navbar, typically in the right section alongside other navigation items:
   ```jsx
   <nav className="flex items-center justify-between p-4">
     <div>{/* Logo and left-side nav items */}</div>
     <div className="flex items-center gap-4">
       {/* Other right-side nav items */}
       <ThemeToggle />
     </div>
   </nav>
   ```


## Step 7: Run Build to Check for Compilation Errors

Build the project to verify there are no compilation errors:

```bash
npm --prefix ./frontend run build
```

If the build succeeds, the setup is complete. If there are errors:
- Check for missing imports or incorrect file paths
- Verify all components were installed correctly
- Ensure `jsconfig.json` path aliases match `vite.config.js` aliases
- Confirm `tailwind.config.js` content paths include all component files

## Setup Complete

The Tailwind CSS and shadcn/ui setup is now complete. The project includes:
- Tailwind CSS with Vite integration
- shadcn/ui design tokens and theme variables
- Dark mode support with class-based switching
- Path aliases configured for clean imports (`@/components`, `@/lib`, etc.)
- Core shadcn/ui components installed and ready to use

