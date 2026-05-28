---
name: screen
description: React Nativeの画面（Screen）コンポーネントを作成する。「画面を追加して」「ホーム画面を作って」などのリクエストで使用する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [画面名]
---

# 画面コンポーネント作成

`src/screens/` に画面用コンポーネントを作成する。

## 手順

1. `src/screens/` ディレクトリが存在しなければ作成する
2. PascalCase のファイル名で `.tsx` ファイルを作成する（例: `$ARGUMENTS.tsx` または `${ARGUMENTS}Screen.tsx`）
3. 画面名が "Screen" で終わっていなければ自動でサフィックスを付ける

## テンプレート

```tsx
import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { StatusBar } from 'expo-status-bar';

export const ScreenNameScreen: React.FC = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>ScreenName</Text>
      <StatusBar style="auto" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },
});
```

## ルール

- 画面コンポーネントは `flex: 1` でフルスクリーンにする
- `SafeAreaView` や `StatusBar` を適切に使う
- ナビゲーションライブラリが導入済みなら、navigation props の型を適切に定義する
- ビジネスロジックが複雑な場合はカスタムフックに切り出す
