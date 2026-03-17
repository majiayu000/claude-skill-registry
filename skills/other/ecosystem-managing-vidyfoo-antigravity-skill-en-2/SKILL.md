---
name: ecosystem-managing
description: 系统生态工程师 - 发布(Release) | 维护(Maintain) | 清理(Purge)
---

# Ecosystem Engineer Skill (v2.0)

> **Role**: 系统园丁。负责代码库的健康、发布与新陈代谢。

---

## 模式选择

| 模式 | 触发词 | 职责 | 原 Workflow |
|------|--------|------|-------------|
| **RELEASE** | 发布, 发版, release | 语义化版本发布与变更日志生成 | `/11.release` |
| **PURGE** | 清理, 删除, 移除, purge | 安全地移除过时功能或死代码 | `/13.purge` |
| **HANDOFF** | 交接, 接手, handoff | 生成交接文档，降低认知负荷 | `/2.handoff` |

---

## 1. RELEASE 协议

1.  **版本决策**: 
    *   Breaking Changes -> Major
    *   New Features -> Minor
    *   Fixes -> Patch
2.  **更新 Changelog**: 
    *   读取 `CHANGELOG.md`
    *   使用 `resources/changelog-template.md` 格式追加新条目。
3.  **更新版本号**: `package.json`

## 2. PURGE 协议

1.  **影响分析**: 使用 `grep_search` 找出所有引用。
2.  **备份策略**: 大规模删除前建议 Commit 或提示用户备份。
3.  **执行删除**: 代码 + 文档 + 测试。
4.  **验证**: `npm run build` 确保没有断链。

## 3. HANDOFF 协议

1.  **知识快照**: 总结当前系统状态、未决问题和关键决策。
2.  **生成文档**: 更新 `doc/explanation/architecture.md` 或创建 `doc/handoffs/YYYY-MM-DD.md`。

---

## 资源索引

| 资源文件 | 用途 |
|----------|------|
| [changelog-template.md](resources/changelog-template.md) | 标准化变更日志格式 |
