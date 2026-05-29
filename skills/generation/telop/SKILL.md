---
name: telop
description: |
  SNS縦型動画（Reels/TikTok/Shorts）向けテロップ作成スキル。Remotion対応。
  Use when: (1) user says「テロップ作成」「字幕スタイル」「ショート動画の文字」,
  (2) user wants video text/subtitle styling,
  (3) user mentions「Reels」「TikTok」「Shorts」「縦型動画」.
  Do NOT use for: 動画編集全般（video-productionを使用）、
  アニメ制作（anime-productionを使用）。
---

# テロップスキル (Telop Skill)

SNS縦型動画（Reels/TikTok/Shorts）向けの高品質テロップ作成スキル。

## 概要

縦型ショート動画向けのテロップスタイルを提供します。
Remotionコンポーネントとスタイルガイドを含みます。

## 使用場面

- 縦型ショート動画のテロップを作成する時
- Instagram Reels、TikTok、YouTube Shortsの字幕を作成する時
- 動画編集でテロップのスタイルを決める時
- Remotionでテロップコンポーネントを実装する時

## テロップの種類

1. **フックテキスト** - 冒頭で注意を引く（ライム/イエロー、特大）
2. **ナレーションテロップ** - 話の内容を表示（白、中サイズ）
3. **強調テロップ** - 重要ポイント（オレンジ/レッド、大きめ）
4. **補足テロップ** - 追加情報（グレー、小さめ）

## 使用方法

```
/テロップ [動画の種類] [テロップ内容]
```

## 含まれるファイル

- `TelopComponents.tsx` - Remotionコンポーネント
- `instructions.md` - 詳細なスタイルガイド

## 関連スキル

- video-production
- anime-production
