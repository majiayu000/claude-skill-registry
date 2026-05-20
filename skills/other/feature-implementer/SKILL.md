---
name: feature-implementer
description: SPEC.mdとScreen文書を入力としてTDD方式で実際のコードを実装するスキル。feature-spec-generatorとreadiness-gateの間の「実装実行者(Executor)」の役割を担う。
doc_contract:
  review_interval_days: 90
---

# Feature Implementer

> **コアコンセプト**: "設計 → コード"の実行者 (The Executor)

このスキルは `feature-spec-generator` が生成した SPEC.md と Screen 文書を入力として、TDD 原則に従いテストとコードを実装します。

## プロジェクト技術スタック前提 (MUST)

> **重要**: このスキルは プロジェクト プロジェクトの技術スタックに合わせて設計されています。

| 項目                   | スタック                                      | 詳細                       |
| ---------------------- | --------------------------------------------- | -------------------------- |
| **アーキテクチャ**     | Feature-First + Simplified Clean Architecture | src/features/ ベース       |
| **状態管理**           | React Hooks                                   | `useXxx()` カスタムフック  |
| **データモデル**       | Zod schema                                    | バリデーション付き型定義   |
| **エラーハンドリング** | try-catch + logger                            | Fail-Fast 原則             |
| **テスト**             | Vitest + React Testing Library                | `renderHook` + `vi.mock()` |

---

## 役割分界

| スキル                     | 責務                                                        | Output                                    |
| -------------------------- | ----------------------------------------------------------- | ----------------------------------------- |
| **feature-architect**      | 意図確定 (Why/Value)、コンテキスト収集、spec-generator 呼出 | `CONTEXT.json`                            |
| **feature-spec-generator** | 入力を実装可能な契約に翻訳                                  | `SPEC.md`, `screens/*.md`                 |
| **feature-implementer**    | SPECをTDDで実装                                             | `src/**/*.ts(x)`, `tests/**/*.test.ts(x)` |
| **feature-wiring**         | Export/ルート/データフロー統合検証                          | Go/No-Go 判定                             |

---

## プロトコル (Protocol)

### Phase 0: 事前検証 (Pre-validation)

1. **CLAUDE.md アーキテクチャルール必読** (MUST):
   - CLAUDE.md の「アーキテクチャ概要」「Feature-First依存関係ルール」セクションを確認
   - Feature-First 依存関係ルール確認
   - プロジェクト構造の標準パス確認

   > **この確認を行わずに実装を開始してはいけません。**

2. **SPEC ロード**: `docs/features/<feature-id>/SPEC-<NNN>-*.md` 読込
3. **完全性検査**: 必須セクション存在確認
   - `## 0. AI 実装契約` - Target Files, State/Hook, Error Handling, Data Model
   - `## 2. 機能要件` - FR 単位仕様
   - `## 3. 依存性 & リスク` - API 契約
4. **不完全時の差し戻し**: SPECが不完全なら `feature-spec-generator` へ差し戻し

   ```
   SPEC 不完全 - Generator へ差し戻し

   不足項目:
   - [ ] §0.2 State/Hook 構造未定義
   - [ ] §0.4 Data Model 未定義

   → /feature-spec-generator を実行して SPEC を補完してください。
   ```

5. **CONTEXT.json 参照**: Hard Constraints 確認 (違反禁止事項の把握)

6. **UI Flow SSOT 参照** (ui_feature 時 MUST):
   - `docs/ui-flow/ui-flow.json` を読み取り、以下を把握:
     - 既存パネル一覧と visibility 条件
     - SSE イベント → 状態遷移マッピング
     - フェーズ別レイアウト構成
   - SPEC §1.5 UI Flow Contract の `json:schema/ui_flow_contract` ブロックと照合
   - `operation: "new"` のパネルは実装完了後に `ui-flow.json` への追加が必要（feature-wiring で検証）

---

### Phase 1: 実装計画策定 (Implementation Planning)

1. **Target Files 分析**:
   - SPEC §0.1 から実装対象ファイル一覧抽出
   - 状態別分類: 完了 / 進行中 / 未着手

2. **依存関係グラフ構築** (Feature-First 基準):

   ```
   [Type + Zod Schema] → [API Layer] → [Custom Hook] → [UI Component]
         ↓                    ↓              ↓               ↓
   src/features/<feature>/types/  →  api/  →  hooks/  →  components/
   ```

3. **実装順序決定** (Bottom-Up):
   ```
   1. Type + Zod Schema (型定義 + バリデーション) ─┐
   2. API Layer (fetch / API Route)              ─┘ 並列可
   3. Custom Hook (useXxx)
   4. Component / Page (UI)
   5. Test (各レイヤー)
   ```

### Phase 2: TDD 実装サイクル (Red-Green-Refactor)

> **原則**: 各ファイルごとに必ずテストを先に作成

**単一ファイル実装サイクル**:

```
+-------------------------------------------------------------+
| 1. RED: 失敗するテスト作成                                      |
|    - SPEC の AC(Acceptance Criteria) をテストケースに変換       |
|    - SPEC の EC(Edge Cases) を追加テストに変換                 |
|    - `npm test <test_file>` → 失敗確認                       |
+-------------------------------------------------------------+
| 2. GREEN: テストを通過する最小コード実装                         |
|    - SPEC の "AI 実装ヒント" 参照                              |
|    - 既存パターン準拠 (プロジェクトコンベンション)                 |
|    - `npm test <test_file>` → 通過確認                       |
+-------------------------------------------------------------+
| 3. REFACTOR: コード品質改善                                    |
|    - 重複排除、ネーミング改善                                   |
|    - `npm run lint` → 警告なし確認                            |
|    - テスト依然として通過確認                                   |
+-------------------------------------------------------------+
```

### Phase 3: FR 単位実装 (Feature Request Implementation)

SPEC の各 FR(Feature Request) を順序通りに実装します。

**FR 実装チェックリスト**:

> **⚡ CHECKLIST UPDATE RULE (MANDATORY)**:
> 各 FR の実装工程で、テスト作成/コード実装/品質検証の各項目完了時にチェックリストを再出力し `[ ]` を `[x]` に更新すること。
> 全項目 `[x]` 確認後に次の FR へ進行すること。
> **未更新のまま次段階に進行 = Violation Protocol 違反 (severity: HIGH)**

```markdown
## FR-NNNNN 実装

### テスト作成 (Red)

- [ ] Unit Test: `tests/unit/features/<feature>/<name>.test.ts(x)` 作成
- [ ] AC 別テストケース作成
- [ ] EC 別エッジケーステスト作成
- [ ] `npm test <path>` → 失敗確認

### コード実装 (Green)

- [ ] Type + Zod Schema 実装 (必要時)
- [ ] API Layer 実装 (必要時)
- [ ] Custom Hook 実装 (必要時)
- [ ] Component/Page 実装 (必要時)
- [ ] `npm test <path>` → 通過確認

### 品質検証 (Refactor)

- [ ] `npm run lint` 通過
- [ ] コード重複排除
- [ ] SPEC の Error Handling Policy 準拠確認
```

### Phase 4: 統合及び引継ぎ (Integration & Handover)

1. **全体テスト実行**:

   ```bash
   npm test
   ```

2. **Lint 検証**:

   ```bash
   npm run lint
   ```

3. **SPEC 状態更新**:
   - SPEC §0.1 の Target Files 状態を完了に更新
   - 変更履歴(§5) に実装完了記録

4. **引継ぎメッセージ**:

   ```markdown
   実装完了

   生成/修正されたファイル:

   - src/features/<feature>/types/index.ts (新規)
   - src/features/<feature>/api/<feature>-api.ts (新規)
   - src/features/<feature>/hooks/use-<feature>.ts (新規)
   - src/features/<feature>/components/<Feature>Panel.tsx (新規)
   - src/features/<feature>/index.ts (バレルファイル更新)
   - tests/unit/features/<feature>/use-<feature>.test.ts (新規)

   テスト結果:

   - 全体テスト: N件 通過
   - 新規テスト: M件 追加

   次のステップ:
   → /feature-wiring <feature-id> を実行して統合検証を行ってください。
   ```

---

## Wisdom 直接記録

> **目的**: 実装過程の学習内容を Wisdom に直接記録してセッション間の連続性を確保

### 作業開始時

**Wisdom 参照** (既存パターン確認):

```bash
Read(".claude/wisdom/project-patterns.md")   # プロジェクトパターン確認
Read(".claude/wisdom/common-errors.md")       # エラー解決策参照
```

### 作業中に学習発生時

**即時 Wisdom に記録** (APPEND のみ使用):

#### 1. 新しいパターン発見時

```bash
bash -c "echo '
## {パターン名}

**状況**: {どの状況で使用するか}
**実装**: \`\`\`typescript
// コード例
\`\`\`
**根拠**: {なぜこの方法が良いか}

---
' >> .claude/wisdom/project-patterns.md"
```

#### 2. エラー解決時

```bash
bash -c "echo '
### {エラー概要}

**原因**: {根本原因}
**解決**: {適用した解決策}
**再発防止**: {同一問題防止方法}

---
' >> .claude/wisdom/common-errors.md"
```

### 注意事項

**APPEND 専用**:

```bash
# 正しい使用
bash -c "echo 'content' >> .claude/wisdom/file.md"

# 誤った使用 (上書き)
bash -c "echo 'content' > .claude/wisdom/file.md"
```

**即時記録**: 作業中に発生したら即記録 (後で整理は禁止)

---

## 実装原則 (Implementation Principles)

### 1. SPEC が Single Source of Truth

| 項目         | 参照位置                         |
| ------------ | -------------------------------- |
| データモデル | SPEC §0.4 Data Model             |
| 状態構造     | SPEC §0.2 State/Hook             |
| エラー処理   | SPEC §0.3 Error Handling Policy  |
| 受入基準     | SPEC §2 各 FR の AC              |
| エッジケース | SPEC §2 各 FR の EC              |
| 実装ヒント   | SPEC §2 各 FR の "AI 実装ヒント" |

### 2. Hard Constraints 絶対準拠

CONTEXT.json の Hard Constraints は **いかなる状況でも違反禁止** です。

```markdown
## 違反時は即座に中断してユーザーに報告

例:

- "DB スキーマ変更禁止" → 新テーブル必要時 → 中断 & 報告
- "外部パッケージ追加禁止" → 新パッケージ必要時 → 中断 & 報告
```

### 3. 既存パターン準拠 (プロジェクト標準)

| パターン          | プロジェクトコンベンション                               |
| ----------------- | -------------------------------------------------------- |
| **フォルダ構造**  | `src/features/{name}/types/` 等                          |
| **Import ルール** | バレルファイル (index.ts) 経由のみ、内部直接 import 禁止 |
| **状態管理**      | `useXxx()` カスタムフック                                |
| **エラー処理**    | `try-catch` + logger                                     |
| **データモデル**  | `interface` + `z.object()` (Zod schema)                  |
| **API Layer**     | `async function` + `fetch`                               |
| **テストモック**  | `vi.mock()` + `renderHook` (React Testing Library)       |
| **ネーミング**    | kebab-case ファイル名、PascalCase コンポーネント名       |
| **UIテキスト**    | `messages.ts` 経由 (ハードコーディング禁止)              |

### 4. 段階的実装

一度に全体を実装しません。

```
BAD:  全ファイルを一括作成
GOOD: 一つのFR → テスト → 実装 → 検証 → 次のFR
```

---

## コードテンプレート

### Type + Zod Schema

```typescript
// src/features/<feature>/types/index.ts

import { z } from 'zod';

/** [機能名] データモデルスキーマ */
export const xxxSchema = z.object({
  id: z.string(),
  name: z.string(),
  // ... フィールド
});

/** [機能名] データモデル型 */
export type XxxModel = z.infer<typeof xxxSchema>;
```

### API Layer

```typescript
// src/features/<feature>/api/<feature>-api.ts

import { xxxSchema, type XxxModel } from '../types';
import { logger } from '@/shared/lib/logger';

const TAG = 'XxxApi';

/**
 * [機能名] データ取得
 *
 * @param id - 対象ID
 * @returns データ (失敗時は null)
 */
export async function fetchXxx(id: string): Promise<XxxModel | null> {
  try {
    const response = await fetch(`/api/xxx/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    return xxxSchema.parse(data);
  } catch (error) {
    logger.error(TAG, 'Error fetching xxx', error);
    return null;
  }
}
```

### Custom Hook

```typescript
// src/features/<feature>/hooks/use-<feature>.ts

'use client';

import { useState, useEffect, useCallback } from 'react';
import { fetchXxx } from '../api/<feature>-api';
import { type XxxModel } from '../types';
import { MESSAGES } from '@/shared/constants/messages';
import { logger } from '@/shared/lib/logger';

const TAG = 'useXxx';

/** [機能名] フック状態 */
interface XxxState {
  data: XxxModel | null;
  isLoading: boolean;
  error: string | null;
}

/**
 * [機能名] カスタムフック
 *
 * @param id - 対象ID
 * @returns 状態とアクション
 */
export function useXxx(id: string) {
  const [state, setState] = useState<XxxState>({
    data: null,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        logger.debug(TAG, `Loading xxx: ${id}`);
        const data = await fetchXxx(id);

        if (cancelled) return;

        if (data === null) {
          setState({ data: null, isLoading: false, error: MESSAGES.errors.dataNotFound });
          return;
        }

        setState({ data, isLoading: false, error: null });
      } catch (error) {
        if (cancelled) return;
        logger.error(TAG, 'Error loading xxx', error);
        setState({ data: null, isLoading: false, error: MESSAGES.errors.loadFailed });
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [id]);

  const doSomething = useCallback(async () => {
    setState((prev) => ({ ...prev, isLoading: true }));

    try {
      // ビジネスロジック
      setState((prev) => ({ ...prev, isLoading: false }));
    } catch (error) {
      logger.error(TAG, 'Error doing something', error);
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: MESSAGES.errors.operationFailed,
      }));
    }
  }, []);

  return { ...state, doSomething };
}
```

---

## テスト作成ガイド

### テストファイル構造

```typescript
// tests/unit/features/<feature>/hooks/use-<feature>.test.ts

import { renderHook, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { useXxx } from '@/features/<feature>/hooks/use-<feature>';
import * as xxxApi from '@/features/<feature>/api/<feature>-api';
import type { XxxModel } from '@/features/<feature>/types';

// モック設定
vi.mock('@/features/<feature>/api/<feature>-api');

describe('useXxx', () => {
  const mockData: XxxModel = { id: 'test-id', name: 'Test' };

  beforeEach(() => {
    vi.resetAllMocks();
  });

  // AC ベーステスト
  describe('AC1: データロード成功', () => {
    it('サービスがデータを返した場合、正常にロードされること', async () => {
      // Arrange
      vi.mocked(xxxApi.fetchXxx).mockResolvedValue(mockData);

      // Act
      const { result } = renderHook(() => useXxx('test-id'));

      // Assert
      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });
      expect(result.current.data).toEqual(mockData);
      expect(result.current.error).toBeNull();
    });
  });

  // EC ベーステスト
  describe('EC1: データなし', () => {
    it('サービスがnullを返した場合、エラーが設定されること', async () => {
      // Arrange
      vi.mocked(xxxApi.fetchXxx).mockResolvedValue(null);

      // Act
      const { result } = renderHook(() => useXxx('test-id'));

      // Assert
      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });
      expect(result.current.data).toBeNull();
      expect(result.current.error).toBeTruthy();
    });
  });

  describe('EC2: ネットワークエラー', () => {
    it('サービスが例外を投げた場合、エラーが設定されること', async () => {
      // Arrange
      vi.mocked(xxxApi.fetchXxx).mockRejectedValue(new Error('Network error'));

      // Act
      const { result } = renderHook(() => useXxx('test-id'));

      // Assert
      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });
      expect(result.current.data).toBeNull();
      expect(result.current.error).toBeTruthy();
    });
  });
});
```

### AC/EC → テスト変換規則

> **BDD 5-column テーブルマッピング**: SPEC の AC テーブルをテストコードに直接変換

| BDD カラム           | テストマッピング                  | コード役割                                     |
| -------------------- | --------------------------------- | ---------------------------------------------- |
| **Given (事前条件)** | Arrange (`beforeEach`, Mock 設定) | `vi.mocked(api.method).mockResolvedValue(...)` |
| **When (行動)**      | Act (実行)                        | `renderHook(() => useXxx(...))`                |
| **Then (期待結果)**  | Assert (検証)                     | `expect(result.current.xxx).toBe(...)`         |
| **観測点**           | `expect()` matcher 対象           | 具体的変数名、状態値                           |

---

## エラーハンドリング規約

### API Layer

| 状況       | 処理                                |
| ---------- | ----------------------------------- |
| データなし | `null` 返却                         |
| 例外発生   | `logger.error()` ログ後 `null` 返却 |

### Custom Hook Layer

| 状況             | 処理                                                             |
| ---------------- | ---------------------------------------------------------------- |
| API が null 返却 | `state.error = MESSAGES.errors.xxx` 設定                         |
| 例外発生         | `logger.error()` ログ + `state.error = MESSAGES.errors.xxx` 設定 |

---

## AI 行動指針

### DO (やるべきこと)

- CLAUDE.md のアーキテクチャルール確認後に実装開始
- SPEC の全 AC をテストケースに変換
- テストを先に作成してから実装 (Red-Green-Refactor)
- 既存コードパターン参照 (`src/` 内の類似ファイル確認)
- バレルファイル (index.ts) を通じた import のみ使用
- エラー処理は `try-catch` + `logger` 使用
- 各 FR 完了後にテスト実行して確認
- UIテキストは `messages.ts` 経由で参照

### DON'T (やってはいけないこと)

- CLAUDE.md のルール確認なしに実装開始
- CONTEXT.json の Hard Constraints 違反
- テストなしでコード実装
- SPEC にない機能追加 (Over-engineering)
- 既存インターフェースシグネチャ変更 (Soft Constraint で許可されない限り)
- `any` 型の濫用 (明示的型 or `unknown` + 型ガード使用)
- 一度に全ファイル作成 (段階的実装)
- Feature 外部にコード作成 (レガシーパス使用禁止)
- バレルファイルを迂回して内部ファイル直接 import
- `console.log` 使用 (logger 使用)

---

## 失敗ケース対処

| ケース                          | 対処                                          |
| ------------------------------- | --------------------------------------------- |
| **SPEC 不完全**                 | 実装中断、`feature-spec-generator` へ差し戻し |
| **Hard Constraint 衝突**        | 実装中断、ユーザーに承認要求                  |
| **テスト失敗持続**              | 原因分析後報告、必要時 SPEC 再検討要求        |
| **外部 API スキーマ不一致**     | SPEC の API 契約と実際 API 比較、差異報告     |
| **Tier 1 セキュリティ作業検出** | 即時停止、ユーザー確認必須 (認証/決済/PII)    |

---

## 自律停止条件 (Auto-Stop Conditions)

> **原則**: 以下の条件検出時 **即座に作業中断** 後ユーザー確認要求

### Tier 1 (High Risk) - 即時停止

| 検出条件                | 必要措置             |
| ----------------------- | -------------------- |
| 認証/権限関連コード修正 | ユーザー承認必須     |
| 決済/課金ロジック       | ユーザー承認必須     |
| 個人情報(PII) 処理      | セキュリティ検討必須 |

### Tier 2 (Medium Risk) - 注意進行

| 検出条件                   | 処理                 |
| -------------------------- | -------------------- |
| 外部 API 連携              | 契約確認後進行       |
| 複数画面にまたがる状態管理 | 既存パターン準拠確認 |
| API Route 新規/修正        | テスト必須           |

---

## CONTEXT.json 直接更新

> **状態遷移**: `SpecDrafting` / `SpecUpdating` → `Implementing`

作業中/完了時に **CONTEXT.json を直接更新** します:

### 実装開始時

```json
{
  "quick_resume": {
    "current_state": "Implementing",
    "current_task": "FR-02901 実装中 - 機能名",
    "next_actions": ["FR-02901 テスト作成", "FR-02902 実装"],
    "last_updated_at": "2026-02-11T12:00:00+09:00"
  }
}
```

### 各 FR 完了時

```json
{
  "progress": {
    "percentage": 40,
    "fr_total": 5,
    "fr_completed": 2,
    "fr_in_progress": 1,
    "details": {
      "FR-02901": { "status": "completed", "files": ["src/features/xxx/types/index.ts"] },
      "FR-02902": { "status": "completed", "files": ["src/features/xxx/api/xxx-api.ts"] },
      "FR-02903": { "status": "in_progress", "files": [] }
    }
  }
}
```

### 全体実装完了時

```json
{
  "quick_resume": {
    "current_state": "Implementing",
    "current_task": "全体実装完了、状態同期待機",
    "next_actions": ["feature-wiring 実行", "feature-status-sync 実行"]
  },
  "progress": {
    "percentage": 100,
    "fr_completed": 5,
    "fr_in_progress": 0
  }
}
```

---

## 使用例

```bash
# 基本使用 - 機能IDで呼出
/feature-implementer 001

# SPEC パス直接指定
/feature-implementer docs/features/001-code-analysis/SPEC-001-code-analysis.md

# 特定 FR のみ実装
/feature-implementer 001 --fr FR-00101

# テストのみ生成 (実装なし)
/feature-implementer 001 --tests-only
```

---

## 統合ワークフロー

```
[アイデア]
     |
[feature-architect] → CONTEXT.json 生成
     |
[feature-spec-generator] → SPEC/Screen 生成
     |
[ui-approval-gate] → UI 承認
     |
[feature-implementer] → TDD 実装  ← ここ!
     |
[feature-wiring] → 統合検証
     |
[完了] → コミット & PR
```

---

## フォルダ構造参照

> **Feature-First アーキテクチャ**: 全コードは `src/features/<feature>/` 配下に配置

```
src/features/<feature>/
├── components/          # 機能固有 UI コンポーネント
│   └── <Feature>Panel.tsx
├── hooks/               # 機能固有カスタムフック
│   └── use-<feature>.ts
├── api/                 # API 呼出/データフェッチ
│   └── <feature>-api.ts
├── types/               # 機能固有型定義
│   └── index.ts         # Zod schema + 型
└── index.ts             # バレルファイル (公開 API)

tests/unit/features/<feature>/
├── hooks/
│   └── use-<feature>.test.ts
└── api/
    └── <feature>-api.test.ts
```

---

## 参照文書

| 優先順位 | 文書                                  |   必須   |
| :------: | ------------------------------------- | :------: |
|    1     | **CLAUDE.md** (アーキテクチャ/ルール) | **必須** |
|    2     | SPEC テンプレート                     |   必須   |
|    3     | 既存 feature 実装例 (`src/features/`) |   推奨   |

> CLAUDE.md のアーキテクチャルールは実装開始前に必ず確認してください。
