---
name: copilot-review
description: GitHub Copilot PRレビュー対応ワークフロー（コメント取得→修正→返信→解決）
version: 1.0.0
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
skill_type: workflow
auto_invoke: false
---

# Copilot PRレビュー対応ワークフロー

## 概要

GitHub Copilot によるPRレビューコメントへの対応を効率化します。レビューコメントの取得から修正、返信、スレッド解決までを自動化し、PRレビュー対応時間を15分→3分に短縮（80%削減）します。

**重要**: ブランチ保護ルールにより、全てのコメントを解決しないとマージできません。

## 入力形式

スキル呼び出し時にPR番号を指定してください:

```
/copilot-review <PR番号>
```

または

```
/copilot-review

PR番号: <番号>
```

## 実行プロセス

### ステップ1: レビューコメント取得

GitHub APIを使用してPRのレビューコメントを取得します。

**コマンド**:
```bash
gh api repos/foie0222/baken-kaigi/pulls/<PR番号>/comments \
  --jq '.[] | {id, path, line, body, user: .user.login}'
```

**出力例**:
```json
{
  "id": 123456789,
  "path": "backend/src/domain/ports/race_data_provider.py",
  "line": 25,
  "body": "Consider adding type hints for the return value",
  "user": "copilot"
}
```

**判断基準**:
- Copilotによるコメント（`user: "copilot"`）のみを対象
- 人間のレビュアーコメントは別途確認を促す

### ステップ2: コメント内容の分析と優先度付け

レビューコメントを以下のカテゴリーに分類:

1. **Critical（即座に対応）**:
   - セキュリティ脆弱性
   - バグの可能性
   - テスト不足

2. **High（優先対応）**:
   - 型ヒント不足
   - エラーハンドリング不足
   - コード品質問題

3. **Medium（推奨対応）**:
   - 命名規則
   - コメント不足
   - リファクタリング提案

4. **Low（任意対応）**:
   - コードスタイル
   - 軽微な改善提案

### ステップ3: 対応方針の提案

各コメントに対して以下のいずれかを提案:

1. **修正する**: コメントの指摘を受け入れて修正
2. **説明を返信**: 現状の実装理由を説明し、修正不要と判断
3. **代替案を提示**: 別のアプローチを提案

#### 優先度別の対応方針（必須）

| 優先度 | 許可される対応 | 禁止される対応 |
|--------|---------------|---------------|
| Critical | 修正のみ | 説明返信、延期、スキップ |
| High | 修正、または技術的根拠のある説明返信 | 延期、スキップ |
| Medium | 修正、説明返信 | なし |
| Low | 修正、説明返信、スキップ | なし |

**Critical指摘の例と必須対応**:
- テスト不足 → **テストを書く**（延期禁止）
- セキュリティ脆弱性 → **修正する**（延期禁止）
- バグの可能性 → **修正する**（延期禁止）

**High指摘の例と対応**:
- エラーハンドリング不足 → **修正する**（原則として対応推奨）
- 型ヒント不足 → **修正する**、または技術的根拠のある説明返信

**重要**: Critical指摘に対して「説明返信」で済ませることは**絶対に禁止**。必ずコードを修正すること。

**提案フォーマット**:
```
📝 レビューコメント #1 [Critical]
ファイル: backend/src/domain/ports/race_data_provider.py:25
指摘: Consider adding type hints for the return value

提案: 修正する
理由: 型ヒントはコードの可読性と保守性を向上させる
修正内容: 戻り値の型ヒントを追加
```

### ステップ4: 修正実施

ユーザーの承認後、Editツールを使用して修正を実施します。

**修正パターン**:

#### パターン1: 型ヒント追加
```python
# Before
def get_race(self, race_id):
    pass

# After
def get_race(self, race_id: RaceId) -> RaceData | None:
    pass
```

#### パターン2: エラーハンドリング追加
```python
# Before
data = response.json()
return data["value"]

# After
try:
    data = response.json()
    return data.get("value")
except (KeyError, ValueError) as e:
    logger.error(f"Failed to parse response: {e}")
    return None
```

#### パターン3: テスト追加
```python
def test_get_race_not_found():
    """存在しないレースIDの場合Noneを返す."""
    # Arrange
    provider = MockRaceDataProvider()
    race_id = RaceId("invalid_id")

    # Act
    result = provider.get_race(race_id)

    # Assert
    assert result is None
```

### ステップ5: コミット・プッシュ

修正をコミットしてプッシュします。

**コマンド**:
```bash
git add <修正ファイル>
git commit -m "fix: Copilotレビュー指摘対応 - <概要>"
git push
```

**コミットメッセージ例**:
- `fix: Copilotレビュー指摘対応 - 型ヒント追加`
- `fix: Copilotレビュー指摘対応 - エラーハンドリング改善`
- `test: Copilotレビュー指摘対応 - テストケース追加`

### ステップ6: コメントに返信

修正内容または説明をコメントに返信します。

**コマンド**:
```bash
gh api repos/foie0222/baken-kaigi/pulls/<PR番号>/comments/<コメントID>/replies \
  -X POST \
  -f body='<返信内容>'
```

**返信テンプレート**:

#### 修正した場合:
```
✅ 修正しました。

変更内容:
- <変更1>
- <変更2>

コミット: <コミットハッシュ>
```

#### 説明で対応する場合:
```
📝 現在の実装理由

<理由の説明>

そのため、この指摘については現状維持とさせていただきます。
```

### ステップ7: スレッド解決

修正完了後、レビュースレッドを解決します。

**ステップ7-1: スレッドID取得**

```bash
gh api graphql -f query='
query {
  repository(owner: "foie0222", name: "baken-kaigi") {
    pullRequest(number: <PR番号>) {
      reviewThreads(first: 20) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              databaseId
              body
            }
          }
        }
      }
    }
  }
}'
```

**ステップ7-2: スレッド解決**

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "<スレッドID>"}) {
    thread {
      isResolved
    }
  }
}'
```

### ステップ8: 対応完了確認

全てのコメントに対応したことを確認します。

**確認コマンド**:
```bash
# 未解決のスレッド数を確認
gh api graphql -f query='
query {
  repository(owner: "foie0222", name: "baken-kaigi") {
    pullRequest(number: <PR番号>) {
      reviewThreads(first: 20) {
        nodes {
          isResolved
        }
      }
    }
  }
}' --jq '.data.repository.pullRequest.reviewThreads.nodes | map(select(.isResolved == false)) | length'
```

**期待値**: `0`（全スレッド解決済み）

## 出力形式

```
📊 Copilot レビュー対応サマリー

PR番号: #<番号>
レビューコメント総数: <件数>

対応状況:
✅ 修正済み: <件数>
📝 説明返信: <件数>
⏭️  スキップ: <件数>

詳細:
---
📝 コメント #1 [Critical]
ファイル: backend/src/domain/ports/race_data_provider.py:25
指摘: Consider adding type hints for the return value
対応: ✅ 修正済み
返信: "型ヒントを追加しました。"
---

次のアクション:
- [ ] 全スレッド解決確認（gh api graphqlで確認）
- [ ] CI/CD成功確認
- [ ] マージ実行
```

## エラーハンドリング

### 頻出エラーと対処法

1. **GraphQL API認証エラー**
   ```
   Error: HTTP 401: Unauthorized
   ```
   - 対処: `gh auth login` で再認証

2. **スレッドIDが見つからない**
   ```
   Error: Invalid thread ID
   ```
   - 対処: GraphQLクエリで最新のスレッドIDを再取得

3. **コメント返信に失敗**
   ```
   Error: Resource not accessible by integration
   ```
   - 対処: `gh` CLI の権限スコープを確認（`repo` スコープが必要）

4. **マージブロック**
   ```
   Error: Required reviews not satisfied
   ```
   - 対処: 全スレッドが解決されているか確認

## 命名規則/パターン

### コミットメッセージ

- `fix: Copilotレビュー指摘対応 - <具体的な修正内容>`
- 複数ファイル修正の場合は概要を記載

### 返信メッセージ

- 簡潔に（3行以内）
- 絵文字で状態を明示（✅, 📝, ⚠️）
- コミットハッシュを含める

## 使用例

### 例1: 型ヒント不足の指摘に対応

```
/copilot-review 42

📊 Copilot レビュー対応サマリー

PR番号: #42
レビューコメント総数: 3件

対応状況:
✅ 修正済み: 2件
📝 説明返信: 1件

詳細:
---
📝 コメント #1 [High]
ファイル: backend/src/domain/ports/race_data_provider.py:25
指摘: Consider adding type hints for the return value
対応: ✅ 修正済み
返信: "戻り値の型ヒントを追加しました。"
コミット: abc1234
---
📝 コメント #2 [Medium]
ファイル: backend/src/api/handlers/races.py:50
指摘: Consider extracting this to a separate function
対応: 📝 説明返信
返信: "現状のロジックは十分シンプルであり、抽出するとかえって複雑になると判断しました。"
---

次のアクション:
- [x] 全スレッド解決確認
- [ ] CI/CD成功確認
- [ ] マージ実行
```

### 例2: セキュリティ指摘への対応

```
/copilot-review 45

📊 Copilot レビュー対応サマリー

PR番号: #45
レビューコメント総数: 1件

対応状況:
✅ 修正済み: 1件

詳細:
---
📝 コメント #1 [Critical]
ファイル: backend/src/api/handlers/races.py:30
指摘: Potential SQL injection vulnerability
対応: ✅ 修正済み
返信: "パラメータ化クエリに変更し、SQLインジェクションを防止しました。"
コミット: def5678
---

次のアクション:
- [x] 全スレッド解決確認
- [x] CI/CD成功確認
- [ ] マージ実行
```

## 参照コマンド

### GitHub CLI (gh) コマンド一覧

```bash
# PR一覧表示
gh pr list

# PR詳細表示
gh pr view <PR番号>

# レビューコメント取得
gh api repos/foie0222/baken-kaigi/pulls/<PR番号>/comments

# コメントに返信
gh api repos/foie0222/baken-kaigi/pulls/<PR番号>/comments/<コメントID>/replies \
  -X POST -f body='返信内容'

# スレッド情報取得
gh api graphql -f query='...'

# スレッド解決
gh api graphql -f query='mutation { resolveReviewThread(...) }'
```

### GraphQL クエリテンプレート

#### 未解決スレッド一覧取得
```graphql
query {
  repository(owner: "foie0222", name: "baken-kaigi") {
    pullRequest(number: <PR番号>) {
      reviewThreads(first: 20) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              body
              path
            }
          }
        }
      }
    }
  }
}
```

#### スレッド解決
```graphql
mutation {
  resolveReviewThread(input: {threadId: "<スレッドID>"}) {
    thread {
      isResolved
    }
  }
}
```

## 注意事項

- **ブランチ保護**: 全コメント解決しないとマージ不可
- **CI/CD**: レビュー対応後も必ずCI/CDの成功を確認
- **人間レビュー**: Copilot以外のレビューコメントは別途対応
- **過剰な修正**: 指摘が不適切な場合は説明返信で対応（盲目的に修正しない）
- **git worktree**: 作業は feature ブランチで実施

## 絶対ルール

**コメントが来たら真摯に対応し、対応完了後に返信してクローズ。**

順序を厳守:

1. コメント内容を確認
2. コード修正（必要な場合）
3. コミット・プッシュ
4. **対応完了後に**返信（何をしたか具体的に記載）
5. スレッド解決
6. マージ

先に返信してから修正するのは禁止。修正してから返信。

## 禁止される返信パターン

以下の返信は**絶対に禁止**：

- 「別のPRで対応します」
- 「後で対応します」
- 「今回のスコープ外です」
- 「別途対応します」
- 「次のイテレーションで対応」
- 「それは別で対応します」
- 「今回は対応しません」
- 「時間の都合で対応できません」

**理由**: これらは技術的負債の先送りであり、PRの品質基準を満たさない。
Critical/High指摘に対してこれらの返信をした場合、PRはマージ不可。

**特に「テスト不足」の指摘に対して**:
- ❌ 「テストは別PRで追加します」→ 禁止
- ❌ 「時間がないのでテストはスキップします」→ 禁止
- ✅ テストコードを書いてコミットする → 正しい対応

## 対応完了の定義

コメントが「対応完了」となる条件：

1. **修正した場合**: コード変更がコミット・プッシュされ、指摘が解消されている
2. **説明返信の場合**（Medium/Low指摘のみ）: 技術的根拠を示し、レビュアーが納得できる説明

**Critical指摘は修正以外の対応は認められない。High指摘は修正、または技術的根拠のある説明返信が必要。**

### 対応完了チェックリスト

Critical指摘の場合:
- [ ] コードを修正した
- [ ] テストを追加/修正した（テスト不足指摘の場合）
- [ ] コミット・プッシュした
- [ ] 返信に具体的な修正内容を記載した

High指摘の場合:
- [ ] コードを修正した、または
- [ ] 技術的根拠のある説明を記載した（「別で対応」は不可）

Medium/Low指摘の場合:
- [ ] 修正、または説明返信で対応した
