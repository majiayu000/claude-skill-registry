---
name: sdd-adr
description: MADR形式のArchitecture Decision Record(ADR)を生成。技術選択の根拠・代替案・トレードオフを記録する。
argument-hint: "[title] [spec-slug] [target-dir(optional)]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep
model: opus
---

# sdd-adr — Architecture Decision Record Generator

## 0. 目的
- 重要な技術決定を記録し、将来の参照を可能に
- MADR（Markdown Any Decision Records）形式で標準化
- 代替案とトレードオフを明確化
- 決定の理由を後から追跡可能に

## 1. 入力と出力

### 入力
- /sdd-adr $ARGUMENTS
  - $0 = ADRタイトル（例: "認証方式としてJWTを採用"）
  - $1 = spec-slug（例: google-ad-report）
  - $2 = target-dir（任意。未指定なら `.kiro/specs/<spec-slug>/adr/` を使う）

### 出力（必須）
- <target-dir>/ADR-XXX-<slug>.md

### 参照
- templates/adr.template.md : ADRテンプレート
- <target-dir>/../requirements.md : 関連要件
- <target-dir>/../design.md : 関連設計

## 2. 重要ルール

1. **MADR形式**: 標準化されたセクション構造を使用
2. **代替案必須**: 最低2つの代替案（+ 何もしない）を検討
3. **トレードオフ明示**: 選択と却下の理由を客観的に記述
4. **ステータス管理**: Proposed → Accepted → Deprecated/Superseded

## 3. ADRステータス

| Status | 意味 |
|--------|------|
| **Proposed** | 提案中。レビュー待ち |
| **Accepted** | 承認済み。実装可能 |
| **Deprecated** | 非推奨。新規利用禁止 |
| **Superseded** | 後続ADRに置き換え |

## 4. 手順

### Step A: ADR番号の決定
1. 既存ADRをスキャン
2. 最大番号 + 1 を新ADR番号とする
3. ファイル名: ADR-XXX-<slug>.md

### Step B: Context（背景・課題）
1. 解決すべき問題を明確に記述
2. 制約条件（技術・ビジネス・時間・コスト）
3. 関連する要件（REQ-xxx）

### Step C: Decision（決定）
1. 選択した技術/アプローチ
2. 選択理由（3つ以上）
3. 詳細な説明（コード例/ダイアグラムあれば含む）

### Step D: Consequences（影響）
1. 良い影響（Benefits）
2. 悪い影響（Drawbacks）
3. トレードオフ表（複数観点で比較）

### Step E: Alternatives Considered（代替案）
各代替案に:
1. 概要
2. メリット
3. デメリット
4. 却下理由

最低限含める代替案:
- 代替案1: 別の技術選択
- 代替案2: 別のアプローチ
- 代替案3: 何もしない（現状維持）

### Step F: Implementation（実装計画）
1. マイルストーン
2. 関連タスク（TASK-xxx）
3. リスクと緩和策

### Step G: Validation（検証）
1. 成功基準
2. 検証方法
3. レビュー予定

## 5. ADR命名規則

```
ADR-XXX-<kebab-case-slug>.md

例:
ADR-001-jwt-authentication.md
ADR-002-postgresql-database.md
ADR-003-react-frontend.md
```

## 6. 実行例

```bash
/sdd-adr "認証方式としてJWTを採用" google-ad-report
```

出力:
- .kiro/specs/google-ad-report/adr/ADR-001-jwt-authentication.md

## 7. ADR一覧管理

各specディレクトリに `adr/README.md` を自動生成し、ADR一覧を管理:

```markdown
# ADR一覧

| ID | タイトル | Status | Created |
|----|---------|--------|---------|
| ADR-001 | JWTを認証方式として採用 | Accepted | 2026-02-02 |
```
