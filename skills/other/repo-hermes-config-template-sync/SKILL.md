---
name: repo-hermes-config-template-sync
description: 在 all-my-ai-needs 中新增 Hermes 脱敏配置模板与同步脚本，并补齐文档与验证。
---

# Repo Hermes Config Template Sync

## Trigger
当用户要求“Hermes 不仅同步 skills，还要有脱敏配置模板/同步方案（参考 Codex）”时使用。

## Steps
1. 新增 `platforms/hermes/config.template.yaml`
- 只保留受管配置片段。
- 敏感值使用占位符（例如 `<PLAYWRIGHT_EXT_TOKEN>`）。

2. 新增 `scripts/sync_to_hermes.sh`
- 默认 `--dry-run`。
- 显式 `--sync-config` 才写入。
- 支持 `--yes` 跳过确认。
- 支持 `--hermes-home` 指定目标目录。

3. 合并策略
- 模板占位符优先保留目标文件中已有的非占位值。
- 若目标缺失，可从环境变量回填。
- 为 Playwright token 增加别名兼容：
  - `PLAYWRIGHT_EXT_TOKEN`
  - `PLAYWRIGHT_MCP_EXTENSION_TOKEN`

4. 文档更新
- 根 `README.md` 增加脚本入口和命令示例。
- `platforms/hermes/README.md` 增加模板与手动合并说明。
- `platforms/hermes/runtime.yaml` 增加 notes/manual_steps/verify。

5. 验证
- `bash -n scripts/sync_to_hermes.sh`
- `./scripts/sync_to_hermes.sh --help`
- `./scripts/sync_to_hermes.sh --dry-run`
- YAML parse check（模板与 runtime）
- `git diff --check`
- 隐私扫描命令无命中

## Pitfalls
- Bridge 报 `Invalid token provided` 常见是占位符未替换为有效值。
- 旧会话可能缓存旧配置；必要时用新会话复验。
- `runtime.yaml` 文本改动后应做 YAML 解析校验，避免格式回归。

## Done Criteria
- 模板与脚本已入库。
- 文档联动更新完成。
- dry-run 可稳定执行。
- 未引入明文 secrets。