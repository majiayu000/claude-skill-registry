---
name: manual-generator
doc_contract:
  review_interval_days: 30
---

# Manual Generator

> スキル/エージェント/パイプラインの使用マニュアルを自動生成・更新するツール

## 概要

このスキルはプロジェクトのすべてのツール（スキル 41個 + エージェント 14個）に対する **Diataxis ベースのマニュアル**を自動生成し管理します。

- **ソース**: SKILL.md, MANIFEST.json, エージェント .md ファイル
- **出力**: `docs/manuals/` 配下の構造化されたマニュアル
- **検出**: Staleness ハッシュでソース変更時に自動検出

## サブコマンド

| コマンド                            | 説明                                                               | モデル |
| ----------------------------------- | ------------------------------------------------------------------ | ------ |
| `/manual-generator`                 | **全ツール ID インベントリ表示** (引数なし)                        | —      |
| `/manual-generator {tool-id}`       | 特定ツールマニュアル生成/更新                                      | Sonnet |
| `/manual-generator --all`           | 全マニュアル Smart 更新 (stale+missingのみ、`--force`で全体再生成) | Sonnet |
| `/manual-generator --pipeline {id}` | パイプラインマニュアル生成                                         | Opus   |
| `/manual-generator --index`         | マスターインデックスのみ再生成                                     | Haiku  |
| `/manual-generator --check`         | Staleness 検査のみ (変更なし)                                      | Haiku  |

## Pre-flight Checklist

実行前に必ず確認:

- [ ] 対象ツールの SKILL.md またはエージェント .md ファイルが存在するか?
- [ ] `docs/manuals/_templates/` ディレクトリにテンプレート 3種が存在するか?
- [ ] `docs/manuals/manifest.json`が存在するか? (なければ生成)

## ワークフロー

### インベントリ表示 (`/manual-generator` 引数なし)

引数なしで実行すると全ツール ID リストをスキャンしてテーブル表示します。
ユーザーが tool-id を選択できるよう案内します。

```
[Phase 1: スキャン] → Bash (モデル不要)
  ├─ .claude/skills/*/SKILL.md → スキル ID 抽出 (ディレクトリ名)
  ├─ .claude/agents/*.md → エージェント ID 抽出 (ファイル名)
  └─ docs/manuals/pipelines/*.md → パイプライン ID 抽出 (ファイル名)

[Phase 2: 表示]
  ├─ スキルリストテーブル (番号 + tool-id + 簡略説明)
  ├─ エージェントリストテーブル (番号 + tool-id + 簡略説明)
  ├─ パイプラインリストテーブル (番号 + pipeline-id + 簡略説明)
  └─ サブコマンド使用案内
```

**簡略説明ソース**: SKILL.mdの最初の `>` 引用ブロック、エージェント .mdの最初の説明行

### 単件生成 (`/manual-generator {tool-id}`)

```
[Phase 1: スキャン] → Haiku
  ├─ ツール種別判別 (スキル vs エージェント)
  ├─ SKILL.md / agent .md 読み取り
  ├─ MANIFEST.json 読み取り (あれば)
  ├─ 既存マニュアル読み取り (あれば、手動補強部分保存用)
  └─ 関連文書参照 (tool-usage-guide.md, CLAUDE.md)

[Phase 2: 抽出] → Haiku
  ├─ MANIFEST → tier, version, triggers, calls/called_by, outputs
  ├─ SKILL.md → description, workflow, examples, constraints
  └─ 既存マニュアル → 手動補強されたプレイブック/落とし穴保存

[Phase 3: 生成] → Sonnet
  ├─ 抽出データ + テンプレート → マニュアル生成
  ├─ 既存手動補強部分 → 統合 (上書き防止)
  └─ staleness_hash 計算 (SHA256 of ソースファイル群)

[Phase 4: 検証] → Haiku
  ├─ 必須セクション存在確認 (スキル: 7セクション、エージェント: 6セクション)
  ├─ 内部リンク有効性
  ├─ manifest.json 更新 (staleness_hash 含む)
  └─ CHANGELOG.md 項目追加
```

### 全体 Smart 更新 (`--all` / `--all --force`)

```
[Phase 0: インベントリ + Staleness 分類] → Haiku
  ├─ .claude/skills/*/SKILL.md → スキル ID リスト
  ├─ .claude/agents/*.md → エージェント ID リスト
  ├─ manifest.json 1回読み取り → 各ツールの staleness_hash 抽出
  ├─ 現在のソースファイルの SHA256 計算
  └─ 3-tier 分類:
       ├─ current: ソース未変更 (ハッシュ一致)
       ├─ stale:   ソース変更済み (ハッシュ不一致)
       └─ missing: マニュアル未存在または manifestに hash なし

[Phase 1: 分類結果表示]
  ├─ 3-tier 分類テーブル出力
  ├─ current: ✅ (スキップ予定)
  ├─ stale:   🔄 (更新予定)
  └─ missing: ➕ (新規生成予定)

[Phase 2: 更新実行] → Sonnet
  ├─ 基本モード: stale + missingのみ単件ワークフロー実行
  ├─ --force モード: current 含む全体再生成
  └─ 並列最大 2個ずつ処理 (コンテキスト圧縮防止)

[Phase 3: 仕上げ] → Haiku
  ├─ manifest.json 全体更新
  ├─ README.md 再生成
  ├─ CHANGELOG.md 一括項目追加
  └─ 最終結果要約: 更新 N個、新規 N個、スキップ N個
```

**Smart 更新ルール**:

- `--all`: stale + missingのみ処理、currentはスキップ → 効率的
- `--all --force`: staleness 無視、全体強制再生成 → 初期セットアップまたはテンプレート変更時に使用

**Staleness データソース階層**:

- **Primary**: `manifest.json`の `staleness_hash` (1ファイル単一読み取り、62個 hash 一括照会)
- **Repair**: `--index` サブコマンドで front matter → manifest.json 再構築 (不一致復旧)
- manifest.jsonに hashがない項目は `missing`として分類

**並列処理ルール**:

- 一度に **最大 2個**のマニュアルを並列生成 (Task ツール 2個同時呼び出し)
- コンテキスト圧縮(context compaction) 発生時に進行状態が喪失される可能性があるため保守的に制限
- 2個完了後に次の2個処理 (バッチ方式)

### Staleness 検査 (`--check`)

```
[Phase 1] → Haiku
  ├─ manifest.json 1回読み取り → 各ツールの staleness_hash 抽出
  ├─ 現在のソースファイルの SHA256 計算
  ├─ 比較 → current | stale | missing 分類
  └─ 結果テーブル出力 (変更なし)
```

### パイプライン生成 (`--pipeline {id}`)

```
[Phase 1: スキャン] → Haiku
  ├─ パイプライン参加ツール識別
  └─ 各ツールの SKILL.md/MANIFEST.json 読み取り

[Phase 2: 分析] → Opus
  ├─ Stage 順序決定
  ├─ Bridge Artifact 識別
  └─ 失敗シナリオ分析

[Phase 3: 生成] → Opus
  ├─ pipeline-manual.md テンプレートベースマニュアル生成
  └─ ダイアグラム生成 (テキストベース)

[Phase 4: 検証] → Haiku
  └─ manifest.json, CHANGELOG.md 更新
```

### インデックス再生成 (`--index`)

manifest.jsonとマニュアル front matter 間の不一致復旧メカニズム。
front matter を ground truth として manifest.json を再構築する。

```
[Phase 1] → Haiku
  ├─ docs/manuals/ 配下の全マニュアルスキャン
  ├─ frontmatterからメタデータ抽出 (Read limit: 15)
  │   └─ staleness_hash, manual_version, target_version など
  ├─ manifest.json 再生成 (staleness_hash 含む)
  └─ README.md 再生成
```

## バージョン管理

### 二重バージョン体系

```yaml
manual_version: '1.2.0' # マニュアル自体の変更
target_version: '9.1.0' # 対象スキル/エージェントバージョン
last_verified: '2026-02-08' # 整合性最終確認日
staleness_hash: 'abc123...' # ソースファイル SHA256
```

### マニュアルバージョンルール

| 変更タイプ              |    バージョン増加    |
| ----------------------- | :------------------: |
| 対象 MAJOR 変更反映     |        MAJOR         |
| セクション追加/構造変更 |        MINOR         |
| 誤字/リンク修正         |        PATCH         |
| 検証のみ (内容同一)     | `last_verified` 更新 |

### Staleness ハッシュ計算 (Canonical Method)

**必ず以下の Node.js 方法で計算する必要があります** (bash `echo -n` 使用禁止):

```javascript
// スキル: SKILL.md + MANIFEST.json 連結後 SHA256
const crypto = require('crypto');
const fs = require('fs');
let content = fs.readFileSync('.claude/skills/{id}/SKILL.md', 'utf-8');
try {
  content += fs.readFileSync('.claude/skills/{id}/MANIFEST.json', 'utf-8');
} catch (e) {}
const hash = crypto.createHash('sha256').update(content).digest('hex');

// エージェント: agent .md ファイル SHA256
const content = fs.readFileSync('.claude/agents/{id}.md', 'utf-8');
const hash = crypto.createHash('sha256').update(content).digest('hex');
```

**注意**: `echo -n "$(cat file)" | shasum -a 256`は trailing newline を削除して異なるハッシュを生成します。必ず `fs.readFileSync` または `shasum -a 256 file` 方法を使用してください。

### doc_contract ブロックとの関係

ソースファイルに `doc_contract:` front matter ブロックが追加される場合があります。
このブロックは `doc-contract.mjs` 検証スクリプトが使用する別個のメタデータです。

- **staleness_hash**: `doc_contract:` ブロックを **含めて**全体ファイルハッシュ化 (変更時 stale 判定)
- **doc-contract.mjs**: `stripDocContractBlock()`で削除後、別途 16字 truncated ハッシュ使用 (別個システム)

独立検証スクリプト: `node .claude/scripts/doc-contract.mjs`

## 手動補強保存ルール

マニュアルを更新する際、既存マニュアルの次のセクションは **自動上書きせず統合**します:

1. **プレイブック (Scenarios)**: ユーザーが手動追加したシナリオ保存
2. **注意事項 & 落とし穴 (Gotchas)**: 実戦経験から追加された項目保存
3. **変更履歴**: 常に append-only

自動更新対象セクション:

- 概要、クイックスタート、動作原理、リファレンス、関連項目マップ

## Post-flight Checklist

実行後に必ず確認:

- [ ] 生成されたマニュアルの必須セクションがすべて存在するか?
- [ ] manifest.jsonの statsが正確か?
- [ ] CHANGELOG.mdに今回の変更項目が追加されたか?
- [ ] README.mdのインデックステーブルが更新されたか?

## 制約事項

- マニュアル生成は **読み取り専用分析** 後、文書生成のみ実行 (コード修正なし)
- `docs/manuals/` 外部ファイルは修正しない (tool-usage-guide.md リンク追加除く)
- パイプラインマニュアル生成時 Opus モデル必須 (複雑な関係分析)
