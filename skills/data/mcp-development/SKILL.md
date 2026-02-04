---
name: mcp-development
description: MCPサーバー開発を支援します。プロトコル準拠、Pydanticスキーマ設計、Playwright統合のベストプラクティスを提供します。
allowed-tools: Read Edit Write Glob Grep Bash
---

# MCP Development スキル

このスキルは、**Constitution Article 3: MCP Protocol Compliance** を支援し、MCPサーバー開発のベストプラクティスを提供します。

## 起動条件

以下の状況で起動します：

1. **MCPツール実装時**: 新しいMCPツールを追加する際
2. **スキーマ設計時**: 入出力スキーマを定義する際
3. **Playwright統合時**: ブラウザ自動化を実装する際
4. **セッション管理実装時**: 認証状態を管理する際
5. **エラーハンドリング設計時**: MCPエラーレスポンスを設計する際

## MCPプロトコル要件

### ツール定義

MCPツールは以下の構造を持つ必要があります：

```python
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

class CreateDraftInput(BaseModel):
    """下書き作成の入力パラメータ"""
    title: str = Field(..., description="記事のタイトル")
    body: str = Field(..., description="記事の本文（Markdown形式）")
    tags: list[str] | None = Field(None, description="記事のタグ一覧")

# ツール定義
create_draft_tool = Tool(
    name="create_draft",
    description="note.comに記事の下書きを作成します",
    inputSchema=CreateDraftInput.model_json_schema(),
)
```

### Pydanticモデル設計

**必須ルール**:

1. **すべての入力パラメータはPydanticモデルで検証**
2. **Fieldに説明を必ず付与**
3. **型アノテーションを明確に指定**

```python
from pydantic import BaseModel, Field, field_validator

class ArticleContent(BaseModel):
    """記事コンテンツのスキーマ"""
    title: str = Field(..., min_length=1, max_length=200, description="記事タイトル")
    body: str = Field(..., min_length=1, description="記事本文")
    status: str = Field("draft", pattern="^(draft|published)$", description="記事状態")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("タイトルは空にできません")
        return v.strip()
```

### エラーレスポンス

MCPエラーは適切な形式で返す必要があります：

```python
from mcp.types import TextContent, ErrorData
from mcp.shared.exceptions import McpError

class NoteApiError(McpError):
    """note.com API関連のエラー"""
    pass

class AuthenticationError(NoteApiError):
    """認証エラー"""
    def __init__(self, message: str = "認証が必要です"):
        super().__init__(ErrorData(code=-32001, message=message))

class SessionExpiredError(NoteApiError):
    """セッション期限切れエラー"""
    def __init__(self):
        super().__init__(ErrorData(
            code=-32002,
            message="セッションの有効期限が切れました。再ログインしてください。"
        ))
```

## Playwright統合

### ブラウザライフサイクル管理

```python
from playwright.async_api import async_playwright, Browser, Page
from contextlib import asynccontextmanager

class BrowserManager:
    """ブラウザインスタンスのライフサイクル管理"""

    def __init__(self) -> None:
        self._browser: Browser | None = None
        self._page: Page | None = None

    async def get_page(self) -> Page:
        """既存のページを再利用、なければ新規作成"""
        if self._page is not None and not self._page.is_closed():
            return self._page

        if self._browser is None:
            playwright = await async_playwright().start()
            self._browser = await playwright.chromium.launch(headless=False)

        self._page = await self._browser.new_page()
        return self._page

    async def close(self) -> None:
        """リソースのクリーンアップ"""
        if self._page:
            await self._page.close()
        if self._browser:
            await self._browser.close()
```

### 作業ウィンドウの再利用

```python
async def show_preview(self, article_id: str) -> None:
    """プレビューを表示（既存ウィンドウを再利用）"""
    page = await self.browser_manager.get_page()

    # 既にプレビューページにいる場合はリロード
    current_url = page.url
    preview_url = f"https://note.com/api/v1/text_notes/{article_id}/preview"

    if current_url == preview_url:
        await page.reload()
    else:
        await page.goto(preview_url)
```

## セッション管理

### セキュアなセッション保存

OSのキーチェーン/資格情報マネージャーを使用：

```python
import keyring
from dataclasses import dataclass
from datetime import datetime
import json

SERVICE_NAME = "note-mcp"

@dataclass
class Session:
    """セッション情報"""
    cookies: dict[str, str]
    user_id: str
    expires_at: datetime

    def is_valid(self) -> bool:
        """セッションが有効かチェック"""
        return datetime.now() < self.expires_at

def save_session(session: Session) -> None:
    """セッションをセキュアに保存"""
    keyring.set_password(
        SERVICE_NAME,
        "session",
        json.dumps({
            "cookies": session.cookies,
            "user_id": session.user_id,
            "expires_at": session.expires_at.isoformat(),
        })
    )

def load_session() -> Session | None:
    """保存されたセッションを読み込み"""
    data = keyring.get_password(SERVICE_NAME, "session")
    if data is None:
        return None

    parsed = json.loads(data)
    session = Session(
        cookies=parsed["cookies"],
        user_id=parsed["user_id"],
        expires_at=datetime.fromisoformat(parsed["expires_at"]),
    )

    if not session.is_valid():
        keyring.delete_password(SERVICE_NAME, "session")
        return None

    return session
```

### セッション期限切れ処理

```python
async def execute_with_session(self, operation: Callable) -> Any:
    """セッションを確認して操作を実行"""
    session = load_session()

    if session is None:
        raise AuthenticationError("ログインが必要です")

    if not session.is_valid():
        raise SessionExpiredError()

    try:
        return await operation()
    except SessionExpiredError:
        # セッションをクリアして再認証を促す
        keyring.delete_password(SERVICE_NAME, "session")
        raise
```

## 実装チェックリスト

### MCPツール作成時

- [ ] Pydanticモデルで入力を定義
- [ ] Fieldに説明を付与
- [ ] ツール定義にdescriptionを記載
- [ ] 適切なエラーレスポンスを実装

### Playwright統合時

- [ ] ブラウザライフサイクルを管理
- [ ] 作業ウィンドウを再利用
- [ ] クリーンアップ処理を実装
- [ ] エラー時のリカバリを考慮

### セッション管理時

- [ ] OSのセキュアストレージを使用
- [ ] 有効期限チェックを実装
- [ ] 期限切れ時のエラーメッセージを明確に
- [ ] 再認証フローを提供

## 参考リソース

- MCP Protocol仕様: https://modelcontextprotocol.io/
- Pydantic v2ドキュメント: https://docs.pydantic.dev/
- Playwright Pythonドキュメント: https://playwright.dev/python/

## 注意事項

- note.comの非公式APIを使用するため、仕様変更で動作しなくなる可能性あり
- レート制限を遵守（目安: 10リクエスト/分）
- 自己責任・無保証での公開を前提
