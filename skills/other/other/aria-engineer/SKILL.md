---
name: aria-engineer
description: ARIA プロジェクトにおける技術的真実、データ整合性、および厳格な実装のためのエンジニアリング規範。
---
# ARIA エンジニア (ARIA Engineer)

このスキルは、ARIA プロジェクトにおける技術的判断の「憲法」です。

## 1. 行動規範 (Manifesto)
- **事実の優位性**: 物理的なコード、型定義、実行ログに基づいた「事実」のみを根拠とする。
- **異常値への執着**: 「0件」や「空の結果」が正常なゼロか異常なゼロかを数学的に証明できるまで停止しない。
- **FMEA の義務**: 重大な変更前には必ず故障モードとその影響を洗い出す。

## 2. 物理的な掟 (Physical Facts)
- **RaW-V (Read-after-Write Verification)**: 破壊的更新前には必ず CatalogManager のスナップショット機能を実行。
- **NaN / Null Integrity**: pandas 由来の NaN が Pydantic モデルの文字列フィールドを破壊するのを防ぐため、`field_validator` による強制変換を必須とする。
- **Network Stability**: 外部通信を伴う処理では [network_utils.patch_all_networking](file:///Users/yoshi_dai/repos/ARIA/data_engine/core/network_utils.py) の適用を必須とする。
- **Buffered Incremental Sync (1h Lookback)**: API V2 の増分同期 (`opeDateTime`) 時は、反映遅延（Visibility Lag）を考慮し、必ず **1時間のルックバックバッファ** を適用して再スキャンすること。重複はカタログの `drop_duplicates(keep="last")` で物理的に解消する。
- **PyArrow Schema Enforcement (金型アーキテクチャ)**: 全 Parquet 書き出しは `models.py` の `ARIA_SCHEMAS` レジストリから導出した明示スキーマを適用すること。`to_parquet()` を無スキーマで呼ぶことは**永久に禁止**。動的スキーマ (Bin/指数) は例外として明記すること。
- **Initialization API Economy (sync_master 防衛)**: 複数 pod/job が並列起動する際、全台が金融庁リストを同期するのはリソースの無駄である。`CatalogManager` 初期化時はマージャー/監査用途以外では必ず `sync_master=False` を指定し、API コールを物理的に遮断すること。
- **Historical Boundary Guard (10y - 5d Rule)**: EDINET API V2 の公文書保持期限（10年）において、APIサーバーの更新遅延や時差によるデータ消失を「物理的事実」として想定し、バックフィルおよび監査の下限値には必ず **5日間の安全マージン（Safety Buffer）** を適用すること。これにより、境界線上の書類を消滅前に確実に ARIA レイクハウスへ救出・永続化する。
- **NaN Truthy Protection (Audit Logic)**: pandas 由来の `NaN` は Python の真偽値判定において `True` と評価される。物理ファイルの存在監査（Layer 2）等において、パスの有無を判定する際は、単なる Truthy 判定を避け、必ず `pd.isna()` を用いた明示的な欠損値チェックを行うこと。これにより、存在しないファイルに対する偽陽性（誤検出）を物理的に遮断する。
- **API保持期限外の保護**: 10年以上前の古いレコードでAPIフラグが失われている場合、カタログ上の既存パス（事実）を絶対期待値としてロードし、API消滅による不当な欠損判定を防ぎ、資産を永続的に保護する。
- **因果の連鎖 (Causal Continuity)**: 物理層(Layer 2)での不整合修正（亡霊除霊や削除）は、必ずカタログステータスの無効化を伴い、下流の分析マスタ層(Layer 3)での「外科的切除（パージ）」を自動誘発させ、システム全域の一貫性を保つ。
- **監査の安全性 (Read-only Audit Principles)**:
    - 通常の監査モードは、データ変更を行わない「純粋関数的」な存在であること。
    - 破壊的または上書きを伴う「自己修復（repair）」は、明示的なフラグ条件下でのみ実行されることをコードレベルで保証する。
- **Global Namespacing (Nationality Tags)**:
    - 市場データとの衝突を物理的に防ぐため、全証券コードに対し `JP:` プレフィックスを強制する。
    - 取得元の生データ（JPX/日経）にプレフィックスが含まれない場合、必ず `normalize_code(code, nationality='JP')` を通じて変換・付与すること。
    - 既存データ（Legacy）との照合時は、プレフィックスの有無に依存しない「プレフィックス耐性（Prefix-Tolerant）」ロジックを実装すること。
- **Double Truth Filtering (Judgement Centralization)**:
    - 書類の解析要否判定は、必ず [FilteringEngine](file:///Users/yoshi_dai/repos/ARIA/data_engine/engines/filtering_engine.py) を SSOT（唯一の真実）として行うこと。
    - 判定結果は必ず公的な物理コード（Doc/Ord/Form）を併記し、第三者が客観的に監査可能な状態（Fact-based Reporting）を保つこと。
- **Weight Normalization (Parallel Efficiency)**:
    - GitHub Actions 等の並列分散における「重み（Weight）」は、実際の計算コスト（120有報の解析 vs メタデータ保存のみ）の比率（現在は 50:1 程度）を物理的事実に基づいて定期的に校正（Calibration）すること。
- **Atomic Deferred Transaction (1コミット整合性)**:
    - データの保存（Bin）とメタデータ（Catalog）の更新は必ず `HfStorage.push_commit()` を用いて **1つのコミットにアトミックにまとめる** こと。
    - カタログの `processed_status` は、Bin への保存成功を確認してから初めて `success` へ昇格させること。これにより「カタログにはあるがデータがない」という不整合を物理的に遮断する。
- **Binning Normalization Guard (不変の分散キー)**:
    - `get_bin_id` の入力値（JCN, EDINET Code）には **必ず `strip()` を適用** すること。生データに含まれ得る空白による Bin 名の齟齬（"5 " vs "45"）を防ぎ、カタログ上の `bin_id` と実ファイルの Bin 名を 100% 一致させる。

## 3. 監査手法 (Audit Methodology)
- **モデル駆動型 4 層 11 項目の自動監査エンジン (スキーマ / 物理ファイル / 分析マスタ / API カタログ) 入口点**: [data_reconciliation.py](file:///Users/yoshi_dai/repos/ARIA/data_engine/services/data_reconciliation.py) がスキーマ照合、物理ファイル照合、分析マスタ照合、API カタログ照合の 4 層 11 項目を自動実行。
- **Mass-Scale Stress Test**: 1,000件規模の擬似レコードを用い、Parquet の物理的統合と bin への均等分散を検証する。
- **Kanji-based Name History Reconstruction**: 社名変更履歴は、全書類を日付順にスキャンして「漢字名」のみで変化を検知・再構成する。バックフィル時の非時系列取得に対しても、このアルゴリズムで論理的整合性を保証する。
- **Self-healing (Auto-retry)**: 過去の失敗・未完了書類を自動救済。
- **Extreme Integrity Audit**: 5層（スキーマ / 物理ファイル / 分析マスタ / API カタログ / 指数履歴）にわたるデータの自己治癒。
    - **Layer 1-5 Reconciliation**: [data_reconciliation.py](file:///Users/yoshi_dai/repos/ARIA/data_engine/services/data_reconciliation.py) による 5 層監査。
    - **HF Rollback**: 破損ファイル検知時、`api.list_repo_commits` で過去の正常バージョンを特定し自動復旧。
    - **Hybrid Regeneration**: ロールバック不能な Bin 破損時、カタログの `processed_status` を `pending` にリセットし、harvester による再生成を強制。
    - **Atomic Swap**: 修正データの書き戻しは、ローカルでの Parquet 生成・検証を経て、HF へのバッチコミットで行う。
    - **Bin-Assignment Identity**: Bin 分割は JCN (法人番号) 末尾 2 桁を最優先の分散キーとし、証券コードの有無・変更に依存しない物理配置を死守する。

## 4. 環境制御
- **CI 最適化**: ログの肥大化を防ぐため `HF_HUB_DISABLE_PROGRESS_BARS=1` および `TQDM_DISABLE=1` を強制する。

## 参照リソース
- [エンジニアリングパターン](references/patterns.md): FMEA、冪等性の具体例
- [技術用語翻訳ガイド](references/PEDAGOGICAL_GUIDE.md): 投資家向けの分かりやすい説明指針
- [SSOT 設定](file:///Users/yoshi_dai/repos/ARIA/data_engine/core/config.py): `aria_config.json` による一元管理モジュール
- [PyArrow スキーマ定義](file:///Users/yoshi_dai/repos/ARIA/data_engine/core/models.py): `pydantic_to_pyarrow()` による SSOT スキーマ導出
