# Agent Memory

会話をまたいで知識を保存する永続的なメモリ空間。

**保存場所**: `.claude/skills/agent-memory/memories/`

---

## いつ使う？

### ユーザーが明示的に指示したとき
- 「記憶して」「覚えて」「メモして」
- 「〇〇について思い出して」「前回の〇〇は？」
- 「記憶一覧」「何を覚えてる？」

### プロアクティブに保存すべきとき
- 調査で見つけた重要な発見
- コードベースの非自明なパターン
- 複雑な問題の解決策
- アーキテクチャの決定事項
- 後で再開するための作業状態
- マーケティングで効果があった施策
- App Storeの審査で学んだこと

---

## フォルダ構造

kebab-case でカテゴリフォルダを作成。柔軟に運用。

```
memories/
├── app-development/       # アプリ開発関連
│   ├── daily-dhamma-learnings.md
│   └── ios-release-notes.md
├── marketing/             # マーケティング関連
│   ├── carousel-best-practices.md
│   └── viral-posts.md
├── project-decisions/     # プロジェクトの決定事項
│   └── tech-stack-choices.md
└── in-progress/           # 進行中の作業
    └── current-feature.md
```

---

## メモリファイルの書き方

### Frontmatter（必須）

```yaml
---
summary: 1-2行の要約（検索用に超重要）
created: YYYY-MM-DD
---
```

### Frontmatter（オプション）

```yaml
---
summary: 要約
created: 2025-01-15
updated: 2025-01-16
status: in-progress | resolved | blocked | abandoned
tags: [daily-dhamma, marketing, ios]
related: [another-memory.md]
---
```

### 本文の書き方

**再開できるように書く**：
- 何を決めたか
- なぜそう決めたか
- 現在の状態
- 次のステップ

```markdown
---
summary: Daily Dhammaのカルーセル投稿で効果があったパターン
created: 2025-01-15
tags: [daily-dhamma, marketing, instagram]
---

## 発見

縦長画像（4:5）で、最初のスライドに質問を入れると保存率が上がる。

## 効果があったパターン
1. 質問で始める（例：「心が疲れていませんか？」）
2. 3-5枚のスライド
3. 最後にCTA（「保存して後で読む」）

## 次に試すこと
- リール動画との組み合わせ
```

---

## 検索の仕方

### 1. カテゴリ一覧を見る
```bash
ls memories/
```

### 2. サマリーで検索（まずこれ）
```bash
rg "^summary:" memories/ --no-ignore --hidden
```

### 3. タグで検索
```bash
rg "tags:.*marketing" memories/ --no-ignore --hidden
```

### 4. キーワードで全文検索
```bash
rg "カルーセル" memories/ --no-ignore --hidden
```

---

## 操作

### 保存
1. 適切なカテゴリフォルダを選ぶ（なければ作る）
2. kebab-caseでファイル名をつける
3. frontmatterを書く（summaryは必須！）
4. 本文を書く

### メンテナンス
- 古くなった情報は更新
- 不要になったメモは削除
- 関連するメモは統合
- 必要に応じてカテゴリを再編成

---

## ガイドライン

1. **サマリーは命** - 検索で見つかるかどうかはサマリー次第
2. **再開できるように** - 1ヶ月後の自分が読んでもわかるように
3. **実用的に** - 全部記録するんじゃなくて、本当に役立つものだけ
4. **最新に保つ** - 古い情報は害になる
