---
name: spec
description: Create or update flutter_real_estate/docs/SPECIFICATION.md for the Flutter Real Estate app, including functional/non-functional requirements, UI/UX, data model, and technical constraints for a real-estate management application.
---

# Specification Authoring (Flutter Real Estate)

## Goal
Write a clear, complete SPECIFICATION.md for a real-estate management app. Use Japanese. Replace outdated or unrelated content.

## Workflow
1. Open `flutter_real_estate/docs/SPECIFICATION.md`.
2. Rewrite it to match a real-estate management app (not music/audio).
3. Keep the section structure and tables, but adapt all content to real estate.
4. Include concrete feature lists, data model entities, and platform/tech constraints.
5. Update "作成日/最終更新/バージョン" with today’s date and a semantic version.

## Content Requirements (must include)
### 1. 概要
- アプリケーション名: Flutter Real Estate
- 目的: 物件・建物・入居者・契約・支払い・メンテナンスを管理
- 対象プラットフォーム: Android (API レベル範囲)

### 2. 機能要件
Use tables with `機能ID / 機能名 / 説明 / 優先度`.
Include at minimum:
- 不動産種別（例: マンション/戸建/オフィスなど）
- 建物一覧・建物詳細
- 物件（部屋/区画）一覧・詳細
- 入居者管理（入居者情報、連絡先、入退去）
- 契約管理（契約期間、賃料、更新、解約）
- 支払い管理（請求、入金、滞納）
- メンテナンス・修繕履歴
- ドキュメント/写真の添付

### 3. 非機能要件
Performance, data persistence, security. Use realistic values for local DB usage.

### 4. UI/UX 要件
画面構成（一覧/詳細/編集/検索/フィルタ）と主要画面要素。

### 5. データモデル
Provide Dart model sketches for core entities:
`PropertyType`, `Building`, `Unit`, `Tenant`, `LeaseContract`, `Payment`, `Maintenance`, `Attachment`.

### 6. 技術仕様
Flutter/Dart versions, state management, storage (SQLite), architecture patterns.

### 7. 制約事項
Offline-first, Android-only (if applicable), local storage only, etc.

### 8. 将来拡張予定
例: クラウド同期、通知、CSV エクスポート、権限ロール。

## Style
- Keep headings and numbering.
- Keep tables consistent.
- Use concise bullet points.
