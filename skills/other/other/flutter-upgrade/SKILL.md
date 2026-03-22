---
name: flutter-upgrade
description: Flutter SDKバージョンアップグレード対応。新バージョンのリリースノート・Breaking Changes調査、コードベース影響分析、mise/CI/Shorebird含むプロジェクト全体の対応タスクリスト作成と実行。「Flutterアップグレード」「Flutter X.Y.Zがリリースされた」「Flutter最新化」「Flutter更新」と言われたとき、またはFlutterの新バージョンについて言及されたときに使用する。
---

# Flutter Upgrade

Flutter SDKの新バージョンへのアップグレードを体系的に進めるスキル。
リリースノート調査からコード修正・検証まで一貫して対応する。

## フェーズ1: 情報収集

### 1-1. リリースノート調査

WebSearch / WebFetch で以下を調査する:

- **Hotfix Issue**: `https://github.com/flutter/flutter/issues` で `[stable] [hotfix] Flutter Release Version X.Y.Z` を検索
- **Release Notes**: `https://docs.flutter.dev/release/release-notes/release-notes-X.Y.0`
- **Breaking Changes**: `https://docs.flutter.dev/release/breaking-changes`
- **Flutter blog**: `https://blog.flutter.dev` の What's new 記事
- **CHANGELOG**: `https://github.com/flutter/flutter/blob/master/CHANGELOG.md`

hotfix リリース (X.Y.1〜) の場合、メジャーリリース (X.Y.0) の Breaking Changes も含めて調査する。

### 1-2. 現在のプロジェクト状態を確認

```bash
# 現在のFlutterバージョン
flutter --version

# mise管理のバージョン
cat .mise.toml

# Dart SDK制約
grep -A1 'environment:' apps/mobile/pubspec.yaml
```

## フェーズ2: プロジェクト影響分析

### 2-1. Breaking Changes のコードベースマッチング

リリースノートで見つかった Breaking Changes / 非推奨API それぞれについて、
`Grep` でコードベース内の使用箇所を検索する。

```
Grep pattern="<deprecated_api>" path="apps/mobile" glob="*.dart"
```

該当なし → 対応不要と明記。該当あり → ファイルと箇所数を記録。

### 2-2. プロジェクト固有の影響チェック

このプロジェクトには以下の固有構成があり、それぞれ確認が必要:

#### mise (バージョン管理)
- `.mise.toml` の `flutter` バージョンを更新する必要がある
- グローバルにも反映する (`mise use --global`)

#### CI/CD (GitHub Actions)
- 全ワークフローが `.mise.toml` から Flutter バージョンを読み取る仕組み
  (`grep 'flutter' .mise.toml` → `flutter-action` の `flutter-version`)
- `.mise.toml` を更新すれば全ワークフローに自動反映される
- ワークフロー一覧を `Grep` で確認し、変更が正しく伝播するか確認する

```bash
grep -r "mise.toml" .github/workflows/
```

#### Shorebird (OTA パッチ)
- Shorebird はリリース時の Flutter バージョンでビルドを管理する
- 既存リリースへのパッチは旧バージョンで行う必要がある
- 新バージョンで新リリースを作る場合は問題ない
- `shorebird doctor` で互換性を確認する

#### dependency_overrides (一時的フォーク)
- `pubspec.yaml` の `dependency_overrides` セクションを確認
- 各オーバーライドが本家にマージ済み / pub.dev にリリース済みなら削除できるか調査
- WebSearch で最新状況を確認する

#### パッケージ互換性
- `flutter pub outdated` で非互換パッケージがないか確認
- 特に Shorebird, Firebase, google_fonts など Flutter バージョンに敏感なパッケージに注意

### 2-3. Dart SDK 制約
- `pubspec.yaml` の `environment.sdk` が新バージョン同梱の Dart と互換か確認
- 非互換なら SDK 制約の更新も必要

## フェーズ3: 対応タスクリスト作成

調査結果を以下の形式でまとめる:

### テンプレート

```
## Flutter X.Y.Z アップグレード対応リスト

### 必須（アップグレードに必要）
1. `.mise.toml` の Flutter バージョン更新
2. `mise install flutter@X.Y.Z && mise use --global flutter@X.Y.Z`
3. `flutter pub get` → `dart analyze` → `flutter test`
4. [Breaking Changes で必要な修正があればここに]

### 推奨（非推奨API解消）
- [非推奨APIの移行タスク]

### 確認（視覚的・動作確認）
- [テーマ色の変化、フォント描画の変化など]

### 棚卸し（dependency_overrides等）
- [削除可能なオーバーライド]
- [更新可能なパッケージ]
```

影響がないものも「該当なし」と明記し、調査漏れがないことを示す。

## フェーズ4: 実行

ユーザーの確認を得てから実行に移る。

### 4-1. mise 更新

```bash
# .mise.toml 編集（Edit ツールで）
# flutter = "旧バージョン" → "新バージョン"

# インストール & グローバル反映
mise install flutter@X.Y.Z
mise use --global flutter@X.Y.Z

# 確認
flutter --version
```

### 4-2. ビルド・テスト

```bash
cd apps/mobile && flutter pub get
dart analyze apps/mobile
cd apps/mobile && flutter test
```

### 4-3. コード修正

Breaking Changes や非推奨API の修正を実施。

### 4-4. 検証

変更内容に応じて `/test-flutter` や `/mobile-automation` を実行。
