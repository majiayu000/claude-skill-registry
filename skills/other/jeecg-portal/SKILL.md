---
name: jeecg-portal
description: >-
  JeecgBoot 门户（Portal）全生命周期管理——通过 API 自动创建、删除、配置门户，管理门户内的 14 种组件（轮播图、新闻动态、系统公告、流程中心、应用快捷入口、协同待办、我的计划、知识库、文本、iframe 等），动态查询数据源并填充组件内容，支持 Web 和 App 双端布局。
  只要用户意图涉及「门户」就必须使用本技能，包括但不限于：
  创建或生成门户（"做一个门户"、"创建门户"、"新增门户"、"生成一个包含轮播图和新闻的门户"、"做一个全组件门户"）、
  删除门户（"删除门户"、"移除XX门户"）、
  修改门户类型（"设为个人工作台"、"设为主门户"、"设为普通门户"、"改门户类型"）、
  管理门户组件（"添加组件"、"加个轮播图"、"加个系统公告"、"删除组件"、"去掉流程中心"）、
  修改组件配置（"修改轮播图配置"、"改标题颜色"、"把新闻动态宽度改为占满一行"、"修改门户里的XX"）、
  查询门户（"查看门户列表"、"有哪些门户"）。
  即使用户没有明确说"门户"二字，只要描述的是 JeecgBoot 系统首页定制、工作台组件配置、portal 相关操作，也应触发此技能。
  关键词触发：门户、portal、工作台、首页定制、门户组件、portalDesign。
---

# JeecgBoot 门户管理技能

通过 JeecgBoot REST API 管理门户系统：创建/删除门户、设置门户类型、添加/删除/配置 14 种门户组件，支持 Web + App 双端。

## 前置条件

需要用户提供：
1. **API 地址**：JeecgBoot 后端地址（如 `http://192.168.x.x:8080/jeecg-boot`）
2. **X-Access-Token**：JWT 登录令牌

如果未提供，提示用户从浏览器 F12 → Network → 任意请求的 Request Headers 中复制。

## 操作类型识别

| 用户意图 | 操作类型 |
|---------|---------|
| 创建/新增/做一个门户 | 新增门户 |
| 删除/移除门户 | 删除门户 |
| 设为个人工作台/普通门户/主门户 | 修改门户类型 |
| 添加组件/加个XX | 添加组件 |
| 删除/移除/去掉组件 | 删除组件 |
| 修改组件配置/改XX颜色/宽度 | 修改组件配置 |
| 查看门户/门户列表 | 查询门户 |

---

## 场景 A：新增门户

### A1. 解析需求

| 信息 | 必填 | 默认值 |
|------|-----|-------|
| 门户名称 | 是 | - |
| 门户编码 | 否 | 名称拼音（小写下划线） |
| 门户类型 | 否 | `common` |
| 包含组件 | 否 | 无 |

### A2. 门户类型

| 类型值 | 显示名 | 约束 |
|-------|-------|------|
| `system` | 主门户 | 系统唯一，管理员设计 |
| `template` | 个人门户模版 | 系统唯一，可被重置 |
| `personal` | 个人工作台 | 用户唯一 |
| `common` | 普通门户 | 无限制 |

### A3. 唯一性校验

创建前必须校验：

```
# 编码唯一性
GET {API_BASE}/sys/duplicate/check?tableName=portal_design&fieldName=code&fieldVal={code}&dataId=
→ success: true 可用，false 已存在

# 类型唯一性（仅 system/template/personal）
GET {API_BASE}/eoa/portalapp/portalDesign/duplicateTypeCheck?portalCategory={type}
→ success: true 可创建
```

### A4. 创建门户

```
POST {API_BASE}/eoa/portalapp/portalDesign/add
Body: { "name": "名称", "code": "编码", "bizMode": "portal", "portalType": "pc,app", "portalCategory": "common", "status": "1", "izDefault": "0" }
→ result 为新门户 ID
```

### A5. 添加组件

创建完成后如果用户指定了组件，进入场景 D 添加组件。

**全组件门户快捷方式**：当用户要求创建包含全部组件的门户时，优先使用 `scripts/build_portal.py` 脚本（`python3 scripts/build_portal.py --api-base {API_BASE} --token {TOKEN} --name {名称}`），或者参考 `references/full-portal-template.md` 手动构建。脚本会自动完成数据源查询、designJson 构建和保存，比手动构建快得多。

---

## 场景 B：删除门户

### B1. 查询列表

```
GET {API_BASE}/eoa/portalapp/portalDesign/list?bizMode=portal&pageNo=1&pageSize=50
```

以表格展示（名称、编码、类型、状态），让用户确认。

**system 和 template 类型不允许删除。**

### B2. 执行删除

```
DELETE {API_BASE}/eoa/portalapp/portalDesign/physicalDelete?id={portalId}
```

---

## 场景 C：修改门户类型

### C1. 查询门户详情

```
GET {API_BASE}/eoa/portalapp/portalDesign/queryById?id={portalId}
```

### C2. 唯一性校验（同 A3）

### C3. 修改

```
POST {API_BASE}/eoa/portalapp/portalDesign/edit
Body: { "id": "ID", "name": "名称", "code": "编码", "portalCategory": "新类型", ...(保留原有字段) }
```

---

## 场景 D：添加组件

### D1. 查询目标门户的 designJson

```
GET {API_BASE}/eoa/portalapp/portalDesign/queryById?id={portalId}
```

### D2. 可用组件（14 种）

| 组件名称 | component 值 | 有配置面板 | 默认 defaultProps |
|---------|-------------|:---------:|-----------------|
| 轮播图 | `JAppCarousel` | 是 | `{ showName: true, autoplay: true, contentPadding: false, textAlign: "center", imgSize: "cover", textFontSize: "default", list: [] }` |
| 新闻动态 | `JCmsNews` | 是 | `{ tabType: 0, noTabsData: [], tabsData: [], showType: 1 }` |
| 系统公告 | `JSystemNotice` | 是 | `{ msgCategory: ["1", "2"], noticeType: [] }` |
| 我的计划 | `JSchedule` | 是 | `{ mobileMaxCount: 3, tabType: 0, singleRange: "week", multiRange: ["week"] }` |
| 近期邮件 | `JEmail` | 否 | 无特有配置 |
| 流程提醒 | `JProcessNotice` | 否 | 无特有配置 |
| 我的申请 | `JMyApplyFlow` | 否 | 无特有配置 |
| 流程中心 | `JMyFlow` | 是 | `{ category: [0,1,2,3], order: [0,1,2,3] }` |
| 知识库 | `JKnowledge` | 是 | `{ tabType: 0, noTabsData: [], tabsData: [] }` |
| 会议 | `JMeeting` | 否 | 无特有配置 |
| 应用快捷入口 | `JAppEnter` | 是 | `{ tabType: 0, noTabsData: { contentSource: 1, infoList: [] }, tabsData: [], styleType: 0, contentIconRadius: "none", ... }` |
| 文本 | `JText` | 是 | `{ showTitleBar: false, text: "文本", fontSize: 16, fontWeight: "normal", color: "#000", textAlign: "center" }` |
| 协同待办 | `JCollaPending` | 是 | `{ category: [0,1,2,3], order: [0,1,2,3] }` |
| iframe | `JIframe` | 是 | `{ frameSrc: "", placeholderImg: "", imgSize: "cover" }` |

### D3. designJson 结构

```json
{
  "webComponentData": [ ... ],
  "appComponentData": [ ... ]
}
```

**Web 端组件结构：**
```json
{
  "i": "32位无横杠UUID",
  "x": 0, "y": 0, "w": 4, "h": 4, "static": false,
  "name": "组件名称",
  "component": "JAppCarousel",
  "icon": "/src/assets/images/portalapp/component-cover/carousel.png",
  "platform": ["WEB", "APP"],
  "defaultProps": { "titleBarColor": "#1890FF", "titleColor": "#000000", ... }
}
```

**App 端组件结构**（比 Web 多 `width` 和 `height`）：
```json
{
  "i": "与Web端相同的UUID",
  "x": 0, "y": 0, "w": 12, "h": 4, "static": false,
  "name": "组件名称", "component": "...", "icon": "...",
  "platform": ["WEB", "APP"],
  "width": "100%", "height": "100%",
  "defaultProps": { ... }
}
```

**icon 对照表：**

| component | icon |
|-----------|------|
| JAppCarousel | `.../carousel.png` |
| JCmsNews | `.../news.png` |
| JSystemNotice | `.../systemNotice.png` |
| JSchedule | `.../schedule.png` |
| JEmail | `.../email.png` |
| JProcessNotice | `.../processNotice.png` |
| JMyApplyFlow | `.../myApplyFlow.png` |
| JMyFlow | `.../myFlow.png` |
| JKnowledge | `.../knowledge.png` |
| JMeeting | `.../meeting.png` |
| JAppEnter | `.../appEnter.png` |
| JText | `.../text.png` |
| JCollaPending | `.../collaPending.png` |
| JIframe | `.../iframe.png` |

icon 路径前缀统一为 `/src/assets/images/portalapp/component-cover/`。

### D4. 布局规则

**Web 端（12 栏网格）：**
- x: 列位置(0-11), y: 行位置, w: 宽度(推荐 4/6/12), h: 高度(推荐 2-8)
- 同行 x + w 不超过 12，不与已有组件重叠
- 默认 w=4, h=4（一行3个），宽组件 w=12

**App 端（单列）：**
- x=0, w=12, y=上一个组件的 y+h+1, 默认 h=4
- 必须含 `width: "100%"` 和 `height: "100%"`

**UUID**：32位无横杠格式，Web/App 同组件共享同一个 `i`。

### D5. 保存 designJson

```
POST {API_BASE}/eoa/portalapp/portalDesign/edit
Body: { "id": "门户ID", "designJson": "{\"webComponentData\":[...],\"appComponentData\":[...]}" }
```

**designJson 的值是字符串化的 JSON**（JSON.stringify 后），不是原始对象。这是因为后端将 designJson 存储为 text 字段。

---

## 场景 E：删除组件

直接执行脚本：
```bash
python3 scripts/modify_component.py --api-base {API_BASE} --token {TOKEN} --portal-id {ID} remove --component JSchedule
```

或按名称删除：`--name "我的计划"`

---

## 场景 F：修改组件配置

直接执行脚本（自动处理双端同步）：
```bash
python3 scripts/modify_component.py --api-base {API_BASE} --token {TOKEN} --portal-id {ID} modify --component JSchedule --props '{"tabType":0,"singleRange":"week"}'
```

也可同时修改布局：`--layout '{"w":12,"h":6}'`

> 需要查具体配置项时，读取 `references/component-configs.md`。

---

## 场景 G：查询门户列表

```
GET {API_BASE}/eoa/portalapp/portalDesign/list?bizMode=portal&pageNo=1&pageSize=50
```

以表格展示：门户名称、编码、类型、状态。

---

## 注意事项

1. **designJson 是字符串**：保存时必须 JSON.stringify，后端 text 字段不接受原始对象
2. **Web/App 联动**：同组件共享 `i`，修改数据属性时双端同步（详见 `references/component-configs.md` 末尾的同步规则表）
3. **system/template 不可删除**：前端和 API 层面都有保护
4. **唯一性校验**：创建 system/template/personal 前必须先校验
5. **编码规则**：以字母开头，可含数字/下划线/横杠，不支持大写
6. **组件布局不重叠**：Web 端添加组件时需计算 x/y/w/h 避免重叠
7. **所有 API 请求**都需要 Header 带 `X-Access-Token`

## 资源文件

| 文件 | 用途 | 何时读取 |
|------|------|---------|
| `references/component-configs.md` | 14种组件的全部配置项详情 | 修改组件配置（场景 F）时 |
| `references/full-portal-template.md` | 全组件门户标准模板（布局、主题色、数据源规则） | 创建全组件门户时 |
| `references/api-reference.md` | 补充 API（默认首页、重置、路由、权限等） | 涉及高级操作时 |
| `scripts/build_portal.py` | 全组件门户一键构建脚本 | 创建全组件门户时直接执行 |
| `scripts/modify_component.py` | 组件配置修改/删除/列表脚本 | 修改、删除组件时直接执行，避免重复写代码 |

## 常用示例

| 用户说法 | 操作 |
|---------|------|
| "创建一个运营门户，包含轮播图和新闻动态" | 新增 + 添加2组件 |
| "创建一个门户包含全组件" | 执行 `scripts/build_portal.py` |
| "删除测试门户" | 查列表 + 确认 + 物理删除 |
| "把XX门户设为个人工作台" | 类型校验 + edit |
| "给首页门户加一个系统公告组件" | 添加组件到 designJson |
| "修改首页门户的轮播图，设置自动播放关闭" | 修改 defaultProps.autoplay |
| "把流程中心去掉" | 删除组件 |
| "查看当前有哪些门户" | 列表查询 |
