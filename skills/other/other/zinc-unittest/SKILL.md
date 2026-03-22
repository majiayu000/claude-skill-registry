---
name: zinc-unittest
description: War3Lib 的 Zinc 单元测试流程规范（.j + .cfg + _Test.j + 可选 w3a/w3u/w3i）：使用 TaskCreateUT.lua 生成测试壳、维护 cfg 注入与 chain 依赖、使用 UnitTestFramwork.assert 断言与 Trace 日志输出。用于创建/重构 Jass 模块单测时。
---

# Zinc Unit Test Workflow (War3Lib)

按以下顺序执行，保持最小改动和可复现。

## 1. 建立三件套文件

1. 以目标模块 `Xxx.j` 为中心，确认同目录存在：`Xxx.cfg`、`Xxx_Test.j`。
2. `Xxx.cfg` 不存在时创建，并补齐：公开 API 关键词 + `[chain]` 基础依赖。
3. 需要物编辅助测试时，按需创建同名扩展文件：`Xxx.w3a`(技能)、`Xxx.w3u`(单位)、`Xxx.w3i`(物品)。

说明：`cfg` 前半段用于外部 dependency 注入关键词；`[chain]` 是该库底层依赖，用于递归注入。

## 2. 生成或刷新 `_Test.j`（必须走任务脚本）

优先复用项目脚本，不手写测试壳。

1. 运行：`bash .codex/skills/zinc-unittest/scripts/create_ut.sh <Xxx.j>`。
2. 该流程会调用 `Lua/tasks/TaskCreateUT.lua`，并使用模板 `Jass/template/UTTemplate.j`。
3. 已存在 `_Test.j` 时默认不覆盖，仅更新 `Jass/config/UnitTest.h` 的 include 到当前测试文件。

如果脚本不可用，再手动按 `UTTemplate.j` 结构补齐占位符：`{UnitTest}`、`LibraryName`、`#include`。

## 3. 编写测试逻辑（参考 UnitUtils 风格）

1. 在 `library UTXxx requires Xxx,...` 中按功能拆分 `Test_*` 私有函数。
2. 使用 `UnitTestAutoTimer` 安排自动测试，避免初始化竞争。
3. 聊天命令入口走 `s1..s10` 或 `-参数`，复用模板函数 `TTestUTXxx*` / `TTestActUTXxx1`。
4. 断言优先使用 `UnitTestFramwork.assert`：`Boolean/Integer/Real/String`。
5. 需要输出到日志时优先用 `Trace(...)`（YDLua），不要依赖仅本地可见的原生提示。

## 4. 宏保护与命名

1. 测试专用注册与入口放在测试文件中；若写在业务库，必须加：`#if (CURRENT_BUILD_VERSION != VERSION_RELEASE)`。
2. 不使用 `_` 开头标识符。
3. 用模块名前缀组织测试名与提示文案，保证日志可检索。

## 5. 验收检查

1. `Xxx.cfg` 关键词覆盖公开能力；`[chain]` 不漏基础库。
2. `_Test.j` 可独立触发核心断言，失败日志能定位到具体测试。
3. 若依赖物编，`Xxx.w3a/w3u/w3i` 与测试步骤匹配，并在说明中写出用途。

## References（按需加载）

- `references/ut-file-layout.md`
- `references/assert-trace-pattern.md`
- `references/examples.md`
