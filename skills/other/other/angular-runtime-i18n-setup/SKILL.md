---
name: angular-runtime-i18n-setup
description: Add or repair runtime localization in Angular 20 applications with a minimal setup using `@ngx-translate/core` and JSON locale files. Use when a user asks for runtime language switching without rebuilding, wants a language toggle UI, needs fallback/default language behavior, needs persisted language selection, or needs troubleshooting for runtime i18n loading.
---

# Angular 20 Runtime Localization Setup

## Goal

Implement runtime translation switching in Angular 20 with the simplest maintainable setup and minimal ceremony.

## Inputs

- `projectRoot` (string, default: current working directory)
- `defaultLang` (string, default: `en`; English is the primary/default language)
- `supportedLangs` (string array, default: `['en', 'de']`; German is the secondary language)
- `translationPath` (string, default: `public/i18n`)
- `persistSelection` (boolean, default: `true`)

## Decision Rule

- Use Angular built-in i18n only for compile-time localization builds.
- Use `@ngx-translate/core` for runtime language switching in one build artifact.
- Use standalone-first configuration unless the project is already NgModule-based.

## Workflow

### 1) Validate the Angular workspace

- Confirm `angular.json` and `package.json` exist in `projectRoot`.
- Confirm `@angular/core` major version is `20`.
- Detect whether the app is standalone-first (`src/app/app.config.ts`) or NgModule-based (`src/app/app.module.ts`) and follow the matching configuration path.
- If multiple Angular projects exist, target the default app project from `angular.json`; otherwise stop and request an explicit project selection.
- Stop and report an error when the workspace is not Angular 20.

### 2) Install runtime i18n dependencies

Run from `projectRoot`:

```bash
npm i @ngx-translate/core @ngx-translate/http-loader
```

- If dependencies already exist, do not reinstall unless versions are broken or missing.

### 3) Create locale JSON files

- Ensure `public/i18n` exists.
- Create at least two files:
  - `public/i18n/en.json` (primary/default)
  - `public/i18n/de.json` (secondary)
- Start with stable dot-notation keys.

Example `public/i18n/en.json`:

```json
{
  "app.title": "My App",
  "nav.home": "Home",
  "settings.language": "Language"
}
```

Example `public/i18n/de.json`:

```json
{
  "app.title": "Meine App",
  "nav.home": "Startseite",
  "settings.language": "Sprache"
}
```

### 4) Configure `app.config.ts`

- Ensure `provideHttpClient()` exists.
- Add `provideTranslateService(...)`.
- Configure `provideTranslateHttpLoader(...)` with `prefix: '/i18n/'` and `suffix: '.json'`.
- Set both `lang` and `fallbackLang` to `defaultLang` initially.

```ts
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { provideTranslateService } from '@ngx-translate/core';
import { provideTranslateHttpLoader } from '@ngx-translate/http-loader';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    provideTranslateService({
      lang: 'en',
      fallbackLang: 'en',
      loader: provideTranslateHttpLoader({
        prefix: '/i18n/',
        suffix: '.json',
      }),
    }),
  ],
};
```

NgModule fallback (only when the project is module-based):

- Keep runtime i18n provider setup equivalent to standalone configuration.
- Ensure `TranslateModule` is available to components that use `| translate`.
- Do not mix deprecated setup styles with modern provider patterns unless required by existing project constraints.

### 5) Add a lightweight language service

Create `src/app/core/i18n/language.service.ts` and wrap runtime language state behind a small API.

Requirements:

- Expose selected language as a signal.
- Validate language changes against `supportedLangs`.
- Call `translate.use(lang)` on every switch.
- Persist language to `localStorage` when `persistSelection` is `true`.
- Update `document.documentElement.lang` on switch.
- Guard browser-only APIs (`localStorage`, `document`) for SSR/hydration-safe behavior.

```ts
import { Injectable, inject, signal } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

type SupportedLanguage = 'en' | 'de';

@Injectable({ providedIn: 'root' })
export class LanguageService {
  private readonly translate = inject(TranslateService);
  private readonly storageKey = 'app.lang';
  readonly supported = ['en', 'de'] as const;
  readonly current = signal<SupportedLanguage>('en');

  init(): void {
    const saved = localStorage.getItem(this.storageKey);
    const browser = this.translate.getBrowserLang();
    const initial = this.isSupported(saved)
      ? saved
      : this.isSupported(browser)
        ? browser
        : 'en';

    this.set(initial);
  }

  set(lang: SupportedLanguage): void {
    this.translate.use(lang);
    this.current.set(lang);
    localStorage.setItem(this.storageKey, lang);
    document.documentElement.lang = lang;
  }

  private isSupported(value: string | null | undefined): value is SupportedLanguage {
    return !!value && (this.supported as readonly string[]).includes(value);
  }
}
```

### 6) Initialize language at app startup

- Call `languageService.init()` once in the root startup path.
- Keep initialization idempotent.

Example in root component:

```ts
import { Component, inject } from '@angular/core';
import { LanguageService } from './core/i18n/language.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
})
export class AppComponent {
  readonly language = inject(LanguageService);

  constructor() {
    this.language.init();
  }
}
```

### 7) Add runtime language switcher UI

- Add a select or button group.
- Bind value to `language.current()`.
- Route all text through `TranslatePipe` and ensure the pipe is imported in standalone components.

```html
<label for="language">{{ 'settings.language' | translate }}</label>
<select id="language" [value]="language.current()" (change)="language.set($any($event.target).value)">
  <option value="en">English</option>
  <option value="de">Deutsch</option>
</select>

<h1>{{ 'app.title' | translate }}</h1>
```

### 8) Verify behavior

Run:

```bash
npm run build
```

Then verify:

- Initial language resolves as expected.
- Switching language updates text immediately without reload.
- Selected language persists after refresh.
- Missing keys fall back to `defaultLang`.
- Translation files are fetched from `/<translationPath>/<lang>.json` with successful network responses.
- `document.documentElement.lang` updates when language changes (browser runtime).

## Guardrails

- Do not mix compile-time Angular i18n workflow with runtime-switch requirements.
- Do not hardcode user-facing copy after runtime i18n setup.
- Keep translation keys stable across all locale files.
- Keep `supportedLangs` and locale files in sync.
- Guard browser-only APIs (`localStorage`, `document`) when the app uses SSR.

## Troubleshooting

- If translations do not load, inspect `/i18n/<lang>.json` network requests.
- If text shows keys, confirm `TranslatePipe` is imported in standalone components.
- If switching does not apply, confirm `TranslateService.use(...)` is called.
- If initial language is wrong, confirm `init()` runs during root startup.

## Success Output Contract

Return a concise report containing:

- Targeted project and detected app style (standalone or NgModule).
- Files created/changed.
- Verification status:
  - `build`: pass/fail
  - `runtime-switch`: pass/fail/manual
  - `persistence`: pass/fail/manual
  - `fallback`: pass/fail/manual
- Any deferred manual checks (for non-browser or CI environments).

## References

- Angular i18n guide: https://angular.dev/guide/i18n
- ngx-translate docs: https://ngx-translate.org/
- ngx-translate configuration: https://ngx-translate.org/reference/configuration/
- ngx-translate NgModules support: https://ngx-translate.org/reference/ngmodules/
- ngx-translate TranslateService API: https://ngx-translate.org/reference/translate-service-api/
