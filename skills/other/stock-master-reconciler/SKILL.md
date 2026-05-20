---
name: stock-master-reconciler
description: ARIA における「マスタ（stocks_master.parquet）」の統合・名寄せ・生存判定・属性継承を統治するための専門スキル。
---

# stock-master-reconciler

ARIA プロジェクトの心臓部である `stocks_master.parquet` の整合性を維持し、EDINET（SSOT: 法論）と JPX（補完: 運論）のデータを工学的に統合するための知識体系です。

## 1. 統治の 5 つの鉄則 (The 5 Sovereign Laws)

1.  **EDINET SSOT (真実の源泉)**: 同一銘柄が両方に存在する場合、情報の鮮度が高い EDINET データを「絶対正」とし、JPX 側の重複レコード（普通株式）は物理的に破棄する。また、EDINET側が「非上場」と判定した場合は JPX に存在したとしても強制的に `is_active=False` とする「絶対優先回路」を設ける。
2.  **JPX 補完原則**: ETF, REIT, PRO Market 等、書類提出義務がなく EDINET に現れない銘柄は、JPX 側の属性を「正」として受容する。
3.  **Identity Bridging (身分ブリッジ)**: 証券コード (`code`) をキーに EDINET コードリストから `edinet_code` や `jcn` を逆引き（Bridge Fill）し、同一銘柄を単一の `identity_key` (JCN優先) に強制集約する。
4.  **Immutability of Existence (存在の不変性)**: 一度マスタに登録された銘柄は物理削除せず、`is_disappeared=True` かつ `is_active=False` として「消失の事実」を記録し続ける。
5.  **Normalization First (先制正規化)**: すべての証券コードは、ソースから抽出された直後に 5 桁化（末尾 0 付与）およびプレフィックス (`JP:`) 強制付与を行い、マッチング不一致を根絶する。

## 2. 具体的統合シナリオ (Reconciliation Scenarios)

### シナリオ A: 普通株式の重複（トヨタ自動車）
- **状況**: EDINET リストに `E02144 / JP:72030` が存在。JPX Excel にも `JP:72030` が存在。
- **挙動**:
    1.  JPX 側の `JP:72030` をロード。
    2.  `IdentityBridger` が 証券コードから `E02144` を逆引きし、一時的な `edinet_code` を付与。
    3.  同一 `edinet_code` のグループとして EDINET 側の属性を優先し、JPX 側の重複分を破棄。
    4.  JPX 由来の「業種コード」「市場区分」のみを EDINET レコードに「承継」させる。

### シナリオ B: 特殊銘柄の受入（ARIA ETF）
- **状況**: EDINET リストには存在しない。JPX Excel に `JP:13010` (Market: ETF) が存在。
- **挙動**:
    1.  `market` カラムに `ETF` が含まれるため、Disposal Rule (破棄ルール) の対象外となる。
    2.  `edinet_code` が NULL のまま、`code` を `identity_key` として新規登録。
    3.  `is_active=True`, `is_listed_edinet=False` としてマスタに追加。

### シナリオ C: 優先株の親子関係（伊藤園優先）
- **状況**: JPX Excel に `JP:25935` (優先株) が存在。
- **挙動**:
    1.  証券コードの末尾が `0` ではないことを検知。
    2.  上 4 桁 `2593` に末尾 `0` を付与した `JP:25930` を生成。
    3.  `parent_code` カラムに `JP:25930` を記録し、普通株との構造的関連性を保持。

### シナリオ D: 銘柄の消失（上場廃止後）
- **状況**: 既存マスタに `JP:88880` が存在。しかし、今回の EDINET および JPX 両リストから `JP:88880` が消失。
- **挙動**:
    1.  `LifecycleManager` が、前回のマスタにはあったが今回の最新入力に無いことを検知。
    2.  当該レコードに対し `is_disappeared=True`, `is_active=False` をセット。
    3.  「かつて存在した」という事実をマスタに永続化。

## 3. データ構造: JPX Definitions と SCD Type 2
業種コードや規模区分などは、名称の揺れを防ぐため `jpx_definitions.parquet` という「次元テーブル」で一括管理する。マスタには「コード」のみを保持し、解釈は定義ファイルに委ねる。
これらは Slowly Changing Dimension (SCD) Type 2 を採用し、`valid_from` (開始日) と `valid_to` (終了日) の境界値を厳格管理する（旧区分は「昨日」で閉め、新区分は「今日」から開始することで期間の重複を論理的に排除する）。
