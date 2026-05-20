---
name: solve-issues
version: "1.0.0"
description: |
  批处理包装器 - 处理单个或多个issues的自动化解决。
  TRIGGER when: 用户要求自动解决issues（单个或批量）
  DO NOT TRIGGER when: 用户需要手动控制或特定阶段（使用独立技能）
last-updated: "2026-03-20"
---

# Solve Issues v1.0 - 批处理包装器

> 统一的issue自动化入口 - 支持单个issue直接委托和多个issues批处理

## 概述

这个技能是 `/auto-solve-issue` 的轻量级包装器，提供：

**功能：**
1. **单个issue** - 直接委托给 `/auto-solve-issue`（无包装开销）
2. **批处理** - 遍历issue列表，逐个调用 `/auto-solve-issue`
3. **进度报告** - 显示当前处理进度（[1/3], [2/3]等）
4. **错误处理** - 支持 `--stop-on-error` 和 `--continue-on-error`
5. **批处理报告** - 完成后生成汇总报告

**为什么需要这个技能：**
- ✅ 统一入口：用户只需记住一个命令
- ✅ 清晰命名：`/solve-issues`（复数）表明支持批处理
- ✅ 零重复：所有实际工作委托给 `/auto-solve-issue`
- ✅ 简化维护：包装器仅~50行代码

**何时使用：**
- 需要自动解决单个issue
- 需要批量处理多个issues
- 需要批处理报告和错误处理

**工作流：**
```bash
# 单个issue（直接委托）
/solve-issues #23
  → 委托给: /auto-solve-issue #23

# 批处理（循环调用）
/solve-issues [23, 45, 67]
  → 处理 #23: /auto-solve-issue #23
  → 处理 #45: /auto-solve-issue #45
  → 处理 #67: /auto-solve-issue #67
  → 生成批处理报告
```

## 参数

```bash
/solve-issues [issue-number-or-array] [options]
```

**常用示例：**
```bash
# 单个issue（自动模式）
/solve-issues #23

# 单个issue（交互模式）
/solve-issues #23 --interactive

# 批处理（自动模式）
/solve-issues [23, 45, 67]

# 批处理（遇到错误时停止）
/solve-issues [23, 45, 67] --stop-on-error

# 批处理（遇到错误继续）
/solve-issues [23, 45, 67] --continue-on-error

# 恢复上次执行
/solve-issues #23 --resume
```

**选项：**
- `[issue-number-or-array]` - 必需，单个issue编号或数组
- `--auto` - 自动模式（默认）- 分数 ≥90 自动继续
- `--interactive` - 在检查点停止进行手动审查
- `--stop-on-error` - 遇到错误时停止批处理（默认）
- `--continue-on-error` - 遇到错误继续处理剩余issues
- `--resume` - 从上次检查点恢复

## AI 执行指令

**关键：轻量级包装器模式**

当执行 `/solve-issues` 时，AI 必须遵循以下模式：

### 第1步：解析输入

```python
import re
import json

def parse_input(args: str) -> dict:
    """
    解析输入参数，规范化为统一格式

    Args:
        args: 命令行参数字符串

    Returns:
        {
            "issues": [23, 45, 67],  # issue编号列表
            "mode": "auto",          # "auto" 或 "interactive"
            "error_handling": "stop", # "stop" 或 "continue"
            "resume": False          # 是否恢复模式
        }
    """
    result = {
        "issues": [],
        "mode": "auto",
        "error_handling": "stop",
        "resume": False
    }

    # 检查选项标志
    if "--interactive" in args:
        result["mode"] = "interactive"
        args = args.replace("--interactive", "")

    if "--continue-on-error" in args:
        result["error_handling"] = "continue"
        args = args.replace("--continue-on-error", "")

    if "--stop-on-error" in args:
        result["error_handling"] = "stop"
        args = args.replace("--stop-on-error", "")

    if "--resume" in args:
        result["resume"] = True
        args = args.replace("--resume", "")

    # 移除 --auto（默认值）
    args = args.replace("--auto", "")

    # 解析issue编号
    args = args.strip()

    # 检测数组格式: [23, 45, 67]
    array_match = re.search(r'\[([0-9,\s]+)\]', args)
    if array_match:
        # 批处理格式
        numbers_str = array_match.group(1)
        result["issues"] = [int(n.strip()) for n in numbers_str.split(',') if n.strip()]
    else:
        # 单个issue格式: #23 或 23
        number_match = re.search(r'#?(\d+)', args)
        if number_match:
            result["issues"] = [int(number_match.group(1))]
        else:
            raise ValueError(f"无法解析issue编号: {args}")

    return result
```

**解析逻辑：**
1. **选项标志**：提取 `--interactive`, `--continue-on-error`, `--resume`
2. **Issue格式**：支持 `#23`, `23`, `[23, 45, 67]`
3. **默认值**：`--auto` 和 `--stop-on-error` 是默认行为

### 第2步：单个Issue直接委托

```python
def solve_single_issue(issue_number: int, mode: str, resume: bool):
    """
    处理单个issue - 直接委托给 /auto-solve-issue

    Args:
        issue_number: issue编号
        mode: "auto" 或 "interactive"
        resume: 是否恢复模式
    """
    # 构建命令参数
    mode_arg = f"--{mode}"
    resume_arg = "--resume" if resume else ""

    # 直接委托（使用 Skill tool）
    print(f"📋 处理 issue #{issue_number}...")

    # 调用 /auto-solve-issue
    Skill(
        skill="auto-solve-issue",
        args=f"{issue_number} {mode_arg} {resume_arg}".strip()
    )

    print(f"✅ Issue #{issue_number} 完成")
```

**关键要点：**
- ✅ 零包装开销：直接调用 `/auto-solve-issue`
- ✅ 参数透传：`--auto`/`--interactive` 和 `--resume` 传递给子技能
- ✅ 简洁实现：仅4-5行核心代码

### 第3步：批处理循环

```python
def solve_multiple_issues(
    issues: list[int],
    mode: str,
    error_handling: str
) -> dict:
    """
    处理多个issues - 循环调用 /auto-solve-issue

    Args:
        issues: issue编号列表
        mode: "auto" 或 "interactive"
        error_handling: "stop" 或 "continue"

    Returns:
        批处理结果 {
            "total": 3,
            "succeeded": 2,
            "failed": 1,
            "results": [
                {"issue": 23, "status": "success"},
                {"issue": 45, "status": "failed", "error": "..."},
                {"issue": 67, "status": "success"}
            ]
        }
    """
    total = len(issues)
    results = []

    print(f"\n📦 批处理模式：处理 {total} 个issues")
    print(f"   错误处理策略：{error_handling}")
    print(f"   执行模式：{mode}\n")

    for idx, issue_number in enumerate(issues, 1):
        print(f"\n{'='*60}")
        print(f"📋 [{idx}/{total}] 处理 issue #{issue_number}")
        print(f"{'='*60}\n")

        try:
            # 调用 /auto-solve-issue
            mode_arg = f"--{mode}"

            Skill(
                skill="auto-solve-issue",
                args=f"{issue_number} {mode_arg}"
            )

            # 记录成功
            results.append({
                "issue": issue_number,
                "status": "success"
            })

            print(f"\n✅ [{idx}/{total}] Issue #{issue_number} 完成")

        except Exception as e:
            # 记录失败
            error_msg = str(e)
            results.append({
                "issue": issue_number,
                "status": "failed",
                "error": error_msg
            })

            print(f"\n❌ [{idx}/{total}] Issue #{issue_number} 失败: {error_msg}")

            # 根据错误处理策略决定是否继续
            if error_handling == "stop":
                print(f"\n⏸️ 遇到错误停止（--stop-on-error）")
                print(f"   已处理：{idx}/{total} issues")
                print(f"   剩余未处理：{total - idx} issues")
                break
            else:
                print(f"\n⚠️ 继续处理剩余issues（--continue-on-error）")
                continue

    # 计算统计
    succeeded = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")

    return {
        "total": total,
        "succeeded": succeeded,
        "failed": failed,
        "results": results
    }
```

**批处理逻辑：**
1. **进度显示**：`[1/3]`, `[2/3]`, `[3/3]`
2. **错误处理**：
   - `--stop-on-error`：第一个错误时停止
   - `--continue-on-error`：记录错误，继续处理
3. **结果收集**：每个issue的状态和错误信息

### 第4步：生成批处理报告

```python
def generate_batch_report(batch_result: dict):
    """
    生成批处理完成报告

    Args:
        batch_result: 从 solve_multiple_issues() 返回的结果
    """
    total = batch_result["total"]
    succeeded = batch_result["succeeded"]
    failed = batch_result["failed"]
    results = batch_result["results"]

    print(f"\n{'='*60}")
    print(f"📊 批处理报告")
    print(f"{'='*60}\n")

    print(f"总计：{total} issues")
    print(f"✅ 成功：{succeeded}")
    print(f"❌ 失败：{failed}")
    print(f"成功率：{(succeeded/total*100):.1f}%\n")

    # 详细结果列表
    if succeeded > 0:
        print(f"✅ 成功的issues：")
        for r in results:
            if r["status"] == "success":
                print(f"   - Issue #{r['issue']}")
        print()

    if failed > 0:
        print(f"❌ 失败的issues：")
        for r in results:
            if r["status"] == "failed":
                print(f"   - Issue #{r['issue']}")
                print(f"     错误: {r['error']}")
        print()

    print(f"{'='*60}\n")
```

**报告格式：**
```
============================================================
📊 批处理报告
============================================================

总计：3 issues
✅ 成功：2
❌ 失败：1
成功率：66.7%

✅ 成功的issues：
   - Issue #23
   - Issue #67

❌ 失败的issues：
   - Issue #45
     错误: Checkpoint 1 score 75 < 90

============================================================
```

### 第5步：主入口逻辑

```python
# 解析输入参数
config = parse_input(args)

issues = config["issues"]
mode = config["mode"]
error_handling = config["error_handling"]
resume = config["resume"]

# 判断单个还是批处理
if len(issues) == 1:
    # 单个issue - 直接委托
    solve_single_issue(issues[0], mode, resume)

else:
    # 批处理 - 循环处理
    batch_result = solve_multiple_issues(issues, mode, error_handling)

    # 生成报告
    generate_batch_report(batch_result)
```

**执行流程：**
1. **解析输入**：提取issues列表和选项
2. **路径选择**：
   - 单个issue → 直接委托
   - 多个issues → 批处理循环
3. **报告生成**：批处理完成后显示汇总

## 架构

### 关系图

```
用户
  ↓ 调用
/solve-issues (包装器)
  ↓ 委托（单个）或循环（批处理）
/auto-solve-issue (核心实现)
  ↓ 使用
Task系统 + Subagents
```

### 与其他技能的比较

| 技能 | 用途 | 代码量 | 复杂度 |
|------|------|--------|--------|
| **/solve-issues** | 批处理包装器 | ~50行 | 低 |
| **/auto-solve-issue** | 核心实现 | ~200行 | 中 |
| **/work-issue** (已删除) | 旧实现 | ~300行 | 高 |

**设计理念：**
- ✅ 单一职责：包装器只负责批处理逻辑
- ✅ 委托模式：实际工作由 `/auto-solve-issue` 完成
- ✅ 简洁维护：包装器代码极简，易于理解

## 工作流步骤

复制此清单以跟踪进度：

```
单个Issue：
- [ ] 解析输入参数
- [ ] 委托给 /auto-solve-issue
- [ ] 完成

批处理：
- [ ] 解析输入参数
- [ ] 循环处理每个issue
- [ ] 显示进度 ([1/N], [2/N], ...)
- [ ] 处理错误（stop/continue）
- [ ] 生成批处理报告
```

## 示例

### 示例1：单个Issue（自动模式）

**用户：** `/solve-issues #23`

**执行流程：**
1. 解析：`issues=[23], mode="auto"`
2. 路径：单个issue → 直接委托
3. 调用：`/auto-solve-issue 23 --auto`
4. 完成

**耗时：** 35-65分钟（与 `/auto-solve-issue` 相同）

### 示例2：批处理（自动模式）

**用户：** `/solve-issues [23, 45, 67]`

**执行流程：**
```
📦 批处理模式：处理 3 个issues
   错误处理策略：stop
   执行模式：auto

============================================================
📋 [1/3] 处理 issue #23
============================================================
（/auto-solve-issue #23 执行）
✅ [1/3] Issue #23 完成

============================================================
📋 [2/3] 处理 issue #45
============================================================
（/auto-solve-issue #45 执行）
✅ [2/3] Issue #45 完成

============================================================
📋 [3/3] 处理 issue #67
============================================================
（/auto-solve-issue #67 执行）
✅ [3/3] Issue #67 完成

============================================================
📊 批处理报告
============================================================

总计：3 issues
✅ 成功：3
❌ 失败：0
成功率：100.0%

✅ 成功的issues：
   - Issue #23
   - Issue #45
   - Issue #67

============================================================
```

**耗时：** 105-195分钟（3个issues × 35-65分钟）

### 示例3：批处理（遇到错误停止）

**用户：** `/solve-issues [23, 45, 67] --stop-on-error`

**执行流程：**
```
📦 批处理模式：处理 3 个issues
   错误处理策略：stop

============================================================
📋 [1/3] 处理 issue #23
============================================================
✅ [1/3] Issue #23 完成

============================================================
📋 [2/3] 处理 issue #45
============================================================
❌ [2/3] Issue #45 失败: Checkpoint 1 score 75 < 90

⏸️ 遇到错误停止（--stop-on-error）
   已处理：2/3 issues
   剩余未处理：1 issues

============================================================
📊 批处理报告
============================================================

总计：3 issues
✅ 成功：1
❌ 失败：1
成功率：50.0%

❌ 失败的issues：
   - Issue #45
     错误: Checkpoint 1 score 75 < 90

============================================================
```

### 示例4：批处理（遇到错误继续）

**用户：** `/solve-issues [23, 45, 67] --continue-on-error`

**执行流程：**
```
📦 批处理模式：处理 3 个issues
   错误处理策略：continue

============================================================
📋 [1/3] 处理 issue #23
============================================================
✅ [1/3] Issue #23 完成

============================================================
📋 [2/3] 处理 issue #45
============================================================
❌ [2/3] Issue #45 失败: Checkpoint 1 score 75 < 90

⚠️ 继续处理剩余issues（--continue-on-error）

============================================================
📋 [3/3] 处理 issue #67
============================================================
✅ [3/3] Issue #67 完成

============================================================
📊 批处理报告
============================================================

总计：3 issues
✅ 成功：2
❌ 失败：1
成功率：66.7%

✅ 成功的issues：
   - Issue #23
   - Issue #67

❌ 失败的issues：
   - Issue #45
     错误: Checkpoint 1 score 75 < 90

============================================================
```

## 性能

| 指标 | 单个Issue | 批处理（3个） |
|------|-----------|---------------|
| **执行时间** | 35-65分钟 | 105-195分钟 |
| **用户干预** | 仅检查点 | 仅检查点 |
| **包装开销** | ~0ms | 每个issue ~10ms |
| **上下文使用** | <50k tokens | <150k tokens |

**批处理效率：**
- ✅ 自动化：无需手动切换issues
- ✅ 报告：一次性查看所有结果
- ✅ 灵活：支持遇错停止或继续

## 错误处理

**单个issue失败：**
```
❌ Issue #23 失败: Checkpoint 1 score 75 < 90

选项：
1. 修复：手动修复issue #23的问题
2. 恢复：/solve-issues #23 --resume
3. 跳过：不处理此issue
```

**批处理部分失败：**
```
📊 批处理报告

总计：3 issues
✅ 成功：2
❌ 失败：1

❌ 失败的issues：
   - Issue #45
     错误: Checkpoint 1 score 75 < 90

下一步：
1. 修复失败的issue #45
2. 重新处理：/solve-issues #45
```

## 集成

**迁移自 /work-issue：**

| 旧命令 | 新命令 |
|--------|--------|
| `/work-issue #23` | `/solve-issues #23` 或 `/auto-solve-issue #23` |
| `/work-issue [23, 45]` | `/solve-issues [23, 45]` |
| `/work-issue #23 --interactive` | `/solve-issues #23 --interactive` |
| `/work-issue #23 --auto` | `/solve-issues #23` （默认） |

**何时使用哪个技能：**

| 需求 | 使用技能 |
|------|----------|
| 单个issue自动化 | `/solve-issues` 或 `/auto-solve-issue` |
| 批量处理issues | `/solve-issues [...]` |
| 手动控制阶段 | 独立技能（`/start-issue`, `/execute-plan`等） |

## 最佳实践

1. **单个issue优先使用直接调用** - `/auto-solve-issue` 或 `/solve-issues`（无区别）
2. **批处理使用 --continue-on-error** - 避免因单个失败影响整体
3. **检查批处理报告** - 总结所有成功和失败的issues
4. **失败后单独处理** - 批处理失败的issue可单独重新运行
5. **信任分数** - 自动模式依赖eval-plan/review分数（≥90）

## 任务管理

此技能不创建Task（委托给 `/auto-solve-issue`，由其管理Task）。

## 最终验证

```
单个Issue：
- [ ] /auto-solve-issue 正确调用
- [ ] 参数正确传递
- [ ] 执行成功

批处理：
- [ ] 所有issues正确遍历
- [ ] 进度显示准确
- [ ] 错误处理符合配置
- [ ] 批处理报告生成
```

## 相关技能

- **/auto-solve-issue** - 核心实现（被此技能调用）
- **/start-issue** - 阶段1（由 `/auto-solve-issue` 调用）
- **/eval-plan** - 阶段1.5（由 `/auto-solve-issue` 调用）
- **/execute-plan** - 阶段2（由 `/auto-solve-issue` 调用）
- **/review** - 阶段2.5（由 `/auto-solve-issue` 调用）
- **/finish-issue** - 阶段3（由 `/auto-solve-issue` 调用）

## 迁移指南（从 /work-issue）

**重大变更：**
- ❌ `/work-issue` 已删除
- ❌ `/solve-issue` 已删除
- ✅ 使用 `/solve-issues`（新）或 `/auto-solve-issue`（核心）

**迁移步骤：**
1. 更新所有引用：`/work-issue` → `/solve-issues`
2. 检查参数：大部分兼容，除了 `--stop-after`（已移除）
3. 测试：在小issue上验证新工作流

**功能对比：**

| 功能 | /work-issue (旧) | /solve-issues (新) |
|------|------------------|-------------------|
| 单个issue | ✅ | ✅ |
| 批处理 | ✅ | ✅ |
| 自动模式 | ✅ | ✅ |
| 交互模式 | ✅ | ✅ |
| --stop-after | ✅ | ❌ (使用独立技能) |
| 错误处理 | 基本 | 增强（stop/continue） |
| 批处理报告 | 无 | ✅ |

---

**Version:** 1.0.0
**Last Updated:** 2026-03-20
**Changelog:**
- v1.0.0 (2026-03-20): Initial release - batch wrapper for auto-solve-issue with enhanced error handling

**Pattern:** Batch Processing Wrapper
**Status:** Stable
**Compliance:** ADR-001 ✅
