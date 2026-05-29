---
name: electron-ui-patterns
description: |
  ElectronデスクトップアプリケーションのUI実装パターンと設計知識。
  BrowserWindow管理、ネイティブUI要素、フレームレスウィンドウを提供。

  Anchors:
  • Electron API / 適用: BrowserWindow・Menu・Tray / 目的: ネイティブUI実装
  • Don't Make Me Think / 適用: ウィンドウレイアウト / 目的: ユーザビリティ向上
  • Electron Security / 適用: preload・contextIsolation / 目的: セキュアなUI実装

  Trigger:
  Use when configuring BrowserWindow, implementing custom titlebars, designing native menus, developing system tray apps, or building frameless windows.
  BrowserWindow, Menu, Tray, frameless window, custom titlebar, native UI
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Electron UI Patterns

## 概要

ElectronデスクトップアプリケーションのUI実装パターンと設計知識を提供。
BrowserWindow管理、ネイティブUI要素の活用、フレームレスウィンドウの実装を支援する。

## ワークフロー

### Phase 1: UI要件の整理

**目的**: 実装対象のUI要素を特定

**アクション**:

1. 実装対象を特定（BrowserWindow、メニュー、ダイアログ）
2. `references/` で対応するパターンを確認
3. プロジェクト要件に合致するパターンを選定

### Phase 2: UI実装

**目的**: UIパターンに従って実装

**アクション**:

1. 該当する`agents/`のTask仕様書を参照
2. `assets/frameless-window.ts` などテンプレートを活用
3. BrowserWindow設定、スタイリング、イベントハンドリングを実装
4. ネイティブUI要素（メニュー、ダイアログ、トレイ）を統合

### Phase 3: 検証と記録

**目的**: 動作検証と記録

**アクション**:

1. ウィンドウ表示、メニュー動作をテスト
2. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task                | 起動タイミング             | 入力             | 出力                  |
| ------------------- | -------------------------- | ---------------- | --------------------- |
| browserwindow-setup | BrowserWindow設定時        | プロジェクト要件 | 初期化コード・preload |
| custom-titlebar     | カスタムタイトルバー実装時 | デザイン仕様     | フレームレス設定・CSS |
| native-menu         | ネイティブメニュー実装時   | 機能要件         | メニュー構築コード    |
| system-tray         | システムトレイ設定時       | アイコン画像     | Tray設定コード        |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **コンテキスト分離**: preload.jsでコンテキストを分離
- **BrowserWindow最小化**: 必要最小限の機能のみ有効化
- **IPC通信**: メインとレンダラーの分離
- **ネイティブUI活用**: プラットフォーム固有のMenu/Dialog/Tray
- **状態永続化**: ウィンドウ位置・サイズを保存

### 避けるべきこと

- **nodeIntegration有効化**: セキュリティリスク
- **enableRemoteModule使用**: 直接APIアクセスは避ける
- **synchronous IPC**: 非同期通信を使用
- **プラットフォーム差異無視**: Windows/macOS/Linuxの違いを考慮

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                     | 用途                     |
| -------------- | ------------------------------------------------------------------------ | ------------------------ |
| ネイティブUI   | See [references/native-ui.md](references/native-ui.md)                   | メニュー・ダイアログ     |
| ウィンドウ管理 | See [references/window-management.md](references/window-management.md)   | BrowserWindow詳細        |
| エディタ統合   | See [references/editor-integration.md](references/editor-integration.md) | EditorInstance・検索統合 |

### scripts/（決定論的処理）

| スクリプト           | 用途               | 使用例                                                          |
| -------------------- | ------------------ | --------------------------------------------------------------- |
| `log_usage.mjs`      | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |
| `validate-skill.mjs` | スキル構造検証     | `node scripts/validate-skill.mjs --verbose`                     |

### assets/（テンプレート）

| テンプレート          | 用途                               |
| --------------------- | ---------------------------------- |
| `frameless-window.ts` | フレームレスウィンドウテンプレート |

## 実装事例（2026-01-06追加）

### EditorView検索統合リファクタリング

search-replace-ui-implementation Phase 10で、ElectronアプリのEditorViewコンポーネントに検索・置換機能を統合した事例。

#### 背景と要件

デスクトップアプリのエディタビューに以下の検索機能を統合する必要があった：

- ファイル内検索・置換（Cmd+F / Cmd+T）
- ワークスペース全体検索・置換（Cmd+Shift+F / Cmd+Shift+T）
- ファイル名検索（Cmd+P）

課題として、検索機能はElectron IPC経由でメインプロセスと通信する必要があり、エディタ操作（ハイライト、スクロール、置換）とも連携が必要だった。

#### 適用したパターン

**EditorInstanceアダプターパターン**

異なるエディタ実装（TextArea、Monaco Editor、CodeMirror）を統一APIで操作するためのアダプターパターンを適用。

- EditorInstanceインターフェースを定義
  - getContent(): エディタ内容を取得
  - scrollToLine(line, column): 指定位置にスクロール
  - replaceText(line, column, length, replacement): 単一箇所を置換
  - replaceAllText(matches, replacement): 複数箇所を一括置換
  - focus(): エディタにフォーカス

- TextAreaEditorAdapterを実装
  - HTMLTextAreaElementをEditorInstanceインターフェースでラップ
  - 文字位置から行・列への変換ロジックを内包
  - 将来Monaco Editorに移行時はMonacoEditorAdapterを実装するだけで対応可能

**IPC検索プロバイダーパターン**

Electron IPC通信をカプセル化し、検索パネルがIPC詳細を知らなくても検索を実行できるようにした。

- WorkspaceSearchProviderをAsyncGeneratorとして定義
- ファイル単位で検索結果をyieldし、UIが段階的に結果を表示可能
- EditorView側でuseWorkspaceSearchフックとして提供
- 検索パネルはプロバイダーを受け取るだけで、IPC通信の詳細は隠蔽

**キーボードショートカット統合パターン**

エディタと検索パネル間のキーボード操作を一元管理。

- useSearchKeyboardShortcutsフックでイベントハンドリングを集約
- 検索モード（file/workspace/filename）に応じた動作の切り替え
- パネル表示中はパネル内でのキー操作を優先（Escapeでパネル閉じる等）

#### Electron固有の考慮事項

1. **IPC通信のオーバーヘッド**
   - 検索はメインプロセスで実行し、結果をレンダラーに返却
   - 大量結果時はストリーミングで段階的に返却

2. **コンテキスト分離**
   - preload.jsで公開するAPIを最小限に
   - 検索APIはelectronAPI.search.executeWorkspaceとして公開

3. **フォーカス管理**
   - 検索パネル表示時にフォーカスを検索入力に移動
   - パネル閉じる時にエディタにフォーカスを戻す

#### 成果

- EditorView: 713行 → 495行（約30%削減）
- 検索機能を独立したfeatureモジュール（apps/desktop/src/features/search/）として分離
- エディタ実装変更時の影響をアダプター層に局所化
- IPC通信のモック化によりテスト容易性向上

### IPC通信エラーハンドリングパターン（2026-01-10追加）

CONV-05-03（履歴/ログ表示UIコンポーネント）で適用したIPC通信のエラーハンドリングパターン。

#### パターン概要

Electron IPC通信において、以下のエラー状況に対応するための統一的なパターン。

| エラー種別     | 原因                               | 対応                       |
| -------------- | ---------------------------------- | -------------------------- |
| API未利用可能  | preload未設定、contextBridge未公開 | 明示的なエラーメッセージ   |
| IPC通信失敗    | チャンネル未登録、タイムアウト     | 再試行機能付きエラー表示   |
| データ取得失敗 | DBエラー、ファイル不在             | Result型でエラー情報を伝播 |

#### Result型パターン

IPC通信の結果を型安全に扱うためのパターン。

```typescript
// 成功/失敗を型で区別
interface SuccessResult<T> {
  success: true;
  data: T;
}

interface ErrorResult {
  success: false;
  error: Error;
}

type Result<T> = SuccessResult<T> | ErrorResult;

// 使用例：IPC応答の処理
const result = await window.historyAPI.getFileHistory(fileId, options);
if (result.success) {
  setHistory(result.data.items);
} else {
  setError(result.error);
}
```

#### API利用可能性チェックパターン

preloadスクリプトでAPIが正しく公開されているかを確認。

```typescript
function useVersionHistory(fileId: string) {
  const [error, setError] = useState<Error | null>(null);

  const fetchHistory = useCallback(async () => {
    // API利用可能性チェック
    if (!window.historyAPI) {
      setError(new Error("History API not available"));
      setIsLoading(false);
      return;
    }

    try {
      const result = await window.historyAPI.getFileHistory(fileId);
      // ...
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    }
  }, [fileId]);
}
```

#### 再試行機能付きエラー表示パターン

エラー発生時にユーザーが再試行できるUIを提供。

```tsx
function ErrorDisplay({
  message,
  onRetry,
}: {
  message: string;
  onRetry: () => void;
}) {
  return (
    <div role="alert" className="rounded-lg bg-red-50 p-4 text-center">
      <p className="mb-3 text-red-700">エラーが発生しました: {message}</p>
      <button
        type="button"
        onClick={onRetry}
        className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white"
      >
        再試行
      </button>
    </div>
  );
}

// 使用例：履歴一覧でのエラーハンドリング
if (error && history.length === 0) {
  return <ErrorDisplay message={error.message} onRetry={refresh} />;
}
```

#### Window型拡張パターン

TypeScriptでwindowオブジェクトの拡張を型安全に行う。

```typescript
// types.tsで型を定義
interface HistoryAPI {
  getFileHistory(
    fileId: string,
    options?: PaginationOptions,
  ): Promise<Result<PaginatedResult>>;
  // ...
}

declare global {
  interface Window {
    historyAPI?: HistoryAPI; // ?でオプショナルに
  }
}

// コンポーネントでの使用
if (window.historyAPI) {
  const result = await window.historyAPI.getFileHistory(fileId);
}
```

#### エラー種別の分類

| エラークラス  | 表示メッセージ                       | 再試行 |
| ------------- | ------------------------------------ | ------ |
| NetworkError  | 「通信エラーが発生しました」         | 可     |
| NotFoundError | 「データが見つかりません」           | 不可   |
| RestoreError  | 「復元に失敗しました」               | 可     |
| DBError       | 「データベースエラーが発生しました」 | 可     |

#### 実装詳細

詳細は以下を参照：

- 実装例: `apps/desktop/src/renderer/hooks/useVersionHistory.ts`
- 型定義: `apps/desktop/src/renderer/components/history/types.ts`
- 仕様書: `.claude/skills/aiworkflow-requirements/references/ui-ux-history-panel.md`

## 変更履歴

| Version | Date       | Changes                                             |
| ------- | ---------- | --------------------------------------------------- |
| 2.4.0   | 2026-01-10 | IPC通信エラーハンドリングパターン追加（CONV-05-03） |
| 2.3.0   | 2026-01-06 | validate-skill.mjs追加                              |
| 2.2.0   | 2026-01-06 | editor-integration.md追加、skill-creator準拠        |
| 2.1.0   | 2026-01-06 | EditorView検索統合パターン追加                      |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠、構造最適化                |
| 1.0.0   | 2025-12-31 | 初版作成                                            |
