---
name: better-auth-best-practices
description: "集成 Better Auth（TypeScript 鉴权框架）时使用。支持邮箱密码、OAuth、魔法链接、Passkey 等，通过插件扩展。编写或配置 Better Auth 时触发。"
license: MIT
---

# Better Auth 集成指南

**代码示例与最新 API 请查阅 [better-auth.com/docs](https://better-auth.com/docs)。**

Better Auth 是 TypeScript 优先、框架无关的鉴权框架，通过插件支持邮箱/密码、OAuth、魔法链接、Passkey 等。

---

## 速查

### 环境变量
- `BETTER_AUTH_SECRET`：加密密钥（至少 32 字符）。生成：`openssl rand -base64 32`
- `BETTER_AUTH_URL`：根 URL（如 `https://example.com`）

仅当未设置环境变量时，在配置中定义 `baseURL` / `secret`。

### 配置文件位置
CLI 在 `./`、`./lib`、`./utils` 或 `./src` 下查找 `auth.ts`。自定义路径用 `--config`。

### CLI 命令
- `npx @better-auth/cli@latest migrate` — 应用 schema（内置 adapter）
- `npx @better-auth/cli@latest generate` — 为 Prisma/Drizzle 生成 schema
- `npx @better-auth/cli mcp --cursor` — 为 AI 工具添加 MCP

**新增或修改插件后需重新执行。**

---

## 核心配置项

| 选项 | 说明 |
|------|------|
| `appName` | 可选显示名称 |
| `baseURL` | 仅当未设置 `BETTER_AUTH_URL` 时 |
| `basePath` | 默认 `/api/auth`，设为 `/` 可放在根路径 |
| `secret` | 仅当未设置 `BETTER_AUTH_SECRET` 时 |
| `database` | 多数功能必需，见 adapter 文档 |
| `secondaryStorage` | Redis/KV，用于 session 与限流 |
| `emailAndPassword` | `{ enabled: true }` 启用 |
| `socialProviders` | `{ google: { clientId, clientSecret }, ... }` |
| `plugins` | 插件数组 |
| `trustedOrigins` | CSRF 白名单 |

---

## 数据库

**直连**：传入 `pg.Pool`、`mysql2` 池、`better-sqlite3` 或 `bun:sqlite` 实例。

**ORM adapter**：从 `better-auth/adapters/drizzle`、`better-auth/adapters/prisma`、`better-auth/adapters/mongodb` 等导入。

**注意**：Better Auth 使用 adapter 的 model 名，而非表名。若 Prisma model 为 `User` 对应表 `users`，用 `modelName: "user"`（Prisma 引用），而非 `"users"`。

---

## Session 管理

**存储优先级**：  
1. 若配置了 `secondaryStorage` → session 存此处（不存 DB）  
2. 设 `session.storeSessionInDatabase: true` 可同时持久化到 DB  
3. 无 DB + `cookieCache` → 纯无状态模式  

**Cookie 缓存策略**：`compact`（默认）、`jwt`、`jwe`。  
**关键选项**：`session.expiresIn`、`session.updateAge`、`session.cookieCache.maxAge`、`session.cookieCache.version`（变更可令所有 session 失效）。

---

## 用户与 Account 配置

**User**：`user.modelName`、`user.fields`、`user.additionalFields`、`user.changeEmail.enabled`、`user.deleteUser.enabled`。  
**Account**：`account.modelName`、`account.accountLinking.enabled`、`account.storeAccountCookie`。  
**注册必需字段**：`email` 与 `name`。

---

## 邮件流程

- `emailVerification.sendVerificationEmail` — 验证邮件发送，必须定义
- `emailVerification.sendOnSignUp` / `sendOnSignIn` — 自动发送时机
- `emailAndPassword.sendResetPassword` — 重置密码邮件

---

## 安全

**`advanced` 中**：`useSecureCookies`、`disableCSRFCheck`（有风险）、`disableOriginCheck`（有风险）、`crossSubDomainCookies.enabled`、`ipAddress.ipAddressHeaders`、`database.generateId` 等。  
**限流**：`rateLimit.enabled`、`rateLimit.window`、`rateLimit.max`、`rateLimit.storage`。

---

## Hooks

**端点**：`hooks.before` / `hooks.after`，`{ matcher, handler }` 数组，可用 `createAuthMiddleware`。  
**数据库**：`databaseHooks.user.create.before/after` 等，用于默认值或创建后逻辑。  
**Hook 上下文**：`session`、`secret`、`adapter`、`generateId()`、`baseURL` 等。

---

## 插件

**按路径导入以支持 tree-shaking**：  
`import { twoFactor } from "better-auth/plugins/two-factor"`  
勿从 `"better-auth/plugins"` 整体导入。

**常用插件**：`twoFactor`、`organization`、`passkey`、`magicLink`、`emailOtp`、`username`、`admin`、`apiKey`、`bearer`、`jwt`、`multiSession`、`sso`、`openAPI` 等。  
客户端插件放在 `createAuthClient({ plugins: [...] })`。

---

## 客户端

从 `better-auth/client`、`better-auth/react`、`better-auth/vue` 等导入。  
常用方法：`signUp.email()`、`signIn.email()`、`signIn.social()`、`signOut()`、`useSession()`、`getSession()`、`revokeSession()` 等。

---

## 类型安全

推断类型：`typeof auth.$Infer.Session`、`typeof auth.$Infer.Session.user`。  
前后端分离项目：`createAuthClient()`。

---

## 常见坑

1. **Model 与表名** — 配置用 ORM model 名，不是表名  
2. **插件 schema** — 增删插件后重跑 CLI  
3. **Secondary storage** — 默认 session 存此处而非 DB  
4. **Cookie cache** — 自定义 session 字段不缓存，每次重新拉取  
5. **无状态模式** — 无 DB 时 session 仅存 cookie，缓存过期即登出  
6. **改邮箱流程** — 先发当前邮箱，再发新邮箱  

---

## 资源

- [文档](https://better-auth.com/docs)
- [配置参考](https://better-auth.com/docs/reference/options)
- [LLMs.txt](https://better-auth.com/llms.txt)
- [GitHub](https://github.com/better-auth/better-auth)
