---
name: output-style-manager
description: 读取和写入输出风格目录的工具技能。当用户需要：（1）读取输出风格文件，（2）写入/创建输出风格文件，（3）管理输出风格目录，（4）解析风格文件格式时使用。
---

# Output Style Manager

读取和写入输出风格目录的工具，用于操作输出风格文件。

## 目录路径

| 范围 | 路径 |
|-----|------|
| **全局** | `~/.pi/agent/output-styles/` |
| **项目** | `.pi/output-styles/` |

## 读取风格

### 读取单个风格文件
```bash
cat ~/.pi/agent/output-styles/<style-name>.md
cat .pi/output-styles/<style-name>.md
```

### 列出所有风格文件
```bash
ls -la ~/.pi/agent/output-styles/
ls -la .pi/output-styles/
```

### 读取激活的风格
```bash
cat ~/.pi/agent/output-styles/active.json
cat .pi/output-styles/active.json
```

## 写入风格

### 创建/覆盖风格文件
```bash
cat > ~/.pi/agent/output-styles/<style-name>.md << 'EOF'
---
name: style-name
description: Style description
keepCodingInstructions: true
---

Your style content here.
EOF
```

### 删除风格文件
```bash
trash ~/.pi/agent/output-styles/<style-name>.md
trash .pi/output-styles/<style-name>.md
```

### 设置激活风格
```bash
echo '{"name": "style-name"}' > ~/.pi/agent/output-styles/active.json
echo '{"name": "style-name"}' > .pi/output-styles/active.json
```

## 风格文件格式

```markdown
---
name: my-style
description: My custom output style
keepCodingInstructions: true
---

Your custom output style instructions here.
```

**Frontmatter 字段：**
- `name`（必需）：风格名称
- `description`（可选）：风格描述
- `keepCodingInstructions`（必需）：true/false

## 读取示例

### 检查风格是否存在
```bash
test -f ~/.pi/agent/output-styles/<name>.md && echo "exists" || echo "not found"
```

### 读取风格内容（排除 frontmatter）
```bash
awk '/^---$/{if(p)exit;p=1;next}p' ~/.pi/agent/output-styles/<name>.md
```

### 解析 frontmatter
```bash
sed -n '/^---$/,/^---$/p' ~/.pi/agent/output-styles/<name>.md | head -n -1 | tail -n +2
```

## 写入示例

### 批量创建风格
```bash
for style in style1 style2 style3; do
  cat > ~/.pi/agent/output-styles/$style.md << EOF
---
name: $style
description: Description for $style
keepCodingInstructions: true
---

Content for $style.
EOF
done
```

### 备份所有风格
```bash
tar -czf output-styles-backup.tar.gz ~/.pi/agent/output-styles/
tar -czf output-styles-backup.tar.gz .pi/output-styles/
```

## 内置风格列表

这些风格在扩展代码中定义，不在文件系统中：

| 名称 | 描述 |
|-----|------|
| `default` | 高效完成编码任务 |
| `explanatory` | 解释实现选择 |
| `learning` | 实践练习模式 |
| `coding-vibes` | 充满活力的编码伙伴 |
| `structural-thinking` | 结构化思维 |

---

# CoT 链路：语义识别与风格生成

当用户请求创建输出风格但未明确指定风格特征时，使用以下 CoT 链路进行语义识别和风格生成。

## 步骤 1：语义识别用户意图

分析用户的对话历史和当前请求，识别以下维度：

| 维度 | 检测指标 | 可能值 |
|-----|---------|--------|
| **语言风格** | 表达方式、语气、用词 | 正式/随意/活泼/严肃 |
| **详细程度** | 回复长度、解释深度 | 简洁/中等/详细 |
| **交互偏好** | 提问方式、反馈需求 | 直接/引导式/协作式 |
| **情感倾向** | 情绪表达、鼓励需求 | 中性/积极/鼓励 |
| **技术深度** | 术语使用、抽象程度 | 实用/理论/平衡 |
| **结构偏好** | 信息组织方式 | 自由/结构化/分步骤 |

### 识别方法

**分析用户消息示例：**
- "帮我写个函数" → 简洁、实用、直接
- "能不能详细解释一下为什么这样写？" → 详细、理论、引导式
- "我想学习，让我自己试试" → 协作式、学习导向
- "嘿，兄弟，帮我看看这段代码" → 随意、活泼、鼓励

**关键词映射：**
| 关键词 | 推断风格 |
|-------|---------|
| 解释、为什么、原理 | explanatory |
| 学习、练习、试试 | learning |
| 简洁、快速、直接 | default |
| 嘿、兄弟、哈哈 | coding-vibes |
| 架构、设计、模块 | structural-thinking |

## 步骤 2：匹配或生成风格

### 2.1 匹配内置风格

根据识别结果，选择最匹配的内置风格：

| 用户特征 | 推荐风格 |
|---------|---------|
| 简洁、高效、直接 | `default` |
| 需要解释、理解原理 | `explanatory` |
| 学习导向、动手实践 | `learning` |
| 轻松、活泼、鼓励 | `coding-vibes` |
| 架构设计、结构化思维 | `structural-thinking` |

### 2.2 生成自定义风格

如果内置风格不匹配，按以下格式生成：

```markdown
---
name: <生成的风格名称>
description: <基于用户特征生成的描述>
keepCodingInstructions: true
---

<根据识别维度生成的风格指令>
```

**生成模板：**

```markdown
---
name: <风格名称>
description: <一句话描述>
keepCodingInstructions: true
---

<语言风格指令>
<详细程度指令>
<交互偏好指令>
<情感倾向指令>
<技术深度指令>
<结构偏好指令>
```

**生成示例：**

```markdown
---
name: friendly-mentor
description: 友好的导师风格，平衡详细和简洁
keepCodingInstructions: true
---

保持友好和鼓励的语气。
提供清晰的解释，但不过于冗长。
在关键步骤暂停，确认用户理解。
使用简单的类比帮助理解复杂概念。
提供代码示例后，询问是否需要更多细节。
```

## 步骤 3：验证风格适用性

验证生成的风格是否满足用户需求：

- [ ] 语言风格与用户一致
- [ ] 详细程度符合预期
- [ ] 交互方式匹配偏好
- [ ] 情感基调恰当
- [ ] 技术深度合适
- [ ] 结构清晰易读

## 步骤 4：写入风格文件

将验证通过的风格写入文件：

```bash
cat > ~/.pi/agent/output-styles/<style-name>.md << 'EOF'
---
name: <style-name>
description: <description>
keepCodingInstructions: true
---

<style-content>
EOF
```

## 步骤 5：激活并反馈

激活新风格并向用户确认：

```bash
echo '{"name": "<style-name>"}' > ~/.pi/agent/output-styles/active.json
```

反馈示例：
```
已为你创建并激活风格 "<style-name>"
描述：<description>
基于你的对话风格，这个风格会：<简要说明>
如需调整，使用 /output-style:edit <style-name>
```

## 完整 CoT 示例

### 用户请求
"我想要一个适合我的风格，我喜欢详细解释但不要太啰嗦"

### CoT 处理

**步骤 1：语义识别**
- 语言风格：中性
- 详细程度：详细但控制（中等偏上）
- 交互偏好：引导式
- 情感倾向：中性
- 技术深度：平衡
- 结构偏好：结构化

**步骤 2：生成风格**

```markdown
---
name: balanced-explanatory
description: 平衡的详细解释风格，清晰但不冗长
keepCodingInstructions: true
---

提供清晰的解释说明代码意图。
使用要点列表组织信息。
每个主要步骤后简要说明原因。
避免过度解释显而易见的内容。
关键概念使用类比帮助理解。
保持回复结构化，使用标题分段。
```

**步骤 3：验证**
- ✅ 详细程度匹配
- ✅ 结构清晰
- ✅ 不冗长

**步骤 4-5：写入并激活**

```
已为你创建并激活风格 "balanced-explanatory"
描述：平衡的详细解释风格，清晰但不冗长
基于你的对话风格，这个风格会：提供清晰解释但控制长度
如需调整，使用 /output-style:edit balanced-explanatory
```