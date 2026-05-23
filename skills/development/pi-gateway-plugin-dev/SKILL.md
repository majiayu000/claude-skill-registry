---
name: pi-gateway-plugin-dev
description: 为 pi-gateway 开发 Gateway 插件的实战技能。当需求涉及通过 pi SDK/RPC 扩展网关能力（如模型列表、模型切换、WS 方法、命令、Hook、后台服务）且要求“每个插件独立目录 + plugin.json + src 多文件结构”时使用。
---

# Pi Gateway Plugin Dev 技能

用于在 **gateway 模式** 开发插件，不是 `pi extension`。

## 适用边界

- 目标是扩展 `pi-gateway` 的连接层能力（消息通道、HTTP/WS、命令、服务）
- 插件加载位置是 `~/.pi/gateway/plugins/` 或 `plugins.dirs[]` 指定目录
- 插件必须有 `plugin.json`，并通过 `main` 指向入口文件

以下场景不要用本技能：

- 修改 Agent 思维、提示词、工具执行行为（那是 `~/.pi/agent/extensions` 的职责）
- 仅在 CLI/TUI 中运行、不经过 gateway 的功能

## 强制规范

1. 每个插件一个独立目录（`<plugins-root>/<plugin-id>/`）。
2. 禁止单文件模式：不能只放一个 `index.ts` 就结束。
3. 入口文件只做组装，不写核心业务逻辑。
4. 业务按职责拆分到 `src/commands.ts`、`src/rpc-methods.ts`、`src/hooks.ts`、`src/services.ts`、`src/types.ts`。
5. 插件只在 gateway 插件机制里加载，不放到 `~/.pi/agent/extensions/`。

## 标准目录

```text
<plugins-root>/<plugin-id>/
  plugin.json
  src/
    index.ts
    types.ts
    commands.ts
    rpc-methods.ts
    hooks.ts
    services.ts
```

## 工作流

1. 先判定是 Gateway 插件需求（不是 pi extension）。
2. 阅读目录规范：`references/plugin-directory-architecture.md`
3. 阅读 SDK 接口：`references/sdk-capabilities.md`
4. 阅读 RPC 能力映射：`references/rpc-capabilities.md`
5. 如涉及模型能力，读取：`references/model-control-pattern.md`
6. 用脚手架生成插件目录，再填业务逻辑。
7. 在 `pi-gateway.json` 里配置 `plugins.dirs[]` 并启动验证。

## 脚手架命令

```bash
bash skills/pi-gateway-plugin-dev/scripts/new-plugin.sh ~/.pi/gateway/plugins model-control "Model Control"
```

生成后会得到完整多文件插件目录，不会退化为单 `index.ts`。

## 模型能力实现策略

- 切模型：用 `GatewayPluginApi.setModel(sessionKey, provider, modelId)`。
- 调思考强度：用 `GatewayPluginApi.setThinkingLevel(sessionKey, level)`。
- 列模型：当前 `GatewayPluginApi` 不直接暴露 `getAvailableModels`，推荐复用网关内置 `models.list` / `/api/models`。
- 若必须插件内部直连 RPC：先扩展 `GatewayPluginApi` + `createPluginApi` + `RpcClient` 映射，见 `references/rpc-capabilities.md` 的“扩展路径”。

## 交付要求

- 输出插件目录树
- 输出 `plugin.json` 和关键源文件
- 说明如何在 gateway 模式加载（`plugins.dirs[]`）
- 给出最小验证命令（至少覆盖“列模型/切模型”或对应能力）
