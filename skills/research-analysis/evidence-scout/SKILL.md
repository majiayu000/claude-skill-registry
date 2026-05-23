---
name: evidence-scout
description: |
  指定薬剤・適応・国・データベース特性に基づき、PubMed/Web検索で先行RWD研究・RCT・ガイドラインを調査し、
  エビデンスランドスケープを要約する。JMDC/MDV等クレームDBとの差別化観点を必ず含める。
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - mcp__plugin_pubmed_PubMed__search_articles
  - mcp__plugin_pubmed_PubMed__get_article_metadata
  - mcp__plugin_pubmed_PubMed__find_related_articles
context: fork
---

# Evidence Scout Skill

## 目的
指定された薬剤・適応症・国・DB特性について、既存エビデンス（RWD研究、RCT、ガイドライン、規制文書）を網羅的に調査し、研究ギャップと機会を特定する。

## 入力パラメータ

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| DRUG | Yes | 対象薬剤（一般名） | daratumumab |
| INDICATION | Yes | 対象疾患/適応 | newly diagnosed multiple myeloma |
| COUNTRY | Yes | 対象国/地域 | Japan |
| DB_CAPABILITIES | No | 利用可能DB特性 | EHR-linked, lab values available |
| TIME_RANGE | No | 検索期間 | 2019-2025 |
| COMPARATORS | No | 比較対照薬 | VRd, KRd |

## 実行手順

### Step 1: PubMed検索（RWD研究）
```
検索式: "{DRUG} AND real-world AND {INDICATION} AND {COUNTRY}"
検索式: "{DRUG} AND pharmacoepidemiology AND {INDICATION}"
検索式: "{DRUG} AND claims database OR electronic health records"
```

### Step 2: PubMed検索（RCT・メタ解析）
```
検索式: "{DRUG} AND {INDICATION} AND (randomized controlled trial OR meta-analysis)"
```

### Step 3: ガイドライン・規制文書（Web検索）
```
検索語: "{DRUG} {INDICATION} clinical guideline {COUNTRY}"
検索語: "{DRUG} FDA approval label"
検索語: "{DRUG} PMDA 添付文書 審査報告書"
```

### Step 4: JMDC/MDV類似研究の特定
```
検索式: "{DRUG} AND Japan AND (claims OR JMDC OR MDV OR NDB)"
```

### Step 5: エビデンスマッピング
各研究を以下の軸で分類:
- 研究デザイン（コホート/ケースコントロール/記述研究）
- データソース（クレーム/EHR/レジストリ）
- アウトカム（有効性/安全性/医療経済）
- 方法論的質（new-user design有無、active comparator有無）

## 出力フォーマット

```markdown
# Evidence Landscape Report: {DRUG} in {INDICATION} ({COUNTRY})

## 1. 検索サマリー
- PubMed RWD研究: X件
- RCT/メタ解析: Y件
- ガイドライン: Z件

## 2. 主要エビデンス一覧

### 2.1 RWD研究（{COUNTRY}）
| 著者/年 | デザイン | データソース | N | 主要所見 | PMID/DOI |
|---------|----------|--------------|---|----------|----------|

### 2.2 RWD研究（海外）
| 著者/年 | デザイン | データソース | N | 主要所見 | PMID/DOI |
|---------|----------|--------------|---|----------|----------|

### 2.3 RCT/メタ解析
| 試験名 | フェーズ | 比較 | 主要結果 | PMID/DOI |
|--------|----------|------|----------|----------|

### 2.4 ガイドライン
| 発行元 | 年 | 推奨グレード | URL |
|--------|---|--------------|-----|

## 3. JMDC/MDV等クレームDB研究との比較

| 観点 | クレームDB研究 | 当社EHR-RWDの優位性 |
|------|----------------|---------------------|
| 臨床詳細度 | 限定的 | 経過記録・サマリー利用可 |
| 検査値 | なし/限定的 | 時系列検査値利用可 |
| アウトカム定義精度 | ICD/レセプトコード依存 | 臨床判断との照合可能 |
| 交絡調整 | 限定的 | ベースライン詳細評価可 |

## 4. 研究ギャップ
1. [ギャップ1]
2. [ギャップ2]
3. [ギャップ3]

## 5. 根拠文献（PMID/DOI一覧）
- ...
```

## 注意事項

1. **機微情報の保護**: 検索クエリに患者ID・施設名・個人情報を含めない
2. **根拠の明示**: 各所見にPMID/DOIを必ず付記。見つからない場合は「根拠不足」と明記
3. **検索の網羅性**: 日本語文献はJ-STAGEやCiNii検索を別途推奨（MCPで利用不可の場合はユーザーに依頼）
4. **更新日の記載**: レポート作成日を明記し、エビデンスの鮮度を示す
5. **バイアス評価**: 各研究の方法論的質（Risk of Bias）を可能な範囲で評価

## エラーハンドリング

- PubMed MCP利用不可 → WebSearchで"site:pubmed.ncbi.nlm.nih.gov"検索にフォールバック
- Web検索利用不可 → ユーザーに特定URLの提供を依頼して続行
- 検索結果0件 → 検索語を広げて再検索、それでも0件なら「該当研究なし」と報告
