---
name: cl-coding-style
description: Common Lispのコーディング規約を適用。Lispコード作成・レビュー時に使用
allowed-tools: Read, Grep, Glob
references:
  - @references/google-common-lisp-style-guide.md
---

# Common Lisp Coding Style

Based on Google Common Lisp Style Guide (@references/google-common-lisp-style-guide.md)

## 命名規則

### 関数・変数
- **通常の名前**: `kebab-case` (例: `find-user-by-id`, `parse-json-string`)
- **述語関数**: `-p` サフィックス (例: `valid-user-p`, `empty-list-p`)
- **変換関数**: `foo->bar` 形式 (例: `string->symbol`, `list->vector`)

### 特殊変数
- **動的変数**: `*earmuffs*` (例: `*default-timeout*`, `*current-connection*`)
- **定数**: `+plus-signs+` (例: `+max-retries+`, `+default-buffer-size+`)

### クラス・条件
- **クラス名**: `kebab-case` (例: `user-account`, `http-request`)
- **条件型**: `-error`, `-warning` サフィックス (例: `invalid-input-error`)

### アクセサ
- **リーダー**: `class-slot` (例: `user-name`, `request-method`)
- **ライター**: `(setf class-slot)` 形式
- **アクセサ**: 両方を提供する場合

## インデント

- **基本**: 2スペースインデント
- **タブ禁止**: スペースのみ使用
- **Emacsスタイル**: 標準的なLispインデントに従う

```lisp
;; Good
(defun process-items (items)
  (loop for item in items
        when (valid-p item)
          collect (transform item)))

;; Bad - インデント不正
(defun process-items (items)
(loop for item in items
when (valid-p item)
collect (transform item)))
```

## パッケージ参照

### シンボル形式
- **推奨**: `#:` 形式 (uninterned symbol)
- **許容**: キーワード形式 `:symbol`
- **非推奨**: 文字列形式 `"SYMBOL"`

```lisp
;; Good
(defpackage #:my-project
  (:use #:cl)
  (:import-from #:alexandria
                #:if-let
                #:when-let)
  (:export #:main
           #:run))

;; Acceptable
(defpackage :my-project
  (:use :cl)
  (:export :main))

;; Bad - 文字列形式
(defpackage "MY-PROJECT"
  (:use "CL"))
```

### import-from vs use
- **:import-from**: 明示的なシンボル指定（推奨）
- **:use**: パッケージ全体の取り込み（CLのみ推奨）

## フォーマット

### 行長
- **推奨**: 100文字以内
- **最大**: 120文字

### 空行
- **関数間**: 1行
- **セクション間**: 2行まで
- **連続空行**: 最大2行

### 括弧
- **閉じ括弧**: 同一行に連続配置
- **開き括弧後の改行**: 必要な場合のみ

```lisp
;; Good - 閉じ括弧は連続
(defun foo ()
  (let ((x 1)
        (y 2))
    (+ x y)))

;; Bad - 閉じ括弧が分離
(defun foo ()
  (let ((x 1)
        (y 2))
    (+ x y)
  )
)
```

## ドキュメント

### Docstring
- **関数**: 目的と引数を説明
- **変数**: 用途を説明
- **クラス**: 役割を説明

```lisp
(defun find-user (id &key (include-deleted nil))
  "Find a user by ID.

   Arguments:
     ID - The user's unique identifier
     INCLUDE-DELETED - If true, include soft-deleted users

   Returns:
     USER object or NIL if not found"
  ...)

(defvar *connection-pool*
  "Pool of database connections for reuse.")
```

## 制御構造

### when/unless vs if
- **when**: else節なしの場合
- **unless**: 否定条件の場合
- **if**: 両方の分岐がある場合

```lisp
;; Good
(when (valid-p x)
  (process x))

(unless (empty-p list)
  (first list))

(if (ready-p)
    (start)
    (wait))

;; Bad - ifをwhenで書くべき
(if (valid-p x)
    (process x)
    nil)
```

### cond vs if
- **cond**: 3つ以上の分岐
- **if**: 2分岐

```lisp
;; Good - condを使用
(cond
  ((< n 0) 'negative)
  ((= n 0) 'zero)
  (t 'positive))

;; Bad - ネストしたif
(if (< n 0)
    'negative
    (if (= n 0)
        'zero
        'positive))
```
