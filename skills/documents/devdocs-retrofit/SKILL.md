---
name: devdocs-retrofit
description: Retrofit existing projects to DevDocs workflow, or migrate old DevDocs to new standards. Use when users want to adapt existing projects, migrate documentation, standardize documents, or upgrade DevDocs version. Triggers on keywords like "retrofit", "改造", "适配", "迁移", "标准化", "逆向", "升级文档".
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash
---

# 项目改造

将已有工程改造为 DevDocs 流程，或将旧版 DevDocs 迁移到新规范。

## 语言规则

- 支持中英文提问
- 统一中文回复
- 使用中文生成文档

## 触发条件

- 用户希望将现有项目适配 DevDocs 流程
- 用户需要标准化项目文档
- 用户要迁移或升级已有 DevDocs 文档
- 项目缺少文档，需要从代码逆向生成

## 工作流程

```
1. 扫描项目结构
   │
   ▼
2. 检测项目状态
   │
   ├── 无 DevDocs ──────────────────┐
   │                                │
   ├── 有 DevDocs（旧版）────┐      │
   │                         │      │
   └── 有 DevDocs（符合规范）│      │
       → 无需改造            │      │
                             ▼      ▼
3a. 版本迁移流程      3b. 新项目改造流程
    │                       │
    ├── 规范检查            ├── 自动识别文档
    ├── 生成差异清单        ├── 用户确认/手动指定
    ├── 用户确认            ├── 代码逆向推导（可选）
    └── 执行迁移            └── 生成 DevDocs 文档
                             │
                             ▼
4. 生成改造报告
```

---

## 项目状态检测

### 检测逻辑

```
1. 检查 docs/devdocs/ 目录是否存在
   │
   ├── 不存在 → 新项目改造流程
   │
   └── 存在 → 检查规范符合性
       │
       ├── 符合当前规范 → 无需改造
       │
       └── 不符合 → 版本迁移流程
```

### 规范符合性检查清单

| 检查项 | 检查内容 | 规范要求 |
|--------|----------|----------|
| **编号体系** | F-XXX, US-XXX, AC-XXX | 必须 |
| **测试编号** | UT-XXX, IT-XXX, E2E-XXX | 必须 |
| **追溯矩阵** | F → US → AC → 测试 映射 | 必须 |
| **文件命名** | 01-requirements.md, 03-test-cases.md 等 | 必须 |
| **章节完整性** | 各文档必要章节 | 必须 |
| **Skill 协作** | 标注协作 Skill | 建议 |

---

## 版本迁移流程

当检测到已有 DevDocs 文档但不符合当前规范时执行。

### Step M1: 规范检查

扫描现有 DevDocs 文档，检查规范符合性：

```markdown
## 规范检查报告

### 检测结果

| 文件 | 状态 | 问题 |
|------|------|------|
| 01-requirements.md | ⚠️ 需迁移 | 缺少 F/US/AC 编号 |
| 02-system-design.md | ✅ 符合 | - |
| 03-test-plan.md | ❌ 需重命名 | 应为 03-test-cases.md |
| 04-dev-tasks.md | ⚠️ 需迁移 | 缺少 T-XX 编号 |
```

### Step M2: 生成差异清单

详细列出需要迁移的内容：

```markdown
## 迁移差异清单

### 编号体系

| 文档 | 当前状态 | 迁移动作 |
|------|----------|----------|
| 01-requirements.md | 无编号 | 为功能点添加 F-001, F-002... |
| 01-requirements.md | 无编号 | 为用户故事添加 US-001, US-002... |
| 01-requirements.md | 无编号 | 为验收标准添加 AC-001, AC-002... |
| 03-test-*.md | 无编号 | 为测试用例添加 UT/IT/E2E-XXX |
| 04-dev-tasks.md | 无编号 | 为任务添加 T-01, T-02... |

### 文件结构

| 当前文件 | 迁移动作 | 目标文件 |
|----------|----------|----------|
| 03-test-plan.md | 重命名 + 拆分 | 03-test-cases.md |
| - | 新建 | 03-test-unit.md |
| - | 新建 | 03-test-integration.md |
| - | 新建 | 03-test-e2e.md |

### 追溯矩阵

| 当前状态 | 迁移动作 |
|----------|----------|
| 不存在 | 在 03-test-cases.md 中新建追溯矩阵章节 |

### 章节补充

| 文档 | 缺失章节 | 迁移动作 |
|------|----------|----------|
| 02-system-design.md | 需求追溯 | 添加第 13 节 |
| 04-dev-tasks.md | Skill 协作约束 | 添加编码约束说明 |
```

### Step M3: 用户确认

使用 AskUserQuestion 展示迁移计划：

```markdown
## 迁移计划确认

检测到当前 DevDocs 文档需要迁移到新规范。

### 迁移内容

1. **编号体系**：为所有功能点、用户故事、验收标准、测试用例添加编号
2. **文件重命名**：03-test-plan.md → 03-test-cases.md
3. **新建追溯矩阵**：建立 F → US → AC → 测试 的追溯关系
4. **章节补充**：补充缺失的规范章节

### 迁移选项

1. **完整迁移**（推荐）- 自动执行所有迁移动作
2. **选择性迁移** - 选择要执行的迁移项
3. **仅生成报告** - 不执行迁移，仅输出差异报告

请选择迁移方式。
```

### Step M4: 执行迁移

#### 编号迁移

为现有内容添加编号：

```markdown
### 迁移前
- 用户注册功能
  - 作为新用户，我希望注册账号
  - 验收标准：邮箱格式正确

### 迁移后
- **F-001**: 用户注册功能
  - **US-001**: 作为新用户，我希望注册账号，以便使用系统
  - **AC-001**: 邮箱格式正确时注册成功
  - **AC-002**: 邮箱格式错误时提示错误信息
```

#### 文件重命名

```bash
# 使用 git mv 保留历史
git mv docs/devdocs/03-test-plan.md docs/devdocs/03-test-cases.md
```

#### 追溯矩阵生成

```markdown
## 追溯矩阵

| 功能点 | 用户故事 | 验收标准 | 单元测试 | 集成测试 | E2E测试 |
|--------|----------|----------|----------|----------|---------|
| F-001 | US-001 | AC-001 | UT-001 | - | E2E-001 |
| F-001 | US-001 | AC-002 | UT-002 | - | E2E-001 |
| F-001 | US-002 | AC-003 | UT-003 | IT-001 | - |
```

---

## 新项目改造流程

当项目没有 DevDocs 文档时执行。

### Step 1: 扫描项目结构

扫描常见文档位置：

```bash
# 文档目录
docs/ doc/ documentation/

# 根目录文档
README.md CHANGELOG.md

# 设计文档
design/ architecture/

# 测试文档
tests/ test/ __tests__/
```

### Step 2: 自动识别文档

#### 识别规则

| DevDocs 阶段 | 识别关键词 | 常见文件名 |
|--------------|------------|------------|
| 需求文档 | requirement, PRD, 需求, spec | `*requirement*.md`, `*prd*.md` |
| 系统设计 | design, architecture, 设计, 架构 | `*design*.md`, `*architecture*.md` |
| 测试用例 | test, QA, 测试, case | `*test*.md`, `*qa*.md` |
| 开发任务 | task, todo, 任务, backlog | `*task*.md`, `*todo*.md` |

### Step 3: 用户确认

```markdown
## 文档识别结果

| 阶段 | 识别状态 | 识别到的文件 |
|------|----------|--------------|
| 需求文档 | ✅ 已识别 | `docs/requirements.md` |
| 系统设计 | ✅ 已识别 | `docs/architecture.md` |
| 测试用例 | ❌ 未找到 | - |
| 开发任务 | ⚠️ 待确认 | `TODO.md` (相似度 60%) |

### 选项

1. **确认识别结果** - 使用自动识别的映射
2. **手动指定文档** - 提供各阶段文档路径
3. **代码逆向推导** - 从代码分析生成文档（适用于无文档项目）
```

### Step 4: 代码逆向推导（可选）

当项目缺少文档时，从代码分析生成文档。

#### 需求推导

| 分析对象 | 推导内容 | 编号分配 |
|----------|----------|----------|
| 路由/页面 | 功能模块 → F-XXX | 按模块顺序 |
| API 端点 | 业务操作 | 归属到 F-XXX |
| 测试描述 | 用户故事 → US-XXX | 按 F-XXX 分组 |
| 测试断言 | 验收标准 → AC-XXX | 按 US-XXX 分组 |

#### 推导示例

```markdown
## 功能清单 [从代码推导]

### F-001: 用户模块

**用户故事**：
- **US-001**: 作为用户，我可以注册新账号
  - 来源：`POST /api/users` + `auth.test.ts`
- **US-002**: 作为用户，我可以登录系统
  - 来源：`POST /api/auth/login`

**验收标准**：
- **AC-001**: 邮箱格式正确时注册成功
  - 来源：`auth.test.ts: "should register with valid email"`
- **AC-002**: 密码少于 6 位时提示错误
  - 来源：`auth.test.ts: "should reject short password"`
```

#### 测试用例推导

| 分析对象 | 推导内容 | 编号分配 |
|----------|----------|----------|
| 单元测试文件 | UT-XXX | 按文件顺序 |
| 集成测试文件 | IT-XXX | 按文件顺序 |
| E2E 测试文件 | E2E-XXX | 按文件顺序 |

```markdown
## 测试用例 [从代码推导]

### 单元测试

| 编号 | 关联 AC | 测试描述 | 来源 |
|------|---------|----------|------|
| UT-001 | AC-001 | should register with valid email | auth.test.ts:12 |
| UT-002 | AC-002 | should reject short password | auth.test.ts:24 |
```

### Step 5: 生成 DevDocs 文档

按 DevDocs 规范生成完整文档：

```
docs/devdocs/
├── 01-requirements.md      # 含 F/US/AC 编号
├── 02-system-design.md     # 含模块-功能点映射
├── 03-test-cases.md        # 含追溯矩阵
├── 03-test-unit.md         # 含 UT-XXX 编号
├── 03-test-integration.md  # 含 IT-XXX 编号
├── 03-test-e2e.md          # 含 E2E-XXX 编号
├── 04-dev-tasks.md         # 含 T-XX 编号
└── 00-retrofit-report.md   # 改造报告
```

---

## 改造报告

```markdown
# DevDocs 改造报告

## 改造概览

- **项目名称**：<project>
- **改造时间**：<timestamp>
- **改造类型**：新项目改造 / 版本迁移

## 改造结果

### 文档状态

| 文档 | 改造前 | 改造后 | 动作 |
|------|--------|--------|------|
| 需求文档 | docs/req.md | docs/devdocs/01-requirements.md | 转换 + 编号 |
| 系统设计 | - | docs/devdocs/02-system-design.md | 新建 |
| 测试用例 | tests/README.md | docs/devdocs/03-test-cases.md | 转换 + 编号 |
| 开发任务 | TODO.md | docs/devdocs/04-dev-tasks.md | 标准化 |

### 编号分配

| 类型 | 数量 | 范围 |
|------|------|------|
| 功能点 (F) | 5 | F-001 ~ F-005 |
| 用户故事 (US) | 12 | US-001 ~ US-012 |
| 验收标准 (AC) | 28 | AC-001 ~ AC-028 |
| 单元测试 (UT) | 15 | UT-001 ~ UT-015 |
| 集成测试 (IT) | 4 | IT-001 ~ IT-004 |
| E2E 测试 (E2E) | 3 | E2E-001 ~ E2E-003 |

### 待完善项

以下内容标记为 [待补充]：

- [ ] AC-015 ~ AC-020 验收标准细化
- [ ] 非功能性需求-性能指标
- [ ] API 响应示例

## 下一步建议（强制路由）

改造完成后，**必须**执行以下之一建立基线：

| 场景 | 必须执行 | 说明 |
|------|----------|------|
| 首次改造 | `/devdocs-sync --audit` | 检查追溯健康度 |
| 有待补充项 | `/devdocs-requirements` | 完善需求文档 |
| 开始开发 | `/devdocs-dev-tasks` → `/devdocs-dev-workflow` | 执行任务 |
| 添加功能 | `/devdocs-feature` | 增量开发 |

> 改造不是终点，必须通过后续 Skill 进入正常开发循环。
```

---

## Skill 协作

| 场景 | 协作 Skill | 说明 |
|------|-----------|------|
| 需求审查 | `/devdocs-requirements` | 审查改造后的需求文档 |
| 设计审查 | `/devdocs-system-design` | 审查系统设计 |
| 测试用例 | `/devdocs-test-cases` | 完善测试用例设计 |
| 新增功能 | `/devdocs-feature` | 改造后添加新功能 |
| Bug 修复 | `/devdocs-bugfix` | 改造后修复问题 |
| 测试质量 | `/testing-guide` | 检查测试有效性 |
| 文件操作 | `/git-safety` | 重命名文件时使用 git mv |

---

## 约束

### 检测约束

- [ ] **必须先检测项目状态（无 DevDocs / 旧版 / 符合规范）**
- [ ] 必须扫描常见文档目录
- [ ] 识别结果必须让用户确认

### 迁移约束

- [ ] **迁移前必须生成差异清单**
- [ ] **迁移前必须用户确认**
- [ ] 文件重命名必须使用 `git mv`
- [ ] 不得删除原有文档的有效内容

### 编号约束

- [ ] **必须为所有功能点分配 F-XXX 编号**
- [ ] **必须为所有用户故事分配 US-XXX 编号**
- [ ] **必须为所有验收标准分配 AC-XXX 编号**
- [ ] **必须为所有测试用例分配 UT/IT/E2E-XXX 编号**
- [ ] 编号必须连续，不得跳号

### 输出约束

- [ ] 输出目录统一为 `docs/devdocs/`
- [ ] 文件命名遵循 DevDocs 规范
- [ ] 必须生成改造报告
- [ ] 逆向推导内容必须标注 `[从代码推导]`

---

## 错误处理

### 无法识别文档

```
未能自动识别到相关文档。

请选择：
1. 手动指定各阶段文档路径
2. 使用代码逆向推导生成文档
3. 使用 /devdocs-requirements 从头创建
```

### 项目无文档

```
当前项目未检测到任何文档。

推荐：使用代码逆向推导功能，从代码自动生成文档。

是否开始代码分析？
```

### 迁移冲突

```
检测到迁移冲突：

| 冲突项 | 说明 | 建议 |
|--------|------|------|
| 编号重复 | F-001 已存在 | 重新分配编号 |
| 文件覆盖 | 03-test-cases.md 已存在 | 备份后覆盖 |

请确认处理方式。
```

---

## 输出文件

```
docs/devdocs/
├── 00-retrofit-report.md    # 改造报告
├── 01-requirements.md       # 需求文档（含编号）
├── 02-system-design.md      # 系统设计
├── 02-system-design-api.md  # API 设计（如需要）
├── 03-test-cases.md         # 测试用例概览 + 追溯矩阵
├── 03-test-unit.md          # 单元测试（含 UT-XXX）
├── 03-test-integration.md   # 集成测试（含 IT-XXX）
├── 03-test-e2e.md           # E2E 测试（含 E2E-XXX）
└── 04-dev-tasks.md          # 开发任务（含 T-XX）
```
