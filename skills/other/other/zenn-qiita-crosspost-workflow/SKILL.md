---
name: zenn-qiita-crosspost-workflow
description: "Use when cross-posting a Zenn article to Qiita. Automated conversion pipeline with platform-specific adaptations."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-11"
---
# Zenn-Qiita Cross-Post Workflow

**Extracted:** 2026-02-11
**Context:** Publishing technical articles to both Zenn and Qiita from a single source

## Problem

記事を Zenn と Qiita の両方に投稿する際、プラットフォーム固有の構文差異とリンク管理が煩雑になる。

## Solution

### ファイル構成

```
~/zenn-content/
├── articles/          # Zenn記事（source of truth）
│   └── ecc-journey-part2.md
├── scripts/
│   ├── publish.py     # Zenn→Qiita変換＆投稿CLI
│   ├── .env           # QIITA_ACCESS_TOKEN
│   └── .venv/         # Python依存（httpx, python-frontmatter）
└── package.json       # zenn-cli
```

### ワークフロー

```bash
# 1. Zenn記事を articles/ に作成（source of truth）
# 2. Qiitaクロスポスト（dry-run → 投稿）
cd ~/zenn-content/scripts
.venv/bin/python publish.py ../articles/ARTICLE.md --platform qiita --dry-run
.venv/bin/python publish.py ../articles/ARTICLE.md --platform qiita

# 3. Zennデプロイ（GitHub連携で自動公開）
git -C ~/zenn-content add articles/ARTICLE.md
git -C ~/zenn-content commit -m "feat: 記事タイトル"
git -C ~/zenn-content push origin main
```

### プラットフォーム差異（publish.pyが自動変換）

| Zenn | Qiita | 変換 |
|------|-------|------|
| `:::message` | `> ` (blockquote) | 自動 |
| `:::details title` | `<details><summary>` | 自動 |
| topics (frontmatter) | tags (API) | 自動 |

### 手動対応が必要な差異

| 項目 | Zenn | Qiita |
|------|------|-------|
| CTA | 「いいね」のみ | 「いいね」＋「ストック」 |
| 前回記事リンク | Zenn URL | Qiita URL |
| published状態 | frontmatter制御 | API `private` フラグ |

### クロスリンクの注意点

- 前回記事へのリンクは **公開済みプラットフォームのURL** を使う
- Zenn記事が `published: false` なら、Qiita URLにフォールバック
- `git remote -v` でGitHubユーザー名を確認し、モックURLを正しいものに差し替える

## When to Use

- ユーザーが「Zenn/Qiitaに投稿して」と依頼した時
- 新しい技術記事を複数プラットフォームに配信する時
- `~/zenn-content/` プロジェクトで作業する時
