---
name: deploy-prep
description: デプロイ前チェックスクリプトを実行し、エラーを解析・修正
version: 1.0.0
tools:
  - Bash
  - Read
  - Edit
  - Grep
skill_type: verification
auto_invoke: false
---

# デプロイ前チェック

## 概要

デプロイ前に必須のチェック項目（テスト・リント・CDK Synth）を自動実行し、エラーが発生した場合は原因を解析して修正を提案します。デプロイ失敗による手戻りをゼロにすることを目標とします。

## 入力形式

スキル呼び出し時にオプションを指定できます:

```
/deploy-prep
```

または特定のチェックのみ実行:

```
/deploy-prep --backend-only
/deploy-prep --frontend-only
/deploy-prep --cdk-only
```

## 実行プロセス

### ステップ1: 環境確認

デプロイ前チェックを実行できる環境か確認します。

**確認項目**:
- 現在のディレクトリが git worktree のルート
- `main` ディレクトリが存在
- `scripts/pre-deploy-check.sh` が存在

**コマンド**:
```bash
# worktree 確認
git worktree list

# スクリプト存在確認
ls -la main/scripts/pre-deploy-check.sh
```

### ステップ2: デプロイ前チェックスクリプト実行

`scripts/pre-deploy-check.sh` を実行し、全チェック項目を検証します。

**コマンド**:
```bash
cd main
./scripts/pre-deploy-check.sh
```

**チェック内容**:
1. **バックエンドテスト** (`pytest`)
2. **フロントエンドリント** (`npm run lint`)
3. **フロントエンドテスト** (`npm run test:run`)
4. **CDK Synth確認** (`npx cdk synth`)

### ステップ3: エラー解析

各チェックでエラーが発生した場合、エラー種別を分析します。

#### エラーカテゴリー

##### 1. バックエンドテストエラー

**エラーパターン**:
```
FAILED tests/domain/test_race.py::test_race_creation - AssertionError: assert None is not None
```

**原因分析**:
- テストロジックの不備
- Mock データの不整合
- 型エラー
- インポート漏れ

**対処法**:
1. 失敗したテストファイルを読む
2. テストコードとソースコードを比較
3. 修正を提案

##### 2. フロントエンドリントエラー

**エラーパターン**:
```
error  'React' is defined but never used  @typescript-eslint/no-unused-vars
warning  Unexpected console statement  no-console
```

**原因分析**:
- 未使用変数・インポート
- console.log の残存
- コーディングスタイル違反

**対処法**:
1. ESLint ルールに従って修正
2. 自動修正可能な場合は `npm run lint -- --fix`

##### 3. フロントエンドテストエラー

**エラーパターン**:
```
FAIL src/components/RaceCard.test.tsx
  ● RaceCard › renders race information
    TypeError: Cannot read property 'name' of undefined
```

**原因分析**:
- Propsの型不整合
- Mockデータの不足
- テストセットアップの不備

**対処法**:
1. テストファイルを読む
2. コンポーネントとテストの整合性を確認
3. Mock データを修正

##### 4. CDK Synthエラー

**エラーパターン**:
```
Error: Cannot find module '@aws-cdk/aws-lambda'
Snapshot verification failed. Re-run with --force
```

**原因分析**:
- 依存関係の不足
- CDK スナップショット不一致
- スタック定義の誤り

**対処法**:
1. 依存関係インストール: `npm install`
2. スナップショット更新: `npx cdk synth --force`
3. スタック定義を確認

### ステップ4: 修正提案

エラー内容に基づいて具体的な修正方法を提案します。

**提案フォーマット**:
```
🔴 エラー検出: <エラー種別>

ファイル: <ファイルパス>:<行番号>
エラー内容: <エラーメッセージ>

原因: <原因の説明>

修正案:
1. <修正手順1>
2. <修正手順2>

修正後の再実行コマンド:
./scripts/pre-deploy-check.sh
```

### ステップ5: 修正実施

ユーザーの承認後、修正を実施します。

**修正パターン例**:

#### パターン1: 未使用インポート削除
```typescript
// Before
import React, { useState } from 'react';
import { UnusedType } from './types';

// After
import { useState } from 'react';
```

#### パターン2: console.log削除
```typescript
// Before
const result = await fetchData();
console.log('Result:', result);
return result;

// After
const result = await fetchData();
return result;
```

#### パターン3: テスト修正
```typescript
// Before
it('renders race information', () => {
  render(<RaceCard />);
});

// After
it('renders race information', () => {
  const mockRace = { name: 'Test Race', venue: 'Tokyo' };
  render(<RaceCard race={mockRace} />);
});
```

### ステップ6: 再実行・検証

修正後、再度チェックスクリプトを実行して全て通過することを確認します。

**コマンド**:
```bash
./scripts/pre-deploy-check.sh
```

**成功出力**:
```
✅ バックエンドテスト成功
✅ フロントエンドリント成功
✅ フロントエンドテスト成功
✅ CDK Synth成功

🎉 全てのチェックに合格しました。デプロイ可能です。
```

### ステップ7: デプロイガイダンス

全チェック通過後、デプロイ手順を案内します。

**フロントエンドデプロイ**:
```bash
# Amplifyが自動デプロイ（mainブランチへのマージ後）
git push origin main
```

**バックエンドデプロイ**:
```bash
cd cdk

# 重要: --context jravan=true を必ず付ける
npx cdk deploy --all --context jravan=true --require-approval never
```

**デプロイ後確認**:
1. CloudWatch Logs でエラーがないか確認
2. ブラウザで動作確認
3. レース情報が正しく表示されるか確認

## 出力形式

### 全チェック成功時

```
✅ デプロイ前チェック完了

実行内容:
- [✅] バックエンドテスト (pytest)
- [✅] フロントエンドリント (npm run lint)
- [✅] フロントエンドテスト (npm run test:run)
- [✅] CDK Synth (npx cdk synth)

🎉 全てのチェックに合格しました。

次のアクション:
- [ ] フロントエンドデプロイ（git push origin main）
- [ ] バックエンドデプロイ（cd cdk && npx cdk deploy --all --context jravan=true）
- [ ] デプロイ後の動作確認
```

### エラー検出時

```
🔴 デプロイ前チェックでエラーを検出

実行内容:
- [✅] バックエンドテスト (pytest)
- [🔴] フロントエンドリント (npm run lint) - 2件のエラー
- [⏭️] フロントエンドテスト (スキップ)
- [⏭️] CDK Synth (スキップ)

---
🔴 エラー #1: 未使用変数

ファイル: frontend/src/pages/RaceDetailPage.tsx:15
エラー: 'unused' is defined but never used

原因: インポートしたが使用していない変数

修正案:
1. 該当インポートを削除
2. または変数名の先頭に _ を付ける（意図的な未使用の場合）

---
🔴 エラー #2: console.log残存

ファイル: frontend/src/api/client.ts:89
エラー: Unexpected console statement

原因: デバッグ用のconsole.logが残っている

修正案:
1. console.log を削除
2. または logger.debug() に置き換え

---

次のアクション:
- [ ] エラー修正
- [ ] 再実行: ./scripts/pre-deploy-check.sh
```

## エラーハンドリング

### 頻出エラーと対処法

1. **pytest: ModuleNotFoundError**
   ```
   ModuleNotFoundError: No module named 'src'
   ```
   - 対処: `cd main/backend` で正しいディレクトリに移動

2. **npm: command not found**
   ```
   bash: npm: command not found
   ```
   - 対処: Node.js がインストールされているか確認

3. **CDK: AWS認証エラー**
   ```
   Error: Unable to resolve AWS credentials
   ```
   - 対処: `aws configure` で認証情報を設定

4. **テストタイムアウト**
   ```
   FAILED tests/api/test_handler.py::test_timeout
   ```
   - 対処: モックの設定を確認、または `pytest -v --timeout=60`

## 使用例

### 例1: リントエラー修正

```
/deploy-prep

実行中...

🔴 デプロイ前チェックでエラーを検出

- [✅] バックエンドテスト (pytest)
- [🔴] フロントエンドリント (npm run lint) - 3件のエラー

---
エラー #1: 未使用インポート
ファイル: frontend/src/pages/RaceDetailPage.tsx:5
修正: `import { UnusedComponent } from './components'` を削除
---

修正しますか？
> はい

✅ 修正完了。再実行中...

✅ 全てのチェックに合格しました。
```

### 例2: テスト失敗修正

```
/deploy-prep

実行中...

🔴 デプロイ前チェックでエラーを検出

- [🔴] バックエンドテスト (pytest) - 1件の失敗

---
エラー: test_get_race_weights 失敗
ファイル: tests/infrastructure/providers/test_mock_race_data_provider.py:45

原因: Mock実装が最新のポート定義に追従していない

修正案:
1. MockRaceDataProvider に get_race_weights メソッドを追加
2. テストケースのMockデータを更新

修正しますか？
> はい

✅ 修正完了。再実行中...

✅ 全てのチェックに合格しました。
```

## 参照スクリプト

### pre-deploy-check.sh の内容

スクリプトは以下のチェックを順次実行:

```bash
#!/bin/bash

# 1. バックエンドテスト
cd backend
pytest

# 2. フロントエンドリント
cd ../frontend
npm run lint

# 3. フロントエンドテスト
npm run test:run

# 4. CDK Synth
cd ../cdk
npx cdk synth
```

## 注意事項

- **実行環境**: 必ず `main` ディレクトリ内で実行
- **CDK Context**: デプロイ時は `--context jravan=true` を必ず付与
- **git worktree**: feature ブランチで作業、main への直接 push 禁止
- **CI/CD**: GitHub Actions でも同じチェックが実行される
- **テスト順序**: 1つでも失敗したら後続をスキップ（高速フィードバック）

## デプロイ後の確認手順

1. **CloudWatch Logs確認**
   ```bash
   aws logs tail /aws/lambda/baken-kaigi-races --follow
   ```

2. **API動作確認**
   ```bash
   curl -X GET "https://api.example.com/races?date=2026-01-23"
   ```

3. **ブラウザ確認**
   - Amplify デプロイURL にアクセス
   - レース一覧が正しく表示されるか
   - エラートーストが出ないか
