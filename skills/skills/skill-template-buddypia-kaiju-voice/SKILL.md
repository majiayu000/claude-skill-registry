---
name: { { SKILL_ID } }
description: |
  {{SKILL_DESCRIPTION}}

  **核心機能**:
  - {{CORE_FEATURE_1}}
  - {{CORE_FEATURE_2}}

  "{{TRIGGER_KEYWORD_1}}", "{{TRIGGER_KEYWORD_2}}" 等の要求でトリガーされる。

  <example>
  user: "{{EXAMPLE_USER_REQUEST}}"
  assistant: "{{SKILL_ID}}を使用して {{EXAMPLE_ACTION}}を実行します"
  </example>
---

# {{SKILL_NAME}} ({{SKILL_KOREAN_NAME}})

> **核心コンセプト**: "{{CORE_CONCEPT}}"

{{SKILL_OVERVIEW_DESCRIPTION}}

## 核心 原則

1. **{{PRINCIPLE_1_NAME}}**: {{PRINCIPLE_1_DESC}}
2. **{{PRINCIPLE_2_NAME}}**: {{PRINCIPLE_2_DESC}}
3. **{{PRINCIPLE_3_NAME}}**: {{PRINCIPLE_3_DESC}}

---

## 🔧 主要 機能

### 1. {{FEATURE_1_NAME}}

**説明**: {{FEATURE_1_DESC}}

```
実行 ロジック:
1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}
```

### 2. {{FEATURE_2_NAME}}

**説明**: {{FEATURE_2_DESC}}

---

## 🚀 実行 プロトコル

### Phase 1: 入力 検証

```
1. 必須 パラメータ 確認
2. 権限/状態 検証
3. 前提条件 チェック
```

### Phase 2: 実行

```
1. {{EXECUTION_STEP_1}}
2. {{EXECUTION_STEP_2}}
3. {{EXECUTION_STEP_3}}
```

### Phase 3: 出力

```
1. 結果 フォーマット
2. ログ 記録
3. 状態 更新
```

---

## ⚠️ 制約 事項

1. **{{CONSTRAINT_1}}**: {{CONSTRAINT_1_DESC}}
2. **{{CONSTRAINT_2}}**: {{CONSTRAINT_2_DESC}}

---

## 📊 出力 例示

```markdown
# {{SKILL_NAME}} 実行 結果

> **実行 時間**: {{TIMESTAMP}}

## Summary

| 項目      | 結果 |
| --------- | :--: |
| 処理 項目 | N個  |
| 成功      | N個  |
| 失敗      | N個  |

## 詳細 結果

{{DETAILED_RESULTS}}
```

---

## 使用 例示

```bash
# 基本 実行
/{{SKILL_ID}}

# オプション 使用
/{{SKILL_ID}} --{{OPTION_1}}

# 特定 対象 指定
/{{SKILL_ID}} {{TARGET}}
```

---

## 変更 履歴

| 日付     | バージョン | 変更 内容                           |
| -------- | ---------- | ----------------------------------- |
| {{DATE}} | v1.0       | 新規 生成 - {{INITIAL_DESCRIPTION}} |
