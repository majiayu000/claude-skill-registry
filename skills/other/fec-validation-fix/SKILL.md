---
name: fec-validation-fix
description: Use when running existing project validation commands and fixing failures after code changes, including lint, type-check, unit/integration test, build, CI, or local script failures. Do not use when the task is to design or author new component/E2E tests; Chinese triggers include 验证, 检查失败, 修复失败, CI 失败.
---

# 验证并修复

## Purpose

自动化执行已有验证命令，分析失败原因并安全修复，确保质量门禁达标。

## Procedure

1. 从 package.json 或仓库文档中识别可用命令。
2. 优先按以下顺序执行：
   - lint
   - type-check
   - unit/integration tests
   - build
3. 仔细阅读失败输出。
4. 将错误按文件、错误类型和依赖关系分组，优先处理阻塞后续诊断的根因。
5. 一次只修复一类问题，并显示或记录关键错误上下文。
6. 每次关键修复后重新执行受影响命令，确认错误是否减少。
7. 如果同一错误连续三次修复仍失败，停止扩大改动并报告阻塞。
8. 最后按 `Expected Output` 总结执行结果、修复内容和剩余风险。

## Failure Triage

- 先修最早出现且会级联的错误，例如缺失类型、导入失败、配置解析失败。
- 区分真实产品 bug、测试环境问题、快照漂移、依赖版本变化和 flaky。
- 对 CI 专属失败记录 Node 版本、包管理器、环境变量、路径大小写和工作目录差异。
- 修复测试时优先修产品代码或测试等待方式，不用删除断言掩盖真实回归。

## 强约束

- 不要盲目关闭规则来消除报错
- 除非有明确理由，不要为了通过检查而降低类型安全
- 不要因为附近测试失败就顺手重写无关模块
- 不要一次性修改多个无关根因
- 不要删除失败测试来让验证通过
- 不要只运行失败命令的片段就声称整体验证通过

## Expected Output

- lint / type-check / test / build 等验证命令全部通过
- 失败项已修复或给出明确原因和后续行动
- 修复报告保存为 `reports/validation-fix-YYYY-MM-DD-HHmmss.md`
- 报告包含命令状态表、问题根因、修复说明、变更文件和剩余风险
