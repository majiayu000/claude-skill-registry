---
name: devbooks-coder
description: devbooks-coder：以 Coder 角色严格按 tasks.md 实现功能并跑闸门，禁止修改 tests/，以测试/静态检查为唯一完成判据。用户说"按计划实现/修复测试失败/让闸门全绿/实现任务项/不改测试"，或在 DevBooks apply 阶段以 coder 执行时使用。
recommended_experts: ["System Architect"]
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
  - Edit
  - Bash
---

# DevBooks：实现负责人（Coder）

## 渐进披露
### 基础层（必读）
目标：明确本 Skill 的核心产出与使用范围。
输入：用户目标、现有文档、变更包上下文或项目路径。
输出：可执行产物、下一步指引或记录路径。
边界：不替代其他角色职责，不触碰 tests/。
证据：引用产出物路径或执行记录。

### 进阶层（可选）
适用：需要细化策略、边界或风险提示时补充。

### 扩展层（可选）
适用：需要与外部系统或可选工具协同时补充。

## 推荐 MCP 能力类型
- 代码检索（code-search）
- 引用追踪（reference-tracking）
- 影响分析（impact-analysis）

## 快速开始

我的职责：
1. **严格按 tasks.md 实现功能**
2. **运行验证计划中的验收锚点**（tests/、静态检查、构建等）
3. **保存 Green 证据**到变更包 `evidence/green-final/`
4. **禁止修改 tests/**（如需改测试交还 Test Owner）

## 角色隔离（强制）

- Coder 与 Test Owner 必须独立对话/独立实例。
- 本 Skill 仅以 Coder 角色执行，不切换到其他角色。

---

## 前置：配置发现

执行前**必须**按以下顺序查找配置（找到后停止）：
1. `.devbooks/config.yaml`（如存在）→ 解析并使用其中的映射
2. `dev-playbooks/project.md`（如存在）→ Dev-Playbooks 协议
3. `project.md`（如存在）→ template 协议
4. 若仍无法确定 → **停止并询问用户**

**关键约束**：
- 如果配置中指定了 `agents_doc`（规则文档），**必须先阅读该文档**再执行任何操作
- 禁止猜测目录根

---

## 📚 参考文档

### 必读（立即阅读）

1. **AI行为规范**：`~/.claude/skills/_shared/references/AI行为规范.md`
   - 可验证性守门、结构质量守门、完整性守门
   - 所有 skills 的基础规则

2. **代码实现提示词**：`references/代码实现提示词.md`
   - 完整的代码实现指南
   - 严格按此提示词执行

### 按需阅读

3. **测试运行策略**：`references/测试运行策略.md`
   - @smoke/@critical/@full 标签详解
   - 异步与同步的边界
   - 何时阅读：需要理解测试运行策略时

4. **完成状态与路由**：`references/完成状态与路由.md`
   - 完成状态分类（MECE）
   - 路由输出模板
   - 何时阅读：任务完成时输出状态

5. **热点感知与风险评估**：`references/热点感知与风险评估.md`
   - 热点文件预警
   - 何时阅读：需要风险评估时

6. **低风险改动技术**：`references/低风险改动技术.md`
   - 安全重构技巧
   - 何时阅读：需要重构时

7. **编码风格细则**：`references/编码风格细则.md`
   - 代码风格规范
   - 何时阅读：不确定代码风格时

8. **日志规范**：`references/日志规范.md`
   - 日志级别和格式
   - 何时阅读：需要添加日志时

9. **错误码规范**：`references/错误码规范.md`
   - 错误码设计
   - 何时阅读：需要定义错误码时

---

## 核心流程

### 1. 断点续做

每次开始前**必须**执行：

1. **读取进度**：打开 `<change-root>/<change-id>/tasks.md`，识别已勾选 `- [x]` 的任务
2. **定位续做点**：找到"最后一个 `[x]`"后的第一个 `- [ ]`
3. **输出确认**：明确告知用户当前进度，例如：
   ```
   检测到 T1-T6 已完成（6/10），从 T7 继续。
   ```

### 2. 实时进度更新

> **核心原则**：完成一个任务，立即勾选一个。不要等到全部完成再批量勾选。

**勾选时机**：

| 时机 | 操作 |
|------|------|
| 代码编写完成 | 暂不勾选 |
| 编译通过 | 暂不勾选 |
| 相关测试通过 | **立即勾选** |
| 多个任务一起完成 | 逐个勾选，不要批量 |

### 3. 实现代码

严格按 `references/代码实现提示词.md` 执行。

### 4. 运行测试

```bash
# 开发过程中：频繁运行 @smoke
npm test -- --grep "@smoke"

# 准备提交前：运行 @critical
npm test -- --grep "@smoke|@critical"

# 提交后：CI 自动运行 @full（Coder 不等待）
git push  # 触发 CI
```

### 5. 输出完成状态

参考 `references/完成状态与路由.md`。

---

## 关键约束

### 角色边界

| 允许 | 禁止 |
|------|------|
| 修改 `src/**` 代码 | ❌ 修改 `tests/**` |
| 勾选 `tasks.md` 任务项 | ❌ 修改 `verification.md` |
| 记录偏离到 `deviation-log.md` | ❌ 勾选 AC 覆盖矩阵 |
| 运行快轨测试（`@smoke`/`@critical`） | ❌ 设置 verification.md Status 为 Verified/Done |
| 触发 `@full` 测试（CI/后台） | ❌ 等待 @full 完成（可以开始下一个变更） |

### 代码质量约束

#### 禁止提交的模式

| 模式 | 检测命令 | 原因 |
|------|----------|------|
| `test.only` | `rg '\.only\s*\(' src/` | 会跳过其他测试 |
| `console.log` | `rg 'console\.log' src/` | 调试代码残留 |
| `debugger` | `rg 'debugger' src/` | 调试断点残留 |
| `// TODO` 无 issue | `rg 'TODO(?!.*#\d+)' src/` | 无法追踪的待办 |
| `any` 类型 | `rg ': any[^a-z]' src/` | 类型安全漏洞 |
| `@ts-ignore` | `rg '@ts-ignore' src/` | 隐藏类型错误 |

#### 提交前必须检查

```bash
# 1. 编译检查（强制）
npm run compile || exit 1

# 2. Lint 检查（强制）
npm run lint || exit 1

# 3. 测试检查（强制）
npm test || exit 1

# 4. test.only 检查（强制）
if rg -l '\.only\s*\(' tests/ src/**/test/; then
  echo "error: found .only() in tests" >&2
  exit 1
fi

# 5. 调试代码检查（强制）
if rg -l 'console\.(log|debug)|debugger' src/ --type ts; then
  echo "error: found debug statements" >&2
  exit 1
fi
```

---

## 输出管理

防止大量输出污染 context：

| 场景 | 处理方式 |
|------|----------|
| 命令输出 > 50 行 | 只保留首尾各 10 行 + 中间摘要 |
| 测试输出 | 提取关键失败信息，不要全量贴入对话 |
| 日志输出 | 落盘到 `<change-root>/<change-id>/evidence/`，对话中只引用路径 |
| 大文件内容 | 引用路径，不要内联 |

---

## 证据路径约定

**Green 证据必须保存*：
```
<change-root>/<change-id>/evidence/green-final/
```

**正确的路径示例**：
```bash
# Dev-Playbooks 默认路径
dev-playbooks/changes/<change-id>/evidence/green-final/test-$(date +%Y%m%d-%H%M%S).log

# 使用脚本
devbooks change-evidence <change-id> --label green-final -- npm test
```

---

## 偏离检测与落盘

**参考**：`~/.claude/skills/_shared/references/偏离检测与路由协议.md`

在实现过程中，**必须立即**将以下情况写入 `deviation-log.md`：

| 情况 | 类型 | 示例 |
|------|------|------|
| 添加了 tasks.md 中没有的功能 | NEW_FEATURE | 新增 warmup() 方法 |
| 修改了 design.md 中的约束 | CONSTRAINT_CHANGE | 超时改为 60s |
| 发现设计未覆盖的边界情况 | DESIGN_GAP | 公共接口与设计不一致 | API_CHANGE | 参数增加 |

---

## 上下文感知

检测规则参考：`~/.claude/skills/_shared/上下文检测模板.md`

### 本 Skill 支持的模式

| 模式 | 触发条件 | 行为 |
|------|----------|------|
| **首次实现** | tasks.md 全部为 `[ ]` | 从 MP1.1 开始 |
| **断点续做** | tasks.md 有部分 `[x]` | 从最后 `[x]` 后的第一个 `[ ]` 继续 |
| **闸门修复** | 测试失败需要修复 | 优先处理失败项 |

### 前置检查

- [ ] `tasks.md` 存在
- [ ] `verification.md` 存在
- [ ] 当前会话未执行过 Test Owner
- [ ] `tests/**` 有测试文件
