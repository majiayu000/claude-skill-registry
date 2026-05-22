---
name: cl-asdf-system
description: ASDFシステム定義のベストプラクティス。.asdファイル作成・編集時に使用
allowed-tools: Read, Grep, Glob
---

# ASDF System Definition

## 基本構造

### 標準的なシステム定義
```lisp
(defsystem "my-project"
  :version "0.1.0"
  :author "Your Name <your@email.com>"
  :maintainer "Your Name <your@email.com>"
  :license "MIT"
  :homepage "https://github.com/you/my-project"
  :bug-tracker "https://github.com/you/my-project/issues"
  :source-control (:git "https://github.com/you/my-project.git")
  :description "Short description of the project"
  :long-description "Longer description with more details."
  :depends-on ("alexandria"
               "cl-ppcre"
               "dexador")
  :pathname "src/"
  :serial t
  :components ((:file "package")
               (:file "conditions")
               (:file "utils")
               (:file "core")
               (:file "api"))
  :in-order-to ((test-op (test-op "my-project/tests"))))
```

### テストシステム
```lisp
(defsystem "my-project/tests"
  :description "Tests for my-project"
  :depends-on ("my-project"
               "rove")
  :pathname "tests/"
  :serial t
  :components ((:file "package")
               (:file "test-utils")
               (:file "core-tests")
               (:file "api-tests"))
  :perform (test-op (o c)
             (symbol-call :rove :run c)))
```

## ディレクトリ構成

### 推奨構造
```
my-project/
├── my-project.asd          # システム定義
├── src/
│   ├── package.lisp        # パッケージ定義
│   ├── conditions.lisp     # 条件/エラー定義
│   ├── utils.lisp          # ユーティリティ
│   ├── core.lisp           # コアロジック
│   └── api.lisp            # 公開API
├── tests/
│   ├── package.lisp        # テスト用パッケージ
│   ├── test-utils.lisp     # テストユーティリティ
│   └── core-tests.lisp     # テスト
├── docs/                   # ドキュメント
├── examples/               # 使用例
├── README.md
├── LICENSE
└── .gitignore
```

### 大規模プロジェクト
```
my-project/
├── my-project.asd
├── src/
│   ├── package.lisp
│   ├── core/
│   │   ├── types.lisp
│   │   ├── protocols.lisp
│   │   └── implementation.lisp
│   ├── http/
│   │   ├── client.lisp
│   │   └── server.lisp
│   └── db/
│       ├── connection.lisp
│       └── queries.lisp
└── tests/
    ├── package.lisp
    ├── core/
    └── http/
```

## コンポーネント指定

### :serial オプション
```lisp
;; serial t - 順番に依存
:serial t
:components ((:file "a")   ; 最初
             (:file "b")   ; aに依存
             (:file "c"))  ; a, bに依存

;; serial nil - 明示的な依存
:serial nil
:components ((:file "a")
             (:file "b" :depends-on ("a"))
             (:file "c" :depends-on ("a" "b")))
```

### モジュール
```lisp
:components
((:module "core"
  :pathname "src/core/"
  :serial t
  :components ((:file "types")
               (:file "protocols")
               (:file "impl")))
 (:module "http"
  :pathname "src/http/"
  :depends-on ("core")
  :components ((:file "client")
               (:file "server"))))
```

### 条件付きコンポーネント
```lisp
:components
((:file "package")
 (:file "core")
 ;; SBCLのみ
 #+sbcl (:file "sbcl-specific")
 ;; Unix系のみ
 #+(or linux darwin) (:file "unix-utils"))
```

## 依存関係

### 基本的な依存
```lisp
:depends-on ("alexandria"        ; ユーティリティ
             "cl-ppcre"          ; 正規表現
             "local-time"        ; 日時処理
             (:version "dexador" "0.9.0"))  ; バージョン指定
```

### フィーチャー依存
```lisp
:depends-on ("alexandria"
             (:feature :sbcl "sb-concurrency")
             (:feature (:not :windows) "osicat"))
```

### 弱い依存 (オプショナル)
```lisp
:weakly-depends-on ("swank")  ; なくても動作
```

## テスト統合

### Rove統合
```lisp
(defsystem "my-project/tests"
  :depends-on ("my-project" "rove")
  :pathname "tests/"
  :components ((:file "package")
               (:file "main"))
  :perform (test-op (o c)
             (symbol-call :rove :run c)))
```

### テスト実行
```bash
# コマンドライン
rove my-project.asd

# REPL
(asdf:test-system :my-project)
```

## ベストプラクティス

### 1. バージョニング
```lisp
;; セマンティックバージョニング
:version "1.2.3"

;; 開発版
:version "0.0.1-dev"
```

### 2. メタデータ
```lisp
;; 必須
:license "MIT"
:description "..."

;; 推奨
:author "Name <email>"
:homepage "https://..."
```

### 3. パッケージ分離
```lisp
;; Good - パッケージ定義は別ファイル
:components ((:file "package")  ; defpackageのみ
             (:file "main"))    ; 実装

;; Bad - 実装ファイル内でdefpackage
```

### 4. 循環依存の回避
```lisp
;; Good - 一方向の依存
;; core -> utils (OK)
;; utils -> core (NG: 循環)

;; 解決策: 共通部分を抽出
;; core -> common
;; utils -> common
```

## Quicklispへの登録

### 準備
1. GitHubでリポジトリ公開
2. タグでバージョン管理
3. README.mdに説明を記載

### 申請
```
https://github.com/quicklisp/quicklisp-projects/issues
```

必要情報:
- プロジェクト名
- リポジトリURL
- 簡単な説明
