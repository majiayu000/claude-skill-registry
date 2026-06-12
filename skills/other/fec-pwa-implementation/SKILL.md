---
name: fec-pwa-implementation
description: 用于添加或审查 Progressive Web App 能力，如可安装性、manifest 元数据、Service Worker 注册、Workbox 缓存、离线兜底、应用更新提示、maskable icons 或 iOS PWA 兼容性。不要用于普通 API 缓存或不可安装的性能调优；中文触发词包括 PWA、离线、Service Worker。
---

# PWA 实现

## 用途

让 Web 应用具备可安装、离线兜底和可控更新能力。

## 流程

1. 确认 PWA 是否值得做：面向移动端/桌面安装、弱网离线、重复访问场景时优先；纯内部后台、强实时流媒体或只需要普通缓存时不要强行 PWA。
2. 先补齐 manifest、图标、主题色和 HTML 引用；图标至少覆盖 192/512，Android 需 maskable，iOS 需 apple touch icon。
3. 注册 Service Worker，并设计更新提示；不要静默 `skipWaiting()` 后强刷用户页面。
4. 用 Workbox 或框架插件管理 precache/runtime cache；登录、支付、权限变更等敏感请求必须走网络。
5. 提供 offline fallback 页面和安装提示 UI，并验证首次加载、离线访问、更新激活、卸载重装。

## 详细参考

- 需要 manifest 字段、HTML 引用、图标要求、截图和 iOS 注意事项时，加载 [references/manifest-and-icons.md](references/manifest-and-icons.md)。
- 需要 Service Worker 注册、Workbox 策略、Vite 集成、离线兜底和更新流程时，加载 [references/service-worker-workbox.md](references/service-worker-workbox.md)。

## 约束

- Service Worker 仅在 HTTPS 下工作（localhost 除外）。
- 缓存策略必须区分页面、静态资源、API 与敏感操作；不要把登录、支付、权限接口缓存起来。
- Service Worker 更新有生命周期延迟；用户可见刷新提示优先于强制刷新。
- iOS PWA 能力弱于 Android，安装、推送和生命周期都要单独验证。
- 缓存有配额和逐出机制，必须设置 max entries / max age。

## 预期输出

产出可安装的 Web 应用、离线 fallback、可见更新提示和明确缓存策略。验证 Lighthouse PWA、DevTools Application 面板、离线模式、更新发布和移动端安装流程。
