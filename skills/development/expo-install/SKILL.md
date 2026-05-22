---
name: expo-install
description: Expoプロジェクトにパッケージをインストールする。「ナビゲーションを入れて」「カメラ機能を追加」などのリクエストで使用する。
allowed-tools: Read, Bash, Edit
argument-hint: [パッケージ名またはカテゴリ]
---

# Expo パッケージインストール

Expo 互換バージョンでパッケージをインストールし、必要な設定を行う。

## 手順

1. 引数がカテゴリ名（例: "navigation", "camera"）の場合は、対応するパッケージ群を特定する
2. `npx expo install` でインストールする（`npm install` は使わない）
3. `app.json` や設定ファイルの変更が必要な場合は更新する
4. 基本的な使い方をコード例として示す

## よく使うカテゴリとパッケージ

- **navigation**: `@react-navigation/native @react-navigation/native-stack react-native-screens react-native-safe-area-context`
- **tabs**: `@react-navigation/bottom-tabs`（navigation も必要）
- **camera**: `expo-camera`
- **image-picker**: `expo-image-picker`
- **location**: `expo-location`
- **storage**: `@react-native-async-storage/async-storage`
- **font**: `expo-font`
- **icons**: `@expo/vector-icons`
- **gradient**: `expo-linear-gradient`
- **haptics**: `expo-haptics`
- **notifications**: `expo-notifications expo-device expo-constants`
- **splash**: `expo-splash-screen`
- **auth**: `expo-auth-session expo-crypto`
- **secure-store**: `expo-secure-store`

## ルール

- 必ず `npx expo install` を使う（Expo SDK との互換性を保証するため）
- インストール後 `npx expo install --check` で互換性を確認する
- app.json への plugin 追加が必要なパッケージは設定も行う
