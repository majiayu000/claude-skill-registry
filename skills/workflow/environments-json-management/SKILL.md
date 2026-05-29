---
name: environments-json-management
description: container-use環境の状態管理のためのSingle Source of Truth（environments.json）の管理API、更新タイミング、復旧ロジックを定義
---

# environments.json 管理

> **Single Source of Truth**: container-use環境の状態管理

---

## 概要

**ALL container-use operations MUST update `environments.json` (project root)** to track Issue/PR/Environment relationships.

---

## ファイル構造

### パス

```
environments.json  # プロジェクトルート直下
```

### 初期化

ファイルが存在しない場合、以下の構造で作成：

```json
{
  "environments": []
}
```

### データ構造

```json
{
  "env_id": "abc-123-def",
  "branch": "feature/issue-42-user-auth",
  "issue_number": 42,
  "pr_number": null,
  "title": "User authentication feature",
  "status": "active",
  "phase": 4,
  "step": "tdd-green",
  "area": "backend",
  "blocked": null,
  "pending_issues": [],
  "created_at": "2026-01-03T10:00:00Z",
  "last_used_at": "2026-01-03T15:30:00Z"
}
```

### フィールド定義

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `env_id` | string | ✅ | container-use環境ID |
| `branch` | string | ✅ | Gitブランチ名 |
| `issue_number` | number | ✅ | GitHub Issue番号 |
| `pr_number` | number \| null | | PR番号（作成後） |
| `title` | string | ✅ | 作業内容の説明 |
| `status` | string | ✅ | 現在のステータス（下記参照） |
| `phase` | number | ✅ | **現在のPhase番号**（0-12） |
| `step` | string | ✅ | **Phase内の詳細ステップ** |
| `area` | string | | 実装領域（backend/frontend/infra等） |
| `blocked` | object \| null | | **Blocked状態の詳細**（下記参照） |
| `pending_issues` | array | | 未解決のレビュー指摘 |
| `created_at` | string | ✅ | 作成日時（ISO 8601） |
| `last_used_at` | string | ✅ | 最終使用日時（ISO 8601） |

### ステータス値

| ステータス | 説明 |
|-----------|------|
| `active` | 作業中 |
| `blocked` | **人間の介入が必要** |
| `pr_created` | PR作成済み |
| `merged` | PRマージ済み |
| `abandoned` | 放棄（PRクローズ等） |

### Phase & Step 定義（再開ポイント）

| Phase | Step | 説明 |
|-------|------|------|
| 0 | `branch-create` | ブランチ作成 |
| 1 | `env-create` | 環境構築 |
| 2 | `design-read` | 設計書参照 |
| 3 | `design-check` | 設計書実現性チェック |
| 4 | `tdd-red` | テスト作成（Red） |
| 5 | `tdd-green` | 実装（Green） |
| 6 | `tdd-refactor` | リファクタリング |
| 7 | `review-request` | レビュー依頼 |
| 8 | `review-fix` | レビュー指摘修正 |
| 9 | `stress-test` | **ストレステスト（任意）** |
| 10 | `approval-wait` | ユーザー承認待ち |
| 11 | `pr-create` | PR作成 |
| 12 | `ci-watch` | CI監視 |
| 13 | `merge-cleanup` | マージ & 環境削除 |
| 14 | `parent-close` | 親Issueクローズ |

### Blocked状態の構造

```json
{
  "blocked": {
    "reason": "design_ambiguity",
    "description": "設計書に矛盾あり。ユーザーIDの型がintかuuidか不明確",
    "blocked_at": "2026-01-03T14:00:00Z",
    "suggested_action": "バックエンド設計書の「ユーザーID」定義を統一してください",
    "context": {
      "ambiguous_points": ["ID型定義不一致", "必須フィールド欠落"]
    }
  }
}
```

| Blocked Reason | 説明 | 推奨アクション |
|----------------|------|---------------|
| `design_ambiguity` | **設計書実現性チェックNG** | 設計書修正 |
| `review_loop_exceeded` | レビュー3回失敗 | 設計書見直し |
| `dependency_missing` | 依存Subtask未完了 | 依存解決待ち |
| `external_blocker` | 外部要因（API未提供等） | 人間エスカレーション |
| `resource_limit` | 環境リソース不足 | Docker cleanup |
| `ci_persistent_failure` | CI 3回連続失敗 | 手動調査必要 |

---

## 必須更新ポイント (NON-NEGOTIABLE)

| トリガー | アクション | 更新フィールド |
|---------|----------|---------------|
| `environment_create` 成功 | **ADD** | `env_id`, `branch`, `issue_number`, `title`, `status: "active"`, `phase: 1`, `step: "env-create"`, `area`, `created_at`, `last_used_at` |
| Phase遷移時 | **UPDATE** | `phase`, `step`, `last_used_at` |
| `environment_open` 成功 | **UPDATE** | `last_used_at` |
| レビュー指摘発生 | **UPDATE** | `pending_issues` に追加 |
| レビュー指摘解決 | **UPDATE** | `pending_issues` から削除 |
| Blocked発生 | **UPDATE** | `status: "blocked"`, `blocked` オブジェクト設定 |
| Blocked解除 | **UPDATE** | `status: "active"`, `blocked: null` |
| `gh pr create` 成功 | **UPDATE** | `pr_number`, `status: "pr_created"`, `phase: 9`, `step: "pr-create"`, `last_used_at` |
| PR merged | **UPDATE** | `status: "merged"`, `phase: 11`, `step: "merge-cleanup"`, `last_used_at` |
| PR closed (マージなし) | **UPDATE** | `status: "abandoned"`, `last_used_at` |
| 環境削除 | **REMOVE** | エントリ全体を削除 |

---

## API

### 主要関数

| 関数 | 用途 |
|------|------|
| `register_environment(issue_id, env_id, branch)` | 環境作成時に登録 |
| `update_phase(env_id, phase, step)` | Phase/Step更新（再開ポイント記録） |
| `find_environment_by_issue(issue_id)` | Issue IDから環境を検索 |

### その他の関数（必要時のみ参照）

| 関数 | 用途 |
|------|------|
| `update_environment_pr(env_id, pr_number)` | PR作成時にPR番号を記録 |
| `mark_environment_merged(env_id)` | PRマージ後にステータス更新 |
| `remove_environment(env_id)` | 環境削除時にレコードを削除 |
| `set_blocked(env_id, reason, description, suggested_action)` | Blocked状態に設定 |
| `clear_blocked(env_id)` | Blocked状態を解除 |
| `add_pending_issue(env_id, issue)` | レビュー指摘を追加 |
| `clear_pending_issues(env_id)` | レビュー指摘をクリア |

### データ構造

```json
{
  "environments": [{
    "issue_number": 123,
    "env_id": "uuid",
    "branch": "feature/xxx",
    "status": "active|blocked|pr_created|merged|abandoned",
    "phase": 5,
    "step": "tdd-red",
    "created_at": "ISO8601",
    "last_used_at": "ISO8601",
    "pr_number": null,
    "blocked": null,
    "pending_issues": []
  }]
}
```

---

## 更新タイミング

| イベント | 関数 | 更新内容 |
|---------|------|---------|
| 環境作成時 | `register_environment()` | 新規登録 |
| Phase遷移時 | `update_phase()` | phase, step 更新 |
| Blocked発生 | `set_blocked()` | blocked状態設定 |
| Blocked解除 | `clear_blocked()` | blocked状態解除 |
| レビュー指摘発生 | `add_pending_issue()` | pending_issues に追加 |
| レビュー指摘解決 | `clear_pending_issues()` | pending_issues クリア |
| PR作成時 | `update_environment_pr()` | PR番号記録 |
| PRマージ後 | `mark_environment_merged()` | ステータス更新 |
| 環境削除時 | `remove_environment()` | レコード削除 |
| PR修正時 | `find_environment_by_issue()` | 既存環境を再利用 |

---

## セッション復旧

作業再開時、**environments.json を最優先で参照**：

```bash
# 1. Read environments.json (project root)
# 2. Find entry matching the Issue number or PR number
# 3. Use the stored env_id to reopen environment
```

### 復旧判定マトリクス

| Entry Status | PR State | Action |
|--------------|----------|--------|
| `active` | No PR | 作業継続、`phase`/`step` から再開 |
| `blocked` | N/A | **人間に通知**、blocked解除後に再開 |
| `pr_created` | PR open | 修正用に `env_id` で環境再開 |
| `pr_created` | PR merged | `status: "merged"` に更新、環境削除 |
| `merged` | N/A | クリーンアップ候補 |
| `abandoned` | N/A | 環境とエントリを即削除 |

### Phase-based 再開ロジック

```python
def resume_from_checkpoint(env_id: str) -> ResumeAction:
    """環境の現在Phase/Stepから再開アクションを決定"""
    env = find_environment_by_id(env_id)
    if not env:
        return ResumeAction(action="create_new")
    
    if env["status"] == "blocked":
        return ResumeAction(
            action="notify_human",
            message=f"Blocked: {env['blocked']['description']}",
            suggested_action=env["blocked"]["suggested_action"]
        )
    
    phase = env.get("phase", 0)
    step = env.get("step", "branch-create")
    
    # Phase別の再開ポイント
    RESUME_POINTS = {
        (0, "branch-create"): "create_branch",
        (1, "env-create"): "open_environment",
        (2, "design-read"): "read_design",
        (3, "design-check"): "check_design_feasibility",
        (4, "tdd-red"): "write_tests",
        (5, "tdd-green"): "implement",
        (6, "tdd-refactor"): "refactor",
        (7, "review-request"): "request_review",
        (8, "review-fix"): "fix_review_issues",
        (9, "stress-test"): "run_stress_tests",
        (10, "approval-wait"): "wait_approval",
        (11, "pr-create"): "create_pr",
        (12, "ci-watch"): "watch_ci",
        (13, "merge-cleanup"): "merge_and_cleanup",
        (14, "parent-close"): "close_parent_issue",
    }
    
    return ResumeAction(
        action=RESUME_POINTS.get((phase, step), "open_environment"),
        env_id=env_id,
        phase=phase,
        step=step,
        pending_issues=env.get("pending_issues", [])
    )
```

### Blocked状態の検出と通知

```python
def check_and_report_blocked() -> list[BlockedEnvironment]:
    """Blocked状態の環境を検出して報告"""
    data = load_environments()
    blocked = []
    
    for env in data["environments"]:
        if env.get("status") == "blocked":
            blocked.append(BlockedEnvironment(
                env_id=env["env_id"],
                issue_number=env["issue_number"],
                reason=env["blocked"]["reason"],
                description=env["blocked"]["description"],
                suggested_action=env["blocked"]["suggested_action"],
                blocked_at=env["blocked"]["blocked_at"]
            ))
    
    if blocked:
        print("⚠️ === BLOCKED ENVIRONMENTS ===")
        for b in blocked:
            print(f"  Issue #{b.issue_number}: {b.description}")
            print(f"    Reason: {b.reason}")
            print(f"    Suggested: {b.suggested_action}")
            print(f"    Blocked since: {b.blocked_at}")
        print("Blocked環境を確認し、問題解決後に clear_blocked() を呼び出してください。")
    
    return blocked
```

---

## クリーンアップポリシー

| 条件 | アクション |
|------|----------|
| `status: "merged"` から 7日以上 | 環境削除 + エントリ削除 |
| `status: "abandoned"` | 即時削除 |
| `last_used_at` から 30日以上 | レビューして削除検討 |

> **実行方法**: 環境削除には [delete-environment](../delete-environment/SKILL.md) スキルを使用してください（コンテナ・ファイル・JSONを一括削除）。

---

## ハードブロック (違反禁止)

| 違反 | 結果 |
|------|------|
| 環境作成時に environments.json 未登録 | **FORBIDDEN** - 復旧不可 |
| PR作成時に environments.json 未更新 | **FORBIDDEN** - 追跡不可 |
| 環境削除時に environments.json 未更新 | **FORBIDDEN** - stale data |

---

## 並列実行時のルール

| Actor | 責任 |
|-------|------|
| `container-worker` | `env_id` を最終レスポンスで返却。environments.json は**更新しない** |
| Main agent (Sisyphus) | 全worker完了後に environments.json を一括更新 |

> **理由**: 並列書き込みによる競合を回避

---

## 変数命名規則

| Context | Variable Name | Rationale |
|---------|---------------|-----------|
| **environments.json** (data) | `issue_number` | JSON field name (GitHub API準拠) |
| **Code/Pseudocode** | `issue_id` | 一般的な変数名規約 |

```python
# Writing
entry = {"issue_number": issue_id, ...}

# Reading
issue_id = entry["issue_number"]
```

---

## CLIスクリプト

**environments.json管理の自動化スクリプト：**

```bash
bash .opencode/skill/environments-json-management/scripts/env-json.sh <command> [args...]
```

| コマンド | 説明 | 使用例 |
|----------|------|--------|
| `add` | 新規環境を登録 | `env-json.sh add abc-123 42 feature/auth "User auth"` |
| `update-pr` | PR番号を記録 | `env-json.sh update-pr abc-123 45` |
| `mark-merged` | ステータスをmergedに更新 | `env-json.sh mark-merged abc-123` |
| `remove` | エントリを削除 | `env-json.sh remove abc-123` |
| `find-by-issue` | Issue番号で環境を検索 | `env-json.sh find-by-issue 42` |
| `list` | 全環境を一覧表示 | `env-json.sh list` |

**使用例：**
```bash
bash .opencode/skill/environments-json-management/scripts/env-json.sh add abc-123 42 feature/auth "User authentication"
bash .opencode/skill/environments-json-management/scripts/env-json.sh list
```
