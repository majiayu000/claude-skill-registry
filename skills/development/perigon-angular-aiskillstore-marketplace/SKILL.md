---
name: perigon-angular
description: Angular 21+ standalone/Material/signal conventions for Perigon WebApp
---
## When to use
- Frontend work in src/ClientApp/WebApp (components, routes, services, styles, i18n).

## Usage
- Layout: entry main.ts; app config in app/app.config.ts; routes in app/app.routes.ts; layout shell in app/layout/*; pages under app/pages/*; shared UI in app/share/components; pipes in app/share/pipe; guards in app/share/auth.guard.ts.
- Components: standalone only; avoid NgModules. Use Angular Material; theming in styles.scss/theme.scss/vars.scss; keep page styles alongside each *.scss.
- State/forms: prefer signals and signal forms; avoid legacy two-way binding when signals suffice.
- Services/API: HTTP clients/types in app/services (admin-client, base.service, models/services); keep customer-http.interceptor active; honor proxy.conf.json; use environments/environment*.ts for endpoints/config.
- i18n: strings live in assets/i18n/*.json; align keys with app/share/i18n-keys.ts and scripts/i18n-keys.js.
- UX/auth: reuse layout/navigation components; auth via auth.service + auth.guard; paginator intl in share/custom-paginator-intl.ts.
- Tooling: use pnpm; avoid builds/tests unless requested. Keep ESLint/tsconfig defaults; prefer standalone Material imports over deprecated modules.
