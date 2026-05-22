---
name: shadcn-component
description: Add shadcn/ui components to this project. Use when user mentions "add component", "install shadcn", "need a dialog/button/card", or references ui.shadcn.com.
---

# Adding shadcn/ui Components

This project uses shadcn/ui with the following configuration (from `components.json`):
- Style: New York
- Base color: Neutral
- CSS variables: enabled
- Tailwind config: `tailwind.config.ts`
- Components path: `components/ui`
- Utils path: `lib/utils`

## Instructions

1. **Install component using npx**:
   ```bash
   npx shadcn@latest add <component-name>
   ```
   Common components: button, card, dialog, dropdown-menu, input, label, badge, alert, separator, scroll-area, sheet, skeleton, tooltip, tabs, switch, select, popover, progress, slider, accordion, avatar, checkbox, toast

2. **Component will be created at**: `components/ui/<component-name>.tsx`

3. **Import pattern** (follow existing style in `app/page.tsx`):
   ```tsx
   import { Button } from '@/components/ui/button';
   import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
   ```

4. **For toast notifications**, this project uses Sonner (not shadcn toast):
   ```tsx
   import { toast } from 'sonner';
   toast.success('Message here');
   toast.error('Error message');
   toast.info('Info message');
   ```

## Project Styling Conventions

- Glass-morphism: `className="glass-card"` (defined in globals.css)
- Button interactions: `className="btn-press"` for press animation
- Card hover: `className="card-hover"` for lift effect
- Gradients: `bg-gradient-to-r from-slate-700 to-slate-600`
- Backdrop blur: `backdrop-blur-xl` or `backdrop-blur`

## Examples

- "Add a tabs component" → `npx shadcn@latest add tabs`
- "I need a modal" → `npx shadcn@latest add dialog`
- "Add progress bar" → `npx shadcn@latest add progress`

## Guardrails

- Run `npx shadcn@latest add` (not manual creation) to ensure proper setup
- Check `components/ui/` for existing components before adding duplicates
- Sonner is already installed for toasts - don't add shadcn toast
- Confirm with user before running install command
