---
name: cl-condition-system
description: condition/restartパターンを適用。エラーハンドリング実装時に使用
allowed-tools: Read, Grep, Glob
---

# Common Lisp Condition System

## 基本概念

Common Lispの条件システムは、エラー処理を「通知」と「回復」に分離する強力な機構です。

| 概念 | 役割 |
|------|------|
| Condition | エラーや状態を表すオブジェクト |
| Handler | 条件を検知して対応を決定 |
| Restart | 回復手段を提供 |

## 条件の定義

### 基本的な条件
```lisp
(define-condition invalid-input-error (error)
  ((input :initarg :input :reader invalid-input)
   (reason :initarg :reason :reader invalid-input-reason))
  (:report (lambda (condition stream)
             (format stream "Invalid input ~S: ~A"
                     (invalid-input condition)
                     (invalid-input-reason condition)))))
```

### 条件の階層
```lisp
;; 基底条件
(define-condition my-app-error (error)
  ((context :initarg :context :reader error-context)))

;; 特殊化
(define-condition database-error (my-app-error)
  ((query :initarg :query :reader error-query)))

(define-condition connection-error (database-error)
  ((host :initarg :host :reader error-host)))
```

### 重大度別の基底クラス
| 基底クラス | 用途 |
|------------|------|
| `error` | 回復必須のエラー |
| `warning` | 警告（処理は継続） |
| `simple-condition` | 単純な状態通知 |

## Restart の提供

### restart-case パターン
```lisp
(defun parse-config (path)
  (restart-case
      (let ((content (read-file path)))
        (if (valid-config-p content)
            (parse content)
            (error 'invalid-config-error :path path)))

    (use-default ()
      :report "Use default configuration"
      *default-config*)

    (retry-with-path (new-path)
      :report "Try a different config file"
      :interactive (lambda ()
                     (format t "Enter new path: ")
                     (list (read-line)))
      (parse-config new-path))

    (skip ()
      :report "Skip configuration loading"
      nil)))
```

### 標準リスタート
```lisp
;; abort - 処理を中止
(restart-case
    (risky-operation)
  (abort ()
    :report "Abort the operation"
    nil))

;; continue - 処理を続行
(restart-case
    (when (suspicious-p data)
      (cerror "Continue anyway" "Suspicious data detected"))
  (continue ()
    :report "Continue processing"))

;; use-value - 代替値を使用
(restart-case
    (or (get-value key) (error 'missing-key :key key))
  (use-value (value)
    :report "Use a specific value"
    :interactive (lambda () (list (read)))
    value))
```

## Handler の設定

### handler-bind
条件発生時に呼ばれるが、スタックは巻き戻されない。
```lisp
(handler-bind
    ((invalid-input-error
       (lambda (c)
         (log:warn "Invalid input: ~A" (invalid-input c))
         (invoke-restart 'use-default)))
     (warning
       (lambda (c)
         (log:info "Warning: ~A" c)
         (muffle-warning c))))
  (process-user-input input))
```

### handler-case
条件発生時にスタックを巻き戻してハンドラを実行。
```lisp
(handler-case
    (parse-and-process input)
  (invalid-input-error (c)
    (format t "Error: ~A~%" c)
    nil)
  (file-error (c)
    (format t "File error: ~A~%" c)
    (retry-with-default))
  (error (c)
    (log:error "Unexpected error: ~A" c)
    (error c)))  ; 再通知
```

### 使い分け
| 状況 | 使用 |
|------|------|
| リスタートを呼び出したい | `handler-bind` |
| 単純なエラー処理 | `handler-case` |
| ロギングのみ | `handler-bind` |
| クリーンアップ必要 | `handler-case` + `unwind-protect` |

## 実践パターン

### パターン1: リトライ機構
```lisp
(defun fetch-with-retry (url &key (max-retries 3))
  (loop for attempt from 1 to max-retries
        do (restart-case
               (return (http-get url))
             (retry ()
               :report "Retry the request"
               (log:info "Retry attempt ~D" attempt)
               (sleep (* attempt 2))))  ; バックオフ
        finally (error 'max-retries-exceeded :url url)))

;; 使用側
(handler-bind
    ((connection-error
       (lambda (c)
         (when (find-restart 'retry)
           (invoke-restart 'retry)))))
  (fetch-with-retry "https://api.example.com"))
```

### パターン2: バリデーション
```lisp
(defun validate-user (user)
  (restart-case
      (progn
        (unless (valid-email-p (user-email user))
          (error 'validation-error :field 'email))
        (unless (strong-password-p (user-password user))
          (error 'validation-error :field 'password))
        user)
    (fix-field (field value)
      :report "Fix the invalid field"
      (setf (slot-value user field) value)
      (validate-user user))))
```

### パターン3: トランザクション
```lisp
(defun with-transaction (thunk)
  (let ((tx (begin-transaction)))
    (restart-case
        (prog1 (funcall thunk tx)
          (commit tx))
      (rollback ()
        :report "Rollback transaction"
        (rollback tx)
        nil)
      (retry ()
        :report "Retry transaction"
        (rollback tx)
        (with-transaction thunk)))))
```

## デバッグ

### 利用可能なリスタートの確認
```lisp
(compute-restarts)           ; 全リスタート
(find-restart 'retry)        ; 特定リスタート
(invoke-restart-interactively 'use-value)  ; 対話的に呼び出し
```

### デバッガでの操作
```
;; SBCLデバッガ内
0: [RETRY] Retry the operation
1: [USE-DEFAULT] Use default value
2: [ABORT] Abort

;; 数字を入力してリスタートを選択
```
