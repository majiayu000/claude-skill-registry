---
name: cl-macro-design
description: マクロ設計のベストプラクティスを適用。マクロ作成・レビュー時に使用
allowed-tools: Read, Grep, Glob, Bash
references:
  - @references/google-common-lisp-style-guide.md
---

# Common Lisp Macro Design

Based on Google Common Lisp Style Guide (@references/google-common-lisp-style-guide.md)

## 基本原則

### 1. マクロを使うべき場面
- 新しい制御構造の定義
- コンパイル時の計算
- ボイラープレートの削減
- DSLの構築

### 2. 関数で十分な場合
- 単純なデータ変換
- 実行時の値に依存する処理
- 高階関数で表現可能な場合

### 3. パフォーマンス目的ならINLINE宣言を使う
```lisp
;; BAD - パフォーマンスのためにマクロ化
(defmacro fast-add (a b)
  `(+ ,a ,b))

;; GOOD - inline宣言で同等の効果
(declaim (inline fast-add))
(defun fast-add (a b)
  (+ a b))
```

## 衛生的マクロ (Hygienic Macros)

### 変数捕捉の防止
```lisp
;; BAD - 変数捕捉の危険
(defmacro with-timing-bad (&body body)
  `(let ((start (get-internal-real-time)))
     ,@body
     (- (get-internal-real-time) start)))

;; GOOD - gensymで安全
(defmacro with-timing (&body body)
  (let ((start (gensym "START")))
    `(let ((,start (get-internal-real-time)))
       ,@body
       (- (get-internal-real-time) ,start))))
```

### with-gensyms ユーティリティ
```lisp
;; Alexandriaのwith-gensymsを使用
(defmacro with-retry ((var max-attempts) &body body)
  (with-gensyms (attempt result success)
    `(loop for ,attempt from 1 to ,max-attempts
           do (multiple-value-bind (,result ,success)
                  (ignore-errors ,@body)
                (when ,success
                  (return ,result)))
           finally (error "Max attempts exceeded"))))
```

## 複数評価の防止

### 問題のあるコード
```lisp
;; BAD - 引数が2回評価される
(defmacro square-bad (x)
  `(* ,x ,x))

(square-bad (incf n))  ; nが2回インクリメントされる！
```

### 正しい実装
```lisp
;; GOOD - 一度だけ評価
(defmacro square (x)
  (let ((v (gensym)))
    `(let ((,v ,x))
       (* ,v ,v))))

;; once-only ユーティリティを使用 (Alexandria)
(defmacro square (x)
  (once-only (x)
    `(* ,x ,x)))
```

## マクロ展開の検証

### 展開確認コマンド
```lisp
;; 1段階展開
(macroexpand-1 '(with-timing (heavy-computation)))

;; 完全展開
(macroexpand '(with-timing (heavy-computation)))

;; プリティプリント
(pprint (macroexpand-1 '(your-macro args)))
```

### SLIMEでの確認
```
;; Emacs/SLIME: C-c C-m (slime-expand-1)
;; カーソル位置のマクロを展開表示
```

## 構造パターン

### パターン0: CALL-WITH スタイル (Google推奨)

マクロは構文処理のみを担当し、セマンティクスは補助関数に委譲する。

```lisp
;; マクロは薄いラッパー
(defmacro with-foo (() &body body)
  `(call-with-foo (lambda () ,@body)))

;; セマンティクスは関数で実装
(defun call-with-foo (thunk)
  (setup-foo)
  (unwind-protect
      (funcall thunk)
    (teardown-foo)))
```

**利点:**
- デバッグ時にスタックトレースに関数名が現れる
- 実行時に関数を更新可能（再コンパイル不要）
- マクロの複雑さを軽減

### パターン1: with-xxx (リソース管理)
```lisp
(defmacro with-open-database ((var connection-string) &body body)
  (let ((db (gensym "DB")))
    `(let ((,db (connect-database ,connection-string)))
       (unwind-protect
           (let ((,var ,db))
             ,@body)
         (disconnect-database ,db)))))
```

### パターン2: do-xxx (イテレーション)
```lisp
(defmacro do-lines ((var stream &optional result) &body body)
  (let ((s (gensym "STREAM")))
    `(let ((,s ,stream))
       (loop for ,var = (read-line ,s nil nil)
             while ,var
             do (progn ,@body)
             finally (return ,result)))))
```

### パターン3: define-xxx (定義マクロ)
```lisp
(defmacro define-api-endpoint (name (method path) &body body)
  `(progn
     (defun ,name (request)
       ,@body)
     (register-endpoint ,method ,path #',name)
     ',name))

;; 使用
(define-api-endpoint get-users (:get "/api/users")
  (fetch-all-users))
```

### パターン4: 条件付きコンパイル
```lisp
(defmacro debug-log (format-string &rest args)
  #+debug
  `(format *debug-io* ,(concatenate 'string "[DEBUG] " format-string "~%")
           ,@args)
  #-debug
  nil)
```

## チェックリスト

### 作成前
- [ ] 本当にマクロが必要か？関数で十分ではないか？
- [ ] 類似の標準マクロはないか？

### 実装時
- [ ] すべての内部変数にgensymを使用
- [ ] 引数は一度だけ評価される
- [ ] 評価順序は直感的
- [ ] &bodyは適切な位置に配置

### 検証時
- [ ] macroexpand-1で展開を確認
- [ ] 副作用のある引数でテスト
- [ ] ネストした使用でテスト
- [ ] エッジケースでテスト

### ドキュメント
- [ ] docstringで目的を説明
- [ ] 使用例を含める
- [ ] 展開例を示す

## パラメータ設計 (Google Style Guide)

### パラメータ命名規約

評価される形式には `-form` サフィックスを付ける:

```lisp
;; 明確: condition-form は評価される式
(defmacro when-available (condition-form &body body)
  `(when ,condition-form
     ,@body))

;; 例外: body, end は慣例的なので -form 不要
```

### 拡張可能なパラメータスペース

将来の拡張に備えて空のパラメータリストを置く:

```lisp
;; BAD - 拡張が困難
(defmacro with-lights-on (&body body)
  ...)

;; GOOD - 後からオプションを追加可能
(defmacro with-lights-on (() &body body)
  ...)

;; 拡張例
(defmacro with-lights-on ((&key color intensity) &body body)
  ...)
```

### alexandria:once-only の活用

引数の複数評価を防止:

```lisp
(defmacro double (value-form)
  (alexandria:once-only (value-form)
    `(+ ,value-form ,value-form)))
```

## アンチパターン

### 1. 過度なマクロ使用
```lisp
;; BAD - 関数で十分
(defmacro add-one (x)
  `(+ ,x 1))

;; GOOD
(defun add-one (x)
  (+ x 1))
```

### 2. 巨大なマクロ
```lisp
;; BAD - マクロ内に大量のロジック
(defmacro complex-operation (...)
  `(progn
     ;; 100行のコード...
     ))

;; GOOD - ヘルパー関数に分離
(defun %complex-operation-impl (...)
  ;; 実装
  )

(defmacro complex-operation (...)
  `(%complex-operation-impl ...))
```

### 3. 不明瞭な副作用
```lisp
;; BAD - 副作用が分かりにくい
(defmacro with-user (user &body body)
  `(let ((*current-user* ,user))
     (log-user-action ,user)  ; 隠れた副作用
     ,@body))

;; GOOD - 明示的
(defmacro with-user (user &body body)
  "Bind *CURRENT-USER* and log the action."
  `(let ((*current-user* ,user))
     ,@body))

;; ログは呼び出し側で明示
(with-user user
  (log-user-action user)
  (do-something))
```

## 禁止事項 (Google Style Guide)

### 1. 新しいリーダーマクロの無許可導入禁止

```lisp
;; 禁止: プロジェクト外に露出するリーダーマクロ
(set-macro-character #\[ ...)  ; 危険

;; 許可される場合のみ: named-readtables で制御
(named-readtables:in-readtable :my-syntax)
```

### 2. 実行時のEVAL禁止

```lisp
;; 禁止: セキュリティ脆弱性
(eval (read-from-string user-input))

;; 許可: 開発ツール、ビルド基盤のみ
```

### 3. バッククォート内での複雑なロジック禁止

```lisp
;; BAD - バッククォート内でロジック
(defmacro complex (&body body)
  `(progn
     ,@(if (some-condition body)
           (transform-body body)
           body)))

;; GOOD - ロジックを外に出す
(defmacro complex (&body body)
  (let ((processed (if (some-condition body)
                       (transform-body body)
                       body)))
    `(progn ,@processed)))
```
