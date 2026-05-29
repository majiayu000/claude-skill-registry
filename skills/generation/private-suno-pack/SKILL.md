---
name: suno-pack
description: 分析ファイルからSunoパック（style, lyrics, image_prompt）を生成。Suno AI用のプロンプトセットを作成する。
allowed-tools: Read Write
---

# Suno Pack Generator

分析ファイルからSuno AI用のプロンプトセットを生成します。

## 入力

分析ファイルのslug

例: `yoasobi_idol`

## 手順

### 1. ナレッジを読む

以下を読んで参照:
```
Read: /Users/takish/Development/music-factory/prompts/suno-vocabulary.md
Read: /Users/takish/Development/music-factory/prompts/suno-structure.md
```

### 2. 分析ファイルを読む
```
Read: /Users/takish/Development/music-factory/data/analysis/{slug}.md
```

分析ファイルから以下を抽出:
- テーマ、キーワード、視点
- 曲構成（セクション順）
- ジャンル、楽器構成
- 感情表現のスタイル

### 3. タイトルを生成

分析の「概念キーワード」「曲の本質」から、**元の曲とは異なる新しいタイトル**を生成。

保存先: `/Users/takish/Development/music-factory/data/outputs/{slug}/title.md`

### 4. スタイルを生成

`suno-vocabulary.md` の表現のみを使って、1000文字以内でスタイルプロンプトを生成。

**含める要素:**
- Genre: 分析のジャンル
- Style: 分析の特徴・設計
- Tempo: BPM
- Harmony: Key、コード進行の特徴
- Structure: セクション構成
- Arrangement: 楽器構成、密度設計
- Lyrics: 言語、視点、言語密度

保存先: `/Users/takish/Development/music-factory/data/outputs/{slug}/suno_style.md`

### 5. 歌詞を書く

分析ファイルの内容をもとに、**実際の歌詞**を書く。

**フォーマット:**
```
[Intro]
(instrumental)

[Verse 1]
(softly)
実際の歌詞をここに
4-6行

[Pre-Chorus]
(building up)
2-4行

[Chorus]
(powerfully)
キャッチーなフック
4-6行

[Verse 2]
(building)
4-6行

[Bridge]
(perspective shift)
視点を変えた歌詞
2-4行

[Final Chorus]
(explosive chorus)
最も感情的な歌詞
4-6行

[Outro]
(fade out)
```

**歌詞のルール:**
- 分析のテーマ・キーワードを反映
- 視点（一人称など）を守る
- 言語密度（高=早口、低=ゆったり）に合わせた行数
- 直接的な感情語を避け、イメージで表現
- サビは繰り返し可能なキャッチーなフレーズ

保存先: `/Users/takish/Development/music-factory/data/outputs/{slug}/suno_lyrics.md`

### 6. 画像プロンプトを生成

YouTube用サムネイル画像のプロンプトを生成。

**要素:**
- 曲の雰囲気を視覚化
- アーティスティックなスタイル
- 色使い、構図の指定

保存先: `/Users/takish/Development/music-factory/data/outputs/{slug}/image_prompt.md`

### 7. 完了報告

生成されたファイル一覧を報告:
- `title.md` - タイトル
- `suno_style.md` - Sunoスタイルプロンプト
- `suno_lyrics.md` - 歌詞
- `image_prompt.md` - 画像生成プロンプト
