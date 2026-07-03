---
name: agf-wiring-apple-llm
description: Use when wiring LLM features into the Apple client (macOS / iOS) — streaming chat via the FastAPI multi-LLM gateway, or on-device inference (Apple Foundation Models / Core ML). Provides the route decision (gateway vs on-device), streaming transport pattern, env/config contract, offline & cost guardrails, and minimum verifications before declaring the integration done.
---

# Wiring LLM into the Apple client (gateway streaming / on-device)

Use this skill when:

- 给 `apple/` app 加对话 / 生成 / 总结类 LLM 功能
- 把某条 LLM 路径从后端网关切到 on-device（或反向）
- 调试 Apple 客户端的流式输出 / token 计量 / 降级行为

## Decision: gateway or on-device?

**默认走后端网关**：FastAPI 后端已按 skill `agf-wiring-multi-llm-sdk` 封装 DeepSeek / Doubao / Qwen / MiniMax（provider 切换、fallback、cost telemetry 全在服务端）。客户端只对**一个**自有 API 说话，不直连任何 LLM 厂商。

| 场景 | 路由 | 理由 |
|---|---|---|
| 对话 / 生成 / RAG（默认） | **后端网关** | key 不进客户端、provider 可热切、成本计量集中、合规审计单点 |
| 离线可用 / 隐私敏感（文本不出设备）/ 低延迟小任务（分类、摘要短文本） | **on-device**（Apple Foundation Models framework，iOS 26+ / macOS 26+；或 Core ML 自带模型） | 零 token 成本、断网可用；但模型能力 / 上下文受限 |
| 多模态生成（文生图 / 视频） | 后端网关（ml-engineer 维护的推理服务） | 客户端不嵌大模型 |

> **铁律：LLM 厂商 API key 永不进客户端**。客户端二进制可被逆向，任何打进 app 的 key 等于公开。只有自有后端的会话凭证可进客户端。

on-device 路径若成为产品主路径（非补充），属技术选型变更 → tech-lead 新开 ADR。

## Gateway streaming pattern（默认路径）

后端以 SSE（`text/event-stream`）暴露流式 chat 端点。**注意**：OpenAPI 对 SSE 描述能力有限——流式端点允许在生成 client 之外**手写一个最小 SSE transport**（这是 ADR-008「禁手写」的**唯一豁免点**，豁免范围仅限流式通道本身；请求/响应模型仍用生成类型）：

```swift
// AppCore/Sources/AppCore/LLM/StreamingClient.swift —— 唯一允许的手写网络层（SSE 豁免）
let (bytes, response) = try await URLSession.shared.bytes(for: request)
for try await line in bytes.lines {
    guard line.hasPrefix("data: ") else { continue }
    let payload = line.dropFirst(6)
    if payload == "[DONE]" { break }
    // decode 用生成的 Components.Schemas.ChatChunk 类型，不手写 DTO
}
```

- 首 token 延迟（TTFT）必须上报（客户端打点 → 后端 observability.md 字段）
- 取消语义：视图消失 / 用户停止 → `Task.cancel()` 必须真正断开 SSE 连接（防后台烧 token）
- UI 增量渲染走 `@MainActor` 的 `AsyncSequence` 消费，禁在主线程做 JSON 解析

## Config contract

客户端无 `.env`；配置走 build configuration / Info.plist 注入：

| 项 | 载体 | 说明 |
|---|---|---|
| 网关 base URL | xcconfig per-configuration（Debug → localhost / UAT 栈，Release → 生产） | 禁硬编码在 Swift 源码 |
| 会话凭证 | Keychain | 禁 UserDefaults / 文件 |
| on-device 模型开关 | feature flag（后端下发或本地配置） | 降级链路可远程关 |

## Fallback & guardrails

- **网关不可达** → 有 on-device 路径的功能降级 on-device 并明示用户"离线模式"；无降级路径的功能给可重试错误态（禁白屏 / 禁假装成功）
- **on-device 模型不可用**（机型 / OS 不支持 Foundation Models）→ `@available` + 能力探测 gating，回落网关或隐藏入口
- **成本护栏**：客户端不直接产生 token 成本（网关集中计量），但必须防"循环重试风暴"——重试上限 + 指数退避
- **合规**（`apple-native.md` §7）：AI 生成内容须有举报 / 过滤入口；用户输入发往后端在隐私政策声明；隐私清单如实标注

## Verifications before "done"

- [ ] Streaming：真实增量到达（非整段一次性返回）；TTFT 已打点
- [ ] 取消：mid-stream 取消后抓包 / 日志确认连接真实断开
- [ ] 降级：模拟网关不可达（base URL 指向 `localhost:1`），确认降级行为符合上表
- [ ] 密钥：`strings` 扫 release 二进制无任何厂商 key / 网关密钥（`strings App | grep -iE 'sk-|api[_-]?key'`）
- [ ] 类型：请求 / 响应模型来自生成代码（SSE transport 豁免仅限通道层）
- [ ] on-device 路径（如有）：在最低支持机型实测延迟 + 内存峰值

## Anti-patterns

- ❌ 厂商 API key 编进客户端（含"先临时测一下"）—— 逆向即泄漏
- ❌ 客户端直连 DeepSeek / Doubao / Qwen / MiniMax —— provider 切换 / 计量 / 合规全失控
- ❌ 借 SSE 豁免扩大手写面 —— 豁免仅限流式通道，请求/响应类型仍走生成代码
- ❌ 流式 UI 全量 setState 重渲染长文本 —— 增量 append，注意 attributed string 成本
- ❌ 取消只停 UI 不断连接 —— 后台连接继续烧 token
- ❌ on-device 与网关行为差异不告知用户 —— 离线模式必须明示

## References

- 后端 provider 封装 / env 契约 / fallback：skill `agf-wiring-multi-llm-sdk`（服务端 SSOT，本 skill 不重复）
- 契约纪律与豁免边界：[ADR-008](../../../docs/adr/008-apple-backend-contract-sync.md)
- Apple Foundation Models framework：developer.apple.com（接入前 WebFetch 当前文档，API 迭代快）
