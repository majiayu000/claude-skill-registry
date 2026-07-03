---
name: agf-releasing-apple
description: Use when apple-release-engineer is about to build the signed distributable (TestFlight build / notarized DMG / internal package) from merged-to-main code (after apple code review + SIT Audit pass and merge, before apple-qa-engineer runs E2E/UAT). Provides the applicability gate, pre-flight checks, lane execution per channel, notarization, real-output smoke test, hand-off, and the release-report skeleton. Pairs with deployment.md §7 "Apple 发布" contract and slash /agf-apple-release.
---

# Releasing the Apple distributable (sign → notarize → package → smoke)

把**合并到 main 后的干净代码**构建成签名分发包，冒烟自检通过后交接 apple-qa-engineer。本 skill 是 apple-release-engineer 的分步 runbook；契约 SSOT 是 [`deployment.md` §7](../../standards/deployment.md)，流水线决策是 [ADR-009](../../../docs/adr/009-apple-release-pipeline.md)。

## 适用门

满足以下**全部**才进入构建：

- 角色 = `apple-release-engineer`（deploy-only，不修业务源码；`apple/fastlane/` 配置是可写域）。
- 目标是 **Apple 原生链路**（`apple/` 工程）。Web docker UAT → 归 deploy-engineer；小程序体验版 → 归 miniapp 轨。**均不适用**。
- apple code review（含 SIT Audit）已通过**且已合并到 main**，product-lead 已确认"构建分发包"（对话内确认或 `/agf-apple-release` 手动触发），且 PRD 已声明渠道。

任一不满足 → 不构建，SendMessage product-lead 说明缺什么。

## 前置检查（构建前必须逐项确认）

- [ ] **main 干净且最新**：`git status` 无未提交改动，记录构建 commit SHA（`git rev-parse --short HEAD`）。
- [ ] **工具链可用**：`xcodebuild -version` / `bundle exec fastlane --version` 正常返回。
- [ ] **签名材料就位且不入库**：App Store Connect API key（`.p8`）路径 / key id / issuer id 经环境变量可达；match 仓可访问（`fastlane match` 能同步证书 + profile）。任何 `.p8` / `.p12` / `.mobileprovision` 都**不得**出现在 git 工作区（scan-secrets / pre-commit 兜底）。
- [ ] **渠道已声明**：PRD / task 写明渠道，映射到 lane（见下表）。
- [ ] **版本号就绪**：marketing version 符合 `versioning.md`；build number 在该渠道单调递增。

任一不勾 → 不构建，先 SendMessage product-lead 解决先决条件。

## 渠道 → lane 执行（映射 SSOT 见 deployment.md §7.2）

```bash
cd apple && bundle exec fastlane <lane>
```

| lane | 渠道 | 关键动作 |
|---|---|---|
| `beta` | TestFlight 内测 | `match(type: appstore)` → `build_app` → `pilot`（上传 + 等待处理完成） |
| `release_appstore` | App Store 上架 | `match` → `build_app` → `deliver`（含元数据 / 截图 / 提审包） |
| `release_dmg` | macOS 直发 | `match(type: developer_id)` → `build_app` → `notarize`（notarytool + API key）→ DMG 打包（`hdiutil` / create-dmg） |
| `release_internal` | 企业 / 内部 | macOS：Developer ID 包内部散发；iOS in-house lane 仅在 Enterprise 会籍就位后启用（ADR-009） |

- 公证有 Apple 侧分钟级排队——`notarize` 等待完成后才继续，**禁止**跳过等待声明成功。
- 构建产物路径 / build 号记录进报告。

## 冒烟（真实输出，非 dry-run）

只接受真实证据，拒绝 "构建 exit 0 就算" / "应该能装"：

- **macOS 直发（DMG）**：
  ```bash
  spctl -a -vv /path/to/App.app          # 期望 "accepted ... Notarized Developer ID"
  hdiutil attach <dmg> && open App.app    # 干净用户目录实际启动
  ```
  贴 `spctl` 真实输出 + app 启动后关键路径点查（主窗口出现 / 核心视图可达）。
- **TestFlight（iOS / macOS App Store 系）**：
  - `pilot` 上传完成 + App Store Connect 处理状态到 "Ready to Test"（贴 fastlane 输出的 build 号 + 状态行）
  - 至少一台设备 / 模拟器装 TestFlight build 实际启动点查
- **App Store 提审包**：`deliver` 校验通过输出（元数据 / 截图齐全），不实际点提交（提审动作由 product-lead 确认后执行）。

任一非预期 → gate = `❌ 构建失败`。

**冒烟范围说明**：冒烟只证明"包出得来、装得上、跑得起"，**不是** E2E——AC 验收归 apple-qa-engineer。冒烟暴露**代码层**缺陷（启动即崩 / 核心视图白屏），采集证据退回 product-lead，不自己改 `apple/App*`。

## 二元 gate

- `✅ 构建成功（冒烟通过）` —— 前置全过 + lane 完成 + 公证/处理完成 + 冒烟真实证据。
- `❌ 构建失败` —— 任一环节失败；报告标明**签名/公证/打包配置问题**（自己重跑）还是**代码问题**（退回 PL → apple-dev）。

不发明新 verdict 词表（保 CLAUDE.md「Verdict 词表 4 套」硬事实）。

## 交接

报告落盘后立即（**不等用户问**）SendMessage product-lead：

```
SendMessage({to: "product-lead", message: "发布构建完成: [功能名]\n报告: docs/deploy/[feature]-apple-[YYYY-MM-DD].md\n渠道/lane: [lane]\n分发包: [TestFlight build 号 / DMG 路径]\n构建 commit: [SHA]\n结果: ✅ 构建成功（冒烟通过） / ❌ 构建失败", summary: "Apple 发布构建: [功能名]"})
```

✅ → PL 触发 apple-qa-engineer 对该分发包跑 E2E；❌ → PL 决策重跑（配置）/ 退回 apple-dev（代码）。

## 发布报告骨架

落到 `docs/deploy/<feature>-apple-<YYYY-MM-DD>.md`（pool=1，无 agf-matrix frontmatter）：

````markdown
# Apple 发布报告 — [Feature]

- **Date**: YYYY-MM-DD
- **Releaser**: apple-release-engineer ([model name])
- **构建 commit (merged main)**: [short SHA]
- **渠道 / lane**: [beta | release_appstore | release_dmg | release_internal]
- **Target**: [macos | ios | universal]
- **版本**: [marketing version] ([build number])

## 分发包定位（交给 apple-qa-engineer 作测试目标）

| 项 | 值 |
|---|---|
| TestFlight build 号 / DMG 路径 | ... |
| 安装方式 | TestFlight 邀请 / DMG 挂载 |

## 前置检查

- [x] main 干净（commit [SHA]）
- [x] 工具链可用（xcodebuild / fastlane 版本）
- [x] 签名材料就位（match 同步成功；无 .p8/.p12 入库）
- [x] 渠道已声明 + 版本号就绪

## Lane 执行

```
bundle exec fastlane <lane>
（贴关键输出：match 同步 / build_app 产物 / pilot 或 notarize 完成行）
```

## 冒烟证据（真实输出，非 dry-run）

- **公证/处理状态**：（贴 spctl -a -vv 输出 / TestFlight "Ready to Test" 状态行）
- **实际启动点查**：（装包启动 + 关键路径可达的证据）

## Release Gate

**Verdict**: ✅ 构建成功（冒烟通过） / ❌ 构建失败
（失败时：问题归类 = 签名/公证/打包配置（自己重跑） / 代码（退回 product-lead → apple-dev）+ 证据）

## Hand-off

✅ → SendMessage product-lead（附分发包定位）→ PL 触发 apple-qa-engineer E2E
❌ → SendMessage product-lead（附失败定位）→ PL 决策重跑 / 退回 apple-dev
````

## 完成前的验证

- [ ] 构建源确为合并后的 main（记了 commit SHA）？
- [ ] 签名走 match 正规链路（无 ad-hoc 绕过 / 无关公证）？
- [ ] 公证 / TestFlight 处理**等到完成状态**才声明（非 exit 0 即成功）？
- [ ] 冒烟每条都有真实输出（spctl / 状态行 / 启动证据）？
- [ ] gate 是二元（✅/❌），失败时标了配置 vs 代码归类？
- [ ] 报告落盘 + SendMessage product-lead 已发（附分发包定位）？

任一不行 → 不要声明构建成功，回去补。

## 反模式

- ❌ 构建未合并分支 —— 必须从合并后的 main 拉。
- ❌ ad-hoc 签名 / 关沙盒 / 跳公证"先测了再说" —— QA 测的必须是真实分发形态。
- ❌ `.p8` / `.p12` / match 密码写进任何入库文件 —— 环境变量 / Keychain only。
- ❌ 公证还在排队就声明成功 —— 等 "Accepted" / "Ready to Test"。
- ❌ 冒烟暴露代码 bug 时自己改 `apple/App*` —— 越界；采证退回 PL → apple-dev。
- ❌ 给发布门发明多档 verdict —— 二元 gate（✅/❌）即可。
