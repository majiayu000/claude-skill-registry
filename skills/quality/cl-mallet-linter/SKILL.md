---
name: cl-mallet-linter
description: malletリンターのルールと設定を適用。コードレビュー・品質チェック時に使用
allowed-tools: Read, Grep, Glob, Bash
---

# Mallet Linter Guide

Malletは、スタイルの強制ではなく実際の間違いを捉えることに特化したCommon Lispリンターです。

## 基本コマンド

```bash
# ファイル/ディレクトリをリント
mallet src/

# 全ルール有効化
mallet -a src/
mallet --all src/

# 自動修正（ドライラン）
mallet --fix-dry-run src/

# 自動修正実行
mallet --fix src/

# 出力形式指定
mallet --format json src/
mallet --format line src/   # GCC形式
```

## 重大度レベル

| レベル | 説明 | 例 |
|--------|------|-----|
| **error** | 確実に間違い | `wrong-otherwise` |
| **warning** | バグの可能性 | `unused-variables`, `missing-otherwise` |
| **convention** | イディオム推奨 | `if-without-else`, `special-variable-naming` |
| **format** | フォーマット | `trailing-whitespace`, `no-tabs` |
| **info** | スタイル選択 | `line-length`, `constant-naming` |
| **metrics** | 品質測定 | `cyclomatic-complexity`, `function-length` |

## 主要ルール

### Error（エラー）
| ルール | 説明 |
|--------|------|
| `wrong-otherwise` | ecase/etypecaseでotherwise/tを使用 |

### Warning（警告）
| ルール | 説明 |
|--------|------|
| `unused-variables` | 未使用変数 |
| `unused-local-functions` | 未使用ローカル関数 |
| `missing-otherwise` | case/typecaseにotherwise句がない |
| `mixed-optional-and-key` | &optionalと&keyの混在 |

### Convention（慣例）
| ルール | 説明 |
|--------|------|
| `if-without-else` | else節なしのif → when/unless推奨 |
| `bare-progn-in-if` | ifでprogn → cond推奨 |
| `interned-package-symbol` | パッケージで#:形式推奨 |
| `special-variable-naming` | 特殊変数は*name*形式 |
| `asdf-component-strings` | ASDFコンポーネントに文字列使用 |

### Format（フォーマット）
| ルール | 説明 |
|--------|------|
| `no-tabs` | タブ禁止 |
| `trailing-whitespace` | 行末空白 |
| `final-newline` | ファイル末尾改行 |

### Info（情報）
| ルール | 説明 | デフォルト |
|--------|------|------------|
| `line-length` | 最大行長 | 100 |
| `consecutive-blank-lines` | 連続空行 | 2 |
| `unused-local-nicknames` | 未使用ニックネーム | - |
| `unused-imported-symbols` | 未使用インポート | - |
| `constant-naming` | 定数は+name+形式 | - |
| `needless-let*` | 不要なlet* | - |

### Metrics（メトリクス）
| ルール | 説明 | デフォルト |
|--------|------|------------|
| `cyclomatic-complexity` | 循環複雑度 | 20 |
| `function-length` | 関数行数 | 50 |

## 設定ファイル (.mallet.lisp)

```lisp
(:mallet-config
 ;; ベース設定
 (:extends :default)  ; :default, :all, :none

 ;; 無視パス
 (:ignore "vendor/**/*.lisp"
          "**/generated/*.lisp"
          "examples/**/*.lisp")

 ;; ルール有効化（オプション付き）
 (:enable :line-length :max 100)
 (:enable :cyclomatic-complexity :max 15)
 (:enable :function-length :max 40)
 (:enable :consecutive-blank-lines :max 2)
 (:enable :constant-naming)

 ;; ルール無効化
 (:disable :if-without-else)

 ;; パス固有設定
 (:for-paths ("tests")
   (:enable :line-length :max 120)
   (:disable :unused-variables))

 (:for-paths ("scripts" "examples")
   (:disable :line-length)
   (:disable :trailing-whitespace)))
```

## CLIオプション

```bash
# プリセット
--preset default    # 推奨ルールのみ
--preset all        # 全ルール
--preset none       # ルールなし

# ルール制御
--enable rule-name
--enable rule-name:opt=value
--disable rule-name
--enable-group metrics
--disable-group info

# 出力
--format text       # デフォルト
--format line       # GCC形式（エディタ統合用）
--format json       # プログラム処理用

# 修正
--fix               # 自動修正
--fix-dry-run       # 修正プレビュー

# その他
--config path       # 設定ファイル指定
--debug             # デバッグモード
```

## 自動修正可能なルール

以下のルールは `--fix` で自動修正可能:

- `trailing-whitespace` - 行末空白を削除
- `final-newline` - ファイル末尾に改行追加
- `consecutive-blank-lines` - 過度な空行を削除
- `unused-local-nicknames` - 未使用ニックネームを削除
- `unused-imported-symbols` - 未使用インポートを削除

## ソースコード内での抑制

```lisp
;; 次のフォームを抑制
#+mallet
(declaim (mallet:suppress-next :if-without-else))
(defun foo () (if x (print "yes")))

;; 領域を抑制
#+mallet
(declaim (mallet:disable :line-length))
;; ... 長い行のコード ...
#+mallet
(declaim (mallet:enable :line-length))

;; スコープ内で抑制
(defun foo ()
  #+mallet
  (declare (mallet:suppress :unused-variables))
  (let ((unused 1))
    (do-something)))

;; 全ルール抑制
#+mallet
(declaim (mallet:suppress-next :all))
(defun generated-code () ...)
```

## 終了コード

| コード | 意味 |
|--------|------|
| 0 | 問題なし |
| 1 | 警告あり |
| 2 | エラーあり |
| 3 | 実行エラー |

## 推奨ワークフロー

### 開発中
```bash
# デフォルトルールでチェック
mallet src/

# 問題を確認して修正
mallet --fix-dry-run src/
mallet --fix src/
```

### PR前
```bash
# 全ルールでチェック
mallet -a src/

# メトリクス確認
mallet --enable-group metrics src/
```

### CI/CD
```bash
# 厳格チェック（エラーで失敗）
mallet --format line src/ && echo "Lint passed"
```
