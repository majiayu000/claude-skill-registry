---
name: dependency-upgrade-path
description: 依存更新計画を策定
user-invocable: true
argument-hint: [パッケージ名または--all]
allowed-tools: Read, Bash, Grep
context: fork
---

# civicship-api 依存関係アップグレード計画

依存パッケージの**アップグレード計画**を策定し、破壊的変更、セキュリティリスク、互換性問題を考慮した**安全なアップデート経路**を提示します。

## 使用方法

```bash
# 特定パッケージのアップグレード計画
/dependency-upgrade-path prisma

# 全パッケージの更新可能リスト
/dependency-upgrade-path --all

# セキュリティ脆弱性のあるパッケージのみ
/dependency-upgrade-path --security-only
```

**引数:**
- `$ARGUMENTS`: パッケージ名、`--all`, または `--security-only`

---

## アップグレード計画プロセス

### ステップ1: 現在の依存関係の分析

```bash
# package.jsonを読み取り
cat package.json

# 現在インストールされているバージョン
pnpm list --depth=0

# 更新可能なパッケージのリスト
pnpm outdated

# セキュリティ脆弱性のチェック
pnpm audit
```

**依存関係レポート:**

```markdown
## 依存関係の現状

### 主要パッケージ

| パッケージ | 現在 | 最新 | 種別 | 遅延 |
|-----------|------|------|------|------|
| @prisma/client | 5.8.0 | 5.10.2 | production | 2バージョン |
| @apollo/server | 4.9.5 | 4.10.0 | production | 1バージョン |
| typescript | 5.3.3 | 5.4.2 | devDependencies | 1バージョン |
| graphql | 16.8.1 | 16.8.1 | production | ✅ 最新 |
| tsyringe | 4.8.0 | 4.8.0 | production | ✅ 最新 |

---

### 依存関係の分類

#### Production Dependencies（本番環境）
- **総数:** 45パッケージ
- **最新:** 30パッケージ（67%）
- **更新可能:** 12パッケージ（27%）
- **メジャー更新:** 3パッケージ（7%）

#### DevDependencies（開発環境）
- **総数:** 38パッケージ
- **最新:** 25パッケージ（66%）
- **更新可能:** 10パッケージ（26%）
- **メジャー更新:** 3パッケージ（8%）

---

### セキュリティ脆弱性

\`\`\`bash
pnpm audit
\`\`\`

**結果:**
- **Critical:** 1件
- **High:** 3件
- **Moderate:** 5件
- **Low:** 2件

**総合評価:** 🔴 High Risk（早急な対応必要）
```

---

### ステップ2: アップグレード候補の分類

更新を影響度別に分類:

```markdown
## アップグレード候補

### 🔴 Critical: セキュリティ脆弱性あり

#### 1. axios: 1.5.0 → 1.6.7

**脆弱性:**
- CVE-2023-45857: SSRF (Server-Side Request Forgery)
- 深刻度: High

**影響範囲:**
- 外部APIへのHTTPリクエスト
- 使用箇所: 3ファイル

**破壊的変更:**
- なし（パッチバージョンアップ）

**推奨アクション:** 🚨 即座にアップデート
**リスク:** 🟢 Low
**工数:** 0.5時間（テスト含む）

---

### 🟡 High Priority: メジャーバージョンアップ

#### 2. Prisma: 5.8.0 → 5.10.2

**変更内容:**
- 新機能: `relationJoins` プレビュー機能（パフォーマンス向上）
- バグ修正: トランザクション関連の修正
- 破壊的変更: なし（マイナーバージョンアップ）

**影響範囲:**
- 全てのRepository層
- Prismaスキーマ

**推奨アクション:** ✅ アップデート推奨
**リスク:** 🟢 Low
**工数:** 1時間
**備考:** `relationJoins` 有効化でN+1問題の改善可能

---

#### 3. @apollo/server: 4.9.5 → 4.10.0

**変更内容:**
- 新機能: `@defer` ディレクティブ対応
- パフォーマンス改善
- 破壊的変更: なし

**影響範囲:**
- GraphQLサーバー起動部分
- ミドルウェア

**推奨アクション:** ✅ アップデート推奨
**リスク:** 🟢 Low
**工数:** 0.5時間

---

### 🟢 Medium Priority: マイナーバージョンアップ

#### 4. TypeScript: 5.3.3 → 5.4.2

**変更内容:**
- 新機能: `NoInfer` ユーティリティ型
- 型チェックの改善
- 破壊的変更: なし

**影響範囲:**
- 全TypeScriptファイル
- コンパイル時のみ

**推奨アクション:** ⏰ 次回メンテナンス時
**リスク:** 🟢 Low
**工数:** 0.5時間（型エラー確認）

---

### 🔵 Low Priority: パッチバージョンアップ

#### 5. @types/node: 20.10.5 → 20.11.20

**変更内容:**
- 型定義の改善
- 破壊的変更: なし

**推奨アクション:** 💤 急ぎではない
**リスク:** 🟢 None
**工数:** 0.1時間
```

---

### ステップ3: 破壊的変更の検出

メジャーバージョンアップの破壊的変更を特定:

```markdown
## 破壊的変更の分析

### パッケージ: なし

**現在の候補に破壊的変更を含むメジャーバージョンアップはありません。**

---

### （参考）もし Prisma 5.x → 6.x へアップグレードする場合

#### 想定される破壊的変更

1. **クライアント生成の変更**
   - `@prisma/client` のインポート方法が変更
   - 既存コードの修正必要

2. **スキーマ構文の変更**
   - 一部の属性が非推奨化
   - `prisma migrate` でスキーマ更新必要

3. **型定義の変更**
   - Prisma型の構造が変更
   - Presenter/Converterの修正必要

#### 影響範囲

- **Repository層:** 全ファイル（50箇所）
- **Presenter層:** 全ファイル（30箇所）
- **Converter層:** 全ファイル（20箇所）
- **テストコード:** 全ファイル（100箇所）

#### 工数見積もり

- コード修正: 16時間
- テスト: 8時間
- マイグレーション: 4時間
- **合計:** 28時間（3.5日）

#### 推奨アクション

- ⏸️ 延期（現状5.xで問題なし）
- 6.xの安定化を待つ（リリース後3ヶ月以上）
- 段階的移行計画を策定
```

---

### ステップ4: 依存関係の互換性チェック

パッケージ間の互換性を確認:

```bash
# 依存関係ツリーを確認
pnpm list --depth=3

# ピア依存関係の確認
pnpm list --dev --depth=0 | grep -E "UNMET|ERR"
```

**互換性レポート:**

```markdown
## 依存関係の互換性

### ピア依存関係の問題

#### 問題なし

- ✅ `@prisma/client` と `prisma` のバージョン一致
- ✅ `graphql` と `@apollo/server` の互換性確認済み
- ✅ `typescript` とすべての `@types/*` の互換性OK

---

### 依存関係の衝突

#### 検出された衝突: なし

---

### トランジティブ依存関係（間接依存）

#### 注意が必要なパッケージ

**1. axios → follow-redirects**
- `axios` が依存する `follow-redirects` に脆弱性
- `axios` のアップデートで自動解決

**2. @apollo/server → graphql-ws**
- `graphql-ws` のバージョンが古い
- `@apollo/server` のアップデートで自動解決

**結論:** ✅ 直接依存のアップデートで全て解決
```

---

### ステップ5: アップグレード戦略の策定

段階的なアップグレード計画:

```markdown
## アップグレード戦略

### Phase 1: セキュリティパッチ（即時実施）

**対象パッケージ:**
1. axios: 1.5.0 → 1.6.7

**実施タイミング:** 🚨 即座（今週中）

**手順:**
\`\`\`bash
# 1. アップデート実行
pnpm update axios

# 2. テスト実行
pnpm test

# 3. 動作確認
pnpm dev
\`\`\`

**リスク:** 🟢 Low
**工数:** 0.5時間
**ロールバック:** `pnpm install axios@1.5.0`

---

### Phase 2: 主要パッケージの更新（今月中）

**対象パッケージ:**
1. Prisma: 5.8.0 → 5.10.2
2. @apollo/server: 4.9.5 → 4.10.0

**実施タイミング:** 2週間以内

**手順:**
\`\`\`bash
# 1. ブランチ作成
git checkout -b chore/upgrade-prisma-apollo

# 2. アップデート実行
pnpm update @prisma/client prisma @apollo/server

# 3. Prisma Client再生成
pnpm db:generate

# 4. TypeScript型チェック
pnpm tsc --noEmit

# 5. テスト実行
pnpm test

# 6. E2Eテスト
pnpm test:e2e

# 7. 開発環境で動作確認
pnpm dev

# 8. ステージング環境でデプロイテスト
\`\`\`

**リスク:** 🟡 Medium
**工数:** 2時間
**ロールバック:** ブランチを削除、`pnpm install`

---

### Phase 3: 開発ツールの更新（来月）

**対象パッケージ:**
1. TypeScript: 5.3.3 → 5.4.2
2. eslint: 8.56.0 → 8.57.0
3. prettier: 3.1.1 → 3.2.5

**実施タイミング:** 1ヶ月以内

**手順:**
\`\`\`bash
# 1. アップデート
pnpm update -D typescript eslint prettier

# 2. 型チェック
pnpm tsc --noEmit

# 3. Lint実行
pnpm lint

# 4. フォーマット確認
pnpm format:check
\`\`\`

**リスク:** 🟢 Low
**工数:** 1時間

---

### Phase 4: その他の依存関係（四半期ごと）

**対象:** パッチバージョンアップ、型定義など

**実施タイミング:** 3ヶ月ごと

**手順:**
\`\`\`bash
# 一括更新（パッチのみ）
pnpm update --latest
\`\`\`

**リスク:** 🟢 Low
**工数:** 0.5時間
```

---

### ステップ6: テスト戦略

アップグレード後の検証:

```markdown
## テスト戦略

### Phase 1: セキュリティパッチ

#### ユニットテスト
\`\`\`bash
# axios を使用するファイルのテスト
pnpm test src/infrastructure/api
\`\`\`

#### 統合テスト
\`\`\`bash
# 外部API連携のテスト
pnpm test __tests__/integration/external-api
\`\`\`

#### 手動確認
- [ ] LINE API連携
- [ ] Firebase Auth連携
- [ ] Google Cloud Storage連携

---

### Phase 2: 主要パッケージ

#### ユニットテスト
\`\`\`bash
# 全テスト実行
pnpm test
\`\`\`

**カバレッジ目標:** 変更なし（85%以上維持）

#### 統合テスト
\`\`\`bash
# GraphQL API テスト
pnpm test __tests__/integration

# E2Eテスト
pnpm test __tests__/e2e
\`\`\`

#### パフォーマンステスト
\`\`\`bash
# クエリパフォーマンス計測
# 期待: Prisma 5.10 の relationJoins でN+1改善
\`\`\`

**目標:**
- レスポンスタイム: 変化なし or 改善
- エラー率: 0%

#### 手動確認
- [ ] ウォレット作成・更新
- [ ] ポイント送受信
- [ ] Opportunity作成
- [ ] LINE通知送信
- [ ] 管理画面の動作

---

### Phase 3: 開発ツール

#### 型チェック
\`\`\`bash
pnpm tsc --noEmit
\`\`\`

**期待:** エラー0件

#### Lint
\`\`\`bash
pnpm lint
\`\`\`

**期待:** 警告・エラー0件

#### フォーマット
\`\`\`bash
pnpm format:check
\`\`\`

**期待:** フォーマット違反0件
```

---

### ステップ7: ロールバック計画

アップグレード失敗時の対処:

```markdown
## ロールバック計画

### Phase 1: セキュリティパッチ

**ロールバック手順:**
\`\`\`bash
# 1. 旧バージョンに戻す
pnpm install axios@1.5.0

# 2. lockファイル確認
git diff pnpm-lock.yaml

# 3. テスト実行
pnpm test

# 4. コミット
git add package.json pnpm-lock.yaml
git commit -m "revert: Rollback axios to 1.5.0"
\`\`\`

**所要時間:** 5分

---

### Phase 2: 主要パッケージ

**ロールバック手順:**
\`\`\`bash
# 1. ブランチごと削除
git checkout main
git branch -D chore/upgrade-prisma-apollo

# 2. 再インストール（念のため）
pnpm install

# 3. Prisma Client再生成
pnpm db:generate
\`\`\`

**所要時間:** 10分

**注意:**
- マイグレーションは実行していないため、DBは影響なし
- 本番環境にデプロイしていなければノーリスク

---

### Phase 3: 開発ツール

**ロールバック手順:**
\`\`\`bash
# 1. package.json を git で戻す
git checkout HEAD -- package.json pnpm-lock.yaml

# 2. 再インストール
pnpm install
\`\`\`

**所要時間:** 3分

---

### 本番環境でのロールバック

**緊急時（本番でエラー発生）:**

\`\`\`bash
# 1. 即座に前バージョンをデプロイ
git revert HEAD
git push origin main

# 2. CI/CDで自動デプロイ
# または
docker-compose pull && docker-compose up -d

# 3. ヘルスチェック
curl https://api.civicship.jp/health
\`\`\`

**所要時間:** 5分（CI/CD次第）
```

---

### ステップ8: スケジュール策定

具体的なアップグレードスケジュール:

```markdown
## アップグレードスケジュール

### Week 1: セキュリティパッチ

| Day | タスク | 担当 | 工数 |
|-----|--------|------|------|
| Mon | axios アップデート | Backend | 0.5h |
| Mon | テスト実行 | Backend | 0.5h |
| Mon | コミット・プッシュ | Backend | 0.1h |
| Mon | ステージング確認 | QA | 0.5h |
| Tue | 本番デプロイ | DevOps | 0.5h |

**Total:** 2.1時間

---

### Week 2-3: 主要パッケージ

| Day | タスク | 担当 | 工数 |
|-----|--------|------|------|
| Week 2 Mon | ブランチ作成、アップデート | Backend | 0.5h |
| Week 2 Mon | 型チェック、テスト | Backend | 1h |
| Week 2 Tue | E2Eテスト | QA | 1h |
| Week 2 Wed | コードレビュー | Tech Lead | 1h |
| Week 2 Thu | ステージングデプロイ | DevOps | 0.5h |
| Week 2 Fri | ステージング確認 | QA | 1h |
| Week 3 Mon | 本番デプロイ | DevOps | 0.5h |
| Week 3 Mon | 本番監視 | Backend | 2h |

**Total:** 7.5時間

---

### Week 4: 開発ツール

| Day | タスク | 担当 | 工数 |
|-----|--------|------|------|
| Mon | アップデート実行 | Backend | 0.3h |
| Mon | 型チェック、Lint | Backend | 0.5h |
| Mon | コミット・プッシュ | Backend | 0.1h |
| Tue | CI確認 | Backend | 0.3h |

**Total:** 1.2時間

---

### 総工数

- **Phase 1:** 2.1時間
- **Phase 2:** 7.5時間
- **Phase 3:** 1.2時間
- **合計:** 10.8時間（約1.5日）
```

---

### ステップ9: 監視とアラート

アップグレード後の監視:

```markdown
## 監視項目

### Phase 1: セキュリティパッチ後

**メトリクス:**
- 外部APIエラー率
- HTTPリクエストの成功率
- レスポンスタイム

**アラート:**
- エラー率 > 1% で警告
- エラー率 > 5% で緊急（ロールバック検討）

**監視期間:** 24時間

---

### Phase 2: 主要パッケージ後

**メトリクス:**
- GraphQLクエリエラー率
- データベースクエリ時間
- トランザクション成功率
- メモリ使用量

**アラート:**
- エラー率 > 0.5% で警告
- クエリ時間 > 200ms で警告（通常100ms）
- メモリ使用量 > 80% で警告

**監視期間:** 1週間

---

### Phase 3: 開発ツール後

**メトリクス:**
- CI/CDビルド成功率
- 型エラー発生数

**アラート:**
- ビルド失敗で即座通知

**監視期間:** 48時間
```

---

### ステップ10: アップグレードレポートの生成

```markdown
# 依存関係アップグレードレポート

**分析日:** YYYY-MM-DD
**対象:** 全依存パッケージ
**総合評価:** 🟡 アップグレード推奨

---

## 要約

### 更新可能パッケージ

- **セキュリティ:** 1件（Critical）
- **主要パッケージ:** 2件
- **開発ツール:** 3件
- **その他:** 16件

### 総工数見積もり

- **Phase 1（必須）:** 2.1時間
- **Phase 2（推奨）:** 7.5時間
- **Phase 3（任意）:** 1.2時間
- **合計:** 10.8時間

### リスク評価

- **セキュリティリスク:** 🔴 High（早急な対応必要）
- **互換性リスク:** 🟢 Low（破壊的変更なし）
- **パフォーマンスリスク:** 🟢 Low（改善の可能性）

---

## 推奨アクション

### 即座に実施

1. **axios のセキュリティパッチ** （Today）
   - 脆弱性対応
   - 工数: 0.5時間

### 2週間以内に実施

2. **Prisma アップグレード** （Week 2-3）
   - パフォーマンス改善
   - 工数: 2時間

3. **Apollo Server アップグレード** （Week 2-3）
   - 新機能対応
   - 工数: 0.5時間

### 1ヶ月以内に実施

4. **TypeScript アップグレード** （Week 4）
   - 型チェック改善
   - 工数: 1時間

---

## 承認

- [ ] テックリード
- [ ] DevOpsリード
- [ ] セキュリティ担当
```

---

## 活用例

### 例1: 全パッケージの確認

```bash
/dependency-upgrade-path --all
```

**出力:**
- 更新可能パッケージ一覧
- 優先度付き
- アップグレード計画

---

### 例2: セキュリティ脆弱性のみ

```bash
/dependency-upgrade-path --security-only
```

**出力:**
- 脆弱性のあるパッケージ
- CVE情報
- 即座のアクションプラン

---

### 例3: 特定パッケージ

```bash
/dependency-upgrade-path prisma
```

**出力:**
- Prismaの詳細なアップグレード計画
- 破壊的変更の分析
- マイグレーション手順

---

## 注意事項

### アップグレードの原則

- ✅ **セキュリティパッチは最優先**
- ✅ **段階的にアップグレード**（一度に全部更新しない）
- ✅ **テストを必ず実行**
- ✅ **ロールバック計画を用意**
- ✅ **本番前にステージングで確認**

### よくある失敗

- ❌ メジャーバージョンアップを一度に複数実行
- ❌ テストをスキップ
- ❌ 破壊的変更を確認せずアップグレード
- ❌ ロールバック計画なし

### 推奨される併用スキル

- `/legacy-audit` - 技術的負債の把握
- `/map-impact-analysis` - 影響範囲の確認
- `/test-domain` - アップグレード後のテスト

---

## 参考資料

- [pnpm update documentation](https://pnpm.io/cli/update)
- [Prisma upgrade guide](https://www.prisma.io/docs/guides/upgrade-guides)
- [Node.js security best practices](https://nodejs.org/en/docs/guides/security/)
