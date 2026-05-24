---
name: issue-to-task
description: GitHub Issue→実装タスク生成（Issue分析→タスク分解→チェックリスト作成）
version: 1.0.0
tools:
  - Bash
  - Read
  - Grep
skill_type: workflow
auto_invoke: false
---

# Issue→実装タスク生成

## 概要

GitHub Issueの内容から実装タスクリストとチェックリストを自動生成します。Issue分析→タスク分解の時間短縮と実装漏れ防止を目的とします。

## 入力形式

スキル呼び出し時にIssue番号を指定:

```
/issue-to-task <Issue番号>
```

または

```
/issue-to-task

Issue: #<番号>
```

## 実行プロセス

### ステップ1: Issue情報取得

**コマンド**:
```bash
gh issue view <Issue番号> --json title,body,labels,assignees
```

**取得情報**:
- タイトル
- 本文
- ラベル
- アサイニー

**出力例**:
```json
{
  "title": "日付セレクターを動的な開催日一覧に変更",
  "body": "現状の日付選択UIを、実際に開催があった日付のみを表示する形式に変更する。\n\n## 背景\n...",
  "labels": ["enhancement", "frontend"],
  "assignees": []
}
```

### ステップ2: Issue分析

#### 分類

**Issue種別判定**:
1. **Feature（新機能）**: `feat:` で始まる、`enhancement` ラベル
2. **Bug（バグ修正）**: `fix:` で始まる、`bug` ラベル
3. **Refactor（リファクタリング）**: `refactor:` で始まる
4. **Docs（ドキュメント）**: `docs:` で始まる
5. **Test（テスト追加）**: `test:` で始まる

#### 影響範囲の特定

**ラベルから判定**:
- `frontend` → フロントエンド実装が必要
- `backend` → バックエンド実装が必要
- `api` → API拡張が必要
- `infra` → インフラ変更が必要
- `database` → DB変更が必要

### ステップ3: タスク分解

#### タスク抽出パターン

**Feature（新機能）の場合**:
1. **設計**
   - データモデル設計（必要に応じて）
   - UI/UX設計（フロントエンド）
   - API設計（バックエンド）

2. **実装**
   - バックエンド実装
     - ports定義
     - provider実装
     - handler実装
     - テスト作成
   - フロントエンド実装
     - 型定義
     - APIクライアント
     - UIコンポーネント
     - ページ実装

3. **検証**
   - ローカルテスト
   - デプロイ前チェック
   - 動作確認

4. **ドキュメント**
   - README更新（必要に応じて）
   - CLAUDE.md更新（必要に応じて）

**Bug（バグ修正）の場合**:
1. **原因調査**
   - エラーログ確認
   - 再現手順確認
   - コードレビュー

2. **修正実装**
   - バグ修正
   - テスト追加（再発防止）

3. **検証**
   - 修正確認
   - 回帰テスト

### ステップ4: ファイル特定

**影響を受けるファイル一覧**:

**バックエンド**:
```
- backend/src/domain/ports/<port_name>.py
- backend/src/infrastructure/providers/<provider_name>.py
- backend/src/api/handlers/<handler_name>.py
- backend/tests/**/<test_file>.py
```

**フロントエンド**:
```
- frontend/src/types/index.ts
- frontend/src/api/client.ts
- frontend/src/pages/<Page>.tsx
- frontend/src/components/<Component>.tsx
```

**インフラ**:
```
- cdk/lib/stacks/<stack_name>.ts
```

### ステップ5: テスト項目の抽出

**テストカテゴリー**:
1. **単体テスト**: 関数・メソッドレベル
2. **統合テスト**: API・コンポーネントレベル
3. **E2Eテスト**: ユーザーシナリオレベル（手動）

**テスト項目例**:
```
- [ ] バックエンド: 開催日一覧取得APIが正しくデータを返す
- [ ] バックエンド: 存在しない日付範囲でエラーハンドリング
- [ ] フロントエンド: 開催日一覧が正しく表示される
- [ ] フロントエンド: 日付選択時にレース一覧が更新される
- [ ] E2E: ブラウザで日付選択→レース表示の流れを確認
```

## 出力形式

```
📋 実装タスク生成完了

Issue: #<番号> - <タイトル>
種別: <Feature/Bug/Refactor/etc>
影響範囲: <Frontend/Backend/API/etc>

## タスクリスト

### 1. 設計
- [ ] データモデル設計（開催日一覧のAPI仕様）
- [ ] UI設計（日付セレクターのデザイン）

### 2. バックエンド実装
- [ ] ports定義: get_race_dates メソッドを追加
- [ ] JRA-VAN Provider実装: get_race_dates を実装
- [ ] Mock Provider実装: get_race_dates のMock実装
- [ ] Handler実装: GET /races/dates エンドポイント作成
- [ ] テスト作成: test_get_race_dates.py

### 3. フロントエンド実装
- [ ] 型定義: ApiRaceDatesResponse 型を追加
- [ ] APIクライアント: getRaceDates メソッドを追加
- [ ] コンポーネント: DateSelector コンポーネント作成
- [ ] ページ更新: RacesPage に DateSelector を統合

### 4. 検証
- [ ] pytest 実行（バックエンド）
- [ ] npm run test 実行（フロントエンド）
- [ ] デプロイ前チェック実行
- [ ] ローカル動作確認

### 5. デプロイ
- [ ] PRレビュー対応
- [ ] mainブランチにマージ
- [ ] CDKデプロイ（--context jravan=true）
- [ ] 本番環境で動作確認

## 影響ファイル

**バックエンド**:
- `backend/src/domain/ports/race_data_provider.py`
- `backend/src/infrastructure/providers/jravan_race_data_provider.py`
- `backend/src/infrastructure/providers/mock_race_data_provider.py`
- `backend/src/api/handlers/races.py`
- `backend/tests/application/use_cases/test_get_race_dates.py`

**フロントエンド**:
- `frontend/src/types/index.ts`
- `frontend/src/api/client.ts`
- `frontend/src/components/DateSelector.tsx` (新規)
- `frontend/src/pages/RacesPage.tsx`

## テスト項目

**バックエンド**:
- [ ] 開催日一覧取得APIが日付範囲を正しく返す
- [ ] from_date, to_date パラメータが機能する
- [ ] データがない場合は空配列を返す
- [ ] 日付が昇順でソートされている

**フロントエンド**:
- [ ] 開催日一覧が正しく表示される
- [ ] 日付選択時にレース一覧APIが呼ばれる
- [ ] ローディング状態が正しく表示される
- [ ] エラー時にトースト通知が表示される

**E2E（手動）**:
- [ ] ブラウザで日付セレクターが表示される
- [ ] 開催日のみが選択可能
- [ ] 日付選択するとレース一覧が更新される
- [ ] モバイル画面でも正しく動作する

## 推奨実装順序

1. バックエンドAPI実装（TDD）
2. フロントエンド型定義・APIクライアント
3. フロントエンドUIコンポーネント
4. 統合テスト
5. デプロイ

## 推定工数

- バックエンド実装: 2時間
- フロントエンド実装: 3時間
- テスト・検証: 1時間
- 合計: 約6時間
```

## 使用例

### 例1: 新機能追加Issue

```
/issue-to-task 39

Issue取得中...

📋 実装タスク生成完了

Issue: #39 - 日付セレクターを動的な開催日一覧に変更
種別: Feature (enhancement)
影響範囲: Frontend, Backend, API

## タスクリスト
（上記の形式で出力）

次のアクション:
- [ ] git worktree add で作業ブランチ作成
- [ ] /api-extend スキルでバックエンド実装
- [ ] /ui-component スキルでフロントエンド実装
```

### 例2: バグ修正Issue

```
/issue-to-task 42

Issue取得中...

📋 実装タスク生成完了

Issue: #42 - レース詳細でオッズが正しく表示されない
種別: Bug (bug)
影響範囲: Frontend

## タスクリスト

### 1. 原因調査
- [ ] エラーログ確認
- [ ] オッズデータの型を確認
- [ ] マッピング関数を確認

### 2. 修正実装
- [ ] mapApiRunnerToRunner 関数を修正
- [ ] オッズのパース処理を追加
- [ ] テスト追加（再発防止）

### 3. 検証
- [ ] ユニットテスト実行
- [ ] ブラウザで動作確認

影響ファイル:
- `frontend/src/types/index.ts`
- `frontend/src/types/index.test.ts` (新規)

推定工数: 1時間
```

## 参照コマンド

```bash
# Issue一覧表示
gh issue list

# Issue詳細表示
gh issue view <Issue番号>

# Issueコメント表示
gh issue view <Issue番号> --comments

# Issue作成
gh issue create --title "タイトル" --body "本文"
```

## 注意事項

- **Issue内容の明確性**: 曖昧なIssueは詳細化を依頼
- **スコープの適切性**: 大きすぎるIssueは分割提案
- **既存実装の確認**: 類似機能の実装パターンを参照
- **テストの重要性**: テスト項目は必ず含める
