---
name: gemini-cli
description: Gemini CLIを使った任意のタスクを実行するスキル。長文翻訳、PDF翻訳、Q&A、コード生成など、gemini_wrapperを活用して様々なタスクを自動化できる。
---

# Gemini CLI Skill

## 使用タイミング

ユーザーが以下のような指示をした時に使用します。

- 「Gemini CLIを使って〜」
- 「PDFを翻訳して」
- 「長文を翻訳して」
- 「Geminiで〜を実行して」

## スキルの概要

このスキルは、Gemini CLIをPythonから簡単に呼び出すための汎用ラッパー(`gemini_wrapper.py`)を提供します。

**主な特徴:**
- ✅ 完全汎用的なCLI呼び出し
- ✅ エラーハンドリング完備
- ✅ subprocess処理の自動化
- ✅ 様々なタスクに対応可能
- ✅ **Windows環境対応**

## ファイル構成

```
gemini-cli/
├── gemini_wrapper.py          # 汎用Gemini CLIラッパー
├── example_pdf_translator.py  # PDF翻訳のサンプルスクリプト
├── SKILL.md                    # このファイル
├── README.md                   # GitHub公開用README
└── requirements.txt            # 依存パッケージ
```

## gemini_wrapper.pyの使い方

### 基本的な使い方

```python
from gemini_wrapper import gemini_execute

# プロンプトを実行
success, result, error = gemini_execute("Pythonとは何ですか?", timeout=60)

if success:
    print(result)
else:
    print(f"エラー: {error}")
```

### 戻り値

すべての関数は`(成功フラグ, 結果, エラーメッセージ)`のタプルを返します。

- **成功時**: `(True, "レスポンステキスト", "")`
- **失敗時**: `(False, "", "エラーメッセージ")`

### クラスベースの使い方

```python
from gemini_wrapper import GeminiCLI

gemini = GeminiCLI()
success, result, error = gemini.execute("質問内容", timeout=60)
```

## 実装例

### 例1: テキスト翻訳

```python
from gemini_wrapper import gemini_execute

def translate_text(text, source_lang="英語", target_lang="日本語"):
    """テキストを翻訳"""
    prompt = f"以下の{source_lang}を{target_lang}に翻訳してください。\n\n{text}"
    success, result, error = gemini_execute(prompt, timeout=120)
    return result if success else f"(エラー: {error})"

# 使用例
translated = translate_text("Hello, world!")
print(translated)
```

### 例2: Q&Aボット

```python
from gemini_wrapper import gemini_execute

def ask_question(question):
    """質問に回答"""
    prompt = f"以下の質問に簡潔に答えてください。\n\n{question}"
    success, answer, error = gemini_execute(prompt, timeout=60)
    return answer if success else f"(エラー: {error})"

# 使用例
answer = ask_question("機械学習とは何ですか?")
print(answer)
```

### 例3: コード生成

```python
from gemini_wrapper import gemini_execute

def generate_code(description, language="Python"):
    """コードを生成"""
    prompt = f"{language}で以下の処理を実装してください。\n\n{description}"
    success, code, error = gemini_execute(prompt, timeout=120)
    return code if success else f"(エラー: {error})"

# 使用例
code = generate_code("フィボナッチ数列を計算する関数")
print(code)
```

### 例4: PDF翻訳（サンプルスクリプト参照）

`example_pdf_translator.py`を参照してください。このスクリプトは、PDFを1ページずつ翻訳する完全な実装例です。

```
python example_pdf_translator.py input.pdf output.md
```

## 使用方法

### ステップ1: スクリプトを作成

ユーザーの要望に応じて、`gemini_wrapper.py`を使ったPythonスクリプトを作成します。

**例: テキストファイル翻訳スクリプト**

```python
import sys
from gemini_wrapper import gemini_execute

def translate_file(input_path, output_path):
    """テキストファイルを翻訳"""
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    prompt = f"以下の英語を日本語に翻訳してください。\n\n{text}"
    success, translated, error = gemini_execute(prompt, timeout=180)

    if success:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated)
        print(f"翻訳完了: {output_path}")
    else:
        print(f"エラー: {error}")

if __name__ == "__main__":
    translate_file(sys.argv[1], sys.argv[2])
```

### ステップ2: Writeツールでファイルを作成

```python
Write(file_path="/path/to/translate_text.py", content="...")
```

### ステップ3: Bashツールで実行

```
python translate_text.py input.txt output.txt
```

## 環境変数

`gemini_wrapper.py`は自動的にGemini CLIのパスを検出します。

**Windows環境:**
- `%APPDATA%\npm\gemini.cmd` を自動検出
- 見つからない場合はPATH上の`gemini`を使用

**カスタムパスの指定:**

```python
from gemini_wrapper import GeminiCLI

gemini = GeminiCLI(gemini_path="C:\\path\\to\\gemini.cmd")
```

## 注意事項

### 前提条件

**注意: このツールはWindows環境専用です。**

1. **Gemini CLIのインストール**
   ```
   npm install -g @google/gemini-cli
   ```

2. **Gemini CLIの認証**
   ```
   gemini auth login
   ```

3. **Python環境**
   - Python 3.7以上
   - 必要なパッケージ: `requirements.txt`参照

### タイムアウト設定

長い処理の場合は、適切なタイムアウト値を設定してください。

```python
# デフォルト: 60秒
success, result, error = gemini_execute(prompt, timeout=180)  # 3分
```

### エラーハンドリング

必ず戻り値の`success`フラグをチェックしてください。

```python
success, result, error = gemini_execute(prompt)

if success:
    # 成功時の処理
    print(result)
else:
    # エラー時の処理
    print(f"エラー: {error}")
```

## タスク例

### 長文翻訳タスク

```python
from gemini_wrapper import gemini_execute

def translate_long_text(text, chunk_size=3000):
    """長文を分割して翻訳"""
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    results = []

    for i, chunk in enumerate(chunks):
        print(f"翻訳中: {i+1}/{len(chunks)}")
        prompt = f"以下の英語を日本語に翻訳してください。\n\n{chunk}"
        success, result, error = gemini_execute(prompt, timeout=120)

        if success:
            results.append(result)
        else:
            results.append(f"(エラー: {error})")

    return "\n".join(results)
```

### 複数ファイル一括処理

```python
import os
from gemini_wrapper import gemini_execute

def batch_translate(input_dir, output_dir):
    """ディレクトリ内の全ファイルを翻訳"""
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"translated_{filename}")

            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            prompt = f"以下を日本語に翻訳:\n\n{text}"
            success, result, _ = gemini_execute(prompt, 120)

            if success:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result)
                print(f"完了: {filename}")
```

## トラブルシューティング

### Gemini CLIが見つからない

```
エラー: Gemini CLIが見つかりません
```

**解決方法:**
1. Gemini CLIがインストールされているか確認
   ```
   gemini --version
   ```
2. パスを明示的に指定
   ```python
   gemini = GeminiCLI(gemini_path="C:\\path\\to\\gemini.cmd")
   ```

### タイムアウトエラー

```
タイムアウト: 60秒以内に応答がありませんでした
```

**解決方法:**
timeout値を増やす
```python
gemini_execute(prompt, timeout=300)  # 5分
```

## 参考リンク

- [Gemini CLI公式ドキュメント](https://geminicli.com/docs/get-started/)
- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
