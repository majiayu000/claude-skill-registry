---
name: web-debug-pro
description: 高级浏览器调试工具，支持网络抓包、性能分析、DOM 检查、反爬虫测试。使用 browser-use CLI 提供专业级浏览器调试能力。
version: 1.0
allowed-tools: Bash(browser-use:*), Bash(curl:*)
---

# Web Debug Pro

专业级浏览器调试工具，基于 `browser-use` CLI 实现高级调试功能。

## 功能模块

| 模块 | 功能 | 本地 | 云端 |
|------|------|------|------|
| **网络分析** | 抓包、请求/响应分析、HAR 导出 | ✅ | ✅ |
| **性能审计** | Lighthouse 风格报告、Core Web Vitals | ✅ | ✅ |
| **DOM 调试** | 元素检查、事件监听、JS 执行 | ✅ | ✅ |
| **反爬虫测试** | UA 检测、Cloudflare 绕过、自动化检测 | ✅ | ✅ |

## 前置条件

确保 `browser-use` 已安装并配置：

```bash
browser-use doctor
```

## 核心工作流

### 1. 网络分析

```bash
# 打开页面并获取网络信息
browser-use open <url>
browser-use eval "
  performance.getEntriesByType('resource').map(r => ({
    name: r.name,
    type: r.initiatorType,
    duration: r.duration,
    size: r.transferSize
  }))
"
```

### 2. 性能审计

```bash
# 获取导航时序
browser-use eval "
  const nav = performance.getEntriesByType('navigation')[0];
  ({
    dns: nav.domainLookupEnd - nav.domainLookupStart,
    tcp: nav.connectEnd - nav.connectStart,
    ttfb: nav.responseStart - nav.requestStart,
    download: nav.responseEnd - nav.responseStart,
    domReady: nav.domContentLoadedEventEnd - nav.fetchStart,
    load: nav.loadEventEnd - nav.fetchStart
  })
"
```

### 3. DOM 调试

```bash
# 获取页面状态
browser-use state

# 检查元素
browser-use get html --selector "#element-id"

# 执行 JavaScript
browser-use eval "document.querySelector('form').outerHTML"
```

### 4. 反爬虫检测

```bash
# 检测自动化特征
browser-use eval "
  ({
    webdriver: navigator.webdriver,
    chrome: !!window.chrome,
    cdc: !!window.document.$cdc_,
    languages: navigator.languages,
    platform: navigator.platform
  })
"

# 使用真实浏览器配置
browser-use --browser real --profile "Default" open <url>
```

## 高级用法

### JavaScript 错误捕获

```bash
browser-use eval "
  window.__errors = [];
  window.onerror = (msg, url, line) => {
    window.__errors.push({msg, url, line});
  };
  'Error listener installed'
"
```

### 网络请求监控

```bash
browser-use python "
  # 在 Python 模式下设置网络拦截
  browser.setup_network_monitor()
"
```

### 性能指标采集

```bash
browser-use eval "
  ({
    fcp: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
    lcp: performance.getEntriesByType('largest-contentful-paint')[0]?.startTime,
    cls: performance.getEntriesByType('layout-shift').reduce((a, e) => a + e.value, 0)
  })
"
```

## 测试用例示例

### 表单填写测试

```bash
# 打开页面
browser-use open http://localhost:8000
browser-use state

# 填写表单（使用 state 返回的索引）
browser-use select <gender-index> "男"
browser-use input <year-index> "2001"
browser-use input <month-index> "9"
browser-use input <day-index> "15"
browser-use select <hour-index> "6"
browser-use click <submit-index>

# 验证结果
browser-use wait text "八字排盘"
browser-use screenshot result.png
```

### API 响应分析

```bash
# 执行 API 请求并分析
browser-use eval "
  (async () => {
    const res = await fetch('/api/chart/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({gender:'男', birth_year:2001, birth_month:9, birth_day:15, birth_hour:6})
    });
    return {status: res.status, headers: Object.fromEntries(res.headers)};
  })()
"
```

## 反爬虫深度指南

### 检测方法详解

| 检测类型 | 检测方式 | 风险等级 |
|----------|----------|----------|
| `navigator.webdriver` | 检查是否为 `true` | 高 |
| User-Agent | 检测 "HeadlessChrome" 字符串 | 高 |
| WebGL 指纹 | vendor 返回 "Brian Paul" 或 "Mesa OffScreen" | 中 |
| plugins 长度 | 检测 plugins 数组和类型 | 中 |
| 自动化特征 | 检测 `$cdc_`、`__webdriver_evaluate` 等 | 高 |

### 绕过技术方案

#### 1. 使用真实浏览器模式
```bash
# 推荐：使用真实 Chrome + 现有配置
browser-use --browser real --profile "Default" open <url>
```

#### 2. 云端 Stealth 浏览器
```bash
# browser-use Cloud 自动处理 stealth
browser-use --browser remote open <url>
```

#### 3. 注入反检测脚本
```bash
browser-use eval "
  // 隐藏 webdriver
  Object.defineProperty(navigator, 'webdriver', {get: () => undefined});

  // 修改 languages
  Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en', 'zh-CN']});

  // 修改 WebGL renderer
  const getParam = WebGLRenderingContext.prototype.getParameter;
  WebGLRenderingContext.prototype.getParameter = function(p) {
    if (p === 37445) return 'Intel Inc.';
    if (p === 37446) return 'Intel Iris OpenGL Engine';
    return getParam.call(this, p);
  };

  // 模拟 Chrome runtime
  window.chrome = {runtime: {}};

  'Stealth scripts applied'
"
```

### 主要反爬虫系统

| 系统 | 检测方式 | 绕过难度 |
|------|----------|----------|
| Cloudflare | JS 挑战 + 行为分析 + Turnstile | 高 |
| reCAPTCHA v3 | 无交互评分 (0.0-1.0) | 中 |
| reCAPTCHA v2 | Checkbox/Invisible | 中 |

## 浏览器模式

```bash
# 本地 Chromium（快速、隔离）
browser-use --browser chromium open <url>

# 本地真实 Chrome（使用登录会话，推荐用于反爬虫）
browser-use --browser real --profile "Default" open <url>

# 云端浏览器（绕过 IP 限制，自动 stealth）
browser-use --browser remote open <url>
```

## 参考资源

- [browser-use CLI 文档](https://github.com/browser-use/browser-use)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [MDN Performance API](https://developer.mozilla.org/en-US/docs/Web/API/Performance)
- [playwright-stealth](https://github.com/AtuboDad/playwright-stealth)
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)
- [Bot Detection Test](https://bot.sannysoft.com/)

### 页面加载问题

```bash
browser-use close --all
browser-use --headed open <url>  # 显示浏览器窗口调试
```

### 元素未找到

```bash
browser-use state
browser-use scroll down
browser-use state  # 再次检查
```

## 清理

```bash
browser-use close              # 关闭当前会话
browser-use close --all        # 关闭所有会话
browser-use session stop --all # 停止云会话
```

## 工具脚本

本 skill 包含以下 Python 工具脚本：

| 脚本 | 功能 | 用法示例 |
|------|------|----------|
| `tools/network-analyzer.py` | 网络分析 | `python network-analyzer.py timing` |
| `tools/performance-audit.py` | 性能审计 | `python performance-audit.py report` |
| `tools/dom-inspector.py` | DOM 检查 | `python dom-inspector.py element "form"` |
| `tools/anti-bot-tester.py` | 反爬虫测试 | `python anti-bot-tester.py scan` |

### 工具使用示例

```bash
# 网络时序分析
python ~/skills/web-debug-pro/tools/network-analyzer.py timing

# 性能报告
python ~/skills/web-debug-pro/tools/performance-audit.py report

# 反爬虫扫描
python ~/skills/web-debug-pro/tools/anti-bot-tester.py scan

# DOM 元素检查
python ~/skills/web-debug-pro/tools/dom-inspector.py element "#chartForm"
```

## 测试报告

### 天机阁项目测试结果

**测试环境**: FastAPI 后端 + 单页前端，运行在 `http://localhost:8000`

| 测试项 | 结果 | 详情 |
|--------|------|------|
| 服务健康检查 | ✅ 通过 | `/health` 返回 `{"status":"ok"}` |
| API 文档访问 | ✅ 通过 | `/docs` Swagger UI 正常 |
| 排盘 API | ✅ 通过 | POST `/api/chart/` 返回正确八字数据 |
| 性能测试 | ✅ 通过 | API 响应时间 ~500ms |

**示例 API 响应**:
```json
{
  "id": 19,
  "bazi": "辛巳 丁酉 辛巳 辛卯",
  "day_master": "辛",
  "day_master_wx": "金",
  "strength": "身弱",
  "ming_palace": "巳",
  "ju": 4
}
```

## 参考资源

- [browser-use CLI 文档](https://github.com/browser-use/browser-use)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [MDN Performance API](https://developer.mozilla.org/en-US/docs/Web/API/Performance)