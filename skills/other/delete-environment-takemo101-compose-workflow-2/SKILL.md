---
name: delete-environment
description: container-use環境（コンテナ、ファイル、メタデータ）を完全に削除する手順
---

# Environment Deletion (環境削除)

container-use環境（Dockerコンテナ、ファイルシステム、GitHub Issueラベル）を安全かつ完全に削除するためのワークフロー。

## 概要

環境削除は以下の3つのリソースをクリーンアップする必要があります：
1. **Docker Resources**: 実行中のコンテナ、ネットワーク、ボリューム
2. **Filesystem**: 作業ディレクトリ（Worktree または サブディレクトリ）
3. **GitHub Issue Labels**: `env:*`, `phase:*` ラベルを削除

---

## 削除フロー

### 1. 環境IDとパスの特定

削除対象の `env_id` とディレクトリパスを特定します。

```bash
# アクティブな環境一覧を確認
gh issue list --label "env:active" --json number,title

# 特定のIssueの詳細を取得（env_idはIssue bodyのメタデータから）
gh issue view <issue_number> --json body
```

### 2. コンテナの停止・削除

**ディレクトリが存在する場合**（推奨）:
Docker Composeを使用してリソースを適切に解放します。

```bash
# 作業ディレクトリへ移動
cd <env_dir>

# コンテナとボリュームの削除
docker compose down -v

# 親ディレクトリへ戻る
cd ..
```

**ディレクトリが既にない場合 / 強制削除**:
環境IDを含むコンテナを検索して強制削除します。

```bash
# env_id を含むコンテナを一括削除
docker rm -f $(docker ps -aq --filter "name=<env_id>")
```

### 3. ファイルシステムの削除

作業ディレクトリ（Worktreeまたはフォルダ）を削除します。

```bash
# Worktreeの場合
git worktree remove <env_dir> --force

# 通常ディレクトリの場合
rm -rf <env_dir>
```

### 4. GitHub Issue ラベルの更新

環境削除後、Issue のラベルを更新します（{{skill:github-issue-state-management}} API）。

```bash
# マージ完了として更新
bash .opencode/skill/github-issue-state-management/scripts/issue-state.sh merged <issue_number>
```

---

## 自動化スクリプト (推奨)

提供されているスクリプトを使用することで、上記の手順を一括で安全に実行できます。

```bash
bash .opencode/skill/delete-environment/scripts/delete_env.sh <env_id> [path_to_delete]
```

**使用例**:

```bash
# JSONとDockerコンテナのみ削除（ディレクトリ削除なし）
bash .opencode/skill/delete-environment/scripts/delete_env.sh abc-123

# ディレクトリも含めて完全削除
bash .opencode/skill/delete-environment/scripts/delete_env.sh abc-123 .worktrees/issue-123
```

### スクリプトの動作詳細
1. **Docker掃除**: `docker compose down -v` および ID名マッチによる強制削除
2. **ファイル掃除**: 指定された場合、Worktree解除または `rm -rf` を実行
3. **ラベル更新**: GitHub Issue のラベルを手動で更新

## エラー対応

- **`docker compose down` が失敗する**: ネットワークが使用中の場合があります。`docker network prune -f` を検討してください。
- **Issue ラベルが既にない**: 既に削除されているか、手動で削除された可能性があります。
