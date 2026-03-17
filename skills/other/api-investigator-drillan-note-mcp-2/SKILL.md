---
name: api-investigator
description: note.com APIの調査を支援します。mitmproxyとPlaywrightを使用してHTTPトラフィックをキャプチャ・分析し、API動作を解明します。
allowed-tools: Read Edit Write Glob Grep Bash
---

# API Investigator スキル

このスキルは、note.com APIの動作を調査するための`investigator`モジュールの利用方法を提供します。

## 起動条件

以下の状況で起動します：

1. **API動作の調査時**: note.com APIのリクエスト/レスポンス形式を確認する際
2. **新機能の実装前調査**: 未知のAPIエンドポイントの動作を理解する必要がある際
3. **バグ調査時**: API通信に関連する問題を診断する際
4. **ProseMirrorエディタ調査時**: note.comのエディタDOM構造やイベントを調査する際
5. **認証フロー調査時**: ログイン・セッション管理の動作を確認する際

## 前提条件

### 必要なソフトウェア

- mitmproxy（mitmdumpコマンド）
- Playwright

### インストール

```bash
# 開発依存関係のインストール（mitmproxy含む）
uv sync --group dev

# Playwrightブラウザのインストール
uv run playwright install chromium
```

## 使用方法

### 1. トラフィックキャプチャ

```bash
# 基本的なキャプチャ（セッション自動復元）
uv run python -m note_mcp.investigator capture

# ドメインフィルタ付きキャプチャ
uv run python -m note_mcp.investigator capture --domain api.note.com

# 出力ファイル指定
uv run python -m note_mcp.investigator capture -o my_capture.flow

# セッション復元なし（新規ログイン必要）
uv run python -m note_mcp.investigator capture --no-session

# カスタムポート
uv run python -m note_mcp.investigator capture --port 8888
```

### 2. キャプチャ分析

```bash
# 基本的な分析
uv run python -m note_mcp.investigator analyze traffic.flow

# パターンで検索
uv run python -m note_mcp.investigator analyze traffic.flow --pattern citation

# ドメインとメソッドでフィルタ
uv run python -m note_mcp.investigator analyze traffic.flow --domain api.note.com --method POST
```

### 3. JSONエクスポート

```bash
# JSON形式でエクスポート
uv run python -m note_mcp.investigator export traffic.flow -o api_calls.json

# ドメインフィルタ付きエクスポート
uv run python -m note_mcp.investigator export traffic.flow --domain api.note.com
```

## セッション管理

### 自動セッション復元

`note_login` MCPツールでログイン済みの場合、保存されたセッションCookieが自動的にブラウザに注入されます。

```
captureコマンド実行
    ↓
SessionManagerからCookie読み込み
    ↓
PlaywrightブラウザにCookie注入
    ↓
ログイン状態でキャプチャ開始
```

### セッションがない場合

1. ブラウザが開く
2. note.comに手動でログイン
3. 調査操作を実行
4. ブラウザを閉じてキャプチャ終了

## 調査ワークフロー例

### 例1: 引用（blockquote）出典APIの調査（実績あり）

```bash
# Step 1: note.comへのトラフィックをキャプチャ
uv run python -m note_mcp.investigator capture -d note.com -o citation.flow

# ブラウザで:
# 1. 新規記事作成画面（/notes/new）を開く
# 2. 引用ブロックを追加
# 3. 出典を入力
# 4. 下書き保存
# 5. ブラウザを閉じる

# Step 2: draft_save APIを分析
uv run python -m note_mcp.investigator analyze citation.flow --pattern draft_save

# Step 3: 詳細をJSONでエクスポート
uv run python -m note_mcp.investigator export citation.flow -o citation_api.json

# Step 4: Pythonで詳細確認
uv run python -c "
import json
with open('citation_api.json') as f:
    data = json.load(f)
for item in data:
    req = item.get('request', {})
    if 'draft_save' in req.get('url', ''):
        body = json.loads(req.get('body', '{}'))
        print(json.dumps(body, indent=2, ensure_ascii=False))
"
```

#### 調査結果例（2024-12-30実施）

引用の出典はAPIで以下のHTML構造として送信されることが判明：

```html
<figure name="UUID" id="UUID">
  <blockquote>
    <p name="UUID" id="UUID">引用テキスト<br>改行も可能</p>
  </blockquote>
  <figcaption>出典URL（例: example.com）</figcaption>
</figure>
```

- `<figure>` で全体をラップ
- `<blockquote><p>` 内に引用テキスト
- `<figcaption>` に出典情報
- 改行は `<br>` タグ

### 例2: 画像アップロードAPIの調査

```bash
# アップロード関連のトラフィックをキャプチャ
uv run python -m note_mcp.investigator capture -d note.com -o upload.flow

# ブラウザで画像をアップロード後、閉じる

# POSTリクエストのみ分析
uv run python -m note_mcp.investigator analyze upload.flow --method POST --pattern upload
```

### 例3: 新規ログインでの調査

```bash
# セッション復元なしでキャプチャ（認証フロー調査）
uv run python -m note_mcp.investigator capture --no-session -o auth.flow

# ブラウザでログイン操作を実行

# 認証関連のリクエストを分析
uv run python -m note_mcp.investigator analyze auth.flow --pattern "login\|session\|auth"
```

## CLIオプション一覧

### capture コマンド

| オプション | 短縮形 | デフォルト | 説明 |
|-----------|--------|-----------|------|
| `--output` | `-o` | `traffic.flow` | 出力ファイルパス |
| `--url` | `-u` | `https://note.com` | 初期表示URL |
| `--port` | `-p` | `8080` | プロキシポート |
| `--domain` | `-d` | なし | ドメインフィルタ |
| `--no-session` | - | `False` | セッション復元を無効化 |

### analyze コマンド

| オプション | 短縮形 | 説明 |
|-----------|--------|------|
| `--pattern` | `-p` | 正規表現パターンで検索 |
| `--domain` | `-d` | ドメインでフィルタ |
| `--method` | `-m` | HTTPメソッドでフィルタ |
| `--body` | `-b` | リクエスト/レスポンスボディを表示 |

### export コマンド

| オプション | 短縮形 | デフォルト | 説明 |
|-----------|--------|-----------|------|
| `--output` | `-o` | `traffic.json` | 出力JSONファイル |
| `--domain` | `-d` | なし | ドメインでフィルタ |

## MCPツール（AI自律調査用）

AI（Claude Code/Claude Desktop）がMCPツールを直接呼び出してAPI調査を自律実行できます。
Docker内でブラウザ操作とトラフィック分析が完結します。

### 前提条件

```bash
# Docker環境でinvestigatorサービスを起動
docker compose up -d investigator

# VNC経由でブラウザ動作を確認（オプション）
vncviewer localhost:5900
```

### キャプチャ制御ツール

#### investigator_start_capture

キャプチャセッションを開始します。

```
investigator_start_capture(domain: str, port: int = 8080) -> str
```

| パラメータ | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| domain | str | - | キャプチャ対象ドメイン（例: "api.note.com"） |
| port | int | 8080 | プロキシポート |

**戻り値**: セッション開始の成功/失敗メッセージ

#### investigator_stop_capture

キャプチャセッションを停止します。

```
investigator_stop_capture() -> str
```

**戻り値**: セッション終了の成功/失敗メッセージ

#### investigator_get_status

現在のキャプチャセッション状態を取得します。

```
investigator_get_status() -> str
```

**戻り値**: セッション状態（アクティブ/非アクティブ、キャプチャ済みリクエスト数など）

### ブラウザ操作ツール

#### investigator_navigate

指定URLに移動します。

```
investigator_navigate(url: str) -> str
```

| パラメータ | 型 | 説明 |
|-----------|-----|------|
| url | str | 移動先URL |

**戻り値**: ナビゲーション結果（成功/失敗、ページタイトル）

#### investigator_click

セレクタで指定した要素をクリックします。

```
investigator_click(selector: str) -> str
```

| パラメータ | 型 | 説明 |
|-----------|-----|------|
| selector | str | CSSセレクタ |

**戻り値**: クリック結果（成功/失敗）

#### investigator_type

指定要素にテキストを入力します。

```
investigator_type(selector: str, text: str) -> str
```

| パラメータ | 型 | 説明 |
|-----------|-----|------|
| selector | str | CSSセレクタ |
| text | str | 入力テキスト |

**戻り値**: 入力結果（成功/失敗）

#### investigator_screenshot

現在のページのスクリーンショットを取得します。

```
investigator_screenshot() -> str
```

**戻り値**: Base64エンコードされた画像データ

#### investigator_get_page_content

現在のページのHTMLを取得します。

```
investigator_get_page_content() -> str
```

**戻り値**: ページのHTMLコンテンツ

### トラフィック分析ツール

#### investigator_get_traffic

キャプチャしたトラフィック一覧を取得します。

```
investigator_get_traffic(pattern: str | None = None) -> str
```

| パラメータ | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| pattern | str | None | URLパターンでフィルタ（正規表現） |

**戻り値**: トラフィック一覧（JSON形式）

#### investigator_analyze

特定パターンのトラフィックを詳細分析します。

```
investigator_analyze(pattern: str, method: str | None = None) -> str
```

| パラメータ | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| pattern | str | - | URLパターン（正規表現） |
| method | str | None | HTTPメソッドでフィルタ |

**戻り値**: 分析結果（リクエスト/レスポンス詳細）

#### investigator_export

キャプチャデータをJSONファイルにエクスポートします。

```
investigator_export(output_path: str) -> str
```

| パラメータ | 型 | 説明 |
|-----------|-----|------|
| output_path | str | 出力ファイルパス |

**戻り値**: エクスポート結果（ファイルパス、レコード数）

### AI自律調査ワークフロー例

#### 例1: note.com記事作成APIの調査

```
# 1. キャプチャ開始
→ investigator_start_capture(domain="note.com")

# 2. note.comにアクセス
→ investigator_navigate("https://note.com/")

# 3. ログインボタンをクリック
→ investigator_click("button.login")

# 4. 認証情報を入力（セッション復元される場合は不要）
→ investigator_type("input[name=email]", "...")
→ investigator_type("input[name=password]", "...")
→ investigator_click("button[type=submit]")

# 5. 記事作成画面に移動
→ investigator_navigate("https://note.com/notes/new")

# 6. 記事内容を入力
→ investigator_click(".editor-content")
→ investigator_type(".editor-content", "テスト記事")

# 7. 下書き保存（APIリクエスト発生）
→ investigator_click("button.save-draft")

# 8. draft_save APIを分析
→ investigator_analyze(pattern="draft_save", method="POST")

# 9. 結果をエクスポート
→ investigator_export(output_path="api_investigation.json")

# 10. キャプチャ終了
→ investigator_stop_capture()
```

#### 例2: 画像アップロードAPIの調査

```
# 1. キャプチャ開始
→ investigator_start_capture(domain="note.com")

# 2. 記事編集画面に移動
→ investigator_navigate("https://note.com/notes/new")

# 3. 画像アップロードボタンをクリック
→ investigator_click("button.upload-image")

# 4. POSTリクエストを分析
→ investigator_analyze(pattern="upload", method="POST")

# 5. レスポンス形式を確認
→ investigator_get_traffic(pattern="upload")

# 6. キャプチャ終了
→ investigator_stop_capture()
```

## ホストClaude Codeからの自律調査

### アーキテクチャ

```
┌─────────────────────────────────────────────┐
│ Host                                        │
│  ┌─────────────────┐    ┌────────────────┐ │
│  │ Claude Code CLI │───►│ MCP Client     │ │
│  └─────────────────┘    └───────┬────────┘ │
└─────────────────────────────────┼───────────┘
                                  │ HTTP :9000
┌─────────────────────────────────┼───────────┐
│ Docker Container                ▼           │
│  ┌───────────────────────────────────────┐  │
│  │ Investigator MCP Server (FastMCP)    │  │
│  │ - investigator_start_capture          │  │
│  │ - investigator_navigate               │  │
│  │ - investigator_click                  │  │
│  │ - investigator_screenshot             │  │
│  │ - investigator_get_traffic            │  │
│  │ - investigator_analyze                │  │
│  └───────────────────────────────────────┘  │
│           │                                 │
│   ┌───────┴───────┐                        │
│   ▼               ▼                        │
│ ┌─────────┐  ┌───────────┐                 │
│ │mitmproxy│  │Playwright │                 │
│ │ :8080   │  │ Browser   │                 │
│ └─────────┘  └───────────┘                 │
│                  ▲                          │
│                  │ VNC :5900 / noVNC :6080 │
└──────────────────┼──────────────────────────┘
                   │
            [Visual Monitoring]
```

### セットアップ

#### 1. Dockerコンテナを起動

```bash
cd /home/driller/amplifier/note-mcp

# investigatorサービスを起動
docker compose up -d investigator

# ログを確認
docker compose logs -f investigator
```

#### 2. 接続確認

```bash
# MCP HTTPサーバーの動作確認
curl http://localhost:9000/mcp

# VNCでブラウザ確認（オプション）
vncviewer localhost:5900
# または noVNC: http://localhost:6080/vnc.html
```

#### 3. MCPクライアント設定

`.mcp.json` にHTTPトランスポート設定が追加済み：

```json
{
  "mcpServers": {
    "note-investigator": {
      "url": "http://localhost:9000/mcp",
      "transport": "http"
    }
  }
}
```

### 利用可能なポート

| ポート | サービス | 説明 |
|--------|----------|------|
| 9000 | MCP HTTP | Claude Codeからの接続 |
| 5900 | VNC | ブラウザ視覚確認 |
| 6080 | noVNC | Webブラウザ経由VNC |
| 8080 | mitmproxy | HTTPトラフィックキャプチャ |

### 技術的な注意事項

#### Docker内での動作

- mitmproxy、Playwright、MCPサーバーすべてがDocker内で動作
- VNC経由でブラウザ動作を視覚確認可能（port 5900）
- noVNCでブラウザ経由確認も可能（port 6080）

#### セッション管理

- Docker内ではkeyringが利用できないため、ファイルベースセッション管理を使用
- セッション情報は `/app/data` にマウントされたボリュームに永続化

#### HTTPS証明書

- `--ignore-certificate-errors` フラグでHTTPS通信をキャプチャ
- 証明書インストールは不要

#### Issue#15の教訓

- `subprocess.PIPE` → `subprocess.DEVNULL`（バッファブロッキング回避）
- `localhost` → `127.0.0.1`（WSL2互換性）

## トラブルシューティング

### mitmproxyが見つからない

```bash
# 開発依存関係をインストール
uv sync --group dev
```

### ブラウザが起動しない

```bash
# Playwrightブラウザをインストール
uv run playwright install chromium
```

### セッションが復元されない

1. `note_login` MCPツールで先にログイン
2. `note_check_auth` で認証状態を確認
3. それでも復元されない場合は `--no-session` で手動ログイン

### ポートが使用中

```bash
# 別のポートを使用
uv run python -m note_mcp.investigator capture --port 8888
```

### WSL2環境でのネットワーク問題

WSL2では `localhost` の名前解決が不安定な場合があります。
investigatorは内部で `127.0.0.1` を使用するよう修正済みですが、
他のツールと連携する際は `127.0.0.1` を明示的に使用してください。

### プロキシ経由でリクエストがタイムアウトする

過去に `subprocess.PIPE` によるバッファブロッキング問題がありました（Issue #15）。
現在は修正済みですが、同様の問題が発生した場合：

1. mitmproxyを直接起動してcurlでテスト
   ```bash
   uv run mitmdump --mode regular@8080 -w test.flow &
   curl -x http://127.0.0.1:8080 -k https://example.com
   ```
2. これが成功する場合、ProxyManagerのsubprocess処理に問題あり
3. 詳細は [Issue #15](https://github.com/drillan/note-mcp/issues/15) を参照

## 関連Issue

- [#15](https://github.com/drillan/note-mcp/issues/15) - subprocess.PIPEによるプロキシブロッキング問題
- [#14](https://github.com/drillan/note-mcp/issues/14) - 引用（blockquote）の出典入力機能

## 注意事項

- キャプチャデータにはセッション情報が含まれる可能性があるため、共有時は注意
- mitmproxyはHTTPSトラフィックを復号するため、開発・調査目的でのみ使用
- note.comの利用規約に従い、調査目的での使用に留める
