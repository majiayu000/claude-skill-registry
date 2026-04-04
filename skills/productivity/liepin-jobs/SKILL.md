---
name: liepin-jobs
description: |
  猎聘求职工具 — 在猎聘上搜索职位、投递简历、查看/编辑简历。
  触发词: 找工作, 搜职位, 投简历, 猎聘, liepin, 求职, 招聘, 简历
version: 0.2.0
author: xllin
license: MIT
homepage: https://github.com/xllinbupt/MCP2skill
repository: https://github.com/xllinbupt/MCP2skill
keywords:
  - jobs
  - liepin
  - resume
  - mcp
  - chinese
requires:
  bins: python3
allowed-tools: Bash(python3:*),Bash(python:*)
---

# 猎聘求职工具 (liepin-jobs)

在猎聘平台上搜索职位、投递简历、查看和编辑简历。基于猎聘官方 MCP Server，零外部依赖。

**脚本位置**: 本 skill 目录下的 `liepin_mcp.py`

---

## !! 首次使用必读：获取凭证

使用此工具前，用户必须先获取猎聘的用户凭证。**没有凭证无法使用任何功能。**

### 获取步骤

1. **打开猎聘 MCP 配置页**: 引导用户在浏览器访问 https://www.liepin.com/mcp/server
2. **登录猎聘账号**: 用户需要有猎聘账号并登录
3. **获取 User Token**:
   - **User Token**: 格式为 `liepin_user_token_xxxx`（页面上的 `x-user-token` 值）
4. **配置 Token**: 运行 setup 命令保存 token

```bash
python3 "<skill_dir>/liepin_mcp.py" setup
# 按提示输入 user token
```

### 或通过环境变量配置

```bash
export LIEPIN_USER_TOKEN="liepin_user_token_xxxx"
```

### Token 过期

- 凭证有效期 **90 天**
- 过期后会收到认证错误，需引导用户重新访问上述页面获取新 Token
- 重新生成 Token 会立即使旧 Token 失效

**如果用户还没有配置 Token，必须先引导他们完成上述步骤，再执行任何操作。**

---

## 命令速查

```bash
SCRIPT="<skill_dir>/liepin_mcp.py"

# 搜索职位
python3 "$SCRIPT" search-job --jobName "AI产品经理" --address "上海"
python3 "$SCRIPT" search-job --jobName "前端开发" --address "北京" --salary "30-50k"
python3 "$SCRIPT" search-job --jobName "数据分析" --companyName "字节跳动" --json

# 投递职位（需要先搜索获取 jobId 和 jobKind）
python3 "$SCRIPT" apply-job --jobId "JOB_ID" --jobKind "JOB_KIND"

# 查看简历
python3 "$SCRIPT" my-resume
python3 "$SCRIPT" my-resume --json

# 更新简历
python3 "$SCRIPT" update-resume --module basic --data '{"name": "张三", "phone": "138xxx"}'
python3 "$SCRIPT" update-resume --module experience --data '{"company": "xxx", "title": "产品经理"}'
python3 "$SCRIPT" update-resume --module expectations --data '{"salary": "30-50k", "city": "上海"}'
python3 "$SCRIPT" update-resume --module self-assessment --data '{"content": "5年产品经验..."}'

# 列出所有可用工具（查看猎聘最新 API 能力）
python3 "$SCRIPT" list-tools
python3 "$SCRIPT" list-tools --json

# 通用调用（适用于猎聘新增的工具）
python3 "$SCRIPT" call <tool-name> -a '{"key": "value"}' --json
```

## 典型求职流程

当用户说"帮我找工作"、"搜一下猎聘上的XX职位"时，按以下流程执行：

1. **检查 Token** → 如果未配置，先引导用户获取（见上方"首次使用必读"）
2. **查看简历** (`my-resume`) → 确认简历信息完整，提醒用户补充缺失项
3. **搜索职位** (`search-job`) → 根据用户意向搜索，用表格展示结果
4. **分析匹配度** → 结合简历和职位要求，帮用户筛选最合适的
5. **投递职位** (`apply-job`) → **必须先向用户展示职位详情并获得明确确认后再投递**

## 搜索参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--jobName` | 职位名称关键词 | "AI产品经理"、"前端开发"、"数据分析师" |
| `--address` | 工作地点 | "上海"、"北京"、"深圳"、"杭州" |
| `--salary` | 薪资范围 | "20-30k"、"30-50k" |
| `--education` | 学历要求 | 本科、硕士 |
| `--experience` | 工作经验 | "3-5年"、"5-10年" |
| `--companyType` | 公司类型 | 外企、国企、民企 |
| `--companyName` | 公司名称 | "字节跳动"、"阿里巴巴"、"腾讯" |

## 简历模块

| 模块 | 说明 |
|------|------|
| `basic` | 基本信息（姓名、手机、邮箱等） |
| `experience` | 工作/项目经历 |
| `expectations` | 求职期望（期望薪资、城市、岗位等） |
| `self-assessment` | 自我评价 |

## 输出格式

- 默认输出人类可读格式
- 加 `--json` 输出原始 JSON，方便程序化处理
- 搜索结果建议以表格形式展示给用户，包含：职位名、公司、薪资、地点、经验要求

## 注意事项

- **投递不可撤回**: 执行 `apply-job` 前必须获得用户明确确认
- **频率限制**: 所有操作共享 60 次/分钟，避免短时间批量调用
- **Token 安全**: 不要在日志或对话中暴露完整的 Token 内容
- **数据来源**: 所有数据来自猎聘平台，实时获取

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| "未配置 LIEPIN_USER_TOKEN" | 没有运行 setup | 引导用户获取 Token 并运行 `setup` |
| HTTP 401 | Token 过期或无效 | 引导用户重新访问配置页获取新 Token |
| HTTP 429 | 频率限制 | 等待 1 分钟后重试 |
| 网络超时 | 网络问题 | 重试一次 |
