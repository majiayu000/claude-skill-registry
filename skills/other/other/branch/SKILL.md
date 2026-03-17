---
name: branch
description: ブランチ作成Skill。仕様策定用（spec/*）または実装用（impl/*）のブランチを作成。/spec や spec-workflow から呼び出される。
---

# /branch Skill - ブランチ作成

SDDワークフローにおけるブランチ作成を担当するSkill。
仕様策定・実装それぞれのフェーズで適切なブランチを作成します。

## 発動条件

- `/branch` コマンドで明示的に呼び出し
- `/spec` Skill から自動呼び出し（仕様策定開始時）
- `spec-workflow` Skill から自動呼び出し（実装開始時）

## ブランチ命名規則

### 仕様策定用

```
spec/{action-id}-{short-description}
```

例: `spec/001-01-01-user-auth`

### 実装用

```
impl/{action-id}-{short-description}
```

例: `impl/001-01-01-user-auth`

## ワークフロー

```
┌─────────────────────────────────────────────────┐
│  1. コンテキスト確認                            │
│     - 呼び出し元を判定（spec or impl）          │
│     - アクションIDを取得                        │
│                                                 │
│  2. ブランチ名生成                              │
│     - 命名規則に従って生成                      │
│     - 重複チェック                              │
│                                                 │
│  3. ユーザー確認                                │
│     「ブランチ '{name}' を作成しますか？」      │
│                                                 │
│  4. ブランチ作成                                │
│     git checkout -b {branch-name}               │
│                                                 │
│  5. 完了通知                                    │
│     「ブランチ '{name}' を作成しました」        │
└─────────────────────────────────────────────────┘
```

## パラメータ

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| type | Yes | ブランチタイプ | `spec` or `impl` |
| action-id | Yes | アクションID | `001-01-01` |
| description | No | 短い説明（省略時は自動生成） | `user-auth` |

## 使用例

### 直接呼び出し

```
ユーザー: /branch spec 001-01-01 user-auth

Claude: ブランチ 'spec/001-01-01-user-auth' を作成しますか？
        ベースブランチ: main

ユーザー: OK

Claude: ✅ ブランチ 'spec/001-01-01-user-auth' を作成しました
        現在のブランチ: spec/001-01-01-user-auth
```

### /spec からの自動呼び出し

```
[/spec Skill 内部]
→ ファイル生成前に /branch を発火
→ type: spec, action-id: 生成するアクションID
```

### spec-workflow からの自動呼び出し

```
[spec-workflow Skill 内部]
→ 実装開始前に /branch を発火
→ type: impl, action-id: 実装するアクションID
```

## 実行コマンド

```bash
# 現在のブランチを確認
git branch --show-current

# mainブランチが最新か確認
git fetch origin main

# ブランチ作成
git checkout -b {branch-name}

# 作成確認
git branch --show-current
```

## エラーハンドリング

### ブランチ名が既に存在する場合

```
Claude: ブランチ 'spec/001-01-01-user-auth' は既に存在します。

対応案:
1. 既存ブランチに切り替える
2. 別の名前で作成する（例: spec/001-01-01-user-auth-v2）
3. 既存ブランチを削除して新規作成

どれを選択しますか？
```

### 未コミットの変更がある場合

```
Claude: 未コミットの変更があります。

対応案:
1. 変更をスタッシュしてブランチ作成
2. 変更をコミットしてからブランチ作成
3. 変更を破棄してブランチ作成（非推奨）

どれを選択しますか？
```

## 禁止事項

- ユーザー確認なしのブランチ作成
- 命名規則に従わないブランチ名
- mainブランチへの直接コミット誘導
