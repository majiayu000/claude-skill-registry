---
name: reviewer-common
description: 各レビュアーエージェント（backend, frontend, database, security, infra, req, basic-design, detailed-design）の共通設定、動作モード、出力形式、スコアリング基準を定義
---

# レビュアー共通ガイドライン

> **参照元**: 全レビュアーエージェントの共通パターン

---

## 1. 共通設定

### 1.1 Frontmatter テンプレート（実装レビュアー用）

```yaml
---
description: {専門領域}を専門的にレビューする{ペルソナ}
mode: subagent
model: google/antigravity-gemini-3-pro
temperature: 0.2
tools:
  read: true
  glob: true
  grep: true
  mcp__container-use__environment_file_read: true
  mcp__container-use__environment_file_list: true
  write: false
  edit: false
  bash: false
---
```

### 1.2 Frontmatter テンプレート（設計レビュアー用）

```yaml
---
description: {設計書種別}をレビューし10点満点でスコアリングする
model: google/antigravity-gemini-3-pro
mode: subagent
temperature: 0.2
tools:
  read: true
  glob: true
  grep: true
  write: false
  edit: false
  bash: false
---
```

---

## 2. 共通動作モード

### 2.1 モード切り替え

| モード | 対象 | 目的 |
|-------|------|------|
| **Mode A: 設計レビュー** | `*設計書.md` | 設計フェーズでの品質保証 |
| **Mode B: 実装レビュー** | ソースコード、Git Diff | 実装コードの品質保証 |

### 2.2 Diff-Driven Review (Mode B)

> **Token最適化**: 実装レビュー時は、必ず「差分（Diff）」を最優先で確認する。

**手順:**

1. `git diff origin/main...HEAD` を読む
2. 変更されたファイルと行を特定
3. 文脈が必要な場合のみ `read(offset, limit)` で周辺を読む
4. **禁止**: 変更がないファイルの全文読み込み

---

## 3. 共通出力形式

### 3.1 実装レビュー出力

```markdown
## {専門領域}実装レビュー結果

### スコア: X/10点

### 各項目の評価
| 項目 | スコア | 詳細 |
|------|--------|------|
| {観点1} | 0-N | ... |
| {観点2} | 0-N | ... |

### 指摘事項（修正必須）
1. [ファイル名] 行番号: 問題の説明
   - 問題: 
   - 修正案: 
   - 理由: 

### 判定
[PASS / FAIL] (9点以上で合格)
```

### 3.2 設計レビュー出力

```markdown
## レビュー結果

### スコア: X/10点

### 各項目の評価
| 項目 | スコア | 詳細 |
|------|--------|------|
| {観点1} | 0-N | コメント |
| {観点2} | 0-N | コメント |

### 問題点
1. [重大度: 高/中/低] 問題の説明
   - 該当箇所: 
   - 修正提案: 

### 改善提案
- 提案1
- 提案2

### 良い点
- 良い点1

### 合格判定: [合格/不合格]
```

### 3.3 最終出力（全レビュアー共通）

```
SCORE: [数値]/10
PASSED: [true/false]
```

---

## 4. スコアリング基準

> **参照**: 合格閾値の正式定義は {{skill:workflow-phase-convention}} §レビュースコア閾値を参照

### 4.1 合格閾値

| レビュアー | 合格閾値 | 備考 |
|-----------|---------|------|
| req-reviewer | 8点以上 | 要件定義 |
| basic-design-reviewer | 9点以上 | 基本設計 |
| detailed-design-reviewer | 9点以上 | 詳細設計 |
| backend-reviewer | 9点以上 | 実装 |
| frontend-reviewer | 9点以上 | 実装 |
| database-reviewer | 9点以上 | 実装 |
| security-reviewer | 9点以上 + Critical/High=0 | 実装 |
| infra-reviewer | 8点以上 | 複雑性考慮 |

### 4.2 配点ガイドライン

| 合計点 | 領域数 | 推奨配点例 |
|--------|--------|-----------|
| 10点 | 4領域 | 3+3+2+2 |
| 10点 | 5領域 | 2+2+2+2+2 |

### 4.3 スコア定義（2点満点の場合）

| スコア | 状態 | 説明 |
|--------|------|------|
| 2点 | 優秀 | 完璧またはそれに近い |
| 1点 | 普通 | 基本要件は満たす |
| 0点 | 不十分 | 重大な問題あり |

### 4.4 重大度定義

| 重大度 | 説明 |
|--------|------|
| 高 | 根幹に関わる問題。修正必須 |
| 中 | 品質に影響。修正推奨 |
| 低 | 軽微。修正でより良くなる |

---

## 5. 共通ルール

### 5.1 全レビュアー共通

1. **建設的**: 問題だけでなく修正案を必ず提示
2. **具体的**: ファイル名、行番号、コード例を含める
3. **優先度明示**: 修正必須と任意提案を区別
4. **一貫性**: プロジェクトの既存パターンを尊重

### 5.2 実装レビュアー追加ルール

- Diff-Driven Review を使用
- 変更がないファイルの全文読み込み禁止
- 常に具体的なファイルパスと行番号を提示

### 5.3 良い指摘例

```markdown
1. [src/auth/service.ts] 45行目: 認証トークンの検証漏れ
   - 問題: JWT有効期限チェックが未実装
   - 修正案: `jwt.verify()` に `maxAge` を追加
   - 理由: 期限切れトークンでのアクセス許可リスク
```

### 5.4 悪い指摘例

```markdown
1. 認証の実装が不十分  ← 曖昧、修正箇所不明
```
