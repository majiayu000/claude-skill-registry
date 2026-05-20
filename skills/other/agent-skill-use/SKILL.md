---
name: agent-skill-use
description: Create and manage AI agent skills following best practices. Use when creating new skills, optimizing context, designing multi-agent systems, or implementing progressive disclosure patterns.
allowed-tools: Bash, Read, Write, Grep, Glob, Edit
---

# Agent Skill Use

**Version**: 1.0.0
**Purpose**: ベストプラクティスに基づくエージェントスキルの作成・管理

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Skill Creation | "create agent skill", "スキル作成", "new skill" |
| Context Optimization | "optimize context", "コンテキスト最適化" |
| Multi-Agent Design | "design multi-agent", "マルチエージェント設計" |
| Best Practices | "agent best practices", "ベストプラクティス" |

---

## Reference Document

```
.claude/docs/AGENT_BEST_PRACTICES.md
```

このスキルは上記ドキュメントのパターンを実装します。

---

## Core Concepts

### 1. 三層アーキテクチャ

```
┌──────────────┬─────────────────┬─────────────────┬─────────────────┐
│              │      MCP        │     Skills      │   Subagents     │
├──────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Primary Role │ External        │ Task            │ Context         │
│              │ Connection      │ Specialization  │ Isolation       │
├──────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Context      │ High (all tools │ Low (metadata   │ Separate        │
│ Impact       │ loaded)         │ first)          │ window          │
├──────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Best For     │ API calls,      │ Workflows,      │ Parallel tasks, │
│              │ data access     │ procedures      │ isolation       │
└──────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### 2. Progressive Disclosure

```
Layer 1: Index Only (~500 tokens)     ← Always loaded
    ↓
Layer 2: Skill Metadata (~1,000)      ← On demand
    ↓
Layer 3: Full Content (~5,000)        ← When activated
```

---

## Workflow: Skill Creation

### Phase 1: 要件定義

#### Step 1.1: スキルの目的を明確化

```markdown
質問リスト:
1. このスキルは何を達成しますか？
2. どのようなトリガーで起動しますか？
3. 必要な入力は何ですか？
4. 期待する出力は何ですか？
5. どのツールが必要ですか？
```

#### Step 1.2: カテゴリの選択

| Category | Use Case |
|----------|----------|
| **Task Automation** | 繰り返しタスクの自動化 |
| **Code Quality** | レビュー・テスト・リファクタ |
| **DevOps** | デプロイ・監視・インフラ |
| **Content** | ドキュメント・コンテンツ生成 |
| **Integration** | 外部サービス連携 |

---

### Phase 2: 構造設計

#### Step 2.1: ディレクトリ作成

```bash
mkdir -p .claude/skills/[skill-name]/resources
mkdir -p .claude/skills/[skill-name]/scripts
```

#### Step 2.2: 必須ファイル構成

```
.claude/skills/[skill-name]/
├── SKILL.md              # Required: メイン定義
├── resources/            # Optional: 参照ドキュメント
│   ├── templates.md      # テンプレート集
│   └── examples.md       # 使用例
└── scripts/              # Optional: 実行スクリプト
    └── helper.sh         # ヘルパースクリプト
```

---

### Phase 3: SKILL.md作成

#### Step 3.1: Frontmatter

```yaml
---
name: "kebab-case-name"           # Required
description: "[Action] [Object]. Use when [trigger]."  # Required
allowed-tools: Bash, Read, Write  # Required
version: "1.0.0"                  # Optional
triggers:                         # Optional (for documentation)
  - "/command"
  - "natural language trigger"
dependencies:                     # Optional
  - "other-skill"
mcp_tools:                        # Optional (wrapped MCP tools)
  - "github.issues"
---
```

#### Step 3.2: 構造テンプレート

```markdown
# [Skill Title]

**Version**: X.Y.Z
**Purpose**: [One-line purpose]

---

## Triggers

| Trigger | Examples |
|---------|----------|
| [Category] | "[EN]", "[JP]" |

---

## Workflow

### Phase 1: [Title]

#### Step 1.1: [Substep]
[Instructions]

---

## Best Practices

✅ GOOD: [Pattern]
❌ BAD: [Anti-pattern]

---

## Checklist

- [ ] [Item 1]
- [ ] [Item 2]
```

---

### Phase 4: MCP Tool Wrapping

#### Step 4.1: ツールをスキル内にラップ

```markdown
<!-- SKILL.md内 -->

## Integrated Tools

This skill wraps the following MCP tools:

| Tool | Purpose |
|------|---------|
| `github.issues.create` | Issue作成 |
| `github.prs.review` | PRレビュー |

### Tool Usage

Tool definitions are loaded only when this skill is activated,
following progressive disclosure pattern.
```

#### Step 4.2: Tool Index (Full Definitionではなく)

```markdown
<!-- resources/tool-index.md -->

# Tool Index

## Available Tools
- `tool.name` - Brief description
- `tool.name2` - Brief description

Full definitions loaded on demand.
```

---

### Phase 5: Subagent統合（必要な場合）

#### Step 5.1: Subagent使用判断

```
Task received
    │
    ▼
┌─────────────────┐
│ Parallel tasks  │──Yes──► Use Subagent
│ (>3 independent)│
└────────┬────────┘
         │ No
         ▼
┌─────────────────┐
│ Security        │──Yes──► Use Subagent
│ isolation needed│
└────────┬────────┘
         │ No
         ▼
┌─────────────────┐
│ Long-running    │──Yes──► Use Subagent
│ background task │
└────────┬────────┘
         │ No
         ▼
Use Skills instead (default)
```

#### Step 5.2: Subagent Spawn定義

```yaml
# agents/[agent-name]/AGENT.md frontmatter
---
name: "parallel-executor"
type: "subagent"
spawn_conditions:
  - "independent_tasks > 3"
  - "explicit_parallel_request"
context_inheritance: "minimal"
---
```

---

## Workflow: Context Optimization

### Step 1: 現状分析

```bash
# スキル数とサイズを確認
find .claude/skills -name "SKILL.md" -exec wc -l {} \;

# MCPツール数を確認
grep -r "mcp_tools" .claude/skills/
```

### Step 2: Index作成

```markdown
<!-- .claude/overview.md -->
---
version: "1.0"
last_updated: "YYYY-MM-DD"
---

# Project Agent Configuration

## Available Skills

| Skill | Description | Triggers |
|-------|-------------|----------|
| skill-1 | Brief desc | /cmd, "phrase" |
| skill-2 | Brief desc | /cmd, "phrase" |

## Loading Rules

1. Always load: This overview only
2. On skill trigger: Load SKILL.md metadata
3. On execution: Load full skill content
```

### Step 3: Token削減の確認

| Metric | Target |
|--------|--------|
| Base context | <15,000 tokens |
| Skill load time | <500ms |
| Token reduction | >30% |

---

## Workflow: Multi-Agent Design

### Team Structure

```
┌─────────────┐
│ Coordinator │
│   (Lead)    │
└──────┬──────┘
       │
┌──────┴──────┬───────────────┐
│             │               │
▼             ▼               ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Planning │ │ Execution│ │  Review  │
│  Team    │ │   Team   │ │   Team   │
└──────────┘ └──────────┘ └──────────┘
```

### A2A Message Format

```json
{
  "message_id": "uuid-v4",
  "from_agent": "coordinator",
  "to_agent": "execution-team",
  "intent": "execute_task",
  "payload": {
    "task_id": "task-123",
    "description": "Task description",
    "priority": "high"
  }
}
```

---

## Naming Rules

### Required

| Rule | Example |
|------|---------|
| Kebab-case | `my-skill` |
| Lowercase | `code-reviewer` |
| Descriptive | `test-generator` |

### Forbidden

| Word | Reason |
|------|--------|
| `claude` | Trademark |
| `anthropic` | Company name |
| `mcp` | Protocol name |

---

## Validation Checklist

### Structure
- [ ] Directory at `.claude/skills/[name]/`
- [ ] SKILL.md has valid frontmatter
- [ ] Name is kebab-case, no forbidden words

### Content
- [ ] Description has action + trigger
- [ ] Triggers cover EN and JP
- [ ] Steps are clear and actionable
- [ ] Best practices documented

### Integration
- [ ] MCP tools wrapped (not loaded directly)
- [ ] Subagent criteria defined (if needed)
- [ ] Index updated in overview.md

---

## Quick Reference

### Create New Skill

```bash
# 1. Create directory
mkdir -p .claude/skills/my-skill/resources

# 2. Create SKILL.md
cat > .claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: Does X. Use when Y.
allowed-tools: Bash, Read, Write
---

# My Skill

**Version**: 1.0.0
**Purpose**: [Purpose]

## Workflow

### Step 1: [Title]
[Instructions]
EOF

# 3. Update overview
echo "| my-skill | Does X | /my, \"do x\" |" >> .claude/overview.md
```

### Validate Skill

```bash
# Check frontmatter
head -n 6 .claude/skills/my-skill/SKILL.md

# Test trigger (in Claude)
# "do x" → Skill should activate
```

---

## Related Documents

- `.claude/docs/AGENT_BEST_PRACTICES.md` - 完全なベストプラクティス
- `.claude/skills/skill-creator/SKILL.md` - 基本スキル作成
- `.claude/skills/README.md` - スキルインデックス
