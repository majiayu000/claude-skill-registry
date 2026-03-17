---
name: oss-analyzer
doc_contract:
  review_interval_days: 90
---

# OSS Analyzer Skill

> **Version**: v4.0.0 (Problem-Decision-Recipe Framework)
> **Type**: Analysis Agent (Tier 1 - Atomic)
> **Constraint**: READ-ONLY (no code modifications)

## Purpose

OSS プロジェクトから **我々の問題(Problem)に対する設計決定(Decision)を逆追跡** し、
プロジェクト に適用できる **具体的なレシピ(Recipe)** を導出するスキル。

**v4.0が解決する問題** (v1~v3 の繰り返し失敗から導出):

| #   | 問題                    | v3.0                    | v4.0 での解決                        |
| --- | ----------------------- | ----------------------- | ------------------------------------ |
| 1   | Mechanism 中心 = 適用 0 | C4+GoF 全数調査         | Problem-first 逆追跡                 |
| 2   | 「なぜこの方式か」不在  | Design Rationale (浅い) | **Forces** (衝突する制約を明示)      |
| 3   | 代替案分析なし          | 単一選択肢の文書化      | **Alternatives Considered** 必須     |
| 4   | 適用レシピなし          | Context Fit のみ提供    | **Recipe** (Pseudocode+Verification) |
| 5   | カタログが空            | mechanisms.json = []    | catalog.json + 逆登録3件             |

---

## Methodology: Problem-Decision-Recipe (PDR)

### 核心転換

```
v3: OSS スキャン → Mechanism 発見 → 抽象的評価 → 適用 0
v4: 我々の Problem → OSS で Decision 逆追跡 → 具体的 Recipe → 適用追跡
```

### 業界標準活用

| 方法論                           | 取り入れるもの                     | 取り入れないもの            |
| -------------------------------- | ---------------------------------- | --------------------------- |
| **ADR** (Nygard)                 | Context-Decision-Consequences 構造 | Status lifecycle            |
| **Pattern Language** (Alexander) | **Forces** (衝突する制約)          | 全体パターン言語体系        |
| **ATAM** (SEI)                   | Quality Attribute トレードオフ     | 3-4日ワークショッププロセス |
| **TW Radar**                     | Adopt/Trial/Assess/Hold 4段階      | 組織全体の技術レーダー      |
| **GoF** (v3で検証)               | Intent/Interface/How It Works      | 23個のパターン分類体系      |

### v3から維持するもの

- C4 Level 1-2 Top-Down 探索 (キーワードなしで開始可能)
- Symbol-first 識別 (行番号の代わりに関数名/クラス名)
- Evidence ルール (根拠なき主張禁止)
- TW Radar 4段階分類
- 3個の成果物構造

### v3から変更するもの

| v3                            | v4                                       | 理由                               |
| ----------------------------- | ---------------------------------------- | ---------------------------------- |
| Phase 1: C4 全数調査          | Phase 1: C4 軽量 + **Problem Discovery** | Problem-firstが適用動機を生む      |
| Phase 2: GoF Mechanism 文書化 | Phase 2: **Decision Archaeology**        | 「何」→「なぜこの方式か」への転換  |
| Phase 3: ATAM 抽象評価        | Phase 3: **Adoption Engineering**        | 「考慮せよ」→「こうせよ」への転換  |
| mechanisms.json               | **catalog.json**                         | PDR は mechanism と異なる概念      |
| メリット/デメリットテーブル   | **Forces + Alternatives**                | 代替案なき分析は批判的思考ではない |

---

## Execution Protocol

### Pre-flight Checklist

| #   | 項目                                    | 確認 |
| --- | --------------------------------------- | ---- |
| 1   | OSS ソースパスにアクセス可能            | ⬜   |
| 2   | 出力ディレクトリへの書き込み可能        | ⬜   |
| 3   | ソースファイルの存在確認                | ⬜   |
| 4   | キャッシュ確認 (--force 時は省略)       | ⬜   |
| 5   | --problem 指定時に Problem の有効性確認 | ⬜   |

> PF-1~3 失敗時は即時中断

### Post-flight Checklist (Quality Scorecard)

| #   | 領域                 | 基準                                          | 配点 | 確認 |
| --- | -------------------- | --------------------------------------------- | :--: | ---- |
| 1   | Forces 完全性        | 全 Decision に Forces 2個以上 (Evidence 含む) |  20  | ⬜   |
| 2   | Alternative 多様性   | 全 Decision に代替案 1個以上 (却下理由含む)   |  20  | ⬜   |
| 3   | Recipe 具体性        | Adopt/Trial Decision に Recipe 含む           |  20  | ⬜   |
| 4   | Problem マッピング率 | 全 Decision が Problem にマッピング済み       |  20  | ⬜   |
| 5   | Evidence 充実度      | 全 Forces/Rationale に Evidence タグ          |  20  | ⬜   |

**総点 80+ = PASS, 60-79 = REVIEW, <60 = FAIL**

> POF-1~3 FAIL 時は分析未完了と見なす

### Model Routing

| 作業                                          | 推奨モデル |
| --------------------------------------------- | :--------: |
| Phase 1 探索 (ファイルスキャン, Problem 収集) |   haiku    |
| Phase 2 分析 (Decision Archaeology)           |   sonnet   |
| Phase 3 評価 + Recipe 作成                    |   sonnet   |

---

## Phase 1: Reconnaissance (C4 軽量 + Problem Mapping)

> **目的**: OSS コンテキストを把握し、我々の Problem を定義して分析の焦点を絞る

### Part A: OSS Context Scan

v3 の C4 Level 1-2 を軽量化:

```
1. README.md → 目的、核心機能、使い方
2. マニフェスト → 技術スタック、Primary Language
3. ディレクトリ 1-depth → モジュール境界
4. Import Hotspot → 核心モジュール TOP 5
5. Entry/Extension Points → 拡張点識別
```

**Primary Language 判定基準** (v3 そのまま維持):

| マニフェスト              | 言語判定                                  |
| ------------------------- | ----------------------------------------- |
| package.json              | JS/TS (devDeps に typescript があれば TS) |
| package.json              | TypeScript                                      |
| Cargo.toml                | Rust                                      |
| go.mod                    | Go                                        |
| setup.py / pyproject.toml | Python                                    |
| pom.xml / build.gradle    | Java/Kotlin                               |

### Part B: Problem Discovery (v4 核心新規)

**プロジェクト の Pain Points を構造化された Problem として収集**:

```
1. CLAUDE.md → プロジェクトルール/制約 → 違反可能性の高い領域
2. .claude/hooks/ + .claude/scripts/ → 現在の自動化レベルとギャップ
3. .claude/skills/ → 現在のスキル能力と限界
4. git log (最近 20 コミット) → 繰り返し作業、回帰パターン
5. Known Issues → TODO, FIXME, HACK 収集
```

**各 Problem に Forces 定義 (最低 2個)**:

Forces とは **互いに衝突する制約** です。
例: 「Hook は速くなければならない(F1: Latency)が、正確な判断をしなければならない(F2: Accuracy)」

```markdown
### Problem: {ID} — {Title}

**Statement**: {一文}

**Forces** (衝突する制約):

- **F1**: {制約 1} — Evidence: {根拠}
- **F2**: {制約 2} — Evidence: {根拠}
- _(F1 と F2 がなぜ同時充足が困難か説明)_

**Current State**: {現在どのように (未) 対処しているか}
```

### Part C: Problem-Module Hypothesis

OSS モジュールがどの Problem を解決できるか仮説を立てる:

```markdown
| Problem | OSS モジュール (仮説) | 根拠 | Phase 2 探索優先順位 |
| ------- | --------------------- | ---- | :------------------: |
```

→ Phase 2 では仮説にマッピングされたモジュールを **優先探索** (全数調査 → 集中調査)

**成果物**: `reconnaissance.md` (テンプレート: `templates/reconnaissance.template.md`)

---

## Phase 2: Decision Archaeology (ADR + Forces + Mechanism)

> **目的**: 各設計決定を「なぜこの方式か」まで逆追跡して文書化

### Decision 分析テンプレート

各 Decision について以下の5セクションを作成します:

#### 1. Problem & Forces

```markdown
### Problem: {Problem IDから参照}

**Forces**:

- **F1**: {制約 1} — Evidence: {OSS コード/ドキュメント根拠}
- **F2**: {制約 2} — Evidence: {OSS コード/ドキュメント根拠}
```

#### 2. Decision & Alternatives

```markdown
### Decision: {決定名}

**Chosen**: {選択された方式}
**Why This Way**: {Forces 解決方式の説明}

**Alternatives Considered** (最低 1個):
| 代替案 | 却下理由 | Evidence |
|------|----------|----------|
| {代替案 A} | {Forces の1つを解決できない} | {根拠} |
```

#### 3. Mechanism (v3 の GoF ディテール維持)

```markdown
### Mechanism

- **Symbol**: {関数名/クラス名} ← Primary Identifier
- **Module**: {モジュール名}
- **File**: {ファイルパス}

**Interface**:

- Input: {型/シグネチャ}
- Output: {型/戻り値}

**How It Works**:

1. {ステップ}: {説明} + コードスニペット
2. ...
```

#### 4. Consequences (ATAM-lite)

```markdown
### Consequences

| タイプ      | 説明           | Evidence |
| ----------- | -------------- | -------- |
| ✅ Positive | {肯定的結果}   | {根拠}   |
| ⚠️ Negative | {否定的結果}   | {根拠}   |
| ↔️ Tradeoff | {トレードオフ} | {根拠}   |
```

#### 5. プロジェクト Relevance

```markdown
### プロジェクト Relevance

- **Problem Match**: {LK のどの Problem に該当するか}
- **Forces Match**: {F1/F2 が LK でも同一か}
- **Forces Mismatch**: {LK では異なる制約があるか}
- **Adaptation Needed**: {そのまま適用可能 / 変形必要 / 不適合}
```

### Evidence 強化ルール

**原則**: 「根拠を出典と共に提示できるか？」

| 許可                                             | 禁止                                         |
| ------------------------------------------------ | -------------------------------------------- |
| 「README に 'fault tolerance のため' と明示」    | 「このプロジェクトはモジュール性を重視する」 |
| 「try-catch 構造でステップ別隔離の意図を推論」   | 「拡張性に優れている」 (根拠なし)            |
| 「TODO: cache 追加すれば改善可能」 (コメント)    | 「99.9%→99.99% 可用性向上」                  |
| 「代替案 A は F2 を解決できない (コードで確認)」 | 「唯一の方法だった」                         |

**v4 追加ルール**:

- 各 Force にコード/ドキュメント根拠 **必須**
- 「Alternative Blindness」防止: 各 Decision に代替案 **最低 1個**
- 「Shallow Forces」防止: 「～が重要だ」だけでは **CRITICAL 違反**

**成果物**: `decisions.md` (テンプレート: `templates/decisions.template.md`)

---

## Phase 3: Adoption Engineering (TW Radar + Recipe)

> **目的**: 評価を超えて **具体的な適用レシピ** を提供

### Step 1: Context Comparison

```markdown
| 属性         | OSS ({name}) | プロジェクト            |   Gap   |
| ------------ | ------------ | ------------------------ | :-----: |
| Language     | {言語}       | TypeScript/Next.js             | {H/M/L} |
| Runtime      | {ランタイム} | Mobile (iOS/Android)     | {H/M/L} |
| Architecture | {パターン}   | Feature-First + React Hooks | {H/M/L} |
| Scale        | {規模}       | Solo dev + AI assisted   | {H/M/L} |
| Backend      | {方式}       | Supabase (PostgreSQL)    | {H/M/L} |
| Hook System  | {方式}       | Claude Code Hooks (.mjs) | {H/M/L} |
| Deployment   | {方式}       | App Store releases       | {H/M/L} |
```

### Step 2: Adoption Decision (ThoughtWorks Radar)

**Impact × Fit Matrix**:

```
              High Fit      Medium Fit     Low Fit
High Impact │  ADOPT       │  TRIAL        │  ASSESS
Medium      │  TRIAL       │  ASSESS       │  HOLD
Low Impact  │  ASSESS      │  HOLD         │  HOLD
```

| Decision   | 意味               | 行動            |
| ---------- | ------------------ | --------------- |
| **Adopt**  | 検証済み、即時適用 | Recipe 作成必須 |
| **Trial**  | 有望、非コアで試行 | Recipe 作成必須 |
| **Assess** | 調査価値あり       | Recipe 任意     |
| **Hold**   | 現時点で不適合     | Recipe 不要     |

### Step 3: Recipe (Adopt/Trial 必須)

**Pseudocode を書く理由**: v2 で Auto-generated Dart が Context Mismatch で失敗。
意図は明確に、実装は実行時点に。

````markdown
### Recipe: {Decision Name}

**Goal**: {一行の目標}

**Prerequisites**:

- {事前条件 1}
- {事前条件 2}

**Adaptation Notes**:

- {OSS と LK の差異に基づく変形事項}

**Steps** (Pseudocode):

1. {ステップ}: {説明}
   ```pseudo
   {擬似コード}
   ```
````

2. ...

**Verification**:

- [ ] {検証項目 1}
- [ ] {検証項目 2}

**Rollback**:

- {失敗時に戻す方法}

```

**成果物**: `adoption.md` (テンプレート: `templates/adoption.template.md`)

---

## Output Specification

### 成果物: 3個

```

docs/oss/{oss-name}/v4/
├── reconnaissance.md # Phase 1: OSS Context + Problem Registry + Hypothesis
├── decisions.md # Phase 2: Decision Archaeology (ADR+Forces+Mechanism)
└── adoption.md # Phase 3: TW Radar + Recipes

````

### カタログ: docs/oss/_catalog/catalog.json

```json
{
  "schema_version": "4.0",
  "description": "OSS Problem-Decision-Recipe Catalog",
  "last_updated": "ISO date",
  "entries": [
    {
      "id": "{kebab-case-id}",
      "problem": {
        "id": "{problem-id}",
        "title": "{問題タイトル}",
        "forces": ["{Force 1 要約}", "{Force 2 要約}"]
      },
      "decision": {
        "name": "{Decision 名}",
        "chosen": "{選択された方式}",
        "adoption": "adopt | trial | assess | hold",
        "context_fit": "high | medium | low",
        "impact": "high | medium | low"
      },
      "recipe": {
        "id": "{recipe-id または null}",
        "exists": true | false,
        "complexity": "low | medium | high"
      },
      "source": {
        "oss": "{oss-name}",
        "module": "{module-name}",
        "symbol": "{function/class name}",
        "file": "{relative path}"
      },
      "follow_up": {
        "status": "pending | in_progress | done | abandoned",
        "implemented_at": "{ファイルパスまたは null}",
        "implementation_path": "{実装パスまたは null}",
        "note": "{任意メモ}"
      },
      "analysis_path": "docs/oss/{oss}/v4/decisions.md#{anchor}",
      "analyzed_at": "{ISO date}"
    }
  ]
}
````

### カタログ同期ルール

> **SSOT 関係**: `decisions.md` + `adoption.md` が原本、`catalog.json` は派生インデックス

| ルール             | 説明                                                                     |
| ------------------ | ------------------------------------------------------------------------ |
| **作成時点**       | Phase 3 完了後                                                           |
| **データ出典**     | `problem`, `decision` → decisions.md, `recipe`, `adoption` → adoption.md |
| **follow_up 更新** | oss-analyzer 外部で手動更新 (適用時に作業者が直接編集)                   |
| **検証**           | Post-flight で decisions.md の Decision 数 == catalog.json の entries 数 |

---

## Anti-Patterns (v1~v3 の失敗 + v4 新規)

### v1~v3で学んだ Anti-Patterns (8個)

| Anti-Pattern                    | 発生バージョン | v4 での代替                         |
| ------------------------------- | -------------- | ----------------------------------- |
| **Grep-First Discovery**        | v2             | C4 軽量 Top-Down 探索               |
| **Line Number Worship**         | v2             | シンボル名 Primary、行番号は参考用  |
| **Philosophy Without Evidence** | v1             | 根拠必須、出典明示                  |
| **Evidence Without Philosophy** | v2             | Forces + Alternatives で Why を提供 |
| **Auto-Generated Dart**         | v2             | Pseudocode Recipe                   |
| **Phantom Metrics**             | v1             | 測定不可な数値は禁止                |
| **Document Inflation**          | v1-v2          | 3個の成果物を維持                   |
| **Analysis Without Adoption**   | v3             | Recipe + catalog.json 追跡          |

### v4 新規 Anti-Patterns (3個)

| Anti-Pattern              | 説明                                               | 違反レベル |
| ------------------------- | -------------------------------------------------- | ---------- |
| **Shallow Forces**        | 「～が重要だ」だけで Force 定義 (衝突する制約なし) | CRITICAL   |
| **Alternative Blindness** | Decision に代替案が0個 (「唯一の方法」)            | HIGH       |
| **Context Copying**       | OSS コードをそのままコピーして Recipe に含む       | HIGH       |

---

## Usage

```bash
# 基本分析
/oss-analyzer --source {oss-sources-path}

# 特定の問題に集中
/oss-analyzer --source {path} --problem {problem-id}

# 特定領域に集中
/oss-analyzer --source {path} --focus {area}

# OSS スキャンのみ (Problem Discovery 省略)
/oss-analyzer --source {path} --oss-only

# キャッシュ無視で再分析
/oss-analyzer --source {path} --force
```

### オプション

| オプション        | 説明                                          | 必須 |
| ----------------- | --------------------------------------------- | :--: |
| `--source <path>` | OSS ソースパス                                |  ✅  |
| `--problem <id>`  | 特定 Problem に集中分析                       |      |
| `--focus <area>`  | 特定領域に集中分析                            |      |
| `--oss-only`      | OSS スキャンのみ実行 (Problem Discovery 省略) |      |
| `--force`         | キャッシュ無視で再分析                        |      |

---

## Version History

| バージョン | 日付       | 核心変更                                                                         |
| ---------- | ---------- | -------------------------------------------------------------------------------- |
| v4.0.0     | 2026-02-07 | Problem-Decision-Recipe フレームワーク: Forces+Alternatives+Recipe, catalog.json |
| v3.0.0     | 2026-02-06 | C4+GoF+ATAM+TW Radar, 3個の成果物, シンボル中心                                  |
| v2.0.0     | 2026-02-06 | 行番号中心のメカニズム抽出 (deprecated)                                          |
| v1.0.0     | 2026-02-05 | 抽象的哲学抽出 (deprecated)                                                      |
