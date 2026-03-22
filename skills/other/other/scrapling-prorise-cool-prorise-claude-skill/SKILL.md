---
name: scrapling-web-scraper
description: 当需要使用 Scrapling 按站点特征自动选择抓取方式、绕过 Cloudflare 或 WAF、处理登录态页面、直接解析已有 HTML，或快速生成 Python 抓取脚本时使用。适用于“这个站有 Cloudflare”“要登录后抓取”“给我一个 Scrapling 脚本”“批量抓多个页面并保留会话”等场景。
---

<!-- AUTO-GENERATED-RESOURCE-MAP:START -->

### Resource Map

> 基准路径: `.claude/skills/scraping-specialist/references/domains/scrapling/`

```
scrapling/
├── assets/
│   └── templates/
│       ├── basic_fetch.py
│       ├── parse_only.py
│       ├── session_login.py
│       └── stealth_cloudflare.py
├── references/
│   ├── api-quick-ref.md
│   ├── cli-quick-ref.md
│   ├── site-patterns.md
│   └── troubleshooting.md
├── requirements.txt
└── SKILL.md
```

<!-- AUTO-GENERATED-RESOURCE-MAP:END -->

# Scrapling 抓取与反爬路线

此技能用于明确要走 `scrapling` 生态的场景，尤其适合“要快速写出 Python 抓取脚本”且目标站点可能存在反爬或登录态要求的任务。

## 先做环境检查

```bash
pip show scrapling
```

如果未安装，执行：

```bash
pip install "scrapling[fetchers]"
scrapling install
```

## 先选 Fetcher，再写脚本

不要直接盲写脚本。先按站点特征选路线：

- 已有 HTML，只需解析：用 `Selector`
- 静态页面、无明显反爬：用 `Fetcher`
- 需要 HTTP 表单登录并保留会话：用 `FetcherSession`
- 有 Cloudflare / WAF：优先 `StealthyFetcher`
- JS 渲染或 SPA：用 `DynamicFetcher`
- 不确定：先 `Fetcher`，失败后再升级到 `StealthyFetcher` 或 `DynamicFetcher`

## 推荐工作流

1. 先读取 [API 速查](references/api-quick-ref.md) 确认 fetcher 参数。
2. 再查 [站点模式经验库](references/site-patterns.md)，看目标站点是否已有经验。
3. 如果只想快速命令行试抓，读取 [CLI 速查](references/cli-quick-ref.md)。
4. 生成脚本时，优先复用 `assets/templates/` 下的模板。
5. 运行失败时，读取 [故障排查](references/troubleshooting.md)。

## 模板位置

- `assets/templates/basic_fetch.py`
- `assets/templates/parse_only.py`
- `assets/templates/session_login.py`
- `assets/templates/stealth_cloudflare.py`

## 使用规则

- 目标是产出能直接运行的 Python 脚本，而不是只给碎片代码。
- 浏览器型 fetcher 的 cookie 必须使用 `list[dict]` 格式。
- 不要把用户真实 cookie 或 token 写回仓库，只能临时本地使用。
