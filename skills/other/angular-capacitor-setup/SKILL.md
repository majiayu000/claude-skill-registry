---
name: angular-capacitor-setup
description: Add, repair, or validate Capacitor in Angular 20 workspaces with deterministic setup for dependency install, cap init, webDir resolution from angular.json, native platform add/open (android/ios), and build-plus-sync verification. Use when users ask to enable mobile builds, fix broken Capacitor wiring, or standardize Angular-to-native sync workflows.
---

# Angular 20 Capacitor Setup

## Goal

Set up or repair Capacitor in an Angular 20 workspace so web builds sync correctly to native Android/iOS projects and can be run from native tooling.

## Inputs

- `projectRoot` (string, default: current working directory)
- `projectName` (string, optional in multi-project workspaces)
- `platforms` (array, default: `['android']`; optional `ios`)
- `appId` (string, default: inferred or `com.example.app`)
- `appName` (string, default: project name)

## Success Criteria

- Capacitor packages are installed.
- `capacitor.config.ts` exists and uses the correct `webDir`.
- At least one native platform is added when requested.
- Angular build output can be copied/synced into native platforms.
- Native project opens/runs from Capacitor CLI commands.

## Workflow

1. Validate workspace and Angular version
- Confirm `package.json` and `angular.json` exist.
- Confirm `@angular/core` major version is `20`.
- Stop and report when workspace is not Angular 20.

2. Resolve target Angular project
- Read `angular.json` projects.
- Use explicit `projectName` when provided.
- If only one application project exists, use it automatically.
- If multiple app projects exist and none is given, ask for `projectName` before making changes.

3. Install Capacitor dependencies (idempotent)
- If `@capacitor/core` and `@capacitor/cli` already exist, keep installed versions unless user asked for an upgrade.
- Otherwise run:
```bash
npm install @capacitor/core @capacitor/cli
```
- Keep user-managed version pinning/lockfile behavior intact.

4. Initialize Capacitor config
- If `capacitor.config.ts` or `capacitor.config.json` does not exist, run:
```bash
npx cap init <appName> <appId>
```
- Prefer `capacitor.config.ts`.
- If config already exists, merge updates instead of replacing user settings.

5. Set correct `webDir` from Angular build config
- Inspect target project build output in `angular.json` and resolve the effective browser output folder.
- Set `webDir` to the directory containing built `index.html`.
- For Angular application builder this is commonly `<outputPath>/browser`; do not hardcode, use actual workspace config.

6. Add native platform projects
- For each requested platform, run:
```bash
npx cap add android
npx cap add ios
```
- Skip platforms already present.
- On Windows, note that `ios` build/open requires macOS/Xcode even if files can be configured in repo.

7. Build web app and sync native projects
- Build the selected Angular app first:
```bash
ng build <projectName>
```
- Sync web assets/plugins:
```bash
npx cap sync
```
- Use `npx cap copy` only when explicitly needing copy without plugin/native project update.

8. Add practical package scripts
- Add or verify scripts in `package.json`:
```json
{
  "build:cap": "ng build <projectName> && npx cap sync",
  "cap:sync": "npx cap sync",
  "cap:copy": "npx cap copy",
  "cap:update": "npx cap update",
  "cap:open:android": "npx cap open android",
  "cap:open:ios": "npx cap open ios"
}
```
- Keep existing user scripts unchanged when unrelated.

9. Verify end to end
- Confirm build output exists in configured `webDir`.
- Run `npx cap sync` with no critical errors.
- Open platform project:
```bash
npx cap open android
npx cap open ios
```
- For Android, verify app launches from Android Studio emulator/device.
- If local IDE launch is unavailable (for example CI/headless environment), mark launch verification as pending manual verification.

10. Report deterministic completion output
- Include:
- selected `projectName`
- configured `webDir`
- platforms added or skipped
- commands run for build/sync/open
- verification result and any pending manual checks

## Troubleshooting Rules

1. `cap sync` fails because `webDir` not found
- Re-check Angular `outputPath` and fix `capacitor.config.ts` `webDir`.
- Rebuild Angular before syncing.

2. Native plugin changes not reflected
- Run `npx cap sync` (or `npx cap update` when native platform deps changed).
- Re-open native IDE project after sync.

3. Android build fails after adding platform
- Ensure Android SDK/JDK requirements are installed.
- Re-run `npx cap doctor` and fix reported environment issues.

4. iOS commands fail on non-macOS
- Explain iOS build/open requires macOS with Xcode.
- Keep iOS setup optional on Windows/Linux.

## Guardrails

- Always build Angular before `cap sync`.
- Always derive `webDir` from actual project config, never hardcode blindly.
- Preserve existing Capacitor config keys (`plugins`, server options, etc.) during edits.
- Avoid deleting/recreating native platform folders unless user explicitly asks.
- Do not run `npx cap add` for platforms that are already added.

## Definition of Done

- Capacitor is installed and initialized.
- `capacitor.config.ts` points to the real Angular build output directory.
- Requested native platform(s) are added and synced.
- CLI open/run workflow is verifiably usable.

## References

[1]: https://capacitorjs.com/docs/config
[2]: https://capacitorjs.com/docs/cli/commands/add
[3]: https://capacitorjs.com/docs/cli/commands/sync
[4]: https://capacitorjs.com/docs/cli/commands/open
[5]: https://angular.dev/reference/configs/workspace-config
