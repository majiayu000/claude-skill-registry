---
name: component
description: React Nativeの再利用可能なUIコンポーネントを作成する。「コンポーネントを作って」「ボタンを作成」などのリクエストで使用する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [コンポーネント名]
---

# コンポーネント作成

`src/components/` に React Native の関数コンポーネントを作成する。

## 手順

1. `src/components/` ディレクトリが存在しなければ作成する
2. PascalCase のファイル名で `.tsx` ファイルを作成する（例: `$ARGUMENTS.tsx`）
3. 既存コンポーネントのスタイルと一貫性を保つ

## テンプレート

```tsx
import React from 'react';
import { StyleSheet, View, Text } from 'react-native';

interface Props {
  // props をここに定義
}

export const ComponentName: React.FC<Props> = ({}) => {
  return (
    <View style={styles.container}>
      <Text>ComponentName</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {},
});
```

## ルール

- `export default` ではなく名前付きエクスポートを使う
- Props は `interface` で定義する
- スタイルは `StyleSheet.create()` で定義する
- React Native のコンポーネント（`View`, `Text`, `TouchableOpacity` 等）を使う（HTML 要素は使わない）
- 不要な依存パッケージを追加しない
