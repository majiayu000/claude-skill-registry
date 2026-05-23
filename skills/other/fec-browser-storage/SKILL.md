---
name: fec-browser-storage
description: Use when choosing, implementing, or reviewing browser storage such as localStorage, sessionStorage, IndexedDB, cookies, client persistence, offline data, secure storage, or cleanup strategy; Chinese triggers include 浏览器存储, 客户端持久化.
---

# 浏览器存储

## Purpose

根据数据大小、安全要求和生命周期选择合适的客户端存储方案。

## Procedure

1. 先判断数据敏感度、体积、生命周期、是否需要跨 Tab、是否需要随请求发送。
2. 小量非敏感偏好用 localStorage；Tab 级临时数据用 sessionStorage；大量结构化数据或离线缓存用 IndexedDB；认证态优先 httpOnly cookie。
3. 封装统一 key 前缀、JSON parse/stringify、异常处理、过期清理和 quota 兜底。
4. 敏感数据按安全规则处理，不把明文 token、密码、信用卡信息放进可被 JS 读取的存储。
5. 审查隐私模式、存储配额、清理策略和跨浏览器兼容性。

## Detailed References

Load [references/storage-patterns.md](references/storage-patterns.md) for storage selection tables, localStorage/sessionStorage wrappers, IndexedDB examples, cookie helpers, and sensitive-data rules.

## Constraints

- localStorage/sessionStorage 是同步 API，大数据读写会阻塞主线程。
- 除 httpOnly cookie 外，客户端存储都可被 XSS 读取。
- Cookie 每次请求自动携带，不适合大数据。
- IndexedDB 配额和隐私模式行为有浏览器差异。
- URL 中不要传 token 或敏感数据。

## Expected Output

产出统一的 storage/cookie/db 封装，key 有命名空间，数据有过期或清理策略，敏感数据只进入合适的安全边界。

## Related Skills / Boundary

- `fec-security-review` — token、隐私数据和 XSS 读取风险深审。
- `fec-pwa-implementation` — Service Worker 离线缓存和 installability。
- `fec-data-fetching` — server state 和 API 缓存，不负责浏览器持久化。
