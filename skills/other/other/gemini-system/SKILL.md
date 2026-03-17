---
name: gemini-system
description: |
  Gemini CLI leverages 1M context for three roles: codebase analysis,
  external research (Google Search grounding), and multimodal file reading.
  MUST use when PDF, video, audio, or image files need content extraction.
  Also use for large-scale codebase understanding and external research/survey.
  Auto-triggers: file extensions .pdf, .mp4, .mov, .mp3, .wav, .m4a.
  Planning/design → use Codex instead.
metadata:
  short-description: Gemini CLI — 1M context analysis, research & multimodal
---

# Gemini System — Analysis, Research & Multimodal

**Gemini CLI は 1M context を活用し、大規模分析・リサーチ・マルチモーダル読取を担当する。**

> **詳細ルール**: `.claude/rules/gemini-delegation.md`

## Gemini の3つの役割

### 1. コードベース・リポジトリ理解

Gemini の 1M context でプロジェクト全体を分析する（Claude の 200K では収まらない場合）。

```bash
# プロジェクト構造の分析
gemini -p "Analyze this codebase: directory structure, key modules, patterns, dependencies, and architecture" 2>/dev/null

# 特定ファイルの詳細分析
gemini -p "Analyze this code: purpose, patterns, dependencies" < /path/to/file 2>/dev/null
```

### 2. 外部リサーチ・サーベイ

Gemini の Google Search grounding で最新情報を調査する。

```bash
# ライブラリ調査
gemini -p "Research: {library}. Latest version, features, constraints, best practices, pitfalls" 2>/dev/null

# ベストプラクティス調査
gemini -p "Research best practices for {topic}. Latest recommendations, patterns, anti-patterns" 2>/dev/null

# 技術比較
gemini -p "Compare {A} vs {B} for {use case}. Pros, cons, performance, community" 2>/dev/null
```

### 3. マルチモーダルファイル読取

PDF、動画、音声、画像ファイルの内容を抽出する。

```bash
# PDF
gemini -p "Extract: {what to extract}" < /path/to/file.pdf 2>/dev/null

# Video
gemini -p "Summarize: key concepts, timestamps" < /path/to/video.mp4 2>/dev/null

# Audio
gemini -p "Transcribe and summarize: decisions, action items" < /path/to/audio.mp3 2>/dev/null

# Image (diagrams, charts)
gemini -p "Analyze: components, relationships, data flow" < /path/to/diagram.png 2>/dev/null
```

| 対象 | 拡張子 |
|------|--------|
| PDF | `.pdf` |
| 動画 | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` |
| 音声 | `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` |
| 画像（高度分析） | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg` |

> スクリーンショットの単純確認は Claude の Read ツールで直接可能。

## Auto-Trigger（自動発動）

マルチモーダルファイルがタスクに登場した時点で、ユーザー指示を待たず自動で Gemini に渡す。

## Gemini を使わないこと

| タスク | 正しい担当 |
|--------|-----------|
| 設計・計画 | **Codex** |
| デバッグ | **Codex** |
| コード実装 | **Claude / サブエージェント** |

## How to Use

### Subagent Pattern（出力が大きい場合）

```
Task tool parameters:
- subagent_type: "gemini-explore"
- prompt: |
    {task description}

    gemini -p "{prompt}" 2>/dev/null

    Save results to .claude/docs/research/{topic}.md
    Return CONCISE summary (5-7 bullet points).
```

### Direct Call（短い抽出の場合）

```bash
gemini -p "{what to extract/research}" 2>/dev/null
```

## Language Protocol

1. Ask Gemini in **English**
2. Receive response in **English**
3. Report to user in **Japanese**
