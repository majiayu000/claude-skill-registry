---
name: local-ci
description: remote CI (GitHub Actions) 相当のチェックをローカルで実行。Biome check、テスト、ビルドを並列実行し、全てのチェックが成功したことを確認する。PR作成前の事前チェックに使用。
---

# Local CI スキル

**このスキルの役割**: remote CI (GitHub Actions) 相当のチェックを**ローカルマシン上**で実行するスキル。

## check-remote-ci コマンドとの違い

| スキル/コマンド | 実行場所 | 目的 | 使用場面 |
|---------------|---------|------|----------|
| **local-ci** (このスキル) | **local** | local CI チェック（remote CI 相当）をローカル実行 | PR作成前の事前チェック、TDD完了後の検証 |
| **check-remote-ci** | **remote** (GitHub Actions) | remote CI の実行状態確認と修正方針提案 | PR作成後、remote CI が失敗した際の原因調査 |

## 目的

プルリクエスト作成前に**ローカルマシン上**で実行することで、remote CI の失敗を事前に検出します。
`.github/workflows/ci.yml` と同じチェックを並列実行し、全ての問題を一度に検出します。

## 実行内容

以下の3つのチェックを**並列**実行します：

### 1. Biome Check
- **コマンド**: `npm run check`
- **目的**: コードスタイル、リント、フォーマットのチェック
- **失敗時の対応**: エラー内容を表示し、`npm run check:fix`で自動修正可能な旨を伝える

### 2. Test
- **コマンド**: `npm run test:run`
- **目的**: 全テストスイートの実行
- **失敗時の対応**: テストエラーを表示

### 3. Build
- **コマンド**: `npm run build`
- **目的**: TypeScriptコンパイル + Viteビルド
- **失敗時の対応**: 型エラーやビルドエラーを表示

**並列実行の利点**:
- 全ての失敗要因を一度に検出できる
- 複数の問題を同時に修正可能
- 再実行の回数を削減し、開発効率を向上

### remote CI (GitHub Actions) との違い

**含まれていないチェック**:
- **Security Audit** (`npm audit`, `secretlint`)
  - **除外理由**:
    - セキュリティチェックは依存関係の脆弱性を検出するため、コード変更のたびに実行する必要性は低い
    - 実行時間は通常30秒以内と高速だが、頻繁に実行する価値は低い
    - 脆弱性は依存関係のアップデート時に主に発生し、コード変更では影響を受けない
  - **remote CI (GitHub Actions) での実行**:
    - すべての PR で自動的に実行されます
    - security-audit ジョブとして独立して実行され、失敗時は PR マージがブロックされます
  - **ローカルでの手動実行**（必要に応じて）:
    ```bash
    npm audit --audit-level=moderate
    npm run secretlint
    ```

**設計方針**:
- **local-ci**: PR作成前の基本的な品質チェック（Biome、Test、Build）に焦点
- **remote CI (GitHub Actions)**: 包括的なチェック（セキュリティ、依存関係の更新など）を含む完全な検証

## 実装手順

### Step 1: local-ci-checker サブエージェントを起動

このスキルは **local-ci-checker サブエージェント**（`.claude/agents/local-ci-checker.md`）を呼び出して実行します。

```javascript
Task({
  "subagent_type": "local-ci-checker",
  "model": "haiku",
  "description": "Run local CI checks in parallel",
  "prompt": "local-ci スキルに従って、3つのサブエージェント（biome-check、test-check、build-check）を並列実行し、全てのチェックが成功することを確認してください。全ての結果をまとめて報告してください。"
})
```

### サブエージェント構造

local-ci-checker サブエージェントは、さらに**3つの専用サブエージェント**を並列起動します：

1. **biome-check** (`.claude/agents/biome-check.md`)
   - 役割: Biome check を実行
   - コマンド: `npm run check`
   - タイムアウト: 2分

2. **test-check** (`.claude/agents/test-check.md`)
   - 役割: テストを実行
   - コマンド: `npm run test:run`
   - タイムアウト: 5分

3. **build-check** (`.claude/agents/build-check.md`)
   - 役割: ビルドを実行
   - コマンド: `npm run build`
   - タイムアウト: 3分

**重要**: これらはBashコマンドを直接実行するのではなく、**個別のエージェント定義ファイル**として存在します。各エージェントは構造化されたJSON形式で結果を返します。

local-ci-checker サブエージェントの処理フロー：

1. **3つのサブエージェントを並列起動**: 単一メッセージで3つのTask呼び出し
2. **結果集計**: TaskOutputツールで各サブエージェントの出力を取得
3. **サマリー表示**: 全体の結果を整形して報告

### Step 2: サマリー表示

**全て成功した場合**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All local CI checks passed!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
  - Biome check: ✓
  - Tests: ✓ (X tests passed)
  - Build: ✓

🎉 Ready to create a pull request!
```

**1つ以上失敗した場合**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Local CI checks failed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
  - Biome check: {✓ or ✗}
  - Tests: {✓ or ✗}
  - Build: {✓ or ✗}

Failed checks:
  {失敗したチェックの詳細}

Fix the issues above and re-run the checks.
```

## エラーハンドリング

- 各チェックは並列実行されるため、すべてのチェックが完了するまで待つ
- 失敗したチェックがある場合、全ての失敗内容を一度に表示する
- Biome checkが失敗した場合は`npm run check:fix`で自動修正可能な旨を伝える
- 複数のチェックが失敗した場合、全ての修正方法をまとめて提示する

### 並列実行の再実行コスト

**部分的失敗時の修正フロー**:
1. 失敗したチェックのエラーを全て確認
2. 全ての問題を修正
3. `npm run check`、`npm run test:run`、`npm run build`を再度並列実行

**コスト比較**（典型的な実行時間）:
- **逐次実行（従来）**: Biome失敗 → 修正 → Biome実行（10秒）→ Test実行（2分）→ Build実行（1分） = 合計 3分10秒
- **並列実行（現在）**: 全て並列実行 = 最大2分（最も遅いTestの実行時間）

**メリット**: 再実行時も並列実行により、逐次実行より約1分10秒高速化されます。

## 実行例

### 成功例

```
🔍 Running local CI checks (in parallel)...

📋 Biome check
✅ Biome check passed

🧪 Running tests
✅ Tests passed (1,736 tests)

🏗️  Building project
✅ Build passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All local CI checks passed!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
  - Biome check: ✓
  - Tests: ✓ (1,736 tests passed)
  - Build: ✓

🎉 Ready to create a pull request!
```

### 失敗例（複数のチェックで失敗）

```
🔍 Running local CI checks (in parallel)...

📋 Biome check
✅ Biome check passed

🧪 Running tests
❌ Tests failed
[テストエラー出力]

🏗️  Building project
❌ Build failed
[ビルドエラー出力]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Local CI checks failed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
  - Biome check: ✓
  - Tests: ✗
  - Build: ✗

Failed checks:
  - Tests: {テストエラーの詳細}
  - Build: {ビルドエラーの詳細}

Fix the issues above and re-run the checks.
```

## 注意事項

- remote CI と完全に同じ環境ではないため、local CI で成功しても remote CI で失敗する可能性はある
- ただし、ほとんどの問題は事前に検出できる
- 実行時間は環境によって異なるが、通常3-5分程度
- `npm ci` は実行しない（依存関係は既にインストール済みと仮定）

## 使い方

```bash
/local-ci
```

このコマンドを実行すると、Claude が上記の手順を実行します（3つのチェックは並列実行されます）。

## 他のコマンドとの違い

詳細な比較は冒頭の表を参照してください。

- **`/local-ci`** (このスキル): local CI チェック（remote CI 相当）を**ローカルマシン上**で実行（Biome check、テスト、ビルド）
- **`/check-remote-ci`**: **remote CI (GitHub Actions)** の実行状態を確認して修正方針を提案
