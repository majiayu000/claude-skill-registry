# Serverless functions (developer platform apps)

Summarized from the [serverless functions overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/overview) and related articles.

## Platform version

- **2026.03** developer platform apps: **full support** for deploying app serverless functions (replacing older limitations called out for e.g. **2025.1** in the overview doc).
- Treat older platform versions as **capability-unknown** until you read `app-hsmeta.json` / migration docs.

## Commercial / account requirements

- **Enterprise** subscription is required for a **customer account to install** an app that includes serverless functions.
- During development, use a **[developer test account](https://developers.hubspot.com/docs/getting-started/account-types#developer-test-accounts)** to build and test without Enterprise on the customer side.

## App serverless vs CMS serverless (doc comparison)

| Capability | 2026.03 app serverless | CMS serverless |
| --- | --- | --- |
| Private functions | Yes | No |
| Public endpoints | Yes (Content Hub Enterprise–related nuance in doc) | Yes |
| UI extension integration | Yes | No |
| Test-account support per doc table | Yes | No |
| NPM packages | Yes | Yes |

CMS serverless is documented under [CMS serverless functions](https://developers.hubspot.com/docs/cms/start-building/features/serverless-functions/getting-started-with-serverless-functions) — different product surface from app projects.

## Where to read next

- [Create serverless functions](https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/create-serverless-functions) — walkthrough including app card + function wiring.
- [Serverless function reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/reference) — structure, schema, limits.
- [Configurable test accounts](https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/developer-tooling/local-development/configurable-test-accounts) — local/serverless testing configuration.

## Upload validation gotchas

If **`hs project upload`** fails on `functions/*-hsmeta.json` with missing **`config.endpoint`** or complaints about **`method`** vs **`methods`**, see **`references/serverless-app-function-hsmeta.md`** and run **`hs project validate`**.
