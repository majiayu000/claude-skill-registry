---
user-invocable: true
description: "[デザイン] （任意）1枚ペラHTML → ページ単位の静的HTMLに分割"
---

# [デザイン] （任意）1枚ペラHTML → ページ単位の静的HTMLに分割

## 入力: $ARGUMENTS
- 分割対象のHTMLパス（例: `doc/input/design/html/mock.html`）
- 任意: 分割したいページキー（例: `HomePage Pricing Login`）

## いつ使う？（位置づけ）
- `/design-mock` で「1枚ペラHTML」を作ったあと、ページ単位に管理したいとき
- 以降の `/design-ui`（静的UI骨格生成）に渡しやすい形に整えるため

## 次に何をする？
- 分割した `doc/input/design/html/{page}.html` を根拠にSSOT（tokens/components/context）も整合させる
- 実装に進むなら `/design-ui` → `/design-components` → `/design-assemble`

---

## 🎯 目的
- 1枚ペラの静的HTMLを、**ページ単位の静的HTML**へ分割して管理しやすくする
- 以降の工程（`/design-ui` や `/design-assemble`）に渡せる形にする

---

## 共通前提（参照）
- 口調・出力規約は `CLAUDE.md` に従う。
- 判断軸は `.claude/skills/*` を適用する（例: `ui-designer` / `usability-psychologist`）。
- 詳細運用（差分/サンプル運用等）は `doc/guide/ai_guidelines.md` を参照。

---

## 出力（差分のみ）
- `doc/input/design/html/{page}.html` を複数生成/更新

---

## 分割ルール（最小）
- **入力にページキーが指定されている場合**
  - そのページキーごとに「ページの目的/主要導線/構成要素」を抽出し、`{page}.html` を生成する
- **指定がない場合**
  - 1枚ペラの主要セクションをページ候補として提案し、ユーザー確認の上で分割する

---

## ゲート
- 各ページが単独で開いて見た目が崩れない
- 主要導線がページ単位で説明できる
- ここで停止
