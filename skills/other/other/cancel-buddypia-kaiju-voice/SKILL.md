---
name: cancel
description: |
  プロジェクト プロジェクトの持続モード(persistent-mode, web-qa, turbo-mode)を安全に終了するスキル.
  State ファイルを削除してStop HookがAIをブロックしないようにします.

  "キャンセル", "中断", "cancel", "stop mode" 等のリクエストでトリガーされます.

  <example>
  user: "persistent mode キャンセルして"
  assistant: "cancel スキルを使用してpersistent modeを終了します"
  </example>

  <example>
  user: "/cancel"
  assistant: "全ての有効化されたモードを終了します"
  </example>

  <example>
  user: "/cancel --force"
  assistant: "強制的に全てのstateファイルを削除します"
  </example>
doc_contract:
  review_interval_days: 90
---

# Cancel Skill (モード終了)

> **核心機能**: persistent-mode, web-qa, turbo-modeの安全な終了

---

## 使用法

```bash
# 全ての有効モード終了
/cancel

# 強制終了 (確認なし)
/cancel --force

# 特定モードのみ終了
/cancel --mode persistent
/cancel --mode web-qa
/cancel --mode turbo
```

---

## 実行プロトコル

### Step 1: 現在の有効モード確認

```bash
# State ディレクトリ確認
ls -la .claude/state/
```

想定出力:

```
persistent-state.json   # persistent-mode 有効化時
web-qa-state.json   # web-qa 有効化時
turbo-state.json        # turbo-mode 有効化時
```

### Step 2: State ファイル + Plan ファイル削除

```bash
# 特定モード終了
# まずState ファイルのplan_file パスを確認
cat .claude/state/persistent-state.json
# completion.plan_file パスがあれば一緒に削除
# 例: completion.plan_file = ".tmp/plans/my-task.md"
rm .claude/state/persistent-state.json
rm .tmp/plans/my-task.md  # plan ファイルも削除 (ある場合)

# 全モード終了 (--force)
rm -f .claude/state/*-state.json
```

### Step 3: 終了確認

```markdown
## Cancel 完了

| モード          | 以前の状態 | 現在の状態 |
| --------------- | :--------: | :--------: |
| persistent-mode |    有効    |    無効    |
| web-qa          |    無効    |    無効    |
| turbo-mode      |    無効    |    無効    |

→ これでAIが正常に停止できます。
```

---

## State ファイル構造

### persistent-state.json

```json
{
  "active": true,
  "iteration": 5,
  "max_iterations": 50,
  "started_at": "2026-02-05T10:00:00+09:00",
  "last_checked_at": "2026-02-05T10:15:00+09:00",
  "prompt": "全てのテスト通過まで続行して",
  "error_history": ["npm run lint: 2 warnings", "npm test: 1 failed"]
}
```

### web-qa-state.json

```json
{
  "active": true,
  "cycle": 3,
  "max_cycles": 10,
  "started_at": "2026-02-05T10:00:00+09:00",
  "last_checked_at": "2026-02-05T10:10:00+09:00",
  "all_passing": false,
  "last_failure": "npm test: 2 tests failed"
}
```

### turbo-state.json

```json
{
  "active": true,
  "reinforcement_count": 5,
  "max_reinforcements": 30,
  "started_at": "2026-02-05T10:00:00+09:00",
  "last_checked_at": "2026-02-05T10:05:00+09:00"
}
```

---

## 注意事項

### 強制終了が必要な場合

| 状況               | 推奨対処                    |
| ------------------ | --------------------------- |
| AIが無限ループ     | `/cancel --force`           |
| State ファイル破損 | `/cancel --force`           |
| 誤ったモード有効化 | `/cancel --mode {モード名}` |

### 強制終了後のクリーンアップ

```bash
# State ディレクトリ確認
ls -la .claude/state/

# 空であるべき (または *-state.json なし)
```

---

## トラブルシューティング

### 1. Cancel 後もAIが停止しない

**原因**: State ファイルが完全に削除されていない

**解決**:

```bash
# 手動削除
rm -f .claude/state/*.json

# 確認
ls .claude/state/
```

### 2. "Permission denied" エラー

**原因**: ファイル権限の問題

**解決**:

```bash
chmod -R 755 .claude/state/
rm -f .claude/state/*-state.json
```

### 3. State ディレクトリがない

**原因**: モードが一度も有効化されていない

**解決**: 正常な状態。対処不要。

---

## 関連スキル

- [persistent-mode](../persistent-mode/SKILL.md): 完了保証モード
- [web-qa](../web-qa/SKILL.md): QA サイクルモード
- [turbo-mode](../turbo-mode/SKILL.md): 並列実行モード

---

## 変更履歴

| 日付       | バージョン | 変更内容                                                   |
| ---------- | ---------- | ---------------------------------------------------------- |
| 2026-02-05 | v1.0       | 新規作成 - cancel パターン適用            |
| 2026-02-07 | v1.1       | Plan ファイル cleanup 手順追加 (persistent-mode v5.0 連携) |
