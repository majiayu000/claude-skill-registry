---
name: integrating-storybook
description: >
  Storybook integration with spec.md. Auto-generates Stories from Component API.
  Triggers: storybook, stories, component api, props, argTypes, variants, csf3.
allowed-tools: [Read, Write, Glob, Grep]
---

# Storybook統合

## コアコンセプト

| コンセプト    | 説明                                       |
| ------------- | ------------------------------------------ |
| Component API | spec.mdで定義されたProps、Variants、States |
| CSF3          | Component Story Format 3 + autodocs        |
| 自動生成      | `/code`がspec.mdからStoriesを生成          |

## Component API場所

フロントエンドコンポーネント実装時にspec.mdへ追加。

| 内容                  | 説明                             |
| --------------------- | -------------------------------- |
| Propsインターフェース | TypeScriptインターフェース       |
| Variants              | スタイルオプション               |
| States                | default, hover, active, disabled |
| 使用例                | TSXコード                        |

## ワークフロー

| コマンド              | アクション                             |
| --------------------- | -------------------------------------- |
| `/think "Add Button"` | spec.mdにComponent APIセクションを追加 |
| `/code`               | specから`Button.stories.tsx`を生成     |

## 既存Storiesの処理

| オプション | アクション              |
| ---------- | ----------------------- |
| [O]        | 既存ファイルを上書き    |
| [S]        | スキップ - 既存を維持   |
| [M]        | マージ - diff表示、手動 |
| [D]        | diffのみ - 新規を追加   |

## 参照

| トピック      | ファイル                               |
| ------------- | -------------------------------------- |
| Component API | `references/component-api-template.md` |
| CSF3パターン  | `references/csf3-patterns.md`          |
