---
name: rfc-compliance-workflow
description: RFC/OIDC仕様書の準拠ワークフロー。要件抽出→Gap分析→実装設計→E2Eテスト生成までの一連の流れを管理。
---

# RFC Compliance Workflow

RFC/OIDC仕様書からの要件抽出、Gap分析、実装設計、E2Eテスト生成までを統合管理するワークフローツール。

## 概要

このスキルは、仕様準拠開発の全体フローを管理します：

1. **要件抽出** (`oidc-spec-requirement-extractor`) - 仕様書からMUST/SHOULD要件を抽出
2. **Gap分析** - 現在の実装と要件のギャップを特定
3. **実装設計** - 設計ドキュメント・ADR生成  
4. **E2Eテスト生成** - テストケース自動生成

### 完全なワークフロー

\`\`\`
RFC/OIDC仕様書
  ↓ [oidc-spec-requirement-extractor]
requirements YAML (documentation/requirements/)
  ↓ [Gap分析]
実装ギャップ特定 & 優先順位付け
  ↓ [実装設計]
設計ドキュメント & ADR
  ↓ [E2Eテスト生成]
e2e/src/tests/compliance/{spec}/
  ↓ [実装]
idp-server コード実装
  ↓ [検証]
E2Eテスト実行 & 準拠確認
\`\`\`

## 使い方

\`\`\`bash
/rfc-compliance-workflow [phase] [requirements_file]
\`\`\`

### フェーズ

- \`full\`: 完全ワークフロー (Gap分析→設計→E2Eテスト)
- \`gap-analysis\`: Gap分析のみ
- \`design\`: 実装設計のみ
- \`e2e-tests\`: E2Eテスト生成のみ

### 例

\`\`\`bash
# 完全ワークフロー
/rfc-compliance-workflow full documentation/requirements/fapi-2.0-requirements.yaml

# Gap分析のみ
/rfc-compliance-workflow gap-analysis documentation/requirements/oauth2-par-requirements.yaml
\`\`\`

## 出力構造

\`\`\`
documentation/
├── gap-analysis/{spec}-gap-analysis.md
└── design/{spec}-implementation-design.md
e2e/src/tests/compliance/{spec}/
├── {spec}-must-requirements.test.js
├── {spec}-should-requirements.test.js
└── {spec}-security-negative.test.js
\`\`\`

## 関連スキル

- \`oidc-spec-requirement-extractor\`: 要件抽出
- \`identity-verification\`: 身元確認機能開発支援
