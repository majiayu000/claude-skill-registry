---
name: release-preview
description: 次回リリースに含まれる変更をプレビューする。「リリースプレビュー」「次のリリース」「リリース内容確認」と言われた場合に使用する。
disable-model-invocation: true
---

# リリースプレビュー

次回リリースに含まれる変更をプレビューします。

## 実行手順

以下のコマンドを順番に実行してください：

### 1. 現在の状態確認

```bash
git describe --tags --abbrev=0 2>/dev/null || echo "タグなし"
git branch --show-current
git status --short
```

### 2. 前回リリースからのコミット一覧

最新タグがある場合：
```bash
git log --oneline --no-merges $(git describe --tags --abbrev=0)..HEAD
```

タグがない場合：
```bash
git log --oneline --no-merges -20
```

### 3. CHANGELOG の Unreleased セクション確認

CHANGELOG.md の先頭部分を確認し、Unreleased セクションがあるか確認：

```bash
head -50 CHANGELOG.md
```

### 4. 変更の分類

コミット一覧から以下を分類して報告：

**リリースノートに含まれるもの：**
- `feat:` 新機能
- `fix:` バグ修正
- `BREAKING CHANGE:` 破壊的変更

**リリースノートに含まれないもの：**
- `docs:`, `test:`, `chore:`, `ci:`, `build:`, `refactor:`, `style:`, `perf:`

### 5. 推奨バージョンの提示

| 変更タイプ | 次のバージョン |
|-----------|---------------|
| BREAKING CHANGE あり | メジャーアップ（例: v1.x.x → v2.0.0） |
| feat: あり | マイナーアップ（例: v1.0.x → v1.1.0） |
| fix: のみ | パッチアップ（例: v1.0.0 → v1.0.1） |

### 6. 品質チェック

```bash
cargo fmt -- --check && cargo clippy --all-targets -- -D warnings && cargo test
```

## 次のステップ

リリースを実行する場合：

```bash
/release v<VERSION>
```
