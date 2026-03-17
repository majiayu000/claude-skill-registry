---
name: expo-gluestack
description: Comprehensive instructions for building Expo apps using gluestack-ui.
---

# Agent Skills: Building Beautiful Expo Apps with Gluestack UI

This document defines the skill set and operational guidelines for AI agents working on this project. The primary goal is to build high-quality, visually appealing mobile applications using **Expo** and **gluestack-ui**.

## 1. Technology Stack & Environment

- **Framework**: React Native (via Expo)
- **UI Library**: gluestack-ui
- **Language**: TypeScript (Preferred)
- **Navigation**: Expo Router (Standard for modern Expo apps)

## 2. Project Initialization Skills

When starting a new project or setting up the environment, the agent must follow these steps:

### A. Create Expo Project
Use the latest Expo template:
```bash
npx create-expo-app@latest my-app --template default
cd my-app
```

### B. Install gluestack-ui
Follow the official installation guide to integrate gluestack-ui:

1.  **Initialize gluestack-ui**:
    ```bash
    npx gluestack-ui init
    ```
    - This command installs dependencies and adds the `GluestackUIProvider`.
    - It sets up the theme configuration.
    - It creates a `components` folder for your UI components.

2.  **Wrap Application Root**:
    Ensure the root layout (e.g., `app/_layout.tsx` or `App.tsx`) is wrapped with the provider:
    ```tsx
    import { GluestackUIProvider } from "@/components/ui/gluestack-ui-provider";
    import "@/global.css"; // If using NativeWind or global styles

    export default function Layout() {
      return (
        <GluestackUIProvider>
          <Slot /> {/* or your main app content */}
        </GluestackUIProvider>
      );
    }
    ```

## 3. Component Management Skills

gluestack-ui is unstyled by default and headless, meaning you add components as you need them.

### A. Adding Components
**NEVER** try to import a component that hasn't been added to the project. Always check the `components/ui` directory first.

To add a new component (e.g., Button, Box, Text):
```bash
npx gluestack-ui add [component-name]
# Example:
npx gluestack-ui add button box text
```
*Agent Note: If a user asks for a UI element, identify the corresponding gluestack component, run the add command if it's missing, and then implement it.*

### B. Common Components & Usage
- **Layout**: Use `Box`, `VStack`, `HStack`, `Center` for layout instead of raw View styles.
  ```tsx
  <VStack space="md" reversed={false}>
    <Box className="w-20 h-20 bg-primary-500" />
  </VStack>
  ```
- **Typography**: Use `Text` and `Heading` with size props.
- **Interactivity**: Use `Button`, `Pressable`, `Link`.

## 4. UI/UX Design & Styling Skills

### A. Theming & Tokens
- Utilize the gluestack-ui tokens for spacing, colors, and typography to ensure consistency.
- Avoid hardcoded pixel values for margins/padding; use tokens (e.g., `$2`, `$4`, `md`, `lg`).

### B. Responsive Design
- gluestack-ui supports responsive props.
- Example: `<Box w="$full" md-w="$1/2">` (Full width on mobile, half width on medium screens/tablets).

### C. "Beautiful" UI Principles
- **Whitespace**: Use ample padding and margin (via `space` prop in stacks or padding props).
- **Hierarchy**: Use font weights and colors to establish visual hierarchy.
- **Feedback**: Ensure interactive elements have hover/pressed states (gluestack handles this by default, but customization is possible).

## 5. Advanced Development Patterns

### A. State Management
- **Global State**: Use **Zustand** for lightweight global state (e.g., user session, theme settings).
  - *Why*: Minimal boilerplate, easy to use with hooks.
- **Server State**: Use **TanStack Query (React Query)** for data fetching.
  - *Why*: Handles caching, loading states, and refetching automatically.

### B. Form Handling
- Use **React Hook Form** controlled by **Zod** schema validation.
  - *Why*: Performance (minimizes re-renders) and type safety.
  ```tsx
  import { useForm, Controller } from "react-hook-form";
  import { zodResolver } from "@hookform/resolvers/zod";
  // ... define z.object schema ...
  ```

### C. Iconography
- Use **Lucide Icons** (`lucide-react-native`).
- Gluestack-ui integrates well with Lucide.
  ```tsx
  import { Camera } from "lucide-react-native";
  import { Icon } from "@/components/ui/icon";
  // Usage: <Icon as={Camera} size="md" />
  ```

### D. Navigation (Expo Router)
- **Structure**:
  - `app/_layout.tsx`: Root provider setup (gluestack, query client).
  - `app/(tabs)`: For tab-based navigation.
  - `app/[id].tsx`: For dynamic routes.
- **Linking**: Use `Link` from `expo-router` for web-compatible navigation.

## 6. Coding Best Practices for Agents

1.  **File Structure**:
    - Keep screens in `app/` (if using Expo Router).
    - Keep reusable UI components in `components/`.
    - Keep business logic/hooks in `hooks/` or `utils/`.

2.  **Code Style**:
    - Use functional components.
    - Use Hooks (`useState`, `useEffect`) appropriately.
    - **Type Safety**: strict TypeScript usage. Define interfaces for props.

3.  **Error Handling**:
    - When running commands (like `npx gluestack-ui add`), if they fail, analyze the error (e.g., missing peer dependencies) and fix it before proceeding.

4.  **Dependency Management**:
    - **Expo Compatibility First**: Always prioritize installing packages compatible with the latest Expo SDK.
    - Use `npx expo install [package-name]` instead of `npm install` or `yarn add` when possible, as this ensures the installed version is compatible with the project's Expo SDK version.

## 7. Workflow Checklist

When assigned a task to build a screen:
1.  [ ] Analyze requirements.
2.  [ ] Identify necessary UI components (e.g., Card, Avatar, Button).
3.  [ ] Check if components exist in `components/ui`; if not, run `npx gluestack-ui add ...`.
4.  [ ] Scaffold the screen using `VStack`/`HStack` for layout.
5.  [ ] Apply styling using theme tokens.
6.  [ ] Verify responsiveness.

## 8. External Agent Skills & Resources

To enhance capability, the agent should leverage established skill sets from industry leaders:

### A. React Native Best Practices (Callstack)
- **Repository**: [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills)
- **Focus**: Performance optimization (re-renders, startup time), bundling, and native modules.
- **Instruction**: Consult these skills when optimizing app performance or debugging complex native issues.

### B. Expo Official Skills
- **Repository**: [expo/skills](https://github.com/expo/skills)
- **Focus**: Best practices for building, deploying (EAS), and upgrading Expo applications.
- **Instruction**: Use these skills for:
    - `upgrading-expo`: When moving between Expo SDK versions.
    - `expo-deployment`: For setting up EAS Build and Submit.
    - `expo-app-design`: General Expo app architecture guidance.
