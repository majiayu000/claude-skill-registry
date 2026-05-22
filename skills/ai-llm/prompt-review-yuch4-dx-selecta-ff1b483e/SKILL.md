---
name: prompt-review
description: .github/prompts/*.prompt.md をレビューして改善提案を出す。frontmatterの妥当性、入力変数(${input:...})の設計、出力フォーマット固定、instructions/skillsへの参照（重複排除）、tools最小化、例の有無、命名規則、壊れやすい指示の検出を行い、レポートをdocs/prompt-review-report.mdに出力する。
---

# Prompt Review Skill

## When to use
- 新しい prompt file を追加/変更した直後
- /コマンドの出力が毎回ブレる、長すぎる、使いづらいと感じたとき
- prompt が増えてきて整理したいとき（重複・命名の整合を取りたい）

## Inputs
- 対象パス（例: `.github/prompts/bootstrap-docs.prompt.md`）
- もしくは `.github/prompts/` 全体

## Output（固定フォーマット）
`docs/prompt-review-report.md` を作成/更新し、以下の構成で出す:

1. Summary（全体所見 + P0/P1/P2件数）
2. Prompt-by-prompt findings（各promptごと）
   - P0: 壊れる/呼べない/誤動作しうる
   - P1: 使いにくい/ブレやすい
   - P2: 改善余地（読みやすさ/保守性）
3. Recommended edits（具体的修正案。必要なら差分形式）

## Review checklist（必須観点）
### A. Frontmatter & naming
- name がユニークで、短く、用途が想像できる
- description が「何をする / いつ使う」を言い切っている
- argument-hint が実際の入力に合っている（例が有効）
- agent/tools が適切（過剰権限でない）
  - prompt files はMarkdownでワークフローを定義する想定なので、frontmatterの整備が重要

### B. Reusability (variables)
- `${input:...}` を最低2つ以上使い、再利用可能
- 入力が曖昧なら「期待値」や「選択肢」を input の説明に入れる
- 変数名が一貫（product, feature, scope など）

### C. Output stability
- 出力フォーマットが固定（章立て/表/チェックリスト）
- “成功時/失敗時の出力” が明示されている

### D. Duplication control
- ルール/規約は instructions / skills に寄せ、promptにコピペしない
- 参照先（docs/ や skills）をリンクで示す（重複排除）

### E. Tooling & safety
- tools は最小限（read/search中心、edit/executeは必要時のみ）
- 破壊的操作や外部送信をしない（必要なら明示し承認ゲートを設ける）
- “自動実行/停止/承認待ち”の制御が明確（あなたのフローだと特に重要）

## Procedure
1) `.github/prompts` を列挙し、対象promptを特定
2) 各promptを読み、A〜Eで評価
3) 可能なら `scripts/validate_prompts.py` を実行し、機械チェック結果も取り込む
4) `docs/prompt-review-report.md` を更新して提示
5) ユーザーが「修正して」と言った場合のみ、該当promptを直す（勝手に改変しない）
