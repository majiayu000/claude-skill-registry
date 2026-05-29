# Add Tutorial

チュートリアルGIFを追加し、Tutorial機能に新しいチュートリアル項目を登録するスキル

## 使用方法

```
/add-tutorial <gif-filename> <title-ja> <title-en>
```

### パラメータ

- `gif-filename`: GIFファイル名（例: `how_to_draw_text.gif`）
- `title-ja`: 日本語タイトル（例: "テキストをマップ上に表示する方法"）
- `title-en`: 英語タイトル（例: "How to Display Text on Map"）

### ステップの追加

コマンド実行後、対話形式でステップを追加します：

1. ステップ数を入力（2-5推奨）
2. 各ステップの日本語と英語のテキストを入力

## 実装手順

### 1. Manifestファイルへの追加

`manifest.json` と `manifest.template.json` の `web_accessible_resources` に GIF ファイルを追加：

```json
{
  "web_accessible_resources": [{
    "resources": [
      "assets/images/tutorial/how_to_draw.gif",
      "assets/images/tutorial/<new-gif-filename>"  // 追加
    ]
  }]
}
```

### 2. Tutorial クラスへの項目追加

`src/features/tutorial/index.ts` の `tutorials` 配列に新しい項目を追加：

```typescript
{
  id: "tutorial_id",
  titleKey: "tutorial_<id>_title",
  gifUrl: runtime.getURL("assets/images/tutorial/<gif-filename>"),
  steps: [
    "tutorial_<id>_step1",
    "tutorial_<id>_step2",
    "tutorial_<id>_step3",
  ],
}
```

### 3. 国際化キーの追加

#### 英語 (`src/i18n/locales/en.ts`)

```typescript
tutorial_<id>_title: "English Title",
tutorial_<id>_step1: "Step 1 description",
tutorial_<id>_step2: "Step 2 description",
tutorial_<id>_step3: "Step 3 description",
```

#### 日本語 (`src/i18n/locales/ja.ts`)

```typescript
tutorial_<id>_title: "日本語タイトル",
tutorial_<id>_step1: "ステップ1の説明",
tutorial_<id>_step2: "ステップ2の説明",
tutorial_<id>_step3: "ステップ3の説明",
```

## 命名規則

### Tutorial ID

- フォーマット: `how_to_<action>` または `how_to_<action>_<target>`
- 例:
  - `how_to_draw` - 画像描画
  - `how_to_archive` - アーカイブ保存
  - `how_to_draw_archive` - アーカイブ描画
  - `how_to_draw_text` - テキスト描画

### i18n キー

- タイトル: `tutorial_<id>_title`
- ステップ: `tutorial_<id>_step1`, `tutorial_<id>_step2`, ...

## 既存のチュートリアル例

### 1. 画像描画 (how_to_draw)

```typescript
{
  id: "how_to_draw",
  titleKey: "tutorial_how_to_draw_title",
  gifUrl: runtime.getURL("assets/images/tutorial/how_to_draw.gif"),
  steps: [
    "tutorial_how_to_draw_step1",  // ギャラリーに画像を保存する
    "tutorial_how_to_draw_step2",  // マップをクリックして、「画像」ボタンを選択
    "tutorial_how_to_draw_step3",  // 配置したい画像をクリック
  ],
}
```

### 2. アーカイブ保存 (how_to_archive)

```typescript
{
  id: "how_to_archive",
  titleKey: "tutorial_how_to_archive_title",
  gifUrl: runtime.getURL("assets/images/tutorial/how_to_archive.gif"),
  steps: [
    "tutorial_how_to_archive_step1",  // マップをクリックして「アーカイブ」を選択
    "tutorial_how_to_archive_step2",  // 「Save Current Tile」ボタンをクリック
  ],
}
```

### 3. テキスト描画 (how_to_draw_text)

```typescript
{
  id: "how_to_draw_text",
  titleKey: "tutorial_how_to_draw_text_title",
  gifUrl: runtime.getURL("assets/images/tutorial/how_to_draw_text.gif"),
  steps: [
    "tutorial_how_to_draw_text_step1",  // マップをクリックして「テキスト」を選択
    "tutorial_how_to_draw_text_step2",  // テキストを入力し、フォントを選んで「Draw」ボタンをクリック
    "tutorial_how_to_draw_text_step3",  // オプション：矢印ボタンで位置を調節
  ],
}
```

## チェックリスト

実装時に確認すべき項目：

- [ ] GIFファイルが `public/assets/images/tutorial/` に配置されている
- [ ] `manifest.json` に GIF が追加されている
- [ ] `manifest.template.json` に GIF が追加されている
- [ ] `src/features/tutorial/index.ts` に項目が追加されている
- [ ] `src/i18n/locales/en.ts` に英語キーが追加されている
- [ ] `src/i18n/locales/ja.ts` に日本語キーが追加されている
- [ ] ステップ数が2-5個の範囲である
- [ ] ID が他のチュートリアルと重複していない

## ファイル構造

```
wplace-studio/
├── public/
│   └── assets/
│       └── images/
│           └── tutorial/
│               ├── how_to_draw.gif
│               ├── how_to_archive.gif
│               ├── how_to_draw_archive.gif
│               ├── how_to_draw_text.gif
│               └── <new-tutorial>.gif
├── manifest.json
├── manifest.template.json
└── src/
    ├── features/
    │   └── tutorial/
    │       └── index.ts
    └── i18n/
        └── locales/
            ├── en.ts
            └── ja.ts
```

## 注意事項

1. **GIFファイルのサイズ**: できるだけ軽量に（推奨: 1MB以下）
2. **ステップ数**: 多すぎると読みにくいため、2-5個を推奨
3. **命名規則**: 一貫性のため `how_to_*` パターンを使用
4. **i18nキーの順序**: 既存のチュートリアルキーの後に追加
5. **空状態メッセージ**: 必要に応じて `empty_*_message` キーも追加

## コミットメッセージ例

```
feat(tutorial): add <action> tutorial

- Add <gif-filename> to web accessible resources
- Add <action> tutorial to Tutorial class
- Add i18n keys for <action> tutorial (en/ja)
```

## トラブルシューティング

### GIFが表示されない

1. ブラウザの開発者ツールでネットワークタブを確認
2. GIF ファイルが正しいパスに配置されているか確認
3. manifest.json を更新後、拡張機能を再読み込み

### チュートリアルが一覧に表示されない

1. `src/features/tutorial/index.ts` の構文エラーを確認
2. i18n キーが正しく登録されているか確認
3. ブラウザコンソールでエラーがないか確認
