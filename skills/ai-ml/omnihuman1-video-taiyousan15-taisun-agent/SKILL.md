# OmniHuman1 AIアバター動画制作ガイド

## 概要

| 項目 | 内容 |
|------|------|
| ツール | OmniHuman1 / OmniHuman 1.5 |
| 開発元 | ByteDance (TikTok親会社) |
| 公式サイト | https://www.omnihuman1.org/ja |
| 用途 | AIアバターによるリップシンク動画生成 |
| 利用プラットフォーム | SousakuAI、Fal.ai、BytePlus |

> **注意**: このツールは指定された場合にのみ使用します。

---

## OmniHuman1とは

OmniHuman1は、**1枚の画像**と**1つの音声ファイル**から、リアルなリップシンク動画を自動生成するAIフレームワークです。

### 主な特徴

```
【完璧なリップシンク】
- 音声に合わせた正確な口の動き
- ほぼ違和感のないレベルの精度
- 音声の感情を理解した表情生成

【全身の動き対応】
- 顔だけでなく全身のジェスチャー
- 話し言葉に合わせた自然な動き
- 歌唱時のリズムに合わせた動作

【柔軟な入力対応】
- 実写人物写真
- アニメキャラクター
- イラスト
- あらゆるアスペクト比に対応
```

### バージョン比較

| バージョン | リリース | 特徴 |
|-----------|---------|------|
| OmniHuman-1 | 2025年2月 | 初期版、基本機能 |
| OmniHuman 1.5 | 2025年9月 | 口元の破綻改善、より自然なリップシンク |

---

## 利用可能なプラットフォーム

### 1. SousakuAI（推奨）

```
URL: https://sousakuai.jp/

【特徴】
- 日本語対応
- 初心者でも使いやすいUI
- 用意された音声テンプレートあり
- OmniHuman 1.5対応
```

### 2. Fal.ai

```
URL: https://fal.ai/

【特徴】
- API経由で利用可能
- 開発者向け
- 高速処理
```

### 3. BytePlus

```
URL: https://www.byteplus.com/

【特徴】
- 公式サービス
- エンタープライズ向け
- 大量処理対応
```

---

## 動画制作ワークフロー

### Step 1: 素材準備

#### 画像の準備

```
【推奨仕様】
- 形式: PNG or JPG
- 解像度: 1024x1024px以上推奨
- 内容: 人物の顔がはっきり見える画像

【画像の種類】
□ 実写ポートレート
□ アニメキャラクター
□ イラスト

【推奨構図】
- ポートレート（顔中心）: リップシンク最適
- ハーフボディ（上半身）: ジェスチャー含む
- フルボディ（全身）: 大きな動き含む

【注意点】
- 顔が正面を向いている
- 照明が均一
- 背景がシンプル
- 高解像度
```

#### 音声の準備

```
【推奨仕様】
- 形式: MP3 or WAV
- サンプルレート: 44.1kHz
- ビット深度: 16bit
- 長さ: 30秒〜7分程度

【音声の種類】
□ 話し言葉（VSL台本読み上げ）
□ 歌唱
□ 対話

【収録のコツ】
1. 静かな環境で録音
2. クリアな発声
3. 適度なペース（1分150-180字）
4. 感情を込める
5. ノイズを除去

【ツール推奨】
- 録音: iPhone ボイスメモ、Audacity
- 編集: Audacity（無料）、Adobe Audition
- AI音声: VOICEVOX、CoeFont、ElevenLabs
```

### Step 2: SousakuAIでの操作手順

```
【基本手順】

1. SousakuAIにログイン
   - アカウント作成（初回のみ）
   - クレジット購入

2. OmniHuman 1.5を選択
   - ツール一覧から選択
   - または検索

3. 画像をアップロード
   - 人物画像をドラッグ&ドロップ
   - または「ファイルを選択」

4. 音声をアップロード
   - 音声ファイルをアップロード
   - または用意されたテンプレートを使用

5. プロンプト入力（オプション）
   - カメラワーク指定
   - 動きの指定
   - 雰囲気の指定

6. 生成開始
   - 「生成」ボタンをクリック
   - 処理時間: 1-5分程度

7. ダウンロード
   - 完成動画をダウンロード
   - 形式: MP4
```

### Step 3: プロンプトのコツ

#### 基本プロンプト構造

```
【プロンプトテンプレート】

[カメラワーク], [人物の動き], [表情/雰囲気], [背景]

例:
"Medium shot, subtle hand gestures while speaking,
professional and confident expression,
blurred office background"
```

#### カメラワーク指定

```
【距離】
- Close-up: 顔のアップ
- Medium shot: 上半身
- Full shot: 全身

【角度】
- Front view: 正面
- Slight angle: 少し斜め
- Three-quarter view: 斜め45度

【動き】
- Static camera: 固定
- Slow zoom in: ゆっくりズームイン
- Gentle pan: ゆっくりパン
```

#### 動き・ジェスチャー指定

```
【手の動き】
- Subtle hand gestures: 控えめな手振り
- Expressive hand movements: 表現豊かな手振り
- Hands folded: 手を組む
- Pointing occasionally: 時々指差し

【体の動き】
- Slight head nods: 軽いうなずき
- Leaning forward slightly: 少し前傾
- Natural body sway: 自然な体の揺れ
```

#### 表情・雰囲気指定

```
【ビジネス/プロフェッショナル】
- Professional and confident
- Trustworthy and knowledgeable
- Calm and composed

【親しみやすさ】
- Friendly and approachable
- Warm and welcoming
- Enthusiastic and energetic

【教育/説明】
- Patient and clear
- Thoughtful and articulate
- Engaging and informative
```

#### プロンプト例（VSL用）

```
【信頼感を出したい場合】
"Medium shot, subtle hand gestures emphasizing key points,
professional and confident expression with occasional smile,
speaking directly to camera,
clean office background with soft lighting"

【親しみやすさを出したい場合】
"Close-up to medium shot, natural body movement,
warm and friendly expression,
casual but professional appearance,
soft focus background"

【緊急性を出したい場合】
"Dynamic medium shot, expressive hand movements,
serious but approachable expression,
slightly faster paced gestures,
neutral background with dramatic lighting"
```

---

## VSL動画制作フロー

### 全体フロー

```
[VSL台本] → [音声収録] → [アバター画像準備] → [OmniHuman1生成] → [動画編集] → [完成]
```

### Step 1: VSL台本作成

```
【7分VSL構成】
00:00-00:30  オープニング（フック）
00:30-02:00  問題提起
02:00-03:30  解決策の提示
03:30-05:00  商品紹介
05:00-06:00  価格・オファー
06:00-07:00  CTA

※詳細は kindle-line-vsl.md 参照
```

### Step 2: 音声収録

```
【自分で録音する場合】
1. 静かな環境を確保
2. 台本を読み上げて録音
3. Audacityで編集
   - ノイズ除去
   - 音量正規化
   - 無音カット
4. MP3/WAVで書き出し

【AI音声を使う場合】
1. VOICEVOX（無料）
   - 商用利用可
   - 日本語特化

2. ElevenLabs（有料）
   - 高品質
   - 感情表現豊か

3. CoeFont（有料）
   - 日本語特化
   - ビジネス向け
```

### Step 3: アバター画像生成

```
【NanoBanana Proで生成】

プロンプト例:
"Professional Japanese business person portrait,
[male/female] in [30s/40s],
smart casual outfit,
confident and trustworthy expression,
looking directly at camera,
clean studio background,
high quality professional headshot,
upper body visible"

サイズ: 1024x1024px
形式: PNG
```

### Step 4: OmniHuman1で動画生成

```
1. SousakuAIにアクセス
2. OmniHuman 1.5を選択
3. 画像をアップロード
4. 音声をアップロード
5. プロンプト入力:
   "Medium shot, professional presentation style,
    subtle hand gestures while speaking,
    confident and engaging expression,
    speaking to camera, soft lighting"
6. 生成実行
7. ダウンロード
```

### Step 5: 動画編集（後処理）

```
【Canva動画 or CapCutで編集】

1. テロップ追加
   - キーワードを強調
   - 読みやすいフォント
   - 背景付き文字

2. BGM追加
   - 控えめな音量
   - 著作権フリー素材
   - 話の邪魔をしない

3. オープニング追加
   - ロゴ
   - タイトル

4. CTA画面追加
   - ボタン風デザイン
   - URL/QRコード

5. 書き出し
   - 1920x1080px
   - MP4形式
   - H.264コーデック
```

---

## トラブルシューティング

### よくある問題と解決策

```
【口の動きが不自然】
原因: 音声の質が低い
対策:
- ノイズを除去
- 発音をクリアに
- 適度なペースで話す

【画像と動きが合わない】
原因: 画像の向きや角度の問題
対策:
- 正面向きの画像を使用
- 解像度を上げる
- 背景をシンプルに

【生成に時間がかかる】
原因: サーバー混雑、音声が長い
対策:
- 時間をずらして再試行
- 音声を分割して生成

【表情が硬い】
原因: プロンプト不足
対策:
- 表情の指定を追加
- "natural expression" を追加
- 感情のキーワードを追加
```

---

## 品質チェックリスト

```
□ リップシンクが自然（音声と口の動きが一致）
□ 表情が内容に合っている
□ ジェスチャーが自然
□ 画質が十分（1080p以上）
□ 音声がクリア
□ 違和感のある部分がない
□ 全体の長さが適切
```

---

## 倫理的ガイドライン

```
【必須事項】
- AI生成であることを明記
- 実在人物の無断使用禁止
- ディープフェイクの悪用禁止
- 著作権の尊重

【推奨事項】
- オリジナルまたは許可済み画像を使用
- 商用利用時はライセンス確認
- 視聴者を欺く目的で使用しない
```

---

## 料金目安（2025年現在）

```
【SousakuAI】
- 従量課金制
- 1動画あたり約100-500円
- 詳細は公式サイト参照

【Fal.ai】
- API利用
- 従量課金
- 開発者向け

【BytePlus】
- エンタープライズ向け
- 要問い合わせ
```

---

## 参照リソース

### 公式

- [OmniHuman1 公式サイト](https://www.omnihuman1.org/ja)
- [SousakuAI](https://sousakuai.jp/)

### 関連ガイド

- `content/creative/video/production-guide.md` - 動画制作ガイド
- `.claude/commands/kindle-line-vsl.md` - VSLスキル

---

## 更新履歴

- 2025-12: 初版作成
