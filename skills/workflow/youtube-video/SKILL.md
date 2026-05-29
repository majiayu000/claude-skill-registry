---
id: youtube-video-download
title: "YouTube動画のダウンロード"
description: "指定されたYouTube URLから資料や調査用動画を取得し、Codexで参照できるようにするAgent Skill。"
entryScript: "skills/youtube-video/run.js"
contexts:
  - Codex
tags:
  - youtube
  - download
  - python
---

## 目的

1. 依頼されたYouTubeリンクを`yt-dlp`などのCLIツールでダウンロードし、`artifacts/videos/`に保存する。
2. 取得した動画を分析し、必要に応じて他のSkillに渡す情報（例: トランスクリプト）をCollected Dataフォルダーに置く。

## 手順

1. **L1**: `skills/index.json`を通じて、このSkillのexistence, entry point, contextをCodexに知らせる。
2. **L2**: この`SKILL.md`を読み込ませ、期待される出力ディレクトリ、使うCLI、注意点（巨大ファイルや著作権）を伝える。
3. **L3**: `skills/youtube-video/run.js`を実行し、引数で受け取ったURLもしくは`stdin`から受け取ったURLを`artifacts/videos/`に保存するためのコマンド例をログに出力する。
4. 必要あれば`yt-dlp`コマンドを提示し、Codexに手動で実行させるか、別スクリプトに差し替えて自動化する。
