---
name: test-and-fix
description: "テスト実行と失敗時の自動修復ループ。テストを実行し、失敗があれば原因を分析して修正を試みる。トリガー: /test-and-fix, テスト修復, CI修復"
user-invocable: true
allowed-tools: Read, Edit, Bash, Grep, Glob
model: sonnet
---

# テスト実行 & 自動修復

テストを実行し、失敗した場合は原因を分析して自動修復を試みます。最大3回のループで問題解決を目指します。

## テストコマンドの自動検出

プロジェクトの構成ファイルから適切なテストコマンドを検出:

| ファイル | テストコマンド |
|---------|---------------|
| package.json | `npm test` または `npm run test` |
| go.mod | `go test ./...` |
| Cargo.toml | `cargo test` |
| pyproject.toml / setup.py | `pytest` または `python -m pytest` |
| Gemfile | `bundle exec rspec` |
| Makefile (test target) | `make test` |

## 実行フロー

```
┌─────────────────────────────────────┐
│ 1. テストコマンドを検出             │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 2. テストを実行                     │
└─────────────────┬───────────────────┘
                  ▼
          ┌───────────────┐
          │ テスト成功？  │
          └───────┬───────┘
         Yes      │      No
          │       │       │
          ▼       │       ▼
      ┌───────┐   │   ┌─────────────────────────────────┐
      │ 完了  │   │   │ 3. エラーメッセージを解析       │
      └───────┘   │   └─────────────────┬───────────────┘
                  │                     ▼
                  │   ┌─────────────────────────────────┐
                  │   │ 4. 関連ファイルを特定           │
                  │   └─────────────────┬───────────────┘
                  │                     ▼
                  │   ┌─────────────────────────────────┐
                  │   │ 5. 修正を適用                   │
                  │   └─────────────────┬───────────────┘
                  │                     ▼
                  │         ┌───────────────────┐
                  │         │ ループ回数 < 3?   │
                  │         └─────────┬─────────┘
                  │                Yes │ No
                  │                   │  │
                  │                   ▼  ▼
                  └───────────────────┘  失敗レポート
```

## エラー解析パターン

### TypeScript / JavaScript
```
# 型エラー
TS2322: Type 'X' is not assignable to type 'Y'
→ 型定義の修正

# 未定義エラー
Cannot find name 'X'
→ import追加 or 変数定義

# プロパティアクセス
Property 'X' does not exist on type 'Y'
→ 型拡張 or オプショナルチェーン
```

### Go
```
# 未定義エラー
undefined: X
→ import追加 or 宣言

# 型エラー
cannot use X (type A) as type B
→ 型変換 or インターフェース実装
```

### Python
```
# Import エラー
ModuleNotFoundError: No module named 'X'
→ import修正 or 依存追加

# 属性エラー
AttributeError: 'X' object has no attribute 'Y'
→ メソッド/属性の追加
```

## 出力形式

```markdown
## テスト修復レポート

### 実行環境
- **プロジェクト**: <project-name>
- **テストコマンド**: `npm test`
- **開始時刻**: YYYY-MM-DD HH:MM

---

### 修復ループ

#### ループ 1
**結果**: ❌ 5 tests failed

**エラー概要**:
- `src/api.test.ts`: TypeError - Cannot read property 'data' of undefined
- `src/handler.test.ts`: AssertionError - Expected 200 but got 500

**修正内容**:
1. `src/api.ts:45` - nullチェックを追加
2. `src/handler.ts:78` - エラーハンドリングを修正

---

#### ループ 2
**結果**: ❌ 2 tests failed

**エラー概要**:
- `src/handler.test.ts`: AssertionError - Expected 'success' but got 'error'

**修正内容**:
1. `src/handler.ts:92` - レスポンスステータスを修正

---

#### ループ 3
**結果**: ✅ All tests passed

---

### 最終結果

**ステータス**: ✅ 成功
**修復ループ**: 3回
**修正ファイル**:
- src/api.ts (1箇所)
- src/handler.ts (2箇所)

### 修正差分

```diff
// src/api.ts
- return response.data;
+ return response?.data ?? null;

// src/handler.ts
- throw error;
+ return { status: 'error', message: error.message };
```
```

## 制限事項

- **最大3回のループ**: 無限ループを防止
- **自動修正の範囲**:
  - 型エラー、nullチェック、import追加などの軽微な修正
  - ビジネスロジックの変更は行わない
- **テスト追加**: 既存テストの修復のみ、新規テスト作成は行わない

## 使用方法

```
/test-and-fix              # 自動検出したコマンドでテスト実行
/test-and-fix npm test     # 指定したコマンドでテスト実行
/test-and-fix --dry-run    # 修正内容の確認のみ（適用しない）
```

## 失敗時の対応

3回のループで解決できなかった場合:

1. 残りのエラーを詳細にレポート
2. 手動修正が必要な箇所を特定
3. 修正のヒントを提供
4. 関連ドキュメントへのリンクを提示
