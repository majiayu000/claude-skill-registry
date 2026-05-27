# 练习 1: 创建你的第一个 Hello Skill

**难度**：⭐ 初级
**预计时间**：15 分钟

## 学习目标

完成这个练习后，你将：

- 理解 Skill 的基本结构
- 知道如何创建一个简单的 Skill
- 能够运行和测试你的 Skill

## 任务描述

创建一个名为 `personal-greeting` 的 Skill，它会：

1. 向用户问好
2. 询问用户的名字
3. 用用户的名字个性化问候
4. 询问用户今天想做什么

## 要求

### 1. 文件结构

创建文件 `personal-greeting.md`：

```markdown
---
name: personal-greeting
description: [你的描述]
---

[你的内容]
```

### 2. 必需元素

- ✅ Frontmatter 包含 `name` 和 `description`
- ✅ `name` 是 `personal-greeting`
- ✅ `description` 清楚说明 Skill 的功能
- ✅ 内容包含问候、询问名字、个性化问候的步骤

### 3. 输出示例

当用户运行 Skill 时，应该看到类似这样的输出：

```
你好！我是你的个人助手。

请问你叫什么名字？

[用户回答：小明]

很高兴见到你，小明！今天有什么我可以帮你的吗？
```

## 提示

### 提示 1: Frontmatter 格式

```yaml
---
name: personal-greeting
description: 向用户问好并询问他们的名字
---
```

### 提示 2: 内容结构

```markdown
# 个人问候助手

你是友好的助手。工作流程：
1. 向用户问好
2. 询问名字
3. 用名字个性化问候
4. 询问如何帮助
```

### 提示 3: 测试

创建后，在 Claude Code 中测试：

```
personal-greeting
```

## 验收标准

完成练习后，检查：

- [ ] 文件名是 `personal-greeting.md`
- [ ] Frontmatter 格式正确
- [ ] name 字段是 `personal-greeting`
- [ ] description 清楚且简洁
- [ ] Skill 可以运行并按预期工作
- [ ] 输出友好且符合描述

## 参考答案

完成练习后，可以查看 `solutions/beginner/exercise-01.md` 对比参考答案。

## 延伸挑战

完成基本要求后，尝试：

- 添加更多个性化问题（如询问用户的职业、兴趣）
- 根据时间调整问候（早上/下午/晚上）
- 添加一个随机鼓励的话

## 相关资源

- [快速入门指南](../../docs/00-getting-started.md)
- [hello-world 示例](../../skills/01-basics/hello-world/)
