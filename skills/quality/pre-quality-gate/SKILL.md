---
name: pre-quality-gate
description: プロジェクト プロジェクトの品質検証スキル。MakefileのSSOT q.checkを実行し結果を解釈する。
doc_contract:
  review_interval_days: 90
---

# Pre-Quality Gate

## SSOT

> **このスキルはルールを定義しません。**
> すべてのルールは `Makefile` で **唯一** 定義されます。

---

## 実行方法

```bash
# 品質検査
make q.check

# 自動修正後に検査
make q.fix
```

---

## Exit Code 解釈

| Code  | 意味 | 次のアクション           |
| :---: | ---- | ------------------------ |
|  `0`  | PASS | コミット/PR 進行可能     |
| `!=0` | FAIL | 出力メッセージに従い修正 |

---

## AI 実行プロトコル

```markdown
## Step 1: 品質検査実行

Bash: make q.check

## Step 2: 結果確認

- Exit 0 → PASS → 完了
- Exit !=0 → Step 3へ

## Step 3: 自動修正試行

Bash: make q.fix

## Step 4: 再検証

- Exit 0 → PASS → 完了
- Exit !=0 → 手動修正案内
```

---

## 検証項目

|  深刻度  | ターゲット             | 説明                             |
| :------: | ---------------------- | -------------------------------- |
| Critical | `q.analyze`            | 静的分析 (ESLint)                |
| Critical | `q.format.check`       | コードフォーマット検査           |
| Critical | `q.check-architecture` | Feature-First アーキテクチャ検証 |
|  Major   | `q.test-exists`        | テストファイル存在確認           |

---

## QAサイクルモード

> **目的**: 品質ゲート通過まで自動的に修正を繰り返す

### ルール

| 項目               | 値                          |
| ------------------ | --------------------------- |
| 最大反復回数       | **5回**                     |
| 同一エラー中断閾値 | **3回**                     |
| カウンター表示     | `[QA 1/5]`, `[QA 2/5]`, ... |

### プロトコル

```markdown
## QAサイクル実行

iteration = 0
same_error_count = 0
last_error = null

LOOP:
iteration += 1
IF iteration > 5 → ABORT("最大反復回数(5回)に到達")

Bash: make q.check
IF exit == 0 → PASS → 完了

current_error = 出力メッセージのハッシュ
IF current_error == last_error:
same_error_count += 1
IF same_error_count >= 3 → ABORT("同一エラーが3回連続で未解決")
ELSE:
same_error_count = 1
last_error = current_error

出力: [QA {iteration}/5] エラー修正中...

Bash: make q.fix
IF exit == 0 → PASS → 完了

エラー内容を分析し、手動修正を試行
GOTO LOOP
```

### 中断時の出力

```markdown
## QAサイクル中断

| 項目               | 内容                           |
| ------------------ | ------------------------------ |
| **反復回数**       | {iteration}/5                  |
| **中断理由**       | {最大回数到達 / 同一エラー3回} |
| **未解決エラー**   | {エラー内容}                   |
| **推奨アクション** | {手動修正の具体的な指示}       |
```

---

## トリガー条件

- "コミット前確認", "PR準備", "品質検査", "quality gate"
- パイプラインの Reviewing ステップ

---

## ルール変更時

**`Makefile`のみ修正してください。** このファイルは修正しません。
