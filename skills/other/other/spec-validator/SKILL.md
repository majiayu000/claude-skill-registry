---
name: spec-validator
description: SPEC 文書の JSON Schema ブロックおよびハイブリッド API 仕様を自動検証するスキル。SPEC 品質ゲート役割遂行。
doc_contract:
  review_interval_days: 90
---

# SPEC Validator (v3.4)

> **コアコンセプト**: SPEC 文書の機械検証可能な部分を自動検証して品質保証

このスキルは SPEC 文書から `json:schema/*` コードブロックを抽出し、該当メタスキーマで検証し、**ハイブリッド API 仕様の Example ↔ Schema 一致**を自動検証します。

## 検証範囲

| 検証項目                     | 方式                            | メタスキーマ                   |
| ---------------------------- | ------------------------------- | ------------------------------ |
| **§0.4.1 TypeScript モデル** | JSON Schema 検証                | `typescript_model.schema.json` |
| **§0.4.2 DB スキーマ**       | JSON Schema 検証                | `db_table.schema.json`         |
| **§0.4.5 Write Operations**  | JSON Schema 検証                | `write_operations.schema.json` |
| **§0.5 API Contract**        | JSON Schema 検証                | `api_endpoint.schema.json`     |
| **必須セクション存在**       | Regex マッチング                | -                              |
| **AC 形式**                  | 5列テーブル検証                 | -                              |
| **ハイブリッド API 完全性**  | テーブル + Example 存在確認     | -                              |
| **Example ↔ Schema 一致**    | タイプ/必須フィールド/enum 検証 | -                              |
| **SSOT パス有効性**          | API Route ファイル存在確認      | -                              |
| **Write Operations 一貫性**  | API↔Operation マッピング検証    | -                              |

---

## プロトコル (Protocol)

### Phase 1: SPEC ファイルロード

1. **単一ファイル検証**:

   ```bash
   /spec-validator docs/features/029-battle/SPEC-029.md
   ```

2. **全体 SPEC 検証**:

   ```bash
   /spec-validator --all
   ```

3. **特定機能のみ検証**:
   ```bash
   /spec-validator 029
   ```

### Phase 2: JSON Schema ブロック抽出

1. **パターンマッチング**:

   ````
   ```json:schema/{type}
   {JSON 内容}
   ````

   ```

   ```

2. **サポートタイプ**:
   - `json:schema/db_table` → DB テーブル定義
   - `json:schema/api_endpoint` → API 契約
   - `json:schema/typescript_model` → TypeScript モデル
   - `json:schema/write_operations` → データ変更仕様 (v3.4 新規)

3. **抽出ロジック**:
   ````python
   pattern = r'```json:schema/(\w+)\n(.*?)\n```'
   matches = re.findall(pattern, content, re.DOTALL)
   ````

### Phase 3: メタスキーマ検証

1. **スキーマロード**:
   - `docs/_templates/schemas/{type}.schema.json`

2. **JSON Schema 検証**:

   ```python
   from jsonschema import validate, ValidationError

   validate(instance=extracted_json, schema=meta_schema)
   ```

3. **エラー収集**:
   - パス、メッセージ、期待値 vs 実際値

### Phase 4: 構造検証

1. **必須セクション確認**:

   ```python
   required_sections = [
       r'## 0\. AI 実装契約',
       r'### 0\.4 Data Schema',
       r'### 0\.5 API Contract',
       r'## 1\. 概要',
       r'## 2\. 機能要求事項',
   ]
   ```

2. **AC 形式検証**:

   ```python
   # BDD 5列テーブル検証
   ac_pattern = r'\| AC\d+ \|.*\|.*\|.*\|.*\|'
   ```

3. **N/A 明示確認**:
   - 空のセクションは `N/A` または `該当なし` 明示必須

### Phase 5: ハイブリッド API 検証 (v3.1)

1. **Schema テーブル存在確認**:

   ```python
   has_schema_table = re.search(r'\|\s*Field\s*\|\s*Type\s*\|', section_content)
   ```

2. **Example ブロック存在確認**:

   ```python
   has_request_example = re.search(r'Request Example', section_content)
   has_response_example = re.search(r'Response Example', section_content)
   ```

3. **Example ↔ Schema 一致検証**:
   - 必須フィールド存在有無
   - タイプ一致有無
   - enum 値一致有無
   - 入れ子オブジェクト再帰検証

4. **SSOT パス有効性**:
   - `src/app/api/*/route.ts` パス抽出
   - ファイル存在有無確認

### Phase 5.5: Write Operations 検証 (v3.4 新規)

> **目的**: §0.4.5 Write Operations の一貫性と完全性検証

1. **Operation Mapping 完全性**:

   ```python
   # §0.5 API Contract の全ての Write API が §0.4.5 にマッピングされているか確認
   api_endpoints = extract_api_endpoints(spec_content)
   write_operations = extract_write_operations(spec_content)

   write_apis = [api for api in api_endpoints if api['method'] in ['POST', 'PUT', 'PATCH', 'DELETE']]

   for api in write_apis:
       if not any(op['api'] == f"{api['method']} {api['path']}" for op in write_operations['operations']):
           warnings.append(f"§0.4.5 欠落: {api['method']} {api['path']}")
   ```

2. **テーブル参照有効性**:

   ```python
   # §0.4.5 のテーブルが §0.4.2 に定義されているか確認
   db_tables = [t['table'] for t in extract_db_tables(spec_content)]

   for op in write_operations['operations']:
       if op['table'] not in db_tables:
           errors.append(f"§0.4.5 エラー: テーブル '{op['table']}'が §0.4.2 に定義されていない")
   ```

3. **トランザクション一貫性**:

   ```python
   # トランザクショングループの演算が Operation Mapping に存在するか確認
   operation_names = [op['api'] for op in write_operations['operations']]

   for tx in write_operations.get('transactions', []):
       for op in tx['operations']:
           if op not in operation_names:
               errors.append(f"§0.4.5 エラー: トランザクション '{tx['name']}'の演算 '{op}'が Operation Mapping にない")
   ```

4. **べき等性戦略適合性**:

   ```python
   # 非べき等 API に対する戦略が定義されているか確認
   non_idempotent_apis = write_operations.get('idempotency', {}).get('non_idempotent_apis', [])
   post_apis = [op['api'] for op in write_operations['operations'] if op['api'].startswith('POST')]

   for api in post_apis:
       if api not in non_idempotent_apis:
           warnings.append(f"§0.4.5 警告: POST API '{api}'が idempotency.non_idempotent_apis にない")
   ```

5. **監査ポリシー適合性** (Tier 1-2):

   ```python
   # Tier 1-2 機能で audit ポリシーが定義されているか確認
   tier = extract_tier(spec_content)
   audit = write_operations.get('audit', {})

   if tier in [1, 2] and not audit.get('enabled'):
       warnings.append("§0.4.5 警告: Tier 1-2 機能だが audit ポリシーが無効化されている")
   ```

6. **N/A 明示確認**:
   ```python
   # Write Operations セクションがないか空の場合 "N/A" 明示確認
   if not write_operations and not re.search(r'0\.4\.5.*N/A', spec_content):
       errors.append("§0.4.5 エラー: Write Operations セクションがなく N/A も明示されていない")
   ```

### Phase 6: 結果出力

```markdown
## SPEC 検証結果: SPEC-029-battle.md

### JSON Schema 検証

✅ §0.4.1 TypeScript Model: OK (1個モデル)
✅ §0.4.2 DB Table: OK (1個テーブル)
✅ §0.4.5 Write Operations: OK (3個演算)
✅ §0.5 API Contract: OK

### 構造検証

✅ 必須セクション: すべて存在
⚠️ AC 形式: 2個 AC に観測点欠落

- FR-02901 AC2: 観測点コラムが空
- FR-02902 AC1: 観測点コラムが空

### ハイブリッド API 仕様検証 (v3.1)

✅ Schema テーブル: 存在
✅ Request Example: 存在
✅ Response Example: 存在
⚠️ Error Examples: FORBIDDEN エラー例示欠落

### Write Operations 検証 (v3.4)

✅ Operation Mapping: 全ての Write API マッピング済 (3/3)
✅ テーブル参照: 全てのテーブルが §0.4.2 に定義されている
✅ トランザクション一貫性: 全てのトランザクション演算が有効
⚠️ べき等性: POST /battles に対する戦略未定義
✅ 監査ポリシー: Tier 2 機能で audit 活性化済

### SSOT パス検証 (v3.1)

✅ src/app/api/battle/start/route.ts

### 要約

| 項目             |          結果           |
| ---------------- | :---------------------: |
| JSON Schema      |           ✅            |
| 構造             |      ⚠️ 2 warnings      |
| ハイブリッド API |      ⚠️ 1 warning       |
| Write Operations |      ⚠️ 1 warning       |
| SSOT パス        |           ✅            |
| 全体             | **PASSED** (4 warnings) |
```

---

## 検証規則詳細

### 1. DB Table Schema 検証

| フィールド           | 必須 | 検証規則                       |
| -------------------- | :--: | ------------------------------ |
| `table`              |  ✅  | snake_case パターン            |
| `columns`            |  ✅  | 1個以上                        |
| `columns[].name`     |  ✅  | snake_case パターン            |
| `columns[].type`     |  ✅  | 許可された PostgreSQL タイプ   |
| `columns[].nullable` |  ⚪  | boolean (既定 true)            |
| `rls.policies`       |  ⚪  | SELECT/INSERT/UPDATE/DELETE 中 |

### 2. API Endpoint Schema 検証

| フィールド | 必須 | 検証規則                                  |
| ---------- | :--: | ----------------------------------------- |
| `id`       |  ✅  | `API-NNN-NN` パターン                     |
| `method`   |  ✅  | GET/POST/PUT/PATCH/DELETE                 |
| `path`     |  ✅  | `/`で開始                                 |
| `errors`   |  ⚪  | http, code, condition, client_action 必須 |

### 3. TypeScript Model Schema 検証

| フィールド      | 必須 | 検証規則                |
| --------------- | :--: | ----------------------- |
| `name`          |  ✅  | PascalCase パターン     |
| `fields`        |  ✅  | 1個以上                 |
| `fields[].name` |  ✅  | camelCase パターン      |
| `fields[].type` |  ✅  | TypeScript タイプ文字列 |

### 4. Write Operations Schema 検証 (v3.4 新規)

| フィールド                        | 必須 | 検証規則                                     |
| --------------------------------- | :--: | -------------------------------------------- |
| `feature_id`                      |  ✅  | `NNN` 形式 (3桁数字)                         |
| `operations`                      |  ✅  | 1個以上 (Write 機能時)                       |
| `operations[].api`                |  ✅  | `{METHOD} {path}` 形式                       |
| `operations[].action`             |  ✅  | INSERT/UPDATE/UPSERT/SOFT_DELETE/HARD_DELETE |
| `operations[].table`              |  ✅  | snake_case, §0.4.2に定義されたテーブル       |
| `operations[].fields`             |  ✅  | 1個以上のフィールド名                        |
| `transactions`                    |  ⚪  | 原子性必要時                                 |
| `transactions[].name`             |  ✅  | 識別可能な名前                               |
| `transactions[].operations`       |  ✅  | operations[].apiとマッチング                 |
| `transactions[].isolation_level`  |  ⚪  | READ_COMMITTED/REPEATABLE_READ/SERIALIZABLE  |
| `transactions[].rollback_scope`   |  ✅  | ALL/PARTIAL                                  |
| `idempotency`                     |  ⚪  | 非べき等 API ある時推奨                      |
| `idempotency.non_idempotent_apis` | ✅\* | POST API リスト (\*非べき等時)               |
| `idempotency.strategy`            | ✅\* | IDEMPOTENCY_KEY/UPSERT/NONE                  |
| `audit`                           |  ⚪  | Tier 1-2 推奨                                |
| `audit.enabled`                   |  ✅  | boolean                                      |
| `audit.operations`                |  ✅  | CREATE/UPDATE/DELETE 中                      |
| `audit.retention_days`            |  ⚪  | 正の整数                                     |

**Cross-Reference 検証**:

| 検証項目                   | 参照セクション | 検証ロジック                                          |
| -------------------------- | -------------- | ----------------------------------------------------- |
| テーブル存在               | §0.4.2         | `operations[].table`が DB スキーマに定義されている    |
| フィールド存在             | §0.4.2         | `operations[].fields`が該当テーブルカラムに存在       |
| API マッピング完全性       | §0.5           | 全ての Write API が operations にマッピングされている |
| トランザクション演算有効性 | §0.4.5.1       | transactions[].operations が operations に存在        |

---

## 失敗ケース対処

| ケース                  | 対処                                         |
| ----------------------- | -------------------------------------------- |
| **JSON パース失敗**     | 該当ブロック位置とパースエラーメッセージ出力 |
| **メタスキーマ未存在**  | 警告出力、該当ブロックスキップ               |
| **SPEC ファイル未存在** | エラー出力、終了                             |
| **空セクション**        | N/A 明示有無確認、未明示時警告               |

---

## CLI オプション

| オプション | 説明                                  | 例示                           |
| ---------- | ------------------------------------- | ------------------------------ |
| `--all`    | 全ての SPEC 検証                      | `/spec-validator --all`        |
| `--json`   | JSON 形式出力                         | `/spec-validator 029 --json`   |
| `--fix`    | 自動修正可能な項目修正 (例: N/A 追加) | `/spec-validator 029 --fix`    |
| `--strict` | 警告も失敗で処理                      | `/spec-validator 029 --strict` |

---

## Makefile 連動

```makefile
# SPEC 検証
spec.validate:
	@echo "SPEC 検証中..."
	@python .claude/skills/spec-validator/scripts/validate.py $(SPEC)

spec.validate-all:
	@python .claude/skills/spec-validator/scripts/validate.py --all
```

**使用例示**:

```bash
make spec.validate SPEC=docs/features/029-battle/SPEC-029.md
make spec.validate-all
```

---

## 統合ワークフロー

```
[feature-spec-generator]
        ↓
    SPEC.md 生成
        ↓
[spec-validator] ←── 自動または手動実行
        ↓
    ┌────┴────┐
    ↓         ↓
 PASS      FAIL
    ↓         ↓
[実装進行]  [SPEC 修正 → 再検証]
```

---

## 参照文書

- [メタスキーマ: db_table](../../docs/_templates/schemas/db_table.schema.json)
- [メタスキーマ: api_endpoint](../../docs/_templates/schemas/api_endpoint.schema.json)
- [メタスキーマ: typescript_model](../../docs/_templates/schemas/typescript_model.schema.json)
- [メタスキーマ: write_operations](../../docs/_templates/schemas/write_operations.schema.json) ← v3.4 新規
- [SPEC テンプレート](../../docs/_templates/spec_template.md)
- [SPEC セクションガイド](../feature-spec-generator/references/spec-sections.md)
