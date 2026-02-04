---
name: create-auth-skill
description: 使用 Better Auth 为 TypeScript/JavaScript 应用创建鉴权层的技能。
---

# Create Auth Skill

使用 Better Auth 为 TypeScript/JavaScript 应用添加鉴权的指南。

**代码示例与语法参见 [better-auth.com/docs](https://better-auth.com/docs)。**

---

## 决策树

```
是否为新项目/空项目？
├─ 是 → 新项目搭建
│ 1. 确定框架
│ 2. 选择数据库
│ 3. 安装 better-auth
│ 4. 创建 auth.ts + auth-client.ts
│ 5. 配置路由处理器
│ 6. 运行 CLI migrate/generate
│ 7. 通过插件添加能力
│
└─ 否 → 项目是否已有鉴权？
 ├─ 是 → 迁移/增强
 │ • 审计现有鉴权缺口
 │ • 规划渐进式迁移
 │ • 参考文档中的迁移指南
 │
 └─ 否 → 为现有项目添加鉴权
 1. 分析项目结构
 2. 安装 better-auth
 3. 创建 auth 配置
 4. 添加路由处理器
 5. 运行 schema 迁移
 6. 接入现有页面
```

---

## 安装

**核心：** `npm install better-auth`

**按需安装的作用域包：**
| 包 | 用途 |
|---------|---------|
| `@better-auth/passkey` | WebAuthn/Passkey 鉴权 |
| `@better-auth/sso` | SAML/OIDC 企业 SSO |
| `@better-auth/stripe` | Stripe 支付 |
| `@better-auth/scim` | SCIM 用户配置 |
| `@better-auth/expo` | React Native/Expo |

---

## 环境变量

```env
BETTER_AUTH_SECRET=<32+ 字符，可用 openssl rand -base64 32 生成>
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL= 
```

按需添加 OAuth 密钥：`GITHUB_CLIENT_ID`、`GITHUB_CLIENT_SECRET`、`GOOGLE_CLIENT_ID` 等。

---

## 服务端配置（auth.ts）

**位置：** `lib/auth.ts` 或 `src/lib/auth.ts`

**最小配置需包含：**
- `database` - 连接或适配器
- `emailAndPassword: { enabled: true }` - 邮箱/密码鉴权

**标准配置可增加：**
- `socialProviders` - OAuth 提供方（google、github 等）
- `emailVerification.sendVerificationEmail` - 验证邮件发送
- `emailAndPassword.sendResetPassword` - 重置密码发送

**完整配置可增加：**
- `plugins` - 功能插件数组
- `session` - 过期、cookie 缓存等
- `account.accountLinking` - 多提供方账号关联
- `rateLimit` - 限流配置

**导出类型：** `export type Session = typeof auth.$Infer.Session`

---

## 客户端配置（auth-client.ts）

**按框架导入：**
| 框架 | 导入 |
|-----------|-----------|
| React/Next.js | `better-auth/react` |
| Vue | `better-auth/vue` |
| Svelte | `better-auth/svelte` |
| Solid | `better-auth/solid` |
| Vanilla JS | `better-auth/client` |

**客户端插件** 放在 `createAuthClient({ plugins: [...] })` 中。

**常用导出：** `signIn`、`signUp`、`signOut`、`useSession`、`getSession`

---

## 路由处理器配置

| 框架 | 文件 | 处理器 |
|-----------|------|------|
| Next.js App Router | `app/api/auth/[...all]/route.ts` | `toNextJsHandler(auth)` → 导出 `{ GET, POST }` |
| Next.js Pages | `pages/api/auth/[...all].ts` | `toNextJsHandler(auth)` → 默认导出 |
| Express | 任意文件 | `app.all("/api/auth/*", toNodeHandler(auth))` |
| SvelteKit | `src/hooks.server.ts` | `svelteKitHandler(auth)` |
| SolidStart | 路由文件 | `solidStartHandler(auth)` |
| Hono | 路由文件 | `auth.handler(c.req.raw)` |

**Next.js Server Components：** 在 auth 配置中添加 `nextCookies()` 插件。

---

## 数据库迁移

| 适配器 | 命令 |
|---------|---------|
| 内置 Kysely | `npx @better-auth/cli@latest migrate`（直接应用） |
| Prisma | `npx @better-auth/cli@latest generate --output prisma/schema.prisma` 然后 `npx prisma migrate dev` |
| Drizzle | `npx @better-auth/cli@latest generate --output src/db/auth-schema.ts` 然后 `npx drizzle-kit push` |

**添加插件后需重新执行。**

---

## 数据库适配器

| 数据库 | 配置 |
|----------|----------|
| SQLite | 直接传入 `better-sqlite3` 或 `bun:sqlite` 实例 |
| PostgreSQL | 直接传入 `pg.Pool` 实例 |
| MySQL | 直接传入 `mysql2` pool |
| Prisma | `prismaAdapter(prisma, { provider: "postgresql" })`，来自 `better-auth/adapters/prisma` |
| Drizzle | `drizzleAdapter(db, { provider: "pg" })`，来自 `better-auth/adapters/drizzle` |
| MongoDB | `mongodbAdapter(db)`，来自 `better-auth/adapters/mongodb` |

---

## 常用插件

| 插件 | 服务端导入 | 客户端导入 | 用途 |
|--------|---------------|---------------|---------|
| `twoFactor` | `better-auth/plugins` | `twoFactorClient` | TOTP/OTP 双因素 |
| `organization` | `better-auth/plugins` | `organizationClient` | 团队/组织 |
| `admin` | `better-auth/plugins` | `adminClient` | 用户管理 |
| `bearer` | `better-auth/plugins` | - | API Token 鉴权 |
| `openAPI` | `better-auth/plugins` | - | API 文档 |
| `passkey` | `@better-auth/passkey` | `passkeyClient` | WebAuthn |
| `sso` | `@better-auth/sso` | - | 企业 SSO |

**插件用法：** 服务端插件 + 客户端插件 + 执行迁移。

---

## 鉴权 UI 实现

**登录流程：**
1. `signIn.email({ email, password })` 或 `signIn.social({ provider, callbackURL })`
2. 处理返回的 `error`
3. 成功时重定向

**客户端会话检查：** `useSession()` 返回 `{ data: session, isPending }`

**服务端会话检查：** `auth.api.getSession({ headers: await headers() })`

**受保护路由：** 检查 session，为空则重定向到 `/sign-in`。

---

## 安全清单

- [ ] 设置 `BETTER_AUTH_SECRET`（32+ 字符）
- [ ] 生产环境启用 `advanced.useSecureCookies: true`
- [ ] 配置 `trustedOrigins`
- [ ] 启用限流
- [ ] 启用邮箱验证
- [ ] 实现密码重置
- [ ] 敏感应用启用 2FA
- [ ] 不要关闭 CSRF 防护
- [ ] 审查 `account.accountLinking`

---

## 故障排查

| 问题 | 处理 |
|-------|-------|
| "Secret not set" | 添加 `BETTER_AUTH_SECRET` 环境变量 |
| "Invalid Origin" | 在 `trustedOrigins` 中加入域名 |
| Cookie 不生效 | 检查 `baseURL` 与域名一致；生产启用 secure cookies |
| OAuth 回调错误 | 在提供方控制台核对 redirect URIs |
| 添加插件后类型报错 | 重新运行 CLI generate/migrate |

---

## 参考

- [文档](https://better-auth.com/docs)
- [示例](https://github.com/better-auth/examples)
- [插件](https://better-auth.com/docs/concepts/plugins)
- [CLI](https://better-auth.com/docs/concepts/cli)
- [迁移指南](https://better-auth.com/docs/guides)
