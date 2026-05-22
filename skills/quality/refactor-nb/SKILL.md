---
name: refactor_nb
description: Jupyter Notebook (.ipynb) 内の import 文やコードセルを一括置換・リファクタリングする
---

# `refactor_notebooks` Skill

Jupyter Notebook (.ipynb) ファイルをプログラムから解析し、特定の import パターンやコードの塊をプログラム的に置換・修正するためのスキルです。

## Instructions

1.  **Analyze Notebook Structure**:
    *   Python コードを使用して `.ipynb` ファイルを JSON としてロードし、`cells` リストを走査します。
    *   各セルの `cell_type` が `code` であるかを確認します。

2.  **Filter and Match**:
    *   `source` フィールド（リスト形式）を文字列に結合し、正規表現やキーワードマッチングで対象のセルを特定します。
    *   特定の import 文 (`from gwexpy.noise import asd`) や関数呼び出し、特定のコメントを検索対象にします。

3.  **Implement Transformation**:
    *   置換用のスクリプトを作成し、メモリ上でセルの `source` リストを書き換えます。
    *   置換後のソースは、リスト形式（各要素が改行で終わる文字列）にする必要があります。

4.  **Write and Verify**:
    *   `json.dump` を使用して、インデント 1 (gwexpy での慣習) を保持し、`ensure_ascii=False` を指定してファイルを保存します。
    *   出力されたノートブックが妥当な JSON であり、意図した通りの変更が行われていることを `view_file` 等で確認します。

## Usage Guidelines

*   多数のノートブックを横断的に修正する場合は、対象ディレクトリ内の `.ipynb` を `glob` 等で収集するループスクリプトを作成してください。
*   修正が複雑な場合は、一時的な `.py` スクリプトとして保存し、`run_command` で実行してから自身を削除するワークフローを採用してください。
