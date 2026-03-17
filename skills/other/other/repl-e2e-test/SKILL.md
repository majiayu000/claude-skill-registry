---
name: repl-e2e-test
description: "Run and maintain the REPL PTY-based end-to-end test after code changes. Use when implementation is complete and you need REPL E2E verification beyond unit tests, especially for output stream or prompt behavior."
---

# REPL E2E Test

## Overview

Verify REPL behavior via a PTY-driven E2E test that uses a local Anthropic SSE mock and checks that agent replies appear in the output stream.

## Workflow

1. 确认测试文件存在  
   - `tests/e2e/repl-pty.test.ts`  
   - `tests/e2e/helpers/anthropic-mock.ts`  
   - `tests/e2e/helpers/repl-pty-runner.mjs`

2. 确认依赖  
   - `node-pty` 在 `devDependencies` 中  
   - 如有变更，先执行 `bun install`

3. 运行 REPL E2E 测试  
   - `bun test tests/e2e/repl-pty.test.ts`

4. 失败处理  
   - 先阅读测试的 stderr 输出  
   - 按需查看 `references/troubleshooting.md`

## 维护要点

- 不要在生产代码中引入 `SYNAPSE_TEST_MODE`，仅允许测试代码使用环境变量。
- 若 REPL 输出提示或交互逻辑变更，需要同步更新断言文本。
- 若 CLI 入口路径变更，需要同步更新 `repl-pty-runner.mjs` 的脚本路径。

## References

- `references/troubleshooting.md`
