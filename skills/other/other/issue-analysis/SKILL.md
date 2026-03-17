---
name: Issue Analysis with Label Inference
description: Analyze GitHub Issues and automatically infer appropriate labels from Miyabi's 57-label system across 11 categories. Use when creating or triaging Issues, or when label inference is needed.
allowed-tools: Read, Grep, Glob, WebFetch
---

# 🏷️ Issue Analysis with Label Inference

**Version**: 2.0.0
**Last Updated**: 2025-11-22
**Priority**: ⭐⭐⭐⭐ (P1 Level)
**Purpose**: AI駆動のIssue分析と57ラベルシステムからの自動推論

---

## 📋 概要

Miyabiの57ラベルシステム（11カテゴリ）に基づいたAI駆動のIssue分析と
自動ラベル推論を実行します。

---

## 🎯 P0: 呼び出しトリガー

| トリガー | 例 |
|---------|-----|
| ラベル質問 | "what labels should I use?" |
| Issue分析 | "analyze this Issue", "triage issue #270" |
| ラベル推論 | "infer labels for this Issue" |
| Issue作成後 | Issue作成後の自動処理 |
| バックログ管理 | "prioritize backlog" |

---

## 🔧 P1: ラベルカテゴリ一覧

### 11カテゴリ・57ラベル

| # | カテゴリ | 数 | 必須/任意 | 用途 |
|---|---------|-----|---------|------|
| 1 | **STATE** | 8 | 自動 | ライフサイクル管理 |
| 2 | **AGENT** | 6 | 推奨 | Agent割り当て |
| 3 | **PRIORITY** | 4 | 必須 | 優先度管理 |
| 4 | **TYPE** | 7 | 必須 | Issue分類 |
| 5 | **SEVERITY** | 4 | 条件 | 重大度（バグのみ） |
| 6 | **PHASE** | 5 | 推奨 | プロジェクトフェーズ |
| 7 | **SPECIAL** | 7 | 条件 | 特殊フラグ |
| 8 | **TRIGGER** | 4 | 自動 | 自動化トリガー |
| 9 | **QUALITY** | 4 | 自動 | 品質スコア |
| 10 | **COMMUNITY** | 4 | 推奨 | コミュニティ |
| 11 | **HIERARCHY** | 4 | 自動 | Issue階層 |

---

## 🚀 P2: ラベル推論ルール

### TYPE推論（必須・1個）

| キーワード | ラベル | 例 |
|-----------|--------|-----|
| "add", "implement", "create", "new" | `✨ type:feature` | 新機能追加 |
| "fix", "crash", "error", "broken" | `🐛 type:bug` | バグ修正 |
| "docs", "README", "guide" | `📚 type:docs` | ドキュメント |
| "refactor", "cleanup", "reorganize" | `🔧 type:refactor` | リファクタ |
| "test", "coverage", "e2e" | `🧪 type:test` | テスト |
| "architecture", "system design" | `🏗️ type:architecture` | アーキテクチャ |
| "deploy", "CI/CD", "docker" | `🚀 type:deployment` | デプロイ |

### PRIORITY推論（必須・1個）

| 条件 | ラベル | SLA |
|------|--------|-----|
| セキュリティ、本番障害、データ損失 | `🔥 priority:P0-Critical` | 24時間 |
| 主要機能、重大バグ、性能劣化 | `⚠️ priority:P1-High` | 3日 |
| 通常機能、標準バグ | `📊 priority:P2-Medium` | 1週間 |
| 軽微改善、typo | `📝 priority:P3-Low` | なし |

### SEVERITY推論（条件付き・バグのみ）

| 条件 | ラベル | エスカレーション |
|------|--------|----------------|
| 本番停止、セキュリティ侵害 | `🚨 severity:Sev.1-Critical` | Guardian + CISO |
| 主要機能障害 | `⚠️ severity:Sev.2-High` | TechLead |
| 部分的機能問題 | `📊 severity:Sev.3-Medium` | Agent自動 |
| 軽微UI問題 | `📝 severity:Sev.4-Low` | Agent自動 |

### SPECIAL推論（条件付き）

| キーワード | ラベル | アクション |
|-----------|--------|-----------|
| "XSS", "SQL injection", "CVE" | `🔐 security` | CISO通知、Issue非公開 |
| "Claude API", "high cost" | `💰 cost-watch` | 予算監視 |
| "depends on #", "blocked by" | `🔄 dependencies` | 依存解決まで待機 |
| "research", "investigate" | `🎓 learning` | SLA延長 |
| "experiment", "POC" | `🔬 experiment` | 失敗許容 |

### COMMUNITY推論（推奨）

| 条件 | ラベル |
|------|--------|
| 2時間以内、依存なし、明確な要件 | `👋 good-first-issue` |
| 外部専門知識が必要 | `🙏 help-wanted` |

### HIERARCHY推論（自動）

| 条件 | ラベル |
|------|--------|
| 親Issueなし | `🌳 hierarchy:root` |
| 子Issueあり | `📂 hierarchy:parent` |
| 親Issueあり | `📄 hierarchy:child` |
| 子Issueなし（末端） | `🍃 hierarchy:leaf` |

---

## ⚡ P3: 分析ワークフロー

### Step 1: Issue内容読み取り

```
- タイトル
- 本文（説明）
- コメント（あれば）
- 関連Issue（リンク）
```

### Step 2: キーワード抽出

```
- 技術キーワード: "security", "performance", "API"
- アクションキーワード: "add", "fix", "refactor"
- 緊急度キーワード: "urgent", "critical", "nice-to-have"
```

### Step 3: 推論ルール適用

```
1. TYPE決定（必須、1個）
2. PRIORITY決定（必須、1個）
3. SEVERITY決定（バグ/インシデント時）
4. SPECIAL条件チェック
5. COMMUNITY適合性評価
6. HIERARCHY位置決定
```

### Step 4: ラベルセット生成

```json
{
  "required": ["type:feature", "priority:P1-High"],
  "recommended": ["agent:codegen", "phase:planning"],
  "optional": ["security", "cost-watch"],
  "automatic": ["state:pending", "hierarchy:leaf"]
}
```

---

## 📊 出力フォーマット

### JSON形式

```json
{
  "issue_number": 270,
  "title": "XSS vulnerability in comment form",
  "analysis": {
    "type": "bug",
    "priority": "P0-Critical",
    "severity": "Sev.1-Critical",
    "estimated_time": "4-6 hours",
    "complexity": "medium",
    "agent_recommendation": "codegen + review",
    "escalation": "Guardian + CISO"
  },
  "labels": {
    "required": ["type:bug", "priority:P0-Critical"],
    "recommended": ["severity:Sev.1-Critical", "security"],
    "automatic": ["state:pending", "hierarchy:leaf"]
  },
  "rationale": {
    "type": "Keywords: 'vulnerability', 'XSS'",
    "priority": "Security issue with global impact",
    "severity": "Security vulnerability"
  }
}
```

### テキスト形式

```
🏷️ Issue Analysis Results

📋 Issue #270: XSS vulnerability in comment form

📊 Analysis:
- Type: bug (Keywords: 'vulnerability', 'XSS')
- Priority: P0-Critical (Security, global impact)
- Severity: Sev.1-Critical (Security vulnerability)
- Estimated: 4-6 hours
- Agent: codegen + review

🏷️ Labels:
✅ Required: type:bug, priority:P0-Critical
📎 Recommended: severity:Sev.1-Critical, security
🔄 Automatic: state:pending, hierarchy:leaf

⚠️ Escalation: Guardian + CISO (immediately)
```

---

## 🛡️ エラーハンドリング

### キーワード検出失敗

```
# デフォルトフォールバック
TYPE: type:feature (不明な場合)
PRIORITY: priority:P2-Medium (不明な場合)
```

### 複数TYPE該当

```
# 優先順位で決定
bug > security > feature > docs > test > chore
```

### コンフリクトするラベル

```
# 相互排他ラベルのチェック
state:pending ⊕ state:in-progress
priority:P0 ⊕ priority:P1
```

---

## ✅ 成功基準

| チェック項目 | 基準 |
|-------------|------|
| TYPE推論 | 1個選択 |
| PRIORITY推論 | 1個選択 |
| SEVERITY推論 | バグ時のみ |
| SPECIAL検出 | 該当時のみ |
| 根拠提示 | 各ラベルに理由 |
| エスカレーション | 必要時に推奨 |

---

## 🔗 関連ドキュメント

| ドキュメント | 用途 |
|-------------|------|
| `docs/LABEL_SYSTEM_GUIDE.md` | ラベルシステム詳細 |
| `.github/labels.yml` | ラベル定義 |
| `agents/specs/coding/issue-agent.md` | IssueAgent仕様 |
| `docs/ENTITY_RELATION_MODEL.md` | エンティティ関係 |

---

## 📝 関連Skills

- **Agent Execution**: ラベル割り当て後のAgent実行
- **Git Workflow**: Issue解決後のコミット
- **Rust Development**: 実装品質チェック
