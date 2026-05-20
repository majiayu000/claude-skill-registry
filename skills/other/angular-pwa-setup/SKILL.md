---
name: angular-pwa-setup
description: Add, repair, or validate Angular 20 Progressive Web App support with `@angular/pwa`, including deterministic `ng add` execution, service-worker registration verification, manifest/icon checks, production-build artifact validation, and manual install/offline checks. Use when users ask to set up PWA, fix broken service workers, troubleshoot installability/offline behavior, or review `ngsw-config.json`/`manifest.webmanifest`.
---

# Angular 20 PWA Setup

## Goal

Set up or repair Angular 20 PWA support with `@angular/pwa` so the app has a valid manifest, service worker registration, generated icons, and verifiable install/offline behavior from a production build.

## Inputs

- `projectRoot` (string, default: current working directory)
- `projectName` (string, optional in multi-project workspaces)
- `registrationStrategy` (string, default: `registerWhenStable:30000`)
- `enabledInDev` (boolean, default: `false`)
- `verifyRuntime` (boolean, default: `true`)

## Success Criteria

- `@angular/pwa` is installed in dependencies.
- PWA scaffolding exists (`manifest.webmanifest`, icons, `ngsw-config.json`).
- Angular registers `ngsw-worker.js` correctly.
- Build output includes service worker artifacts (`ngsw.json`, worker files).
- App passes basic manual checks for installability and offline behavior.

## Workflow

1. Validate workspace and Angular version
- Confirm `package.json` and `angular.json` exist.
- Confirm `@angular/core` major version is `20`.
- Stop and report when the workspace is not Angular 20.

2. Resolve target Angular project
- Read `angular.json` projects.
- Use explicit `projectName` when provided.
- If only one application project exists, use it automatically.
- If multiple app projects exist and no target is given, ask for the project name.

3. Apply official PWA integration
- Run the schematic non-interactively:
```bash
ng add @angular/pwa --project <projectName> --skip-confirmation
```
- Keep generated files unless the user explicitly requests customization.

4. Verify generated/updated files
- Confirm presence of:
- `<projectRoot>/ngsw-config.json`
- `<sourceRoot>/manifest.webmanifest`
- icon assets in `<sourceRoot>/icons` or configured public assets path
- `<link rel="manifest" href="manifest.webmanifest">` in `<sourceRoot>/index.html`
- `theme-color` meta tag in `<sourceRoot>/index.html`

5. Verify service worker registration wiring
- For standalone bootstrap (preferred in Angular 20), ensure provider exists in `src/app/app.config.ts`:
```ts
provideServiceWorker('ngsw-worker.js', {
  enabled: !isDevMode(),
  registrationStrategy: 'registerWhenStable:30000'
})
```
- For NgModule-based apps, ensure equivalent `ServiceWorkerModule.register(...)` wiring exists.
- Keep production-safe default behavior: enabled only outside dev mode unless `enabledInDev=true`.
- If `registrationStrategy` input is provided, verify registration uses that exact value.

6. Build and confirm artifacts
- Run project build for the selected app:
```bash
ng build <projectName>
```
- Confirm service-worker artifacts are present in output (for example `ngsw.json` and `ngsw-worker.js`).

7. Verify runtime behavior over HTTP server
- If `verifyRuntime=true`, serve the production output from a static server (not `file://`).
- Open in Chrome and verify:
- Application tab shows active service worker
- Manifest is detected and installable
- Offline toggle still loads cached app shell/routes

8. Apply minimal, safe customizations when requested
- Only customize `ngsw-config.json` when user asks for explicit asset/data caching behavior.
- Keep broad defaults first, then add targeted `assetGroups`/`dataGroups` rules.
- Avoid overcaching API calls unless TTL/versioning strategy is defined.

9. Report deterministic completion output
- Include:
- selected `projectName`
- files created or changed
- registration wiring location (`app.config.ts` or module file)
- build command run and artifact paths found
- runtime verification result (or reason skipped)

## Troubleshooting Rules

1. `ng add` fails
- Confirm Angular CLI and workspace dependencies are consistent.
- Re-run with explicit `--project` in multi-project repos.

2. Service worker never activates
- Confirm app is served from built output via HTTP(S), not `ng serve` in normal dev mode.
- Confirm registration code exists and `enabled` evaluates to `true` in production.

3. Offline mode does not work
- Confirm `ngsw.json` exists in build output.
- Inspect `ngsw-config.json` patterns and ensure the tested routes/assets are covered.

4. App not installable
- Confirm manifest fields/icons are valid and reachable.
- Confirm HTTPS (or localhost), and no critical PWA warnings in DevTools.

## Guardrails

- Prefer schematic-generated defaults before manual edits.
- Merge config changes; do not overwrite unrelated workspace settings.
- Keep environment-aware service worker enablement (`!isDevMode()`) by default.
- Validate with a real production build before declaring success.
- If runtime verification cannot be executed (for example CI-only environment), explicitly mark as pending manual verification.

## Definition of Done

- `ng add @angular/pwa` has been applied successfully for the target app.
- Manifest, icons, and service worker registration are present and valid.
- Production build emits service worker artifacts.
- Installability and basic offline behavior are verified.

## References

[1]: https://angular.dev/ecosystem/service-workers/getting-started
[2]: https://angular.dev/ecosystem/service-workers/devops
[3]: https://angular.dev/cli/add
[4]: https://www.npmjs.com/package/@angular/pwa
