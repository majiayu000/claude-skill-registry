---
name: find-refactoring
description: コードベースからリファクタリング候補を検出し、優先度付きでGitHub Issueを作成します
---

# リファクタリング候補検出コマンド

コードベースを分析し、リファクタリングが必要な箇所を検出してGitHub Issueを作成します。

---

## 入力

$ARGUMENTS（対象パス、オプション）

例:
- `/find-refactoring src/` - src配下を分析
- `/find-refactoring --dry-run` - Issue作成せずレポートのみ
- `/find-refactoring src/ --min-priority=high` - 高優先度のみ

---

## 前提条件

> **詳細**: `refactoring-detection` skill を参照

| ツール | 必須/任意 | フォールバック |
|--------|---------|---------------|
| `ast-grep (sg)` | **必須** | エラー終了 |
| `jscpd` | 任意 | 重複検出スキップ |

---

## 全体フロー

| Phase | 名称 | 内容 |
|-------|------|------|
| 0 | 入力解析 | 対象パス・オプション解析 |
| 0.3 | 言語検出 | プロジェクト言語の自動判定 |
| 0.5 | ツール確認 | 必須ツールの存在確認 |
| 0.7 | 既存Issue確認 | 重複Issue防止チェック |
| 1 | 静的分析 | コード品質ルール違反の検出 |
| 2 | パターン分析 | コードスメル・重複の検出 |
| 3 | 優先度判定 | 優先度付与、粒度チェック |
| 3.5 | ユーザー確認 | `approval-gate` skill |
| 4 | Issue作成 | GitHub Issue作成（`--dry-run`時スキップ） |

> **Phase規約**: `workflow-phase-convention` skill を参照

---

## サーキットブレーカー

| 条件 | アクション |
|------|----------|
| **必須ツール不在** | エラー終了、インストール手順を表示 |
| **検出件数0件** | 「問題なし」を報告して終了 |
| **検出件数30件超** | 上位15件のみ表示、`--min-priority=high`を提案 |
| **Issue作成失敗** | 失敗分をレポート、成功分は継続 |

---

## Phase 0.3-0.7: 事前準備

### 言語検出

```bash
LANG=$(detect_language)  # typescript / rust / go / python
```

### ツール確認

```bash
check_required_tools || exit 1
check_optional_tools
```

### 既存Issue確認

```bash
EXISTING_ISSUES=$(get_existing_refactoring_issues)
```

> **実装詳細**: `refactoring-detection` skill を参照

---

## Phase 1-2: 検出実行

### 検出ルール

| カテゴリ | ルール | 優先度 |
|---------|--------|--------|
| **サイズ** | 500行超過ファイル | High |
| **サイズ** | 80行超過関数 | High |
| **サイズ** | 6引数超過関数 | Medium |
| **型安全** | `any`型使用 | High |
| **型安全** | ``ts-ignore` skill`使用 | Critical |
| **エラー処理** | 空catchブロック | High |
| **品質** | `console.log`残存 | Medium |
| **品質** | 重複コード（10行以上） | Medium |

### 言語別追加ルール

| 言語 | ルール | 優先度 |
|------|--------|--------|
| Rust | `todo!`/`unimplemented!`残存 | High |
| Rust | `unwrap()`多用（5箇所超/ファイル） | Medium |

> **検出パターン詳細**: `refactoring-detection` skill を参照

---

## Phase 3: 優先度・粒度判定

### 優先度基準

| 優先度 | 対応期限目安 |
|--------|-------------|
| Critical | 即時 |
| High | 1週間 |
| Medium | 2週間 |
| Low | 余裕時 |

### Issue粒度チェック

> 実装タスクは200行以下を対象

| 推定作業行数 | アクション |
|-------------|----------|
| 200行以下 | 単一Issueとして作成 |
| 200行超 | 「**要分割**」注記、`/decompose-issue`リンク付与 |

> **工数算出ロジック**: `refactoring-detection` skill を参照

---

## Phase 3.5: ユーザー確認

> **共通仕様**: `approval-gate` skill を参照

```markdown
## 検出されたリファクタリング候補

### サマリー
| 優先度 | 件数 |
|--------|------|
| Critical | {n} |
| High | {n} |
| Medium | {n} |

### 詳細（上位15件）

| # | ファイル | 問題 | 優先度 | 推定工数 | 備考 |
|---|---------|------|--------|---------|------|
| 1 | `src/foo.ts` | 723行（超過） | High | 1h | |
| 2 | `src/bar.ts` | any型 5箇所 | High | 25m | |
| 3 | `src/big.ts` | 1200行 | High | 3h | **要分割** |

### スキップ（既存Issue）
- `src/old.ts`: #45

---
**選択肢**:

1. 全件 → 全件Issue作成
2. High以上 → High以上のみ作成
3. 選択 → 指定番号のみ（例: `3 1,2,5`）
4. 終了 → 作成せず終了

> 番号を選択してください（1-4）:
```

---

## Phase 4: Issue作成

### ラベル事前作成

```bash
ensure_labels() {
    for label in refactoring automated priority/{critical,high,medium,low}; do
        gh label create "$label" --force 2>/dev/null || true
    done
}
```

### Issueテンプレート

```bash
gh issue create \
  --title "refactor: ${TITLE}" \
  --body "## 概要
${PROBLEM}

## 対象
- **ファイル**: \`${FILE_PATH}\`

## 推奨アクション
${ACTION}

## 推定工数
${EFFORT}
${DECOMPOSE_NOTE}

---
*\`/find-refactoring\` により自動生成*" \
  --label "refactoring,automated,priority/${PRIORITY}"
```

---

## 出力形式

### 成功時

```markdown
## リファクタリングIssue作成完了

| Issue | タイトル | 優先度 | 推定工数 |
|-------|---------|--------|---------|
| #101 | refactor: src/foo.ts 分割 | High | 1h |
| #102 | refactor: src/bar.ts any除去 | High | 25m |

### スキップ（既存Issue）
- `src/old.ts` → #45

### 次のステップ
1. 実装: `task #101 #102`
2. 大きなIssue分割: `/decompose-issue 103`
```

### dry-run時

```markdown
## リファクタリング候補レポート（dry-run）

| # | ファイル | 問題 | 優先度 | 推定工数 |
|---|---------|------|--------|---------|
| 1 | `src/foo.ts` | 723行超過 | High | 1h |

### Issue作成コマンド
\`/find-refactoring src/ --min-priority=high\`
```

---

## 完了条件

- [ ] 必須ツール（ast-grep）が利用可能
- [ ] 対象パスの分析が完了
- [ ] 既存Issueとの重複チェック済み
- [ ] 検出結果がユーザーに提示済み
- [ ] 承認されたIssueが作成済み（dry-run以外）
- [ ] 200行超Issueに分割推奨が注記済み

---

## 関連スキル

| スキル | 用途 |
|--------|------|
| `refactoring-detection` skill | 検出パターン・工数算出 |
| `code-quality-rules` skill | 品質ルール定義 |
| `issue-size-estimation` skill | Issue粒度判定 |
| `approval-gate` skill | ユーザー承認ゲート |

---

## 変更履歴

| バージョン | 変更内容 |
|-----------|---------|
| v1.2 | 検出ロジックをrefactoring-detectionスキルに分離 |
| v1.1 | 言語検出、ツール確認、既存Issue重複チェック、粒度チェック追加 |
| v1.0 | 初版作成 |
