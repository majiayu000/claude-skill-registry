---
name: bug-fix
description: |
  プロジェクト プロジェクトのバグ修正専用スキル。
  バグレポートを分析し、根本原因を特定して修正し、回帰テストを追加する。
  feature-pilot から BUG_FIX 作業タイプで呼び出されるか、直接使用可能。

  "バグ修正", "エラー発生", "動かない", "動作しない", "クラッシュ", "fix bug" 等のリクエストでトリガーされる。

  <example>
  user: "説明パネルでストリーミングが途中で止まる"
  assistant: "bug-fix スキルを使用してストリーミングバグを分析・修正します"
  </example>

  <example>
  user: "クイズの回答選択後にスコアが反映されない"
  assistant: "bug-fix スキルを使用して状態更新バグを分析します"
  </example>
doc_contract:
  review_interval_days: 90
---

# Bug Fix (バグ修正スキル)

> **核心コンセプト**: "再現 → 根本原因 → 修正 → 回帰防止" (Reproduce → Root Cause → Fix → Prevent Regression)

このスキルはバグレポートを受け取り体系的に分析し、根本原因を特定して修正し、同じバグが再発しないようテストを追加します。

## プロジェクト技術スタック前提

| 項目                   | スタック                                          | 備考                     |
| ---------------------- | ------------------------------------------------- | ------------------------ |
| **アーキテクチャ**     | Feature-First + Simplified Clean Architecture     | Components → Hooks → API |
| **状態管理**           | React Hooks (useState, useReducer, useContext)    | Custom Hook パターン     |
| **エラーハンドリング** | try-catch + logger                                | **サイレント失敗禁止**   |
| **テスト**             | Vitest + vi.mock() + renderHook (testing-library) | React Testing Library    |

---

## 役割分担

| 状況         | 担当スキル                                                       |
| ------------ | ---------------------------------------------------------------- |
| 新機能開発   | feature-architect → feature-spec-generator → feature-implementer |
| 既存機能修正 | feature-spec-updater → feature-implementer                       |
| **バグ修正** | **bug-fix** (このスキル)                                         |

---

## 入力 (Input)

| 必須 | 項目              | 例                                   |
| :--: | ----------------- | ------------------------------------ |
|  ✅  | バグ症状説明      | "ストリーミングが途中で止まる"       |
|  -   | 再現経路          | "コード入力 → 分析実行 → 説明パネル" |
|  -   | エラーログ        | コンソール出力、スタックトレース     |
|  -   | 関連ファイル/画面 | "ExplanationPanel.tsx"               |

---

## プロトコル (Protocol)

### Phase 1: バグ分析 (Bug Analysis)

> **目標**: バグの正確な位置と条件の把握

**Step 1.1: 症状整理**

```markdown
## バグ症状整理

| 項目         | 内容                           |
| ------------ | ------------------------------ |
| **症状**     | [ユーザーが報告した問題]       |
| **期待動作** | [正常に動作すべき方式]         |
| **実際動作** | [現在発生している問題]         |
| **深刻度**   | Critical / High / Medium / Low |
```

**Step 1.2: 関連コード探索**

```bash
# キーワードで関連ファイル検索
Grep "<keyword>" src/ --type ts --type tsx

# 特定画面/機能の関連ファイル確認 (Feature-First構造)
Glob src/features/<feature>/components/
Glob src/features/<feature>/hooks/
```

**Step 1.3: 再現条件確認**

| 質問                   | 回答                     |
| ---------------------- | ------------------------ |
| 常に再現されるか？     | Y/N                      |
| 特定条件でのみ発生？   | [条件]                   |
| 特定データでのみ発生？ | [データ特性]             |
| 最近の変更と関連？     | [コミットまたは変更履歴] |

---

### Phase 2: 根本原因分析 (Root Cause Analysis)

> **目標**: "なぜ" バグが発生したかを把握

**Step 2.1: コードフロー追跡**

Feature-First + Simplified Clean Architecture 基準のフロー分析:

```
[UI Event] → [Custom Hook] → [API Call] → [Response]
     ↓            ↓              ↓            ↓
   確認        状態変更       fetch実行    データ処理
```

**Step 2.2: 仮説立案と検証**

```markdown
### 仮説リスト

| #   | 仮説    | 検証方法   | 結果  |
| --- | ------- | ---------- | ----- |
| 1   | [仮説1] | [検証方法] | OK/NG |
| 2   | [仮説2] | [検証方法] | OK/NG |
| 3   | [仮説3] | [検証方法] | OK/NG |
```

**Step 2.3: 根本原因確定**

```markdown
## 根本原因

**位置**: `src/features/<feature>/hooks/<file>.ts:123`

**原因**: [具体的な原因説明]

**影響範囲**: [他の機能への影響]
```

---

### Phase 3: 修正実装 (Fix Implementation)

> **目標**: 最小限の変更でバグ修正

**Step 3.1: 修正方針決定**

| 方針   | 長所   | 短所   | 選択 |
| ------ | ------ | ------ | :--: |
| 方針 A | [長所] | [短所] |  -   |
| 方針 B | [長所] | [短所] |  -   |

**選択基準**:

- 最小変更範囲
- 既存パターン準拠
- 副作用最小化

**Step 3.2: 回帰テスト先行作成 (TDD)**

バグ修正前に、バグを再現するテストケース作成:

```typescript
// tests/unit/features/<feature>/<file>.test.ts

describe('BUG: [バグタイトル]', () => {
  it('should [正常動作] when [条件]', async () => {
    // Arrange - バグ発生条件設定
    // Act - バグトリガー
    // Assert - 正常動作確認 (現時点では失敗)
  });
});
```

```bash
# テスト失敗確認 (Red) - 必ず失敗してから進行
npm test -- tests/unit/features/<feature>/<file>.test.ts
```

**Step 3.3: 失敗確認 (Red)**

- テストが **成功した場合** → テストが不正 → 修正して再実行
- テストが **失敗した場合** → 次のステップへ進行

**Step 3.4: コード修正 (Green)**

```typescript
// 修正前
// [問題のあるコード]

// 修正後
// [修正されたコード]
```

```bash
# テスト通過確認
npm test -- tests/unit/features/<feature>/<file>.test.ts
```

**Step 3.5: 静的分析**

```bash
npm run lint
```

---

### Phase 4: 検証と完了 (Verification & Completion)

**Step 4.1: 全体テスト実行**

```bash
npm test
```

**Step 4.2: 影響範囲確認**

> **⚡ CHECKLIST UPDATE RULE (MANDATORY)**:
> 各確認項目の完了時にチェックリストを再出力し `[ ]` を `[x]` に更新すること。
> 全項目 `[x]` 確認後に次ステップへ進行すること。
> **未更新のまま次段階に進行 = Violation Protocol 違反 (severity: HIGH)**

- [ ] 修正されたファイルと関連する他の機能の動作確認
- [ ] 修正による新しい警告なし
- [ ] 既存テストすべて通過

**Step 4.3: 完了報告**

```markdown
## バグ修正完了

### バグ要約

| 項目         | 内容                  |
| ------------ | --------------------- |
| **症状**     | [症状]                |
| **根本原因** | [原因]                |
| **修正位置** | `<ファイルパス>:<行>` |

### 変更履歴

| ファイル    | 変更タイプ | 説明       |
| ----------- | ---------- | ---------- |
| `src/...`   | 修正       | [説明]     |
| `tests/...` | 追加       | 回帰テスト |

### 検証結果

- 回帰テスト追加・通過
- 全体テスト通過
- npm run lint 通過

### 次のステップ

→ コミット準備完了
```

---

## 特殊ケース処理

### Case 1: エラーログがある場合

```markdown
## エラーログ分析

**エラータイプ**: [Exception/Error タイプ]
**発生位置**: [スタックトレースから抽出]
**発生条件**: [ログから把握した条件]
```

### Case 2: 再現が困難な場合

1. **ログ強化**: 疑わしい箇所に logger 追加
2. **条件範囲の絞り込み**: 可能な条件を一つずつテスト
3. **類似ケース検索**: 同じパターンの他のコードを確認

### Case 3: 複数原因が複合した場合

1. **分離**: 各原因を別イシューに分離
2. **優先順位**: 最も影響が大きいものから修正
3. **順次修正**: 一つずつ修正しながら中間検証

### Case 4: SPECに関連するバグ

バグがSPEC仕様のエラーに起因する場合:

```markdown
SPEC修正が必要

**問題**: SPECの[セクション]に明示された動作が実際の要件と異なる

**提案**:

1. SPEC修正: `/feature-spec-updater <機能ID>`
2. その後バグ修正を進行
```

---

## バグ深刻度分類

|    深刻度    | 基準                         | 対応                 |
| :----------: | ---------------------------- | -------------------- |
| **Critical** | アプリクラッシュ、データ損失 | 即時修正             |
|   **High**   | 核心機能不可                 | 24時間以内に修正     |
|  **Medium**  | 機能の制限的動作             | 次回リリース前に修正 |
|   **Low**    | UI崩れ、誤字                 | 余裕を持って修正     |

---

## エラーハンドリング規約 (復習)

### API層

```typescript
/** データ取得 */
async function fetchData(id: string): Promise<DataModel | null> {
  try {
    const response = await fetch(`/api/data/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return (await response.json()) as DataModel;
  } catch (error) {
    logger.error('fetchData', `Error fetching data: ${error}`);
    return null;
  }
}
```

### Custom Hook層

```typescript
/** データ取得Hook */
function useData(id: string) {
  const [data, setData] = useState<DataModel | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const result = await fetchData(id);
        if (result === null) {
          setError(MESSAGES.ERROR.DATA_NOT_FOUND);
          return;
        }
        setData(result);
      } catch (e) {
        logger.error('useData', `Error: ${e}`);
        setError(MESSAGES.ERROR.LOAD_FAILED);
      }
    };
    load();
  }, [id]);

  return { data, error };
}
```

---

## AI 行動指針

### DO (すべきこと)

- バグ症状を正確に把握してから分析開始
- 仮説を立てて検証しながら根本原因を探索
- **修正前に必ず回帰テスト作成** (TDD)
- 最小限の変更で問題解決
- 既存コードパターン・コンベンション準拠
- `npm run lint` 通過確認
- 修正完了後に全体テスト実行
- 変更履歴と検証結果を明確に報告

### DON'T (してはいけないこと)

- 症状だけ見て原因推測で修正開始
- テストなしでコード修正
- バグと無関係なリファクタリングを同時進行
- 副作用検討なしに修正完了
- **Workaround/一時的対処の適用** (根本解決必須)
- エラー無視 (`catch (e) {}`)
- サイレント失敗の導入

---

## CONTEXT.json 直接更新

> **状態遷移**: `Any State` → `BugFixing`

バグ修正作業はどの状態からでも開始可能。作業開始/完了時に **CONTEXT.json を直接更新**:

### バグ修正開始時

```markdown
## CONTEXT.json 更新内容

1. Read `docs/features/<id>/CONTEXT.json`
2. Edit:
   - quick_resume.current_state → "BugFixing"
   - quick_resume.current_task → "バグ分析: [症状]"
   - quick_resume.next_actions → ["根本原因把握", "回帰テスト作成", "修正実装"]
   - quick_resume.last_updated_at → 現在時刻
   - history[] += 状態遷移記録
```

### バグ修正完了時

```json
{
  "quick_resume": {
    "current_state": "SyncingStatus",
    "current_task": "バグ修正完了、状態同期待ち",
    "next_actions": ["feature-status-sync 実行", "index.md 状態反映"],
    "last_updated_at": "2026-02-11T15:30:00+09:00"
  },
  "decisions": [
    {
      "at": "2026-02-11T15:30:00+09:00",
      "summary": "バグ根本原因: [原因要約]",
      "rationale": "[修正方針選択理由]"
    }
  ],
  "history": [
    {
      "at": "2026-02-11T15:30:00+09:00",
      "from_state": "BugFixing",
      "to_state": "SyncingStatus",
      "triggered_by": "bug-fix",
      "note": "バグ修正完了 - [症状] → [修正内容]"
    }
  ]
}
```

---

## Wisdom 直接記録

> **目的**: バグ修正過程の学習内容を Wisdom に直接記録し、類似バグの再発防止

### 作業開始時

**Wisdom 参照** (既存エラーパターン確認):

```bash
Read(".claude/wisdom/common-errors.md")
Read(".claude/wisdom/project-patterns.md")
```

### 作業中に学習発生時

**即座に Wisdom に記録** (APPENDのみ使用):

#### 1. 新しいエラーパターン発見時

```markdown
## {エラー名}

**症状**: {バグ発生状況}
**根本原因**: {なぜ発生したか}
**解決方法**: {どう修正したか}

\`\`\`typescript
// 修正前
{問題コード}

// 修正後
{解決コード}
\`\`\`

**再発防止**: {同一バグ予防策}
**テスト**: {回帰テスト追加}
```

#### 2. 新しい解決パターン発見時

```markdown
## {パターン名}

**状況**: {いつ使用するか}
**実装**: \`\`\`typescript
{コード例}
\`\`\`
**根拠**: {なぜこの方法が良いか}
```

### 注意事項

**バグ修正特化ルール**:

- **再現手順** 記録必須 (他の開発者が理解できるよう)
- **エラーログ** 全文含む (スタックトレース全体)
- **回帰テスト** 必ず作成 (同一バグ再発防止)

---

## 使用例

```bash
# 直接呼び出し
/bug-fix "説明パネルでストリーミングが途中で止まる"

# エラーログと共に
/bug-fix "クイズ回答時にNull エラー発生" --log "<エラーログ>"

# 特定ファイル指定
/bug-fix "Diff表示が崩れる" --file src/features/diff-view/components/DiffViewPanel.tsx
```

---

## 参照文書

- [CLAUDE.md - エラーハンドリング規約](../../../CLAUDE.md)

---

## 変更履歴

| 日付       | バージョン | 変更内容                                         |
| ---------- | ---------- | ------------------------------------------------ |
| 2026-02-11 | v1.0       | プロジェクト 向けに新規作成 - Next.js/TypeScript |
