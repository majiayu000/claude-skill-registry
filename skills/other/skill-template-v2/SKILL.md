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
  assistant: "{{SKILL_ID}}を使用して{{EXAMPLE_ACTION}}を実行します"
  </example>
---

# {{SKILL_NAME}} ({{SKILL_KOREAN_NAME}})

> **核心コンセプト**: "{{CORE_CONCEPT}}"

{{SKILL_OVERVIEW_DESCRIPTION}}

---

## 🚨 EXECUTION PROTOCOL (MANDATORY)

> **CRITICAL**: このセクションは **省略不可**です。AIは このスキル実行時に 必ず以下の チェックリストを **出力して確認**しなければなりません。

### Pre-flight Checklist (実行前 必須)

スキル実行前に 必ず以下の チェックリストを **出力**して 各項目を確認:

> **⚡ CHECKLIST UPDATE RULE (MANDATORY)**:
> 各チェック項目の確認完了時に、チェックリスト全体を再出力し、該当項目の状態を更新すること。
> `⬜` → `✅` (通過) または `❌` (失敗)。全項目確認まで毎回最新状態を反映。
> **未更新のまま次段階に進行 = Violation Protocol 違反 (severity: HIGH)**

```markdown
## ✈️ Pre-flight Checklist

|  #  | 項目                  | 状態 | 備考 |
| :-: | --------------------- | :--: | ---- |
|  1  | {{PREFLIGHT_CHECK_1}} |  ⬜  |      |
|  2  | {{PREFLIGHT_CHECK_2}} |  ⬜  |      |
|  3  | {{PREFLIGHT_CHECK_3}} |  ⬜  |      |

→ 各項目確認後に本テーブルを再出力 (状態列を ✅/❌ に更新)
→ 全項目 ✅: 実行進行 / 1つでも ❌: 即時中断 + 理由報告
```

### Model Routing Policy (モデルポリシー)

> **MANDATORY**: Task ツール呼び出し時必ず`model`パラメータ明示

| 作業タイプ      | モデル                         | 根拠         |
| --------------- | ------------------------------ | ------------ |
| {{TASK_TYPE_1}} | {{MODEL_1: haiku/sonnet/opus}} | {{REASON_1}} |
| {{TASK_TYPE_2}} | {{MODEL_2: haiku/sonnet/opus}} | {{REASON_2}} |
| {{TASK_TYPE_3}} | {{MODEL_3: haiku/sonnet/opus}} | {{REASON_3}} |

**フォールバック戦略**:

- {{MODEL_LOW}} 失敗 → {{MODEL_MED}} 自動昇格
- {{MODEL_MED}} 失敗 → {{MODEL_HIGH}} 自動昇格

### Evidence Policy (キャッシュポリシー)

| 検証タイプ          |    有効時間    | 無効化条件         | キャッシュキー  |
| ------------------- | :------------: | ------------------ | --------------- |
| {{EVIDENCE_TYPE_1}} | {{VALIDITY_1}} | {{INVALIDATION_1}} | {{CACHE_KEY_1}} |
| {{EVIDENCE_TYPE_2}} | {{VALIDITY_2}} | {{INVALIDATION_2}} | {{CACHE_KEY_2}} |

**動作**:

1. 検証要求時 `CONTEXT.json > evidence_cache` 確認
2. 有効なキャッシュ存在 → スキップ + キャッシュ結果使用
3. キャッシュなし/期限切れ → 実行 + 結果キャッシュ

### Post-flight Checklist (実行後必須)

スキル完了前必ず下記チェックリストを**出力**して検証:

> **⚡ CHECKLIST UPDATE RULE (MANDATORY)**:
> 各チェック項目の確認完了時に、チェックリスト全体を再出力し、該当項目の状態を更新すること。
> `⬜` → `✅` (通過) または `❌` (失敗)。全項目確認まで毎回最新状態を反映。
> **未更新のまま次段階に進行 = Violation Protocol 違反 (severity: HIGH)**

```markdown
## 🛬 Post-flight Checklist

|  #  | 項目                   | 状態 | 備考 |
| :-: | ---------------------- | :--: | ---- |
|  1  | {{POSTFLIGHT_CHECK_1}} |  ⬜  |      |
|  2  | {{POSTFLIGHT_CHECK_2}} |  ⬜  |      |
|  3  | {{POSTFLIGHT_CHECK_3}} |  ⬜  |      |

→ 各項目確認後に本テーブルを再出力 (状態列を ✅/❌ に更新)
→ 全項目 ✅: 完了報告 / 1つでも ❌: 修正後再検証
```

### Violation Protocol (違反時処理)

| 違反タイプ              |  深刻度  | 処理                     |
| ----------------------- | :------: | ------------------------ |
| Pre-flight 未出力       | CRITICAL | 即時中断、最初から再開始 |
| Model パラメータ欠落    |   HIGH   | 該当Task再実行           |
| Post-flight 未検証      |   HIGH   | 完了報告前検証実行       |
| Evidence キャッシュ無視 |  MEDIUM  | 警告後進行               |

---

## 核心原則

1. **{{PRINCIPLE_1_NAME}}**: {{PRINCIPLE_1_DESC}}
2. **{{PRINCIPLE_2_NAME}}**: {{PRINCIPLE_2_DESC}}
3. **{{PRINCIPLE_3_NAME}}**: {{PRINCIPLE_3_DESC}}

---

## 🔧 主要機能

### 1. {{FEATURE_1_NAME}}

**説明**: {{FEATURE_1_DESC}}

```
実行ロジック:
1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}
```

### 2. {{FEATURE_2_NAME}}

**説明**: {{FEATURE_2_DESC}}

---

## 🚀 実行フロー

```
Pre-flight Checklist 出力 + 確認
        ↓ (全て ✅)
Phase 1: {{PHASE_1_NAME}}
        ↓
Phase 2: {{PHASE_2_NAME}}
        ↓
Phase 3: {{PHASE_3_NAME}}
        ↓
Post-flight Checklist 出力 + 検証
        ↓ (全て ✅)
完了報告 + Evidence キャッシュ
```

---

## ⚠️ 制約事項

| 制約             | 理由                    | 違反時                     |
| ---------------- | ----------------------- | -------------------------- |
| {{CONSTRAINT_1}} | {{CONSTRAINT_1_REASON}} | {{CONSTRAINT_1_VIOLATION}} |
| {{CONSTRAINT_2}} | {{CONSTRAINT_2_REASON}} | {{CONSTRAINT_2_VIOLATION}} |

---

## 📊 出力形式

### 成功時

```markdown
# {{SKILL_NAME}} 実行完了

> **実行時間**: {{TIMESTAMP}}
> **モデル使用**: {{MODELS_USED}}
> **キャッシュ活用**: {{CACHE_HIT_RATE}}

## Summary

| 項目     | 結果 |
| -------- | :--: |
| 処理項目 | N個  |
| 成功     | N個  |
| 失敗     | 0個  |

## Evidence キャッシュ

| 検証           | キャッシュキー | 期限         |
| -------------- | -------------- | ------------ |
| {{EVIDENCE_1}} | {{KEY_1}}      | {{EXPIRY_1}} |
```

### 失敗時

```markdown
# {{SKILL_NAME}} 実行失敗

> **失敗時点**: {{FAILURE_POINT}}
> **失敗理由**: {{FAILURE_REASON}}

## 推奨処置

1. {{REMEDIATION_1}}
2. {{REMEDIATION_2}}
```

---

## 使用例

```bash
# 基本実行
/{{SKILL_ID}}

# オプション使用
/{{SKILL_ID}} --{{OPTION_1}}

# キャッシュ無視 (強制再実行)
/{{SKILL_ID}} --force
```

---

## 変更履歴

| 日付     | バージョン | 変更内容                           |
| -------- | ---------- | ---------------------------------- |
| {{DATE}} | v1.0       | 新規生成 - {{INITIAL_DESCRIPTION}} |
