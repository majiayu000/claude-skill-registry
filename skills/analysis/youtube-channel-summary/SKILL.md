---
name: youtube-channel-summary
description: |
  YouTubeチャンネルの動画を分析し、要約を生成するスキル。
  Use when: (1) user says「チャンネル分析」「YouTube分析」「競合チャンネル調査」,
  (2) user wants to analyze YouTube channel content patterns,
  (3) user mentions「動画トレンド」「コンテンツ戦略」.
  Do NOT use for: 単発の動画ダウンロード（video-downloadを使用）、
  サムネイル作成（youtube-thumbnailを使用）。
---

# YouTube Channel Summary Skill

YouTubeチャンネルの動画を分析し、要約を生成するスキル。

## 概要

指定されたYouTubeチャンネルの動画コンテンツを分析し、
主要なテーマ、トピック、コンテンツパターンを要約します。

## 使用場面

- チャンネル分析が必要な時
- 競合分析を行う時
- コンテンツ戦略を立てる時
- 動画のトレンドを把握したい時

## 機能

- チャンネル動画のリスト取得
- 動画タイトル・説明の分析
- 主要トピックの抽出
- コンテンツパターンの特定

## 使用方法

```
/youtube_channel_summary [チャンネルURL or チャンネルID]
```

## 関連ツール

- youtube MCP server
- video-download skill
