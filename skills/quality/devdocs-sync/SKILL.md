---
name: devdocs-sync
description: Sync documentation with implementation progress. Use when users need to update docs after development, verify doc-code consistency, or track implementation progress. Triggers on keywords like "sync docs", "update progress", "doc consistency", "同步文档", "更新进度".
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion
---

# 文档同步

保持 DevDocs 文档与实际实现进度一致，检测偏差并更新状态。

## 语言规则

- 支持中英文提问
- 统一中文回复
- 使用中文生成文档

## 触发条件

- 用户完成一个或多个开发任务后
- 用户要求检查文档与代码一致性
- 用户需要更新文档进度
- 定期同步（如 Sprint 结束时）

## 运行模式

```
/devdocs-sync                    → 完整同步（检查 + 确认 + 更新）
/devdocs-sync --check            → 仅检查，不更新文档
/devdocs-sync --absorb           → 吸收模式（自动 + 智能补齐）
/devdocs-sync --trace            → 代码追溯扫描（更新矩阵代码位置）
/devdocs-sync --archive          → 强制归档已完成任务
/devdocs-sync --audit            → 追溯健康度检查
/devdocs-sync T-01 T-02          → 指定范围同步
```

### 模式对比

| 模式 | 检查 | 自动更新 | 智能补齐 | 用户确认 |
|------|------|----------|----------|----------|
| check | ✅ | ❌ | ❌ | ❌ |
| sync（默认） | ✅ | ✅ | ❌ | ✅ 全部 |
| absorb | ✅ | ✅ | ✅ | ✅ 仅高风险 |
| trace | ✅ 代码扫描 | ✅ 矩阵 | ❌ | ❌ |
| audit | ✅ 追溯 | ❌ | ❌ | ❌ |

## 核心理念

### 文档与代码的关系

```
文档定义（计划）          代码实现（实际）
     │                        │
     ├── F-XXX 功能点    ←→   ├── 功能模块
     ├── AC-XXX 验收标准 ←→   ├── 业务逻辑
     ├── T-XX 开发任务   ←→   ├── 代码提交
     └── UT/IT/E2E 测试  ←→   └── 测试文件
```

**核心原则**：
- 文档是计划，代码是实现
- 偏差是正常的，关键是及时同步
- 同步应该双向：文档→代码（指导）、代码→文档（记录）

### 同步时机

| 时机 | 同步内容 |
|------|----------|
| 任务完成后 | 更新任务状态、测试结果 |
| Sprint 结束 | 全量检查、进度报告 |
| 需求变更后 | 更新需求文档、影响分析 |
| 代码审查后 | 记录设计决策变更 |

## 工作流程

```
1. 读取 DevDocs 文档
   │
   ▼
2. 扫描代码库（工作区状态）
   ├── 检查文件是否存在（Glob）
   ├── 运行测试（获取实时结果）
   ├── 检查未提交变更（git status）
   └── 参考提交记录（git log，辅助）
   │
   ▼
3. 对比分析
   ├── 任务完成状态
   ├── 测试覆盖情况
   └── 功能实现状态
   │
   ▼
4. 生成偏差报告
   │
   ▼
5. 询问用户确认更新
   │
   ▼
6. 更新文档
```

**重要**：检查基于**当前工作区状态**，而非仅依赖 git 提交历史。

## 模式详解

### 吸收模式 (--absorb)

从"检查员"进化为"记录员"，支持代码优先开发路径。低风险偏差自动吸收，高风险需确认。

详见 [absorb-mode.md](absorb-mode.md)

### 追溯健康度检查 (--audit)

检测编号体系完整性，防止文档维护债积累。检查 AC 覆盖、F 任务闭环、INS 转化、孤立编号。

详见 [audit-mode.md](audit-mode.md)

### 代码追溯扫描 (--trace)

扫描代码中的 `@satisfies`/`@verifies` 标注，与文档交叉验证，更新追溯矩阵代码位置列。

详见 [trace-mode.md](trace-mode.md)

### 任务归档

当已完成任务过多时自动建议归档，保持主文档简洁。

详见 [archive.md](archive.md)

## 同步命令

### 快速检查

```bash
/devdocs-sync --check
# 输出: 偏差报告（仅显示，不写入）
```

### 完整同步

```bash
/devdocs-sync
# 流程: 检查 → 显示报告 → 确认 → 更新文档
```

### 吸收模式

```bash
/devdocs-sync --absorb
# 流程: 检查 → 自动吸收低风险 → 确认高风险 → 生成报告
```

### 指定范围

```bash
/devdocs-sync T-01 T-02
# 只同步特定任务
```

## 输出文件

### 进度报告

生成 `docs/devdocs/00-progress-report.md`，包含总体进度、偏差汇总、下一步建议。

### 文档更新

| 文档 | 更新内容 |
|------|----------|
| `04-dev-tasks.md` | 任务完成状态、执行检查清单 |
| `03-test-cases.md` | 追溯矩阵状态、测试通过状态 |
| `01-requirements.md` | 功能点实现状态（如有状态列） |

## 约束

### 检查约束

- [ ] **必须读取所有 DevDocs 文档后再进行检查**
- [ ] **必须生成偏差报告**
- [ ] **更新文档前必须询问用户确认**（吸收模式低风险除外）
- [ ] 检查结果必须可追溯（显示检查方法）

### 更新约束

- [ ] **不自动删除文档内容，只标记状态**
- [ ] **不自动修改代码，只更新文档**
- [ ] 保留原有文档结构
- [ ] 更新时记录时间戳

### 吸收模式约束

- [ ] **低风险吸收仅限状态字段更新**
- [ ] **高风险吸收必须用户确认**
- [ ] 新增内容必须指定关联编号（AC/F/US）
- [ ] 无法确定关联的内容标记为"待手动处理"
- [ ] 吸收操作必须生成吸收报告

### 安全约束

- [ ] 不执行未知的 shell 命令
- [ ] 测试命令使用项目配置的命令
- [ ] 大规模更新前必须确认

## Skill 协作

| 场景 | 协作 Skill | 说明 |
|------|-----------|------|
| 开发完成 | `/devdocs-dev-workflow` | 被调用：任务完成后触发 --trace |
| 任务完成后 | `/devdocs-dev-tasks` | 执行任务后触发同步 |
| 测试追溯 | `/devdocs-test-cases` | 协作：更新追溯矩阵代码位置 |
| 需求变更 | `/devdocs-feature` | 新功能添加后同步 |
| Bug 修复 | `/devdocs-bugfix` | Bug 修复后更新文档 |
| 洞察确认 | `/devdocs-insights` | 改进建议确认后同步 |
| 项目改造 | `/devdocs-retrofit` | 改造后全量同步 |

## 参考资料

- [absorb-mode.md](absorb-mode.md) - 吸收模式详解
- [audit-mode.md](audit-mode.md) - 追溯健康度检查
- [trace-mode.md](trace-mode.md) - 代码追溯扫描
- [archive.md](archive.md) - 任务归档功能
- [examples.md](examples.md) - 使用示例与偏差类型

## 偏差修复路由（调度器功能）

当检测到偏差时，必须在报告中指派下一步修复 Skill：

| 偏差类型 | 修复 Skill | 说明 |
|----------|-----------|------|
| 设计缺失/漂移 | `/devdocs-system-design` | 代码有新接口但文档未记录 |
| AC 缺测试 | `/devdocs-test-cases` | 验收标准无对应测试用例 |
| F 缺任务闭环 | `/devdocs-dev-tasks` | 功能点无关联开发任务 |
| 代码已实现文档落后 | `/devdocs-sync --absorb` | 状态未更新、新内容未登记 |
| 追溯矩阵代码位置缺失 | `/devdocs-sync --trace` | 代码标注未扫描到矩阵 |

> **调度器原则**：偏差报告不能只列出问题，必须给出明确的修复路由。

## 调用顺序建议

任务完成后的推荐顺序：

```
/devdocs-sync --trace    # 1. 先更新追溯矩阵代码位置
        │
        ▼
/devdocs-sync            # 2. 再检查整体状态并更新
  或 --absorb            #    （absorb 自动包含 trace 步骤）
```

> `--trace` 专注于代码标注扫描，`--absorb` 专注于状态吸收。两者可独立使用，也可组合使用。

## 下一步

同步完成后，根据进度报告中的**偏差修复路由**执行对应 Skill。
