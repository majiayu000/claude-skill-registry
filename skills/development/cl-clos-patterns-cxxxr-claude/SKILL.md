---
name: cl-clos-patterns
description: CLOS設計パターンを適用。クラス設計・メソッド実装時に使用
allowed-tools: Read, Grep, Glob
---

# CLOS Design Patterns

## クラス定義

### 基本構造
```lisp
(defclass user ()
  ((id
    :initarg :id
    :reader user-id
    :type integer
    :documentation "Unique identifier")
   (name
    :initarg :name
    :accessor user-name
    :type string
    :documentation "Display name")
   (email
    :initarg :email
    :accessor user-email
    :type string)
   (created-at
    :initform (get-universal-time)
    :reader user-created-at
    :type integer)
   (active-p
    :initarg :active-p
    :initform t
    :accessor user-active-p
    :type boolean))
  (:documentation "Represents a user account."))
```

### スロットオプション
| オプション | 用途 |
|------------|------|
| `:initarg` | コンストラクタ引数 |
| `:initform` | デフォルト値 |
| `:reader` | 読み取り専用アクセサ |
| `:writer` | 書き込み専用アクセサ |
| `:accessor` | 読み書きアクセサ |
| `:type` | 型宣言（最適化ヒント） |
| `:allocation` | `:instance` または `:class` |
| `:documentation` | ドキュメント |

### アクセサの使い分け
```lisp
;; :reader - 変更不可のID
(id :initarg :id :reader user-id)

;; :accessor - 変更可能な属性
(name :initarg :name :accessor user-name)

;; :writer のみ - 稀なケース
(password-hash :writer (setf user-password-hash))
```

## 継承

### 単一継承
```lisp
(defclass person ()
  ((name :initarg :name :accessor person-name)))

(defclass employee (person)
  ((employee-id :initarg :employee-id :reader employee-id)
   (department :initarg :department :accessor employee-department)))
```

### 多重継承
```lisp
(defclass named-mixin ()
  ((name :initarg :name :accessor object-name)))

(defclass timestamped-mixin ()
  ((created-at :initform (get-universal-time) :reader created-at)
   (updated-at :initform (get-universal-time) :accessor updated-at)))

(defclass document (named-mixin timestamped-mixin)
  ((content :initarg :content :accessor document-content)))
```

### クラス優先順位 (CPL)
```lisp
;; C3線形化でメソッド解決順序を決定
(defclass a () ())
(defclass b (a) ())
(defclass c (a) ())
(defclass d (b c) ())  ; CPL: d -> b -> c -> a -> standard-object -> t
```

## メソッド定義

### 基本メソッド
```lisp
(defgeneric process (object)
  (:documentation "Process the given object."))

(defmethod process ((obj user))
  (format t "Processing user: ~A~%" (user-name obj)))

(defmethod process ((obj document))
  (format t "Processing document: ~A~%" (object-name obj)))
```

### メソッド組み合わせ

#### :before / :after
```lisp
;; メインメソッドの前後に実行
(defmethod process :before ((obj user))
  (log:info "Starting process for user ~A" (user-id obj)))

(defmethod process :after ((obj user))
  (log:info "Finished process for user ~A" (user-id obj)))
```

#### :around
```lisp
;; メインメソッドをラップ
(defmethod process :around ((obj user))
  (let ((start (get-internal-real-time)))
    (prog1 (call-next-method)  ; メインメソッドを呼び出し
      (log:debug "Process took ~Dms"
                 (- (get-internal-real-time) start)))))
```

#### 実行順序
```
:around (外側)
  :before (CPL順)
    primary (最も特化)
  :after (CPL逆順)
:around (内側に戻る)
```

### 特化子 (Specializer)

#### クラス特化
```lisp
(defmethod draw ((shape circle))
  ...)
```

#### EQL特化
```lisp
(defmethod handle-event ((event (eql :click)))
  (format t "Click event~%"))

(defmethod handle-event ((event (eql :keypress)))
  (format t "Keypress event~%"))
```

## 初期化プロトコル

### initialize-instance
```lisp
(defmethod initialize-instance :after ((user user) &key)
  ;; IDが未指定なら生成
  (unless (slot-boundp user 'id)
    (setf (slot-value user 'id) (generate-id)))
  ;; バリデーション
  (unless (valid-email-p (user-email user))
    (error "Invalid email: ~A" (user-email user))))
```

### make-instance のカスタマイズ
```lisp
;; ファクトリ関数を提供
(defun make-user (name email &key (active-p t))
  "Create a new user with validation."
  (make-instance 'user
                 :name name
                 :email email
                 :active-p active-p))
```

### reinitialize-instance
```lisp
(defmethod reinitialize-instance :after ((user user) &key)
  (setf (updated-at user) (get-universal-time)))

;; 使用
(reinitialize-instance user :name "New Name")
```

## 設計パターン

### パターン1: プロトコル (Interface)
```lisp
;; 抽象プロトコル
(defgeneric serialize (object stream)
  (:documentation "Serialize object to stream."))

(defgeneric deserialize (class stream)
  (:documentation "Deserialize object from stream."))

;; 実装
(defmethod serialize ((user user) stream)
  (format stream "~A:~A:~A"
          (user-id user)
          (user-name user)
          (user-email user)))
```

### パターン2: Mixin
```lisp
(defclass validatable-mixin ()
  ())

(defgeneric validate (object)
  (:method-combination progn))

(defmethod validate progn ((obj validatable-mixin))
  ;; 基本バリデーション
  t)

(defclass user (validatable-mixin)
  (...))

(defmethod validate progn ((user user))
  (assert (valid-email-p (user-email user))))
```

### パターン3: ビジター
```lisp
(defgeneric visit (visitor object)
  (:documentation "Visit object with visitor."))

(defclass print-visitor () ())

(defmethod visit ((v print-visitor) (u user))
  (format t "User: ~A~%" (user-name u)))

(defmethod visit ((v print-visitor) (d document))
  (format t "Document: ~A~%" (object-name d)))
```

### パターン4: シングルトン
```lisp
(defclass configuration ()
  ((instance :allocation :class :initform nil)))

(defun get-configuration ()
  (or (slot-value (find-class 'configuration) 'instance)
      (setf (slot-value (find-class 'configuration) 'instance)
            (make-instance 'configuration))))
```

## ベストプラクティス

### 1. defgeneric を明示
```lisp
;; Good - 明示的なジェネリック定義
(defgeneric process (object)
  (:documentation "Process the object."))

(defmethod process ((obj user))
  ...)

;; Bad - 暗黙的なジェネリック
(defmethod process ((obj user))
  ...)
```

### 2. 適切なアクセサ選択
```lisp
;; 変更不可 -> :reader
;; 変更可能 -> :accessor
;; 内部使用 -> アクセサなし
```

### 3. スロットの直接アクセスを避ける
```lisp
;; Good - アクセサ経由
(user-name user)

;; Bad - 直接アクセス（テストやデバッグ以外）
(slot-value user 'name)
```
