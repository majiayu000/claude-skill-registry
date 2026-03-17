---
name: persistent-mode
description: |
  プロジェクト プロジェクトの **強制持続モード**.
  ralph パターンを Web プロジェクトに合わせて適用.

  **核心メカニズム**: Stop Hook + State ファイル基盤の強制反復
  - AIが停止しようとした時にStop Hookがstop-handler.mjsを実行
  - State ファイルがactive=trueならAIが強制的に継続
  - /cancelでState ファイルを削除しないと終了不可

  "最後まで", "完了まで", "止めないで", "persistent", "ralph" 等のリクエストでトリガーされる.

  <example>
  user: "最後までこの機能を完成させて"
  assistant: "persistent-modeを有効化します。完了まで停止しません。"
  </example>

  <example>
  user: "テストが通るまで止めないで"
  assistant: "persistent-modeを開始します。全てのテストが通過するまで続行します。"
  </example>
doc_contract:
  review_interval_days: 30
---

# Persistent Mode v5.0 (強制持続モード)

> **核心コンセプト**: Stop Hook + State ファイル基盤の **技術的強制**
>
> ralph パターンを Web プロジェクトに合わせてポーティング。
> ドキュメントで「繰り返せ」と書くだけではなく、**実際にAIを強制**します。

---

## 強制メカニズム (How It Works)

### アーキテクチャ

```
AIが応答を完了しようとする
         ↓
Stop Hook 発動
         ↓
stop-handler.mjs 実行
         ↓
.claude/state/persistent-state.json チェック
         ↓
┌─────────────────────────────────────┐
│ active=true?                        │
│   ├─ Yes → { decision: 'block' }    │
│   │         AIが強制的に継続        │
│   │                                 │
│   └─ No  → { continue: true }       │
│            正常終了を許可           │
└─────────────────────────────────────┘
```

### 核心ファイル

| ファイル                              | 役割                        |
| ------------------------------------- | --------------------------- |
| `.claude/scripts/stop-handler.mjs`    | Stop Hook ハンドラー (統合) |
| `.claude/state/persistent-state.json` | モード状態保存              |
| `.claude/settings.json`               | Stop Hook 登録              |

---

## 使用法

### 1. モード有効化 (State ファイル生成)

**自然言語での呼び出し** (推奨):

```
"最後までこの機能を完成させて"
"テストが通るまで止めないで"
"完了まで進めて"
```

**明示的呼び出し**:

```
/persistent-mode
/persistent-mode --max-iterations 30
/persistent-mode --plan .tmp/plans/my-task.md
/persistent-mode --plan .tmp/plans/my-task.md --max-iterations 30
```

**有効化時にAIがすべきこと**:

```bash
# State ファイル生成 (基本モード)
mkdir -p .claude/state

cat > .claude/state/persistent-state.json << 'EOF'
{
  "active": true,
  "iteration": 1,
  "max_iterations": 50,
  "started_at": "2026-02-05T10:00:00+09:00",
  "last_checked_at": "2026-02-05T10:00:00+09:00",
  "prompt": "[元の作業リクエスト]",
  "error_history": []
}
EOF
```

```bash
# State ファイル生成 (--plan モード)
mkdir -p .claude/state

cat > .claude/state/persistent-state.json << 'EOF'
{
  "active": true,
  "iteration": 1,
  "max_iterations": 50,
  "started_at": "2026-02-05T10:00:00+09:00",
  "last_checked_at": "2026-02-05T10:00:00+09:00",
  "prompt": "[元の作業リクエスト]",
  "error_history": [],
  "completion": {
    "type": "plan",
    "plan_file": ".tmp/plans/my-task.md"
  }
}
EOF
```

### Plan 基盤の自動完了 (v5.0)

**動作フロー**:

1. AIがState ファイルを生成 (`completion.type: "plan"` を含む)
2. AIが計画ファイルを生成 (マークダウンチェックボックス)
3. 作業を進めながら完了項目を `- [x]` でチェック
4. Stop Hookが毎回の反復でチェックボックスの状態を確認
5. **全て完了 → 自動終了** (State + 計画ファイル削除)

**計画ファイルの例**:

```markdown
# 作業計画: SPEC 文書分析

## チェックリスト

- [ ] SPEC-006 読み込みおよび分析
- [ ] SPEC-007 読み込みおよび分析
- [ ] SPEC-008 読み込みおよび分析
- [ ] 最終要約文書作成
```

**進捗表示**:

```
[PERSISTENT MODE - 5/20] 進捗率: 2/4 (50%)

未完了項目:
  - [ ] SPEC-008 読み込みおよび分析
  - [ ] 最終要約文書作成

全ての項目完了時に自動で終了します。
```

**終了条件の比較**:

| モード          | 完了条件                     | /cancel 必要 |
| --------------- | ---------------------------- | :----------: |
| `--plan` 使用   | 全てのチェックボックス `[x]` |   自動終了   |
| `--plan` 未使用 | ユーザー判断                 |     必須     |

### 2. 作業実行

State ファイルが存在すれば、AIが停止しようとするたびにStop Hookが強制的に継続させます。

```markdown
[PERSISTENT MODE - 1/50]

## 現在の作業

FR-02901: 単語帳リスト画面の実装

## 実行中

- VocabularyListPage 実装...
```

### 3. 検証失敗時の自動リトライ

```markdown
[PERSISTENT MODE - 2/50]

## 前回の失敗

- npm run lint: 2個 warning (unused import)

## 修正作業

- src/features/vocabulary/components/ListPage.tsx:3
  - 未使用 import 削除

## 再検証中...
```

### 4. モード終了 (/cancel)

作業完了後、必ず `/cancel` で終了:

```bash
# State ファイル削除
rm .claude/state/persistent-state.json
```

```markdown
## Persistent Mode 終了

State ファイル削除完了
これでAIが正常に停止できます
```

---

## State ファイル構造

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

| フィールド        | 説明                                |
| ----------------- | ----------------------------------- |
| `active`          | モード有効化状態 (true/false)       |
| `iteration`       | 現在の反復回数                      |
| `max_iterations`  | 最大反復回数 (デフォルト 50)        |
| `started_at`      | モード開始時刻                      |
| `last_checked_at` | 最終チェック時刻 (Staleness判定用)  |
| `prompt`          | 元の作業リクエスト                  |
| `error_history`   | 直近のエラー一覧 (同一エラー検知用) |

---

## 終了条件

### 成功終了

1. 全ての検証通過:
   - `npm run lint`: Exit 0, エラー 0個
   - `npm test`: 全テスト通過
   - Task システム: pending/in_progress 0個

2. `/cancel` 実行でState ファイル削除

```markdown
[PERSISTENT MODE - 完了]

## 最終検証結果

| 項目            |     状態     |
| --------------- | :----------: |
| npm run lint    |   0 issues   |
| npm test        | 47/47 passed |
| Tasks           |  0 pending   |

→ 全ての検証通過!
→ 反復回数: 3回
```

### 失敗終了

| 条件                            | 処理                        |
| ------------------------------- | --------------------------- |
| **最大反復到達** (50回)         | 中断 + 根本原因分析要求     |
| **同一エラー3回反復**           | 早期中断 + 構造的問題警告   |
| **Staleness 超過** (2時間)      | 自動無効化                  |
| **ユーザーキャンセル** (Ctrl+C) | 即時中断許可                |
| **Context Limit**               | 即時中断許可 (Compact 必要) |

```markdown
[PERSISTENT MODE - 中断]

## 同一エラー3回反復

エラー: npm test - VocabularyViewModel テスト失敗
原因: MockSupabase 設定の問題と推定

## 推奨対処

1. MockSupabase 設定を手動で検証
2. テスト環境の依存関係確認
3. /cancelでモード終了後、手動解決
```

---

## 設定オプション

### デフォルト設定

```json
{
  "max_iterations": 50,
  "staleness_hours": 2,
  "same_error_limit": 3
}
```

### カスタム設定

```bash
# 最大反復回数変更
/persistent-mode --max-iterations 100

# 高速失敗モード (同一エラー2回で中断)
/persistent-mode --same-error-limit 2
```

---

## 連携スキル

### web-qaとの組み合わせ

```bash
# QA サイクル + 完了保証
/web-qa --persistent
```

→ web-qaのQAサイクルをpersistent-modeで強制

### turbo-modeとの組み合わせ

```bash
# 並列実行 + 完了保証
/turbo-mode --persistent
```

→ 並列作業が全て完了するまで強制

---

## トラブルシューティング

### 1. モードが終了しない

**原因**: State ファイルが残っている

**解決**:

```bash
# 手動削除
rm .claude/state/persistent-state.json

# または強制 cancel
/cancel --force
```

### 2. Stop Hookが動作しない

**原因**: settings.jsonにHookが登録されていない

**確認**:

```bash
cat .claude/settings.json | grep stop-handler
```

**解決**: Hookを再登録

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node \"$CLAUDE_PROJECT_DIR\"/.claude/scripts/stop-handler.mjs",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

### 3. Stalenessにより自動無効化された

**原因**: 2時間以上応答なし

**解決**: モードを再有効化

```bash
/persistent-mode
```

---

## 既存バージョンとの比較

| 項目               | v3.0 (ドキュメント基盤) | v4.0 (スクリプト強制) | v5.0 (Plan自動完了)  |
| ------------------ | :---------------------: | :-------------------: | :------------------: |
| 強制性             |         AI裁量          |      技術的強制       |      技術的強制      |
| 反復保証           |      従う場合あり       |      無条件反復       |      無条件反復      |
| 終了方法           |      AIが自動判断       |     /cancel 必須      |     自動終了可能     |
| Staleness チェック |          なし           |         2時間         |        2時間         |
| 同一エラー検知     |          なし           |        3回検知        |       3回検知        |
| 進捗表示           |          なし           |         なし          | チェックボックス基盤 |

---

## 参照文書

- [stop-handler.mjs (統合 Stop Hook ハンドラー)](../../scripts/stop-handler.mjs)
- [cancel SKILL.md](../cancel/SKILL.md)
- [web-qa SKILL.md](../web-qa/SKILL.md)
- [turbo-mode SKILL.md](../turbo-mode/SKILL.md)

---

## 変更履歴

| 日付       | バージョン | 変更内容                                               |
| ---------- | ---------- | ------------------------------------------------------ |
| 2026-02-01 | v1.0       | 新規作成 - ralph パターンのドキュメント基盤            |
| 2026-02-01 | v3.0       | Enforced Skill Pattern 適用                            |
| 2026-02-05 | v4.0       | **Stop Hook + State ファイル基盤の強制メカニズム実装** |
| 2026-02-07 | v5.0       | **Plan基盤の自動完了検知追加** (`--plan` オプション)   |
