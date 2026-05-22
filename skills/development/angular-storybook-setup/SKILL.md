---
name: angular-storybook-setup
description: Install, repair, or verify Storybook in Angular 20 applications that already use Tailwind CSS, including required addons (`@storybook/addon-themes`, `@storybook/addon-designs`, `@storybook/addon-a11y`) and optional Chromatic setup. Use when users ask to add Storybook, make Tailwind styles visible in stories, enable theme/design/a11y panels, fix broken Storybook config, or validate setup end to end.
---

# Angular 20 Storybook Tailwind Addons

## Goal

Install, repair, or verify Storybook for Angular 20 + Tailwind projects. Ensure stories render with the app's global Tailwind styles and that themes, designs, and a11y addons are configured. Optionally set up Chromatic CLI when explicitly requested.

## Inputs

- `projectRoot` (string, default: current working directory)
- `globalStylePath` (string, default: auto-detect from `angular.json` styles list; fallback `src/styles.css` then `src/styles.scss`)
- `installChromaticCli` (boolean, default: `false`, install only on explicit request)
- `runVerification` (boolean, default: `true`)

## Preconditions

- `angular.json` exists in `projectRoot`.
- The project already has Tailwind configured in a global stylesheet. If not, use $angular-tailwind-setup to install and configure Tailwind CSS.
- Use the repo package manager; examples below use `npm`.

## Success Criteria

- Storybook is installed and `npm run storybook` starts.
- `.storybook/preview.ts` imports the global stylesheet used by the Angular app.
- `.storybook/main.ts` includes all required addons:
  - `@storybook/addon-a11y`
  - `@storybook/addon-themes`
  - `@storybook/addon-designs`
- Theme switching works with class-based Tailwind dark mode.
- At least one story shows a `parameters.design` example.
- If `installChromaticCli=true`, `chromatic` can be invoked from `npm run chromatic`.

## Workflow

1. Validate workspace and detect versions
   - Read `package.json` and confirm Angular major version (`@angular/core`) is close to `20`.
   - Abort with an error if major is not exactly `20`.
   - Detect Storybook version if already installed (for addon compatibility checks).
   - Resolve the global style file from `angular.json > build.options.styles`; fallback to `src/styles.css` or `src/styles.scss`.

2. Install Storybook (Angular preset)
   - Run from `projectRoot`:

   ```bash
   npx storybook@latest init
   ```

   - Keep Angular framework defaults from the installer.
   - Ensure `.storybook/main.ts` and `.storybook/preview.ts` were created.
   - Run once after installation:

   ```bash
   npm run storybook
   ```

3. Install required addons

   ```bash
   npm i -D @storybook/addon-themes @storybook/addon-designs @storybook/addon-a11y
   ```

   - Check `@storybook/addon-designs` compatibility with the installed Storybook major.
   - If needed, pin `@storybook/addon-designs` to the matching major range.
   - If `installChromaticCli=true`, run:

   ```bash
   npm i -D chromatic
   ```

4. Configure `.storybook/main.ts`
   - Ensure `framework.name` is `@storybook/angular`.
   - Ensure `stories` includes both MDX and stories globs.
   - Ensure `addons` includes all required addons exactly once.
   - Merge with existing config instead of destructive overwrite.

   ```ts
   import type { StorybookConfig } from '@storybook/angular';

   const config: StorybookConfig = {
     framework: {
       name: '@storybook/angular',
       options: {},
     },
     stories: ['../src/**/*.mdx', '../src/**/*.stories.@(ts|tsx)'],
     addons: [
       '@storybook/addon-a11y',
       '@storybook/addon-themes',
       '@storybook/addon-designs',
     ],
   };

   export default config;
   ```

5. Configure `.storybook/preview.ts`
   - Import the Angular global stylesheet used by Tailwind.
   - Add themes decorator for class-based switching (`light` -> empty class, `dark` -> `dark` class).
   - Keep existing parameters and decorators when present.

   ```ts
   import '../src/styles.css';
   import type { Preview } from '@storybook/angular';
   import { withThemeByClassName } from '@storybook/addon-themes';

   const preview: Preview = {
     decorators: [
       withThemeByClassName({
         themes: { light: '', dark: 'dark' },
         defaultTheme: 'light',
       }),
     ],
   };

   export default preview;
   ```

   - Use `styles.scss` import when the project global style file is SCSS.

6. Add a minimal design-panel example
   - Add or update a story with `parameters.design` so the Designs panel is visible.

   ```ts
   export const Primary = {
     args: { label: 'Button' },
     parameters: {
       design: {
         type: 'figma',
         url: 'https://www.figma.com/file/XXXX/YourFile?node-id=123-456',
       },
     },
   };
   ```

7. Verify
   - Run `npm run storybook` and confirm no startup errors.
   - Confirm Tailwind classes render in stories.
   - Confirm A11y panel appears in Storybook UI.
   - Confirm theme switcher toggles classes on the preview root.
   - Confirm Design panel appears for stories with `parameters.design`.
   - If `installChromaticCli=true`, run `npm run chromatic -- --help` and confirm CLI is available.

## Guardrails

- Do not replace existing Storybook config wholesale; merge settings safely.
- Do not assume `src/styles.css`; detect and import the actual configured global style file.
- Keep addon entries unique; avoid duplicate addon registrations.
- If Tailwind styles are not visible, check style import path first, then verify Tailwind directives in the imported file.
- Do not install Chromatic unless explicitly requested.
