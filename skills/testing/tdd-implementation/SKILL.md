---
name: tdd-implementation
description: container-use環境内でのTDD実装フロー（Red→Green→Refactor）、テスト項目書の活用、DBマイグレーションテストを定義
---

# TDD実装フロー (Red -> Green -> Refactor)

> **参照元**: implement-issues.md から分離されたTDD実装ガイド

---

## 概要

**全てcontainer-use環境内で実行**する。

---

## 0. テスト項目書の参照（推奨）

TDD開始前に、詳細設計フェーズで作成されたテスト項目書を参照する。

**テスト項目書活用のメリット**:
- 詳細設計フェーズで網羅性が検証済み
- 境界条件・エラーケースが明確
- TDDのRed→Greenがスムーズに

**テスト項目書がない場合**:
- 設計書から必要なテストケースを推論
- 基本的なハッピーパス + エラーケースを実装

---

## 🔴 Red: テスト実装

### Test Log Compression (ログ圧縮)

> **Token最適化**: テスト実行ログは膨大になりがち。成功ログはノイズ。
> 常に**失敗したテストのみ**を出力するか、出力をフィルタリングする。

```bash
# npm (Jest) の場合: --silent または failureのみgrep
npm test -- --silent --testPathPattern='feature-name'
# または
npm test 2>&1 | grep -A 5 "FAIL"

# Cargo (Rust) の場合: --quiet
cargo test --quiet
```

```python
# テスト実行 (失敗を確認)
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    # 冗長な出力を抑制
    command="npm test -- --silent --testPathPattern='feature-name'"
)
```

---

## 🟢 Green: 最小実装

```python
# ファイル編集
container-use_environment_file_write(
    environment_id=env_id,
    environment_source="/path/to/repo",
    target_file="src/feature.ts",
    contents="// implementation"
)

# テスト実行 (成功を確認)
container-use_environment_run_cmd(...)
```

---

## 🔵 Refactor: 整理

```python
# Lint & 型チェック
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    command="npm run lint -- --fix && npm run type-check"
)
```

---

## DBマイグレーションのテスト (DB関連Issue)

```python
# マイグレーション実行
container-use_environment_run_cmd(command="npx flyway migrate")

# ロールバックテスト
container-use_environment_run_cmd(command="npx flyway undo")

# 再マイグレーション
container-use_environment_run_cmd(command="npx flyway migrate")
```

---

## 次のステップ

| 状況 | 対応 |
|------|------|
| 設計の矛盾が見つかった | `/request-design-fix` を実行 |
| 他領域への影響がある | [申し送り処理ガイド](./handover-process.md) に従う |
| 実装完了 | 自己チェック → 品質レビューへ |
