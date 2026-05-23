---
name: japanese-tts-reading
description: 日本語テキストを音声に変換するTTS（Text-to-Speech）スキル。ナレーション原稿の読み上げ、コンテンツの音声化、アクセシビリティ対応に使用。
---

# Japanese TTS Reading Skill

日本語テキストを自然な音声に変換するText-to-Speechスキル。

## When to Use This Skill

以下の場合にこのスキルを使用：
- 「テキストを読み上げて」「音声に変換して」
- 「ナレーション音声を作成して」
- 「日本語TTSで出力して」
- 「音声ファイルを生成して」

## 対応TTS エンジン

### 1. macOS Say コマンド（ローカル・無料）

macOS標準の音声合成機能を使用。追加設定不要で即座に利用可能。

```bash
# 基本的な使用法
say -v Kyoko "こんにちは、世界"

# ファイルに保存
say -v Kyoko -o output.aiff "こんにちは、世界"

# MP3に変換（ffmpegが必要）
say -v Kyoko -o output.aiff "テキスト" && ffmpeg -i output.aiff output.mp3
```

**利用可能な日本語ボイス**:
| ボイス名 | 性別 | 特徴 |
|---------|------|------|
| Kyoko | 女性 | 標準的な女性の声 |
| Otoya | 男性 | 標準的な男性の声 |

**インストール確認**:
```bash
# 利用可能な日本語ボイスを確認
say -v '?' | grep ja_JP
```

---

### 2. Google Cloud Text-to-Speech（クラウド・高品質）

Google の WaveNet / Neural2 音声を使用した高品質TTS。

**セットアップ**:
```bash
# 1. Google Cloud SDK インストール
brew install --cask google-cloud-sdk

# 2. 認証
gcloud auth application-default login

# 3. TTS API 有効化
gcloud services enable texttospeech.googleapis.com
```

**使用例**:
```bash
# Python で使用
pip install google-cloud-texttospeech

# スクリプト実行
python scripts/google-tts.py --text "こんにちは" --output output.mp3
```

**推奨ボイス**:
| ボイス名 | 性別 | 品質 |
|---------|------|------|
| ja-JP-Neural2-B | 女性 | 最高品質 |
| ja-JP-Neural2-C | 男性 | 最高品質 |
| ja-JP-Wavenet-A | 女性 | 高品質 |
| ja-JP-Wavenet-B | 女性 | 高品質 |
| ja-JP-Wavenet-C | 男性 | 高品質 |
| ja-JP-Wavenet-D | 男性 | 高品質 |

---

### 3. VOICEVOX（ローカル・高品質・無料）

日本語に特化したオープンソース音声合成エンジン。

**セットアップ**:
```bash
# Docker で起動
docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest
docker run --rm -p 50021:50021 voicevox/voicevox_engine:cpu-ubuntu20.04-latest
```

**使用例**:
```bash
# 音声合成クエリを作成
curl -X POST "http://localhost:50021/audio_query?text=こんにちは&speaker=1" \
  -H "Content-Type: application/json" > query.json

# 音声を生成
curl -X POST "http://localhost:50021/synthesis?speaker=1" \
  -H "Content-Type: application/json" \
  -d @query.json > output.wav
```

**利用可能なキャラクター**:
| speaker ID | キャラクター |
|-----------|-------------|
| 0 | 四国めたん（あまあま） |
| 1 | ずんだもん（あまあま） |
| 2 | 四国めたん（ノーマル） |
| 3 | ずんだもん（ノーマル） |

---

### 4. OpenAI TTS（クラウド・高品質）

OpenAI の TTS API を使用。

**セットアップ**:
```bash
# 環境変数設定
export OPENAI_API_KEY="sk-xxx"
```

**使用例**:
```bash
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1-hd",
    "input": "こんにちは、世界",
    "voice": "nova"
  }' \
  --output output.mp3
```

**利用可能なボイス**:
| ボイス | 特徴 |
|-------|------|
| alloy | 中性的 |
| echo | 男性的 |
| fable | 男性的・イギリス風 |
| onyx | 男性的・深い |
| nova | 女性的 |
| shimmer | 女性的・柔らかい |

---

## Usage Examples

### 基本的な使用法

```
ユーザー: /japanese-tts-reading 「本日は晴天なり」

→ macOS: say -v Kyoko "本日は晴天なり"
→ ファイル保存: say -v Kyoko -o narration.aiff "本日は晴天なり"
```

### 長文の読み上げ

```
ユーザー: /japanese-tts-reading --file script.txt --output narration.mp3

→ テキストファイルを読み込んで音声化
→ MP3形式で保存
```

### 高品質出力

```
ユーザー: /japanese-tts-reading --engine google --voice ja-JP-Neural2-B "高品質なナレーション"

→ Google Cloud TTS を使用
→ Neural2 ボイスで最高品質出力
```

### VOICEVOX キャラクター

```
ユーザー: /japanese-tts-reading --engine voicevox --speaker 1 "ずんだもんなのだ"

→ VOICEVOX エンジンを使用
→ ずんだもんの声で出力
```

---

## パラメータ

| パラメータ | デフォルト | 説明 |
|-----------|-----------|------|
| --engine | macos | TTS エンジン (macos/google/voicevox/openai) |
| --voice | Kyoko | ボイス名 |
| --speaker | 0 | VOICEVOX speaker ID |
| --output | - | 出力ファイルパス |
| --file | - | 入力テキストファイル |
| --rate | 1.0 | 読み上げ速度 (0.5-2.0) |
| --format | mp3 | 出力形式 (mp3/wav/aiff) |

---

## 実装ガイド

### macOS Say コマンド（推奨・即時利用可能）

```bash
#!/bin/bash
# scripts/tts-macos.sh

TEXT="$1"
OUTPUT="${2:-output.aiff}"
VOICE="${3:-Kyoko}"
RATE="${4:-200}"  # 1-500 (デフォルト: 200)

say -v "$VOICE" -r "$RATE" -o "$OUTPUT" "$TEXT"

# MP3に変換（オプション）
if command -v ffmpeg &> /dev/null; then
  ffmpeg -i "$OUTPUT" -y "${OUTPUT%.aiff}.mp3"
  rm "$OUTPUT"
fi
```

### Google Cloud TTS

```python
# scripts/google-tts.py

from google.cloud import texttospeech
import argparse

def synthesize_speech(text, output_file, voice_name="ja-JP-Neural2-B"):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP",
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    print(f"Audio saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--output", default="output.mp3")
    parser.add_argument("--voice", default="ja-JP-Neural2-B")
    args = parser.parse_args()

    synthesize_speech(args.text, args.output, args.voice)
```

### VOICEVOX

```python
# scripts/voicevox-tts.py

import requests
import argparse

VOICEVOX_URL = "http://localhost:50021"

def synthesize_voicevox(text, speaker=1, output_file="output.wav"):
    # 音声合成クエリを作成
    query_response = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={"text": text, "speaker": speaker}
    )
    query = query_response.json()

    # 音声を合成
    synthesis_response = requests.post(
        f"{VOICEVOX_URL}/synthesis",
        params={"speaker": speaker},
        json=query
    )

    with open(output_file, "wb") as f:
        f.write(synthesis_response.content)

    print(f"Audio saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--speaker", type=int, default=1)
    parser.add_argument("--output", default="output.wav")
    args = parser.parse_args()

    synthesize_voicevox(args.text, args.speaker, args.output)
```

---

## ユースケース

### 1. ナレーション原稿の音声化

```
ユーザー: セールス動画のナレーションを音声化して

→ 1. 原稿テキストを確認
→ 2. 適切なボイスを選択（プロフェッショナル: Google Neural2）
→ 3. 音声ファイルを生成
→ 4. 必要に応じて速度・トーンを調整
```

### 2. ブログ記事の音声版作成

```
ユーザー: この記事を音声に変換してポッドキャスト用に

→ 1. テキストを段落ごとに分割
→ 2. 適切な間を挿入
→ 3. 音声ファイルを生成
→ 4. MP3形式で出力
```

### 3. アクセシビリティ対応

```
ユーザー: ウェブサイトのコンテンツを音声で提供したい

→ 1. 主要コンテンツを抽出
→ 2. 音声ファイルを生成
→ 3. ウェブプレイヤーと統合
```

---

## 品質ガイドライン

### 読み上げテキストの最適化

1. **句読点を適切に配置** - 自然な間を作る
2. **難読漢字にルビを追加** - 読み間違いを防ぐ
3. **長い文は分割** - 1文30文字程度を目安
4. **専門用語は読み仮名を併記**

### 例

```
Before:
「日本国憲法第九条は戦争放棄を規定している。」

After:
「日本国憲法（にほんこくけんぽう）第九条（だいきゅうじょう）は、
戦争放棄（せんそうほうき）を規定（きてい）しています。」
```

---

## トラブルシューティング

### macOS で日本語ボイスが見つからない

```bash
# システム環境設定で日本語ボイスをダウンロード
open "x-apple.systempreferences:com.apple.preference.speech"

# または直接確認
say -v '?' | grep -i japan
```

### VOICEVOX が起動しない

```bash
# Docker 確認
docker ps

# ログ確認
docker logs voicevox

# ポート確認
curl http://localhost:50021/speakers
```

### Google TTS 認証エラー

```bash
# 認証状態確認
gcloud auth application-default print-access-token

# 再認証
gcloud auth application-default login
```

---

## 関連スキル

- **copywriting-helper** - ナレーション原稿の作成
- **vsl** - VSL台本の音声化
- **launch-video** - ローンチ動画ナレーション

---

## References

- [macOS say コマンド](https://ss64.com/osx/say.html)
- [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech)
- [VOICEVOX](https://voicevox.hiroshiba.jp/)
- [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech)
