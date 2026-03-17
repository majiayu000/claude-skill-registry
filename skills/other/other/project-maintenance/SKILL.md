---
name: project-maintenance
description: プロジェクトメンテナンス統合監査。複雑度（Lizard）・セキュリティ（Gitleaks/npm audit）・デッドコード（Knip）の3つの監査を統合実行し、リファクタリング対象を優先順位付けして特定する。リファクタリング計画、コード品質チェック、PR作成前の包括的監査に使用。
allowed-tools: Bash, Read
---

# Project Maintenance Protocol

ユーザーからリファクタリング計画、コード品質チェック、または包括的な監査を求められた場合、以下の手順を実行せよ。

## 概要

このスキルは以下の3つの監査を統合し、**1コマンドで実行**できます：

1. **複雑度解析（Lizard）** - 循環的複雑度（CCN）を測定し、リファクタリング対象を特定
2. **セキュリティ監査（Gitleaks + npm audit）** - シークレット漏洩と依存関係の脆弱性を検出
3. **デッドコード検出（Knip）** - 未使用ファイル・依存関係・エクスポートを特定

**統合の利点:**
- 横断的な優先順位付け（複雑度が高く、かつデッドコードも多いファイルなど）
- 1つの統合レポートで全体像を把握
- リファクタリング効率の向上

---

## 前提条件

以下のツールがインストールされていること：

| ツール | インストール | 用途 |
|--------|-------------|------|
| **Lizard** | `pip install lizard` | 複雑度解析 |
| **Gitleaks** | [公式サイト](https://github.com/zricethezav/gitleaks) | シークレット検出 |
| **Knip** | `npm install -D knip` | デッドコード検出 |

> Windowsの場合、Gitleaksは `gitleaks.exe` として `C:\Users\kensa\bin` にインストール済み。

---

## 実行コマンド

### 統合監査（推奨）

すべての監査を一括実行：

```bash
uv run scripts/run-project-maintenance.py --output maintenance-report.md
```

### 個別監査

特定の監査のみ実行：

```bash
# 複雑度解析のみ
uv run scripts/run-project-maintenance.py --complexity --output complexity-report.md

# セキュリティ監査のみ
uv run scripts/run-project-maintenance.py --security --output security-report.md

# デッドコード検出のみ
uv run scripts/run-project-maintenance.py --deadcode --output deadcode-report.md

# 複数を組み合わせ
uv run scripts/run-project-maintenance.py --complexity --security --output report.md
```

### 閾値カスタマイズ

```bash
uv run scripts/run-project-maintenance.py --ccn-threshold 20 --nloc-threshold 60 --output report.md
```

### 標準出力に表示

```bash
uv run scripts/run-project-maintenance.py
```

---

## 閾値設定

### 複雑度（CCN）

| 指標 | 閾値 | 説明 |
|------|------|------|
| CCN（循環的複雑度） | **15** | 条件分岐・ループの複雑さ。15超は要リファクタリング |
| NLOC（論理行数） | **50** | 関数の長さ。50行超は分割を検討 |

#### CCN重症度レベル

| レベル | CCN範囲 | 対応 |
|--------|---------|------|
| 正常 | 1-10 | 問題なし |
| 注意 | 11-15 | モニタリング |
| 警告 | 16-25 | リファクタリング推奨 |
| 危険 | 26-50 | リファクタリング必須 |
| 即対応 | 51+ | 即座に分割すべき |

---

## 統合レポートフォーマット

```markdown
# プロジェクトメンテナンスレポート

**日時**: 2026-02-05
**対象**: RoastPlus

## 📊 総合サマリー

| カテゴリ | ステータス | 重要度HIGH | 要対応 |
|---------|-----------|-----------|--------|
| 複雑度 | ⚠️ WARNING | 3件 | 5件 |
| セキュリティ | ✅ PASS | 0件 | 0件 |
| デッドコード | ⚠️ WARNING | 0件 | 76件 |

## 🎯 優先アクション（統合推奨順）

1. 【最優先】`DesktopTableView:DesktopTableView` 複雑度削減 (CCN: 125)
2. 【最優先】`TableModals:TableModals` 複雑度削減 (CCN: 117)
3. 【高】`page.tsx:(anonymous)` 複雑度削減 (CCN: 97)
4. 【中】未使用依存関係削除 (3件)
5. 【中】未使用ファイル削除 (4件)
6. 【低】未使用エクスポート削除 (76件)

## 詳細レポート

### 1. 複雑度解析
[複雑度の詳細]

### 2. セキュリティ監査
[セキュリティの詳細]

### 3. デッドコード検出
[デッドコードの詳細]
```

---

## 分析手順

### Step 1: 統合監査の実行

上記コマンドを実行し、3つの監査結果を取得する。

### Step 2: 優先順位の判定

統合レポートの「優先アクション」セクションを確認し、以下の基準で優先順位を付ける：

#### 優先度判定基準

1. **セキュリティ問題（最優先）**
   - シークレット漏洩
   - Critical/High脆弱性

2. **複雑度が極めて高い関数（CCN 51+）**
   - 即座に分割すべき

3. **複雑度が高い関数（CCN 26-50）**
   - 計画的にリファクタリング

4. **デッドコード（中優先度）**
   - 未使用依存関係・ファイル

5. **デッドコード（低優先度）**
   - 未使用エクスポート（バレルファイル経由の可能性あり）

### Step 3: リファクタリング計画の策定

優先順位に基づいて、具体的なリファクタリング手法を提案：

### Step 4: リファクタリングIssue + Working Documents自動生成

統合監査の結果、リファクタリングが必要な場合、Issue作成とWorking Documents生成を連携します。

#### 自動生成フロー

```
1. project-maintenance実行 → 2. 優先順位判定 → 3. Issue自動作成 → 4. Working自動生成
```

#### Issue自動作成の条件

以下のいずれかに該当する場合、自動的にIssueを作成することを提案:

| 優先度 | 条件 | Issueタイプ |
|--------|------|------------|
| 最優先 | シークレット漏洩・Critical脆弱性 | `bug`（セキュリティ） |
| 最優先 | CCN 51+ | `refactor`（複雑度削減） |
| 高 | CCN 26-50 | `refactor`（複雑度削減） |
| 中 | 未使用依存関係3件以上 | `chore`（依存関係整理） |

#### Issue作成例

```bash
# 複雑度が極めて高い関数が検出された場合
gh issue create --title "refactor(assignment-table): DesktopTableViewの複雑度削減 (CCN: 125)" \
  --body-file /tmp/refactor_issue.md \
  --label "refactor"

# 作成後、Working Documents自動生成
/create-spec 124
```

#### Issue本文テンプレート（複雑度削減）

```markdown
## 概要
複雑度が極めて高い関数をリファクタリングして可読性・保守性を向上させる。

## 理由/背景
プロジェクトメンテナンス監査で検出:
- **CCN**: 125（閾値: 15）
- **NLOC**: 289行（閾値: 50）
- **重症度**: 即対応

## 対象箇所
- `components/assignment-table/DesktopTableView.tsx:15` - DesktopTableView関数

## 作業内容
- [ ] ガード節の導入（早期リターン）
- [ ] 関数の抽出（責務分割）
- [ ] コンポーネント分割（子コンポーネント化）
- [ ] テストカバレッジ確保

## 影響範囲
- assignment-table機能全体
- TableModalsとの連携部分
```

#### Working Documents自動生成の統合

Issue作成後、`/create-spec` スキルを自動実行:

1. project-maintenanceが優先アクションを特定
2. ユーザーに「Issue + Working Documentsを自動生成しますか？」と確認
3. 承認後、issue-creatorでIssue作成
4. `/create-spec [Issue番号]` で Working Documents生成
5. `/fix-issue [Issue番号]` で実装開始可能

これにより、リファクタリング計画から実装までのワークフローが完全に統合されます。

### Step 5: リファクタリング手法の提案

#### 複雑度削減の手法（Step 5で使用）

1. **ガード節の導入** - 早期リターンでネストを削減
2. **関数の抽出** - 一つの責務に分割
3. **ストラテジーパターン** - 条件分岐をポリモーフィズムで置換
4. **テーブル駆動** - switch/if-else チェーンをマップに変換
5. **コンポーネント分割** - 巨大なReactコンポーネントを子コンポーネントに分離

#### セキュリティ問題の対応

- **シークレット漏洩**: `.env.local` に移動、`.gitignore` に追加、Git履歴から削除
- **脆弱性**: `npm audit fix` で修正、必要に応じて手動更新

#### デッドコードの削除

- **未使用依存関係**: `npm uninstall <package>`
- **未使用ファイル**: 確認後に削除
- **未使用エクスポート**: バレルファイル経由でないか確認後に削除

---

## 使用タイミング

### 定期実行（推奨）

- **週次**: 開発サイクルごとに実行
- **PR作成前**: 必ず実行して品質を確認
- **リリース前**: 大規模リリース前の総合チェック

### 特定シナリオ

- **リファクタリング計画**: 対象範囲の特定に使用
- **コードレビュー**: レビュー前の自己チェック
- **パフォーマンス改善**: ボトルネック特定の起点

---

## CI/CD統合

GitHub Actionsなどで自動実行を設定することを推奨：

```yaml
name: Project Maintenance
on:
  pull_request:
    branches: [main]

jobs:
  maintenance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Project Maintenance
        run: |
          pip install lizard
          npm ci
          uv run scripts/run-project-maintenance.py --output report.md
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: maintenance-report
          path: report.md
```

---

## ベースライン（2026-02-01 測定）

初回測定結果：

### 複雑度 Top 3

| ファイル | 関数名 | CCN | NLOC |
|---------|--------|-----|------|
| `assignment-table/DesktopTableView.tsx` | `DesktopTableView` | 125 | 289 |
| `assignment-table/TableModals.tsx` | `TableModals` | 117 | 414 |
| `coffee-trivia/stats/page.tsx` | `(anonymous)` | 97 | 193 |

### デッドコード

| カテゴリ | 件数 |
|---------|------|
| 未使用ファイル | 4件 |
| 未使用依存関係 | 3件 |
| 未使用エクスポート | 76件 |

### セキュリティ

- シークレット検出: なし
- 依存関係脆弱性: 定期チェック推奨

---

## 注意事項

### デッドコード検出の偽陽性

- **バレルファイル（`index.ts`）経由の再エクスポート**: 実際には使われていても検出される場合がある
- **動的インポート**: 静的解析では検出できない場合がある
- **テストコード**: テストでのみ使用される関数が検出される場合がある

→ 削除前に必ず確認すること。

### 複雑度の妥当性

- **ビジネスロジックの複雑さ**: 本質的に複雑な処理は、無理に削減しない
- **テストカバレッジ**: リファクタリング前に十分なテストを書く

---

*このスキルは `complexity-audit`, `security-audit`, `deadcode-audit` の3つを統合したものです。*
