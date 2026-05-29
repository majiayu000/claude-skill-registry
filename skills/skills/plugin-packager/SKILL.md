---
name: plugin-packager
description: 生成したプラグインをZIP形式にまとめる。プラグインパッケージング時、配布準備時、またはユーザーがZIP作成、プラグイン配布、パッケージング、リリース準備に言及した際に使用する。
---

# Plugin Packager

## 概要

このSkillは、生成したプラグインをZIP形式にパッケージングする。プラグインのファイルを収集し、必要なメタデータを生成して、配布可能なZIPファイルを作成する。

## 責任範囲

このSkillは以下の範囲をカバーする:

- パッケージング対象ファイルの収集
- ファイルの完全性検証
- メタデータファイルの生成（package.json、VERSION）
- ZIPファイルの作成
- パッケージの出力とメタデータの記録
- 配布用ドキュメントの準備

## ワークフロー

### フェーズ1: ファイル収集

パッケージングするファイルを収集し、リストを作成する。

**実施内容:**

1. プラグインディレクトリを確認する
2. パッケージング対象のファイルを特定する
3. 除外ファイルを確認する（.claudeignore）
4. ファイルリストを作成する
5. ファイルサイズを集計する

**収集対象:**

- README.md（必須）
- agents/[agent-name].md
- skills/[skill-name]/SKILL.md
- commands/[command-name].md
- LICENSE（オプション）
- CHANGELOG.md（オプション）

**除外対象:**

- .git/
- node_modules/
- .DS_Store
- *.tmp
- .claudeignore に記載されたファイル

**良い例:**

```markdown
【ファイル収集結果】

プラグイン名: database-design-plugin
プラグインディレクトリ: D:\projects\database-design-plugin

収集対象ファイル（11個）:
- README.md
- agents/database-design-agent.md
- skills/entity-definition-collector/SKILL.md
- skills/normalization-processor/SKILL.md
- skills/er-diagram-generator/SKILL.md
- skills/table-definition-writer/SKILL.md
- skills/ddl-script-generator/SKILL.md
- skills/database-naming-conventions/SKILL.md
- skills/normalization-rules/SKILL.md
- commands/design-database.md
- commands/generate-schema.md

除外ファイル:
- .git/（Gitディレクトリ）
- .DS_Store（システムファイル）

合計サイズ: 125 KB
```

**悪い例:**

```markdown
【ファイル収集結果】

何かファイルを集めた
```

### フェーズ2: 検証

収集したファイルの完全性を検証する。

**実施内容:**

1. 必須ファイルの存在を確認する
2. ファイル形式の正当性を確認する
3. フロントマター情報を検証する
4. ファイル内容の完全性を確認する
5. 検証結果をレポートする

**検証項目:**

- README.md が存在するか
- 全ての AGENT.md, SKILL.md, COMMAND.md が正しく読み込めるか
- フロントマター情報が正しくパースできるか
- 必須フィールド（name, description）が存在するか
- ファイル内容が破損していないか

**良い例:**

```markdown
【検証結果】

必須ファイル: ✓ OK
- ✓ README.md が存在する

ファイル形式: ✓ OK
- ✓ 全てのファイルが正しく読み込める（11個）

フロントマター: ✓ OK
- ✓ 全てのフロントマターが正しくパースできる（10個）
- ✓ 必須フィールド（name, description）が全て存在する

ファイル内容: ✓ OK
- ✓ 全てのファイルが破損していない

検証: 合格
```

**悪い例（問題がある場合）:**

```markdown
【検証結果】

必須ファイル: ✗ NG
- ✗ README.md が存在しない

ファイル形式: ✗ NG
- ✗ entity-definition-collector/SKILL.md が読み込めない

フロントマター: ✗ NG
- ✗ normalization-processor/SKILL.md でフロントマターがパースできない

検証: 不合格（3個の問題）
```

### フェーズ3: メタデータ生成

パッケージに必要なメタデータファイルを生成する。

**実施内容:**

1. package.json を生成する
2. VERSION ファイルを生成する
3. MANIFEST.md を生成する（ファイルリスト）
4. ハッシュ値を計算する（整合性確認用）
5. メタデータの妥当性を確認する

**生成するメタデータ:**

- **package.json**: プラグインのメタ情報（名前、バージョン、説明、作者など）
- **VERSION**: バージョン番号
- **MANIFEST.md**: 含まれるファイルのリスト
- **CHECKSUM.txt**: ファイルのハッシュ値（オプション）

**良い例:**

```markdown
【メタデータ生成結果】

package.json:
{
  "name": "database-design-plugin",
  "version": "1.0.0",
  "description": "データベース設計を支援するプラグイン",
  "author": "Your Name",
  "created": "2025-11-15",
  "agents": ["database-design-agent"],
  "skills": [
    "entity-definition-collector",
    "normalization-processor",
    "er-diagram-generator",
    "table-definition-writer",
    "ddl-script-generator",
    "database-naming-conventions",
    "normalization-rules"
  ],
  "commands": ["design-database", "generate-schema"]
}

VERSION:
1.0.0

MANIFEST.md:
# Manifest

このパッケージには以下のファイルが含まれています:

## プラグイン情報
- package.json
- VERSION
- MANIFEST.md
- README.md

## エージェント
- agents/database-design-agent.md

## スキル
- skills/entity-definition-collector/SKILL.md
- skills/normalization-processor/SKILL.md
- skills/er-diagram-generator/SKILL.md
- skills/table-definition-writer/SKILL.md
- skills/ddl-script-generator/SKILL.md
- skills/database-naming-conventions/SKILL.md
- skills/normalization-rules/SKILL.md

## コマンド
- commands/design-database.md
- commands/generate-schema.md

合計: 14ファイル

メタデータ生成: 完了
```

**悪い例:**

```markdown
【メタデータ生成結果】

何か作った
```

### フェーズ4: パッケージング

収集したファイルとメタデータをZIP形式にまとめる。

**実施内容:**

1. ZIPファイル名を決定する
2. ファイルをZIPに追加する
3. ディレクトリ構造を保持する
4. 圧縮レベルを設定する
5. ZIP作成を実行する

**パッケージング設定:**

- **ファイル名形式**: `{plugin-name}-v{version}.zip`
- **圧縮レベル**: 標準（balance between size and speed）
- **ディレクトリ構造**: 保持する
- **ルートディレクトリ**: プラグイン名のディレクトリを作成

**良い例:**

```markdown
【パッケージング結果】

ZIPファイル名: database-design-plugin-v1.0.0.zip

ディレクトリ構造:
database-design-plugin/
  package.json
  VERSION
  MANIFEST.md
  README.md
  agents/
    database-design-agent.md
  skills/
    entity-definition-collector/
      SKILL.md
    normalization-processor/
      SKILL.md
    er-diagram-generator/
      SKILL.md
    table-definition-writer/
      SKILL.md
    ddl-script-generator/
      SKILL.md
    database-naming-conventions/
      SKILL.md
    normalization-rules/
      SKILL.md
  commands/
    design-database.md
    generate-schema.md

ファイル数: 14個
圧縮前サイズ: 125 KB
圧縮後サイズ: 35 KB
圧縮率: 72%

パッケージング: 完了
```

**悪い例:**

```markdown
【パッケージング結果】

ZIPを作った
```

### フェーズ5: 出力

作成したパッケージを出力し、メタデータを記録する。

**実施内容:**

1. 出力先ディレクトリを確認する
2. ZIPファイルを出力する
3. パッケージ情報を記録する
4. 配布用ドキュメントを準備する
5. 次のステップを案内する

**出力先:**

- デフォルト: `{plugin-directory}/dist/`
- カスタム: ユーザー指定のディレクトリ

**良い例:**

```markdown
【出力結果】

出力先: D:\projects\database-design-plugin\dist\
ZIPファイル: database-design-plugin-v1.0.0.zip
ZIPファイルパス: D:\projects\database-design-plugin\dist\database-design-plugin-v1.0.0.zip

パッケージ情報:
- プラグイン名: database-design-plugin
- バージョン: 1.0.0
- 作成日時: 2025-11-15 10:30:00
- ファイル数: 14個
- 圧縮後サイズ: 35 KB
- ハッシュ値（SHA-256）: a1b2c3d4e5f6...

配布用ドキュメント:
- README.md（プラグインの概要、インストール方法、使い方）
- CHANGELOG.md（変更履歴）
- LICENSE（ライセンス情報）

【配布方法】

1. GitHub リリースとして配布
   - ZIPファイルをアップロード
   - リリースノートを作成

2. 手動配布
   - ZIPファイルを共有
   - README.md を参照してもらう

【次のステップ】

1. パッケージを配布する
2. ユーザーにインストール方法を案内する
3. フィードバックを収集する

パッケージング完了: ✓
```

**良い例:**

出力結果が明確で、パッケージ情報、配布方法、次のステップが案内されている。

**悪い例:**

```markdown
【出力結果】

ZIPを作った
```

## アウトプット

このスキルは以下を生成する:

- **ZIPファイル**: プラグイン全体をまとめたZIPファイル
- **メタデータファイル**: package.json, VERSION, MANIFEST.md
- **パッケージ情報レポート**: パッケージの詳細情報（ファイル数、サイズ、ハッシュ値など）

## 想定されるエラーと対処法

### エラー1: 必須ファイルが存在しない

**検出例:**

```markdown
README.md が存在しない
```

**対処法:**

- README.md を作成する
- プラグインの概要、使い方、コマンド一覧を記述する
- パッケージングを再実行する

### エラー2: ファイルが破損している

**検出例:**

```markdown
entity-definition-collector/SKILL.md が読み込めない
```

**対処法:**

- ファイルの内容を確認する
- ファイルを再生成する
- パッケージングを再実行する

### エラー3: メタデータ生成に失敗

**検出例:**

```markdown
package.json の生成に失敗した
```

**対処法:**

- プラグイン名、バージョン、説明が正しいか確認する
- メタデータ生成の設定を確認する
- 再度メタデータ生成を実行する

## ベストプラクティス

- パッケージング前にプラグインを検証する（plugin-validator スキルを使用）
- メタデータファイルを必ず含める（package.json, VERSION, MANIFEST.md）
- README.md を詳細に記述する（インストール方法、使い方）
- CHANGELOG.md を作成する（変更履歴を記録）
- LICENSE ファイルを含める（ライセンス情報）
- ハッシュ値を記録する（整合性確認用）
- 配布用ドキュメントを準備する

## チェックリスト

### ファイル収集完了時

- [ ] プラグインディレクトリが確認されている
- [ ] パッケージング対象のファイルが特定されている
- [ ] 除外ファイルが確認されている
- [ ] ファイルリストが作成されている
- [ ] ファイルサイズが集計されている

### 検証完了時

- [ ] 必須ファイルの存在が確認されている
- [ ] ファイル形式の正当性が確認されている
- [ ] フロントマター情報が検証されている
- [ ] ファイル内容の完全性が確認されている
- [ ] 検証結果がレポートされている

### メタデータ生成完了時

- [ ] package.json が生成されている
- [ ] VERSION ファイルが生成されている
- [ ] MANIFEST.md が生成されている
- [ ] ハッシュ値が計算されている（オプション）
- [ ] メタデータの妥当性が確認されている

### パッケージング完了時

- [ ] ZIPファイル名が決定されている
- [ ] ファイルがZIPに追加されている
- [ ] ディレクトリ構造が保持されている
- [ ] 圧縮レベルが設定されている
- [ ] ZIP作成が実行されている

### 出力完了時

- [ ] 出力先ディレクトリが確認されている
- [ ] ZIPファイルが出力されている
- [ ] パッケージ情報が記録されている
- [ ] 配布用ドキュメントが準備されている
- [ ] 次のステップが案内されている
- [ ] ユーザーの承認を得ている

### 最終確認

- [ ] ZIPファイルが作成されている
- [ ] メタデータファイルが生成されている
- [ ] パッケージ情報レポートが作成されている
- [ ] すべてのアウトプットが明確で理解しやすい
- [ ] ユーザーがパッケージを配布できる状態になっている
