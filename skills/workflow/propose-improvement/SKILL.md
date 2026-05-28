---
name: propose-improvement
description: ワークフロー改善提案の起案からIssue化までを行う（ROI分析・アクションプラン付）
---

# ワークフロー改善提案プロセス

現場の気づきを体系的な提案書に昇華し、実装可能なタスク（GitHub Issue）として具体化します。

## 入力

$ARGUMENTS（改善のテーマ）

---

## 全体フロー

| Phase | 名称 | 内容 |
|-------|------|------|
| 0 | 入力解析 | テーマの分析、関連ファイル・ログの収集 |
| 0.5 | 既存提案確認 | `docs/proposals/` の既存提案との重複確認 |
| 1 | 現状分析 & 起案 | As-Is分析、ROI試算、ドラフト作成 |
| 2 | レビュー & 洗練 | ユーザーへのドラフト提示、フィードバック反映 |
| 2.5 | ユーザー承認 | `approval-gate` skill |
| 3 | 確定 & Issue化 | ステータス更新、GitHub Issue作成 |

> **Phase規約**: `workflow-phase-convention` skill を参照

---

## サーキットブレーカー

| 条件 | アクション |
|------|----------|
| **既存提案と重複** | 既存提案を提示、統合 or 中断を確認 |
| **レビュー2回失敗** | 現状をユーザーに報告、判断を仰ぐ |
| **ROI算出不能** | 定性的効果のみで続行、警告を付与 |

---

## Phase 0: 入力解析

1. 改善テーマを分析
2. 関連ファイル・ログ・ルールを収集
3. 影響範囲を特定

---

## Phase 0.5: 既存提案確認

```bash
# 既存提案の確認
ls docs/proposals/*.md 2>/dev/null || echo "No existing proposals"
```

| チェック項目 | 確認内容 |
|-------------|---------|
| 重複提案 | 同一テーマの既存提案がないか |
| 関連提案 | 類似テーマの提案との整合性 |

**ユーザー確認オプション**: `1. 続行` / `2. 統合` / `3. 中断`（番号選択）

---

## Phase 1: 現状分析 & 起案

1. **現状分析 (As-Is)**: 具体的にどの作業が非効率か？（ログ、ファイル、現状のルールから分析）
2. **ROI試算**: その改善により、どれだけの「時間」「トークン」「精神的負荷」が削減できるか？
3. **ドラフト作成**: 指定テンプレートに基づき `docs/proposals/` にドラフトを作成

---

## Phase 2: レビュー & 洗練

1. ユーザーにドラフトを提示
2. フィードバックを収集
3. 必要に応じて修正（最大2回）

---

## Phase 2.5: ユーザー承認ゲート

> **共通仕様**: `approval-gate` skill を参照

```markdown
## 承認リクエスト: 改善提案の確定

**提案タイトル**: {title}
**推定ROI**: {roi_summary}

### 提案サマリー
{executive_summary}

---
**選択肢**:

1. 続行 → Phase 3（Issue作成）へ進む
2. 却下 → 提案を却下、ファイルを削除
3. 修正 → Phase 1に戻り修正

> 番号を選択してください（1-3）:
```

---

## Phase 3: 確定 & Issue化

1. ドキュメントのステータスを `Open` に更新
2. **GitHub Issueを作成**（提案書へのリンクを含む）
3. Issueには `improvement-proposal` ラベルを付与

```bash
# Issue作成
gh issue create \
  --title "改善提案: {title}" \
  --body "$(cat <<'EOF'
## 概要
{executive_summary}

## 提案書
[PROP-{id}.md](docs/proposals/PROP-{id}.md)

## 期待効果
{roi_summary}
EOF
)" \
  --label "improvement-proposal"
```

---

## 提案書テンプレート (Strict Format)

```markdown
---
id: PROP-{YYYYMMDD}-NNN
title: {title}
status: Draft  # Draft | Open | Accepted | Rejected | Implemented
author: Sisyphus
date: {YYYY-MM-DD}
---

# {Title}

## 1. Executive Summary
<!-- 提案の核心を3行以内で -->

## 2. Problem & Context (As-Is)
### 現状の課題
<!-- 具体的なペインポイント。例: "〇〇の手順が手動で発生し、毎回5分ロスしている" -->

### 発生頻度・影響範囲
<!-- 例: チーム全体で毎日発生、〇〇機能の開発に影響 -->

## 3. Solution (To-Be)
### 改善案
<!-- 具体的な解決策。新しいコマンド、ツール設定、ルール変更など -->

### 期待される効果 (ROI)
| 項目 | 現状 (Cost) | 改善後 (Benefit) | 効果 (Delta) |
|------|-------------|------------------|--------------|
| 時間 | 例: 10分/回 | 例: 1分/回 | 90%削減 |
| 品質 | 手動ミスあり | 自動化 | ミスゼロ |
| トークン | 大 | 小 | 節約 |

## 4. Implementation Details
### 具体的な変更点
- [ ] ファイル: `path/to/file`
- [ ] コマンド: `/new-command`
- [ ] ルール: `SKILL.md` の修正

### 依存関係・リスク
<!-- 既存機能への影響、学習コストなど -->

## 5. Next Actions
- [ ] GitHub Issue作成
- [ ] 実装担当割り当て: （例: 自分、他のメンバー）
- [ ] 適用ワークフロー: （例: /implement, /basic-design-workflow）
```

## 実行プロンプト（document-writerへの指示）

```markdown
あなたは「厳格なエンジニアリングマネージャー」兼「テクニカルライター」です。
以下の情報を元に、単なるアイデアメモではなく、**「投資判断が可能」なレベルの改善提案書**を作成してください。

**入力情報**:
- テーマ: {theme}
- コンテキスト: {context}

**制約事項**:
1. **ROI分析を必須とする**: 数値（概算で可）を用いて効果をアピールすること。
2. **アクション重視**: 抽象的な「良くする」ではなく、「どのファイルをどう変えるか」まで踏み込むこと。
3. **ファイルパス**: `docs/proposals/PROP-{YYYYMMDD}-{kebab-case-title}.md`
4. **Issue連携**: ドキュメント作成後、Phase 2.5でユーザー承認を得てからIssue作成に進むこと。
```

---

## 参考スキル

| スキル | 用途 |
|--------|------|
| `approval-gate` skill | ユーザー承認ゲート |
| `workflow-phase-convention` skill | Phase命名規約 |

---

## 変更履歴

| バージョン | 変更内容 |
|-----------|---------|
| v2.0 | Phase構造に再構成、全体フロー表追加、承認ゲート追加 |
| v1.0 | 初版 |
