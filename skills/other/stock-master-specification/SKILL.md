---
name: stock-master-specification
description: ARIA 銘柄マスタ (`stocks_master.parquet`) の詳細仕様、データソース、および物理実装ガイド。
---

# ARIA Stock Master Specification (Engineering Sovereignty)

## 1. 概要
`stocks_master.parquet` は、ARIA プロジェクトにおける「銘柄の真実」を司る中央リポジトリです。EDINET、JPX、および内部集約リストからの情報を統合し、ウェブアプリ・API での高速な検索と、金融監査に耐えうる正確性を両立します。

## 2. 物理構造とカラム順序 (Web-Ready Architecture)
`stocks_master.parquet` (StockMasterRecord) は、ARIAプロジェクト全体の「実体（Entity）」の最新状態を統治する主権的リポジトリです。
ウェブアプリでの利用を考慮し、Identifiers -> Identity -> Lifecycle -> Industry -> Financial の論理グループで物理カラムを配置しています。

### 1) Essential Web Identity (Primary Keys)
| カラム名 | 型 | 役割・ロジック | 情報源 |
| :--- | :--- | :--- | :--- |
| `identity_key` | string | **Primary Key**. ARIA内における不変のユニークID。EDINET絶対優先、次点で証券コード、最後にJCNの順で生成。 | Logic |
| `edinet_code` | string | EDINET提出者コード (EXXXXX)。ARIAデータの永続的な主キー、およびビン分割の主軸。 | EDINET |
| `code` | string | 証券コード。常に5桁化し `JP:` プレフィックスを強制 | JPX / EDINET |
| `jcn` | string | 法人番号 (13桁)。EDINETと証券コードが共に存在しない場合のフォールバック。 | EDINET |

### 2) Identity Attributes
| カラム名 | 型 | 役割・ロジック | 情報源 |
| :--- | :--- | :--- | :--- |
| `company_name` | string | 提出者名 (和文) | EDINET/JPX |
| `company_name_en` | string | 提出者名 (英文)。欠損（NaN/None等）は工学的にNull化。 | EDINET/JPX |
| `company_name_kana` | string | 提出者名 (ヨミ) | EDINET |

### 3) Lifecycle & Tracking (Operational Metadata)
| カラム名 | 型 | 役割・ロジック | 情報源 |
| :--- | :--- | :--- | :--- |
| `is_active` | bool | ARIAの追跡対象フラグ。EDINET連携リストで上場区分が「非上場」のものは（JPXに存在しても特例を除き）絶対的に `False` | システム判定 |
| `is_disappeared` | bool | EDINETとJPXの双方ソースから完全に「消失」したことを示す差分判定フラグ | 差分ロジック |
| `is_listed_edinet` | bool | 金融庁名簿（EDINETリスト）上で明示的に「上場」となっているか | EDINET |
| `last_submitted_at` | string | 該当企業が最後に書類を提出した日時 | Catalog |

### 4) Industry & Market Classification (Normalized)
業種区分等（`jpx_definitions.parquet`。SCD Type 2で日時重複排除済）
| カラム名 | 型 | 役割・ロジック | 情報源 |
| :--- | :--- | :--- | :--- |
| `market` | string | 上場市場名 (プライム、スタンダード等) | JPX |
| `sector_jpx_33` | string | JPX 33業種区分名 | JPX |
| `sector_33_code` | string | JPX 33業種コード | JPX |
| `sector_jpx_17` | string | JPX 17業種区分名 | JPX |
| `sector_17_code` | string | JPX 17業種コード | JPX |
| `industry_edinet` | string | EDINETが提供する提出者業種(和文) | EDINET |
| `industry_edinet_en` | string | EDINETが提供する提出者業種(英文) | EDINET |
| `size_code` | string | 規模コード (TOPIX Core30等) | JPX |
| `size_category` | string | 規模区分名 | JPX |

### 5) Financial & Corporate Attributes
| カラム名 | 型 | 役割・ロジック | 情報源 |
| :--- | :--- | :--- | :--- |
| `parent_code` | string | 親会社の証券コード（優先株などの場合、上4桁に0を付与した普通株コードを保持） | JPX派生 |
| `former_edinet_codes` | string | 逆方向名寄せで追記された旧EDINETコードの履歴。文字列混入を排除したカンマ区切り。 | 集約リスト |
| `submitter_type` | string | 提出者種別 (内国法人・外国法人等) | EDINET |
| `is_consolidated` | bool | 連結の有無 ("有"->True, "無"->False に強制変換処理) | EDINET |
| `capital` | float | 資本金 (百万円単位) | EDINET |
| `settlement_date` | string | 決算期末日 (例: 3月31日) | EDINET |
| `address` | string | 本店所在地 | EDINET |

### 1) Essential Web Identity (Primary Keys)
| カラム名 | 型 | 役割・ロジック | 情報源 |
| :--- | :--- | :--- | :--- |
| `identity_key` | string | **Primary Key**. ARIA内における不変のユニークID。JCN優先、次点でEDINET、最後に証券コードで生成。 | Logic |
| `jcn` | string | 法人番号 (13桁)。最終的な永続的ビン分割キー | EDINET |
| `edinet_code` | string | EDINET提出者コード (EXXXXX)。JCN不明時の暫定キー | EDINET |
| `code` | string | 証券コード。常に5桁化し `JP:` プレフィックスを強制 | JPX / EDINET |

### 2) Identity Attributes
| カラム名 | 型 | 役割・ロジック | 情報源 |
| :--- | :--- | :--- | :--- |
| `company_name` | string | 提出者名 (和文) | EDINET/JPX |
| `company_name_en` | string | 提出者名 (英文)。欠損（NaN/None等）は工学的にNull化。 | EDINET/JPX |
| `company_name_kana` | string | 提出者名 (ヨミ) | EDINET |

### 3) Lifecycle & Tracking (Operational Metadata)
| カラム名 | 型 | 役割・ロジック | 情報源 |
| :--- | :--- | :--- | :--- |
| `is_active` | bool | ARIAの追跡対象フラグ。EDINET連携リストで上場区分が「非上場」のものは（JPXに存在しても特例を除き）絶対的に `False` | システム判定 |
| `is_disappeared` | bool | EDINETとJPXの双方ソースから完全に「消失」したことを示す差分判定フラグ | 差分ロジック |
| `is_listed_edinet` | bool | 金融庁名簿（EDINETリスト）上で明示的に「上場」となっているか | EDINET |
| `last_submitted_at` | string | 該当企業が最後に書類を提出した日時 | Catalog |

### 4) Industry & Market Classification (Normalized)
業種区分等（`jpx_definitions.parquet`。SCD Type 2で日時重複排除済）
| カラム名 | 型 | 役割・ロジック | 情報源 |
| :--- | :--- | :--- | :--- |
| `market` | string | 上場市場名 (プライム、スタンダード等) | JPX |
| `sector_jpx_33` | string | JPX 33業種区分名 | JPX |
| `sector_33_code` | string | JPX 33業種コード | JPX |
| `sector_jpx_17` | string | JPX 17業種区分名 | JPX |
| `sector_17_code` | string | JPX 17業種コード | JPX |
| `industry_edinet` | string | EDINETが提供する提出者業種(和文) | EDINET |
| `industry_edinet_en` | string | EDINETが提供する提出者業種(英文) | EDINET |
| `size_code` | string | 規模コード (TOPIX Core30等) | JPX |
| `size_category` | string | 規模区分名 | JPX |

### 5) Financial & Corporate Attributes
| カラム名 | 型 | 役割・ロジック | 情報源 |
| :--- | :--- | :--- | :--- |
| `parent_code` | string | 親会社の証券コード（優先株などの場合、上4桁に0を付与した普通株コードを保持） | JPX派生 |
| `former_edinet_codes` | string | 逆方向名寄せで追記された旧EDINETコードの履歴。文字列混入を排除したカンマ区切り。 | 集約リスト |
| `submitter_type` | string | 提出者種別 (内国法人・外国法人等) | EDINET |
| `is_consolidated` | bool | 連結の有無 ("有"->True, "無"->False に強制変換処理) | EDINET |
| `capital` | float | 資本金 (百万円単位) | EDINET |
| `settlement_date` | string | 決算期末日 (例: 3月31日) | EDINET |
| `address` | string | 本店所在地 | EDINET |


## 3. 実体識別ロジック (Identity Sovereignty)

### 1) 識別子の遷移と統合（Identity Upgrade）
ARIA は、情報の鮮度と権威に基づき、以下の優先順位で実体 ID（`identity_key`）を決定します。
1.  🔒 **JCN (13桁法人番号)**: **[最優先]** ストレージの物理パス（bin分割）と一致する最終的な ID。
2.  ⚠️ **EDINET Code (E...)**: JCN が不明な期間の暫定 ID。
3.  🔄 **Security Code (JP:...)**: 上記いずれも不明な（IPO直後等の）暫定 ID。

### 2) identity_key が「変化する」理由と工学的必要性
プログラミングの観点では、ID は一度決まったら変わらないのが理想です。しかし、現実の金融データでは「証券コードはあるが法人番号は後から判明する」という情報の不完全性が発生します。
- **必要性**: もし `identity_key` がなければ、プログラムは常に「JCN または EDINETコード または 証券コード」の 3 つすべてをチェックし続けなければならず、処理が劇的に遅くなり、バグの温床になります。
- **解決策**: ARIA では「現時点で判明している中で最も信頼できる ID」を `identity_key` と呼び、実体を 1 つの ID で代表させます。
- **遷移の管理**: ID が `JP:...` から `JCN` へ遷移した際、ARIA は内部で「名寄せ」を行い、マスタ上の関係性を更新します。カタログ側には管理キーを持たない（Pure Catalog）ため、カタログデータを書き換えることなく、マスタを介した動的な紐付けが可能です。

## 4. 消失判定の数学的根拠 (Anomaly Obsession)
銘柄が `is_disappeared=True` となるのは、以下の **AND 条件** を満たした場合のみです。
1. 今回の EDINET コードリスト同期に含まれていない。
2. 今回の JPX 上場銘柄一覧同期に含まれていない。
3. 過去に一度も `is_disappeared` になったことがない（または直近まで生存していた）。

## 5. 逆方向名寄せブリッジ (Backward Aggregation)
`ESE140190.csv` に基づき、合併・持株会社移行等のコード変更に対して「順方向置換」を排除し、以下の原則で履歴を紐付けます。
- `former_edinet_codes`: 現在の継続EDINETコードを持つレコードに対してのみ、配列（カンマ区切り）として過去の廃止コードを「逆方向追記（マージ）」し、現在の識別子の絶対性を保護と過去データとのトレーサビリティを完全確保します。
