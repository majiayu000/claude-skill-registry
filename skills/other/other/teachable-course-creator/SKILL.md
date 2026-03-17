---
name: teachable-course-creator
description: Create and manage Teachable online courses with browser automation and AI content generation. Use when building courses, setting up curriculum, generating content with CCG, or automating Teachable admin tasks.
allowed-tools: Bash, Read, Write, Grep, Glob, WebFetch, mcp__claude-in-chrome__*
---

# Teachable Course Creator

**Version**: 1.1.0
**Purpose**: AI Course Content Generator連携でTeachableコースを自動作成

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Course Creation | "create teachable course", "コース作成", "Teachableセットアップ" |
| Curriculum | "setup curriculum", "カリキュラム作成", "セクション追加" |
| Import | "import from mindmeister", "構造をインポート" |
| CCG Integration | "CCGからTeachableへ", "コンテンツ生成してアップロード" |

---

## Prerequisites

1. **Chrome MCP**: ブラウザ自動操作が有効
2. **Teachable Login**: 管理者としてログイン済み
3. **Course Structure**: Markdownまたはマインドマップ形式の構造

---

## Workflow

### Phase 1: コース構造の準備

#### Step 1.1: 構造データの取得

```markdown
# コース構造フォーマット

course_title: "コースタイトル"
curriculum:
  - section: "SECTION 1：【カテゴリ】セクションタイトル"
    lessons:
      - title: "レッスン1タイトル"
        type: "Video"
      - title: "レッスン2タイトル"
        type: "Video"
  - section: "SECTION 2：【カテゴリ】セクションタイトル"
    lessons:
      - title: "レッスン1タイトル"
        type: "Video"
```

#### Step 1.2: MindMeisterからの取得（オプション）

1. MindMeisterのマップURLを取得
2. WebFetchでマップ構造を解析
3. 上記フォーマットに変換

---

### Phase 2: Teachable ブラウザ操作

#### Step 2.1: 管理画面へのアクセス

```
URL形式: https://[school-name].teachable.com/admin-app/courses/[course-id]/curriculum
```

1. `tabs_context_mcp` でタブ情報取得
2. `navigate` でカリキュラムページへ移動
3. `screenshot` で現在の状態を確認

#### Step 2.2: セクションの作成/編集

**新規セクション作成:**
1. 「New section」ボタンをクリック
2. セクション名を入力
3. 「Save」をクリック

**セクション名変更:**
1. セクション行の3点メニュー（⋮）をクリック
2. 「Rename section」を選択
3. 新しい名前を入力
4. 「Save」をクリック

```javascript
// セクション操作のセレクター
Section Menu: 3点メニュー（⋮）
Rename Option: "Rename section"
Save Button: "Save"
Cancel Button: "Cancel"
```

#### Step 2.3: レッスンの作成

1. 対象セクション内の「New lesson」をクリック
2. レッスンタイトルを入力
3. コンテンツタイプを選択（Video/Text/Quiz）
4. 保存

---

### Phase 3: コース設定

#### Step 3.1: 基本情報

```
Information ページ:
- コース名
- サブタイトル
- 説明文
- サムネイル画像
```

#### Step 3.2: 価格設定

```
Pricing ページ:
- Free / Paid
- 一括払い / サブスクリプション
- 価格（円/ドル）
```

#### Step 3.3: セールスページ

```
Sales pages ページ:
- ヘッダー画像
- コース説明
- CTA ボタン
```

---

## Browser Automation Patterns

### 要素の検索と操作

```
1. find tool: 自然言語で要素検索
   例: "search bar", "save button"

2. read_page: アクセシビリティツリー取得
   - depth: 15 (デフォルト)
   - filter: "interactive" (ボタン/リンクのみ)

3. computer tool actions:
   - left_click: クリック
   - type: テキスト入力
   - scroll: スクロール
   - screenshot: スクリーンショット
```

### 安全な操作フロー

```
1. screenshot → 現状確認
2. find/read_page → 要素特定
3. click/type → 操作実行
4. screenshot → 結果確認
5. 必要に応じて修正
```

---

## Input Format Examples

### Markdown形式

```markdown
# コースタイトル

## SECTION 1：【基礎】イントロダクション
- レッスン1：はじめに (Video)
- レッスン2：基本概念 (Video)

## SECTION 2：【実践】ハンズオン
- レッスン1：実演 (Video)
- レッスン2：演習 (Quiz)
```

### YAML形式

```yaml
course_title: "コースタイトル"
curriculum:
  - section: "SECTION 1：【基礎】イントロダクション"
    lessons:
      - title: "はじめに"
        type: "Video"
      - title: "基本概念"
        type: "Video"
```

---

## Checklist

### コース作成前
- [ ] Teachableにログイン済み
- [ ] コース構造データを準備
- [ ] Chrome MCPが利用可能

### カリキュラム作成
- [ ] 全セクションを作成/命名
- [ ] 各セクションにレッスンを追加
- [ ] レッスンの順序を確認
- [ ] 公開ステータスを設定

### コース設定
- [ ] コース基本情報を入力
- [ ] 価格を設定
- [ ] セールスページを作成
- [ ] プレビューで確認

---

## Error Handling

| Error | Solution |
|-------|----------|
| 要素が見つからない | scroll して再検索 |
| クリックが効かない | 座標を確認して再試行 |
| 入力が反映されない | フィールドをクリアしてから入力 |
| ページ遷移しない | wait してから screenshot |

---

## Best Practices

```
✅ GOOD:
- 操作前後で screenshot を撮る
- セクション名は「SECTION N：【カテゴリ】タイトル」形式
- 一度に1つの操作を実行

❌ BAD:
- screenshot なしで連続操作
- 長すぎるセクション名
- 確認なしの大量操作
```

---

## CCG Integration (AI Course Content Generator)

### Overview

```
AI Course Content Generator (CCG)
/Users/shunsukehayashi/dev/ai-course-content-generator-v2

機能:
- Gemini AIでコース構造を自動生成
- レッスン台本の自動作成
- TTS音声生成
- グラフィックレコーディング風スライド
- MP4動画レンダリング
- Teachableエクスポート用MCPサーバー
```

### CCG → Teachable ワークフロー

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CCG App       │ -> │   MCP Server    │ -> │   Teachable     │
│ コンテンツ生成   │    │ エクスポート     │    │ ブラウザ操作     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Phase A: CCGでコンテンツ生成

#### Step A.1: CCGアプリ起動

```bash
cd /Users/shunsukehayashi/dev/ai-course-content-generator-v2
npm run dev          # Webモード (port 3000)
npm run electron:dev # Electronモード
```

#### Step A.2: コース構造生成

1. Vision Panelで参考資料をアップロード（画像/PDF/URL）
2. コースタイトルと概要を入力
3. 「Generate Structure」でJSON構造を生成
4. 必要に応じて構造を編集

#### Step A.3: レッスンコンテンツ生成

各レッスンで:
1. 「Generate Plan」→ 統合プラン生成
2. 「Generate Script」→ 台本生成
3. 「Generate Audio」→ TTS音声生成
4. 「Generate Slides」→ スライド画像生成
5. 「Generate Video」→ MP4動画生成

### Phase B: MCPでエクスポート

#### Step B.1: MCP Teachable Uploader

```bash
# 初回セットアップ
cd /Users/shunsukehayashi/dev/ai-course-content-generator-v2/mcp-teachable-uploader
npm install
```

#### Step B.2: MCPツール一覧

| Tool | Purpose |
|------|---------|
| `list_projects` | プロジェクト一覧取得 |
| `get_project_info` | プロジェクト詳細 |
| `get_lesson_files` | レッスンファイル一覧 |
| `export_single_lesson` | 単一レッスンエクスポート |
| `build_teachable_export` | 全レッスンエクスポート |
| `save_export_to_file` | JSONファイル保存 |

#### Step B.3: エクスポートコマンド例

```
# Claude Desktopで実行
"プロジェクト一覧を見せて"
"〇〇プロジェクトをTeachable用にエクスポートして"
"export.jsonに保存して"
```

### Phase C: Teachableにアップロード

#### Step C.1: カリキュラム構造の反映

エクスポートしたJSONからカリキュラム構造を取得し、
Phase 2のブラウザ操作でTeachableに反映。

#### Step C.2: 動画アップロード

1. Teachableのレッスン編集画面を開く
2. 「Add Video」をクリック
3. CCGで生成したMP4ファイルをアップロード

### CCG出力ファイル構造

```
projects/
└── [project-name]/
    ├── course.json           # コース構造
    ├── lessons/
    │   └── [lesson-id]/
    │       ├── plan.json     # 統合プラン
    │       ├── script.md     # 台本
    │       ├── audio.mp3     # 音声
    │       ├── slides/       # スライド画像
    │       └── video.mp4     # 完成動画
    └── export/
        └── teachable.json    # Teachableエクスポート
```

---

## Related Skills

- `ccg`: AI Course Content Generator（コンテンツ生成）
- `doc-generator`: ドキュメント生成
