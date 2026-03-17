---
name: browser-ext-creator
description: |
  ブラウザ拡張機能の開発を支援するスキル。
  Chrome (Manifest V3) と Firefox に対応したブラウザ拡張を設計・実装する。
  以下の状況で使用:
    (1) ユーザーが「ブラウザ拡張を作って」「Chrome拡張を実装して」「Firefox拡張を開発して」と依頼した時
    (2) ユーザーが明示的に「/browser-ext-creator」を実行した時
    (3) 特定のウェブサイトの機能拡張や自動化を求められた時
    (4) content script、background script、popup UIなどの拡張機能コンポーネントの実装が必要な時
---

# Browser Extension Creator

ブラウザ拡張機能（Chrome Manifest V3 / Firefox）の設計・実装を支援するスキル。

## ワークフロー概要

```
1. 要件収集 → AskUserQuestion で機能仕様を確認
2. 設計     → プロジェクト構造とファイル構成を決定
3. 実装     → テンプレートをベースにコード生成
4. 自己評価 → セキュリティ・パフォーマンス観点で自己評価
```

## Step 1: 要件収集

AskUserQuestion ツールで以下を確認する：

### 必須項目

1. **機能概要**: 実装したい機能の全体像と目的
2. **機能要件リスト**: 実現したい機能を箇条書きで
3. **対象ブラウザ**: Chrome / Firefox / 両方
4. **動作対象サイト**: 機能が動作するURL（例: `https://www.youtube.com/watch*`）

### UI要件

- **ページ埋め込みUI**: 対象ページに追加するUI要素
- **ポップアップ**: 拡張アイコンクリックで表示するUI
- **設定ページ (Options)**: ユーザー設定用UI

### データ連携

- **外部API連携**: エンドポイント、リクエスト/レスポンス形式
- **データ保存**: `chrome.storage.sync` / `chrome.storage.local` の使用

## Step 2: 設計（プロジェクト構造の決定）

### Chrome (Manifest V3)

```
extension-name/
├── manifest.json           # 拡張機能の設定（Manifest V3）
├── content-script.js       # 対象ページに注入されるスクリプト
├── background.js           # Service Worker（バックグラウンド処理）
├── popup/
│   ├── popup.html          # ポップアップUI
│   ├── popup.css
│   └── popup.js
├── options/
│   ├── options.html        # 設定ページUI
│   ├── options.css
│   └── options.js
├── styles/
│   └── content.css         # ページ埋め込みスタイル
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

### Firefox

Firefox はほぼ同じ構造だが、`manifest.json` に差異あり（`browser_specific_settings` が必要）。

## Step 3: 実装

### manifest.json (Chrome Manifest V3)

```json
{
  "manifest_version": 3,
  "name": "Extension Name",
  "version": "1.0.0",
  "description": "Extension description",
  "permissions": [],
  "host_permissions": ["https://example.com/*"],
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "content_scripts": [
    {
      "matches": ["https://example.com/*"],
      "js": ["content-script.js"],
      "css": ["styles/content.css"]
    }
  ],
  "background": {
    "service_worker": "background.js"
  },
  "options_ui": {
    "page": "options/options.html",
    "open_in_tab": true
  }
}
```

### Content Script パターン

```javascript
// content-script.js
(() => {
  'use strict';

  // Wait for page load
  const init = () => {
    // Avoid duplicate initialization
    if (document.querySelector('#my-extension-container')) return;

    // Create UI element
    const container = document.createElement('div');
    container.id = 'my-extension-container';
    container.textContent = 'Extension Loaded';
    document.body.appendChild(container);
  };

  // Handle SPA navigation
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Observe URL changes for SPA
  let lastUrl = location.href;
  new MutationObserver(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      init();
    }
  }).observe(document.body, { subtree: true, childList: true });
})();
```

### Background Script (Service Worker)

```javascript
// background.js
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});

// Message handler
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'fetchData') {
    fetchData(request.url)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep message channel open for async response
  }
});

const fetchData = async (url) => {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
};
```

### Storage API

```javascript
// Save settings
const saveSettings = async (settings) => {
  await chrome.storage.sync.set(settings);
};

// Load settings
const loadSettings = async () => {
  return chrome.storage.sync.get({
    // Default values
    apiKey: '',
    enabled: true
  });
};
```

## Step 4: 自己評価

生成したコードを以下の観点で評価：

### 要件準拠

- [ ] すべての機能要件を満たしているか
- [ ] 指定されたサイトで正しく動作するか

### Manifest V3 準拠

- [ ] `manifest_version: 3` を使用
- [ ] Service Worker を background script として使用
- [ ] `host_permissions` で必要なドメインのみ許可
- [ ] 動的コード実行（`eval`, `new Function`）を使用していない

### セキュリティ

- [ ] XSS防止: `textContent` 使用 or DOMPurify でサニタイズ
- [ ] 最小権限の原則: 必要最小限の permissions のみ要求
- [ ] 外部通信: 必要最小限のエンドポイントのみ
- [ ] ユーザー入力のバリデーション実施

### パフォーマンス

- [ ] 不要な DOM 操作を避けている
- [ ] MutationObserver の監視範囲が適切
- [ ] メモリリークを防止している

## コーディング規約

| 項目 | 規約 |
|------|------|
| ファイル名 | ケバブケース（例: `content-script.js`） |
| 変数名 | キャメルケース（例: `selectedElement`） |
| 関数 | アロー関数を優先 |
| エラー処理 | try-catch で適切に例外処理 |

## リファレンス

詳細な技術情報：

- **Manifest V3 詳細**: {このSKILL.mdのDIR}/references/manifest-v3.md
- **セキュリティガイド**: {このSKILL.mdのDIR}/references/security.md

## テンプレート

プロジェクトテンプレート：

- **Chrome**: {このSKILL.mdのDIR}/assets/chrome-template
- **Firefox**: {このSKILL.mdのDIR}/assets/firefox-template
