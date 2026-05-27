---
name: career-document-creator
description: 職務経歴書・履歴書の作成・改善を支援するスキル。「職務経歴書を作りたい」「履歴書を書きたい」「経歴書をブラッシュアップしたい」「転職用の書類を作成したい」などのリクエストに使用。IT/セキュリティ/エンジニア向けの推奨スキル・資格のレコメンド機能も含む。
allowed-tools: Read, Grep, Glob, Write, Edit
user-invocable: true
---

# Career Document Creator

職務経歴書・履歴書の作成・改善を支援する。

## ワークフロー

### Phase 1: 情報収集
1. 既存の職務経歴書があれば読み込む
2. なければ以下をヒアリング：
   - 現職・前職の会社名、期間、役職
   - 担当業務、プロジェクト
   - 定量的な成果（人数、金額、期間など）
   - 使用技術・ツール
   - 希望職種・業界

### Phase 2: 分析・改善提案
1. 強み・コアコンピタンスの抽出
2. 不足している情報の特定
3. 業界トレンドに基づく推奨スキル・資格のレコメンド

### Phase 3: 作成・改善
1. 構成の最適化（読みやすさ、アピール力）
2. 定量成果の追加・強調
3. スキルマトリクスの整理
4. 自己PRの強化

## 出力フォーマット

```markdown
# 職務経歴書

**YYYY年MM月DD日現在**
**氏名**

---

## ■ 職務要約
（3-5行で経歴のハイライト）

---

## ■ 職務経歴

### 会社名（期間）
| 項目 | 内容 |
|------|------|
| 事業内容 | ... |
| 従業員数 | ... |

#### 【役職】担当業務（期間）
- 定量成果を含む実績
- プロジェクト詳細

---

## ■ テクニカルスキル
（カテゴリ別の表形式、経験レベル付き）

### 推奨取得スキル・資格
（業界トレンドに基づくレコメンド）

---

## ■ 強み・コアコンピタンス
（3-4項目に整理）

---

## ■ 自己PR
（プレイヤー/マネージャー両面、今後の展望）
```

## 業界別推奨スキル

### IT/セキュリティ領域

**セキュリティ:**
- EDR/XDR: CrowdStrike, Microsoft Defender XDR, SentinelOne
- SIEM/SOAR: Splunk, Microsoft Sentinel, Chronicle
- 資格: CompTIA Security+, AWS Security Specialty, CISSP

**クラウド/インフラ:**
- IaC: Terraform, Pulumi, AWS CDK
- コンテナ: Docker, Kubernetes
- 資格: AWS SAA/SAP, Azure Administrator

**生成AI/自動化:**
- コーディング支援: GitHub Copilot, Cursor, Claude Code
- RAG/エージェント: LangChain, LlamaIndex, Dify

## 改善チェックリスト

- [ ] 定量成果が含まれているか
- [ ] 技術スタックが明確か
- [ ] 強みが3-4項目に整理されているか
- [ ] 読みやすい構成か
- [ ] 業界トレンドの推奨スキルが提示されているか
