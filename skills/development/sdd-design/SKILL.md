---
name: sdd-design
description: C4モデルに基づく設計ドキュメント(design.md)を生成。Context/Container/Component図をMermaidで作成し、API契約・データモデル・セキュリティ設計を含む。
argument-hint: "[spec-slug] [target-dir(optional)]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep
model: opus
---

# sdd-design — C4 Model Design Document Generator

## 0. 目的
- C4モデル（Context, Container, Component, Code）に基づく設計ドキュメントを生成
- Mermaid図で視覚的なアーキテクチャを表現
- API契約、データモデル、セキュリティ設計を含む包括的な設計書

## 1. 入力と出力

### 入力
- /sdd-design $ARGUMENTS
  - $0 = spec-slug（例: google-ad-report）
  - $1 = target-dir（任意。未指定なら `.kiro/specs/<spec-slug>/` を使う）
- 前提: requirements.md が既に存在すること

### 出力（必須）
- <target-dir>/design.md

### 参照
- templates/design.template.md : 設計書テンプレート
- <target-dir>/requirements.md : 要件定義（入力として読む）

## 2. 重要ルール

1. **C4モデル厳守**: Context → Container → Component の順で抽象度を下げる
2. **Mermaid形式**: 全図はMermaid記法で記述（プレビュー可能）
3. **要件トレーサビリティ**: 各コンポーネントがどのREQを実現するか明記
4. **セキュリティバイデザイン**: セキュリティ考慮を設計段階で組み込む

## 3. 手順

### Step A: 要件の読み込み
1. <target-dir>/requirements.md を読み込む
2. 機能要件・非機能要件・セキュリティ要件を抽出
3. ステークホルダーと外部システムを特定

### Step B: C4レベル1 - Context図
1. システムの境界を定義
2. 外部アクター（ユーザー、外部システム）を配置
3. 主要なデータフローを示す

### Step C: C4レベル2 - Container図
1. システム内の主要コンテナ（アプリ、DB、キャッシュ等）を配置
2. 技術スタックを明記
3. コンテナ間の通信プロトコルを示す

### Step D: C4レベル3 - Component図
1. 各コンテナ内の主要コンポーネントを配置
2. 責務と依存関係を明確化
3. 要件とのマッピング（REQ-xxx）

### Step E: API契約
1. 主要エンドポイントの定義
2. リクエスト/レスポンス形式
3. エラーコード体系

### Step F: データモデル
1. エンティティ関係図（ER図）
2. 主要テーブル/コレクションの定義
3. インデックス戦略

### Step G: セキュリティ設計
1. 認証・認可の仕組み
2. データ暗号化方針
3. 監査ログ設計

### Step H: 非機能設計
1. スケーラビリティ戦略
2. 可観測性（Observability）設計
3. 障害復旧設計

## 4. 出力形式

design.template.md に従って出力する。

## 5. 実行例

```bash
/sdd-design google-ad-report
```

前提:
- .kiro/specs/google-ad-report/requirements.md が存在

出力:
- .kiro/specs/google-ad-report/design.md
