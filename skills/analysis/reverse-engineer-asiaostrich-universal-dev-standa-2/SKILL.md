---
name: reverse
scope: partial
description: "[UDS] Reverse engineer code to Specs, BDD, or TDD coverage"
allowed-tools: Read, Grep, Glob
argument-hint: "[spec|bdd|tdd] <input>"
disable-model-invocation: true
---

# Reverse Engineering Assistant | 反向工程助手

Reverse engineer existing code into specifications, BDD scenarios, or TDD coverage reports.

將現有程式碼反向工程為規格文件、BDD 場景或 TDD 覆蓋率報告。

## Subcommands | 子命令

| Subcommand | Input | Output | Description | 說明 |
|------------|-------|--------|-------------|------|
| `spec` | Code files/dirs | `SPEC-XXX.md` | Extract spec from code | 從程式碼提取規格 |
| `bdd` | `SPEC-XXX.md` | `.feature` | Convert ACs to Gherkin | 將 AC 轉為 Gherkin |
| `tdd` | `.feature` | Coverage Report | Analyze test coverage | 分析測試覆蓋率 |

## Workflow | 工作流程

### spec: Code to Specification

1. **Scan** - Read source files and identify public APIs, data flows, and business logic
2. **Classify** - Tag each finding as `[Confirmed]`, `[Inferred]`, or `[Unknown]`
3. **Structure** - Organize into SDD spec format with Acceptance Criteria
4. **Attribute** - Cite every reversed item with `file:line` source reference

### bdd: Specification to Gherkin

1. **Parse** - Read SPEC-XXX.md and extract Acceptance Criteria
2. **Convert** - Map each AC to a Gherkin Scenario (1:1 mapping)
3. **Tag** - Add `@SPEC-XXX` and `@AC-N` tags for traceability
4. **Write** - Output `.feature` file with `# [Source: path:AC-N]` comments

### tdd: Feature to Coverage Report

1. **Parse** - Read `.feature` file scenarios
2. **Search** - Find corresponding test files using Grep/Glob
3. **Map** - Match scenarios to existing unit tests
4. **Report** - Output coverage matrix (covered / missing / partial)

## Anti-Hallucination Rules | 防幻覺規則

| Rule | Requirement | 要求 |
|------|-------------|------|
| **Certainty Tags** | Use `[Confirmed]`, `[Inferred]`, `[Unknown]` for all findings | 所有發現須標注確定性 |
| **Source Attribution** | Cite `file:line` for every reversed item | 每項反向結果須引用來源 |
| **No Fabrication** | Never invent APIs or behaviors not found in code | 不得捏造程式碼中不存在的 API 或行為 |

## Usage | 使用方式

- `/reverse spec src/auth/` - Extract specification from auth module
- `/reverse bdd specs/SPEC-AUTH.md` - Convert spec ACs to Gherkin scenarios
- `/reverse tdd features/auth.feature` - Analyze test coverage for feature file

## Reference | 參考

- Detailed guide: [guide.md](./guide.md)
- Core standard: [reverse-engineering-standards.md](../../core/reverse-engineering-standards.md)
