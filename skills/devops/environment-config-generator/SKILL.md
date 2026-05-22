---
name: environment-config-generator
description: 生成多环境配置清单和dotenv模板文件，确保dev/test/staging/prod环境配置完整。当需要创建环境配置、生成.env.example模板、文档化测试框架setup、映射CI环境变量时使用。解决dotenv经常被忽视的痛点。
stage: EXECSPEC_COMPILE
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# Environment Config Generator

> **Scope**: EXECSPEC_COMPILE — Compile ExecSpec（编译 ExecSpec）
>
> **版本**: 1.0.0 | **创建日期**: 2025-02-03

---

## 1. 描述

Environment Config Generator 生成完整的环境配置清单和dotenv模板，解决"dotenv经常被忽视"的用户痛点。

**核心职责**：
- 生成多环境配置清单（dev/test/staging/prod）
- 创建.env.example模板文件
- 文档化测试框架setup（Jest/Pytest/RSpec）
- CI环境变量映射（GitHub Actions/GitLab CI）

**Why**：
- **用户痛点**: dotenv配置经常被遗漏，导致"在我机器上能跑"问题
- **ExecSpec concern**: 这是"如何执行（编译/落实）"的问题，属于 EXECSPEC_COMPILE（dir: `execspec_compile/`）范畴，而非implementation_planning的"测试什么"
- **权威要求**: Build_Exec_Spec_Plans L1/L2/L3都明确要求"环境配置清单"（Step 3）

---

## 2. 适用场景

- **WORKFLOW Step 3 Task 3-2**: 编译 ExecSpec Master Plan 时，生成环境配置清单
- **场景A**: 新项目启动，需要定义标准环境配置
- **场景B**: 环境变量缺失导致启动失败，需要补全配置
- **场景C**: CI/CD配置，需要映射环境变量到pipeline

**对应 Build_Exec_Spec_Plans**: Step 3 (环境配置)

---

## 3. 输入

- `spec/build/scaffold_analysis_report.md` - 脚手架分析报告（包含环境变量扫描结果）
- 项目配置（从scaffold-analysis识别的项目类型和测试框架）

---

## 4. 输出

- `spec/build/environment_config_checklist.md` - 环境配置清单（含4个环境：dev/test/staging/prod）
- `.env.example` - dotenv模板文件（位于项目根目录）
- 环境配置说明（嵌入Master Plan中）

**输出包含**:
- 每个环境的完整变量列表（dev用mock值，staging/prod用占位符）
- 测试框架setup配置（Jest/Pytest/RSpec）
- CI环境变量映射模板（GitHub Actions/GitLab CI）

---

## 5. 执行步骤

<!-- 💡 Prompt 提示：这是给 AI 看的指令。请使用【指令性语言】(Imperative)。
     例如：\"Read input...\", \"Generate output...\"
     不要写：\"You should read...\" -->

### Step 1: 读取脚手架分析报告

```
Read `spec/build/scaffold_analysis_report.md`
Extract environment variables list with file locations
Extract project type (Node.js/Python/Go)
Extract test framework
```

### Step 2: 为每个环境变量生成配置项

```
For each variable in the list:
  - Generate dev value (local/mock)
  - Generate test value (mock/test-specific)
  - Generate staging value (placeholder)
  - Generate prod value (placeholder with security note)
```

### Step 3: 生成.env.example模板

```
Create `.env.example` file at project root
Format: KEY=<description-or-placeholder>
Group by category:
  # Database
  DATABASE_URL=<database-connection-string>

  # External Services
  API_KEY=<api-key>

  # Application
  PORT=3000
```

### Step 4: 生成环境配置清单

```
Write `spec/build/environment_config_checklist.md`
Structure by environment (dev/test/staging/prod)
Include checkboxes for validation
```

### Step 5: 生成测试框架setup文档

```
Based on test framework (Jest/Pytest/RSpec):
  - Generate setup script template
  - Document environment variable loading
  - Add to environment_config_checklist.md
```

### Step 6: 生成CI环境变量映射

```
Generate CI configuration snippet:
  GitHub Actions: .github/workflows/ci.yml env section
  GitLab CI: .gitlab-ci.yml variables section
Add to environment_config_checklist.md
```

---

## 6. 快速开始

<!-- 💡 Prompt 提示：这是给人类看的指南。请使用【描述性语言】或明确主语。
     例如：\"The developer should...\", \"User needs to...\"
     明确告诉 AI 这是人类的职责。 -->

### 第1步：开发者确保脚手架分析已完成

开发者需要先执行scaffold-analysis SKILL，生成`spec/build/scaffold_analysis_report.md`。

### 第2步：调用此SKILL

通过WORKFLOW或手动触发：
```
///environment-config-generator
```

### 第3步：查看生成的配置

查看输出文件：
- `spec/build/environment_config_checklist.md` - 环境配置清单
- `.env.example` - dotenv模板

### 第4步：补全敏感信息

开发者需要手动补全：
- staging/prod环境的实际值
- API密钥和凭证
- CI环境变量配置

**预计耗时**: 5-10分钟（取决于环境变量数量）

---

## 7. 使用说明

### 输入要求
`scaffold_analysis_report.md` 必须包含环境变量依赖章节（至少3个变量）、项目类型和测试框架识别结果

### 输出格式示例

**environment_config_checklist.md**: 分4个环境（dev/test/staging/prod），每个变量一行checkbox格式

**.env.example**: 按类别分组（Database/External Services/Application），使用占位符或描述性注释

---

## 8. 价值

### SPEC组织
- 标准化环境配置流程，减少配置遗漏
- 提供清单化验证机制（checkbox）

### PM/BA
- 快速了解环境依赖
- 识别环境配置风险（如缺少prod凭证）

### Dev
- 自动化生成.env.example，避免手动整理
- 明确多环境差异，减少"在我机器上能跑"问题
- CI环境变量映射模板，加速CI/CD配置

---

## 9. 质量检查

- [ ] .env.example已生成且包含所有扫描到的环境变量
- [ ] environment_config_checklist.md包含4个环境（dev/test/staging/prod）
- [ ] 每个环境变量有合理的默认值或占位符
- [ ] 测试框架setup文档已生成（如适用）
- [ ] CI环境变量映射已生成（如适用）
- [ ] 敏感信息使用占位符而非真实值

---

## 10. 限制条件

**不支持**：
- 自动填充staging/prod真实凭证（需人工补全）
- 环境变量加密存储（需运维工具如AWS Secrets Manager）

**最大输入规模**：
- 环境变量数量：100个以内
- 文件扫描范围：src/ 目录（不包括node_modules/等）

**依赖**：
- 需要scaffold-analysis先执行
- 需要项目根目录有写权限（生成.env.example）

---

## 相关 SKILLs

- **前置**: scaffold-analysis（提供环境变量扫描结果）
- **并行**: constraints-generator（可同时生成约束文件）
- **后续**: round-planning（使用环境配置评估setup时间）

---
