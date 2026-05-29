---
name: content-creator
description: Generates daily development reports and converts them into social media content for X, TikTok, and note.com. Use when the user asks to write a daily report, summarize today's work, create SNS posts, or convert development logs into shareable content.
---

# Content Creator

日報の自動生成とSNSコンテンツへの変換を行うスキル。

---

## いつ使う？

### 自動（Hook経由）
- セッション終了時 → 日報を自動保存

### 手動
- 「日報書いて」
- 「今日の作業まとめて」
- 「X用に変換して」
- 「TikTok台本作って」
- 「カルーセル作って」
- 「Build in Public投稿作って」

---

## 日報フォーマット

保存先: `.claude/skills/agent-memory/memories/daily-logs/YYYY-MM-DD.md`

```markdown
---
summary: [日付]の作業ログ
created: YYYY-MM-DD
tags: [daily-log, build-in-public]
---

## やったこと
- [具体的なタスク1]
- [具体的なタスク2]

## 学び・発見
- [技術的な学び]
- [プロセスの改善点]

## 課題・ブロッカー
- [あれば記載]

## 明日やること
- [次のタスク]
```

---

## SNS変換テンプレート

### X (Twitter) - 280文字以内

```
[フック：1行で注目を引く]

[本題：2-3行で内容を伝える]

[CTA or ハッシュタグ]

#BuildInPublic #IndieHacker #[関連タグ]
```

**例:**
```
🔨 Day 15: AIに「記憶して」って言うだけで覚えてくれる仕組みを作った

- 過去の失敗を繰り返さない
- 成功パターンを蓄積
- 作業の中断・再開がスムーズに

#BuildInPublic #IndieHacker #AIツール
```

### TikTok / Reels 台本

```
【フック】0-3秒
[視聴者の注意を引く質問や衝撃的な事実]

【本題】3-45秒
[ステップバイステップで説明]
1. [ステップ1]
2. [ステップ2]
3. [ステップ3]

【CTA】45-60秒
[フォロー、コメント、シェアを促す]
```

### Instagram カルーセル (5枚構成)

```
【1枚目】フック
- 質問形式が効果的
- 例：「AIに記憶させる方法、知ってる？」

【2枚目】問題提起
- なぜこれが必要か

【3枚目】解決策1
- 具体的なステップ

【4枚目】解決策2
- さらに具体的に

【5枚目】CTA
- 「保存して後で試してみて」
- 「フォローで最新情報をゲット」
```

---

## 変換のルール

1. **フックが命** - 最初の1行で止まらせる
2. **具体的に** - 抽象的な表現を避ける
3. **数字を使う** - 「Day 15」「3ステップ」
4. **絵文字は最小限** - 🔨 とかワンポイント
5. **ハッシュタグは3-5個** - 多すぎない

---

## ワークフロー

```
1. セッション終了 or 「日報書いて」
   ↓
2. daily-logs/YYYY-MM-DD.md に保存
   ↓
3. 「X用に変換して」
   ↓
4. テンプレートに沿って生成
   ↓
5. ユーザーが投稿 (or Composio経由で自動投稿)
```

---

## Build in Public のコツ

1. **毎日投稿** - 継続が信頼を生む
2. **失敗も共有** - 完璧より本物
3. **数字で見せる** - DAU、売上、ダウンロード数
4. **Before/After** - 変化を可視化
5. **感情を入れる** - 喜び、苦労、学び
