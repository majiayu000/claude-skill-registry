---
name: jeecg-dev
description: JeecgBoot 开发规范。当编写/修改 JeecgBoot 代码、应用 GitHub PR/issue 的改动、修复 bug、新增功能、重构代码、代码生成时自动触发。Use when writing or modifying any JeecgBoot code, applying changes from a GitHub PR/issue (e.g. user shares a PR URL, says "改这个PR", "合入这个issue", "按这个PR改"), code generation, bug fix, feature addition, or refactoring. Enforces update-begin/end markers, naming conventions, entity/controller/service patterns, API conventions, database design rules, and log practices.
---

# JeecgBoot 开发规范

在 JeecgBoot 项目中编写或修改代码时，必须遵循以下规范。本 skill 是强制性的——任何代码变更都必须符合这些标准。

---

# 一、必做事项（每次代码修改必须完成，缺一不可）

## 1. 代码修改痕迹注释（内联注释）

**所有新增或修改的代码块必须用 `update-begin` / `update-end` 注释包裹。**

```java
//update-begin---author:作者名 ---date:YYYYMMDD  for：【bug号/需求号】修改说明-----------
// 新增或修改的代码
//update-end---author:作者名 ---date:YYYYMMDD  for：【bug号/需求号】修改说明-----------
```

**规则：**
- `author` 填实际修改人，`date` 格式 `YYYYMMDD`（无横线），`for` 填 bug号/需求号 + 简要说明
- 新增方法：`update-begin` 放在方法声明前，`update-end` 放在方法结束 `}` 后
- 修改已有方法中的代码：只包裹被修改的代码段，不包裹整个方法
- 用户未提供 bug 号时，必须主动询问

**⚠️ 不需要加痕迹注释的改动（只要求逻辑变更才包裹）：**

以下纯机械性、轻量级或与业务逻辑无关的改动 **不要** 加 `update-begin/end` 注释，否则徒增 diff 噪音、破坏代码整洁：

- `import` 语句的新增 / 删除 / 排序
- 包声明 `package` 调整
- 纯格式化、空行、缩进调整
- 注释的错别字修正
- 未使用 import / 变量的清理
- IDE 自动生成的 `@Override`、`serialVersionUID` 等
- **单行注解的新增 / 修改**：例如给已有方法补 `@RequiresPermissions("xxx")`、`@Transactional`、`@Deprecated`、Swagger/Knife4j `@Operation`、`@Schema(description=...)`、`@TableField(...)`、`@JsonProperty(access=...)`、Lombok 类级注解（`@Slf4j`/`@Data` 等）。这类改动 SVN diff 一眼可见、无业务分支逻辑，加 2 行 `update-begin/end` 包 1 行注解会让 diff 噪音翻倍
- 字段访问修饰符微调（如 `private` → `protected`）、`final` 添加等单行属性变更
- 删除单个 `@Excel`/`@Schema` 之类不影响调用方的注解

判断标准：**"这行改动是否需要后人通过痕迹注释才能理解为什么改？"**。
- 影响业务流程、含有 if/loop/异常处理、修改了方法体内多行逻辑 → **加** `update-begin/end`
- 单行声明性变更（注解、修饰符）+ SVN 提交日志 + `代码修改日志` 文件已能说明清楚 → **不加**

举例：
- 给 `/queryById` 方法补一行 `@RequiresPermissions("airag:model:queryById")` → **不加**痕迹注释，理由和上下文写到 `代码修改日志` 即可
- 在 `/edit` 方法体里加一段"如果 credential 为空则从 DB 读旧值"的 if 判断 → **加** `update-begin/end`，因为后人需要知道这段防御性代码的来由
- 为新功能新增 `import UserAccountInfo` 时，只在**用到该类的代码块**外加 `update-begin/end`，import 本身不加

**Java 示例（用 `//` 行注释，允许 `---` 分隔）：**
```java
//update-begin---author:chenrui ---date:20250606  for：[issues/8337]关于ai工作列表的数据权限问题 #8337------------
if (MybatisPlusSaasConfig.OPEN_SYSTEM_TENANT_CONTROL) {
    AiragApp app = airagAppService.getById(id);
    String currentTenantId = TokenUtils.getTenantIdByRequest(request);
    if (null == app || !app.getTenantId().equals(currentTenantId)) {
        return Result.error("删除AI应用失败，不能删除其他租户的AI应用！");
    }
}
//update-end---author:chenrui ---date:20250606  for：[issues/8337]关于ai工作列表的数据权限问题 #8337------------
```

### XML / MyBatis Mapper XML 特殊规则（重要）

**XML 注释内严禁出现 `--`（XML 规范禁止 double-hyphen 出现在 `<!-- -->` 内）**，因此在 `.xml` 文件（如 Mapper XML、`pom.xml`、Flyway xml 等）中写痕迹注释时：

- ❌ 错误：`<!-- update-begin---author:scott ---date:20260421  for：【xxx】说明----------- -->`（含 `--`，解析器可能报错或告警）
- ✅ 正确：`<!-- update-begin author:scott date:20260421 for：【xxx】说明 -->`（用空格或单 `-` 分隔，避免任何连续两个及以上的 `-`）

**XML 痕迹注释模板：**
```xml
<!-- update-begin author:作者名 date:YYYYMMDD for：【bug号/需求号】修改说明 -->
<if test="processApplyUserId != null and processApplyUserId !=''">
    AND ahp.START_USER_ID_ = #{processApplyUserId}
</if>
<!-- update-end author:作者名 date:YYYYMMDD for：【bug号/需求号】修改说明 -->
```

其他同样要求避免 `--` 的注释场景：HTML（`.html`/`.vue` template）、SVG、XSL 等所有基于 XML 的文件类型。

## 2. 代码修改日志（历史记录文件）

在对应模块的日志文件**末尾**追加记录，格式：

```
-- author:作者名---date:YYYYMMDD--for: 【bug号/PR号】修改说明 ---
涉及的文件路径（每行一个）
-- author:作者名---date:YYYYMMDD--for: 【bug号/PR号】修改说明 ---
```

各模块日志文件位置：
- `jeecg-boot-base-core/doc/修改日志.log`
- `jeecg-module-system/jeecg-system-biz/docs/代码修改日志`
- `jeecg-boot-module/jeecg-module-demo/doc/代码修改日志.log`
- 其他模块在各自 `doc/` 或 `docs/` 目录下查找

## 3. SVN 提交日志

代码和日志文件都修改完成后，提醒用户进行 SVN 提交。**提交日志格式必须与 `代码修改日志` 文件条目保持一致**：

```
--author:作者名--date:YYYYMMDD--for:【bug号/PR号】简要说明
```

**示例：**
```
--author:scott--date:20251030--for:【issues/9450】online导入数据库表时，如果字段有两个下划线则会报错
--author:scott--date:20260424--for:【JHHB-1336】我发起的流程-当前办理人支持多人展示
```

**格式要点：**
- 开头必须是 `--author:` 三段式：`--author:xxx--date:xxx--for:xxx`（短横线 `--` 作分隔）
- `date` 为 `YYYYMMDD`（无横线）
- `for` 字段内 bug 号用中文书名号 `【】` 包裹，常见形式：`【issues/XXXX】`（GitHub 开源）、`【JHHB-XXXX】`（内部 Jira）、`【VUEN-XXXX】`（VUE 专项）、`【QQYUN-XXXX】` 等
- bug 号后直接接简要说明，不加空格也可接空格（两种历史风格都存在，推荐无空格紧贴 `】`）

### ⚠️ Windows 中文 commit 消息防乱码（强制遵守）

**禁止用 `svn commit -m "<中文>"` + `--encoding utf-8` 的写法**。在 Windows (Git Bash/MSYS) 下，shell 会把参数按 GBK (CP936) 传给 svn.exe，而 `--encoding utf-8` 又告诉 SVN "这是 UTF-8"，结果服务端存的是乱码（形如 `�ҷ�...`）。

**✅ 正确做法：commit message 先写入 UTF-8 文件，再用 `-F` 提交**

```bash
# 1. 写入 UTF-8 文件（用 Write 工具，或 printf + iconv）
cat > /tmp/svn_msg.txt <<'EOF'
JHHB-XXXX 简要说明
EOF

# 2. 用 -F 提交，--encoding 指定文件的编码
svn commit -F /tmp/svn_msg.txt --encoding utf-8 "<file1>" "<file2>" 2>&1 | iconv -f GBK -t UTF-8

# 3. 提交完成后删除临时文件
rm /tmp/svn_msg.txt
```

**提交后必须验证**：用 `svn log -l 1 --xml <path> | iconv -f GBK -t UTF-8` 或直接看命令行输出，**肉眼确认** commit message 中的中文没有变成 `�?` 之类的乱码；一旦发现乱码立即用 `svn propset --revprop -r <rev> svn:log "<新msg>"` 修复（需服务端开启 `pre-revprop-change` hook）。

**变通方案（如果服务端不允许改 revprop）**：改用纯 ASCII commit message，中文说明写在 `代码修改日志` 里，例如 `svn commit -m "JHHB-1336 fix multi-assignee display"`。

---

# 二、建表规范

| 规则 | 说明 |
|------|------|
| 主键 | 必须是 `id`，字符串 varchar(32)，唯一索引 |
| 标准字段 | 必须有 `create_by`、`create_time`、`update_by`、`update_time` |
| 字段注释 | 每个字段必须有注释，状态字段注明取值规则如 `'性别 0/男,1/女'` |
| 命名 | 英文单词，多词用下划线连接如 `school_id`，禁止拼音 |
| 类型字段 | 优先用 `varchar(1)` / `varchar(2)`，少用 `int` |
| 索引 | 高频查询字段加索引 |
| 逻辑删除 | 设计 `del_flag` 字段 |

---

# 三、代码质量规范

1. 只做最少的改动，不要破坏SVN对比
2. 禁止提交与功能无关的变更（格式化、空格、缩进调整等）
3. 修改代码同步写好 `代码修改日志（历史记录文件）`
4. 功能变化同步更新文档
5. 方法超过 50 行拆分，抽取共通