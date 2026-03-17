---
name: methodology
scope: partial
description: "[UDS] Manage development methodology workflow"
allowed-tools: Read, Write, Grep, Glob
argument-hint: "[action] [argument]"
---

# Methodology System | 方法論系統

> [!WARNING]
> **Experimental Feature / 實驗性功能**
>
> This feature is under active development and may change significantly in v4.0.
> 此功能正在積極開發中，可能在 v4.0 中有重大變更。

Manage the active development methodology for the current project with two independent systems.

管理當前專案的開發方法論，支援兩個獨立系統。

**Two Independent Systems / 兩個獨立系統：**
- **System A: SDD** - Spec-Driven Development (AI-era, spec-first)
- **System B: Double-Loop TDD** - BDD (outer) + TDD (inner) (traditional)

**Optional Input:** ATDD - Acceptance Test-Driven Development (feeds into either system)

## Actions | 動作

| Action | Description | 說明 |
|--------|-------------|------|
| *(none)* / `status` | Show current phase and checklist | 顯示當前階段和檢查清單 |
| `switch <id>` | Switch to different methodology | 切換到不同方法論 |
| `phase [name]` | Show or change current phase | 顯示或變更當前階段 |
| `checklist` | Show current phase checklist | 顯示當前階段檢查清單 |
| `skip` | Skip current phase (with warning) | 跳過當前階段（會有警告） |
| `list` | List available methodologies | 列出可用方法論 |
| `create` | Create custom methodology | 建立自訂方法論 |

## Available Methodologies | 可用方法論

| System | ID | Workflow | 工作流程 |
|--------|-----|---------|---------|
| A: SDD | `sdd` | /sdd -> Review -> /derive-all -> Implementation | 規格優先 |
| B: BDD | `bdd` | Discovery -> Formulation -> Automation | 外部迴圈 |
| B: TDD | `tdd` | Red -> Green -> Refactor | 內部迴圈 |
| Input | `atdd` | Workshop -> Examples -> Tests | 驗收測試驅動 |

## Usage Examples | 使用範例

```bash
/methodology                    # Show current status
/methodology switch sdd         # Switch to Spec-Driven Development
/methodology phase green        # Move to GREEN phase (TDD)
/methodology checklist          # Show current phase checklist
/methodology list               # List all available methodologies
/methodology skip               # Skip current phase (with warning)
/methodology create             # Start custom methodology wizard
```

## Configuration | 配置

Methodology settings are stored in `.standards/manifest.json`:

```json
{
  "methodology": {
    "active": "sdd",
    "available": ["tdd", "bdd", "sdd", "atdd"]
  }
}
```

## Reference | 參考

- Detailed guide: [guide.md](./guide.md)
