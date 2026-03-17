---
name: naist-papers
description: arXivから論文を検索して要約する。Use when user says 「論文調べて」「arXivで{キーワード}を検索して」「最新の{テーマ}の論文は？」「{キーワード}の研究教えて」or similar paper search requests in #ai-<name> channels.
metadata:
  source: arxiv-watcher (ClawHub) + arXiv API
  requires:
    bins: [bash, curl, python3]
---

# naist-papers

ユーザーが任意のキーワードでarXivから論文を検索して要約する。

## 実行手順

### 1. クエリを抽出

ユーザーのメッセージからキーワードを抽出する（例: 「mind wandering の論文」→ `mind+wandering`）。

### 2. arXiv検索

```bash
# arxiv-watcher のスクリプトを使用
bash /Users/anicca/.openclaw/workspace/skills/arxiv-watcher/scripts/search_arxiv.sh "<query>" 5
```

XMLが返ってくるので、`<entry>` を解析して以下を取得:
- `<title>` — 論文タイトル
- `<id>` — arXivリンク
- `<summary>` — abstract
- `<author><name>` — 著者
- `<published>` — 公開日

### 3. Slack出力フォーマット

```
📄 arXiv検索: "{query}"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. *タイトル*
   著者名 et al. | 公開日
   https://arxiv.org/abs/XXXX.XXXXX

   要約: 3-4行で内容を日本語で説明

2. *タイトル*
   ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
計 N件ヒット（上位5件表示）
```

## 注意

- クエリはURLエンコードする（スペース→`+`）
- 結果が0件の場合は「該当なし。キーワードを変えてみて」と返す
- abstractは日本語で3-4行に要約する
