---
name: actions-debugger
description: GitHub Actions のワークフロー実行エラーを調査し、原因を特定して解決策を提案する。「Actions エラー」「ワークフロー失敗」「CI が落ちた」「ビルド失敗」「テスト失敗」「Actions を調べて」「CI のエラーを見て」などで起動。失敗したジョブのログを分析し、具体的な修正方法を提示。
allowed-tools: [Read, Bash, Grep, Glob]
context: fork
agent: debugger
---

# Actions Debugger

GitHub Actions のワークフロー実行エラーを調査し、原因を特定して解決策を提案します。

## ワークフロー

### 1. 失敗した Run の特定

```bash
# 最近の失敗した Run を一覧表示
gh run list --status failure --limit 5

# 特定の PR に関連する Run を確認
gh pr checks {pr番号}
```

### 2. エラーログの取得

```bash
# Run の詳細とジョブ一覧を取得
gh run view {run_id} --verbose

# 失敗したステップのログを取得
gh run view {run_id} --log-failed
```

### 3. エラー分析

ログから以下を特定:

- エラーメッセージ
- 失敗したステップ
- 関連するファイル・行番号

### 4. 解決策の提案

エラーパターンに基づいて:

- 具体的な修正コード
- 設定変更の提案
- 参考ドキュメントへのリンク

## よくあるエラーパターン

### テスト失敗

```bash
# テストログの詳細確認
gh run view {run_id} --log-failed | grep -A 10 "FAIL"
```

**対処法**:

- 失敗したテストケースを特定
- ローカルで再現
- テストまたはコードを修正

### ビルドエラー

```bash
# ビルドログの確認
gh run view {run_id} --log-failed | grep -A 5 "error"
```

**対処法**:

- コンパイルエラーを特定
- 型エラーや構文エラーを修正
- 依存関係を確認

### 依存関係エラー

```bash
# npm / yarn エラーの確認
gh run view {run_id} --log-failed | grep -A 5 "npm ERR!"
```

**対処法**:

- `package-lock.json` を更新
- 依存関係のバージョンを確認
- キャッシュをクリア

### 権限エラー

**対処法**:

- workflow の permissions を確認
- GITHUB_TOKEN の権限を確認
- secrets の設定を確認

## 出力形式

### エラーレポート

```
## GitHub Actions エラー調査結果

**Run ID**: {run_id}
**ワークフロー**: {workflow_name}
**ステータス**: ❌ failure

### 失敗したジョブ

| ジョブ | ステップ | 原因 |
|--------|----------|------|
| test | Run tests | テスト失敗 |

### エラー詳細

```
FAIL src/__tests__/user.test.ts
  ● UserService > should return user
    Expected: "John"
    Received: "Jane"
```

### 修正提案

1. `src/__tests__/user.test.ts` の期待値を確認
2. または `UserService` の実装を確認

### 参考コマンド

```bash
# ローカルでテスト実行
npm test -- --testPathPattern=user.test.ts
```
```

## 重要な注意事項

- ✅ エラーログを詳細に分析
- ✅ 具体的な修正提案を含める
- ✅ ローカルでの再現方法を提示
- ❌ 漠然とした提案を避ける
- ❌ 関係ないエラーを混同しない
