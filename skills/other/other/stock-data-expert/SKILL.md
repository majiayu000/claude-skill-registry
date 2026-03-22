---
name: stock-data-expert
description: 日本の証券データ（JPX/EDINET）のドメイン知識と、ARIA 規格への正規化・整合性管理の専門スキル。
---
# 証券データ・エキスパート (Stock Data Expert)

ARIA における「証券データの真実」を管理するためのドメイン知識とツールを提供します。

## 1. 証券コードの 5 桁正規化と SICC ルール
あらゆる入力ソースからの証券コードを 5 桁に統一し、SICC（### 1. Identity Bridging (証券コードと EDINET コードの架け橋)
- **原則**: EDINET コードリストを主軸とし、JPX 証券コードを Bridge Fill 処理で紐付ける。
- **名寄せキー**: `edinet_code.fillna(code)` を `identity_key` として使用し、物理的なレコード統合を強制する。詳細は [stock-master-reconciler](file:///Users/yoshi_dai/repos/ARIA/.agent/skills/stock-master-reconciler/SKILL.md) を参照。
）の採番ルールに基づいて親子関係を定義します。
- **5 桁正規化 & 国籍プレフィックス**: 4 桁コードには末尾に `0` を付与し、さらに「国籍プレフィックス（例: `JP:`）」を強制付与する。これは全 Pydantic モデル（生データ、マスタ、履歴）のバリデータとして物理的に強制される。英文字を含むコード（例：`145A0`）も同様に扱う。
- **親子紐付け (Preferred Stock Linkage)**: 
    - 5 桁目が `0` 以外（5, 6, 7, 8, 3, 4）の銘柄は「種類株」と判定。
    - 上 4 桁が共通する `0` 銘柄（普通株）を `parent_code` として自動的にリンク。
    - 種類株は親銘柄から `edinet_code` や `jcn` を継承することを許可する。
- **Decoupled Master Architecture (生殺与奪権の分離)**:
    - **EDINET**: 銘柄の「存続 (is_active)」に関する唯一の主権者。Harvester-Merger がこの同期を司る。
    - **JPX**: 銘柄の「属性 (sector/market)」の補完ソース。Market Pipeline がこの更新を司る。
    - 両者は `sync_master` フラグおよびモードにより疎結合に保たれ、EdinetEngine が無効な環境でも JPX 属性の更新（既存銘柄への適用）は安全に行われるべきである（`discover_edinet_code` の Null ガードを遵守）。

## 2. 属性解決とリコンシリエーション (Hierarchy of Truth)
[ReconciliationEngine.update_stocks_master](file:///Users/yoshi_dai/repos/ARIA/data_engine/reconciliation_engine.py) の実装に基づき、以下の優先順位を遵守します。
- [stock-master-reconciler](file:///Users/yoshi_dai/repos/ARIA/.agent/skills/stock-master-reconciler/SKILL.md): マスタ統合と名寄せの「5つの鉄則」の統治。
- [company-name-historian](file:///Users/yoshi_dai/repos/ARIA/.agent/skills/company-name-historian/SKILL.md): 漢字商号の変遷管理。
1. **EDINET Document API (Real-time)**: IPO 銘柄の `secCode` から `edinetCode/jcn` を逆引きする最優先ソース。
2. **EDINET / Catalog (Regulatory)**: 会社名および公的ステータスの正解。
3. **JPX Master (Market)**: 業種区分および市場名の補完ソース。

## 3. 登録ガードと IPO 自動発見 (Registration Guard & Discovery)
二重登録（証券コード不明レコードの増殖）を物理的に防ぐため、以下のプロトコルを適用します。
- **IPO Discovery**: JPX にのみ存在する JCN 不明銘柄に対し、直近 30 日間の書類一覧 API をスキャン。`secCode` が一致する書類から識別子を動的に抽出。
- **Registration Guard**: 書類 API でも識別子が発見できない一般事業会社は、マスタへの登録を「保留（スキップ）」する。
- **例外**: ETF / REIT / PRO Market は EDINET 名簿対象外のため、JPX 情報のみでの登録を許可。
- **Centralized Judgement (Targeting SSOT)**:
    - 市場監視における解析対象の選定は、[FilteringEngine](file:///Users/yoshi_dai/repos/ARIA/data_engine/engines/filtering_engine.py) の `TARGET_DOC_TYPES` 等の物理コード定義に基づき、ARIA 規格として一元的に実施すること。

## 4. 履歴の自己修復 (History Self-Healing)
- **Status-based History**: `is_active` フラグの遷移に基づき、`LISTING` / `DELISTING` イベントを一貫して生成。
- **Kanji-based Name Tracking**: 社名変更履歴を「漢字名」のみで管理。カタログ（提出書類）に記録された漢字名のみをソースとすることで、歴史的事実としての正確性を担保する。
- **Chronological Reconstruction**: バックフィル（非時系列な書類取得）に対処するため、特定の銘柄コードに紐付く全書類を日付順に動的スキャンし、隣接する書類間での名称変化を検知して `NameEvent` を再構成する。
- **0000-00-00 Seed**: 社名変更履歴の起点としてシードレコードを注入。

## 5. 異常検知の閾値 (Anomaly Thresholds)
以下の状態を検知した場合、直ちに処理を停止し整合性を疑います：
- **指数構成銘柄 < 40件**: API エラーまたはデータ欠落の可能性。
- **bin=No への割り当て**: 証券コードの抽出失敗（NULL 非許容）。

## 詳細リファレンス
- [正規化ロジック詳細](references/RECONCILIATION_LOGIC.md)
- [ARIA データスキーマ定義](references/SCHEMA_DEFINITION.md): bin sharding 構造の定義
- [EDINET API V2 物理検証済み事実集](references/EDINET_API_FACTS.md): エンコーディング、レスポンスフィールド、opeDateTime等の実測値
