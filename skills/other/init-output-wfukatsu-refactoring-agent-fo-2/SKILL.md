---
name: init-output
description: 出力ディレクトリ初期化 - リファクタリング分析用の出力ディレクトリ構造を作成。/init-output [出力パス] で呼び出し。
user_invocable: true
---

# Output Directory Initializer

出力ディレクトリを初期化し、必要なフォルダ構造を作成するユーティリティスキルです。

## 使用方法

リファクタリング分析を開始する前に、このスキルを実行して出力ディレクトリを準備します。

## 実行コマンド

```bash
# デフォルトの出力先（reports/）
/init-output

# カスタム出力先
/init-output ./custom-output
```

## 作成されるディレクトリ構造

```
reports/
├── 00_summary/
├── 01_analysis/
├── 02_evaluation/
├── 03_design/
├── 04_stories/
├── graph/
│   └── data/
└── 99_appendix/
```

## 初期化スクリプト

以下のBashコマンドを実行して出力ディレクトリを作成します：

```bash
#!/bin/bash

OUTPUT_DIR="${1:-reports}"

mkdir -p "${OUTPUT_DIR}/00_summary"
mkdir -p "${OUTPUT_DIR}/01_analysis"
mkdir -p "${OUTPUT_DIR}/02_evaluation"
mkdir -p "${OUTPUT_DIR}/03_design"
mkdir -p "${OUTPUT_DIR}/04_stories"
mkdir -p "${OUTPUT_DIR}/graph/data"
mkdir -p "${OUTPUT_DIR}/99_appendix"

# メタデータファイルの初期化
cat > "${OUTPUT_DIR}/00_summary/project_metadata.json" << 'EOF'
{
    "project": {
        "name": "",
        "version": "1.0.0",
        "created_at": "",
        "updated_at": ""
    },
    "source": {
        "path": "",
        "type": "",
        "languages": [],
        "frameworks": []
    },
    "analysis": {
        "status": "not_started",
        "modules_count": 0,
        "domains_count": 0,
        "average_mmi": 0
    },
    "agents": {
        "system_analyzer": { "status": "pending" },
        "mmi_evaluator": { "status": "pending" },
        "domain_mapper": { "status": "pending" },
        "microservice_architect": { "status": "pending" },
        "domain_storyteller": { "status": "pending" }
    }
}
EOF

echo "Output directory initialized: ${OUTPUT_DIR}"
```

## 既存ディレクトリの扱い

- 既存のディレクトリがある場合は上書きしません
- `--force` オプションで強制的に再作成できます

```bash
/init-output --force
```

## プロンプト

あなたは出力ディレクトリを初期化するユーティリティエージェントです。

以下の手順で実行してください：

1. 出力先ディレクトリパスを確認
2. 既存ディレクトリの有無を確認
3. ディレクトリ構造を作成
4. メタデータファイルを初期化
5. 完了メッセージを表示

```
# Bashツールで実行
Bash: mkdir -p reports/{00_summary,01_analysis,02_evaluation,03_design,04_stories,graph/data,99_appendix}
```

## 注意事項

- 書き込み権限がない場合はエラーになります
- 大文字小文字は区別されます
- 相対パスと絶対パスの両方が使用可能です
