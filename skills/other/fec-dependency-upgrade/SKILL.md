---
name: fec-dependency-upgrade
description: 用于规划、实现或审查前端依赖升级、包迁移、lockfile 变更、框架大版本升级、CVE 修复、peer dependency 冲突、ESM/CJS 切换、构建工具兼容性或 CI 验证矩阵；中文触发词包括 依赖升级、版本升级、lockfile、peer dependency、CVE 修复、大版本迁移。
---

# 依赖升级

适用于前端依赖升级、漏洞修复、大版本迁移和 lockfile 风险评审。需要具体流程和检查清单时加载 [references/dependency-upgrade-workflow.md](references/dependency-upgrade-workflow.md)。

## 用途

用来源驱动和小批验证的方式升级依赖，降低破坏性变更、供应链风险和 CI 回归。

## 流程

1. 建立事实基线：读取 package manager、lockfile、Node 版本、workspace 范围、CI 命令和当前验证状态。
2. 分类升级目标：安全修复、补丁升级、小版本升级、大版本迁移、框架迁移、构建工具迁移或依赖清理。
3. 查证来源：对版本敏感的库读取官方 release notes、migration guide、peer dependency、Node/browser 支持和弃用项。
4. 拆小批次：安全补丁可集中处理；大版本、构建工具、框架和测试工具必须单独批次验证。
5. 处理兼容边界：检查 ESM/CJS、TypeScript 类型、CSS 处理、SSR/RSC、插件 API、peer dependency 和 polyfill 变化。
6. 运行验证矩阵：至少覆盖 install、typecheck、unit/component tests、build；关键应用补 E2E、Storybook 或手工冒烟。
7. 同步文档：记录升级原因、版本、破坏性变更、迁移命令、回滚方式和仍需人工验证的路径。

## 约束

- 不在缺少来源和验证的情况下进行大版本连跳。
- 不为了消除 audit 警告盲目升级运行时关键包；先判断可利用路径和修复影响。
- 不手工编辑 lockfile 规避依赖冲突。
- 不把依赖升级和无关重构混在一个批次。
- 不移除 peer dependency 或构建插件，除非有证据证明没有被运行时、子包或 CI 使用。

## 预期输出

输出升级清单、风险分类、来源依据、批次策略、修改范围、验证命令、失败处理和回滚建议。完成后 lockfile 与 package 清单一致，关键验证通过，破坏性变更有记录。
