---
name: deep-explain
description: |
  プロジェクト内/外部対象に対する構造化された深層分析を提供する読み取り専用ユーティリティスキル。
  スキル、機能、OSS、ライブラリ、技術コンセプトなど「これは何？」に対する一貫した回答を提供する。

  例:
  - /deep-explain feature-pilot
  - /deep-explain 035
  - /deep-explain @tanstack/react-query
  - /deep-explain <OSS名>
  - /deep-explain feature-pilot
  - /deep-explain feature-pilot --no-save
doc_contract:
  review_interval_days: 90
---

# deep-explain

> **一言**: 分からないことに対して `/deep-explain X` 一行で構造化された深層分析を受け取り、`docs/explain/`に自動保存される。

---

## 核心原則

1. **自動検出**: 対象タイプを自動で判別して適切なコンテキストソースを探索
2. **一貫した構造**: 常に同じ6セクション構造で出力（スキップ禁止）
3. **読み取り専用**: コード変更なし。分析と説明のみ実行（docs/explain/保存を除く）
4. **コンテキスト優先**: 一般知識よりプロジェクト内の実際のファイルベース分析を優先
5. **視覚化**: 複雑なワークフロー/依存関係は`diagram-generator`エージェントでダイアグラム生成
6. **デフォルト保存**: 分析結果は常に`docs/explain/`に保存（`--no-save`で無効化）

---

## EXECUTION PROTOCOL (LIGHT)

> このスキルは読み取り専用なので軽量プロトコルを適用する。

### Pre-flight (必須)

スキル実行時に必ず以下のチェックリストを出力して確認する。

```
Pre-flight Checklist
├─ [ ] 分析対象識別: {target}
├─ [ ] 対象タイプ決定: {skill | feature | oss | library | general}
├─ [ ] コンテキストソース確認: {source_files}
└─ [ ] --no-save 有無: {yes | no}
```

### Model Routing

| 作業                              | モデル | 理由                             |
| --------------------------------- | ------ | -------------------------------- |
| コンテキスト探索 (Glob/Grep/Read) | Haiku  | 単純なファイル探索、トークン節約 |
| 分析および出力生成                | Sonnet | 構造化された分析品質保証         |

### ダイアグラム生成

分析対象が**ダイアグラム生成条件**に該当すれば`diagram-generator`エージェントを呼び出して視覚的ダイアグラム(.drawio + .svg)を一緒に生成する。（`--no-save`時にはダイアグラムを生成せずテキスト/ASCIIで表現）

**ダイアグラム生成条件**（1つ以上満たす時）:

| 条件                                             | 例                                | ダイアグラムタイプ        |
| ------------------------------------------------ | --------------------------------- | ------------------------- |
| 呼び出す/呼び出されるスキルが**3個以上**         | feature-pilot (15個呼び出し)      | Dependency ダイアグラム   |
| パイプライン/ワークフローステップが**4段階以上** | feature-pilotの7 Stepパイプライン | Data Flow ダイアグラム    |
| ステートマシンが存在                             | CONTEXT.jsonの10個状態            | State ダイアグラム        |
| アーキテクチャレイヤーが**3個以上**              | presentation/domain/data          | Architecture ダイアグラム |

**呼び出し方法**（MUST: `draw-io`スキル使用）:

```
1. Skillツールで`draw-io`スキルを呼び出して.drawio XML生成
2. drawio CLIでSVG変換: drawio -x -f svg -t -o "{output}.svg" "{input}.drawio"
```

> ⚠️ `.drawio`生成後必ず`drawio CLI`で`.svg`変換まで完了する必要がある。
> `.svg`変換が完了してこそダイアグラム生成が完了したことになる。
> `general-purpose`エージェントに委任するとSVG変換を漏らす可能性があるので禁止。

**保存場所**: `docs/explain/diagrams/{target}-{type}.drawio` + `.svg`

**SVG挿入（MUST）**: 生成された`.svg`ファイルは必ず分析文書の該当セクションに挿入する:

- **セクション2（ワークフロー）**: `![{target} Data Flow](diagrams/{target}-data-flow.svg)`
- **セクション6（関連項目マップ）**: `![{target} Dependency](diagrams/{target}-dependency.svg)`

**`--no-save`指定時**: ダイアグラムエージェントを呼び出さず、セクション内テキスト/ASCIIダイアグラムで表現する。

### Post-flight

なし（読み取り専用スキルなので検証不要）

---

## 対象タイプ自動検出

AIは入力を分析して以下のルールで対象タイプを自動決定する。
**優先順位順**でマッチし、最初のマッチで確定する。

### 検出ルール

| 優先順位 | 条件                                                | タイプ      | コンテキストソース      |
| :------: | --------------------------------------------------- | ----------- | ----------------------- |
|    1     | `.claude/skills/{input}/`ディレクトリ存在           | **skill**   | SKILL.md, MANIFEST.json |
|    2     | 3桁数字または`docs/features/*{input}*/`マッチ       | **feature** | CONTEXT.json, SPEC.md   |
|    3     | `docs/oss/{input}/`または`oss-sources/{input}/`存在 | **oss**     | 分析文書、ソースコード  |
|    4     | `package.json`のdependenciesに存在                  | **library** | package.json, context7  |
|    5     | 上記どこにも該当しない                              | **general** | WebSearch、一般知識     |

### タイプ別コンテキスト収集

#### skill タイプ

```
1. Read: .claude/skills/{name}/SKILL.md          ← 核心動作/プロトコル
2. Read: .claude/skills/{name}/MANIFEST.json      ← メタデータ/依存性
3. Glob: .claude/skills/{name}/templates/         ← テンプレート（あれば）
4. Grep: "calls".*"{name}" in .claude/skills/     ← 誰がこのスキルを呼ぶか？
5. Grep: "{name}" in CLAUDE.md                    ← プロジェクト指針での役割

── 関連項目収集（セクション6用）──
6. MANIFEST.jsonの"calls"配列 → 各下位スキルのMANIFEST.json読み込み（description, tier, public_api）
7. MANIFEST.jsonの"called_by"配列 → 各上位スキルのMANIFEST.json読み込み
8. Grep: "{name}" in docs/features/*/CONTEXT.json  ← このスキルを使用する機能
9. Grep: "{name}" in docs/                         ← 関連文書（explain/, oss/, technical/）
```

#### feature タイプ

```
1. Read: docs/features/{id}-*/CONTEXT.json        ← 機能コンテキスト（SSOT）
2. Read: docs/features/{id}-*/SPEC-*.md            ← 技術仕様（あれば）
3. Glob: docs/features/{id}-*/screens/             ← UI仕様（あれば）
4. Glob: lib/features/{feature_name}/              ← 実装コード構造
5. Read: docs/features/index.md                    ← 全機能リストでの位置

── 関連項目収集（セクション6用）──
6. CONTEXT.jsonの"dependencies" / "related_features" → 関連機能CONTEXT.json読み込み（title, status）
7. SPEC.mdのimport/provider参照 → 依存する他のfeatureバレルファイル識別
8. Grep: "{feature_name}" in .claude/skills/       ← この機能に関連するスキル
9. Grep: "{feature_name}" in docs/                 ← 関連技術文書/ADR
```

#### oss タイプ

```
1. Read: docs/oss/{name}/ 内全分析文書        ← 既存分析結果
2. Read: docs/oss/_catalog/mechanisms.json         ← カタログ内関連項目
3. Glob: oss-sources/{name}/                       ← ソースコード構造（あれば）
4. Read: oss-sources/{name}/README.md              ← プロジェクト説明（あれば）

── 関連項目収集（セクション6用）──
5. mechanisms.jsonでこのOSS所属メカニズムリスト → 各メカニズムのcontext_fit, decision確認
6. Grep: "{name}" in .claude/skills/               ← このOSSからインスパイアされたスキル
7. Grep: "{name}" in .claude/skills/               ← 関連スキル追加検索
8. Read: docs/oss/ 内他のOSS分析文書           ← 比較対象OSS（あれば）
```

#### library タイプ

```
1. Read: package.json                              ← バージョン、依存性
2. context7: 公式文書検索                          ← 最新API/ガイド
3. Grep: import.*{name} in src/                    ← プロジェクト内実際使用箇所
4. Read: package-lock.json                         ← 正確なインストールバージョン（必要時）

── 関連項目収集（セクション6用）──
5. package.jsonで一緒に使用する関連パッケージ識別（例: @tanstack/react-query → zod, axios）
6. Grep: "{name}" in src/features/                 ← このライブラリを使用するfeatureリスト
7. Grep: "{name}" in docs/                         ← 関連技術文書/ADR
```

#### general タイプ

```
1. WebSearch: "{対象}"最新情報                     ← 一般知識
2. Grep: {対象} in lib/ + docs/                     ← プロジェクト内関連性確認
3. context7: 関連ライブラリ文書（該当時）            ← 技術文書
```

---

## 出力構造（6セクション固定）

**すべての分析は必ず以下の6セクションを全部含める。セクションをスキップしない。**

情報が不足しているセクションは「情報不足 - {理由}」と表示する。

### セクション1: 概要

```markdown
## 1. 概要

- **一行要約**: {対象}は{核心機能}を実行する{分類}である。
- **存在理由（Why）**: {なぜ必要か？どんな問題を解決するか？}
- **なければ？**: {これがなければどうなるか？}
```

### セクション2: ワークフロー

```markdown
## 2. ワークフロー

- **入力**: {何を受け取るか？}
- **処理**: {内部で何をするか？}
- **出力**: {何を生産するか？}
- **トリガー**: {いつ/どのように実行されるか？}

**実行フロー**:
{テキストまたはダイアグラムでフロー表示}
```

### セクション3: 核心メカニズム

```markdown
## 3. 核心メカニズム

### {メカニズム1名}

{動作原理説明}

### {メカニズム2名}

{動作原理説明}

**構成要素関係**:

| 要素 | 役割 | 依存対象 |
| ---- | ---- | -------- |
| ...  | ...  | ...      |
```

### セクション4: 比較分析

```markdown
## 4. 比較分析

| 項目       | {対象} | {代案1} | {代案2} |
| ---------- | ------ | ------- | ------- |
| アプローチ | ...    | ...     | ...     |
| 長所       | ...    | ...     | ...     |
| 短所       | ...    | ...     | ...     |
| 適した状況 | ...    | ...     | ...     |

**選択根拠**: {なぜこれを選択したか / どんな状況で選択すべきか}
```

### セクション5: 詳細情報

```markdown
## 5. 詳細情報

- **設定/オプション**: {使用可能な設定、フラグ、パラメータ}
- **注意事項**: {よくある間違い、既知の制限事項}
- **関連項目**: {関連スキル/機能/文書リンク}
```

### セクション6: 関連項目マップ（Relationship Map）

> **核心**: 対象を単独で見ず、**接続された生態系全体**を眺める。
> 関連項目収集段階で収集したデータを基に作成する。

```markdown
## 6. 関連項目マップ

### 呼び出し/依存関係（Dependency Graph）

{対象が呼び出すまたは依存する項目の関係を表示}

| 方向         | 項目              | 役割要約   | 関係                        |
| ------------ | ----------------- | ---------- | --------------------------- |
| → 呼び出し   | {skill/feature名} | {一行役割} | {どんな文脈で呼び出し/依存} |
| ← 被呼び出し | {skill/feature名} | {一行役割} | {どんな文脈で呼び出される}  |

### 関連スキル（Related Skills）

{対象と直・間接的に関連するAgent Skills}

| スキル     | Tier  | 関係タイプ                                     | 説明          |
| ---------- | ----- | ---------------------------------------------- | ------------- |
| {スキル名} | {1-3} | {calls/called_by/shares_data/同じパイプライン} | {1行関係説明} |

### 関連機能（Related Features）

{対象と関連するアプリ機能}

| 機能ID | 機能名   | 状態   | 関係           |
| ------ | -------- | ------ | -------------- |
| {XXX}  | {機能名} | {状態} | {どんな関係か} |

### 関連文書（Related Documents）

{対象を理解するのに役立つ文書}

| 文書     | パス   | 関連性             |
| -------- | ------ | ------------------ |
| {文書名} | {パス} | {なぜ関連があるか} |
```

**タイプ別セクション6作成ガイド**:

| タイプ      | 主要焦点                                                     | 例                                               |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------ |
| **skill**   | calls/called_byスキル分析、所属パイプライン                  | feature-pilotの11個下位スキル各々の役割          |
| **feature** | 依存feature、使用するサービス/スキル、関連SPEC               | 035の依存: ai_tutor, lesson, review              |
| **oss**     | 抽出されたメカニズム、インスパイアされたスキル、カタログ位置 | <OSS名> → turbo-mode, persistent-mode            |
| **library** | 一緒に使用するパッケージ、使用するfeatureリスト              | @tanstack/react-query → zod, axios; 30+ features |
| **general** | プロジェクト内関連コード/文書（あれば）                      | ATAM → oss-analyzer v3.0で使用                   |

**作成規則**:

- 関連項目が**5個以下**なら各々に対して2-3行説明追加
- 関連項目が**6個以上**ならテーブルで要約し、核心3個のみ詳細説明
- 関連項目が**なければ**「関連項目なし - {理由}」と表示（セクション自体は省略しない）

---

## デフォルト保存動作

分析結果は**常に**ファイルで保存される。`--no-save`フラグで無効化できる。

### 保存ルール

- **位置**: `docs/explain/{target}.md`
- **ダイアグラム**: `docs/explain/diagrams/{target}-{type}.drawio` + `.svg`（生成条件充足時）
- **ディレクトリ自動生成**: `docs/explain/`, `docs/explain/diagrams/`がなければ生成
- **形式**: 上記6セクション構造 + メタデータヘッダー
- **ダイアグラムリンク（MUST）**: 生成された`.svg`は必ず分析文書内該当セクションに挿入:
  - セクション2（ワークフロー）: `![{target} Data Flow](diagrams/{target}-data-flow.svg)`
  - セクション6（関連項目マップ）: `![{target} Dependency](diagrams/{target}-dependency.svg)`

### ファイルヘッダー

```markdown
---
target: { 対象 }
type: { skill | feature | oss | library | general }
generated: { YYYY-MM-DD }
sources:
  - { コンテキストソースファイル1 }
  - { コンテキストソースファイル2 }
---
```

### --no-save オプション

`--no-save`が指定されれば対話内でのみ出力してファイルを生成しない。ダイアグラムも生成しない。

---

## エラー処理

| 状況                           | 対応                                           |
| ------------------------------ | ---------------------------------------------- |
| 対象を見つけられない           | 類似名候補を提示して選択要請                   |
| コンテキストソースが空         | general タイプにフォールバック、WebSearch 活用 |
| 曖昧な入力（複数タイプマッチ） | マッチした候補を表示してユーザーに選択要請     |

---

## 他スキルとの境界

| スキル               | 目的                                | deep-explainとの違い                                     |
| -------------------- | ----------------------------------- | -------------------------------------------------------- |
| `oss-analyzer`       | OSS深層Due Diligence + **文書生成** | deep-explainは迅速な理解用、ファイル未生成（--save除く） |
| `skill-health-check` | スキルガバナンス**検査**            | deep-explainはスキル内容**説明**                         |
| `feature-doctor`     | CONTEXT.json **診断/復旧**          | deep-explainは機能**説明**                               |

**原則**: deep-explainは「理解」を助けるツール。「変更/検証/生成」は他スキルの責任。

---

## 使用例

```bash
# スキル分析 - "feature-pilotが何だったっけ？"
/deep-explain feature-pilot

# 機能分析 - "035番機能は何？"
/deep-explain 035

# OSS分析 - "OSSでhooksがどう動作する？"
/deep-explain <OSS名>

# ライブラリ分析 - "@tanstack/react-query staleTimeは何？"
/deep-explain @tanstack/react-query staleTime

# 一般技術 - "ATAMは何？"
/deep-explain ATAM

# 保存なしで対話でのみ出力
/deep-explain feature-pilot --no-save
```

---

## 変更履歴

| バージョン | 日付       | 変更                                                                                                 |
| ---------- | ---------- | ---------------------------------------------------------------------------------------------------- |
| 1.3.0      | 2026-02-07 | デフォルト保存に変更: --save → デフォルト動作、--no-saveでオプトアウト。ダイアグラムもデフォルト生成 |
| 1.2.0      | 2026-02-06 | diagram-generatorエージェント統合: 複雑なワークフロー/依存関係ダイアグラム自動生成                   |
| 1.1.0      | 2026-02-06 | セクション6「関連項目マップ」追加: タイプ別関連項目収集・分析、依存グラフ、関連スキル/機能/文書含む  |
| 1.0.0      | 2026-02-06 | 初期バージョン: 5セクション構造分析、対象自動検出、--saveオプション                                  |
