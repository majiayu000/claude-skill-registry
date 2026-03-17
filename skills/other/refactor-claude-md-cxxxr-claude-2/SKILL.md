---
name: refactor-claude-md
description: CLAUDE.mdをベストプラクティスに基づいてリファクタリング
user-invocable: true
---

# CLAUDE.md Refactoring Guide

Boris Cherny（Claude Code作者）の原則に基づくCLAUDE.mdリファクタリングガイド。

## Core Principles

### 1. サイズ制限
- **目標: ~2.5kトークン以下**
- 長すぎるとClaudeが重要な情報を見落とす
- 詳細なルールは `.claude/rules/` に分離

### 2. 間違いを文書化
- 「Claudeが間違えるたびにCLAUDE.mdに追加する」
- `## よくある間違い` セクションを設ける
- 具体的なエラーと正しい方法を記載

### 3. 検証手段を提供
- 「検証手段を与えると品質が2-3倍向上する」
- `## 検証コマンド` セクションを設ける
- テスト実行、ビルド確認などのコマンドを記載

## Recommended Structure

```markdown
# Project Name

簡潔な説明（1-2行）

## Quick Reference

| Key | Value |
|-----|-------|
| ... | ...   |

## 技術スタック

- **Language**: ...
- **Framework**: ...

## 検証コマンド

```
# テスト実行
command here

# ビルド確認
command here
```

## よくある間違い

- **問題1**: 説明と正しい方法
- **問題2**: 説明と正しい方法

## コード規約

`.claude/rules/` に配置（自動読み込み）
```

## Anti-patterns

### 避けるべきもの

1. **@file参照の多用**
   - 機能が不安定
   - 直接必要な情報を記載するか、`.claude/rules/`に分離

2. **一般的なプログラミング知識**
   - Claudeは既に知っている
   - プロジェクト固有の情報のみ記載

3. **長大なディレクトリ構造**
   - 必要な場合のみ最小限に
   - Claudeはコードベースを探索できる

4. **古いドキュメントへの参照**
   - 混乱の原因になる
   - 参照する場合は最新のものを確認

## Modularization Strategy

### .claude/rules/ の活用

詳細なルールは自動読み込みされるルールファイルに分離:

```
.claude/rules/
├── testing.md       # テストガイド
├── controllers.md   # コントローラー規約
├── routes.md        # ルーティング規約
├── errors.md        # エラー定義規約
├── models.md        # モデル定義規約
└── {domain}.md      # その他ドメイン固有ルール
```

**CLAUDE.md**: プロジェクト概要、クイックリファレンス、検証コマンド、よくある間違い
**rules/**: 詳細な実装規約、パターン、アンチパターン

## Refactoring Checklist

リファクタリング時の確認項目:

- [ ] トークン数が2.5k以下か
- [ ] 「よくある間違い」セクションがあるか
- [ ] 「検証コマンド」セクションがあるか
- [ ] 詳細ルールは `.claude/rules/` に分離されているか
- [ ] @file参照は最小限か（または使用していないか）
- [ ] プロジェクト固有の情報のみ含まれているか
- [ ] 参照しているドキュメントは最新か
