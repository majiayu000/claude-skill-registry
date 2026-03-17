---
name: feature-wiring
description: |
  プロジェクト プロジェクトの機能統合検証スキル。
  実装された機能の Export、ルート、データフロー、Lint を検証し、
  全コンポーネントが正しく接続されていることを確認する。

  "統合検証して", "接続確認", "wiring 実行" 等の要求でトリガーされる。

  <example>
  user: "code-analysis 機能の統合検証をして"
  assistant: "feature-wiring スキルで Export/ルート/データフロー/Lint を検証します"
  </example>
doc_contract:
  review_interval_days: 90
---

# Feature Wiring (機能統合検証スキル)

> **核心コンセプト**: "全接続ポイントの検証" - 実装後の統合完全性を保証

このスキルは機能実装後に、Export・ルート・データフロー・Lint の 4 項目を検証し、機能がアプリに正しく統合されていることを確認します。

## 検証項目

| #   | 検証                 | 対象                     | 合格基準                                 |
| --- | -------------------- | ------------------------ | ---------------------------------------- |
| 1   | **Export 検証**      | barrel file (`index.ts`) | 必要なモジュールが全て export されている |
| 2   | **ルート検証**       | Next.js App Router       | ページファイルが `src/app/` に存在する   |
| 3   | **データフロー検証** | Hook → API → Backend     | 接続チェーンが途切れていない             |
| 4   | **Lint 検証**        | プロジェクト全体         | `npm run lint` エラー 0                  |

---

## 実行フロー

```
[Start]
  |
  +-- Phase 1: 静的検証
  |     +-- 1.1 Export 検証: barrel file (index.ts) の公開 API 確認
  |     +-- 1.2 ルート検証: App Router 上のページ存在確認
  |
  +-- Phase 2: 動的検証
  |     +-- 2.1 データフロー検証: Hook → API → Backend 接続確認
  |     +-- 2.2 Lint 検証: `npm run lint` エラー 0 確認
  |     +-- 2.3 UI Flow検証: `make q.ui-flow` 通過確認
  |
  +-- Phase 3: 結果レポート
        +-- 全項目 Pass → Go 判定
        +-- 失敗あり → 修正案提示 → 修正後再検証
```

---

## Phase 1: 静的検証

### 1.1 Export 検証

対象: `src/features/<feature>/index.ts`

確認内容:

- 型定義 (types) が export されているか
- カスタムフック (hooks) が export されているか
- コンポーネント (components) が export されているか
- API 関数が必要に応じて export されているか (内部のみの場合は不要)

```bash
# barrel file の内容を確認
Read("src/features/<feature>/index.ts")

# 各サブモジュールのファイル存在確認
Glob("src/features/<feature>/**/*.ts*")
```

### 1.2 ルート検証

対象: `src/app/` 配下

確認内容:

- 機能に対応するページファイルが存在するか
- `page.tsx` が正しいパスに配置されているか
- 該当コンポーネントを import しているか

---

## Phase 2: 動的検証

### 2.1 データフロー検証

接続チェーン: `Component → Hook → API → Backend (API Route)`

確認内容:

- Component が Hook を呼び出しているか
- Hook が API 関数を呼び出しているか
- API 関数が適切なエンドポイントを参照しているか
- API Route (`src/app/api/`) が存在するか (必要な場合)

### 2.2 Lint 検証

```bash
npm run lint
```

- エラー 0 が必須
- 警告は報告するが、通過扱い

### 2.3 UI Flow検証

対象: `docs/ui-flow/ui-flow.json`

確認内容:

- 新パネルが ui-flow.json の panels に定義されているか
- 新SSEイベントが sse_mapping に登録されているか
- phases で新パネルが適切なフェーズに追加されているか
- `make q.ui-flow` で検証通過

```bash
make q.ui-flow
```

- 全12項目 Pass が必須（MVS項目は exit 1 でブロック）

---

## 失敗時の対応

各検証項目の失敗時:

| 検証         | よくある原因         | 修正アクション                     |
| ------------ | -------------------- | ---------------------------------- |
| Export       | barrel file 更新漏れ | `index.ts` に export 追加          |
| ルート       | ページファイル未作成 | `src/app/` にページ作成            |
| データフロー | import パス不一致    | barrel file 経由の import に修正   |
| Lint         | 型エラー、未使用変数 | エラー内容に従い修正               |
| UI Flow      | panels/phases未登録  | `docs/ui-flow/ui-flow.json` を更新 |

修正後は必ず **再検証** を実行します。

---

## 出力形式

### 全項目 Pass

```markdown
Feature Wiring - 検証完了

機能: <feature-id>
結果: 全項目 Pass

| #   | 検証             | 結果 |
| --- | ---------------- | ---- |
| 1   | Export 検証      | Pass |
| 2   | ルート検証       | Pass |
| 3   | データフロー検証 | Pass |
| 4   | Lint 検証        | Pass |

→ 機能の統合が正常に完了しています。
```

### 失敗あり

```markdown
Feature Wiring - 要修正

機能: <feature-id>
結果: N 件の問題を検出

| #   | 検証             | 結果 | 問題               |
| --- | ---------------- | ---- | ------------------ |
| 1   | Export 検証      | Fail | useXxx が未 export |
| 2   | ルート検証       | Pass | -                  |
| 3   | データフロー検証 | Pass | -                  |
| 4   | Lint 検証        | Fail | 2 errors           |

修正アクション:

1. src/features/<feature>/index.ts に `export { useXxx }` 追加
2. Lint エラー修正 (詳細は上記)

→ 修正後に再検証を実行します。
```

---

## 使用例

```bash
# 機能 ID で実行 (推奨)
/feature-wiring code-analysis

# feature-implementer 完了後の自動呼出 (feature-pilot 経由)
# → 手動呼出不要
```

---

## AI 行動指針

### DO (やるべきこと)

- 4 項目全てを検証してからレポート出力
- 失敗時は具体的な修正案を提示
- 修正後に再検証を実行
- barrel file (index.ts) の存在を前提として確認

### DON'T (やってはいけないこと)

- 検証項目のスキップ
- テストコード修正 (Wiring スキル範囲外)
- 不必要な新ファイル作成
- ユーザー確認なしでの破壊的変更
