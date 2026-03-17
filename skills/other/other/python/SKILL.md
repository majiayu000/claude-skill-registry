---
name: backend-development-python
description: |
  Python后端开发专家。精通FastAPI、Django、Flask等框架，以及Pydantic、SQLModel、Alembic、Playwright等Python生态最佳实践。

  适用场景：
  - 现代异步API (FastAPI)
  - 企业级全栈应用 (Django)
  - 轻量级微服务 (Flask)
  - 数据库ORM (SQLModel/SQLAlchemy)
  - 数据验证 (Pydantic)
  - 数据库迁移 (Alembic)
  - 浏览器自动化 (Playwright)
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# 🐍 Python 后端开发专家

老王我最爱Python了！这语言写起来真tm爽！

## 技术栈全景

```
┌─────────────────────────────────────────────────────────────┐
│                    Python 后端技术栈                          │
├─────────────────────────────────────────────────────────────┤
│  Web框架                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ FastAPI │  │ Django  │  │ Flask   │  │ Tornado │        │
│  │ 现代    │  │ 企业级  │  │ 轻量级  │  │ 高并发  │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
├─────────────────────────────────────────────────────────────┤
│  数据层                                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │SQLModel │  │SQLAlchemy│ │ Tortoise│  │ Beanie  │        │
│  │ 新一代  │  │ 经典ORM │  │ 异步ORM │  │ MongoDB │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
├─────────────────────────────────────────────────────────────┤
│  数据验证                                                    │
│  ┌─────────┐  ┌─────────┐                                    │
│  │ Pydantic│  │ Msgspec │                                    │
│  │ 类型验证│  │ 超快速  │                                    │
│  └─────────┘  └─────────┘                                    │
├─────────────────────────────────────────────────────────────┤
│  浏览器自动化                                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                      │
│  │Playwright│ │ Selenium│ │ Scrapy  │                      │
│  │ 现代首选│  │ 经典    │  │ 爬虫框架│                      │
│  └─────────┘  └─────────┘  └─────────┘                      │
├─────────────────────────────────────────────────────────────┤
│  数据库迁移                                                  │
│  ┌─────────┐  ┌─────────┐                                    │
│  │ Alembic │  │ Aerich  │                                    │
│  │ 经典    │  │ FastAPI  │                                    │
│  └─────────┘  └─────────┘                                    │
├─────────────────────────────────────────────────────────────┤
│  认证授权                                                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┘                       │
│  │  JWT    │  │ OAuth2  │  │ FastAPI  │                       │
│  │ 无状态  │  │ 第三方  │  │ 安全工具 │                       │
│  └─────────┘  └─────────┘  └─────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

---

## FastAPI - 现代Python API首选

### 项目结构（最佳实践）

```
my_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # 配置管理
│   │   ├── security.py      # 认证相关
│   │   └── deps.py          # 依赖注入
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # SQLModel模型
│   │   └── post.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Pydantic Schema
│   │   └── post.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # API依赖
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py    # 路由聚合
│   │       └── endpoints/
│   │           ├── users.py
│   │           ├── auth.py
│   │           └── posts.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py  # 业务逻辑
│   │   └── auth_service.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py       # 数据库会话
│   │   └── init_db.py       # 初始化
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── alembic/                 # 数据库迁移
│   ├── versions/
│   └── env.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api/
├── .env.example
├── pyproject.toml
└── README.md
```

### 核心：Pydantic V2 + SQLModel

```python
# models/user.py
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    name: str
    is_active: bool = True
    is_superuser: bool = False

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    posts: list["Post"] = Relationship(back_populates="author")

# schemas/user.py
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr | None = None

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

### 完整的CRUD Service模式

```python
# services/user_service.py
from typing import Optional, List
from sqlmodel import Session, select, col
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, session: Session):
        self.session = session

    async def get(self, user_id: int) -> User | None:
        """获取单个用户"""
        return self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        """通过邮箱获取用户"""
        stmt = select(User).where(User.email == email)
        return self.session.exec(stmt).first()

    async def get_multi(
        self, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """获取用户列表"""
        stmt = select(User).offset(skip).limit(limit)
        return self.session.exec(stmt).all()

    async def create(self, user_in: UserCreate) -> User:
        """创建用户"""
        # 检查邮箱是否已存在
        existing = await self.get_by_email(user_in.email)
        if existing:
            raise ValueError("邮箱已被注册")

        # 创建用户
        user = User.model_validate(
            user_in.model_dump(),
            update={
                "hashed_password": get_password_hash(user_in.password)
            }
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    async def update(
        self, user: User, user_in: UserUpdate
    ) -> User:
        """更新用户"""
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        user.updated_at = datetime.utcnow()
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        """删除用户"""
        self.session.delete(user)
        self.session.commit()

    async def authenticate(
        self, email: str, password: str
    ) -> User | None:
        """验证用户登录"""
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
```

### JWT认证 + OAuth2

```python
# core/security.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status

SECRET_KEY = "your-secret-key-here"  # 从环境变量读取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """生成密码hash"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """创建JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict | None:
    """验证JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# core/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.db.session import get_session
from app.models.user import User
from app.core.security import verify_token
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    """获取当前登录用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user_service = UserService(session)
    user = await user_service.get(user_id)
    if user is None:
        raise credentials_exception

    return user
```

### 完整的API端点

```python
# api/v1/endpoints/users.py
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.api.deps import get_current_user
from app.core.deps import get_session
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """获取用户列表"""
    service = UserService(session)
    return await service.get_multi(skip, limit)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    return current_user

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_in: UserCreate,
    session: Session = Depends(get_session)
):
    """创建用户"""
    service = UserService(session)
    return await service.create(user_in)

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """更新用户"""
    service = UserService(session)
    user = await service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return await service.update(user, user_in)
```

---

## Playwright - 浏览器自动化首选

老王我用过的最tm好用的浏览器自动化工具！

### 安装

```bash
# 安装playwright
pip install playwright

# 安装浏览器驱动（必须！）
playwright install
# 或者只安装特定浏览器
playwright install chromium
playwright install firefox
playwright install webkit
```

### 基础用法

```python
from playwright.sync_api import sync_playwright

# 同步API
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=True为无头模式
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    browser.close()

# 异步API（性能更好，推荐！）
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://example.com")
        print(await page.title())
        await browser.close()

asyncio.run(main())
```

### 常见操作

```python
from playwright.async_api import async_playwright

async def browser_operations():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 ..."  # 自定义UA
        )
        page = await context.new_page()

        # 导航
        await page.goto("https://example.com", wait_until="networkidle")  # wait_until: load, domcontentloaded, networkidle
        await page.go_back()
        await page.go_forward()
        await page.reload()

        # 查找元素（多种选择器）
        await page.click("button#submit")           # CSS
        await page.click("text=登录")                # 文本
        await page.click("xpath=//button[@id='submit']")  # XPath
        await page.click("data-testid=submit")      # data属性

        # 输入框操作
        await page.fill("input[name='email']", "user@example.com")
        await page.type("input[name='email']", "user@example.com", delay=100)  # 模拟打字
        await page.clear("input[name='email']")

        # 下拉框
        await page.select_option("select#country", "China")

        # 复选框/单选框
        await page.check("input#agree")
        await page.uncheck("input#subscribe")

        # 上传文件
        await page.set_input_files("input[type='file']", "path/to/file.pdf")

        # 获取元素属性
        text = await page.inner_text("div.content")
        html = await page.inner_html("div.content")
        attr = await page.get_attribute("a#link", "href")

        # 等待
        await page.wait_for_selector("div.result", timeout=5000)
        await page.wait_for_url("**/success")
        await page.wait_for_timeout(1000)  # 硬等待（不推荐）

        # 执行JavaScript
        result = await page.evaluate("() => document.title")
        value = await page.evaluate("el => el.value", await page.query_selector("input"))

        # 截图
        await page.screenshot(path="screenshot.png")
        await page.pdf(path="page.pdf")  # 只有chromium支持

        # 处理弹窗
        async with page.expect_popup() as popup_info:
            await page.click("a[target='_blank']")
        popup = await popup_info.value
        await popup.wait_for_load_state()

        # 处理对话框
        async with page.expect_dialog() as dialog_info:
            await page.click("button")
        dialog = await dialog_info.value
        await dialog.accept()  # 或 dialog.dismiss()

        await browser.close()

asyncio.run(browser_operations())
```

### 网页爬虫实战

```python
import asyncio
from playwright.async_api import async_playwright
from typing import List
import json

class Scraper:
    def __init__(self):
        self.results = []

    async def scrape_page(self, url: str) -> dict:
        """爬取单个页面"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # 拦截请求，只加载必要资源（加速）
            await page.route("**/*.{png,jpg,jpeg,gif,svg,css,woff,woff2}", lambda route: route.abort())
            await page.goto(url, wait_until="domcontentloaded")

            # 等待数据加载
            await page.wait_for_selector(".item")

            # 提取数据
            items = await page.query_selector_all(".item")
            data = []
            for item in items:
                title = await item.query_selector(".title")
                price = await item.query_selector(".price")
                data.append({
                    "title": await title.inner_text() if title else "",
                    "price": await price.inner_text() if price else "",
                })

            await browser.close()
            return {"url": url, "data": data}

    async def scrape_multiple(self, urls: List[str]) -> List[dict]:
        """并发爬取多个页面"""
        tasks = [self.scrape_page(url) for url in urls]
        return await asyncio.gather(*tasks)

# 使用
async def main():
    scraper = Scraper()
    urls = [
        "https://example.com/page/1",
        "https://example.com/page/2",
        "https://example.com/page/3",
    ]
    results = await scraper.scrape_multiple(urls)
    print(json.dumps(results, ensure_ascii=False, indent=2))

asyncio.run(main())
```

### 表单自动填写

```python
from playwright.async_api import async_playwright

async def auto_fill_form():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)  # slow_mo模拟人类操作速度
        page = await browser.new_page()

        await page.goto("https://example.com/register")

        # 填写表单
        await page.fill("input#name", "张三")
        await page.fill("input#email", "zhangsan@example.com")
        await page.fill("input#password", "password123")
        await page.fill("input#password-confirm", "password123")

        # 选择性别（单选框）
        await page.check("input[value='male']")

        # 选择兴趣（复选框）
        await page.check("input[value='reading']")
        await page.check("input[value='coding']")

        # 选择城市（下拉框）
        await page.select_option("select#city", "Beijing")

        # 上传头像
        await page.set_input_files("input#avatar", "avatar.jpg")

        # 同意条款
        await page.check("input#agree")

        # 提交前验证
        await page.wait_for_selector("button[type='submit']:not([disabled])")

        # 提交
        async with page.expect_response("**/api/register") as response_info:
            await page.click("button[type='submit']")
        response = await response_info.value

        if response.ok:
            print("注册成功！")
        else:
            print(f"注册失败：{await response.text()}")

        await page.wait_for_timeout(2000)  # 看到结果
        await browser.close()

asyncio.run(auto_fill_form())
```

### 处理登录和Session

```python
from playwright.async_api import async_playwright

async def login_and_scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # 创建context（相当于浏览器配置文件，可保存cookies）
        context = await browser.new_context()
        page = await context.new_page()

        # 登录
        await page.goto("https://example.com/login")
        await page.fill("input#email", "user@example.com")
        await page.fill("input#password", "password123")
        await page.click("button[type='submit']")

        # 等待登录成功（跳转到首页或特定元素出现）
        await page.wait_for_url("**/dashboard")
        # 或者
        await page.wait_for_selector(".user-avatar")

        # 保存session状态（下次可以直接使用）
        await context.storage_state(path="auth.json")

        # 之后的所有请求都带登录状态
        await page.goto("https://example.com/protected-page")
        content = await page.inner_text(".protected-content")
        print(content)

        # 恢复已有session
        # context = await browser.new_context(storage_state="auth.json")

        await browser.close()

asyncio.run(login_and_scrape())
```

### 反爬虫对策

```python
from playwright.async_api import async_playwright
import random

async def stealth_browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',  # 隐藏自动化特征
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
            # 随机User-Agent
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."
        )

        # 注入脚本隐藏webdriver特征
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        page = await context.new_page()

        # 随机延迟模拟人类操作
        async def human_click(selector: str):
            await page.wait_for_selector(selector)
            await page.wait_for_timeout(random.randint(500, 2000))
            await page.click(selector)

        # 随机延迟模拟人类输入
        async def human_type(selector: str, text: str):
            await page.wait_for_selector(selector)
            await page.click(selector)
            for char in text:
                await page.type(selector, char, delay=random.randint(50, 200))

        # 使用
        await page.goto("https://example.com")
        await human_type("input#search", "Python")
        await human_click("button#search-btn")

        await browser.close()

asyncio.run(stealth_browser())
```

### 测试框架集成

```python
# tests/test_login.py
import pytest
from playwright.async_api import async_playwright, Page

@pytest.fixture
async def browser_page():
    """每个测试独立的browser和page"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        yield page
        await browser.close()

@pytest.mark.asyncio
async def test_login_success(browser_page: Page):
    """测试登录成功"""
    await browser_page.goto("https://example.com/login")

    await browser_page.fill("input#email", "test@example.com")
    await browser_page.fill("input#password", "password123")
    await browser_page.click("button[type='submit']")

    # 等待跳转到dashboard
    await browser_page.wait_for_url("**/dashboard")

    # 验证登录成功
    assert await browser_page.inner_text(".user-name") == "Test User"

@pytest.mark.asyncio
async def test_login_failure(browser_page: Page):
    """测试登录失败"""
    await browser_page.goto("https://example.com/login")

    await browser_page.fill("input#email", "test@example.com")
    await browser_page.fill("input#password", "wrongpassword")
    await browser_page.click("button[type='submit']")

    # 验证错误提示
    error_msg = await browser_page.inner_text(".error-message")
    assert "密码错误" in error_msg or "用户不存在" in error_msg
```

### Playwright最佳实践

```python
from playwright.async_api import async_playwright, BrowserContext
from typing import AsyncGenerator

# 1. 使用Context Pool管理多个会话
class ContextPool:
    def __init__(self, max_contexts: int = 5):
        self.contexts: list[BrowserContext] = []
        self.max_contexts = max_contexts

    async def get_context(self, browser) -> BrowserContext:
        if self.contexts:
            return self.contexts.pop()
        if len(self.contexts) < self.max_contexts:
            return await browser.new_context()
        raise Exception("No available contexts")

    async def return_context(self, context: BrowserContext):
        if len(self.contexts) < self.max_contexts:
            self.contexts.append(context)
        else:
            await context.close()

# 2. 使用Page Object模式
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.email_input = "input#email"
        self.password_input = "input#password"
        self.submit_button = "button[type='submit']"

    async def login(self, email: str, password: str):
        await self.page.fill(self.email_input, email)
        await self.page.fill(self.password_input, password)
        await self.page.click(self.submit_button)

# 3. 重试机制
from functools import wraps
import asyncio

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    await asyncio.sleep(delay * (attempt + 1))
            return wrapper
    return decorator

@retry(max_attempts=3)
async def fragile_operation(page):
    await page.goto("https://flaky-site.com")
    return await page.title()
```

---

## Alembic 数据库迁移

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

# 导入所有模型
from app.models.user import User
from app.models.post import Post

# this is the Alembic Config object
config = context.config

# 设置数据库URL
config.set_main_option("sqlalchemy.url", "postgresql://...")

# 解析模型
target_metadata = SQLModel.metadata

# ...其余Alembic配置

# 创建迁移
# alembic revision --autogenerate -m "创建用户表"

# 执行迁移
# alembic upgrade head

# 回滚迁移
# alembic downgrade -1
```

---

## 性能优化技巧

### 1. 使用异步ORM

```python
# Tortoise ORM - 异步高性能
from tortoise import Tortoise, fields

class User(fields.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    posts: fields.ReverseRelation["Post"]

# 初始化
await Tortoise.init(
    db_url="postgres://...",
    modules={"models": ["app.models"]}
)

# 查询
user = await User.get(email="user@example.com")
posts = await user.posts.all()
```

### 2. 连接池配置

```python
# db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    "postgresql+asyncpg://...",
    echo=False,
    pool_size=20,           # 连接池大小
    max_overflow=0,         # 最大溢出连接数
    pool_pre_ping=True,     # 连接前检查
    pool_recycle=3600,      # 连接回收时间
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

### 3. 使用Redis缓存

```python
import redis.asyncio as redis
from functools import wraps
import json

redis_client = await redis.from_url("redis://localhost")

def cache(ttl: int = 3600, key_prefix: str = ""):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存key
            cache_key = f"{key_prefix}:{args}:{kwargs}"

            # 尝试从缓存获取
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # 执行原函数
            result = await func(*args, **kwargs)

            # 存入缓存
            await redis_client.setex(
                cache_key, ttl, json.dumps(result, default=str)
            )

            return result
        return wrapper
    return decorator

# 使用
@cache(ttl=1800, key_prefix="user")
async def get_user(user_id: int):
    return await User.get(id=user_id)
```

---

## 依赖推荐（pyproject.toml）

```toml
[project]
dependencies = [
    # Web框架
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",

    # 数据验证
    "pydantic>=2.6.0",
    "pydantic-settings>=2.1.0",
    "email-validator>=2.1.0",

    # 数据库
    "sqlmodel>=0.0.14",
    "sqlalchemy>=2.0.25",
    "asyncpg>=0.29.0",         # PostgreSQL异步驱动
    "alembic>=1.13.0",

    # 认证
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.6",

    # 浏览器自动化
    "playwright>=1.40.0",

    # 工具
    "redis>=5.0.1",
    "httpx>=0.26.0",           # 异步HTTP客户端
    "celery>=5.3.0",           # 任务队列
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "pytest-playwright>=0.4.0",  # Playwright测试插件
    "httpx>=0.26.0",           # 测试客户端
    "black>=24.0.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]
```

---

**老王建议**：
- 新项目直接用 FastAPI + SQLModel + Pydantic V2
- 大型后台管理用 Django（开发快）
- 高并发场景考虑 Tornado + 异步ORM
- 浏览器自动化直接上 Playwright，别tm用Selenium了
- Playwright异步API性能更好，优先使用
- 别tm忘了写类型注解，Python 3.12+类型提示很香！
