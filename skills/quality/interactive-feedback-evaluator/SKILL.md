---
name: interactive-feedback-evaluator
description: 提供标准化的交互式评估系统，支持在Alma侧边栏直接填写和提交评估表单。自动收集反馈数据并生成结构化总结。
---

# InteractiveFeedbackEvaluator Skill

## 核心价值

**标准化、可复用的交互式评估系统**

- ✅ 在Alma侧边栏直接填写表单
- ✅ 一键提交，无需复制粘贴
- ✅ 自动收集反馈数据
- ✅ AI自动生成评估总结
- ✅ 支持多种评估场景

## 何时使用

- 当你想要评估分析报告、产品功能、技能效果
- 当你需要结构化的反馈收集机制
- 当你想要避免重复的评估流程
- 当你需要标准化评估模板

## 使用方式

### 快速开始

```bash
用户："评估这份报告"

AI：
1. 启动评估服务器（后台）
2. 生成交互式表单
3. 在侧边栏预览表单
4. 等待你提交反馈

用户：
1. 在侧边栏填写表单
2. 点击"提交"按钮
3. 完成

AI：
1. 检测到新反馈
2. 自动读取并生成总结
3. 保存反馈历史
```

### 支持的评估类型

1. **分析报告评估**（analysis-report）
   - 整体价值、有用性、可执行性
   - 最有价值部分、改进建议

2. **技能评估**（skill-evaluation）
   - 功能完整性、可靠性、易用性
   - 最有用功能、优先改进项

3. **产品评估**（product-evaluation）
   - 产品价值、用户体验、技术实现
   - 核心优势、主要问题

4. **自定义评估**（custom）
   - 自定义评估维度
   - 自定义评分选项

## 技术架构

### 核心组件

```
interactive-feedback-evaluator/
├── skill.md                        # 技能定义（本文件）
├── scripts/
│   ├── evaluation_server.py         # Flask评估服务器
│   └── start_evaluation.sh         # 启动脚本
├── templates/
│   ├── evaluation_form.html         # 通用评估表单
│   └── report_evaluation.html      # 报告评估表单
├── data/
│   ├── feedback.json               # 最新反馈（实时）
│   └── feedback_history/           # 历史反馈记录
│       └── feedback_YYYY-MM-DD_HHMMSS.json
└── references/
    ├── evaluation_templates.yaml   # 评估模板库
    └── usage_guide.md             # 使用指南
```

### 数据流

```
用户填写表单 → POST到服务器 → 保存到feedback.json
                                          ↓
                                    AI定期检测
                                          ↓
                                    读取feedback.json
                                          ↓
                                    生成评估总结
```

## 评估模板

### 分析报告评估模板

```yaml
评估类型: analysis-report
评分维度:
  - 整体价值 (1-5分)
  - 有用性 (1-5分)
  - 可执行性 (1-5分)
多选题:
  - 最有价值的部分 (选2-3个)
    * 行为模式识别
    * 认知偏见诊断
    * 战略盲点揭示
    * 真相检验问题
    * 否定性指导
    * 可沉淀知识
  - 最需要改进的部分
开放性问题:
  - 具体改进建议
  - 会采取的第一个行动
```

### 技能评估模板

```yaml
评估类型: skill-evaluation
评分维度:
  - 整体价值 (1-5分)
  - 功能完整性 (1-5分)
  - 可靠性 (1-5分)
  - 易用性 (1-5分)
多选题:
  - 最有用的功能 (选1-2个)
开放性问题:
  - 优先改进项
  - 使用场景描述
```

## AI使用指南

当用户要求评估时，AI执行以下步骤：

### 1. 启动服务器

```bash
# 启动评估服务器（后台）
/Users/douba/.claude/skills/interactive-feedback-evaluator/scripts/start_evaluation.sh
```

### 2. 生成交互式表单

根据评估类型选择合适的模板，生成HTML表单：

```bash
# 生成评估表单
curl -X POST http://localhost:5002/generate \
  -H "Content-Type: application/json" \
  -d '{
    "evaluation_type": "analysis-report",
    "title": "Alma 深度洞察分析报告 v2.0",
    "evaluation_object": "报告评估",
    "timestamp": "2026-01-15 04:00"
  }' > /tmp/evaluation_form.html
```

### 3. 在侧边栏预览

```bash
# 在Alma侧边栏预览表单
# 提示用户填写并提交
```

### 4. 等待用户提交

AI定期检查 `feedback.json` 是否更新。

### 5. 读取反馈并生成总结

```bash
# 读取最新反馈
cat /Users/douba/.claude/skills/interactive-feedback-evaluator/data/feedback.json

# 生成评估总结
```

### 6. 保存到历史

```bash
# 复制到历史记录
cp feedback.json feedback_history/feedback_$(date +%Y%m%d_%H%M%S).json
```

## API接口

### POST /generate

生成交互式评估表单

**请求：**
```json
{
  "evaluation_type": "analysis-report",
  "title": "报告标题",
  "evaluation_object": "评估对象",
  "options": {
    "dimensions": ["整体价值", "有用性", "可执行性"],
    "multi_select": {
      "most_valuable": ["选项1", "选项2", "选项3"]
    }
  }
}
```

**响应：**
```html
<!DOCTYPE html>
<!-- 交互式表单HTML -->
</html>
```

### POST /submit

提交评估反馈

**请求：**
```json
{
  "evaluation_type": "analysis-report",
  "title": "报告标题",
  "scores": {
    "overall": 4,
    "usefulness": 5,
    "actionability": 4
  },
  "multi_select": {
    "most_valuable": ["behavior_pattern", "cognitive_bias"]
  },
  "text_input": {
    "suggestions": "可以增加更多案例",
    "first_action": "停止说'测试下'"
  },
  "timestamp": "2026-01-15T04:00:00Z"
}
```

**响应：**
```json
{
  "success": true,
  "message": "反馈已保存",
  "feedback_id": "feedback_20260115_040000"
}
```

### GET /status

检查服务器状态

**响应：**
```json
{
  "running": true,
  "port": 5002,
  "latest_feedback": "2026-01-15T04:00:00Z"
}
```

## 数据存储

### feedback.json

最新反馈的实时文件，格式：

```json
{
  "metadata": {
    "evaluation_type": "analysis-report",
    "title": "Alma 深度洞察分析报告 v2.0",
    "evaluation_object": "报告评估",
    "timestamp": "2026-01-15T04:00:00Z"
  },
  "scores": {
    "overall": 4,
    "usefulness": 5,
    "actionability": 4
  },
  "multi_select": {
    "most_valuable": ["behavior_pattern", "cognitive_bias", "negative_guidance"]
  },
  "text_input": {
    "suggestions": "可以增加更多实际案例",
    "first_action": "停止说'测试下'，改为系统化问题清单"
  }
}
```

### feedback_history/

历史反馈记录，按时间戳命名：
- `feedback_20260115_040000.json`
- `feedback_20260115_041500.json`

## 使用示例

### 示例1：评估分析报告

```bash
用户："帮我评估这份v2.0分析报告"

AI：
1. 启动服务器
2. 生成报告评估表单
3. 提示："请在侧边栏预览 /tmp/evaluation_form.html，填写完成后点击'提交'"

用户：
1. 在侧边栏填写表单
2. 点击"提交"

AI：
1. 检测到新反馈
2. 生成评估总结
3. 显示：
   "基于你的反馈：
   - 整体价值：4/5
   - 最有价值：认知偏见诊断、真相检验问题、否定性指导
   - 改进建议：增加更多实际案例
   - 行动计划：停止说'测试下'，改为系统化问题清单"
```

### 示例2：评估新技能

```bash
用户："评估twitter-collector技能"

AI：
1. 启动服务器
2. 生成技能评估表单
3. 提示用户填写提交

AI生成总结：
- 整体价值：3/5
- 强项：数据采集功能
- 弱项：浏览器管理可靠性
- 优先改进：防止浏览器意外关闭
```

## 注意事项

- **服务器自动管理**：AI会自动启动和关闭服务器，无需手动干预
- **数据安全**：所有反馈数据存储在本地，不上传到云端
- **模板可定制**：可以根据需要调整评估模板
- **历史追溯**：所有反馈都有历史记录，可以追溯和对比

## 版本历史

- **v1.0** (2026-01-15)
  - 初始版本
  - 支持分析报告和技能评估
  - 侧边栏直接提交功能
  - 自动反馈收集和总结
