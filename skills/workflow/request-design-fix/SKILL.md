---
name: request-design-fix
description: 実装フェーズ等で発覚した設計不備を修正し、整合性を回復させるためのコマンド。
---

# 設計修正リクエスト (Design Fix)

実装フェーズ等で発覚した設計不備を修正し、整合性を回復させるためのコマンド。
実装者が「勝手に直す」のではなく、「設計に戻る」プロセスを正規化します。

## 入力

$ARGUMENTS

| パラメータ | 必須 | 説明 |
|-----------|:----:|------|
| `issue` | ✅ | 関連するGitHub Issue番号 |
| `target` | ✅ | 修正対象の設計書パス |
| `problem` | ✅ | 発生している問題・不備の説明 |

---

## 全体フロー

| Phase | 名称 | 内容 |
|-------|------|------|
| 0 | 入力検証 | 設計書の存在確認、Issue番号の検証 |
| 0.5 | 影響分析 | 変更の影響範囲、関連設計書の特定 |
| 1 | 問題分析 & 方針策定 | 問題の特定、修正方針の決定 |
| 2 | 設計書修正 | ``detailed-design-writer` skill` による修正 |
| 2.5 | ユーザー承認（大規模時） | `approval-gate` skill ※3ファイル以上の場合 |
| 3 | レビューループ | ``detailed-design-reviewer` skill` によるレビュー（最大3回） |
| 4 | テスト項目書更新 | ``test-spec-writer` skill` による追従（存在する場合） |
| 5 | 完了通知 | GitHub Issueへのコメント |

> **Phase規約**: `workflow-phase-convention` skill を参照

---

## サーキットブレーカー

| 条件 | アクション |
|------|----------|
| **最大リトライ回数**: 3回 | 3回修正してもレビュー通過しない場合、現状をユーザーに報告して判断を仰ぐ |
| **スコア悪化検知** | 修正後にスコアが悪化した場合、即座に中断 |
| **大規模変更検知** | 変更が3ファイル以上に及ぶ場合、Phase 2.5でユーザーに確認 |

---

## Phase 0: 入力検証

1. 設計書パス (`target`) の存在確認
2. GitHub Issue番号の有効性確認

```bash
# 設計書の存在確認
test -f "{target}" || echo "Error: 設計書が見つかりません"

# Issue番号の確認
gh issue view {issue} --json state
```

---

## Phase 0.5: 影響分析

| チェック項目 | 確認内容 |
|-------------|---------|
| 影響ファイル数 | 修正が複数ファイルに波及するか |
| 関連設計書 | 同一機能の他設計書への影響 |
| API互換性 | 既存APIシグネチャへの影響 |

---

## Phase 1: 問題分析 & 方針策定

1. 入力された `problem` と現在の設計書を比較
2. どの部分（ロジック、データ構造、API定義など）を修正すべきか特定
3. 修正方針を決定

---

## Phase 2: 設計書修正 (``detailed-design-writer` skill`)

- 修正方針に基づき、設計書 (`.md`) を更新する
- **注意**: 既存の整合性を壊さないよう、変更は局所化する

---

## Phase 2.5: ユーザー承認ゲート（大規模変更時）

> **トリガー**: Phase 0.5で3ファイル以上の変更を検出した場合

> **共通仕様**: `approval-gate` skill を参照

```markdown
## 承認リクエスト: 大規模設計修正

**影響ファイル数**: {count}ファイル
**影響範囲**:
{affected_files_list}

---
**選択肢**:

1. 続行 → Phase 3（レビュー）へ進む
2. 中断 → 修正を中断、手動対応を推奨
3. 再分析 → 影響範囲を絞って再分析

> 番号を選択してください（1-3）:
```

---

## Phase 3: レビューループ (``detailed-design-reviewer` skill`)

| 条件 | アクション |
|------|----------|
| スコア >= 9 | Phase 4へ |
| スコア < 9 | Phase 2に戻り修正（最大3回） |
| スコア悪化 | 即時中断 |

---

## Phase 4: テスト項目書の追従 (``test-spec-writer` skill`)

- 設計変更によりテストケースに影響がある場合、テスト項目書も更新する
- テスト項目書が存在しない場合は警告を出して続行

---

## Phase 5: 完了通知

GitHub Issueに以下のフォーマットでコメントする。

```markdown
## :wrench: 設計修正完了 (Design Fix)

**修正対象**: `{target}`
**修正内容**:
[修正の概要]

**実装者へのメッセージ**:
設計書が更新されました。最新の設計書とテスト項目書をPullして、実装を再開してください。
```

---

## エラーハンドリング

| 状況 | 対処法 |
|------|--------|
| 設計書が存在しない | エラー報告、正しいパスをユーザーに確認 |
| 問題の特定が困難 | 追加情報をユーザーに要求 |
| 修正が複数設計書に波及 | 影響範囲を報告し、ユーザー承認後に実行 |
| レビュー3回失敗 | 現状の問題点をまとめて報告、手動対応を推奨 |
| テスト項目書が存在しない | 警告を出して続行（テスト更新をスキップ） |

---

## Sisyphusへの指示

このコマンドは、実装作業中の「割り込み」として機能します。
実装タスクを一時停止し、設計修正タスクを優先実行し、完了後に実装タスクへ戻るよう制御してください。

```python
def request_design_fix(issue: int, target: str, problem: str):
    """
    設計修正リクエストの実行
    
    Args:
        issue: GitHub Issue番号
        target: 修正対象の設計書パス
        problem: 問題・不備の説明
    """
    
    # 0. 入力検証
    if not file_exists(target):
        return error(f"設計書が見つかりません: {target}")
    
    # 1. 問題分析 & 方針策定
    current_design = read(target)
    analysis = analyze_problem(current_design, problem)
    
    if analysis.scope == "large":
        # 大規模変更の場合はユーザー確認
        approval = await_user_approval(f"""
大規模な変更が必要です。
影響ファイル: {analysis.affected_files}
続行しますか？
""")
        if not approval:
            return cancelled()
    
    # 2. 修正・レビューループ
    history = []
    for i in range(3):  # 最大3回リトライ
        # 設計書修正
        task(
            subagent_type="detailed-design-writer",
            description=f"設計書修正: {target}",
            prompt=f"""
## 修正対象
{target}

## 問題
{problem}

## 修正方針
{analysis.fix_plan}

## 注意
- 変更は局所化すること
- 既存の整合性を壊さないこと
"""
        )
        
        # レビュー
        review = task(
            subagent_type="detailed-design-reviewer",
            description=f"修正レビュー: {target}",
            prompt=f"修正後の{target}をレビューしてください"
        )
        
        if review.score >= 9:
            break
        
        # スコア悪化検知
        if i > 0 and review.score < history[-1]:
            return fail("スコアが悪化しました。手動対応を推奨します。")
        
        history.append(review.score)
    else:
        # 3回失敗
        return fail(f"3回の修正でレビュー通過できませんでした。最終スコア: {review.score}")
    
    # 3. テスト項目書更新（存在する場合）
    test_spec = find_test_spec(target)
    if test_spec:
        task(
            subagent_type="test-spec-writer",
            description="テスト項目書更新",
            prompt=f"設計変更に伴い{test_spec}を更新してください"
        )
    
    # 4. Issue通知
    comment_on_issue(issue, f"""
## :wrench: 設計修正完了 (Design Fix)

**修正対象**: `{target}`
**修正内容**: {analysis.summary}

**実装者へのメッセージ**:
設計書が更新されました。最新の設計書をPullして、実装を再開してください。
""")
    
    return success()
```

---

## 参考スキル

| スキル | 用途 |
|--------|------|
| `approval-gate` skill | ユーザー承認ゲート（大規模変更時） |
| `workflow-phase-convention` skill | Phase命名規約 |

---

## 関連ドキュメント

- 呼び出し元: 実装フェーズ（実装中に設計不備を検知した場合）
- 修正対象: `docs/designs/detailed/**/*.md`
- レビュー: ``detailed-design-reviewer` skill`

---

## 変更履歴

| バージョン | 変更内容 |
|-----------|---------|
| v2.0 | Phase構造に再構成、全体フロー表追加、承認ゲート追加 |
| v1.0 | 初版 |
