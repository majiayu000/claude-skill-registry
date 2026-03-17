---
name: fix-issue
description: GitHub Issueを自動解決するワークフロー。Working Documents読み込み→Issue説明→計画→実装→動作確認→要件確認→検証→独立レビュー→Steering更新→PR作成・自動マージまで。Issue番号を引数に取る。「/fix-issue 123」のように使用。トピックブランチ必須、main直接コミット禁止。
---

# Issue自動解決スキル

## ワークフロー概要

```
Working読込 → Issue確認 → 説明 → 計画 → 実装 → 動作確認 → 要件確認 → 検証 → PR作成・レビュー → Steering更新 → 自動マージ → マージ待機 → クリーンアップ
                          🔹①     🔹②                       🔹③
```

🔹 = ユーザー確認ポイント（AskUserQuestionで確認後に次へ進む）
確認ポイントは3つ（Issue説明、計画、要件確認）

---

## Phase 1: Working Documents読み込み

**Working Documentsが存在する場合は読み込み、存在しない場合は生成を促します。**

### 1.1 Working Documents検索

```bash
# Issue番号でディレクトリを検索
ls docs/working/*_${ISSUE_NUMBER}_*/
```

### 1.2 存在する場合

以下のファイルを読み込み、コンテキストを復元:

```
docs/working/{YYYYMMDD}_{Issue番号}_{タイトル}/
├── requirement.md  # 要件定義 → 何を実装するか
├── tasklist.md     # タスクリスト → 作業の進め方
├── design.md       # 設計書 → どこを修正するか
└── testing.md      # テスト計画 → どうテストするか
```

⚠️ **Working Documentsがあれば、コード探索は不要。設計書に必要な情報が記載されている。**

### 1.3 存在しない場合

```
⚠️ Working Documents が見つかりません。

以下のいずれかを選択してください:
1. 今ここで Working Documents を生成する（推奨）
2. Working なしで続行（探索フェーズを実行）
```

**選択肢1の場合**: Phase 1.4（Working生成）を実行
**選択肢2の場合**: Phase 1.5（コード探索）を実行

---

## Phase 1.4: Working Documents生成（既存Issue用）

**Working Documentsがない既存Issueに対して、その場で生成します。**

### 手順

1. **Issue本文を読み込み**（Phase 2で取得済み）
2. **Serena MCPで関連コード調査**
   ```
   search_for_pattern → get_symbols_overview → find_symbol → find_referencing_symbols
   ```
3. **Working Documents生成**
   - `docs/working/{YYYYMMDD}_{Issue番号}_{タイトル}/` を作成
   - requirement.md, tasklist.md, design.md, testing.md を生成
   - タスクタイプに応じて生成内容を調整

4. **ユーザー確認**
   - 生成されたWorking Documentsを提示
   - 修正があれば対応
   - OKならPhase 3（説明）へ

---

## Phase 1.5: コード探索（Working Documentsがない場合のみ）

⚠️ **通常はスキップ。Working Documentsがない緊急時のみ実行。**

Serena MCPで関連コードを探索:

```
search_for_pattern → get_symbols_overview → find_symbol → find_referencing_symbols
```

---

## Phase 2: Issue確認

```bash
gh issue view $ARGUMENTS --json title,body,labels,number,assignees
```

Working Documentsと照合し、要件を確認。

---

## Phase 3: Issue説明 🔹確認ポイント①

**エンジニア初心者向けに**以下を説明します:

1. **問題の背景** - なぜこのIssueが作られたのか
2. **解決したいこと** - 何を実現したいのか
3. **根本原因** - 技術的に何が起きているのか
4. **修正の方針** - どのように直すのか
5. **懸念点・リスク** - 考慮すべき影響や可能性

**説明スタイル:**
- 技術用語は使用OK（ただし初出の用語は簡潔に補足説明する）
- ⚠️ **コードは提示しない**（ファイル名や関数名は記載OK）
- 図解やダイアグラムを活用
- 具体例を用いる

**説明後、ユーザーの意見を確認して修正可能か判断を仰ぐ。**

---

## Phase 4: 計画 🔹確認ポイント②

**Working Documentsのtasklist.mdを確認し、実装計画をユーザーに提示して承認を得る。**

### tasklist.mdがある場合

- tasklist.mdのフェーズ・タスクに沿った計画を提示
- 複雑な実装のみEnterPlanModeで詳細化

### tasklist.mdがない/不十分な場合

- EnterPlanModeで実装計画を立案
- 「think hard」で計画を検討
- 計画承認後、次のフェーズへ

⚠️ **必ずユーザーの承認を得てから実装に進む。毎回省略不可。**

---

## リファレンスドキュメント

詳細な実装パターンと過去事例は以下を参照:

- **[error-patterns.md](references/error-patterns.md)** - よくあるエラーパターンの原因・解決方法・予防策
- **[issue-resolution-history.md](references/issue-resolution-history.md)** - 過去に解決したIssueの詳細記録

---

## Phase 5: 実装

### ブランチ作成(必須)

⚠️ **mainブランチへの直接コミット禁止**

```bash
# Issueラベルに応じたブランチ名
git checkout -b fix/#番号-説明    # bug/bugfixラベル
git checkout -b feat/#番号-説明   # enhancement/featureラベル
git checkout -b test/#番号-説明   # testingラベル
```

### Context7 MCPでドキュメント確認

実装前に必ず最新ドキュメントを参照:

```
resolve-library-id → query-docs
```

### 実装実行（TDD必須）

**コード変更を含む実装は、TDDスキル（`.claude/skills/tdd/SKILL.md`）のRed→Green→Refactorサイクルに従う。**

#### TDD対象の場合（lib/, hooks/, components/のロジック, バグ修正）

```
1. testing.md を読み込み → テスト設計のインプット
2. 🔴 Red: 失敗テストを作成 → コミット
3. 🟢 Green: テスト合格する最小実装 → コミット
4. 🔵 Refactor: テスト維持したまま改善 → コミット（必要な場合のみ）
```

⚠️ **テストなしの実装コミットは行わない。必ずテストを先に書く。**

#### TDD対象外の場合（docs/, chore, ビジュアル調整のみ）

Claude Code標準ツール(Edit/Write)でそのまま実装。

#### 共通

**⚠️ tasklist.mdを逐次更新**: 完了したタスクは `[x]` に変更。

---

## Phase 6: 動作確認（選択式）

**実装が完了したら、まず動作を確認します。ユーザーが実際の画面を見てから要件確認に進みます。**

AskUserQuestionで以下を提示:

1. **自動確認（推奨）** - Chrome DevTools MCPでスクリーンショット・スナップショットを取得してユーザーと一緒に確認
2. **手動確認** - ユーザーが自分でブラウザで確認（`npm run dev` を案内）
3. **スキップ** - 動作確認を省略（テストで十分と判断した場合）

**自動確認の場合**: スクリーンショットをユーザーに提示し、問題がないか確認する。

---

## Phase 7: 要件確認 🔹確認ポイント③（ループ型・検証なし）

**動作確認の結果を踏まえて、ユーザーに要件の充足を確認します。ユーザーの承認が得られるまでループします。**

### 確認内容

1. **実装した変更の概要** - どのファイルに何を追加/修正したか（コードなし）
2. **Issueの要件との対応** - 各要件をどのように満たしたか
3. **動作確認の結果** - Phase 6で確認した内容のまとめ

### フローチャート

```
動作確認完了 → ユーザーに報告
                    ↓
             ユーザー承認？
              ├── ✅ OK → Phase 8（検証）へ
              └── ❌ 追加修正が必要
                    ↓
             追加の指示を受ける
                    ↓
             修正を実施 → 必要に応じて動作再確認
                    ↓
             再度ユーザーに報告（ループ）
```

### ⚠️ 重要ルール

- **このフェーズでは `npm run lint` / `npm run build` / `npm run test` を実行しない**
- 追加修正は実装のみに集中し、検証はPhase 8でまとめて1回だけ実行する
- ユーザーの承認なしに検証フェーズへ進まないこと

---

## Phase 8: 検証（自動実行）

**ユーザーの操作なしで自動実行します。**

```bash
npm run lint && npm run build && npm run test
```

- Lintエラーは完全解消するまでループ
- ビルド・テストが通るまで修正を繰り返す
- 自動で完了する（ユーザーへの確認不要）

---

## Phase 9: コミット・PR作成・コードレビュー

**実装をコミットしてPRを作成し、code-reviewプラグインで独立レビューを実行します。**

### 手順

1. **コミット・プッシュ**

   まず `git status` で全ての未コミット変更を確認する。

   **① 実装外の変更がある場合（chore コミットを先に作成）**
   ```bash
   # スキル更新、.gitignore、CLAUDE.md、docs等の実装外変更を先にコミット
   git add <実装外の変更ファイル>
   git commit -m "chore(#<Issue番号>): <説明>"
   ```

   対象例: `.claude/skills/`, `.gitignore`, `CLAUDE.md`, `docs/steering/`, `docs/working/`

   **② 実装コミット**
   ```bash
   git add <実装の変更ファイル>
   git commit -m "<type>(#<Issue番号>): <説明>"
   git push -u origin $(git branch --show-current)
   ```

   ⚠️ **両方のコミットを同じPR（同じブランチ）に含める。別ブランチは不要。**

2. **PR作成**
   ```bash
   # ⚠️ 一時ファイルはリポジトリルートに相対パスで作成（Windows互換）
   # /tmp/ はWindowsで正しく解決されないため使用禁止
   cat > .tmp-pr-body.md <<'PREOF'
   ## 概要
   Issue #番号 を解決。

   ## 変更内容
   - 変更点1
   - 変更点2

   ## テスト
   - [x] lint / build / test 通過
   - [ ] コードレビュー（code-reviewプラグイン）
   - [ ] 実機動作確認

   Closes #番号
   PREOF

   gh pr create --base main --title "<type>(#<Issue番号>): <タイトル>" --body-file .tmp-pr-body.md

   # 一時ファイルを必ず削除
   rm -f .tmp-pr-body.md
   ```

3. **コードレビュー（選択式）**

   AskUserQuestionで以下を提示:

   1. **フルレビュー** - code-reviewプラグインで5並列エージェントによる多角的レビュー（大規模変更・重要機能向け）
   2. **スキップ** - コードレビューを省略（小規模リファクタリング・CSS変更等）

   **フルレビューを選択した場合:**
   - Skillツールで `code-review:code-review` を呼び出し
   - 信頼度スコア80以上の問題のみPRにコメント投稿

4. **レビュー結果の処理**
   - **問題なし / スキップ** → Phase 10（Steering更新）へ
   - **問題あり** → 修正 → コミット → プッシュ → 再度code-reviewを実行（ループ）

⚠️ **レビューで指摘された問題は、修正するか技術的根拠をもって反論すること。盲従は不要。**

---

## Phase 10: Steering Documents更新

**PR作成前に、Steering Documentsの更新が必要か判断します。**

### 更新対象の判定

以下のいずれかに該当する場合、Steering更新が必要:
- 新機能追加（FEATURES.md 更新）
- 技術スタック変更（TECH_SPEC.md 更新）
- 新しいドメイン用語追加（UBIQUITOUS_LANGUAGE.md 更新）
- 実装パターン変更（GUIDELINES.md 更新）

### 更新ドラフト生成

Working Documents（特に design.md）を参照し、更新ドラフトを生成。

**ユーザーに提示し、承認後に更新します。**

⚠️ **ユーザーの最終確認なしに Steering Documents を更新しないこと。**

---

## Phase 11: 最終更新・自動マージ・クリーンアップ（全自動）

**ユーザーの確認なしで自動実行します。PR作成・レビューはPhase 9で完了済み。**
**このフェーズではマージ待機→クリーンアップまで一気通貫で実行します。**

### 1. Working Documents最終更新

tasklist.mdを完了状態に更新:

```markdown
**ステータス**: ✅ 完了
**完了日**: YYYY-MM-DD
```

### 2. Steering/Working更新のコミット・プッシュ（Phase 10で更新があった場合）

```bash
git add docs/
git commit -m "docs(#<Issue番号>): Steering/Working Documents更新"
git push
```

### 3. 自動マージ設定

```bash
gh pr merge --auto --merge
```

### 4. マージ待機・クリーンアップ

**自動マージ設定後、マージ完了をポーリングで待機し、完了次第ブランチクリーンアップを実行する。**

```bash
# PR番号とブランチ名を変数に保持
PR_NUMBER=<PR番号>
BRANCH_NAME=$(git branch --show-current)

# マージ完了までポーリング（30秒間隔、最大10分）
for i in $(seq 1 20); do
  STATE=$(gh pr view $PR_NUMBER --json state --jq '.state')
  if [ "$STATE" = "MERGED" ]; then
    echo "✅ PR #$PR_NUMBER がマージされました"
    break
  fi
  echo "⏳ マージ待機中... ($i/20)"
  sleep 30
done

# マージ確認
STATE=$(gh pr view $PR_NUMBER --json state --jq '.state')
if [ "$STATE" = "MERGED" ]; then
  # mainに切り替え & 最新を取得
  git switch main && git fetch origin && git pull origin main

  # ローカルブランチ削除
  git branch -d "$BRANCH_NAME"

  # リモートブランチ削除（GitHub自動削除設定の場合はスキップ）
  git push origin --delete "$BRANCH_NAME" 2>/dev/null || true

  echo "🧹 ブランチクリーンアップ完了"
else
  echo "⚠️ マージがまだ完了していません（state: $STATE）"
  echo "手動で確認してください: gh pr view $PR_NUMBER"
fi
```

⚠️ **ポーリングは最大10分。タイムアウトした場合はユーザーに状況を報告する。**
⚠️ **リモートブランチがGitHub側で自動削除設定の場合は `git push origin --delete` は不要（エラーを無視する）。**

---

## 完了

```
✅ Issue #番号 を解決しました

📋 実施内容:
- [変更の概要]

🔀 PR: #番号 → マージ完了 ✅
🧹 ブランチクリーンアップ完了

📝 Steering Documents:
- [更新した場合] FEATURES.md を更新しました
- [更新しなかった場合] 更新不要と判断しました
```
