---
name: tech-blog
description: Zenn向けテックブログ記事の作成支援。プロジェクト紹介、技術解説、TIL/学習記録など様々な記事タイプに対応。トリガー: (1) ブログを書いて、(2) 記事を作成、(3) Zenn記事、(4) 技術記事、(5) /tech-blog
---

# Tech Blog (Zenn)

Zenn 向けテックブログ記事を作成する。

## 記事タイプ

| タイプ | 用途 | emoji 例 |
|--------|------|----------|
| project | 自作ツール/プロジェクト紹介 | 🛠️ 🚀 |
| tutorial | 技術解説/ハウツー | 📝 📚 |
| til | 今日学んだこと/ハマりポイント | 💡 🔍 |

## ワークフロー

1. **タイプ判定**: ユーザーの要望から記事タイプを判定
2. **情報収集**: 必要に応じてコードベースを調査
3. **構成決定**: references/templates.md のテンプレートを参照
4. **執筆**: Zenn frontmatter 付きで出力
5. **出力**: `articles/<slug>.md` に保存

## Zenn Frontmatter

```yaml
---
title: "記事タイトル"
emoji: "🎯"
type: "tech"  # tech or idea
topics: ["topic1", "topic2"]  # 最大5つ
published: false
---
```

## 執筆ガイドライン

- **見出し**: h2 (##) から開始、h1 は使わない
- **コード**: 言語指定付きコードブロック、diff 表記活用
- **長さ**: 1500-3000字目安（読了5-10分）
- **トーン**: 技術的かつ親しみやすく、断定的に書く
- **構成**: 結論ファースト、背景→課題→解決→まとめ

## リファレンス

- **テンプレート**: [references/templates.md](references/templates.md) - 記事タイプ別の構成テンプレート
