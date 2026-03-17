---
name: tdd-workflow
description: TDDワークフローを強制し、テストファースト開発を支援します。新機能実装時に自動起動し、Red-Green-Refactorサイクルを確実に実行します。
allowed-tools: Read Edit Write Glob Grep Bash
---

# TDD Workflow スキル

このスキルは、**Constitution Article 1: Test-First Imperative** を強制し、テスト駆動開発（TDD）ワークフローを支援します。

## 起動条件

以下の状況で自動起動します：

1. **新機能実装開始時**: 新しい機能の実装を開始する際
2. **バグ修正開始時**: バグを修正する際（再現テストを先に作成）
3. **リファクタリング開始時**: 既存コードの改善前にテストを確認

## TDDサイクル

### Phase 1: Red（テスト作成・失敗確認）

**目的**: 失敗するテストを先に作成する

1. **テストファイルの作成/特定**
   - ファイル命名規則: `test_<機能名>.py`
   - 配置場所: `tests/` ディレクトリ

2. **テストケースの設計**
   - 期待する動作を明確に定義
   - エッジケースを考慮
   - 失敗する理由を明確に

3. **テストの実行と失敗確認**
   ```bash
   uv run pytest tests/test_<機能名>.py -v
   ```

4. **ユーザー承認**
   - テストケースをユーザーに提示
   - 承認を得てから次のフェーズへ

### Phase 2: Green（最小限の実装）

**目的**: テストを通過する最小限のコードを実装する

1. **実装ファイルの作成**
   - テストを通過させることのみに集中
   - 過剰な設計を避ける

2. **テストの実行と成功確認**
   ```bash
   uv run pytest tests/test_<機能名>.py -v
   ```

3. **品質チェック**
   ```bash
   uv run ruff check --fix . && uv run ruff format . && uv run mypy .
   ```

### Phase 3: Refactor（リファクタリング）

**目的**: テストを維持しながらコードを改善する

1. **コードの改善**
   - 重複の除去
   - 可読性の向上
   - パフォーマンスの最適化

2. **テストの再実行**
   ```bash
   uv run pytest tests/test_<機能名>.py -v
   ```

3. **全テストの確認**
   ```bash
   uv run pytest
   ```

## テスト構成の原則

### ファイル対応

| 実装ファイル | テストファイル |
|-------------|--------------|
| `src/auth.py` | `tests/test_auth.py` |
| `src/article.py` | `tests/test_article.py` |
| `src/session.py` | `tests/test_session.py` |

### テストクラス構成

```python
# tests/test_auth.py
import pytest

class TestLogin:
    """ログイン機能のテスト"""

    def test_login_success(self) -> None:
        """正常なログインが成功すること"""
        ...

    def test_login_invalid_credentials(self) -> None:
        """無効な認証情報でエラーになること"""
        ...


class TestLogout:
    """ログアウト機能のテスト"""

    def test_logout_success(self) -> None:
        """正常なログアウトが成功すること"""
        ...
```

### テスト命名規則

- `test_<機能>_<状況>_<期待結果>`
- 例: `test_login_with_valid_credentials_returns_session`

## ワークフロー例

### 例1: 新しいログイン機能の実装

**Step 1: テスト作成（Red）**

```python
# tests/test_auth.py
import pytest
from src.auth import login

class TestLogin:
    def test_login_success(self) -> None:
        """正常なログインが成功すること"""
        result = login("valid_user", "valid_password")
        assert result.success is True
        assert result.session_id is not None

    def test_login_invalid_password(self) -> None:
        """無効なパスワードでエラーになること"""
        with pytest.raises(AuthenticationError):
            login("valid_user", "wrong_password")
```

**Step 2: テスト失敗確認**

```bash
uv run pytest tests/test_auth.py -v
# FAILED - ImportError: cannot import name 'login' from 'src.auth'
```

**Step 3: ユーザー承認**

「このテストケースで進めてよろしいですか？」

**Step 4: 最小実装（Green）**

```python
# src/auth.py
from dataclasses import dataclass

@dataclass
class LoginResult:
    success: bool
    session_id: str | None

class AuthenticationError(Exception):
    pass

def login(username: str, password: str) -> LoginResult:
    if password == "wrong_password":
        raise AuthenticationError("Invalid credentials")
    return LoginResult(success=True, session_id="session_123")
```

**Step 5: テスト成功確認**

```bash
uv run pytest tests/test_auth.py -v
# PASSED
```

**Step 6: リファクタリング（Refactor）**

必要に応じてコードを改善

## 注意事項

- **テストなしの実装は禁止**: Article 1 は非交渉的原則
- **テストの承認は必須**: ユーザー承認なしに実装を進めない
- **テストカバレッジ**: 主要なパスとエッジケースをカバー
- **モック使用**: 外部依存はモックを使用して単体テストを実現

## チェックリスト

実装開始前に確認：

- [ ] テストファイルが存在するか
- [ ] テストが失敗状態（Red）であることを確認したか
- [ ] ユーザーがテストケースを承認したか

実装完了時に確認：

- [ ] すべてのテストがパス（Green）しているか
- [ ] 品質チェック（ruff, mypy）がパスしているか
- [ ] 不要なコードがないか（リファクタリング完了）
