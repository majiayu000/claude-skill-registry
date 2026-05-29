---
name: good-mp-post
displayName: Good 公众号发布
description: 微信公众号文章发布完整流程管理，包括AI辅助创作、图片生成、排版和发布。
version: 1.0.0
license: MIT
---

# Good 公众号发布

## 任务目标
通过AI辅助完成微信公众号文章的创作、排版和发布全流程。

**能力：** 文章创作、图片生成与上传、草稿创建、文章发布

**触发：** 用户需要创建或发布微信公众号文章

## 使用模式

### 模式1：Web UI (推荐)
可视化界面，支持文章管理、在线编辑和发布：

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务（默认端口8000）
uvicorn app.main:app --reload

# 浏览器访问
http://localhost:8000
```

**功能：**
- 文章CRUD操作（创建、查看、编辑、删除）
- Markdown内容编辑
- 数据库持久化（SQLite）
- 直接发布到微信公众号
- 发布历史记录

### 模式2：脚本 (命令行)
适合自动化场景，与Web UI共享数据库：

```bash
# 上传图片
python scripts/upload_media.py /path/to/image.jpg thumb

# 创建草稿
python scripts/create_draft.py --title "标题" --content "内容"

# 发布文章
python scripts/publish_article.py --media_id <草稿ID>
```

**数据互通：** 脚本发布的文章会自动记录到数据库，Web UI可查看和管理。

## 前置准备
**依赖：** requests>=2.28.0, python-dotenv>=1.0.0, fastapi>=0.104.1, sqlalchemy>=2.0.35

**凭证配置：**
- 在 .env 文件配置 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET`
- 获取方式：微信公众平台 → 开发 → 基本配置
- 需配置IP白名单

**数据库：** 自动创建 SQLite 数据库（data/articles.db），无需手动配置

## 标准流程（Web UI）

### 1. 启动服务
```bash
cd skills/good-mp-post
uvicorn app.main:app --reload
```

### 2. 创建文章
- 打开 http://localhost:8000
- 填写标题、作者、摘要
- 编写 Markdown 内容
- 保存草稿

### 3. 发布文章
- 在文章列表点击"发布"按钮
- 自动处理封面图上传、草稿创建、发布流程
- 查看发布状态

## 脚本流程（命令行）

### 1. 创作文章内容
- 根据用户需求创作文章（Markdown格式）
- 参考 `assets/templates/article-template.md` 了解格式建议

### 2. 生成图片
- 生成封面图（建议 900×383px，<5MB）
- 生成插图（宽度≤900px）

### 3. 上传图片
调用 `scripts/upload_media.py`:
```bash
python scripts/upload_media.py /path/to/cover.jpg thumb    # 封面图
python scripts/upload_media.py /path/to/image.png image    # 正文图
```

### 4. 创建草稿
调用 `scripts/create_draft.py`:
```bash
python scripts/create_draft.py \
  --title "文章标题" \
  --author "作者名" \
  --thumb_media_id <封面图ID> \
  --content "<p>HTML正文</p>" \
  --media_ids '[]'
```

**注意：** 作者名最长8个中文字符

### 5. 发布文章
调用 `scripts/publish_article.py`:
```bash
python scripts/publish_article.py --media_id <草稿ID>
```

## 资源索引
- `app/main.py` - FastAPI 主应用入口
- `app/api/articles.py` - 文章管理 API
- `app/api/images.py` - 图片上传 API
- `app/database.py` - 数据库模型和连接
- `app/static/index.html` - Web UI 界面
- `scripts/upload_media.py` - 上传图片到素材库
- `scripts/create_draft.py` - 创建图文草稿
- `scripts/publish_article.py` - 发布草稿
- `scripts/db_logger.py` - 数据库日志记录（可选）
- `references/api-guide.md` - API详细说明
- `assets/templates/article-template.md` - 文章格式模板

## 图片路径规范（重要）

AI生成文章时必须遵循以下规范：

### 禁止使用相对路径
❌ 错误示例：
```markdown
![封面](./cover.jpg)
![插图](../images/chart.png)
![示例](images/demo.jpg)
```

### 正确的图片处理流程
1. 先生成图片文件并保存到临时目录
2. 调用 `upload_media.py` 上传到微信获取 media_id
3. 使用占位符或说明文字，不要直接插入本地路径

✅ 正确示例：
```markdown
<!-- 步骤1：生成图片 -->
<!-- 步骤2：上传图片 -->
python scripts/upload_media.py /path/to/cover.jpg thumb

<!-- 步骤3：记录 media_id，在创建草稿时使用 -->
<!-- 正文中不插入相对路径 -->
```

### 原因说明
- 相对路径在预览和发布时无法正常显示
- 微信公众号要求先上传图片获取 media_id
- 已有的工作流（上传图片→创建草稿）是正确的

## 关键注意事项
1. **作者名限制：** 最长8个中文字符
2. **图片有效期：** 封面图永久，正文图3天
3. **图片路径：** 禁止使用相对路径（见上方图片路径规范）
4. **HTML要求：** 使用简单标签（p/h1-h3/ul/li/img/a），避免复杂CSS
5. **发布审核：** 发布后需微信审核才能展示
6. **调用频率：** 上传1000次/天，创建草稿100次/天，发布10次/天
