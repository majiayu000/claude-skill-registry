---
name: build-check
description: Kotlin shared層とiOS/Androidのビルドを実行し、エラー・警告を報告する
user-invocable: true
argument-hint: "[ios|android|shared|all] (デフォルト: all)"
allowed-tools: Bash, Read, Grep, mcp__xcode__BuildProject, mcp__xcode__GetBuildLog
---

# ビルド確認スキル

指定されたプラットフォームのビルドを実行し、エラー・警告を収集して報告する。

## 処理フロー

1. 引数に応じてビルドコマンドを実行
2. エラー/警告を収集・分類
3. 修正アドバイスを提示

## ビルドコマンド

| 引数 | コマンド |
|------|---------|
| `shared` | `./gradlew :shared:testDebugUnitTest` |
| `android` | `./gradlew :composeApp:assembleDebug` |
| `ios` | Xcode MCPの`BuildProject` |
| `all`（デフォルト） | 上記すべてを順に実行 |

## 出力フォーマット

```markdown
## ビルドレポート

### shared (Kotlin)
- ステータス: SUCCESS / FAILURE
- エラー: X件
- 警告: Y件
- テスト: Z passed, W failed

### android
- ステータス: SUCCESS / FAILURE
- エラー: X件

### ios
- ステータス: SUCCESS / FAILURE
- エラー: X件
- 警告: Y件

### エラー詳細
（各エラーの内容と修正アドバイス）
```

## 注意事項

- `all`指定時はshared → android → iOSの順で実行（sharedがベースのため）
- ビルドエラーが発生した場合、後続のビルドもスキップせず全て実行する
- Xcode MCPが利用できない場合はiOSビルドをスキップし、その旨を報告
