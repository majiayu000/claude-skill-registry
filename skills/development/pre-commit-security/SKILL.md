---
name: pre-commit-security
description: |
  pre-commit hookセキュリティスキル。機密情報検出パターン、git-secrets/gitleaks統合、チーム展開戦略、Git履歴スキャンを実装し、コミット前の機密情報漏洩を防ぐ。

  Anchors:
  • Web Application Security (Andrew Hoffman) / 適用: 脅威モデリング・セキュア設計 / 目的: セキュリティリスクの体系的評価
  • OWASP Top 10 / 適用: 機密情報検出パターン設計 / 目的: 業界標準の脆弱性分類に基づくパターン定義
  • git-secrets / gitleaks公式ドキュメント / 適用: ツール統合・設定 / 目的: 公式ベストプラクティスに準拠した導入

  Trigger:
  Use when implementing pre-commit hooks for secret detection, designing detection patterns, integrating git-secrets/gitleaks, scanning Git history for leaked secrets, or deploying security hooks across teams.
  pre-commit security, secret detection, git-secrets, gitleaks, credential scanning, Git history scan
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Pre-commit Security Hooks

## 概要

pre-commit hookセキュリティスキル。コミット前に機密情報（APIキー、パスワード、接続文字列など）を自動検出し、誤ってリポジトリに含めることを防ぐ。git-secrets/gitleaksの統合、カスタム検出パターンの設計、チーム全体への展開戦略、Git履歴の遡及的スキャンをカバーする。

## ワークフロー

### Phase 1: 機密情報分析

**目的**: 検出すべき機密情報のパターンを特定

**アクション**:

1. プロジェクトで使用するクラウドサービス・APIを洗い出す
2. 検出すべきシークレットの種類（APIキー、接続文字列、証明書等）を特定
3. 既存コードベースをスキャンし、漏洩リスクを評価
4. 検出パターンの優先度を決定

**Task**: See [agents/analyze-secrets.md](agents/analyze-secrets.md)

### Phase 2: フック設定

**目的**: pre-commit hookを実装・統合

**アクション**:

1. git-secrets/gitleaksの選定と導入
2. カスタム検出パターンの実装
3. ホワイトリスト（誤検知除外）の設定
4. チーム展開戦略の策定（.git/hooks/共有方法）
5. CI/CD統合の実装

**Task**: See [agents/configure-hooks.md](agents/configure-hooks.md)

**ツール選択基準**:

| 条件                                 | 推奨ツール  | 理由                       |
| ------------------------------------ | ----------- | -------------------------- |
| AWS中心のプロジェクト                | git-secrets | AWS公式、軽量              |
| 多様なクラウドサービス使用           | gitleaks    | 包括的なパターンライブラリ |
| CI/CD統合が必須                      | gitleaks    | SARIF形式対応              |
| カスタムパターンのメンテナンスを重視 | git-secrets | シンプルな正規表現ベース   |

**詳細**: See [references/basics.md](references/basics.md) - ツール選択ガイド

### Phase 3: セキュリティ検証

**目的**: フックの有効性を検証し、継続的に改善

**アクション**:

1. テストケースによる検出精度の確認
2. Git履歴の遡及的スキャン（既存リークの発見）
3. 誤検知率の測定と調整
4. CI/CD統合の実装

**Task**: See [agents/validate-security.md](agents/validate-security.md)

**検証スクリプト**:

```bash
# Hook動作検証
node .claude/skills/pre-commit-security/scripts/validate-security.mjs

# 検出精度テスト
node .claude/skills/pre-commit-security/scripts/validate-security.mjs --test-mode

# Git履歴スキャン
node .claude/skills/pre-commit-security/scripts/scan-history.mjs --verbose --report=leak-report.json
```

## Task仕様ナビ

| Task              | 起動タイミング | 入力                           | 出力                              |
| ----------------- | -------------- | ------------------------------ | --------------------------------- |
| analyze-secrets   | Phase 1開始時  | コードベース、使用サービス一覧 | 検出パターン仕様、リスク評価      |
| configure-hooks   | Phase 2開始時  | 検出パターン仕様               | 設定済みpre-commit hook、展開計画 |
| validate-security | Phase 3開始時  | 設定済みhook                   | 検証レポート、履歴スキャン結果    |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **導入時**:
  - プロジェクトで使用するクラウドサービスを洗い出してから導入
  - git-secrets/gitleaksのツール選択基準に従う
  - 必ずホワイトリストを設定（`.env.example`等）

- **パターン設計時**:
  - プロバイダー固有パターンを優先（AWS、OpenAI、Anthropic等）
  - エントロピーベース検出はホワイトリストと併用
  - 定期的なパターン更新（四半期ごと推奨）

- **チーム展開時**:
  - `.githooks/` で共有hookを管理
  - README.mdにセットアップ手順を記載
  - セットアップスクリプトを提供

- **運用時**:
  - CI/CDで必須チェックを実施（ローカルhookの補完）
  - Git履歴スキャンを初回セットアップ時に必ず実施
  - 検出精度メトリクスを定期測定（TP率≥95%、FP率≤5%）

### 避けるべきこと

- **導入時**:
  - ホワイトリストなしで運用しない（誤検知多発）
  - チーム展開戦略なしで個人設定のままにしない
  - Git履歴スキャンを省略しない（既存リークが残る）

- **パターン設計時**:
  - 検出パターンを確認せずに導入しない
  - 広範すぎるエントロピーパターンを使用しない
  - パターン更新を怠らない（新サービス対応）

- **運用時**:
  - CI/CD統合なしでローカルのみに依存しない
  - `--no-verify` を常用しない（緊急時もホワイトリストで対応）
  - リーク発見時にシークレットローテーションを遅延させない

## リソース参照

### references/（詳細知識）

| リソース           | パス                                                                                   | 内容                                                     |
| ------------------ | -------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 基礎ガイド         | See [references/basics.md](references/basics.md)                                       | pre-commit hookの仕組み、ツール選択、基本設定            |
| 検出パターン設計   | See [references/patterns.md](references/patterns.md)                                   | 正規表現、エントロピー検出、ホワイトリスト戦略           |
| パターンライブラリ | See [references/detection-pattern-library.md](references/detection-pattern-library.md) | AWS/GCP/OpenAI/GitHub等のパターン集                      |
| チーム展開戦略     | See [references/deployment.md](references/deployment.md)                               | 共有hook、husky統合、強制適用戦略                        |
| CI/CD統合          | See [references/ci-integration.md](references/ci-integration.md)                       | GitHub Actions、GitLab CI、その他CI/CDサービス統合ガイド |

### agents/（Task仕様書）

| Task              | パス                                                           | 入力                       | 出力                           |
| ----------------- | -------------------------------------------------------------- | -------------------------- | ------------------------------ |
| analyze-secrets   | See [agents/analyze-secrets.md](agents/analyze-secrets.md)     | コードベース、サービス一覧 | 検出パターン仕様、リスク評価   |
| configure-hooks   | See [agents/configure-hooks.md](agents/configure-hooks.md)     | 検出パターン仕様           | 設定済みhook、展開計画         |
| validate-security | See [agents/validate-security.md](agents/validate-security.md) | 設定済みhook               | 検証レポート、履歴スキャン結果 |

### scripts/（自動化）

| スクリプト             | 用途                         | 使用例                                                              |
| ---------------------- | ---------------------------- | ------------------------------------------------------------------- |
| setup-git-security.mjs | Git Security自動セットアップ | `node scripts/setup-git-security.mjs`                               |
| validate-security.mjs  | Hook動作検証・検出精度テスト | `node scripts/validate-security.mjs --test-mode --verbose`          |
| scan-history.mjs       | Git履歴スキャン              | `node scripts/scan-history.mjs --verbose --report=leak-report.json` |
| log_usage.mjs          | 使用記録・自動評価           | `node scripts/log_usage.mjs --result success --phase "Phase 3"`     |

### assets/（テンプレート）

| テンプレート             | 用途                 | パス                                                                         |
| ------------------------ | -------------------- | ---------------------------------------------------------------------------- |
| Pre-commit Hook Template | カスタムhookの実装例 | See [assets/pre-commit-hook-template.sh](assets/pre-commit-hook-template.sh) |

## クイックスタート

### 1. ツールインストール

```bash
# git-secrets（AWS中心）
brew install git-secrets

# gitleaks（多様なサービス）
brew install gitleaks
```

### 2. 自動セットアップ

```bash
# セットアップスクリプト実行
node .claude/skills/pre-commit-security/scripts/setup-git-security.mjs
```

**含まれる処理**:

- git-secretsのインストール確認・初期化
- AWSパターン登録
- OpenAI/Anthropic/Discord/GitHub等のパターン追加
- ホワイトリスト設定
- Git履歴スキャン
- .gitignore検証

### 3. 手動セットアップ（カスタマイズ時）

**git-secretsの場合**:

```bash
# 初期化
cd your-repo
git secrets --install

# パターン追加
git secrets --register-aws
git secrets --add 'sk-proj-[a-zA-Z0-9]{48}'

# ホワイトリスト
git secrets --add --allowed 'example'
```

**gitleaksの場合**:

```bash
# .gitleaks.toml作成
cat > .gitleaks.toml <<'EOF'
title = "Gitleaks Configuration"

[[rules]]
id = "openai-api-key"
description = "OpenAI API Key"
regex = '''sk-proj-[a-zA-Z0-9]{48}'''
tags = ["api-key", "openai"]

[allowlist]
paths = [".env.example"]
regexes = ["example", "sample"]
EOF

# pre-commit hook設定
cat > .git/hooks/pre-commit <<'EOF'
#!/bin/sh
gitleaks protect --staged --verbose
EOF
chmod +x .git/hooks/pre-commit
```

### 4. テスト

```bash
# 検出テスト（ブロックされるべき）
# Replace the placeholder with a disposable local canary before running this test.
echo 'API_KEY="<DISPOSABLE_TEST_SECRET>"' > test.txt
git add test.txt
git commit -m "test"  # ❌ ブロックされる

# クリーンアップ
rm test.txt
git reset HEAD
```

### 5. チーム展開

**共有hookスクリプト（推奨）**:

```bash
# .githooks/ に配置
mkdir -p .githooks
cp .git/hooks/pre-commit .githooks/pre-commit
git add .githooks/pre-commit

# チームメンバーは設定のみ
git config core.hooksPath .githooks
```

**詳細**: See [references/deployment.md](references/deployment.md)

### 6. CI/CD統合

**GitHub Actions**:

```yaml
# .github/workflows/security.yml
name: Secret Scan
on: [push, pull_request]

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
```

**詳細**: See [references/ci-integration.md](references/ci-integration.md)

## トラブルシューティング

### よくある問題

| 問題                           | 原因                             | 対策                                                    |
| ------------------------------ | -------------------------------- | ------------------------------------------------------- |
| 誤検知が多い                   | ホワイトリスト不足               | `.env.example`、`tests/fixtures/`等を除外               |
| hookが動作しない               | 実行権限がない                   | `chmod +x .git/hooks/pre-commit`                        |
| チームメンバーが設定していない | セットアップ忘れ                 | CI/CDで必須チェック、セットアップスクリプト提供         |
| パフォーマンスが遅い           | 大規模リポジトリで全履歴スキャン | 差分のみスキャン（`gitleaks protect`）、CI/CDで並列実行 |
| `--no-verify`でバイパスされる  | ローカルhookのみ                 | CI/CDで必須チェック、pre-receive hook（サーバー側）     |

**詳細**: See [references/patterns.md](references/patterns.md#トラブルシューティング)、[references/deployment.md](references/deployment.md#トラブルシューティング)

## リーク発見時の対処

### Critical/Highリスクの場合

1. **即座にシークレットを無効化**

   ```bash
   # AWS例
   aws iam delete-access-key --access-key-id AKIA...
   ```

2. **影響範囲の調査**

   ```bash
   # コミット情報確認
   git log --all --grep="<leaked-secret>"
   ```

3. **Git履歴からの削除**（チーム調整後）

   ```bash
   # BFG Repo-Cleaner使用
   brew install bfg
   bfg --delete-files credentials.json your-repo.git
   git push --force
   ```

4. **インシデントレポート作成**
   - 漏洩したシークレットの種類
   - 漏洩期間（コミット日時）
   - 対応履歴（無効化、削除、影響調査）

**詳細**: See [agents/validate-security.md](agents/validate-security.md#4-リーク発見時の対応)

## 変更履歴

| Version | Date       | Changes                                                                          |
| ------- | ---------- | -------------------------------------------------------------------------------- |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠に移行、詳細知識をreferencesに外部化、agents/scripts追加 |
| 2.0.0   | 2026-01-02 | Task仕様書追加、検証スクリプト強化                                               |
| 1.0.0   | 2025-12-24 | 初版作成、基本構造とリソース整備                                                 |
