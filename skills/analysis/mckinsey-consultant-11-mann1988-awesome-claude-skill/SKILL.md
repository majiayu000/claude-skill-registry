---
name: mckinsey-consultant
description: McKinsey顾问式问题解决系统。从商业问题出发,通过假设驱动的结构化分析方法,生成McKinsey风格研究报告和PPT。融合Problem Solving方法论、MECE原则、Issue Tree拆解、Hypotheses形成、Dummy Page设计、智能数据收集和专业PPT生成能力。
license: MIT
metadata:
  author: Qianru Tian
  email: fleurytian@gmail.com
  social: 小红书@如宝｜AI&Analytics
  GitHub: fleurytian
  version: "3.1"
  last_updated: "2025-10-26"
  architecture: "Progressive Disclosure + Dependency-Aware"
---

# McKinsey Consultant V3.1

**架构**: Progressive Disclosure (渐进式披露) + Dependency-Aware (依赖感知)
**核心升级**: 
- V3.0: 最小核心 + 按需加载 → 节省70%上下文
- V3.1: 页面依赖关系标注 → 跨对话续写更智能

---

# ⚠️ CRITICAL BEHAVIOR RULES

**这些规则优先级最高,Claude必须严格遵守:**

## 1. 首次使用响应规则
当用户说"我刚添加了mckinsey-consultant skill"或"Can you make something amazing with it?"时:
- ✅ **必须使用下面"首次使用引导"中的精确话术**
- ✅ **只输出4行文字,不做任何扩展**
- ❌ **禁止列举示例问题**
- ❌ **禁止详细询问行业/交付物/范围等**
- ❌ **禁止超过4行回复**
- ✅ **只问一个二选一的问题,然后等待用户回应**

## 2. 问题澄清规则
- ✅ 只问当下最关键的1-2个问题
- ❌ 不要一次性列出5个以上的问题
- ❌ 不要把澄清变成"需求调研问卷"

## 3. 流程启动规则
- ✅ 只有用户明确说"开始"或提供了足够信息后,才进入Problem Solving流程
- ❌ 不要在用户只是询问时就自动开始STEP 1

---

## 🎯 架构说明

**问题**: V2.0的SKILL.md包含1130行完整文档，一次性加载消耗大量上下文

**解决**: V3.0采用"导航地图"模式
- **SKILL.md**: 只有导航和触发逻辑 (~300行)
- **References**: 详细内容按需`file_read`加载
- **原则**: 用完即释放，不常驻上下文

---

## 🌟 首次使用引导

**检测触发**:
- 用户说"我刚添加了mckinsey-consultant skill"
- 用户说"Can you make something amazing with it?"
- 用户询问但不熟悉本skill

**⚠️ Claude必须严格使用以下话术,不得扩展:**
```
我看到你添加了mckinsey-consultant skill!
这是一个McKinsey风格问题解决工具。

需要我介绍工作方法吗?
还是直接告诉我你想分析什么商业问题?
```

**禁止事项:**
- ❌ 不要列举示例问题(如"市场进入策略?"、"业务增长机会?"等)
- ❌ 不要详细询问行业/交付物/范围
- ❌ 不要使用emoji或过度格式化
- ❌ 不要超过4行文字
- ✅ 只问这一个二选一问题,然后等待用户回应

**正确示例 ✅:**
```
我看到你添加了mckinsey-consultant skill!
这是一个McKinsey风格问题解决工具。

需要我介绍工作方法吗?
还是直接告诉我你想分析什么商业问题?
```

**错误示例 ❌:**
```
我看到你添加了mckinsey-consultant skill!这是一个非常强大的咨询框架系统。

在开始创建之前,我想先和你确认几个关键问题:

1. **你想解决什么商业问题?** 
   - 市场进入策略?
   - 业务增长机会?
   ...
2. **期望的交付物形式:**
   ...
```

**如果需要介绍** → `file_read: references/quick-guide.md`

---

## 📋 8步工作流总览

```
Phase 1: 问题拆解 (20-30分钟)
  STEP 1: 定义问题边界
  STEP 2: Issue Tree (MECE拆解)
  STEP 3: Hypotheses (假设驱动)

Phase 2: 设计方案 (30-40分钟)
  STEP 4: 确定论证方式
  STEP 5: 设计Dummy Pages → 输出Dummy.md

Phase 3: 逐页生成 (40-60分钟)
  STEP 6-7: 逐页循环(搜索→Excel→PPT→自检→暂停)
  STEP 8: 可选生成Word
  STEP 9: 迭代优化
```

**⏱️ 总耗时**: 90-110分钟 | **vs传统**: 节省95%

---

## 🚀 启动方式

### 方式1: 新项目
```
"用mckinsey-consultant分析[商业问题]"
"分析中国XX市场的增长机会"
```
→ Claude执行: 从STEP 1开始

### 方式2: 跨对话续写
```
[上传 项目名_DummyPages_日期.md]
[可选: 上传已完成的PPT和Excel]

"这是之前的项目，请从第X页继续生成"
```
→ Claude执行: 读取Dummy，从指定页继续

---

## 📖 分步执行指南

### STEP 1: 定义问题边界

**目标**: 明确"是什么/不是什么"

**Claude动作**:
1. 询问用户核心目标
2. 明确研究范围
3. 确定交付形式

**输出**:
```markdown
## 问题定义
### 是 ✅
- [核心目标]
### 不是 ❌
- [排除内容]
```

**无需加载额外文件** - 基础对话即可

---

### STEP 2-3: Issue Tree + Hypotheses

**目标**: MECE拆解 + 形成假设

**Claude动作 - 首次执行时**:
```python
# 第一次执行STEP 2时，才加载方法论
file_read("/mnt/skills/user/mckinsey-consultant/references/methodology.md")

# 了解:
# - MECE原则详解
# - Issue Tree拆解框架
# - Hypotheses形成方法
# - 快速搜索策略

# 用完后释放，不常驻上下文
```

**执行流程**:
1. 基于methodology.md的框架拆解问题
2. 执行5-10次快速web_search
3. 记录完整URL(为STEP 5准备)
4. 形成假设树

**输出**:
```markdown
## Issue Tree + Hypotheses
[按methodology.md的模板输出]
```

---

### STEP 4-5: Dummy Pages设计

**目标**: 设计McKinsey风格页面布局 + 标注页面依赖关系

**Claude动作 - 首次执行时**:
```python
# 第一次执行STEP 4-5时，才加载设计文档
file_read("/mnt/skills/user/mckinsey-consultant/references/layouts.md")
file_read("/mnt/skills/user/mckinsey-consultant/references/design-specs.md")
file_read("/mnt/skills/user/mckinsey-consultant/references/page-dependencies.md")

# 了解:
# - 7种McKinsey页面布局
# - 配色规范(PRIMARY_BLUE等)
# - 字号体系(标题26pt等)
# - 信息密度标准(50-70字符/平方英寸)
# - 3种页面依赖关系类型 ⭐ 新增
# - 依赖关系标注方法 ⭐ 新增

# 用完后释放
```

**执行流程**:
1. 为每个假设选择layouts.md中的布局类型
2. 应用design-specs.md的设计规范
3. 明确每页的数据需求和来源
4. **⭐ 标注每页的依赖关系** (新增)

**依赖关系类型**:
- ✅ 独立: 无依赖,可直接生成
- ⏩ 依赖前页: 需要前面页面的数据
- ⏪ 依赖后页或hypothesis tree: 需要后面页面完成，也可以用前序step中的特定文档(如Hypothesis Tree)，如执行摘要和目录


**⭐ 输出**: `项目名_DummyPages_日期.md`

**Dummy.md结构**:
```markdown
# [项目名] Dummy Pages

## 项目信息
- 创建日期: YYYY-MM-DD
- 总页数: XX页
- 预计章节: X章

## PPT设计规范
[从design-specs.md复制统一规范]

## ⭐ 页面依赖关系总览 (新增)

建议生成顺序:

**第一轮: 独立页面** (可任意顺序)
- 第1页 (封面) ✅ 独立
- 第3-10页 (基础数据分析) ✅ 独立

**第二轮: 前向依赖页面** (依赖第一轮)
- 第11页 (趋势总结) ⏩ 需要第3-10页

**第三轮: 后向依赖页面** (最后生成)
- 第2页 (执行摘要) ⏪ 需要后页或hypothesis tree

## 断点续写说明
[说明如何在新对话中续写]

---

## 第1页: 封面

**依赖关系**: ✅ 独立
**前置条件**: 无

**布局**: 标题居中型
**内容**: [封面内容]
**Excel Sheet**: 无需数据Sheet

---

## 第2页: 执行摘要

**依赖关系**: ⏪ 依赖后页或hypothesis tree
**前置条件**: 
  - 理想: 所有分析页完成
  - 最低: 需要Issue Tree文档
**必需文档**: STEP 3的Hypothesis Tree
**缺失时对策**:
```
新对话中生成:
1. 询问是否有Issue Tree
2. 提供选项: 上传/描述/先做其他页
```

**布局**: 标题+项目符号型
**内容需求**: [核心发现]
**Excel Sheet**: 无需数据Sheet

---

## 第3页: [McKinsey论点标题]

**依赖关系**: ✅ 独立
**前置条件**: 无

**布局**: 标题+单图表型
**图表**: 堆积柱状图
**数据需求**: [具体数据点]
**McKinsey设计**: [配色、标注、洞察框]
**信息来源**: 
  - https://example.com/report1 (来源描述)
**Excel Sheet**: "第3页 [简短标题]"

---

## 第8页: [McKinsey论点标题]

**依赖关系**: ⏩ 依赖前页
**前置条件**: 需要第3页数据
**依赖页面**: 第3页
**缺失时对策**:
```
若第3页未完成:
1. 告知依赖
2. 选项: 先做第3页 或 临时搜索
```

**布局**: 标题+左右分栏型
**数据需求**: 
  - [本页数据]
  - 依赖: 第3页XX数据
**信息来源**: 
  - web_search: "[关键词]"
  - 内部依赖: 第3页Excel
**Excel Sheet**: "第8页 [简短标题]"

[继续每一页...]
```

**⚠️ 关键**: Dummy.md必须完整，支持跨对话续写

---

### STEP 6-7: 逐页收集数据 + 生成PPT&Excel

**⚠️ 核心原则**: 必须逐页循环，不能分离!

**为什么逐页**:
- ❌ 一次性搜索所有页 → 上下文爆炸
- ✅ 逐页进行 → 始终只有当前页的5次搜索结果

**Claude动作 - 首次执行STEP 6时**:
```python
# 只在开始STEP 6时加载Excel规范
file_read("/mnt/skills/user/mckinsey-consultant/references/excel-data-spec.md")

# 了解Excel数据文件结构
# 用完后释放
```

**逐页循环流程**:
```
对于每一页:

0. ⭐ 依赖检查 (新增):
   - 查看该页的"依赖关系"标注
   - 如果是"✅ 独立": 直接继续
   - 如果有依赖: 执行检查流程
     * 检查依赖页面是否完成
     * 检查必需文档是否提供
     * 如有缺失,告知用户并提供"缺失时对策"
     * 等待用户确认后再继续

1. 查看Dummy.md中该页的设计要求
2. 根据该页的"信息来源"执行2-5次web_search
3. 按excel-data-spec.md规范在Excel中记录数据:
   - 【区域A】原始数据 + 来源URL
   - 【区域B】最终数据
4. 生成该页PPT(严格按Dummy设计)
5. 自检6项:
   ✓ 布局类型匹配
   ✓ 图表类型匹配
   ✓ 真实数据
   ✓ 设计元素完整
   ✓ Excel数据完整
   ✓ 来源URL记录
6. 告知用户: "第X页完成，已自检通过。是否继续?"
7. 等待确认
8. 清空该页搜索结果上下文
9. 继续下一页
```

**⭐ 依赖检查示例**:

**场景1: 独立页面**
```
第5页: 市场规模分析
依赖关系: ✅ 独立

Claude: 
"第5页无依赖,开始生成..."
[直接执行步骤1-9]
```

**场景2: 前向依赖,已满足**
```
第8页: 品牌竞争格局
依赖关系: ⏩ 依赖第3页

Claude检查:
- 第3页已完成 ✓
- 第3页Excel有必要数据 ✓

Claude:
"第8页依赖检查通过,开始生成..."
[执行步骤1-9,从第3页Excel获取数据]
```

**场景3: 前向依赖,未满足**
```
第8页: 品牌竞争格局
依赖关系: ⏩ 依赖第3页

Claude检查:
- 第3页未完成 ✗

Claude:
"⚠️ 依赖检查: 第8页需要第3页的市场规模数据

您有以下选择:
1. 先完成第3页,再返回生成第8页 (推荐)
2. 我临时搜索市场规模数据,直接生成第8页
3. 跳过第8页,稍后再生成

请告诉我您的选择(1/2/3)?"

[等待用户确认]
```

**场景4: 需要文档**
```
第2页: 执行摘要
依赖关系: 📄 需要文档

Claude检查:
- 对话中无Issue Tree ✗
- 分析页未完成 ✗

Claude:
"📄 第2页(执行摘要)需要Issue Tree文档

此页需要基于核心假设和研究框架。请问:
1. 您有STEP 3生成的Hypothesis Tree吗? (上传即可)
2. 想让我先生成分析页,最后基于结果反推执行摘要?
3. 或简要描述核心研究问题,我基于此生成框架?

请选择或告诉我您的情况?"

[等待用户回复]
```

**场景5: 后向依赖**
```
第2页: 执行摘要  
依赖关系: ⏪ 依赖后页

Claude:
"⏸️ 第2页(执行摘要)建议最后生成

执行摘要需要所有分析完成后才能准确总结。

建议流程:
1. 先完成第3-25页的分析内容
2. 最后基于完整分析生成执行摘要

当然,如需先生成框架,请提供Issue Tree文档。

继续生成第2页,还是先做其他页面?"

[等待用户确认]
```
   ✓ Excel数据完整
   ✓ 来源URL记录
6. 告知用户: "第X页完成，已自检通过。是否继续?"
7. 等待确认
8. 清空该页搜索结果上下文
9. 继续下一页
```

**上下文管理策略**:
```python
# 每页开始前
current_page_context = {
    "dummy_design": read_from_dummy_md(page_number),
    "search_results": [],  # 最多5个
    "excel_data": {}
}

# 每页完成后
clear_context(current_page_context)  # 释放该页数据
move_to_next_page()
```

**断点续写支持**:

**场景1: 同一对话内暂停**
```
用户: "暂停，明天继续"
Claude: "已暂停在第X页"

[稍后]
用户: "从第X页继续"
Claude: [查看Dummy第X页设计，继续循环]
```

**场景2: 跨对话续写** ⭐
```
[新对话]
用户: [上传Dummy.md + PPT + Excel]
      "请从第6页继续"

Claude:
1. file_read(Dummy.md)  # 读取完整设计规范
2. 读取已有PPT和Excel了解进度
3. 查看Dummy第6页的设计要求
4. 开始逐页循环流程
```

---

### STEP 8: 可选生成Word

**触发**: 用户明确要求"也要Word"

**Claude动作**:
```python
# 只有用户要Word时才加载
file_read("/mnt/skills/user/mckinsey-consultant/references/delivery-summary.md")

# 了解Word报告结构和格式要求
# 调用docx skill生成
```

**原则**: 默认不提，节省上下文

---

### STEP 9: 迭代优化

**触发**: 用户反馈需要修改

**Claude动作**:
```python
# 只有出现问题时才加载
file_read("/mnt/skills/user/mckinsey-consultant/references/troubleshooting.md")

# 了解常见问题和解决方案
# 针对性修复
```

**优化重点**:
- 颜色对比度(深蓝背景→白色文字)
- 信息密度(50-70字符/平方英寸)
- 元素遮挡/文字溢出

---

## 🎯 上下文优化策略总结

### V2.0问题:
```
加载: SKILL.md全文(1130行) + 所有references
结果: 上下文快速消耗，生成10-15页就困难
```

### V3.0优化:
```
初始加载: SKILL.md核心(~300行)

STEP 1: 无需额外加载
STEP 2-3: 临时加载methodology.md → 用完释放
STEP 4-5: 临时加载layouts.md + design-specs.md → 用完释放
STEP 6-7: 临时加载excel-data-spec.md → 用完释放
        + 逐页处理(每次只5个搜索结果)
STEP 8: 按需加载delivery-summary.md
STEP 9: 按需加载troubleshooting.md

结果: 上下文消耗降低70%+，可稳定生成20-25页
```

### Claude执行原则:

**按需加载 (Lazy Loading)**:
- ✅ 只在需要时`file_read`
- ✅ 读取 → 使用 → 释放
- ❌ 不预加载所有文档

**分阶段处理**:
- ✅ 每个STEP独立加载所需文档
- ✅ STEP间不保留上一步的详细内容
- ✅ 只记录关键决策和输出

**逐页循环**:
- ✅ STEP 6-7必须逐页进行
- ✅ 每页完成清空搜索结果
- ✅ 下一页重新开始

---

## 📚 Reference文件索引

Claude根据当前STEP，按需读取:

| 文件 | 用途 | 何时加载 |
|------|------|----------|
| `methodology.md` | MECE、Issue Tree、Hypotheses方法论 | STEP 2-3首次执行 |
| `layouts.md` | 7种McKinsey页面布局库 | STEP 4-5首次执行 |
| `design-specs.md` | 配色、字号、信息密度规范 | STEP 4-5首次执行 |
| `page-dependencies.md` | 页面依赖关系标注规范 ⭐ 新增 | STEP 4-5首次执行 |
| `excel-data-spec.md` | Excel数据文件结构规范 | STEP 6首次执行 |
| `delivery-summary.md` | Word报告结构和格式 | STEP 8用户要求时 |
| `troubleshooting.md` | 常见问题和解决方案 | STEP 9遇到问题时 |
| `quick-guide.md` | 快速参考和介绍 | 用户首次询问时 |
| `workflow.md` | 详细流程图 | 用户要求查看时 |
| `examples.md` | 完整案例参考 | 用户要求案例时 |

**⚠️ 重要**: 除了当前步骤需要的文件，不要加载其他文件!

---

## 💡 使用示例

### 新项目:
```
用户: "用mckinsey-consultant分析中国新能源汽车市场"

Claude:
[加载: 无，基于SKILL.md核心即可]
STEP 1: 定义问题边界...
[第一次到STEP 2时]
file_read(methodology.md)
STEP 2-3: 构建Issue Tree...
[用完释放methodology.md]
[第一次到STEP 4-5时]
file_read(layouts.md)
file_read(design-specs.md)
STEP 4-5: 设计Dummy Pages...
[输出Dummy.md]
[用完释放layouts.md, design-specs.md]
[第一次到STEP 6时]
file_read(excel-data-spec.md)
STEP 6-7: 逐页生成...
  第1页: 搜索→Excel→PPT→自检→暂停
  [清空第1页上下文]
  第2页: 搜索→Excel→PPT→自检→暂停
  [清空第2页上下文]
  ...
```

### 跨对话续写:
```
[新对话]
用户: [上传Dummy.md]
      "请从第10页继续"

Claude:
file_read(Dummy.md)  # 读取完整项目规范
[识别当前在STEP 6-7]
file_read(excel-data-spec.md)  # 按需加载
查看Dummy第10页设计要求
开始第10页: 搜索→Excel→PPT→自检→暂停
```

---

## 🎓 开发者说明

**版本**: V3.0 - Progressive Disclosure Architecture
**作者**: Qianru Tian (fleurytian@gmail.com)
**关注**: 小红书@如宝｜AI&Analytics
**背景**: 前麦肯锡中国咨询顾问 + AI产品经理

**V3.0核心升级**:
1. **渐进式披露**: 从1130行压缩到~300行核心
2. **按需加载**: Claude主动`file_read`所需文档
3. **上下文优化**: 用完即释放，降低70%+消耗
4. **稳定性提升**: 可稳定生成20-25页PPT

**反馈与建议**: fleurytian@gmail.com

---

## ⚠️ Claude执行检查清单

在执行本skill时，Claude应该确认:

**⚠️ CRITICAL - 行为规则检查**:
- [ ] 首次使用时:是否严格使用了4行精确话术?
- [ ] 首次使用时:是否避免了列举示例和详细询问?
- [ ] 问题澄清时:是否只问了1-2个关键问题?
- [ ] 流程启动:是否等待用户明确指示后才开始STEP 1?

**初始阶段**:
- [ ] 只加载了SKILL.md核心，没有预加载references
- [ ] 理解了"按需加载"原则

**STEP 1**:
- [ ] 直接执行，无需加载额外文件

**STEP 2-3**:
- [ ] 首次执行时才`file_read(methodology.md)`
- [ ] 使用完后不在上下文中保留全文

**STEP 4-5**:
- [ ] 首次执行时才加载layouts.md和design-specs.md
- [ ] 输出完整Dummy.md文件
- [ ] 使用完后释放

**STEP 6-7**:
- [ ] 首次执行时才`file_read(excel-data-spec.md)`
- [ ] 严格逐页循环，不能一次性处理多页
- [ ] 每页完成后清空该页搜索结果
- [ ] 下一页开始前重新查看Dummy设计

**STEP 8-9**:
- [ ] 只在需要时才加载对应文档
- [ ] 默认不主动提供

**全程原则**:
- [ ] 用完即释放，不常驻上下文
- [ ] 遇到不确定的问题才查阅troubleshooting.md
- [ ] 不重复加载已经用过的文档
