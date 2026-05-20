---
name: angular-json-server-setup
description: Add, repair, or verify a local json-server mock REST API for Angular 20 workspaces, including deterministic dependency setup, `mocks/db.json`, proxy wiring (`src/proxy.conf.json` + `angular.json`), npm scripts, and mock API docs. Use when users ask to create/fix `/api` proxy flows, run Angular+API together, troubleshoot json-server option/version mismatches, or add advanced middleware/routes/auth simulation.
---

# Angular 20 json-server Setup

## Goal

Provide a repeatable, repo-friendly setup for a local mock REST API using `json-server`, integrated with Angular 20 development (`ng serve`, proxy, scripts, and a sane folder layout).

## Recommended Layout

Create this structure at repo root:

```text
/
  mocks/
    db.json
    README.md
  src/
    proxy.conf.json
  package.json
  angular.json
```

## Inputs

- `projectRoot` (string, default: current working directory)
- `apiPort` (number, default: `3000`)
- `apiPrefix` (string, default: `/api`)
- `useConcurrently` (boolean, default: `true`)
- `addAdvancedServerTemplate` (boolean, default: `false`)
- `packageManager` (string, default: auto-detect from lockfile: `npm` | `pnpm` | `yarn`)

## Success Criteria

- `json-server` is installed as a dev dependency.
- `mocks/db.json` exists and serves resources.
- `src/proxy.conf.json` exists and rewrites `/api/*` to the mock API origin.
- `angular.json` serve options include `proxyConfig: "src/proxy.conf.json"`.
- `npm run start:mock` starts Angular and mock API together.
- Angular uses relative `/api/...` calls instead of hardcoded `localhost` URLs.

## Workflow

1. Preflight and workspace validation
   - Resolve `projectRoot` to an absolute path.
   - Detect package manager from lockfile:
   - `pnpm-lock.yaml` -> `pnpm`
   - `yarn.lock` -> `yarn`
   - otherwise -> `npm`
   - Confirm `angular.json` and `package.json` exist in `projectRoot`.
   - Confirm `@angular/core` major version is `20`.
   - Abort with an error when the project is not Angular 20.
   - If monorepo/multi-project, apply proxy and serve updates to the actively used Angular app target; do not modify unrelated targets.

2. Install dependencies
   - Install `json-server` as a dev dependency using detected package manager:
   ```bash
   npm i -D json-server
   ```
   - If `useConcurrently` is true, install `concurrently` as a dev dependency:
   ```bash
   npm i -D concurrently
   ```
   - Keep installs local; do not require global packages.
   - Do not downgrade or remove unrelated dependency entries.

3. Create `mocks/db.json`
   - Ensure `mocks/` exists.
   - Create `mocks/db.json` with valid JSON when missing.
   - If it already exists, preserve existing data.
   - Prefer this minimal seed when no domain data is provided:
   ```json
   {}
   ```

4. Add npm scripts in `package.json`
   - Ensure these scripts exist (merge safely with existing scripts):
   ```json
   {
     "scripts": {
       "mock:api": "json-server ./mocks/db.json --port 3000",
       "start": "ng serve",
       "start:mock": "concurrently -n API,NG \"npm:mock:api\" \"npm:start\""
     }
   }
   ```
   - If `useConcurrently` is false, set `start:mock` to only run the API script:
   ```json
   {
     "scripts": {
       "start:mock": "npm run mock:api"
     }
   }
   ```
   - Preserve script names unless the user asks otherwise.
   - Update scripts idempotently:
   - create missing keys
   - replace only targeted script values
   - never remove unrelated scripts

5. Configure Angular proxy
   - Create or update `src/proxy.conf.json`:
   ```json
   {
     "/api": {
       "target": "http://localhost:3000",
       "secure": false,
       "changeOrigin": true,
       "logLevel": "debug",
       "pathRewrite": {
         "^/api": ""
       }
     }
   }
   ```
   - If `apiPrefix` differs from `/api`, update both the top-level key and `pathRewrite` consistently.
   - In `angular.json`, set `proxyConfig` under the active serve target:
   - preferred path: `projects.<name>.architect.serve.options.proxyConfig`
   - alternate path in newer builders: `projects.<name>.targets.serve.options.proxyConfig`
   - Do not delete existing serve options when inserting `proxyConfig`.
   ```json
   {
     "proxyConfig": "src/proxy.conf.json"
   }
   ```

6. Apply Angular usage pattern
   - Prefer environment-based API base URL in development.
   - Set `apiBaseUrl: '/api'` in `environment.development.ts`.
   - Build service URLs as `${environment.apiBaseUrl}/resource`.
   - Do not hardcode `http://localhost:3000` in app code.

7. Add mock API docs
   - Create `mocks/README.md` with:
   - endpoint list
   - run commands (`npm run mock:api`, `npm run start:mock`)
   - sample curl commands
   - reset instructions (edit or replace `mocks/db.json`)
   - Include one troubleshooting section for common errors:
   - `Unknown option` from `json-server`
   - proxy not applied due to wrong serve target
   - hardcoded backend URLs bypassing `/api`

8. Verify setup
   - Run:
   ```bash
   npm run start:mock
   ```
   - Verify process behavior:
   - API listens on `apiPort`
   - Angular serve starts successfully
   - Verify integration behavior:
   - Angular app can call `${apiPrefix}/...` without CORS errors
   - resources in `mocks/db.json` map to endpoints
   - proxy rewrite removes `apiPrefix` before reaching json-server
   - Verify code hygiene:
   - no hardcoded `http://localhost:<apiPort>` in Angular data services
   - if found, convert calls to relative `${apiPrefix}` base URLs

## Advanced Rules (Version-Sensitive)

1. Handle v1 differences explicitly
   - Recent `json-server` versions in the v1 beta line differ from v0.17.
   - Expect changes including:
   - ID handling differences (string-like IDs in many scenarios)
   - pagination via `_page` + `_per_page`
   - removed delay flag behavior

2. Avoid relying on removed/changed CLI flags
   - Do not assume `--delay` works in newer versions.
   - Do not assume `--routes` and `--middlewares` flags are available across versions.
   - If users report `Unknown option`, treat it as version/line mismatch first.

3. Prefer module-based wrapper for advanced behavior
   - For auth simulation, custom routes, custom middleware, artificial latency, or reset endpoints:
   - create a small Node wrapper (`server.js` or `mocks/server.js`) using `json-server` as a module
   - attach custom middleware and route handlers before delegating to the router
   - keep this optional and enabled only when requested

## Guardrails

- Merge JSON changes safely; do not overwrite unrelated config.
- Keep edits idempotent; running this skill multiple times should converge to the same working state.
- Keep API URLs in Angular app relative (`/api/...`).
- Keep `mocks/db.json` committed for reproducibility.
- Prefer small, explicit defaults over broad scaffolding.
- If conflicting existing conventions are present, preserve them unless they break success criteria.

## Assistant Portability Rules

- Drive edits from on-disk config and lockfiles; do not assume a package manager or Angular target without checking.
- Keep script/proxy mutations idempotent and narrowly scoped to required keys.
- If active serve target resolution is ambiguous, stop with one explicit blocker and required target path.

## Definition of Done

- `npm run start:mock` launches Angular + mock API.
- Angular calls to `/api/...` succeed through proxy without CORS issues.
- Endpoints are generated from `mocks/db.json`.
- Mock API run/reset/extension steps are documented in `mocks/README.md`.
- Re-running setup does not corrupt scripts or Angular serve configuration.

## References

[1]: https://github.com/typicode/json-server#readme
[2]: https://angular.dev/tools/cli/serve
[3]: https://angular.dev/tools/cli/environments
[4]: https://docs.npmjs.com/cli/v10/commands/npm-install
