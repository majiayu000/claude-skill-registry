---
name: mcp-tools
description: 使用 FastMCP 框架开发交易相关的 MCP 工具, 包括交易所 API 集成(币安/OKX等)、行情数据获取、订单管理等.当需要创建 MCP 服务器或交易工具时触发此技能.
---

# FastMCP 交易工具开发指南

## 概述

本技能指导使用 [FastMCP](https://github.com/jlowin/fastmcp) 框架开发交易相关的 MCP (Model Context Protocol) 工具.

- **官方文档**: https://gofastmcp.com
- **GitHub**: https://github.com/jlowin/fastmcp
- **API 参考**: 见 `reference/fastmcp-api.md`

---

## 快速开始

### 依赖安装

```bash
uv add fastmcp httpx pydantic
```

### 最小示例

```python
from fastmcp import FastMCP

mcp = FastMCP("trading_mcp")

@mcp.tool
async def get_price(symbol: str) -> str:
    """获取价格"""
    # 实现逻辑
    pass

if __name__ == "__main__":
    mcp.run()
```

---

## 项目结构

```
trading_mcp/
├── server.py           # MCP 服务器入口
├── tools/
│   ├── __init__.py
│   ├── market.py       # 行情数据工具
│   ├── account.py      # 账户信息工具
│   ├── order.py        # 订单管理工具
│   └── analysis.py     # 分析工具
├── models/
│   ├── __init__.py
│   └── schemas.py      # Pydantic 模型定义
├── utils/
│   ├── __init__.py
│   ├── client.py       # API 客户端
│   └── errors.py       # 错误处理
└── pyproject.toml
```

---

## 环境变量加载 (重要)

MCP 服务器必须在启动时主动加载 `.env` 文件, 因为 MCP 进程不会自动继承 shell 环境变量.

```python
from pathlib import Path
from dotenv import load_dotenv

# 必须在模块顶部、其他 os.environ 调用之前加载 .env
_project_root = Path(__file__).parent.parent
load_dotenv(_project_root / ".env")
```

**关键点:**
- `load_dotenv()` 必须在任何 `os.environ.get()` 之前调用
- 使用绝对路径定位 `.env` 文件, 避免工作目录问题
- 修改 `.env` 后需要**重启 MCP 服务器**才能生效

---

## 安全要求 (重要)

```python
import os

# API 密钥必须使用环境变量, 禁止硬编码!
API_KEY = os.environ.get("BINANCE_API_KEY")
API_SECRET = os.environ.get("BINANCE_API_SECRET")

if not API_KEY or not API_SECRET:
    raise ValueError("BINANCE_API_KEY 和 BINANCE_API_SECRET 环境变量必须设置")
```

### .env 文件示例

```bash
# 项目根目录 .env 文件
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
COINANK_API_KEY=your_coinank_key

# 模拟交易模式 (默认开启, 防止误操作)
TRADING_SIMULATION=true
```

---

## 开发规范

### 命名规范

- 服务器名称: `{exchange}_mcp` (如 `binance_mcp`, `okx_mcp`)
- 工具名称: `{exchange}_{action}_{target}` (如 `binance_get_price`, `okx_place_order`)
- 使用 snake_case

### 工具分类

| 类型 | 说明 | readOnlyHint | destructiveHint |
|------|------|--------------|-----------------|
| 行情查询 | 价格、K线、深度 | true | false |
| 账户查询 | 余额、持仓 | true | false |
| 下单操作 | 开仓、平仓 | false | true |
| 订单管理 | 撤单、修改 | false | true |

### 错误处理

```python
import httpx

def handle_api_error(e: Exception) -> str:
    """统一错误处理 - 必须提供清晰、可操作的错误信息"""
    if isinstance(e, httpx.HTTPStatusError):
        status = e.response.status_code
        error_messages = {
            400: "请求参数错误, 请检查交易对符号是否正确",
            401: "API 认证失败, 请检查 API Key 配置",
            403: "权限不足, 请检查 API Key 权限设置",
            429: "请求频率过高, 请稍后重试",
            418: "IP 被临时封禁, 请等待解封",
            500: "交易所服务器错误, 请稍后重试"
        }
        return f"Error: {error_messages.get(status, f'API 请求失败, 状态码 {status}')}"
    elif isinstance(e, httpx.TimeoutException):
        return "Error: 请求超时, 请重试"
    return f"Error: {type(e).__name__}: {str(e)}"
```

---

## 运行与测试

### 启动服务器

```bash
# stdio 模式 (默认, 用于本地工具)
python server.py

# HTTP 模式 (用于远程服务)
python -c "from server import mcp; mcp.run(transport='http', port=8000)"
```

### 使用 MCP Inspector 测试

```bash
npx @modelcontextprotocol/inspector python server.py
```

---

## 支持的交易所

| 交易所 | 现货 | 合约 | API 文档 |
|--------|------|------|----------|
| Binance | Yes | Yes | https://binance-docs.github.io/apidocs |
| OKX | Yes | Yes | https://www.okx.com/docs-v5 |
| Bybit | Yes | Yes | https://bybit-exchange.github.io/docs |
| Bitget | Yes | Yes | https://bitgetlimited.github.io/apidoc |

---

## 参考资料

- **FastMCP API 参考**: `reference/fastmcp-api.md`
- FastMCP 官方文档: https://gofastmcp.com
- MCP 协议规范: https://modelcontextprotocol.io
