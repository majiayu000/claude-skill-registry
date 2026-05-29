---
name: fix-mermaid
description: Mermaid修正エージェント - Mermaid図のシンタックスエラーを検出・修正。/fix-mermaid [対象パス] で呼び出し。
user_invocable: true
---

# Mermaid Format Fixer Agent

Mermaid図のシンタックスエラーを検出し、修正するエージェントです。

## 概要

このエージェントは、マークダウンファイル内のMermaid図を検証し、一般的なシンタックスエラーを自動修正します。

## よくあるMermaidエラーと修正方法

### 1. 日本語テキストの問題

**問題**: ノード内の日本語テキストにスペースや特殊文字が含まれる

```mermaid
# NG
graph TD
    A[監査セット 作成]

# OK - 引用符で囲む
graph TD
    A["監査セット作成"]
```

### 2. HTMLタグ風の改行

**問題**: `<br/>` がエスケープされていない

```mermaid
# NG
graph TD
    A[複数行<br/>テキスト]

# OK - 引用符で囲む
graph TD
    A["複数行<br/>テキスト"]
```

### 3. サブグラフ名の問題

**問題**: サブグラフ名にスペースや日本語

```mermaid
# NG
subgraph Phase 1
    A[Node]
end

# OK - 引用符で囲む
subgraph "Phase 1"
    A[Node]
end
```

### 4. エッジラベルの問題

**問題**: エッジラベルに特殊文字

```mermaid
# NG
A -->|Customer-Supplier| B

# OK - 引用符で囲む
A -->|"Customer-Supplier"| B
```

### 5. ノードIDの問題

**問題**: ノードIDに特殊文字や数字のみ

```mermaid
# NG
graph TD
    1[First]

# OK - 英字プレフィックス
graph TD
    N1[First]
```

### 6. sequenceDiagramの参加者名

**問題**: 参加者名にスペースや特殊文字

```mermaid
# NG
sequenceDiagram
    participant API Gateway

# OK - エイリアス使用
sequenceDiagram
    participant G as API Gateway
```

### 7. sequenceDiagramの予約語

**問題**: Mermaidの予約語がparticipant名に使用されている

```mermaid
# NG - BOXは予約語
sequenceDiagram
    participant BOX as BOX Platform

# OK - 予約語を避ける
sequenceDiagram
    participant BoxAPI as BOX Platform
```

**予約語リスト:**
| 予約語 | 説明 | 代替案 |
|-------|------|-------|
| `BOX`, `box` | グループ化構文 | `BoxAPI`, `BoxPlatform` |
| `loop`, `alt`, `opt`, `par` | 制御構文 | プレフィックスを付ける |
| `Note`, `note` | 注釈構文 | `NoteService` など |
| `activate`, `deactivate` | アクティベーション | プレフィックスを付ける |

### 8. クラス図のクラス名

**問題**: クラス名に特殊文字やスペース

```mermaid
# NG
classDiagram
    class User-Account

# OK - アンダースコア使用
classDiagram
    class User_Account
```

## 実行プロンプト

あなたはMermaid図のシンタックスエラーを修正する専門家です。以下の手順で修正を実行してください。

### Step 1: ファイルの検索

```
# Mermaidを含むマークダウンファイルを検索
Grep: "```mermaid" --glob="*.md"
```

### Step 2: エラーパターンの検出

各ファイルで以下のパターンを検出:

1. **サブグラフ名の問題**
   - `subgraph [^"].*[空白|日本語]` → 引用符で囲む

2. **HTMLタグの問題**
   - `\[.*<br/>.*\]` で引用符なし → 引用符で囲む

3. **エッジラベルの問題**
   - `-->|.*-.*|` で引用符なし → 引用符で囲む

4. **ノードラベルの問題**
   - `\[.*[日本語].*\]` で複雑な内容 → 引用符で囲む

5. **予約語の問題（sequenceDiagram）**
   - `participant BOX` → `participant BoxAPI as BOX`
   - `participant loop` → `participant LoopService as loop`

6. **クラス名の問題（classDiagram）**
   - `class Foo-Bar` → `class Foo_Bar`

### Step 3: 修正の適用

Editツールを使用して修正:

```
# 例: サブグラフ名の修正
old: subgraph Phase 1
new: subgraph "Phase 1"

# 例: HTMLタグを含むノードの修正
old: A[Text<br/>More]
new: A["Text<br/>More"]
```

### Step 4: 検証

修正後、構文が正しいことを確認:
- 各ブロックの開始と終了が対応
- ノードIDが有効
- 矢印の構文が正しい

## 修正チェックリスト

- [ ] サブグラフ名が引用符で囲まれている
- [ ] `<br/>`を含むノードが引用符で囲まれている
- [ ] 日本語を含む複雑なノードラベルが引用符で囲まれている
- [ ] エッジラベルの特殊文字が引用符で囲まれている
- [ ] 参加者名にスペースがある場合はエイリアス使用
- [ ] ノードIDが英字で始まっている
- [ ] sequenceDiagramで予約語（BOX, loop, alt, opt, par, Note, activate, deactivate）が参加者名に使われていない
- [ ] classDiagramでクラス名にハイフンが使われていない

## 出力

修正完了後、以下を報告:
- 修正したファイル数
- 修正したエラー数
- 修正内容のサマリー
