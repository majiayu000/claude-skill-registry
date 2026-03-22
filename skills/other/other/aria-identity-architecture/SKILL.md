---
name: aria-identity-architecture
description: ARIA の識別子ヒエラルキー（JCN/EDINET Code/証券コード）の設計思想と、コード変更シナリオへの対応戦略。
---
# ARIA 識別子アーキテクチャ (Identity Architecture)

ARIA が「企業の同一性」をどのように追跡・保証するかを定義するスキル。

## 1. 3層識別子ヒエラルキー

| 層 | 識別子 | 安定性 | 管轄 | ARIA での役割 |
|:--:|:-------|:------:|:----:|:-------------|
| 🔒 | **EDINET Code** | 準静的 | 金融庁 | 真の主キー。物理パス分散（`bin=EXX`）およびデータ統合の軸 |
| ⚠️ | **国籍付証券コード** | 動的 | JPX | `JP:37780` 形式。グローバル展開とサブ検索用 |
| 🔍 | **JCN (法人番号)** | 完全不変 | 国税庁 | 最終フォールバック用検索属性 |

**設計原則**: 下位の識別子が変更されても、上位の識別子で企業の一貫性を保証する。また、将来のグローバル展開を見据え、証券コードは常に「国籍プレフィックス」を伴う。

### 1. Identity Bridging (証券コードと EDINET コードの架け橋)
- **原則**: EDINET コードリストを主軸とし、JPX 証券コードを Bridge Fill 処理で紐付ける。
- **名寄せキー**: `edinet_code.fillna(code)` を `identity_key` として使用し、物理的なレコード統合を強制する。詳細は [stock-master-reconciler](file:///Users/yoshi_dai/repos/ARIA/.agent/skills/stock-master-reconciler/SKILL.md) を参照。

## 2. コード変更シナリオと ARIA の対応

| シナリオ | JCN | EDINET Code | 証券コード | ARIA の対応 |
| :--- | :--- | :--- | :--- | :--- |
| **商号変更** | 不変 | 不変 | 不変 | `stocks_master` の `company_name` を更新。 |
| **本店移転** | 不変 | 不変 | 不変 | `stocks_master` の `address` を更新。 |
| **合併 (吸収)** | 存続会社 | 存続会社 | 存続会社 | 消滅会社の `is_disappeared` を `True` に設定。 |
| **コード集約** | 不変 | **変更** | 不変 | `ESE140190.csv` を用い、廃止される旧コードを継続コードの `former_edinet_codes` へ逆方向に追記（マージ）し、現在の識別子を保護。 |

---

## 3. 証券コードの正規化と不変性

- **5 桁正規化 & 国籍プレフィックス**: 4 桁コードには末尾に `0` を付与し、さらに国籍プレフィックス（例: `JP:`）を強制付与する。
- **不変性の原理**: 一度付与された 5 桁コードは、企業の属性変化に関わらず、ARIA 内での不変の物理キーとして機能する。
- **プレフィックス耐性 (Prefix Tolerance)**: 既存のプレフィックスなしコードとの前方互換性を保つため、`CatalogManager` はプレフィックスを無視した「コア・マッチング」をフォールバックとして備える。

---

## 4. Master Data Integrity Laws (マスタデータの 5 鉄則)

ARIA は、以下の「工学的主権」に基づき、マスタデータの整合性を死守します。

1. **EDINET SSOT**: 同一銘柄は EDINET データを正とし、JPX 側の重複普通株は破棄。
2. **JPX 補完**: ETF/REIT/PRO 銘柄は JPX 由来を正として受容。
3. **Identity Bridging**: grouping 直前に証券コードから EDINET コードを逆引き補完。
4. **Existence Immutability**: 消えた銘柄は `is_disappeared=True` とし、物理削除しない。
5. **Normalize First**: 常にプレフィックス付 5 桁コードでマッチングを行う。

詳細は [stock-master-reconciler](file:///Users/yoshi_dai/repos/ARIA/.agent/skills/stock-master-reconciler/SKILL.md) を参照。
