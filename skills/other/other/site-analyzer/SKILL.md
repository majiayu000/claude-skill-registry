---
name: site-analyzer
description: 大型商业网站深度分析工具。基于 neo 项目理念，通过被动捕获 + 主动探索 + 视觉理解，完整解析网站操作逻辑。支持 API 逆向、模式提取、知识库生成。
version: 1.1
allowed-tools: Bash(neo:*), Bash(browser-use:*), Bash(curl:*), Bash(jq:*)
---

# Site Analyzer

大型商业网站深度分析框架，整合三种分析方式：
- **被动捕获** - neo Chrome 扩展拦截所有 API 流量
- **主动探索** - browser-use 进行交互式测试
- **视觉理解** - VL 模型辅助页面语义分析

## 完成标准

触发此 skill 时，任务完成必须满足：
- [ ] 至少捕获 50 个 API 请求
- [ ] API Schema 已生成（OpenAPI 格式）
- [ ] 关键流程已识别（登录/核心操作）
- [ ] 知识库 SKILL.md 已生成

## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| Chrome 连接失败 | 检查 CDP 端口，重启浏览器 |
| 扩展未捕获 | 重新加载扩展，检查权限 |
| API 解析失败 | 手动标注，跳过复杂 schema |
| 超时 | 增加 capture 时间或分批处理 |

## Token 效率优化

- 分批捕获（每批 100 请求）
- 压缩 API 输出（仅保留关键字段）
- 分页生成知识库

```bash
# 压缩 API 列表输出
neo capture list target-site.com --limit 20 --json | \
  jq '[.[] | {method, path, status, has_body}]'
```

## Orchestrator-Workers 模式

复杂网站分析采用分工协作：

```
┌─────────────────┐
│   Orchestrator  │  协调分析任务
└────────┬────────┘
         │
    ┌────┼────┐
    ▼    ▼    ▼
┌──────┐ ┌──────┐ ┌──────┐
│捕获层│ │分析层│ │生成层│
└──────┘ └──────┘ └──────┘
   │        │        │
   ▼        ▼        ▼
 neo     flows    SKILL.md
 capture  deps    openapi.yaml
```

### Orchestrator 职责

```bash
# 主控脚本
analyze_site() {
  local site="$1"
  mkdir -p "site-analysis/$site"

  # Phase 1: 捕获（可并行）
  neo capture start "$site" &
  capture_pid=$!

  # Phase 2: 分析（依赖捕获）
  wait $capture_pid
  neo schema generate "$site" > "site-analysis/$site/schema.json"
  neo flows "$site" > "site-analysis/$site/flows.json"

  # Phase 3: 生成
  neo export-skill "$site" > "site-analysis/$site/SKILL.md"
}
```

### Workers 分工

| Worker | 工具 | 输出 |
|--------|------|------|
| 捕获 Worker | neo capture | traffic.har |
| 分析 Worker | neo flows/deps | flows.json, deps.json |
| 生成 Worker | neo export-skill | SKILL.md, openapi.yaml |

## 核心理念

```
用户操作 → Neo 捕获 API → Schema 自动生成 → 知识库输出
    ↓           ↓              ↓
 UI 探索   → 数据流分析   → 可复用 Skill
    ↓           ↓              ↓
 VL 理解   → 模式提取     → 测试用例
```

## 前置条件

### 1. 安装 neo CLI

```bash
# 克隆并安装
git clone https://github.com/4ier/neo.git
cd neo && npm install && npm run build
npm link  # 使 neo 命令全局可用

# 加载 Chrome 扩展
# 1. 打开 chrome://extensions
# 2. 启用"开发者模式"
# 3. 点击"加载已解压的扩展程序" → 选择 extension/dist/
```

### 2. 安装 browser-use

```bash
npm install -g browser-use
browser-use doctor
```

### 3. 配置 VL 模型

环境变量已在 `~/.config/fish/config.fish` 中配置：
- `DASHSCOPE_API_KEY` ✅
- `DASHSCOPE_BASE_URL` ✅

## 工作流

### Phase 1: 捕获阶段

```bash
# 启动 neo 并连接浏览器
neo connect 9222

# 打开目标网站
neo open https://target-site.com

# 开始捕获（扩展自动运行）
# 浏览网站，执行各种操作...

# 查看捕获状态
neo status
neo capture summary
```

### Phase 2: 分析阶段

```bash
# 列出捕获的 API 调用
neo capture list target-site.com --limit 20

# 生成 API Schema
neo schema generate target-site.com

# 分析 API 流程
neo flows target-site.com

# 发现数据依赖
neo deps target-site.com

# 语义标签
neo label target-site.com
```

### Phase 3: 知识生成

```bash
# 导出 OpenAPI 规范
neo schema openapi target-site.com > api-spec.yaml

# 生成 Agent Skill
neo export-skill target-site.com > SKILL.md

# 发现可复用工作流
neo workflow discover target-site.com
```

## 命令详解

### 捕获命令

```bash
# 实时监控
neo capture watch target-site.com

# 按时间过滤
neo capture list target-site.com --since 2h

# 搜索特定 API
neo capture search "CreateTweet" --method POST

# 导出为 HAR
neo capture export target-site.com --format har > traffic.har

# 统计分析
neo capture stats target-site.com
```

### API 重放

```bash
# 重放捕获的请求
neo replay <capture-id> --tab target-site.com

# 执行新请求
neo exec <url> --method POST \
  --body '{"key":"value"}' \
  --tab target-site.com \
  --auto-headers

# 智能 API 调用（自动查找 schema）
neo api target-site.com HomeTimeline
```

### UI 自动化

```bash
# 获取页面快照（accessibility tree）
neo snapshot

# 交互操作
neo click @1
neo fill @2 "search query"
neo press Enter

# 截图
neo screenshot page.png --full --annotate
```

## 分析模板

### 电商网站分析

```bash
# 1. 捕获购物流程
neo open https://shop.example.com
# 浏览商品 → 加购物车 → 结算 → 支付

# 2. 分析关键 API
neo capture list shop.example.com --since 1h
neo flows shop.example.com

# 3. 提取商品 API
neo capture search "product" --method GET
neo capture search "cart" --method POST

# 4. 生成知识库
neo schema generate shop.example.com
neo export-skill shop.example.com
```

### SaaS 平台分析

```bash
# 1. 捕获认证流程
neo open https://app.example.com/login
# 登录操作...

# 2. 分析认证 API
neo capture list app.example.com --since 30m
neo label app.example.com

# 3. 发现工作流
neo workflow discover app.example.com
neo workflow show <workflow-name>
```

### API 密集型应用

```bash
# 1. 监控所有 API 调用
neo capture watch api-app.com

# 2. 分析 API 依赖
neo deps api-app.com --min-confidence 2

# 3. 生成 OpenAPI 规范
neo schema openapi api-app.com > openapi.yaml
```

## 与其他 Skills 协作

### 配合 visual-analyzer

```bash
# VL 模型分析页面布局
python ~/skills/visual-analyzer/tools/page-analyzer.py \
  --url https://target-site.com \
  --output analysis.json

# 结合 neo 捕获的数据
neo capture list target-site.com --json > api-data.json

# 合并分析结果
python ~/skills/knowledge-generator/tools/merge-analysis.py \
  --visual analysis.json \
  --api api-data.json \
  --output final-report.md
```

### 配合 api-pattern-extractor

```bash
# 提取 API 模式
python ~/skills/api-pattern-extractor/tools/extract-patterns.py \
  --schema $(neo schema show target-site.com --json) \
  --output patterns.yaml
```

## 输出结构

```
site-analysis/
├── captures/           # 原始捕获数据
│   ├── traffic.har
│   └── captures.json
├── schemas/           # API Schema
│   ├── schema.json
│   └── openapi.yaml
├── analysis/          # 分析结果
│   ├── flows.json
│   ├── deps.json
│   └── labels.json
├── knowledge/         # 知识库
│   ├── SKILL.md
│   └── workflows/
└── tests/            # 测试用例
    └── test-cases.yaml
```

## 高级技巧

### 1. 自动化探索脚本

```bash
#!/bin/bash
# auto-explore.sh

TARGET=$1

neo open "https://$TARGET"
neo snapshot > "snapshots/home.json"

# 点击主要导航
neo snapshot | jq -r '.[] | select(.role == "link") | .@ref' | head -10 | while read ref; do
  neo click "$ref"
  sleep 2
  neo snapshot > "snapshots/nav-$ref.json"
  neo capture list "$TARGET" --since 5m >> "captures/session.log"
done
```

### 2. API 依赖图生成

```bash
# 生成依赖图
neo deps target-site.com --format dot > deps.dot
dot -Tpng deps.dot -o deps.png
```

### 3. Mock 服务器

```bash
# 基于捕获创建 mock 服务器
neo mock target-site.com --port 8080 --latency 100
```

## 故障排除

### Chrome 连接问题

```bash
# 检查 CDP 端点
neo discover

# 重新连接
neo connect 9222
```

### 扩展未捕获数据

```bash
# 检查扩展状态
neo doctor

# 重新加载扩展
neo reload

# 手动注入
neo inject --persist
```

## 参考资源

- [neo 项目](https://github.com/4ier/neo)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [browser-use CLI](https://github.com/browser-use/browser-use)