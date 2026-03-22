---
description: 提供数据库设计、优化、数据工程和数据分析能力。当需要处理数据库操作、数据管道或数据分析时使用。
name: data-specialist
---
# Data Specialist

提供数据库设计、优化、数据工程和数据分析能力。当需要处理数据库操作、数据管道或数据分析时使用。

## Skill Index

<!-- AUTO-GENERATED-SKILL-INDEX:START -->
以下索引由 `node scripts/update-skill-index.js` 自动生成，用于让 Claude 在顶层专家触发后继续路由到最相关的子技能。

### Claude 使用说明

1. 先将用户当前任务与每个子技能的 `触发语义` 进行语义匹配，不要只看目录名。
2. 一旦找到最相关的子技能，立即打开其 `入口文件` 指向的 `SKILL.md`，把它作为下一层入口。
3. 进入子技能后，再根据该子技能自己的说明按需加载同目录下的 `references/`、`scripts/`、`assets/`，不要在顶层专家中预先展开大段细节。
4. 如果多个子技能都相关，先加载最贴近主目标的那个，再按需补充其他子技能，避免一次性加载过多上下文。
5. 下方 `入口文件` 路径相对于项目根目录，可直接用于 `Read` 操作。

### 子技能索引

#### data-consolidation-agent (1)
- `data-consolidation-agent`
  - 触发语义: AI agent that consolidates extracted sales data into live reporting dashboards with territory, rep, and pipeline summaries
  - 入口文件: `.claude/skills/data-specialist/references/domains/data-consolidation-agent/SKILL.md`

#### data-engineer (1)
- `data-engineer`
  - 触发语义: Expert data engineer specializing in building reliable data pipelines, lakehouse architectures, and scalable data infrastructure. Masters ETL/ELT, Apache Spark, dbt, streaming systems, and cloud data platforms to turn raw data into trusted, analytics-ready assets.
  - 入口文件: `.claude/skills/data-specialist/references/domains/data-engineer/SKILL.md`

#### database-optimizer (1)
- `database-optimizer`
  - 触发语义: Expert database specialist focusing on schema design, query optimization, indexing strategies, and performance tuning for PostgreSQL, MySQL, and modern databases like Supabase and PlanetScale.
  - 入口文件: `.claude/skills/data-specialist/references/domains/database-optimizer/SKILL.md`

#### sales-data-extraction-agent (1)
- `sales-data-extraction-agent`
  - 触发语义: AI agent specialized in monitoring Excel files and extracting key sales metrics (MTD, YTD, Year End) for internal live reporting
  - 入口文件: `.claude/skills/data-specialist/references/domains/sales-data-extraction-agent/SKILL.md`

<!-- AUTO-GENERATED-SKILL-INDEX:END -->

## Notes

- 顶层 `SKILL.md` 仅做索引导航，不承载大体量细节内容。
- 详细资料下沉到 `references/domains/`，按树形结构组织。
