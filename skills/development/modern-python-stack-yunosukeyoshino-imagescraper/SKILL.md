---
name: modern-python-stack
description: Astral社製ツール（uv, Ruff, ty）でPython開発環境を構築。プロジェクト作成、依存関係管理、コード品質改善、CI/CD設定時に使用。
---

# Modern Python Stack

Astral社製Rustツールを中心とした高速Python開発環境。

## 技術スタック

| カテゴリ | ツール | 用途 |
|---------|--------|------|
| パッケージ管理 | **uv** | pip代替（10-100倍高速） |
| リンター/フォーマッター | **Ruff** | flake8/black/isort統合 |
| 型チェッカー | **ty** | mypy代替（約7倍高速） |
| 依存性制御 | **import-linter** | アーキテクチャ境界強制 |
| コミット前チェック | **pre-commit** | 自動品質担保 |

## 🔄 セットアップワークフロー

新規プロジェクト作成時はこのチェックリストで進捗を追跡：

```
セットアップ進捗:
- [ ] Step 1: uv初期化
- [ ] Step 2: 開発依存追加
- [ ] Step 3: Ruff設定
- [ ] Step 4: pre-commit設定
- [ ] Step 5: 動作確認
```

**Step 1: uv初期化**
```bash
uv init
uv sync
```

**Step 2: 開発依存追加**
```bash
uv add --dev ruff ty pre-commit pytest
```

**Step 3: Ruff設定（pyproject.tomlに追加）**
```toml
[tool.ruff]
line-length = 120
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.ruff.lint.isort]
force-single-line = true
```

**Step 4: pre-commit設定**
```bash
uv run pre-commit install
```

**Step 5: 動作確認**
```bash
uv run ruff check .
uv run ty check src/
uv run pytest
```

確認が失敗した場合は、Step 3に戻って設定を修正。

---

## コマンドリファレンス

### uv（パッケージ管理）
```bash
uv sync                    # 依存同期
uv add package             # 追加
uv add --dev package       # 開発依存追加
uv run script.py           # 実行（常にuv run経由）
```

### Ruff（リント/フォーマット）
```bash
uv run ruff check .        # リント
uv run ruff check --fix .  # 自動修正
uv run ruff format .       # フォーマット
```

### ty（型チェック）
```bash
uv run ty check src/       # 型チェック
```

エラー抑制: `# ty: ignore[rule-name]`

---

## 原則

### 【MUST】必須
- `uv`をパッケージ管理に使用（pip禁止）
- `pyproject.toml`で依存関係を一元管理
- 行長は`120`文字
- importは`force-single-line = true`
- `pre-commit`をセットアップ

### 【SHOULD】推奨
- `uv.lock`をgitにコミット（再現性確保）
- `ty`を型チェックに使用
- アーキテクチャ境界を`import-linter`で強制

---

## Anti-Patterns

- ❌ `pip install`の使用
- ❌ `python script.py`の直接実行（`uv run`経由で）
- ❌ 複数の設定ファイル（`.flake8`, `.isort.cfg`等）→ pyproject.tomlに統合

## References

詳細設定は以下を参照:
- [REFERENCE.md](REFERENCE.md) - 設定テンプレート、CUDA対応、import-linter
- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [ty (Astral)](https://github.com/astral-sh/ty)
