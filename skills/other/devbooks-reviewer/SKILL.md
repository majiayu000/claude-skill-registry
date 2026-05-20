---
name: devbooks-reviewer
description: devbooks-reviewer：以 Reviewer 角色做可读性/一致性/依赖健康/坏味道审查，只输出审查意见与可执行建议，不讨论业务正确性。用户说"帮我做代码评审/review 可维护性/坏味道/依赖风险/一致性建议"，或在 DevBooks apply 阶段以 reviewer 执行时使用。
recommended_experts: ["System Architect", "Security Expert"]
allowed-tools:
  - Glob
  - Grep
  - Read
  - Bash
---

# DevBooks：代码评审（Reviewer）

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

## 工作流位置感知（Workflow Position Awareness）

> **核心原则**：Code Review 在 Test Owner 阶段 2 验证之后执行，是归档前的最后一个评审步骤。

### 我在整体工作流中的位置

```
proposal → design → test-owner(阶段1) → coder → test-owner(阶段2) → [Code Review] → archive
                                                                          ↓
                                                              可读性/一致性/依赖审查
```

### Code Review 的职责边界

| 允许 | 禁止 |
|------|------|
| 审查代码可读性/一致性 | ❌ 修改代码文件 |
| 设置 verification.md Status = Done | ❌ 讨论业务正确性（那是 Test Owner 的事） |
| 提出改进建议 | ❌ 勾选 AC 覆盖矩阵（那是 Test Owner 的事） |

### 前置条件

- [ ] Test Owner 阶段 2 已完成（AC 矩阵已打勾）
- [ ] 测试全绿
- [ ] evidence/green-final/ 存在

---

## 前置：配置发现（协议无关）

- `<truth-root>`：当前真理目录根
- `<change-root>`：变更包目录根

执行前**必须**按以下顺序查找配置（找到后停止）：
1. `.devbooks/config.yaml`（如存在）→ 解析并使用其中的映射
2. `dev-playbooks/project.md`（如存在）→ Dev-Playbooks 协议，使用默认映射
3. `project.md`（如存在）→ template 协议，使用默认映射
4. 若仍无法确定 → **停止并询问用户**

**关键约束**：
- 如果配置中指定了 `agents_doc`（规则文档），**必须先阅读该文档**再执行任何操作
- 禁止猜测目录根
- 禁止跳过规则文档阅读

## 审查维度

### 1. 可读性审查
- 命名一致性（PascalCase/camelCase）
- 函数长度和复杂度
- 注释质量和必要性
- 代码格式化

### 2. 依赖健康审查
- 分层约束遵守（参见 `<truth-root>/architecture/c4.md`）
- 循环依赖检测
- 内部模块封装（禁止深度导入 *Internal 文件）
- 依赖方向正确性

### 3. 资源管理审查

**必须检查的资源泄漏模式**：

| 检查项 | 违规模式 | 正确模式 |
|--------|----------|----------|
| 订阅未取消 | `event.on(...)` 无对应 `off()` | 注册到 DisposableStore |
| 定时器未清理 | `setInterval()` 无 `clearInterval()` | 在 dispose() 中清理 |
| 监听器未移除 | `addEventListener()` 无 `removeEventListener()` | 使用 AbortController |
| 流未关闭 | `createReadStream()` 无 `close()` | 使用 try-finally 或 using |
| 连接未释放 | `connect()` 无 `disconnect()` | 使用连接池或 dispose 模式 |

**DisposableStore 模式检查**：

```typescript
// 违规：可变的 disposable 字段
private disposable = new DisposableStore(); // 应该是 readonly

// 违规：dispose() 未调用 super.dispose()
dispose() {
  this.cleanup(); // 缺少 super.dispose()
}

// 正确模式
private readonly _disposables = new DisposableStore();

override dispose() {
  this._disposables.dispose();
  super.dispose();
}
```

**资源管理检查清单**：
- [ ] DisposableStore 字段是否声明为 `readonly` 或 `const`？
- [ ] dispose() 方法是否调用了 `super.dispose()`？
- [ ] 订阅/监听器是否注册到 DisposableStore？
- [ ] 测试是否包含 `ensureNoDisposablesAreLeakedInTestSuite()`？

### 4. 类型安全审查

- [ ] 是否存在 `as any` 类型断言？
- [ ] 是否存在 `{} as T` 危险断言？
- [ ] 是否使用了 `unknown` 而非 `any`？
- [ ] 泛型约束是否足够严格？

### 5. 坏味道检测

参见：`references/坏味道速查表.md`

### 6. 测试质量审查

- [ ] 是否存在 `test.only` / `describe.only`？
- [ ] 测试是否有清理逻辑（afterEach）？
- [ ] 测试是否独立（不依赖执行顺序）？
- [ ] mock 是否正确重置？

## 执行方式

1) 先阅读并遵守：`~/.claude/skills/_shared/references/AI行为规范.md`（可验证性 + 结构质量守门）。
2) 阅读资源管理指南：`references/资源管理审查清单.md`。
3) 严格按完整提示词输出评审意见：`references/代码评审提示词.md`。

---

## 上下文感知

本 Skill 在执行前自动检测上下文，选择合适的审查范围。

检测规则参考：`skills/_shared/上下文检测模板.md`

### 检测流程

1. 检测变更包是否存在
2. 检测是否有代码变更（git diff）
3. 检测热点文件（基于变更历史与复杂度分析）

### 本 Skill 支持的模式

| 模式 | 触发条件 | 行为 |
|------|----------|------|
| **变更包审查** | 提供 change-id | 审查该变更包相关的代码变更 |
| **文件审查** | 提供具体文件路径 | 审查指定文件 |
| **热点优先审查** | 检测到热点文件变更 | 优先审查高风险热点 |

### 检测输出示例

```
检测结果：
- 变更包状态：存在
- 代码变更：12 个文件
- 热点文件：3 个（需重点关注）
- 运行模式：变更包审查 + 热点优先
```

---

## 下一步推荐

**参考**：`skills/_shared/工作流下一步.md`

完成 code-review 后，下一步取决于具体情况：

| 条件 | 下一个 Skill | 原因 |
|------|--------------|------|
| 有 spec deltas | `devbooks-archiver` | 归档前合并规格到真理 |
| 无 spec deltas | 归档完成 | 无需其他 skill |
| 发现重大问题 | 交回 `devbooks-coder` | 归档前修复问题 |

### Reviewer 专属权限：设置 verification.md Status

**只有 Reviewer 可以将 `verification.md` 的 Status 设为 `Done`**。

Review 通过后，Reviewer 必须执行：
1. 打开 `<change-root>/<change-id>/verification.md`
2. 将 `- Status: Ready` 改为 `- Status: Done`
3. 这是归档的前置条件（`change-check.sh --mode archive` 会检查）

### 输出模板

完成 code-review 后，输出：

```markdown
## 推荐的下一步

**下一步：`devbooks-archiver`**（如果有 spec deltas）
或
**归档完成**（如果无 spec deltas）

原因：代码评审已完成。下一步是[合并 spec deltas 到真理 / 完成归档]。

### 如何调用（如果有 spec deltas）
```
运行 devbooks-archiver skill 处理变更 <change-id>
```
```
