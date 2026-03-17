---
name: react-new-project
description: Create a new React project using Vite, TypeScript, and Feature-based architecture.
---

# React + Vite + TypeScript Project Generator

This skill guides the creation of a modern React application using Vite and organizes it into a scalable feature-based architecture.

## Prerequisite

- Node.js and npm installed

## Directory Structure (Feature-Based)

The goal is to move away from purely technical folders (`components`, `hooks`) to domain-oriented folders (`features`).

```
project-name/
├── src/
│   ├── app/                # Global app setup (providers, router, store)
│   ├── features/           # Feature-based modules
│   │   ├── auth/           # Example feature
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── types/
│   │   └── dashboard/
│   ├── shared/             # Shared utilities and UI components
│   │   ├── ui/             # Generic UI components (Buttons, Inputs)
│   │   └── utils/          # Helper functions
│   ├── App.tsx
│   └── main.tsx
└── ... config files
```

## Step-by-Step Instructions

### 1. Initialize Vite Project

```bash
# Create project using the React-TypeScript template
npm create vite@latest __PROJECT_NAME__ -- --template react-ts

cd __PROJECT_NAME__
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Setup Folder Structure

Remove default boilerplate and create the architecture:

```bash
# Clean up default assets if desired (optional)
# rm src/assets/react.svg

# Create core directories
mkdir -p src/app
mkdir -p src/features
mkdir -p src/shared/ui
mkdir -p src/shared/utils
mkdir -p src/shared/hooks
```

### 4. Basic Configuration

- Ensure `vite.config.ts` is set up (defaults are usually fine).
- Recommend setting up path aliases (e.g., `@/` pointing to `src/`) in `tsconfig.json` and `vite.config.ts` if the user agrees, but start with standard relative paths for simplicity unless requested.

## Verification

Run the dev server to ensure it starts:

```bash
npm run dev
```


## Parent Hub
- [_frontend-mastery](../_frontend-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
