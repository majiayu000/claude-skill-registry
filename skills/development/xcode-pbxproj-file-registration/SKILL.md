---
name: xcode-pbxproj-file-registration
description: "Use when xcodebuild fails with 'cannot find in scope' after adding a .swift file outside Xcode. Register in 4 pbxproj sections."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-11"
---

# Xcode pbxproj Manual File Registration

**Extracted:** 2026-02-11
**Context:** Xcode プロジェクト (.xcodeproj) に新規 .swift ファイルを CLI から追加する場合

## Problem

`GKentei/Views/Quiz/EnhancedExplanationView.swift` を作成後、`xcodebuild` で以下のエラー:

```
error: cannot find 'EnhancedExplanationView' in scope
```

ファイルがディスク上に存在しても、`project.pbxproj` に登録されていないとビルド対象にならない。

## Solution

`project.pbxproj` の **4箇所** に新規エントリを追加する:

### 1. PBXBuildFile (ビルド対象登録)
```
UNIQUE_ID_BB /* FileName.swift in Sources */ = {isa = PBXBuildFile; fileRef = UNIQUE_ID_CC /* FileName.swift */; };
```

### 2. PBXFileReference (ファイル参照定義)
```
UNIQUE_ID_CC /* FileName.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = FileName.swift; sourceTree = "<group>"; };
```

### 3. PBXGroup children (グループ内ファイル一覧)
```
UNIQUE_ID_CC /* FileName.swift */,
```

### 4. Sources ビルドフェーズ
```
UNIQUE_ID_BB /* FileName.swift in Sources */,
```

## ID 命名規則

既存ファイルの ID パターンに合わせる。例:
- `AAAA000011112222BBBB0006` (BuildFile)
- `AAAA000011112222CCCC0006` (FileReference)

## 手順

1. 既存の同グループファイル（例: `QuizQuestionComponents.swift`）を `grep` で探す
2. 4箇所の挿入ポイントを特定
3. 既存エントリの直前/直後に新規エントリを追加
4. `xcodebuild` で確認

## When to Use

- CLI（Claude Code 等）から `.swift` ファイルを新規作成した時
- `xcodebuild` で "cannot find ... in scope" エラーが出た時
- `.xcodeproj` を使用するプロジェクト（SPM-only プロジェクトでは不要）

## Gotcha

- `.xcodeproj` が `.gitignore` に入っている場合、pbxproj の変更はコミットされない。Xcode で手動追加が必要
- `xcodebuild` でシミュレータ名が重複する場合は `id=UUID` で指定する
