---
name: github-trending
description: GitHub Trending 探索与分析。用于发现热门开源项目、技术趋势、开发者偏好，帮助理解技术社区的兴趣走向。
---
# GitHub Trending 探索

## 核心能力

- **趋势发现** — 实时获取 GitHub Trending 仓库和开发者
- **技术洞察** — 分析热门项目背后的技术栈和架构
- **社区脉搏** — 理解开发者社区的兴趣偏好和需求
- **机会识别** — 发现潜在的开源贡献机会和学习方向

---

## 使用场景

| 场景 | 命令示例 |
|------|----------|
| 探索今日热门 | "看看今天 GitHub 上什么项目火了" |
| 语言趋势 | "Rust 最近有什么热门项目" |
| 领域研究 | "AI/ML 领域最近的趋势项目" |
| 竞品分析 | "看看有没有类似 X 的热门项目" |
| 技术选型 | "有什么热门的 React 组件库" |
| 学习方向 | "最近什么技术在快速增长" |

---

## 数据源

### Primary: GitHub Trending

```
https://github.com/trending                    # 总榜
https://github.com/trending/{language}         # 按语言
https://github.com/trending?since=daily        # 今日
https://github.com/trending?since=weekly       # 本周
https://github.com/trending?since=monthly      # 本月
https://github.com/trending/developers         # 热门开发者
```

### Secondary: GitHub API

```
# 搜索高星项目
https://api.github.com/search/repositories?q=stars:>1000+pushed:>2024-01-01&sort=stars

# 最近创建的热门项目
https://api.github.com/search/repositories?q=created:>2024-06-01+stars:>100&sort=stars
```

### Supplementary Sources

- **Hacker News** — https://news.ycombinator.com (Show HN)
- **Product Hunt** — https://producthunt.com (开发者工具)
- **Reddit** — r/programming, r/webdev, r/rust, r/golang
- **X/Twitter** — 技术热点讨论

---

## 分析框架

### 项目评估维度

```markdown
## 基础指标
- Stars / Star 增长速度
- Forks / Fork 活跃度
- Contributors 数量
- Issue/PR 活跃度
- 最近提交频率

## 质量指标
- README 完整度
- 文档质量
- 测试覆盖率
- CI/CD 配置
- License 类型

## 社区指标
- Issue 响应时间
- PR 合并效率
- Discussions 活跃度
- 社区友好度 (good first issue)

## 趋势指标
- Star 增长曲线 (线性/指数/爆发)
- 媒体曝光度
- 被 fork/依赖的情况
- 相关生态项目
```

### 趋势解读模板

```markdown
## 项目名称: {name}

### 一句话总结
{这个项目解决什么问题，为什么火}

### 核心数据
- Stars: X (本周 +Y)
- Language: Z
- Created: YYYY-MM-DD
- License: MIT/Apache/etc

### 为什么火
1. {原因1: 解决了什么痛点}
2. {原因2: 技术上有何创新}
3. {原因3: 社区/营销做得好}

### 技术亮点
- {亮点1}
- {亮点2}

### 适用场景
- {场景1}
- {场景2}

### 潜在风险/局限
- {风险1}
- {风险2}

### 相关/竞品项目
- {项目A}: 区别是...
- {项目B}: 区别是...
```

---

## 趋势分类

### 按热度类型

```markdown
## 1. 爆发型 (Viral)
- 特征: 短时间内 star 暴涨 (1天1000+)
- 原因: HN/Reddit 首页、名人推荐、解决热点问题
- 风险: 可能只是 hype，需观察持续性

## 2. 稳定增长型 (Steady)
- 特征: 持续稳定增长 (每天 10-100 stars)
- 原因: 真正解决问题，口碑传播
- 信号: 通常质量较高，值得关注

## 3. 周期型 (Cyclical)
- 特征: 随特定事件周期性上榜
- 例如: 年度总结类项目、面试题库
- 特点: 可预测，有特定时间窗口

## 4. 长尾型 (Long Tail)
- 特征: 低调但持续有用
- 原因: 特定领域的刚需工具
- 价值: 往往是真正的生产力工具
```

### 按项目类型

```markdown
## 工具类
- CLI 工具
- 开发者效率工具
- 系统工具

## 框架类
- Web 框架
- UI 组件库
- 测试框架

## AI/ML 类
- LLM 应用
- AI 工具链
- 模型相关

## 学习资源类
- Awesome 列表
- 教程/指南
- 面试准备

## 基础设施类
- 数据库
- 消息队列
- 监控运维
```

---

## 深度分析技巧

### 识别真正有价值的项目

```markdown
## 真正有价值的项目通常具备:
✓ 解决明确的痛点问题
✓ 有清晰的使用场景
✓ 代码质量高，架构合理
✓ 文档完善，易于上手
✓ 维护活跃，响应及时
✓ 社区友好，欢迎贡献

## 可能只是 Hype 的信号:
✗ 只有 README，代码很少
✗ 概念大于实现
✗ Star 多但 Fork 少
✗ Issue 积压严重
✗ 只有一个维护者
✗ 没有实际使用案例
```

### 预测潜力项目

```markdown
## 早期信号
- 知名开发者/公司背书
- 解决新兴技术的痛点
- 独特的技术方案
- 清晰的 Roadmap
- 活跃的早期社区

## 增长潜力判断
1. 市场: 目标用户群体大小
2. 竞争: 是否有强力竞品
3. 技术: 是否有护城河
4. 团队: 维护者背景和投入
5. 生态: 是否容易集成
```

---

## 技术趋势追踪

### 2024-2025 热点领域

```markdown
## AI/LLM 工具链
- RAG 框架 (LangChain, LlamaIndex)
- Agent 框架 (AutoGPT, CrewAI)
- 本地 LLM (Ollama, llama.cpp)
- AI Code Assistant

## Rust 生态爆发
- 系统工具 Rust 重写
- Web 框架 (Axum, Actix)
- 前端工具链 (SWC, Turbopack)

## Developer Experience
- AI 辅助开发
- 开发环境容器化
- 类型安全全栈

## 边缘计算
- Edge Runtime (Cloudflare Workers, Deno Deploy)
- WASM 应用

## 可观测性
- OpenTelemetry 生态
- eBPF 工具
```

### 语言趋势

```markdown
## 上升趋势
- Rust: 系统编程、WebAssembly
- Go: 云原生、CLI 工具
- TypeScript: 全栈开发、类型安全
- Zig: 系统编程新秀

## 稳定主流
- Python: AI/ML、脚本
- JavaScript: Web 开发
- Java/Kotlin: 企业后端

## 特定领域
- Swift: Apple 生态
- C#: 游戏、Windows
- Elixir: 高并发系统
```

---

## 输出格式

### 趋势日报

```markdown
# GitHub Trending 日报 - {date}

## 今日亮点
{简短总结今日最值得关注的趋势}

## 热门项目 TOP 5

### 1. {project_name} ⭐ {stars} (+{daily_increase})
> {one_line_description}

**语言**: {language} | **License**: {license}
**为什么火**: {reason}
**适合谁**: {target_audience}

[GitHub]({url}) | [Demo]({demo_url})

---

### 2. ...

## 技术趋势观察
- {trend_observation_1}
- {trend_observation_2}

## 值得关注的新项目
{刚起步但有潜力的项目}

## 本周回顾
{如果是周末，加入周总结}
```

### 领域深度报告

```markdown
# {领域} 技术趋势报告

## 概述
{领域现状和趋势概述}

## 主流方案对比

| 项目 | Stars | 特点 | 适用场景 |
|------|-------|------|----------|
| A    | 10k   | ...  | ...      |
| B    | 8k    | ...  | ...      |

## 技术演进
{技术发展脉络}

## 选型建议
{根据不同需求的推荐}

## 未来展望
{预测未来发展方向}
```

---

## 实践建议

### 如何利用 Trending

```markdown
## 学习
- 阅读热门项目源码
- 学习最佳实践
- 了解新技术方向

## 贡献
- 寻找 good first issue
- 提交 bug fix
- 完善文档

## 灵感
- 发现创业/产品机会
- 技术选型参考
- 解决方案借鉴

## 社交
- 关注活跃开发者
- 参与技术讨论
- 建立行业联系
```

### 避免的陷阱

```markdown
✗ 不要盲目追热点
✗ 不要只看 star 数
✗ 不要忽视项目成熟度
✗ 不要低估维护成本
✗ 不要忽略社区活跃度
```

---

## 工具推荐

### 趋势追踪

- **GitHub Trending** — 官方趋势榜
- **Star History** — https://star-history.com
- **OSS Insight** — https://ossinsight.io
- **GitHunt** — 每日推送热门项目

### 项目分析

- **Repobeats** — 仓库活跃度分析
- **Snyk Advisor** — 安全和维护评分
- **Libraries.io** — 依赖关系分析

### 开发者洞察

- **GitHub Profile README** — 了解开发者
- **Git Awards** — 开发者排名
- **Commit History** — 了解项目演进
