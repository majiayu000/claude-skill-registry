---
name: fec-vite-project-standard
description: Use when creating, configuring, reviewing, or debugging Vite-based frontend projects, vite.config.ts, env variables, dev server proxy, HMR, plugin ordering, library mode, dependency pre-bundling, bundle splitting, or Vite build performance. Use framework-specific skills for React/Vue component architecture; Chinese triggers include Vite 配置, vite.config, Vite 构建, Vite 性能.
---

# Vite 项目规范

适用于 Vite 应用、组件库、开发服务器和构建配置的设计与审查。

## Purpose

规范 Vite 配置、安全边界和构建性能，避免开发环境与生产构建的常见陷阱。

## Procedure

1. 识别项目类型
   - 应用项目优先检查 `root`、`base`、`server.proxy`、`envPrefix`、`build` 和框架插件。
   - 组件库项目优先检查 `build.lib`、类型产物、peer dependencies external 和导出入口。
   - Monorepo 额外检查 `server.fs.allow`、路径别名和包依赖边界。

2. 选择插件
   - React 默认优先 `@vitejs/plugin-react-swc`；需要 Babel 插件时才用 `@vitejs/plugin-react`。
   - Vue 项目使用 `@vitejs/plugin-vue`，路径别名优先交给 `vite-tsconfig-paths`。
   - TypeScript 项目必须通过 `tsc --noEmit`、CI 或 `vite-plugin-checker` 补齐类型检查。

3. 管理环境变量
   - 客户端只读取明确公开的前缀，如 `VITE_`。
   - `loadEnv` 第三个参数使用显式前缀数组，不使用空字符串加载全部变量。
   - 密钥、数据库地址、私有 token 必须留在服务端或构建系统，不进入客户端 bundle。

4. 优化开发体验
   - 慢启动先用 `vite --profile` 定位插件、解析或预构建瓶颈。
   - 对 CJS/UMD 依赖用 `optimizeDeps.include` 处理互操作问题。
   - 大项目可用 `server.warmup.clientFiles` 预热核心入口。

5. 优化生产构建
   - 发布前运行 `vite build`，并用 `vite preview` 做本地构建烟测。
   - 手动分包使用稳定的对象形式优先，避免把每个依赖拆成独立小 chunk。
   - 生产 sourcemap 默认关闭；若上传错误追踪平台，上传后不随站点公开。
   - 动效、3D、图表、编辑器、地图和音视频处理库优先通过动态导入或路由级拆包隔离。
   - 检查静态资源是否进入正确目录、是否被 hash/cache、是否存在占位 URL 或过大的未压缩媒体。

## Minimal Config

```ts
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react-swc";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), ["VITE_"]);

  return {
    plugins: [react(), tsconfigPaths()],
    define: {
      __PUBLIC_API_URL__: JSON.stringify(env.VITE_API_URL),
    },
    server: {
      proxy: {
        "/api": {
          target: "http://localhost:8080",
          changeOrigin: true,
        },
      },
    },
  };
});
```

## Constraints

- `vite build` 只转译和打包，不等于类型检查；CI 必须另跑 typecheck。
- `VITE_` 不是安全边界；任何 `VITE_` 变量都会进入客户端包。
- 不设置 `envPrefix: ""`，不使用 `loadEnv(mode, root, "")` 后再随意 `define`。
- 不默认引入 legacy 插件；只有真实用户数据需要时再启用。
- 不用 `vite preview` 作为生产服务器。
- 组件库必须 externalize peer dependencies，并单独产出 `.d.ts`。
- 不把服务端密钥通过 `define`、`import.meta.env` 或空前缀 `loadEnv` 注入客户端。
- 不把 GSAP、Three.js、Lottie、Monaco、地图 SDK 等重型库放进所有页面共享入口；先评估 async chunk 和首屏影响。

## Expected Output

输出应包含项目类型判断、关键配置变更、环境变量安全说明、构建/开发性能验证方式。完成后 Vite 配置应可类型检查、可构建、密钥不泄露，并能解释 dev 与 build 的差异。
