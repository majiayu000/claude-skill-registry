# Gemini Image Generator (NanoBanana統合)

## Description
Google Gemini (NanoBanana) を使用した統合画像生成スキル。
YouTubeサムネイル、図解、一般画像生成を一元化。

## Capabilities

### 1. 一般画像生成
- テキストプロンプトからの画像生成
- スタイル指定（リアル、アニメ、イラスト等）
- アスペクト比指定

### 2. YouTubeサムネイル
- 4パターン自動生成
- 文字配置最適化
- クリック率最大化デザイン

### 3. 図解・解説画像
- 6種類の図解スタイル
  - フローチャート
  - 比較表
  - プロセス図
  - 階層図
  - タイムライン
  - インフォグラフィック

### 4. 画像編集
- 背景変更
- フェイススワップ
- スタイル転送
- キャラクター一貫性維持

## Usage

```
/gemini-image-generator [mode] [prompt]

Modes:
  generate   - 一般画像生成
  thumbnail  - YouTubeサムネイル
  diagram    - 図解生成
  edit       - 画像編集
```

## Examples

```
# YouTubeサムネイル
/gemini-image-generator thumbnail "驚きの収益化方法"

# 図解生成
/gemini-image-generator diagram flowchart "ユーザー登録フロー"

# 一般画像
/gemini-image-generator generate "プロフェッショナルなビジネスミーティング"
```

## Integration
- nanobanana-prompts スキルと連携可能
- 自動プロンプト最適化
