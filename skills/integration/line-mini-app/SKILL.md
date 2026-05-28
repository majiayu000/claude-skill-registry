---
name: line-mini-app
description: Comprehensive reference for LINE MINI App — Service Messages, Common Profile Quick Fill, In-App Purchase, Console setup (3 internal channels), submission review, and performance guidelines for web apps running inside LINE as an enhanced LIFF platform. This skill should be used when the user asks to "build a LINE MINI App", "send a service message", "set up Common Profile Quick Fill", "implement in-app purchase", "configure MINI App Console", "submit MINI App for review", or mentions LINE MINI App, Service Messages, notification token, Common Profile, IAP purchase flow, 3 internal channels, consent simplification, Custom Path, custom share messages, or verified vs unverified MINI App. Always use this skill whenever the user mentions LINE MINI App, mini apps in LINE, or enhanced LIFF features like service messages or in-app purchase, even if they don't explicitly say "MINI App".
---

# LINE MINI App

**Do not answer LINE MINI App questions from memory — LINE updates APIs frequently and training data is unreliable. Always consult the references below.**

LINE MINI App is a web app platform built on LIFF that runs inside LINE.

## Workflow

1. Read [references/guidelines.md](references/guidelines.md) first (policy rules, specs, constraints)
2. Load the relevant reference for the feature being worked on
3. For architecture or design choices, consult [references/experts.md](references/experts.md)
4. When reviewing, cross-check code against specs (token lifecycle, message limits, scope requirements, template naming, IAP order flow)

## Environment Variables

```
LIFF_ID=LIFF app ID (LINE MINI App runs on LIFF)
LINE_CHANNEL_ACCESS_TOKEN=Stateless channel access token (Service Messages, IAP)
LINE_LOGIN_CHANNEL_ID=LINE Login Channel ID (server-side verification)
LINE_LOGIN_CHANNEL_SECRET=Channel secret (server-side only)
```

## MINI App vs LIFF

| Feature | LIFF | MINI App |
|---------|------|----------|
| Service Messages | ✗ | ✅ Proactive notifications via notification token |
| Common Profile Quick Fill | ✗ | ✅ Auto-fill forms with LINE profile data |
| In-App Purchase | ✗ | ✅ App store payments (iOS/Android) |
| Submission review | Not required | Required (LINE review process) |
| Entry point | LIFF URL | LINE MINI App list + LIFF URL |

All LIFF APIs are available in MINI App context (LIFF browser). See Key Constraints for external browser limitations.

## Service Messages

```
User opens MINI App → liff.getAccessToken() → Issue notification token → Send service messages (max 5)
```

- Token validity: **1 year**, max **5 messages** per token
- LIFF access token is **revoked when user closes the MINI App** — issue notification token before user leaves

Full API specs, template structure, error codes → **[references/service-messages.md](references/service-messages.md)**

## Common Profile Quick Fill

```javascript
const result = await liff.$commonProfile.get(scopes, { formatOptions });
liff.$commonProfile.fill(result.data);  // auto-fill <input data-liff-autocomplete="...">
```

Full API specs, scopes, dummy data → **[references/common-profile.md](references/common-profile.md)**

## In-App Purchase

Japan only. Consumable digital content only. Requires LIFF SDK ≥ 2.26.0, LINE ≥ 15.6.0, LIFF browser.

Purchase flow (client + server), dev guidelines, error codes → **[references/in-app-purchase.md](references/in-app-purchase.md)**

## Key Constraints

- MINI App runs on LIFF — all LIFF constraints apply (Endpoint URL, init order, environment differences)
- Stateless channel access tokens only — long-lived and v2.1 tokens **cannot be used** for MINI App channels
- Channel consent simplification only skips `openid` — `profile`, `email`, `chat_message.write` require verification screen; needs LIFF SDK **v2.13.x+**, verified MINI App
- Custom share messages must use **Bubble** container (not Carousel); actions only on buttons and footer
- External browser: `liff.init()` doesn't auto-login (use `withLoginOnExternalBrowser: true`); `sendMessages`, `openWindow`, `closeWindow`, `iap.*` unavailable
- LINE Pay terminated in Japan (April 30, 2025) — verify current availability at [LINE Pay docs](https://developers.line.biz/en/docs/line-mini-app/develop/iap/)
- IAP auth differs by endpoint: reserve uses **user** token, webhook history uses **channel** token; webhook uses **signature verification**, not IP restriction
- Channel **cannot be moved** to another provider after creation; user IDs differ per provider

## Reference Index

| File | Topic |
|------|-------|
| [references/guidelines.md](references/guidelines.md) | **Read first.** MINI App overview, verified vs unverified, specs, performance, migration, development rules, Quick Fill design regulations |
| [references/console-setup.md](references/console-setup.md) | Channel creation, 3 internal channels, LIFF ID, tokens, basic auth, display mapping, localization, settings reflection, re-review |
| [references/features.md](references/features.md) | Built-in features (action button, multi-tab, consent simplification), custom features (Custom Path, shortcuts, custom action button, share messages, OA, payments), permanent links, external browser, UI components |
| [references/service-messages.md](references/service-messages.md) | Notification token lifecycle, sending API, template structure, review lifecycle, character limits, error codes |
| [references/common-profile.md](references/common-profile.md) | Quick Fill API, scopes, form auto-fill, plugin setup, dummy data |
| [references/in-app-purchase.md](references/in-app-purchase.md) | Purchase flow (client + server), reserve, webhooks, dev guidelines, application & setup, test payment, error codes |
| [references/submission-review.md](references/submission-review.md) | Submission process, pre-review checklist, review period, approval flow, publish changes |
| [references/experts.md](references/experts.md) | LINE MINI App domain experts for architecture guidance |

## SDK & Tools

- LINE MINI App is built on **LIFF SDK**: [@line/liff](https://www.npmjs.com/package/@line/liff)
- **Quick Fill plugin**: [@line/liff-common-profile-plugin](https://www.npmjs.com/package/@line/liff-common-profile-plugin)
- Scaffold: `npx @line/create-liff-app`
- **LINE MINI App Playground**: [miniapp.line.me/lineminiapp_playground](https://miniapp.line.me/lineminiapp_playground) — online MINI App API testing
