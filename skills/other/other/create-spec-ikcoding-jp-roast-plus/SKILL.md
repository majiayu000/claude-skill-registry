---
name: create-spec
description: 【手動用】既存IssueからWorking Documentsを生成。通常は /issue-creator で自動生成されるため、手動実行が必要な場合（古いIssue、外部で作成されたIssue等）に使用。「/create-spec 123」のように使用。
argument-hint: "[Issue番号]"
---

# Working Documents手動生成スキル

## 概要

**通常は `/issue-creator` でIssue作成と同時にWorking Documentsが生成されます。**

このスキルは以下の場合に手動で使用します:
- 古いIssue（Working Documentsがない）
- 外部で作成されたIssue（GitHub Web等）
- `/issue-creator` を使わずに作成されたIssue

## Working Documentsの役割

- **永続的な設計メモ**: 実装中のコンテキストを保持、セッション間で引き継ぐ
- **EnterPlanModeとの違い**: Working = 永続化、Plan = 一時的詳細計画（併用推奨）
- **Git保管**: PR完了後も削除せず、過去の設計判断の記録として保管

## ワークフロー

```
1. Issue取得 → 2. Steering参照 → 3. Serena MCP調査 → 4. Working生成 → 5. ユーザー確認
```

---

## Phase 1: Issue情報取得

```bash
gh issue view $ARGUMENTS --json title,body,labels,number,assignees
```

以下の情報を抽出:
- Issue番号
- タイトル
- 本文（要件、背景、作業内容）
- ラベル（bug, enhancement, refactor 等）

---

## Phase 2: Steering Documents参照

Working Documents生成前に、以下のSteering Documentsを読み込みます:

```
1. docs/steering/PRODUCT.md（プロダクトビジョン）
2. docs/steering/FEATURES.md（関連機能の確認）
3. docs/steering/UBIQUITOUS_LANGUAGE.md（用語統一）
4. docs/steering/GUIDELINES.md（実装パターン）
```

**目的**: Issueの文脈をプロジェクト全体のコンテキストで理解する

---

## Phase 3: Serena MCP調査

関連コードをSerena MCPで調査します（探索のみ、編集禁止）:

### 調査手順

1. **パターン検索**: `search_for_pattern` でキーワード検索
   - Issueのタイトル・本文からキーワード抽出
   - 例: "ドリップガイド" → `search_for_pattern "DripGuide|drip-guide"`

2. **シンボル構造把握**: `get_symbols_overview` でファイル構造確認
   - 関連ファイルの関数・型・エクスポートを把握

3. **シンボル詳細確認**: `find_symbol` で具体的な実装確認
   - 修正対象のコンポーネント・関数を特定

4. **影響範囲確認**: `find_referencing_symbols` で依存関係追跡
   - 修正による影響範囲を特定

### 調査深度の判断

| Issueタイプ | 調査深度 | 理由 |
|------------|---------|------|
| bug | 詳細 | 根本原因特定が必須 |
| refactor | 詳細 | 影響範囲の完全把握が必須 |
| enhancement | 中程度 | 既存パターンの参照が主 |
| docs | 軽微 | コード調査は最小限 |

### Serena MCPの使い方

- **探索のみ**: `search_for_pattern`, `get_symbols_overview`, `find_symbol`, `find_referencing_symbols`
- **編集禁止**: `replace_symbol_body`, `insert_*`, `rename_symbol` は使用しない
- **理由**: 編集はClaude Code標準ツール（Edit/Write）の方が安定

---

## Phase 4: Working Documents生成

`docs/working/{YYYYMMDD}_{Issue番号}_{タイトル}/` ディレクトリを作成し、以下の4ファイルを生成します。

### ディレクトリ命名規則

```
docs/working/20260205_123_ドリップガイド4-6メソッド実装/
```

- `YYYYMMDD`: 生成日（ソート用）
- `Issue番号`: GitHub Issue番号
- `タイトル`: Issueタイトル（日本語可、50文字以内）

---

### 1. requirement.md（要件定義）

```markdown
# 要件定義

**Issue**: #123
**作成日**: 2026-02-05
**ラベル**: enhancement

## ユーザーストーリー

ユーザー「[セリフ形式で記述]」
アプリ「[期待する動作]」

## 要件一覧

### 必須要件
- [ ] 要件1 - 具体的な動作
- [ ] 要件2 - 具体的な動作

### オプション要件
- [ ] 要件3 - あれば望ましい動作

## 非機能要件
- パフォーマンス: [目標値]
- アクセシビリティ: [対応内容]
- モバイル対応: [レスポンシブ要件]

## 受け入れ基準
- [ ] 基準1
- [ ] 基準2

## 参照
- 関連Issue: #xxx
- Steering Documents: FEATURES.md「[機能名]」
```

**生成ロジック**:
- Issue本文の「要件」セクションをパース
- Steering Documents（FEATURES.md）から関連機能を参照
- AIが80%ドラフト生成、ユーザーが確認・修正

---

### 2. design.md（設計書）

```markdown
# 設計書

## アーキテクチャ概要

[システム構成図 - Mermaid等]

## 実装方針

### 変更対象ファイル
- `app/drip-guide/page.tsx` - [変更内容]
- `components/drip-guide/RecipeCard.tsx` - [変更内容]

### 新規作成ファイル
- `lib/drip-guide/46method.ts` - [役割]

## データモデル

### Firestoreスキーマ
```typescript
interface DripRecipe {
  id: string;
  name: string;
  ...
}
```

## UI設計

### 画面遷移
[Mermaid図]

### コンポーネント構成
- `RecipeCard` (既存) → [変更内容]
- `MethodDialog` (新規) → [役割]

## API設計

### 関数シグネチャ
```typescript
function calculate46Method(servings: number, ...): DripRecipe
```

## 依存関係

### 新規依存
- なし

### 影響範囲
- `drip-guide/` 配下のみ
- 他機能への影響なし

## UI実装ルール確認

- ✅ 共通コンポーネント使用: [使用するコンポーネント]
- ✅ クリスマスモード対応: `isChristmasMode` prop
- ✅ 配色: [参照する配色スキーム]

## 禁止事項チェック

- ❌ 独自CSS生成しない
- ❌ 新しい状態管理ライブラリ導入しない
- ❌ 設計方針を変更しない（変更が必要な場合は相談）

## ADR（この設計の決定事項）

### Decision-001: [タイトル]
- **理由**: [理由]
- **影響**: [影響]
```

**生成ロジック**:
- Serena MCP調査結果から変更対象ファイルを特定
- Steering Documents（GUIDELINES.md, TECH_SPEC.md）から実装パターンを参照
- FEATURES.mdの「禁止事項」を反映
- 既存コードのパターンを踏襲

---

### 3. tasklist.md（タスクリスト）

```markdown
# タスクリスト

## フェーズ1: データモデル実装
- [ ] `lib/drip-guide/46method.ts` を作成
  - [ ] 基本スケーリング関数（豆量・湯量計算）
  - [ ] 味わい調整ロジック
  - [ ] 濃度調整ロジック
  - [ ] 注湯スケジュール生成関数

## フェーズ2: UI実装
- [ ] `components/drip-guide/MethodDialog.tsx` を作成
  - [ ] 人前セレクト（1〜8）
  - [ ] 味わいセレクト（ラジオボタン）
  - [ ] 濃度セレクト（ラジオボタン）
  - [ ] プレビュー表示
  - [ ] 「ガイド開始」ボタン

- [ ] `app/drip-guide/page.tsx` を修正
  - [ ] 4:6メソッドカードを追加
  - [ ] 「ガイド開始」押下でMethodDialog表示

## フェーズ3: ガイド実行
- [ ] `app/drip-guide/run/page.tsx` を修正
  - [ ] 4:6メソッドのプリセット受け取り
  - [ ] 既存のガイド機能で実行

## フェーズ4: テスト
- [ ] ユニットテスト: `lib/drip-guide/46method.test.ts`
- [ ] 統合テスト: `components/drip-guide/MethodDialog.test.tsx`

## 依存関係
- フェーズ1 → フェーズ2 → フェーズ3 → フェーズ4（順次実行）

## 見積もり
- フェーズ1: 1時間
- フェーズ2: 2時間
- フェーズ3: 30分
- フェーズ4: 1時間
- **合計**: 4.5時間
```

**生成ロジック**:
- design.md の「変更対象ファイル」「新規作成ファイル」から自動生成
- GUIDELINES.md の「実装フロー」（型定義→ロジック→UI→テスト）に従う
- 依存関係を明示（フェーズ間のブロック）

---

### 4. testing.md（テスト計画）

```markdown
# テスト計画

## テスト戦略

### ユニットテスト（Vitest）
- `lib/drip-guide/46method.test.ts`
  - 基本スケーリング計算の正確性
  - 味わい調整の境界値テスト
  - 濃度調整の境界値テスト
  - 異常値処理（人前0, 負数等）

### 統合テスト（Testing Library）
- `components/drip-guide/MethodDialog.test.tsx`
  - UI操作シナリオ（セレクト変更→プレビュー更新）
  - プレビュー表示の正確性
  - 「ガイド開始」ボタン押下時の挙動

### E2Eテスト（手動）
- Chrome DevTools MCP でスクリーンショット確認
  - モバイル表示
  - デスクトップ表示
  - クリスマスモード ON/OFF

## テストケース

### ユニットテスト: calculate46Method

| テストケース | 入力 | 期待出力 |
|-------------|-----|---------|
| 1人前・ベーシック・薄く | servings=1, taste=0, strength=0 | 豆10g, 湯150g, 5投 |
| 2人前・より甘く・より濃く | servings=2, taste=1, strength=1 | 豆20g, 湯300g, ... |
| 境界値: 0人前 | servings=0 | Error throw |
| 境界値: 9人前 | servings=9 | Error throw（1〜8のみ） |

### 統合テスト: MethodDialog

| テストケース | 操作 | 期待結果 |
|-------------|-----|---------|
| デフォルト表示 | ダイアログ表示 | 人前=1, 味わい=ベーシック, 濃度=薄く |
| 人前変更 | 人前を3に変更 | プレビューの豆量・湯量が更新 |
| ガイド開始 | ボタン押下 | `/drip-guide/run` へ遷移 |

## カバレッジ目標
- `lib/drip-guide/`: 90%以上
- `components/drip-guide/`: 85%以上

## テスト実行コマンド
```bash
npm run test -- --coverage
```

## 非機能テスト
- パフォーマンス: 計算処理は100ms以内
- アクセシビリティ: キーボード操作可能
- モバイル対応: 320px幅でも表示崩れなし
```

**生成ロジック**:
- tasklist.md のタスクから自動生成
- GUIDELINES.md の「テスト戦略」を参照
- 境界値テスト、異常系テストを自動提案

---

## Phase 5: ユーザー確認

生成されたWorking Documentsをユーザーに提示し、以下を確認します:

### 確認内容
1. **requirement.md**: 要件が正しく理解されているか
2. **design.md**: 実装方針が適切か
3. **tasklist.md**: タスク分割・見積もりが妥当か
4. **testing.md**: テスト計画が十分か

### フィードバック対応
- **修正依頼**: AIが該当ファイルを修正 → 再度確認
- **OK**: fix-issue の Phase 3（探索）へ進む

---

## 注意事項

### Serena MCPの使い方
- **探索のみ**: `get_symbols_overview`, `find_symbol`, `find_referencing_symbols`, `search_for_pattern`
- **編集禁止**: `replace_symbol_body`, `insert_*`, `rename_symbol` は使用しない
- 理由: 編集はClaude Code標準ツールの方が安定

### Working Documentsの更新
- 実装中に逐次更新（設計変更、タスク完了）
- PR完了後も削除しない（Git保管で過去の設計判断を記録）

### EnterPlanModeとの使い分け
- **Working Documents**: 永続的な設計メモ、Issueスコープ
- **EnterPlanMode**: 一時的な詳細計画、複雑な実装の事前検討
- 併用推奨: Working生成後、EnterPlanModeで詳細計画

---

## 実行例

```bash
# 1. Issue作成
gh issue create --title "feat: ドリップガイドに4:6メソッドを追加" --label "enhancement"

# 2. Working Documents自動生成
/create-spec 123

# 3. 生成されたドキュメントを確認
ls docs/working/20260205_123_ドリップガイド4-6メソッド実装/
# → requirement.md, design.md, tasklist.md, testing.md

# 4. /fix-issue で実装開始
/fix-issue 123
```

---

## 参照

- **Steering Documents**: `docs/steering/`
- **実装計画**: `C:\Users\kensa\.claude\plans\cryptic-forging-charm.md`
- **Planエージェント詳細出力**: agent a921d18
