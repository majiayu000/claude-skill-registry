---
name: hono-ddd-guidelines
description: DDDアーキテクチャでHonoのバックエンドを新規実装または既存コードベースをリファクタリングする際のガイド。レイヤー構成（domain/application/infrastructure/controller）、依存方向、責務境界、Hono公式ミドルウェア/プラグインの活用、Hono OpenAPIプラグイン（hono-openapi）とzod-openapiの必須採用、Drizzle ORMの利用、トランザクション境界、エラーハンドリング、テスト指針、ESLint/Prettierの必須導入を含む。
---

# Hono DDD Guidelines

## 目的
- HonoでDDD構成のバックエンドを設計/実装/リファクタリングする手順と判断基準を提供する
- レイヤー責務と依存方向を明確化する
- Honoの公式ミドルウェア/プラグインを優先した構成を徹底する
- OpenAPIは `hono-openapi` + `zod-openapi` を必須とし、スキーマ駆動で設計する
- Drizzle ORMを前提にセッション/トランザクション境界を標準化する
- テストはHono公式ガイドに準拠し、`app.request()` をベースに設計する
- ESLint/Prettier を必須とし、型安全性とフォーマットの自動化を前提にする

## 使い方
1) 依頼内容が「新規実装」か「リファクタリング」かを明確化する
2) 必要に応じて `references/` を読む（下記参照）
3) レイヤー構成・依存方向・責務の合意を作成する
4) 具体的なディレクトリ構成・実装方針・コード例を示す

## 参照ファイル
- レイヤー責務と依存方向のルール: `references/layers.md`
- Drizzleのトランザクション/UoW/DI: `references/transactions-uow.md`
- OpenAPI/Zodプラグイン運用: `references/openapi.md`
- テスト指針: `references/testing.md`
- 実装テンプレ/ディレクトリ構成例: `references/templates.md`

## 実行ガイド
- まず `references/layers.md` を読み、責務/依存方向/配置ルールを回答の土台にする
- トランザクションやDIが必要なら `references/transactions-uow.md` を読む
- OpenAPIやバリデーション設計が必要なら `references/openapi.md` を読む
- テスト方針が必要なら `references/testing.md` を読む
- 新規実装やリファクタリングで具体的な構成が必要なら `references/templates.md` を読む
- 出力は日本語、簡潔かつ具体的に
