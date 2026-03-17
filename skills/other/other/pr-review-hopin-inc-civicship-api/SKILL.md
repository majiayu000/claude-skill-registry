---
name: pr-review
description: PRレビュー支援
context: fork
agent: Explore
user-invocable: true
argument-hint: [PR番号]
allowed-tools: Read, Grep, Bash
---

# civicship-api プルリクエストレビュー

プルリクエストの包括的なレビューを実行します。アーキテクチャ、セキュリティ、コード品質、テストカバレッジを総合的に評価します。

## 使用方法

```bash
# PR番号を指定してレビュー
/pr-review 123

# 現在のブランチの変更をレビュー
/pr-review
```

**引数:**
- `$ARGUMENTS`: PR番号（オプション）

---

## レビュープロセス

### ステップ1: PR情報の取得

**PR番号が指定された場合:**

```bash
# GitHub CLIでPR情報を取得
gh pr view $PR_NUMBER --json title,body,author,commits,files,additions,deletions
```

**PR番号が未指定の場合:**

```bash
# 現在のブランチから関連PRを検索
gh pr list --head $(git branch --show-current) --json number,title
```

**PR情報を表示:**

```markdown
## プルリクエスト情報

- **PR**: #123
- **タイトル**: feat: Add product domain with DDD pattern
- **作成者**: @username
- **コミット数**: 5
- **変更ファイル数**: 12
- **追加**: +450 lines
- **削除**: -20 lines
```

---

### ステップ2: 変更ファイルの取得

```bash
# PRの変更ファイルとdiffを取得
gh pr diff $PR_NUMBER > /tmp/pr-$PR_NUMBER.diff

# 変更ファイル一覧
gh pr view $PR_NUMBER --json files --jq '.files[].path'
```

**変更ファイルを分類:**

```markdown
## 変更ファイル

### ドメインロジック（7ファイル）
- src/application/domain/product/usecase.ts
- src/application/domain/product/service.ts
- src/application/domain/product/data/repository.ts
- src/application/domain/product/data/converter.ts
- src/application/domain/product/data/type.ts
- src/application/domain/product/presenter.ts
- src/application/domain/product/controller/resolver.ts

### GraphQLスキーマ（3ファイル）
- src/application/domain/product/schema/query.graphql
- src/application/domain/product/schema/mutation.graphql
- src/application/domain/product/schema/type.graphql

### 設定ファイル（2ファイル）
- src/application/provider.ts
- src/presentation/graphql/resolver.ts
```

---

### ステップ3: アーキテクチャレビュー

`/validate-architecture` スキルを実行:

```bash
# 変更されたドメインのアーキテクチャを検証
/validate-architecture product
```

**期待される出力:**
- レイヤー違反のチェック
- トランザクションパターンの検証
- RLSの実装確認
- GraphQL型の命名規則
- DataLoaderの使用

**レビュー結果に含める:**

```markdown
## アーキテクチャレビュー

### ✅ 準拠項目
- Resolverは UseCaseのみを呼び出している
- UseCaseで適切にトランザクションを管理
- Serviceがビジネスロジックを実装
- Repositoryで RLS を使用
- GraphQL型が正しい命名規則

### ⚠️  改善推奨
- [ ] `controller/dataloader.ts` の追加を推奨（N+1問題防止）
- [ ] `service.ts:45` でのenum値バリデーションの追加を検討
```

---

### ステップ4: セキュリティレビュー

`/security-review` スキルを実行:

```bash
# 変更されたファイルのセキュリティチェック
/security-review product
```

**期待される出力:**
- 認証・認可のチェック
- RLSの実装
- センシティブデータの取り扱い
- 入力バリデーション
- SQLインジェクション対策

**レビュー結果に含める:**

```markdown
## セキュリティレビュー

### ✅ セキュリティ準拠
- 適切な認証チェック
- RLS が全てのクエリで使用されている
- 入力バリデーションが実装されている

### ⚠️  セキュリティ警告
- なし
```

---

### ステップ5: コード品質レビュー

**TypeScriptエラーチェック:**

```bash
# TypeScriptコンパイルエラーをチェック
pnpm build 2>&1 | grep "error TS"
```

**Lintエラーチェック:**

```bash
# Lintエラーをチェック
pnpm lint 2>&1 | grep "error"
```

**コードスタイルのチェック:**
- コメントの適切性
- 関数の複雑度
- 重複コードの有無
- 命名規則の一貫性

**レビュー結果:**

```markdown
## コード品質

### ✅ 品質基準
- TypeScriptコンパイルエラー: 0件
- Lintエラー: 0件
- 適切なコメント
- 命名規則が一貫している

### 📝 推奨事項
- [ ] `service.ts` の複雑な関数を分割することを検討
- [ ] `converter.ts` にJSDocコメントの追加を推奨
```

---

### ステップ6: テストカバレッジレビュー

**テストファイルの存在確認:**

```bash
# 新規ドメインに対応するテストファイルを検索
find src/application/domain/product -name "*.test.ts"
find __tests__ -path "*/product/*" -name "*.test.ts"
```

**テストの実行:**

```bash
# ドメインのテストを実行
pnpm test src/application/domain/product/**/*.test.ts --coverage --runInBand
```

**カバレッジ分析:**

```markdown
## テストカバレッジ

### 📊 カバレッジ統計
- Statements: 92.5%
- Branches: 85.3%
- Functions: 90.0%
- Lines: 91.8%

### ✅ テスト実装
- ユニットテスト: 8ファイル、42テスト
- 統合テスト: 2ファイル、12テスト

### ⚠️  カバレッジ不足
- [ ] `service.ts` のエラーハンドリングをテスト（現在: 78%）
- [ ] `converter.ts` のエッジケースをテスト（現在: 82%）

### 💡 推奨
- 目標カバレッジ90%に対して現在92.5% ✅
```

---

### ステップ7: GraphQLスキーマレビュー

**スキーマ変更の検証:**

```bash
# GraphQLスキーマファイルの変更を確認
git diff origin/main -- '**/*.graphql'
```

**チェック項目:**
- 型命名が `Gql*` 規則に従っているか
- 破壊的変更がないか
- フィールドの説明（description）があるか
- クエリ/ミューテーションが適切に分類されているか

**レビュー結果:**

```markdown
## GraphQLスキーマ

### ✅ スキーマ準拠
- 型命名が `Gql*` 規則に従っている
- 破壊的変更なし
- 全フィールドに説明あり

### 📝 提案
- [ ] `GqlProduct` に `imageUrl` フィールドの追加を検討
- [ ] `productCreate` ミューテーションのエラーハンドリングを明記
```

---

### ステップ8: データベーススキーマレビュー

**Prismaスキーマの変更確認:**

```bash
# Prismaスキーマファイルの変更を確認
git diff origin/main -- prisma/schema.prisma
```

**チェック項目:**
- 命名規則（テーブル: `t_*`, カラム: camelCase）
- 適切なインデックス
- 外部キー制約
- デフォルト値

**マイグレーションファイルの確認:**

```bash
# 新しいマイグレーションファイルを確認
ls -t prisma/migrations/ | head -1
```

**レビュー結果:**

```markdown
## データベーススキーマ

### ✅ スキーマ準拠
- 命名規則に従っている
- 適切なインデックスが設定されている
- 外部キー制約が適切

### 📝 確認事項
- マイグレーション: `add_products_table`
- マイグレーションSQLが安全であることを確認済み ✅
```

---

### ステップ9: ドキュメントレビュー

**ドキュメント更新の確認:**

```bash
# ドキュメントファイルの変更を確認
git diff origin/main -- 'docs/**/*.md' 'README.md' 'CHANGELOG.md'
```

**チェック項目:**
- README の更新
- CHANGELOG への記載
- 機能ドキュメントの更新
- APIドキュメントの更新

**レビュー結果:**

```markdown
## ドキュメント

### ✅ ドキュメント更新
- CHANGELOG.md に機能追加を記載

### 📝 推奨更新
- [ ] README.md に新規ドメインの説明を追加
- [ ] `docs/handbook/FEATURES.md` に機能詳細を追加
```

---

### ステップ10: 総合評価とレビューコメント生成

全てのレビュー結果を統合し、総合評価を生成:

```markdown
# プルリクエストレビュー総合評価

## PR情報
- **PR**: #123
- **タイトル**: feat: Add product domain with DDD pattern
- **作成者**: @username
- **変更**: +450 / -20 lines (12ファイル)

## 総合評価: ✅ 承認（条件付き）

このPRは全体的に高品質で、DDD/Clean Architectureの原則に従っています。いくつかの軽微な改善提案がありますが、マージ可能な状態です。

---

## レビュー詳細

### ✅ 優れている点

1. **アーキテクチャ準拠**
   - レイヤー責任が明確
   - トランザクション管理が適切
   - RLSが全てのクエリで使用されている

2. **セキュリティ**
   - 認証・認可が適切に実装
   - 入力バリデーションが実装されている
   - センシティブデータの取り扱いが安全

3. **テストカバレッジ**
   - カバレッジ92.5%（目標90%を達成）
   - ユニットテストと統合テストの両方を実装

4. **GraphQLスキーマ**
   - 命名規則に従っている
   - 破壊的変更なし
   - 全フィールドに説明あり

### 📝 改善提案（マージ前）

- [ ] **High**: `controller/dataloader.ts` を追加してN+1問題を防止
- [ ] **Medium**: `service.ts` の複雑な関数を分割
- [ ] **Low**: README.md に新規ドメインの説明を追加

### 💡 将来の改善提案（マージ後）

- [ ] `service.ts` のエラーハンドリングのテストカバレッジ向上（現在78%）
- [ ] `GqlProduct` に画像URLフィールドの追加を検討
- [ ] パフォーマンスベンチマークの実施

---

## チェックリスト

- ✅ アーキテクチャレビュー完了
- ✅ セキュリティレビュー完了
- ✅ コード品質チェック完了
- ✅ テストカバレッジ確認完了
- ✅ GraphQLスキーマレビュー完了
- ✅ データベーススキーマレビュー完了
- ⚠️  ドキュメント更新推奨

---

## 次のステップ

1. **DataLoaderの追加**（必須）
   - `controller/dataloader.ts` を作成
   - N+1問題を防止

2. **ドキュメント更新**（推奨）
   - README.md に新規ドメインの説明を追加

3. **マージ後**
   - `/test-domain product` で最終確認
   - 本番環境へのデプロイ前にステージング環境でテスト

---

## コメント

素晴らしいPRです！DDD/Clean Architectureの原則に忠実で、テストカバレッジも十分です。DataLoaderの追加後、安心してマージできます。

お疲れ様でした！🎉
```

---

## レビュー基準

### マージ可否の判断基準

| 状態 | 条件 |
|------|------|
| **✅ マージ可** | 重大な問題なし、軽微な改善提案のみ |
| **⚠️  条件付き承認** | 軽微な問題あり、修正後にマージ可 |
| **❌ 変更要求** | 重大な問題あり、修正必須 |

### 重大な問題の例

- アーキテクチャ違反（レイヤー責任の逸脱）
- セキュリティ脆弱性（RLSバイパス、認証漏れ）
- 破壊的なAPI変更
- テストカバレッジ著しく不足（< 70%）
- TypeScriptコンパイルエラー
- 既存テストの失敗

### 軽微な問題の例

- DataLoaderの欠如（N+1問題の可能性）
- コメント不足
- ドキュメント更新漏れ
- 軽微なコードスタイルの不一致
- カバレッジがやや低い（70-80%）

---

## レビュー後のアクション

### 作成者へのフィードバック

GitHubのPRコメントとして投稿:

```bash
# レビューコメントを投稿
gh pr review $PR_NUMBER --approve --body "$(cat review-report.md)"

# または変更要求の場合
gh pr review $PR_NUMBER --request-changes --body "$(cat review-report.md)"
```

### レビューの記録

```bash
# レビュー履歴をファイルに保存
echo "$(date): PR #$PR_NUMBER reviewed" >> .claude/review-history.log
```

---

## 参考資料

以下については `@CLAUDE.md` を参照してください:
- プルリクエストのベストプラクティス
- コードレビューガイドライン
- マージ基準
