---
name: market-intelligence-scanner
description: |
  プロジェクト プロジェクトの docs/research/で競合分析と市場トレンドをスキャンして未定義機能候補を発見し docs/features/candidates/market/に生成するスキル。
  "競合機能分析", "未定義機能探し", "機能ギャップ分析", "市場トレンドスキャン", "新機能候補" などの要求でトリガーされる。
  候補管理サブコマンド: --accept, --reject, --defer, --list, --merge, --triage で候補状態を構造的に管理する。--force フラグで状態検証をバイパスした強制遷移をサポート。
doc_contract:
  review_interval_days: 90
---

# Market Intelligence Scanner

docs/research/ ディレクトリの競合分析、市場トレンド、ユーザー研究文書をスキャンして **まだ docs/features/に定義されていない機能候補**を自動的に発見し文書化するスキル。

**核心価値**: リサーチインサイト → 実行可能な機能候補変換

---

## Phase データ契約

> 各 Phaseの進入条件、産出物、不変条件を定義する。Phase 遷移時に必ず遵守する必要がある。

| Phase | 入力                    | 産出物              | 完了条件                |
| :---: | ----------------------- | ------------------- | ----------------------- |
|   0   | ユーザー要求            | scan_id             | scans[]に登録済み       |
|  1.0  | —                       | manifest            | `generated_at` < 24時間 |
|   1   | scan_context + manifest | scanned_docs[]      | len ≥ 1                 |
|   2   | index.md                | existing_features{} | 全体 Feature マッピング |
|   3   | scanned_docs + features | gaps[]              | フィルタリング完了      |
|  3.1  | gaps (sources==0)       | gaps + research     | 根拠 1+ 確保            |
|   4   | gaps                    | scored[]            | ICE 計算完了            |
|  4.1  | scored (C<5)            | scored (updated)    | 補強完了                |
|   5   | scored (top N)          | .md + .json         | **Evidence Gate** 通過  |
|   6   | —                       | completed           | phase=completed         |
|  6.1  | —                       | validation_result   | check スクリプト通過    |

**不変条件**:

- Phase N+1 進入前に Phase N 完了必須 (ただし、3.1/4.1は条件付き)
- Phase 5 進入時: **Evidence Gate** + **WIP 制限** チェック
- Phase 6.1 完了時: `validation_result`を scan 項目に記録

---

## SSOT (Single Source of Truth)

```
assets/scan-status.json           → スキャン作業 + 候補状態 (SSOT)
docs/research/*.md Frontmatter    → リサーチメタデータ (SSOT)
docs/_manifests/research-manifest.json → Frontmatter キャッシュ (読み取り専用)
docs/features/candidates/market/  → 生成された候補文書
```

**原則**:

- スキャン/候補状態は `assets/scan-status.json`でのみ管理
- リサーチメタデータ: Frontmatter = SSOT, Manifest = キャッシュ
- Manifest 更新: `python scripts/generate_research_manifest.py`

> スキーマ: [scan-status-schema.json](references/scan-status-schema.json) (v4)
> Frontmatter スキーマ: [research-frontmatter.schema.json](../../../docs/_schemas/research-frontmatter.schema.json)

---

## トリガー条件

### スキャン (基本モード)

1. **機能ギャップ発見**: "競合にあって我々にない機能は何?"
2. **市場トレンド分析**: "市場トレンドベースで新機能探して"
3. **候補生成要求**: "機能候補生成して", "新機能アイデア"
4. **定期スキャン**: "market scan", "リサーチスキャン"
5. **深層調査要求**: "deep researchで分析して", `--deep` オプション使用

### 候補管理 (サブコマンド)

> 詳細プロトコル: [subcommand-protocol.md](references/subcommand-protocol.md)

| コマンド                     | 説明                                                                  |
| ---------------------------- | --------------------------------------------------------------------- |
| `--accept <id> [id2 ...]`    | 候補承認 (複数対応) → `/feature-architect` 自動呼び出し → `converted` |
| `--reject <id> [id2 ...]`    | 候補却下 (複数対応、共通事由)                                         |
| `--defer <id> [id2 ...]`     | 候補保留 (複数対応、共通事由/時期)                                    |
| `--force --<cmd> <id> [...]` | 状態検証バイパスして強制遷移 (merged 除く、ユーザー確認必須)          |
| `--list`                     | 候補現況テーブル出力                                                  |
| `--merge <id> <feature-id>`  | 既存 Featureに統合 (単一のみ)                                         |
| `--triage`                   | pending_reviewを ICE順ソート + 自動分類提案 + Tier別一括実行          |

### Deep Research 自動トリガー

| 条件                | Phase | 自動/手動 |
| ------------------- | :---: | :-------: |
| 根拠文書 0件        |  3.1  |   自動    |
| ICE Confidence < 5  |  4.1  |   自動    |
| `--deep` オプション | 全体  |   手動    |

---

## ワークフロー

### Phase 0: スキャン作業登録

スキャン開始 **前**に `assets/scan-status.json`の `scans[]`に作業を登録する:

```json
{
  "scan_id": "scan-{YYYY-MM-DD}",
  "phase": "scanning",
  "focus": "{集中領域または null}",
  "target_competitor": "{特定競合または null}",
  "created_at": "{現在時刻}",
  "started_at": "{現在時刻}"
}
```

### Phase 0.5: Competitor Gap Ingestion (競合ギャップ収集)

> 選択的段階. `docs/analysis/gap-candidates.json`が存在し有効な場合のみ実行.

**入力**: `docs/analysis/gap-candidates.json` (competitive-tracker 産出物)

**実行条件**:

1. ファイル存在確認
2. Freshness 検証: `generated_at` + `freshness_ttl_days` > now
3. スキーマ検証: `schema == "gap-candidates-v1"`

**Staleness 検出時**:

- `competitor-registry.json` mtime > `gap-candidates.json` generated_atの場合
- ⚠️ 警告出力 + `node .claude/scripts/audit-runner.mjs` 自動実行 ($0 コスト)
- 再生成された gap-candidates.jsonで続行

**処理ロジック**:

1. `recommended_action == "candidate_creation"` AND `already_tracked == false` フィルター
2. 各 gapに対して scan-status.json 既存候補と重複検査:
   - comp_id で `competitor_gap_ref` マッチング (正確)
   - 名前 Sørensen–Dice 類似度 >= 0.4 (fuzzy)
   - 重複発見時: 既存候補に `competitor_evidence` 追加 (source_type → "hybrid")
3. 重複でない gap → 候補生成待ち行列に追加
4. Phase 5で研究ベース候補と共に生成

**生成される候補の追加フィールド** (v4 スキーマ):

- `source_type: "competitor_gap"`
- `competitor_gap_ref: "comp-025"`
- `competitor_evidence: { gap_severity, app_count, apps, opportunity_score, is_industry_standard }`

**`opportunity_score: null` 処理**: gap-candidates.jsonで JTBD マッチングがないギャップは `opportunity_score: null`で伝達される. この場合:

- 候補生成時 `opportunity_score`を ICEの `impact` フィールドに直接マッピングしない
- 候補の ICE impactは別途算出 (研究証拠ベース)
- `competitor_evidence.opportunity_score`は null のまま保存 (情報損失防止)

**候補文書テンプレート拡張** (competitor_gap 専用セクション):

- "## Competitor Analysis" セクション追加
- 競合別実装深度、我々との差異点記述
- evidence[] 配列に `type: "competitor_evidence"` 項目自動追加

**WIP 制限**: 既存ルール維持 (max 10 pending_review, max 5 per scan)

- gap 候補も WIP カウントに含まれる

### Phase 1.0: Manifest 鮮度チェック

> ⚠️ **必須**: Phase 1 進入前に Manifest キャッシュの鮮度を確認する.

1. `docs/_manifests/research-manifest.json`の `generated_at` 確認
2. 24時間超過時: `python scripts/generate_research_manifest.py` 実行して再生成
3. ファイル未存在時: 同じスクリプトで初期生成

### Phase 1: リサーチ文書収集

**3段階 fallback 戦略**で文書を収集する:

1. **Manifest キャッシュ活用** (推奨): `research-manifest.json`の `scanner_hints`でフィルタリング
   - `scannable`, `scan_priority`, `keywords`, `exclude_sections` フィールド活用
2. **Frontmatter 直接パース**: Manifest がないか古い場合、各文書の YAML Frontmatter を直接パース
3. **Glob パターン**: レガシー文書対応 — `docs/research/competitor*.md`, `*market*.md`, `*feature*.md` など

**フィルタリング基準**: `scanner_hints.scannable`, `scan_priority`, カテゴリ、競合言及有無、キーワードマッチング

### Phase 2: 既存機能マッピング

```bash
Read: docs/features/index.md
Glob: docs/features/*/index.md
```

各 Featureの核心キーワードを収集し、同義語/類似語マッピングを生成する。

> キーワードマッピング: [keyword-mapping.json](references/keyword-mapping.json) (SSOT), [keyword-mapping.md](references/keyword-mapping.md) (ビューア)

### Phase 3: ギャップ識別

リサーチで発見された機能言及を既存 Featureと対照して未定義ギャップを識別する。

**フィルタリング基準**:

| 基準      | 通過条件             | 却下条件                          |
| --------- | -------------------- | --------------------------------- |
| 関連性    | 韓国語学習と直接関連 | 一般アプリ機能 (例: ダークモード) |
| 差別化    | 競争優位可能         | 既に飽和した機能                  |
| 実現性    | 実装可能             | 大規模チーム必要                  |
| Japan-Fit | 日本市場にアピール   | 日本市場不適合                    |

### Phase 3.1: リサーチギャップ Deep Research (条件付き)

**トリガー**: Phase 3で根拠文書 0件の領域発見または `--deep` オプション

1. `deep-research --provider google` スキル呼び出し (韓国語学習アプリ + Japan-First コンテキスト)
2. 必須調査項目: 競合実装方式、ユーザーニーズ、日本市場適合性、実装複雑度
3. 結果を `gap.deep_research_result`に保存して Phase 4で活用

### Phase 4: 候補スコアリング

> 詳細: [scoring-criteria.md](references/scoring-criteria.md)

**ICE v3 加重平均**:

```
Base ICE = (Impact × 0.4) + (Confidence × 0.3) + (Effort × 0.3)
Japan Bonus = max(0, (Japan-Fit - 5)) × 0.2
Final Score = clamp(Base ICE + Japan Bonus, 0, 10)
```

| 要素           | 重み | 評価基準                               |
| -------------- | :--: | -------------------------------------- |
| **Impact**     | 40%  | KPI 寄与度 (リテンション, 転換率, LTV) |
| **Confidence** | 30%  | 根拠信頼度 (出典数, データ品質)        |
| **Effort**     | 30%  | 実装複雑度 (逆算: 易しいほど高い)      |

### Phase 4.1: Low Confidence 補強 (条件付き)

**トリガー**: ICE Confidence < 5の候補

1. `deep-research --provider google` スキル呼び出し (市場妥当性検証フォーカス)
2. 必須調査: ユーザーニーズ, 競合事例, 成功指標, Japan 適合性
3. Confidence 再計算後 `deep_research_sources`に出典追加

### Phase 5: 候補文書生成 + 状態登録

> ⚠️ **Evidence Gate**: この Phase 進入時に次の条件を検証する.

**Evidence Gate (遮断条件)**:

1. `evidence` 配列が空 → **候補生成遮断**
2. `evidence` 中 `quantitative`/`competitor_evidence` 0件 → ⚠️ 警告
3. すべての evidenceの `strength`が `weak` → ユーザー確認要求

**WIP Gate**: pending_review 候補が 10個以上なら警告 + `--triage` 実行要求

**生成プロセス**:

1. **ファイル名**: `YYYY-MM-DD-kebab-case-feature-name.md`
2. **位置**: `docs/features/candidates/market/`
3. **テンプレート**: [feature_candidate_template.md](../../../docs/_templates/feature_candidate_template.md)
4. **Write ツール**で候補文書自動生成
5. **Optimistic Locking**で `scan-status.json` 安全更新:
   - Read → メモリ修正 → Re-Read 比較 → Write (不一致時リトライ)
6. 候補エントリに `evidence[]`, `success_metrics[]` 含む (v3 スキーマ)

**単一スキャン最大候補**: 5個 (ICE 上位 5個のみ即時生成, 残りは待機)

### Phase 6: スキャン完了

1. `scan-status.json`の該当スキャン phase → `"completed"` 更新
2. `completed_at`, `scanned_docs_count`, `candidates_generated` 自動記録

### Phase 6.1: 自動検証

> ⚠️ Phase 6 完了直後に必ず実行する.

```bash
python3 .quality/scripts/check_scan_status.py
```

1. 検証スクリプトを実行してデータ整合性確認
2. 結果を scan 項目の `validation_result`に記録:
   ```json
   {
     "validation_result": {
       "passed": true,
       "errors": 0,
       "warnings": 2,
       "checked_at": "{時刻}"
     }
   }
   ```
3. errors > 0ならユーザーに警告 + 手動修正要求

---

## 出力形式

> 詳細テンプレート: [output-format.md](references/output-format.md)

スキャン完了後、結果をマークダウン形式で報告する. 含む項目:

- スキャンメタデータ (スキャン日, 分析文書数, 発見候補数, Deep Research 実行有無)
- 候補要約テーブル (ICE Score, Japan-Fit 順)
- 新規候補詳細 (Problem, Solution, Evidence, ICE, Japan-Fit)
- 次のステップ案内 (サブコマンド使用法)

**⚠️ ID 表示必須ルール**: 候補を表示する **すべてのテーブル**に `ID` カラムを必ず含む.

- IDは `candidate_id`から日付接頭辞(`YYYY-MM-DD-`)を削除した **短縮 ID**
- ユーザーが `--accept`, `--reject` などサブコマンドにすぐコピーして使用できる必要がある
- 適用対象: `--list`, `--triage`, スキャン結果要約, すべての候補テーブル出力

**⚠️ バッチ構文必須ルール**: **すべての出力**の "次のステップ" セクションに複数 ID 構文を必ず含む.

- `--accept`, `--reject`, `--defer`に `[id2 ...]` 表記必須
- 実際の pending 候補 IDを活用した `bash` 例示ブロック含む必須
- `--merge`は単一のみ可能という点を明示
- 適用対象: `--list`, スキャン結果要約, `--triage` など "次のステップ"が含まれるすべての出力

---

## 候補状態管理

> 詳細: [candidate-lifecycle.md](references/candidate-lifecycle.md)

```
pending_review → approved → converted
              ↘ rejected        ↘ reverted → pending_review
              ↘ merged (Terminal)
              ↘ deferred → pending_review / rejected

[--force] merged 除くすべての状態 → 対象状態 (ユーザー確認必須)
```

**核心ルール**:

- すべての状態変更時 `history[]`に append 必須
- `from_status: null`は history[0] (初期生成)でのみ許可
- `triggered_by`: `market-intelligence-scanner` | `manual` | `feature-architect` | `feature-pilot`
- 検証: `python3 .quality/scripts/check_scan_status.py`

---

## WIP 制限

| ルール               |    値    | 超過時行動                                                        |
| -------------------- | :------: | ----------------------------------------------------------------- |
| pending_review 最大  | **10個** | Phase 5 進入時に警告 + `--triage` 実行要求                        |
| 単一スキャン最大候補 | **5個**  | ICE 上位 5個のみ即時生成, 残りは待機                              |
| WIP 超過時メッセージ |    —     | `⚠️ pending_review {n}個 (制限: 10). --triageで整理してください.` |

---

## リサーチキーワードマッピング

> SSOT: [keyword-mapping.json](references/keyword-mapping.json)
> ビューア: [keyword-mapping.md](references/keyword-mapping.md) (読み取り専用)

10個ドメイン × キーワード × 重みでリサーチ文書を機能ドメインに自動マッピングする.
未マッチングキーワードは `undefined_domains`に自動登録されて新規機能候補検出に活用される.

---

## 連携スキル/エージェント

| ツール                              | 役割                        | 呼び出し条件                   | 連動 |
| ----------------------------------- | --------------------------- | ------------------------------ | :--: |
| `deep-research` (--provider google) | リアルタイムWebリサーチ     | Phase 3.1, 4.1 または `--deep` | 自動 |
| `feature-architect`                 | 承認 → CONTEXT 生成         | `--accept` 実行時              | 自動 |
| `priority-analyzer`                 | RICE ベース全体優先順位評価 | 候補生成完了後                 | 手動 |
| `research-gap-analyzer`             | 根拠不足追加調査            | ICE Confidence < 5             | 代替 |

---

## 参照文書

| 文書                                                                                    | 用途                                        |
| --------------------------------------------------------------------------------------- | ------------------------------------------- |
| [scoring-criteria.md](references/scoring-criteria.md)                                   | ICE v3 + Japan-Fit スコアリング基準         |
| [keyword-mapping.json](references/keyword-mapping.json)                                 | キーワードマッピング SSOT (機械判読)        |
| [keyword-mapping.md](references/keyword-mapping.md)                                     | キーワードマッピングビューア (読み取り専用) |
| [candidate-lifecycle.md](references/candidate-lifecycle.md)                             | 候補状態遷移 + History ルール               |
| [subcommand-protocol.md](references/subcommand-protocol.md)                             | サブコマンドプロトコル (--accept など)      |
| [output-format.md](references/output-format.md)                                         | スキャン結果出力テンプレート                |
| [scan-status-schema.json](references/scan-status-schema.json)                           | 状態ファイル JSON スキーマ (v4)             |
| [feature_candidate_template.md](../../../docs/_templates/feature_candidate_template.md) | 候補文書テンプレート                        |

---

## 使用例

### スキャンモード

```bash
/market-intelligence-scanner                                  # 全体スキャン
/market-intelligence-scanner --deep                           # Deep Research 強制
/market-intelligence-scanner --focus=gamification --deep       # 特定領域深層
/market-intelligence-scanner --competitor=duolingo             # 特定競合集中
```

### 候補管理モード

```bash
/market-intelligence-scanner --list                                              # 現況照会
/market-intelligence-scanner --triage                                             # 一括分類 + Tier別実行
/market-intelligence-scanner --accept minimal-pair-pronunciation-drill            # 単一承認
/market-intelligence-scanner --accept ai-error-pattern-tracker ai-safety-moderation-system context-based-phrase-cards  # 複数承認
/market-intelligence-scanner --reject drama-comprehension-badge debate-discussion-mode     # 複数却下
/market-intelligence-scanner --defer ai-companion-characters speed-quiz-fluency-mode       # 複数保留
/market-intelligence-scanner --merge streak-repair-system 030-streak-freeze-system         # 統合 (単一のみ)
/market-intelligence-scanner --force --defer ai-error-pattern-tracker vocabulary-notebook   # 強制保留 (状態無関)
/market-intelligence-scanner --force --reject speaking-output-enforcement                  # 強制却下
```

---

## 注意事項

1. **SSOT 遵守**: スキャン/候補状態は **必ず** `assets/scan-status.json`でのみ管理
2. **スキーマ遵守**: 状態ファイル修正時 `scan-status-schema.json` (v4) 参照必須
3. **Evidence-first**: 根拠のない候補生成禁止 (Evidence Gate)
4. **WIP 制限**: pending_review 10個, 単一スキャン 5個超過禁止
5. **リソース現実性**: 大規模チーム必要機能は自動フィルタリング
6. **Japan-First**: 日本市場と無関係な機能は低い優先順位
7. **重複防止**: 既存 docs/features/と明示的比較
8. **品質 > 量**: 10個曖昧な候補より 3個明確な候補
9. **出典明示**: すべての候補は根拠文書リンク必須
10. **Manifest = キャッシュ**: 直接修正禁止, `python scripts/generate_research_manifest.py`で更新

---

## ファイル構造

```
.claude/skills/market-intelligence-scanner/
├── SKILL.md                              # このファイル (~350行)
├── assets/
│   └── scan-status.json                  # スキャン作業 + 候補状態 (SSOT)
└── references/
    ├── scoring-criteria.md               # ICE v3 + Japan-Fit 基準
    ├── keyword-mapping.json              # キーワードマッピング SSOT (機械判読)
    ├── keyword-mapping.md                # キーワードマッピングビューア (読み取り専用)
    ├── candidate-lifecycle.md            # 候補状態遷移ルール
    ├── subcommand-protocol.md            # サブコマンドプロトコル
    ├── output-format.md                  # スキャン結果出力テンプレート
    └── scan-status-schema.json           # 状態ファイル JSON スキーマ (v4)
```

**検証スクリプト**: `.quality/scripts/check_scan_status.py`

---

## Changelog

| バージョン |    日付    | 変更内容                                                                                                                                                                                                                                                                           |
| :--------: | :--------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    5.2     | 2026-01-27 | **`--force` フラグ**: 状態検証バイパス強制遷移対応. `merged` 除くすべての状態で `--accept`/`--reject`/`--defer` 可能. Historyに `[FORCE]` 接頭辞自動記録. ユーザー確認必須                                                                                                         |
|    5.1     | 2026-01-26 | **バッチ処理**: `--accept`, `--reject`, `--defer` 複数 ID 対応. `--triage` Tier別一括実行プロトコル追加. Partial Success エラー処理                                                                                                                                                |
|    5.0     | 2026-01-26 | **全面再設計**: Phase データ契約導入, Evidence Gate + WIP 制限追加, ICE v3 加重平均公式, Phase 6.1 自動検証, SKILL.md アーキテクチャ分離 (1012行→350行) — candidate-lifecycle.md, subcommand-protocol.md, output-format.md, keyword-mapping.json 抽出. `--triage` サブコマンド新規 |
|    4.2     | 2026-01-26 | サブコマンド体系導入: `--accept`, `--reject`, `--defer`, `--list`, `--merge`                                                                                                                                                                                                       |
|    4.1     | 2026-01-26 | Deep Research 自動連動: Phase 3.1/4.1, `--deep` オプション                                                                                                                                                                                                                         |
|    4.0     | 2026-01-26 | 完全自動化: Phase 5-6 AI 自動文書生成 + 状態更新                                                                                                                                                                                                                                   |
|    3.0     | 2026-01-26 | Frontmatter ベース SSOT 転換: Phase 1 3段階構造化                                                                                                                                                                                                                                  |
|    2.1     | 2026-01-25 | Research Manifest 連動                                                                                                                                                                                                                                                             |
|    2.0     | 2026-01-25 | 状態トラッキングシステム導入                                                                                                                                                                                                                                                       |
|    1.0     | 2026-01-25 | 初期バージョン                                                                                                                                                                                                                                                                     |
