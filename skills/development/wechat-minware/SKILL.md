---
name: wechat-minware
description: Build, review, and refactor WeChat Mini Program (微信小程序) frontends. Use for tasks like WXML/WXSS/JS/TS structure, page routing, componentization, state management patterns, API requests, login/openid flows integration points, performance optimization (setData), security/privacy compliance, and release/QA checklists.
---

# wechat-minware

Use this skill for 微信小程序（大前端 / 端侧）开发与评审。

## Defaults (unless repo dictates otherwise)

- Framework: 原生小程序（WXML/WXSS/JS）优先；如已使用 Taro/uni-app/mpvue，按现有框架走
- Language: TypeScript if present; otherwise JavaScript
- Componentization: 自定义组件（`components/`）+ 页面内 `_components/`（可选）
- Network: 封装 `request`（统一鉴权/重试/错误码处理）

## Project structure (recommended for native)

- `miniprogram/`
  - `app.ts|js`, `app.json`, `app.wxss`
  - `pages/<route>/index.(wxml|wxss|ts|js|json)`
  - `components/<name>/...`
  - `utils/`（request、storage、date、logger）
  - `services/`（API 客户端、DTO、mapping）
  - `assets/`

## Workflow

1) Establish constraints
- Base library version, target WeChat version, current framework.
- Whether using cloud development (云开发) or external backend.

2) Routing and page design
- Confirm `app.json` routes and tabBar strategy.
- Keep page responsibilities single-purpose; extract reusable UI to components.

3) State & data flow
- Prefer local state for simple pages.
- For cross-page/session state: centralized store (if already present) or minimal shared module in `utils/`.
- Avoid storing sensitive data in plain storage; use short TTL for session tokens.

4) Networking & auth integration points
- Wrap requests: base URL, headers, signature, retry/backoff, timeout, standardized errors.
- Login flow: `wx.login` → code exchange on backend → session token.
- Do not hardcode secrets in mini program; all secrets stay server-side.

5) Performance
- Reduce `setData` frequency and payload size; batch updates.
- Use `wx:if` vs `hidden` appropriately; avoid deep data binding.
- Images: use CDN, proper sizes; lazy load for long lists.

6) Security & privacy compliance
- Only request necessary permissions; provide user-facing explanation.
- Minimize logging of PII; ensure privacy policy matches actual behavior.
- Handle error states safely; avoid leaking server internal details.

7) QA / release checklist
- Check `app.json` permissions and domains (request合法域名).
- Verify on real devices and different WeChat versions.
- Ensure stable fallbacks for network errors and empty states.

## Output expectations when making changes

- Keep diffs localized; avoid large rewrites unless requested.
- For new features: include page route, UI, request wiring, and analytics events if present.

