---
name: bicep-what-if-analysis
description: azd up/azd provisionの影響分析、Bicep what-if実行とノイズフィルタリング。インフラ変更・デプロイ前の影響確認時に使用。
---

# Bicep What-If 分析

インフラ変更前の影響範囲確認とノイズフィルタリングを支援します。

## ⚠️ このスキルを使うべき状況

以下のいずれかに該当する場合、**必ずこのスキルを呼び出してください**：

| ユーザーの質問・依頼 | 理由 |
|---------------------|------|
| 「azd up の影響は？」「azd provision で何が変わる？」 | 実際のAzure環境との差分が必要 |
| 「このBicep変更の影響を教えて」 | 静的分析では不十分、what-ifが必要 |
| 「デプロイしても大丈夫？」「破壊的変更はある？」 | リスク評価にwhat-if結果が必須 |
| 「インフラの変更点を確認したい」 | 現在の状態との比較が必要 |

**静的コード分析（Bicepファイルを読むだけ）では不十分です。**
What-if は Azure Resource Manager API を呼び出し、**現在デプロイ済みの状態との実際の差分**を取得します。

## クイックスタート

```bash
# フィルタ済みwhat-if分析（推奨）
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh

# 生出力が必要な場合
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh --raw

# 破壊的変更のみ抽出
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh | jq 'select(.changeType == "Delete")'
```

## 前提条件

- `azd env`が初期化済み（`AZURE_LOCATION`等が設定済み）
- Azure CLIでログイン済み

## ノイズ判定基準

### 無視して良い変更

| リソース | プロパティ | 理由 |
|---------|-----------|------|
| 全リソース | `provisioningState` | 読み取り専用 |
| 全リソース | `etag` | 常に変化 |
| 全リソース | `resourceGuid`, `uniqueId` | 動的生成 |
| AKS | `currentOrchestratorVersion` | 読み取り専用 |
| AKS | `nodeImageVersion` | 読み取り専用 |
| AKS | `fqdn`, `azurePortalFQDN` | 動的生成 |
| AKS | `powerState.code` | 読み取り専用 |
| AKS | `identityProfile.*` | 動的生成 |
| Managed Identity | `principalId`, `clientId`, `tenantId` | 読み取り専用 |

### 要注意の変更（破壊的変更の可能性）

以下が `Modify` で表示された場合は**リソース再作成**の可能性があります：

| リソース | プロパティ | 影響 |
|---------|-----------|------|
| AKS | `networkProfile.networkPlugin` | クラスター再作成 |
| AKS | `networkProfile.networkPluginMode` | クラスター再作成 |
| AKS | `apiServerAccessProfile.subnetId` | クラスター再作成 |
| AKS | `agentPoolProfiles[*].vnetSubnetID` | ノードプール再作成 |
| Redis | `sku.name`, `sku.capacity` | データロスの可能性 |
| VNet | `addressSpace.addressPrefixes` | 依存リソースへ影響 |

## 分析フロー

```
1. what-if実行
   ↓
2. 変更タイプで分類
   - NoChange / NoEffect / Ignore → 無視
   - Create / Delete / Modify → 詳細確認
   ↓
3. Modifyの詳細確認
   - ノイズリストに該当 → 無視
   - 破壊的変更リストに該当 → 要注意
   - それ以外 → 意図した変更か確認
```

## 変更タイプの意味

| タイプ | 説明 | 対応 |
|--------|------|------|
| **Create** | 新規作成 | 設定内容を確認 |
| **Delete** | 削除 | 意図した削除か確認 |
| **Modify** | 変更あり | 破壊的変更か確認 |
| **NoChange** | 変更なし | 無視 |
| **NoEffect** | 影響なし（読み取り専用等） | 無視 |
| **Ignore** | 評価対象外 | 通常は無視 |

## トラブルシューティング

### "AZURE_LOCATION is not set" エラー

```bash
# azd環境を初期化
azd env refresh
```

### what-ifが大量の変更を報告する

- APIバージョン更新後は多くの「変更」が報告されることがあります
- `--raw`オプションで生出力を確認し、実際の差分を確認してください

### 特定リソースの詳細を確認したい

```bash
# リソースIDでフィルタ
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh | \
  jq 'select(.resourceId | contains("managedClusters"))'
```

## このスキルを使わない場合

以下の場合は静的分析で十分です：

- 「Bicepファイルの構文を確認して」（リンター実行）
- 「このモジュールは何を作成する？」（コードリーディング）
- 「パラメータのデフォルト値は？」（ファイル参照）
