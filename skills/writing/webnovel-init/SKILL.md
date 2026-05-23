---
name: webnovel-init
description: Initializes webnovel projects with settings, outline framework, and state.json. Supports quick/standard/deep modes. Activates when user wants to start a new novel or /webnovel-init.
allowed-tools: Bash Write Read Edit AskUserQuestion Task
---

# Project Initialization Skill

## Workflow Checklist

```
项目初始化进度：
- [ ] Phase 1: 模式确定 + 基础资料加载
- [ ] Phase 2: 题材选择（两轮）
- [ ] Phase 3: 基本信息收集
- [ ] Phase 4: 金手指设计 (Standard+)
- [ ] Phase 5: 世界构建 (Standard+)
- [ ] Phase 6: 创意深挖 (Deep)
- [ ] Phase 7: 生成项目文件
- [ ] Phase 8: 验证并报告
```

---

## Phase 1: 模式确定 + 基础资料

### 1.1 加载基础资料（必须执行）

```bash
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/genre-tropes.md"
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/system-data-flow.md"
```

### 1.2 确定初始化模式

**[AskUserQuestion Round 1]**

| 问题 | 选项 |
|------|------|
| 初始化模式 | ⚡ Quick (5分钟，基本信息) / 📝 Standard (15-20分钟，+金手指设计) / 🎯 Deep (30-45分钟，+创意评估+市场定位) |

---

## Phase 2: 题材选择

### 2.1 选择题材大类

**[AskUserQuestion Round 2]**

| 问题 | 选项 |
|------|------|
| 题材大类 | 玄幻修仙类 / 都市现代类 / 言情类 / 特殊题材 |

### 2.2 选择具体题材 + 目标字数

**[AskUserQuestion Round 3]** 根据大类显示：

| 大类 | 具体题材选项 |
|------|-------------|
| 玄幻修仙类 | 修仙 / 系统流 |
| 都市现代类 | 都市异能 / 现实题材 |
| 言情类 | 狗血言情 / 古言 / 替身文 / 多子多福 |
| 特殊题材 | 知乎短篇 / 规则怪谈 / 黑暗题材 |

同时询问：

| 问题 | 选项 |
|------|------|
| 目标字数 | 30万字 / 50万字 / 100万字 / 200万字+ |

### 2.3 加载题材模板（必须执行）

根据选择的题材执行：

```bash
cat "${CLAUDE_PLUGIN_ROOT}/templates/genres/{题材}.md"
```

---

## Phase 3: 基本信息收集

### 3.1 小说标题

**[AskUserQuestion Round 4-Q1]**

| 问题 | 选项 |
|------|------|
| 标题风格 | 《XXX系统》金手指型 / 《我在XXX当XXX》身份型 / 《从XXX开始》开局型 / 《XXX：XXX》副标题型 |

> AskUserQuestion 自动提供 Other 选项，用户可直接输入完整标题；若选择风格模板，Claude 根据风格生成具体建议。

### 3.2 主角姓名

**[AskUserQuestion Round 4-Q2]**

| 问题 | 选项 |
|------|------|
| 姓名风格 | 古风名（林天/萧炎/叶凡/陈平安） / 现代名（李明/张伟/王强） / 特殊名（需自定义） |

> 选择风格后，Claude 可生成具体姓名建议供用户确认。

---

## Phase 4: 金手指设计 (Standard + Deep)

**跳过条件**: Quick 模式跳过此阶段

### 4.1 加载设计资料

```bash
cat "${CLAUDE_PLUGIN_ROOT}/templates/golden-finger-templates.md"
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/creativity/selling-points.md"
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/worldbuilding/character-design.md"
```

### 4.2 金手指核心设计

**[AskUserQuestion Round 5]**

| 问题 | 选项 |
|------|------|
| 金手指类型 | 系统面板型 / 签到打卡型 / 鉴定万物型 / 吞噬进化型 |
| 系统性格 | 冷酷理性 / 傲娇话痨 / 沉默寡言 / 搞笑吐槽 |
| 成长曲线 | 前期爆发型 / 稳步提升型 / 厚积薄发型 |

### 4.3 金手指细节设计

**[AskUserQuestion Round 6]**

| 问题 | 选项 |
|------|------|
| 系统命名风格 | 天道类（天道系统/造化系统） / 商城类（万界商城/无限商店） / 功能类（无限升级/万能抽卡） / 自定义名称 |
| 代价/限制 | 积分消耗型 / 任务惩罚型 / 生命值扣除型 / 无明显代价 |
| 核心卖点方向 | 战力碾压型 / 智商压制型 / 收集养成型 / 感情治愈型 |

---

## Phase 5: 世界构建 (Standard + Deep)

**跳过条件**: Quick 模式跳过此阶段

### 5.1 按需加载世界构建资料

```bash
# 势力体系设计（推荐加载）
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/worldbuilding/faction-systems.md"
# 设定一致性指南
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/worldbuilding/setting-consistency.md"
# 世界规则设计
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/worldbuilding/world-rules.md"
```

### 5.2 世界观框架

**[AskUserQuestion Round 7]** (可选)

| 问题 | 选项 |
|------|------|
| 世界规模 | 单一大陆 / 多大陆 / 多位面/多世界 / 星际宇宙 |
| 势力格局 | 门派/宗门 / 家族/世家 / 国家/帝国 / 组织/联盟 |
| 力量体系 | 境界修炼型 / 等级数值型 / 血脉觉醒型 / 职业技能型 |

---

## Phase 6: 创意深挖 (Deep)

**跳过条件**: Quick/Standard 模式跳过此阶段

### 6.1 加载创意资料

```bash
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/creativity/inspiration-collection.md"
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/worldbuilding/power-systems.md"
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/creativity/creative-combination.md"
cat "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/creativity/market-positioning.md"
```

### 6.2 市场定位与主角设计

**[AskUserQuestion Round 8]**

| 问题 | 选项 |
|------|------|
| 市场定位 | 大众爽文 / 小众精品 / 中间路线 |
| 主角原型 | 废材逆袭 / 天才崛起 / 重生复仇 / 穿越者 |
| 主角性格 | 隐忍腹黑 / 热血冲动 / 冷静理智 / 外冷内热 |

### 6.3 反派与感情线设计

**[AskUserQuestion Round 9]**

| 问题 | 选项 |
|------|------|
| 反派类型 | 嚣张跋扈型 / 阴险狡诈型 / 悲情反派 / 理念冲突型 |
| 感情线设计 | 后宫多女 / 单一真爱 / 无感情线 / 暧昧不明确 |
| 主角缺陷 | 性格缺陷 / 能力限制 / 心理阴影 / 无明显缺陷 |

### 6.4 创意组合评估

根据以上选择，使用 **创意 A+B+C 组合法** 评估：
- A = 题材基础
- B = 金手指特色
- C = 差异化卖点

输出灵感五维评估：新颖度/市场性/可写性/爽点密度/长线潜力

---

## Phase 7: 生成项目文件

### 7.1 执行初始化脚本

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/init_project.py" \
  "./webnovel-project" \
  "{title}" \
  "{genre}" \
  --protagonist-name "{name}" \
  --target-words {count} \
  --golden-finger-name "{gf_name}" \
  --golden-finger-type "{gf_type}" \
  --core-selling-points "{points}"
```

### 7.2 生成文件清单

| 文件 | 说明 |
|------|------|
| `.webnovel/state.json` | 运行时状态 |
| `.webnovel/index.db` | 实体索引数据库 |
| `设定集/世界观.md` | 世界设定 |
| `设定集/力量体系.md` | 力量体系 |
| `设定集/主角卡.md` | 主角卡 |
| `设定集/金手指设计.md` | 金手指设计 |
| `大纲/总纲.md` | 总纲 |

---

## Phase 8: 验证并报告

### 8.1 验证文件

```bash
ls -la .webnovel/state.json
ls -la 设定集/*.md
```

### 8.2 初始化 Git（可选）

```bash
git init && git add . && git commit -m "初始化网文项目：{title}"
```

### 8.3 输出三大定律提醒

1. **大纲即法律**: 遵循大纲，不擅自发挥
2. **设定即物理**: 遵守设定，不自相矛盾（查询 index.db 确认）
3. **发明需识别**: 新实体由 Data Agent 自动提取

---

## AskUserQuestion 轮次汇总

| 轮次 | 阶段 | 问题数 | 适用模式 |
|------|------|--------|----------|
| Round 1 | Phase 1 | 1 | All |
| Round 2 | Phase 2 | 1 | All |
| Round 3 | Phase 2 | 2 | All |
| Round 4 | Phase 3 | 2 | All |
| Round 5 | Phase 4 | 3 | Standard/Deep |
| Round 6 | Phase 4 | 3 | Standard/Deep |
| Round 7 | Phase 5 | 3 | Standard/Deep |
| Round 8 | Phase 6 | 3 | Deep |
| Round 9 | Phase 6 | 3 | Deep |

**Quick 模式**: Round 1-4 (4轮，约6个问题)
**Standard 模式**: Round 1-7 (7轮，约15个问题)
**Deep 模式**: Round 1-9 (9轮，约21个问题)
