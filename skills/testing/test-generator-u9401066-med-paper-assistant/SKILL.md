---
name: test-generator
description: 生成測試套件。觸發：test、測試、寫測試、coverage、覆蓋率、pytest、unittest、驗證、TG、unit test、整合測試、e2e、static、ruff、mypy、lint。
---

# 測試生成技能

## 測試金字塔

```
    /\  E2E (少量)
   /--\ Integration (中等)
  /----\ Unit (大量)
 /------\ Static Analysis (基礎)
```

---

## 靜態分析工具 (Static Analysis)

### 工具總覽

| 工具 | 用途 | 命令 |
|------|------|------|
| **ruff** | Linter + Formatter | `uv run ruff check src/` |
| **mypy** | 類型檢查 | `uv run mypy src/ --ignore-missing-imports` |
| **bandit** | 安全漏洞掃描 | `uv run bandit -r src/ -ll` |
| **vulture** | 死代碼檢測 | `uv run vulture src/ --min-confidence 80` |

### Bandit 安全掃描

```bash
# 只顯示 Medium+ 嚴重度 (推薦)
uv run bandit -r src/ -ll

# 顯示所有問題 (包含 Low)
uv run bandit -r src/ -l

# 常見 nosec 註解
# nosec B110 - 有意的 try_except_pass
# nosec B404 - 有意使用 subprocess
# nosec B603 - 信任的 subprocess 呼叫
# nosec B607 - 信任的部分路徑執行
```

### Vulture 死代碼檢測

```bash
# 80% 置信度以上
uv run vulture src/ --min-confidence 80

# 產生 whitelist（排除誤報）
uv run vulture src/ --make-whitelist > vulture_whitelist.py
```

### Ruff 配置 (pyproject.toml)

```toml
[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "SIM"]
ignore = ["E501"]  # 行長由 formatter 處理

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # 允許 re-export
"tests/**" = ["S101"]  # 允許 assert

[tool.ruff.format]
quote-style = "double"
```

### Mypy 配置 (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
no_implicit_optional = true

[[tool.mypy.overrides]]
module = ["mcp.*", "docx.*", "PyPDF2.*"]
ignore_missing_imports = true
```

### 靜態分析執行流程

```bash
# 1. Ruff 自動修復 (先執行)
uv run ruff check src/ --fix --unsafe-fixes
uv run ruff format src/

# 2. Mypy 類型檢查
uv run mypy src/ --ignore-missing-imports

# 3. Bandit 安全掃描
uv run bandit -r src/ -ll

# 4. Vulture 死代碼檢測 (可選)
uv run vulture src/ --min-confidence 80

# 完整一次執行
uv run ruff check src/; uv run mypy src/ --ignore-missing-imports; uv run bandit -r src/ -ll
```
uv run mypy src/ --ignore-missing-imports

# 3. 安全掃描 (可選)
uv run bandit -r src/ -ll
```

### 常見 Mypy 錯誤修復

| 錯誤 | 解法 |
|------|------|
| `no_implicit_optional` | `def foo(x: str = None)` → `def foo(x: Optional[str] = None)` |
| `var-annotated` | `results = []` → `results: List[T] = []` |
| `arg-type` | 檢查 Optional 是否需要 `or default` |
| `return-value` | 確保函數返回類型與聲明一致 |
| `call-overload` | 使用 `# type: ignore[call-overload]` |

---

## Python 測試工具

| 層級 | 工具 | 配置 |
|------|------|------|
| Static | `mypy`, `ruff`, `bandit` | pyproject.toml |
| Unit | `pytest` | tests/unit/ |
| Integration | `pytest` + `httpx` | tests/integration/ |
| E2E | `playwright` | tests/e2e/ |
| Coverage | `pytest-cov` | 目標 ≥80% |

---

## 目錄結構

```
tests/
├── conftest.py          # 共用 fixtures
├── unit/                # 單元測試
│   └── test_domain/
├── integration/         # 整合測試
│   └── test_api/
└── e2e/                 # 端對端測試
```

---

## 單元測試模式

### 必須涵蓋
1. **Happy Path** - 正常流程
2. **Edge Cases** - 邊界條件
3. **Error Handling** - 錯誤處理
4. **Null/None** - 空值處理

### 範例結構
```python
class TestUser:
    def test_create_user_valid(self):          # Happy path
        ...
    def test_create_user_min_length(self):     # Edge case
        ...
    def test_create_user_empty_raises(self):   # Error handling
        with pytest.raises(ValidationError):
            ...
    @pytest.mark.parametrize(...)              # 多參數測試
    def test_variations(self, input, expected):
        ...
```

---

## 整合測試模式

### API 測試
```python
@pytest.mark.integration
async def test_create_endpoint(async_client):
    response = await async_client.post("/api/users", json={...})
    assert response.status_code == 201
```

### DB 測試
```python
@pytest.mark.integration
async def test_save_and_retrieve(repository, db_session):
    saved = await repository.save(entity)
    retrieved = await repository.get_by_id(saved.id)
    assert retrieved is not None
```

---

## 常用 Fixtures

```python
# conftest.py
@pytest.fixture
def sample_user():
    return User(name="Test", email="test@test.com")

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app) as client:
        yield client

@pytest_asyncio.fixture
async def db_session():
    async with AsyncSession() as session:
        yield session
        await session.rollback()
```

---

## 執行命令

```bash
# 靜態分析
mypy src/
ruff check src/

# 單元測試
pytest tests/unit -v

# 整合測試
pytest tests/integration -v -m integration

# 全部 + 覆蓋率
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# E2E
pytest tests/e2e -v --headed  # 顯示瀏覽器
```

---

## pyproject.toml 配置

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = ["unit", "integration", "e2e", "slow"]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

---

## 生成 Checklist

- [ ] 確認測試目錄結構
- [ ] Happy path 測試
- [ ] Edge cases 測試
- [ ] Error handling 測試
- [ ] Fixtures 設定
- [ ] CI workflow 整合
- [ ] 覆蓋率 ≥ 80%

---

## 相關技能

- `code-reviewer` - 審查測試品質
