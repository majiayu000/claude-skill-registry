---
name: scaffold-analysis
description: 识别项目技术栈、测试框架和环境依赖，为 Compile ExecSpec 提供基础上下文。当需要编译 ExecSpec 前，识别项目类型（Node/Python/Go）、测试框架（Jest/Pytest/RSpec）、环境变量依赖（dotenv/os.getenv）时使用。
stage: EXECSPEC_COMPILE
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# Scaffold Analysis

> **Scope**: EXECSPEC_COMPILE — Compile ExecSpec（编译 ExecSpec）
>
> **版本**: 1.0.0 | **创建日期**: 2025-02-03

---

## 1. 描述

Scaffold Analysis 识别项目的技术栈和依赖上下文，为后续编译 ExecSpec 提供基础信息。

**核心职责**：
- 读取Registry识别项目类型（Node.js/Python/Go）
- 识别测试框架（Jest/Pytest/RSpec/Go test）
- 从SPEC推断环境变量依赖（NFR/GOAL中声明的依赖）
- 识别外部服务依赖（数据库、API、消息队列）

**Why**：
- 避免环境配置遗漏（如dotenv经常被忽视）
- 为environment-config-generator提供输入依据
- 为round-planning提供技术复杂度上下文

---

## 2. 适用场景

- **WORKFLOW Step 3 Task 3-1**: 编译 ExecSpec Master Plan 前，执行脚手架分析
- **场景A**: 新项目启动 Compile ExecSpec，需要识别技术栈
- **场景B**: 跨项目迁移，需要快速了解技术上下文
- **场景C**: 环境配置缺失，追溯技术依赖

**对应 Build_Exec_Spec_Plans**: Step 1 (Parse Implementation Plan)

---

## 3. 输入

- `spec/spec_artifacts_registry.md` - Registry文件，包含项目元数据和artifact清单
- `package.json` / `requirements.txt` / `go.mod` - 依赖配置文件

---

## 4. 输出

- `spec/build/scaffold_analysis_report.md` - 脚手架分析报告

**报告包含**:
- 项目类型（Language/Framework/Package Manager）
- 测试框架（Unit/Integration/E2E）
- 环境变量依赖（变量名 + Registry来源）
- 外部服务依赖（数据库/缓存/API）

---

## 5. 执行策略

### 步骤1: 读取Registry识别项目类型
扫描 spec_artifacts_registry.md，提取 project_language/project_framework 字段，推断项目类型（Node.js/Python/Go/Java）

### 步骤2: 识别测试框架
根据依赖配置文件推断：Node.js(jest/mocha) / Python(pytest/unittest) / Go(go test/testify)

### 步骤3: 推断环境变量依赖
从Registry文件提取NFR和GOAL中的环境配置需求（DATABASE_URL, API_KEY等），结合依赖配置文件推断外部服务依赖

**注意**: Compile ExecSpec 阶段发生在编码前，不扫描src/代码

### 步骤4: 识别外部服务依赖
根据依赖列表和环境变量模式推断服务类型：
- 数据库: pg/mysql/psycopg2/gorm + *_URL
- 缓存: redis/memcached
- API: axios/requests + *_KEY

### 步骤5: 生成报告
写入 spec/build/scaffold_analysis_report.md，包含项目类型 + 测试框架 + 环境变量 + 外部服务

---

## 6. 价值

### SPEC组织
- 标准化技术栈识别流程，减少人工遗漏
- 为环境配置生成提供准确依据

### PM/BA
- 快速了解项目技术上下文
- 识别环境配置风险点（如缺少dotenv导致启动失败）

### Dev
- 自动化脚手架分析，避免手动梳理依赖
- 明确环境变量清单，减少"在我机器上能跑"问题

---

## 7. 验收标准

### L1-STREAMLINED

**检查清单**（4项，≥75%通过）：
- [ ] 项目类型已识别（Node.js/Python/Go）
- [ ] 测试框架已识别（Unit Test框架）
- [ ] 环境变量依赖已扫描（至少3个常见变量）
- [ ] 报告已生成（scaffold_analysis_report.md）

**通过标准**：
- 4项中≥3项通过（≥75%）
- 必过项：项目类型已识别

---

### L2-BALANCED

**检查清单**（6项，≥83%通过）：
- [ ] 项目类型已识别（Language + Framework）
- [ ] 测试框架已识别（Unit + Integration）
- [ ] 环境变量依赖已扫描（包含文件位置）
- [ ] 外部服务依赖已识别（数据库/缓存）
- [ ] 依赖配置文件已检查（package.json/requirements.txt）
- [ ] 报告已生成（包含依赖分析）

**通过标准**：
- 6项中≥5项通过（≥83%）
- 必过项：环境变量包含文件位置

---

### L3-RIGOROUS

**检查清单**（8项，≥88%通过）：
- [ ] 项目类型已识别（Language + Framework + Package Manager）
- [ ] 测试框架已识别（Unit + Integration + E2E）
- [ ] 环境变量依赖已扫描（包含文件位置 + 使用频率）
- [ ] 外部服务依赖已识别（数据库/缓存/消息队列/API）
- [ ] 依赖配置文件已检查（版本约束分析）
- [ ] 安全性扫描（硬编码凭证检测）
- [ ] 技术债务识别（过时依赖/弃用API）
- [ ] 报告已生成（包含风险评估）

**通过标准**：
- 8项中≥7项通过（≥88%）
- 必过项：安全性扫描无硬编码凭证

---

## 8. `///` 命令

```
///scaffold-analysis
```

---

## 相关 SKILLs

- **前置**: 无（这是 Compile ExecSpec 的起点）
- **后续**: environment-config-generator（使用分析报告生成环境配置）
- **后续**: round-planning（使用技术复杂度评估Round数量）

---
