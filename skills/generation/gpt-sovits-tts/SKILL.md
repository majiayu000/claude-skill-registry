# GPT-SoVITS TTS スキル

高品質な音声クローニング・TTS（Text-to-Speech）システム。

## 概要

| 項目 | 内容 |
|------|------|
| ツール | GPT-SoVITS v2 |
| 開発元 | RVC-Boss |
| インストール先 | `/Users/matsumototoshihiko/Desktop/semi/miyabi_taiyou/GPT-SoVITS` |
| 用途 | 音声クローニング、ナレーション生成 |

## 特徴

- **Zero-shot TTS**: 5秒の音声サンプルから即座に音声合成
- **Few-shot TTS**: 1分のトレーニングデータで声質を学習
- **多言語対応**: 日本語、英語、中国語、韓国語、広東語
- **高速推理**: RTF 0.028（4060Ti）〜0.526（M4 CPU）

## クイックスタート

### 1. 環境起動

```bash
cd /Users/matsumototoshihiko/Desktop/semi/miyabi_taiyou/GPT-SoVITS
source venv/bin/activate

# WebUI起動（ポート9874）
python webui.py

# または API サーバー起動（ポート9880）
python api.py -dr "参考音声.wav" -dt "参考テキスト" -dl "ja"
```

### 2. API経由で音声生成

```bash
# テキストから音声生成
curl -X POST "http://127.0.0.1:9880" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "こんにちは、これはテスト音声です。",
    "text_language": "ja"
  }' \
  --output output.wav
```

### 3. 参考音声を指定して生成

```bash
curl -X POST "http://127.0.0.1:9880" \
  -H "Content-Type: application/json" \
  -d '{
    "refer_wav_path": "/path/to/reference.wav",
    "prompt_text": "参考音声のテキスト",
    "prompt_language": "ja",
    "text": "生成したいテキスト",
    "text_language": "ja",
    "speed": 1.0
  }' \
  --output output.wav
```

## API パラメータ

| パラメータ | 型 | 説明 |
|-----------|-----|------|
| `text` | string | 生成するテキスト |
| `text_language` | string | テキストの言語（ja/en/zh/ko/yue） |
| `refer_wav_path` | string | 参考音声ファイルのパス |
| `prompt_text` | string | 参考音声の文字起こし |
| `prompt_language` | string | 参考音声の言語 |
| `speed` | float | 話速（0.5〜2.0） |
| `top_k` | int | サンプリングパラメータ |
| `top_p` | float | サンプリングパラメータ |
| `temperature` | float | サンプリングパラメータ |

## Python統合スクリプト

```python
#!/usr/bin/env python3
"""GPT-SoVITS API Client"""
import requests
import os

def generate_audio(
    text: str,
    output_path: str,
    refer_wav_path: str = None,
    prompt_text: str = None,
    prompt_language: str = "ja",
    text_language: str = "ja",
    speed: float = 1.0,
    api_url: str = "http://127.0.0.1:9880"
):
    """Generate audio using GPT-SoVITS API"""

    payload = {
        "text": text,
        "text_language": text_language,
        "speed": speed
    }

    if refer_wav_path:
        payload["refer_wav_path"] = refer_wav_path
        payload["prompt_text"] = prompt_text
        payload["prompt_language"] = prompt_language

    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Audio saved to: {output_path}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

if __name__ == "__main__":
    generate_audio(
        text="AIゴールドラッシュの波に乗り遅れないでください。",
        output_path="output.wav",
        text_language="ja"
    )
```

## ディレクトリ構造

```
GPT-SoVITS/
├── venv/                    # Python仮想環境
├── GPT_SoVITS/
│   └── pretrained_models/   # プレトレーニングモデル（5GB）
├── api.py                   # APIサーバー
├── api_v2.py                # v2 APIサーバー
├── webui.py                 # Web UI
├── config.py                # 設定ファイル
└── output/                  # 出力ディレクトリ
```

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| ポートが使用中 | `lsof -i :9880` で確認し、プロセスを終了 |
| CUDA エラー | `--device cpu` で CPU モードで実行 |
| 音質が悪い | 参考音声の品質を改善、ノイズ除去 |
| 速度が遅い | バッチサイズを調整、GPUを使用 |

## 関連リソース

- [GPT-SoVITS GitHub](https://github.com/RVC-Boss/GPT-SoVITS)
- [ドキュメント（英語）](https://rentry.co/GPT-SoVITS-guide)

## Creatify Aurora リップシンク

GPT-SoVITSで生成した音声を使って、Creatify Aurora APIでリップシンク動画を生成できます。

### 使用方法

```bash
cd /Users/matsumototoshihiko/Desktop/semi/miyabi_taiyou/GPT-SoVITS
source venv/bin/activate

# リップシンク動画を生成
python scripts/generate_lipsync_aurora.py \
  --image /path/to/person.jpg \
  --audio /path/to/narration.wav \
  --output output_lipsync.mp4 \
  --resolution 720p
```

### パラメータ

| パラメータ | 説明 |
|-----------|------|
| `--image` | 人物画像（顔がはっきり見えるもの） |
| `--audio` | 音声ファイル（GPT-SoVITSで生成） |
| `--output` | 出力動画パス |
| `--resolution` | 480p ($0.10/秒) または 720p ($0.14/秒) |
| `--prompt` | オプションのプロンプト |

### 環境変数

```bash
# .envに設定済み
RUNCOMFY_API_KEY=your-api-key
LIPSYNC_MODEL_PRIMARY=creatify-aurora
CREATIFY_AURORA_RESOLUTION=720p
```

## 更新履歴

- 2025-12-25: Creatify Aurora リップシンク統合
- 2025-12-25: 初期インストール・スキル作成
