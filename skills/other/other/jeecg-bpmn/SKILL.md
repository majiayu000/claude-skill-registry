---
name: jeecg-bpmn
description: Use when user asks to create/generate a BPM workflow, design a Flowable BPMN process, or says "创建流程", "生成流程", "新建流程", "设计流程", "画流程", "审批流程", "工作流", "BPM", "BPMN", "create flow", "create process", "new workflow", "generate workflow". Also triggers when user describes an approval chain like "先经理审批再HR审批" or mentions process nodes like "开始→审批→网关→结束". Also triggers for OA application creation: "创建OA应用", "创建审批单", "创建报销单", "创建请假单", "做一个OA表单带流程", "一键创建表单和流程", "create OA app", "create approval form with workflow".
---

# JeecgBoot BPM 流程自动生成器

将自然语言的流程描述转换为 Flowable BPMN 2.0 XML，并通过 API 在 JeecgBoot 系统中自动创建流程。

## 介绍组件时的完整性要求

> **重要：** 当用户要求介绍流程设计器各组件时，必须包含以下内容，不可遗漏：
>
> 1. **会签节点**：串行/并行两种模式；全部通过/一人通过/半数通过/按比例/自定义 5种通过规则；指定人员/角色/审批角色/部门/岗位/职级/表单字段/流程变量 8种审批人类型
> 2. **条件表达式**：系统内置流程变量（`result`、`applyUserId`、`applyDate` 等）；13种条件运算符；多条件组合用法（AND/OR）
> 3. **监听器**：执行监听器/任务监听器/全局事件监听器三种类型；系统预置监听器（ProcessEndListener必需、TaskSkipApprovalListener、TaskCreatedAutoSubmitListener等）；taskExtendJson 节点行为控制字段说明

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://api3.boot.jeecg.com`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

如果用户未提供，提示：
> 请提供 JeecgBoot 后端地址和 X-Access-Token（从浏览器 F12 → Network → 任意请求的 Request Headers 中复制）。

## 后端项目路径（本地环境）

> 当需要自动创建 Java 类时，从记忆中读取后端项目路径。若记忆中无此信息，询问用户：
> "请提供后端项目根目录路径（如 D:\path\to\jeecg-boot-framework），用于自动创建 Java 服务类。"

## 主数据复用规则

> **重要：** 配置审批人（角色、用户、部门）或字典时，必须遵循"先查后建"原则。
> 使用 `jeecg-system` skill 的 `system_utils.py` 查询和管理主数据。
> 详见 `../jeecg-system/SKILL.md`。

## 交互流程

### Step 0: 解析用户需求

从用户描述中提取以下信息：

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 流程名称 | 用户指定或自动生成 | "员工请假审批流程" |
| 流程类型 | `oa` | 字典 `bpm_process_type` 的值 |
| 节点列表 | 从描述中解析 | 开始→员工提交→经理审批→HR审批→结束 |
| 网关逻辑 | 从描述中解析 | "通过→下一步，拒绝→结束" |
| 审批人配置 | 从描述中解析 | assignee/candidateUsers/candidateGroups/表达式 |

### Step 0.5: 识别「代码生成 + 审批流程」联合创建场景

**触发条件（满足任一即触发）：**
- 用户说"用代码生成创建审批"、"代码生成一个XXX审批单"、"生成代码并配置流程"
- 用户明确选择 `formType=3`（自定义开发表单）作为流程关联表单
- 用户描述中同时包含"建表/CRUD/代码生成" + "审批/流程/BPM"
- 代码生成完成后，用户紧接着要求创建流程

> **重要（用户明确规则）：** 代码生成完成后直接进入流程创建，**跳过 Step 2 的流程摘要确认**，无需再次展示摘要等待用户确认，直接执行角色查询、BPMN 配置生成和 API 调用。用户在代码生成阶段已完成整体确认，流程创建是连续操作，中间的二次确认是多余的打断。

**联合创建流程（必须按顺序执行）：**

**第 1 步：告知用户并调用 `jeecg-codegen` skill 生成 CRUD 代码**

> 告知用户："检测到您需要代码生成 + 审批流程，将先调用代码生成 skill 生成 CRUD 代码（含 bpm_status 字段），再创建审批流程。"

调用 jeecg-codegen skill 时，在需求描述中明确追加以下要求：
- 实体必须包含 `bpm_status` 字段（`@Dict(dicCode = "bpm_status")`，varchar(10)）
- 需要生成 `Form.vue`（BPM 流程审批表单组件）
- `List.vue` 需包含"发起流程"和"审批进度"功能
- `Modal.vue` 需将 `formSchema` 替换为 `getBpmFormSchema({})`

**第 2 步：收集代码生成结果，确定流程关联参数**

从 jeecg-codegen 输出中获取：
- `tableName`（数据库表名） → 用作 `formTableName` 和 `relationCode`
- `viewDir`（前端视图目录） → 用作 `formUrl` 路径前缀
- `entityName`（实体名） → 用作 `formUrl` 中的组件名

**第 3 步：使用 `formType=3` 创建 BPM 流程**

在 JSON 配置的 `formLink` 中使用：
```json
{
  "formLink": {
    "formType": "3",
    "relationCode": "dev_{tableName}_001",
    "formTableName": "{tableName}",
    "flowStatusCol": "bpm_status",
    "titleExp": "${关键字段名}提交的{业务名}"
  }
}
```

草稿节点（`draft: true`）表单地址（Step 5.5 需要）：
```
modelAndView: "{viewDir}/components/{entityName}Form?edit=1"
modelAndViewMobile: ""
```

> **注意：** `formType=3` 不需要发起授权步骤（跳过 Step 5），但必须完成 Step 5.5（草稿节点表单地址配置）。

---

### Step 1: 识别节点并构建流程结构

**支持的节点类型：**

| 用户描述关键词 | BPMN 节点类型 | XML 元素 |
|---------------|---------------|----------|
| 开始 | 开始事件 | `startEvent` |
| 结束 | 结束事件 | `endEvent` |
| 审批/审核/处理/提交 | 用户任务 | `userTask` |
| 条件判断/分支/通过或拒绝 | 排他网关（条件分支） | `exclusiveGateway` |
| **手工分支/意见分支/选择分支** | **userTask 多出线（无条件）** | **无网关，直接从 userTask 引出多条 sequenceFlow** |
| 同时/并行 | 并行网关 | `parallelGateway` |
| 条件并行/部分并行 | 包含网关 | `inclusiveGateway` |
| **子流程/嵌套/扩展子流程** | **内嵌子流程** | **`subProcess`** — 详见 `references/bpmn-call-activity.md` 内嵌子流程章节 |
| **调用子流程/主子流程** | **调用子流程** | **`callActivity`** — 详见 `references/bpmn-call-activity.md` |
| 会签子流程 | 调用子流程+多实例 | `callActivity` + `multiInstance` |
| **Java服务/表达式执行/调用Bean** | **Java 服务节点** | **`serviceTask`** — `bpmn_creator.py` 原生支持，见下方「serviceTask 配置」 |
| **AI流程编排/AIGC调用** | **AI 服务节点** | **`aiTask`** — `bpmn_creator.py` 原生支持，见下方「aiTask 配置」 |
| **调用外部HTTP接口** | **API 服务节点** | **`apiTask`** — `bpmn_creator.py` 原生支持，见下方「apiTask 配置」 |
| **节点超时/定时触发** | **边界定时器事件** | **`timer`** 字段附加在 `userTask` 上 — `bpmn_creator.py` 原生支持，见下方「timer 边界定时器」 |
| **脚本节点/执行脚本/Groovy/JS脚本** | **脚本节点** | **`scriptTask`** — `bpmn_creator.py` 原生支持，见下方「scriptTask 配置」 |
| **等待信号/捕获信号/接收广播** | **信号捕获事件** | **`signalCatch`** — 中断等待匹配信号，见下方「信号与消息事件配置」 |
| **发出信号/广播信号/抛出信号** | **信号抛出事件** | **`signalThrow`** — 向所有订阅者广播信号，见下方「信号与消息事件配置」 |
| **任务上挂信号/信号边界** | **信号边界事件** | **`signalBoundary`** 字段附加在 `userTask` 上，见下方「信号与消息事件配置」 |
| **等待消息/捕获消息/接收消息** | **消息捕获事件** | **`messageCatch`** — 中断等待唯一消息，见下方「信号与消息事件配置」 |
| **发出消息/抛出消息/调用外部系统** | **消息抛出事件** | **`messageThrow`** — 发送内部消息或调用外部接口，见下方「信号与消息事件配置」 |
| **任务上挂消息/消息边界** | **消息边界事件** | **`messageBoundary`** 字段附加在 `userTask` 上，见下方「信号与消息事件配置」 |

> **手工分支 vs 条件分支：** 条件分支使用 `exclusiveGateway` + 条件表达式自动判断走哪条线；手工分支（也叫意见分支）不使用网关，而是从一个 userTask 直接引出多条无条件的 sequenceFlow，用户在审批时手动选择走哪条线，线的名称显示为选项。详见 `references/bpmn-manual-branch.md`。
>
> **手工分支使用前提：** 手工分支仅在通过/拒绝后还需要经过不同的后续处理节点时才使用。如果审批节点后没有其他节点、只有结束节点，则**不需要手工分支**，直接一条线连到结束即可。分支的意义是让不同审批结果走不同路径，如果通过和拒绝都直接到结束，分支没有实际意义。

**审批人配置映射（8 种类型 + 扩展，基于 `references/example/审批人员.bpmn` 实测验证）：**

| 用户描述 | JSON assignee type | BPMN XML 属性 | 说明 |
|----------|-------------------|---------------|------|
| "发起人/申请人" | `expression` + `applyUserId` | `flowable:assignee="${applyUserId}"` | 流程发起人自动填充 |
| "admin/指定用户名" | `assignee` | `flowable:assignee="admin"` | 固定指定人 |
| "张三或李四" | `candidateUsers` | `flowable:candidateUsers="zhangsan,lisi"` | 多候选人（固定用户名） |
| "部门负责人（表达式）" | `candidateUsersExpression` | `flowable:candidateUsers="${flowNodeExpression.getDepartLeaders(applyUserId)}"` | 候选人表达式 |
| "经理角色/角色组" | `role` | `flowable:candidateGroups="admin,vue3" groupType="role"` | 系统角色 |
| "审批角色" | `approvalRole` | `flowable:candidateUsers="${flowUtil.getUsersByApprRole(...)}" groupType="approvalRole"` | 审批专用角色（**注意用 candidateUsers**） |
| "某部门审批" | `dept` | `flowable:candidateGroups="部门ID" groupType="dept"` | 部门 |
| "某岗位审批" | `deptPosition` | `flowable:candidateGroups="岗位ID" groupType="deptPosition"` | 岗位 |
| "职级审批" | `position` | `flowable:candidateUsers="${oaFlowExpression.getApplyUserDeptPositionLevel(...)}" groupType="position"` | 职务级别（**注意用 candidateUsers**） |
| "提交/填写/草稿" | `expression` + `draft: true` | `flowable:assignee="${applyUserId}"` + `sameMode=0` + `AutoSubmitListener` | 首节点（由发起人对自己审批 + 自动提交监听） |
| "上一节点指派" | `assignedByPrev: true` | `isAssignedByPreviousNode=true` | 上一审批人选择 |
| "会签/多人同时审批" | `callActivity` + `countersign` | `multiInstance` + `flowUtil.stringToList` | 并行/顺序会签 |

> **重要区别：** `approvalRole` 和 `position` 类型使用 `candidateUsers`（不是 `candidateGroups`），value 传 ID，脚本自动包装为表达式。`role`/`dept`/`deptPosition` 使用 `candidateGroups`。参考 `references/example/审批人员.bpmn`。

**审批人数据查询：** 当用户提到具体角色/用户/部门名称时，可查数据库获取准确编码：
- 角色编码：`SELECT role_code, role_name FROM sys_role`
  - **创建系统角色**：`POST /sys/role/add`，body: `{"roleName":"角色名","roleCode":"role_code","description":"..."}`
  - **创建角色后默认添加 admin 为成员**：`POST /sys/user/addSysUserRole`，body: `{"roleId":"{roleId}","userIdList":["e9ca23d68d884d4ebb19d07889727dae"]}`（admin 固定 ID）
- 用户名：`SELECT username, realname FROM sys_user`
- 部门/岗位ID：`SELECT id, depart_name, org_category FROM sys_depart`（org_category: 1=公司, 2=部门, 3=岗位, 4=子公司）
- 审批角色ID：`GET /sys/approvalRole/search?keyword=` 查询（返回 `result.roles[]`，取 `id` 字段）
  - 查询分组列表：`GET /sys/approvalRole/rootList?pageNo=1&pageSize=50`
  - 查询分组下角色：`GET /sys/approvalRole/childList?pid={groupId}`
  - **创建分组**：`POST /sys/approvalRole/group/add`，body: `{"name":"分组名", "pid":"0"}`
  - **创建审批角色**：`POST /sys/approvalRole/role/add`，body: `{"name":"角色名", "pid":"{groupId}"}`
  - **绑定用户**：`POST /sys/approvalRoleUser/add`，body: `{"approvalRoleId":"{roleId}", "userIds":["{userId}"], "bizScope":"all", "includeSub":0}`

### serviceTask 配置（Java 服务节点）

`bpmn_creator.py` 原生支持 `serviceTask`，直接在 nodes 数组中配置即可，无需额外编写脚本。

**JSON 节点配置：**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | 是 | - | 节点唯一ID |
| `type` | 是 | - | 固定为 `serviceTask` |
| `name` | 是 | - | 节点名称 |
| `serviceType` | 否 | `expression` | `expression` / `class` / `delegateExpression` |
| `expression` | serviceType=expression 时 | - | UEL 表达式，如 `${myBean.doWork(execution)}` |
| `className` | serviceType=class 时 | - | Java 全类名 |
| `delegateExpr` | serviceType=delegateExpression 时 | - | 委托表达式 |
| `resultVar` | 否 | - | 把表达式返回值存入该流程变量（仅 expression 类型） |

**三种类型示例：**

```json
// 表达式（最常用）
{"id": "svc1", "type": "serviceTask", "name": "测试服务节点",
 "serviceType": "expression", "expression": "${testExpression.test()}"}

// Java 类
{"id": "svc2", "type": "serviceTask", "name": "Java服务",
 "serviceType": "class", "className": "com.example.MyJavaDelegate"}

// 委托表达式
{"id": "svc3", "type": "serviceTask", "name": "委托服务",
 "serviceType": "delegateExpression", "delegateExpr": "${myDelegate}"}

// 带返回值（存入流程变量）
{"id": "svc4", "type": "serviceTask", "name": "计算服务",
 "serviceType": "expression", "expression": "${calcService.calc(execution)}",
 "resultVar": "calcResult"}
```

> **注意：** serviceTask 节点不需要配置审批人，不会出现在节点选择列表（nodes 参数）中，纯粹由引擎自动执行后流转到下一节点。

---

### serviceTask 自动创建 Java 类（用户未提供类名/表达式时）

> **触发条件：** 用户要配置 serviceTask 但没有提供 `className`、`expression` 或 `delegateExpr` 时，**必须按以下步骤自动创建 Java 类**，不能使用占位符或留空。

#### 自动创建流程

**Step A：确定后端项目路径**

从记忆（MEMORY.md）读取后端项目路径。如无记忆，询问用户并保存到记忆。

**Step B：查找 servicetask 包路径**

在后端项目中查找已有的 servicetask 包（包含 `JavaDelegate` 实现类的目录）：

```
Glob: **/servicetask/*.java  →  提取包名和目录路径
```

如未找到，在 BPM 模块（含 `joa-flowable` 或 `bpm-flowable` 关键字的模块）下创建 `servicetask` 包。

参考包结构（来自本地项目实测）：
```
jeecg-boot-module-joa-flowable
  └─ src/main/java/org/jeecg/modules/servicetask/
       ├─ TestDelegateExpression.java   ← 参考模板
       └─ TestClass.java
```

**Step C：根据流程 processKey 推导类名**

类名规则：将 processKey 转为大驼峰 + `ServiceTask` 后缀。

| processKey | 推导类名 |
|-----------|---------|
| `oa_doc_countersign_process` | `OaDocCountersignProcessServiceTask` |
| `leave_apply` | `LeaveApplyServiceTask` |
| `contract_approval` | `ContractApprovalServiceTask` |

Spring Bean 名（委托表达式）：类名首字母小写，如 `${oaDocCountersignProcessServiceTask}`。

**Step D：创建 Java 类文件**

使用 Write 工具在 Step B 确定的目录下创建类文件：

```java
package org.jeecg.modules.servicetask;

import lombok.extern.slf4j.Slf4j;
import org.flowable.engine.delegate.DelegateExecution;
import org.flowable.engine.delegate.JavaDelegate;
import org.springframework.stereotype.Component;

/**
 * {流程中文名} - {节点名称}服务节点
 * 流程编码：{processKey}
 */
@Slf4j
@Component
public class {ClassName} implements JavaDelegate {

    @Override
    public void execute(DelegateExecution execution) {
        String processInstanceId = execution.getProcessInstanceId();
        String businessKey = execution.getProcessInstanceBusinessKey();
        log.info("======== {ClassName} 执行 ========= processInstanceId={}, businessKey={}",
                processInstanceId, businessKey);
        // TODO: 在此处添加业务逻辑
    }
}
```

**Step E：配置 serviceTask JSON**

类创建后，自动填入 serviceTask 配置：

```json
{
  "id": "svc_{processKey_short}",
  "type": "serviceTask",
  "name": "{节点名称}",
  "serviceType": "delegateExpression",
  "delegateExpr": "${beanName}"
}
```

**Step F：告知用户**

流程创建完成后，告知用户已自动创建的类：

```
已自动创建 Java 服务类：
  路径：{完整文件路径}
  类名：{ClassName}
  Bean：{beanName}
  委托表达式：${beanName}

请在 execute() 方法中填写您的业务逻辑。
```

---

### aiTask 配置（AI 流程编排节点）

`bpmn_creator.py` 原生支持 `aiTask`，对应 JeecgBoot AIGC 流程编排服务任务。底层是 `serviceTask` + `AigcServiceTaskDelegate`，直接在 nodes 数组中配置即可。

**JSON 节点配置：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 节点唯一ID |
| `type` | 是 | 固定为 `aiTask` |
| `name` | 是 | 节点名称 |
| `aiFlowId` | 是 | AIGC 流程 ID（从系统 AIGC 流程管理页面获取） |
| `inputParamsList` | 否 | 输入参数映射，将流程变量传入 AI 流程，如 `[{"key": "content", "value": "${name}"}]` |
| `outputParamsList` | 否 | 输出参数映射，将 AI 流程输出存入流程变量，如 `[{"key": "result", "value": "aiResult"}]` |

**示例：**

```json
{
  "id": "task_ai",
  "type": "aiTask",
  "name": "AI内容生成",
  "aiFlowId": "2034580389262573569",
  "inputParamsList": [
    {"key": "content", "value": "${userName}"}
  ],
  "outputParamsList": [
    {"key": "summary", "value": "aiSummary"}
  ]
}
```

> **生成的 XML 结构：** `serviceTask` + `flowable:class="org.jeecg.modules.extbpm.listener.service.AigcServiceTaskDelegate"` + 扩展元素 `<flowable:aiServiceTaskConfig value="{base64编码的配置JSON}" />`
>
> **注意：** `aiTask` 与 `serviceTask` 一样不需要配置审批人，由引擎自动调用 AI 流程后流转到下一节点。`aiFlowId` 从系统「AIGC > 流程编排」管理页面获取。

---

### timer 边界定时器（附加在 userTask 上）

在任意 `userTask` 节点中添加 `timer` 字段，即可附加边界定时器事件。定时器触发时节点被中断，可路由到其他节点（如超时直接结束）。

**`timer` 字段说明：**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `type` | 是 | `duration` | `date`=指定日期 / `duration`=等待时长 / `cycle`=重复周期 |
| `value` | 是 | — | 定时器值，支持 ISO 8601 / cron 表达式 / `${var}` 流程变量 |
| `timerTarget` | 否 | — | 定时器触发后流转到的节点ID（不填则只附加定时器，不添加出线） |
| `eventId` | 否 | `timer_{nodeId}` | 边界事件ID，默认自动生成 |
| `timerFlowId` | 否 | `flow_{eventId}` | 超时连线ID，默认自动生成 |

**三种类型详细说明：**

**① `date` — 指定日期（一次性）**

到达指定时间点触发，格式：`yyyy-MM-ddTHH:mm:ss`

```
2026-04-03T15:00:59
```

**② `duration` — 等待时长**

节点激活后等待指定时长触发，使用 ISO 8601 Duration 格式，**支持 `${var}` 表达式**：

| 示例值 | 含义 |
|--------|------|
| `PT1M` | 1分钟后 |
| `PT10M` | 10分钟后 |
| `PT1H` | 1小时后 |
| `P1D` | 1天后 |
| `P1W` | 1周后 |
| `P1M` | 1个月后 |
| `P1Y2M10DT2H30M` | 1年2月10天2小时30分后 |
| `${duration}` | 从流程变量中取值 |

> ISO 8601 格式：`P[年Y][月M][日D]T[时H][分M][秒S]`，`T` 是日期和时间的分隔标记，无年月日时 `T` 不能省略（如 `PT1H` 而不是 `P1H`）

**③ `cycle` — 重复周期**

支持两种格式：

**格式一：ISO 8601 重复格式（推荐）**

```
R{次数}/{开始时间}/{间隔}   完整格式
R{次数}/{间隔}             省略开始时间
```

| 示例值 | 含义 |
|--------|------|
| `R3/PT10H` | 每隔10小时重复3次 |
| `R/PT1H` | 每小时无限重复（R 不带数字=无限） |
| `R3/2026-04-03T15:00:00/P1D` | 从指定时间开始，每天重复3次 |
| `${cronExpr}` | 从流程变量中取值 |

**格式二：Cron 表达式**

```
0 0/5 * * * ?      每5分钟执行一次（从整点开始）
0 0 12 * * ?       每天12点执行
0 0/30 9-18 * * ?  工作时间每30分钟执行
```

**示例配置：**

```json
// 等待1天超时跳转结束
{
  "timer": {"type": "duration", "value": "P1D", "timerTarget": "end"}
}

// 从流程变量取超时时间
{
  "timer": {"type": "duration", "value": "${approvalTimeout}", "timerTarget": "end"}
}

// 每5分钟催办一次，共3次
{
  "timer": {"type": "cycle", "value": "R3/PT5M"}
}

// 每5分钟执行（cron格式）
{
  "timer": {"type": "cycle", "value": "0 0/5 * * * ?"}
}

// 指定日期截止
{
  "timer": {"type": "date", "value": "2026-12-31T23:59:59", "timerTarget": "end"}
}
```

> **边界事件自动定位**在任务节点右下角（符合 BPMN 设计器规范）。
> `timerTarget` 可以指向任何已存在的节点ID，通常为结束节点或专门的超时处理节点。

---

### apiTask 配置（API 服务节点）

`bpmn_creator.py` 原生支持 `apiTask`，用于在流程中调用内部或外部 HTTP 接口。底层是 `serviceTask` + `ApiServiceTaskDelegate`。

**JSON 节点配置：**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | 是 | — | 节点唯一ID |
| `type` | 是 | — | 固定为 `apiTask` |
| `name` | 是 | — | 节点名称 |
| `apiUrl` | 是 | — | 接口路径，如 `/sys/user/list`，支持 `${var}` 引用流程变量 |
| `method` | 否 | `GET` | HTTP 方法：`GET` / `POST` / `PUT` / `DELETE` |
| `headersList` | 否 | `[]` | 请求头列表，如 `[{"key": "Content-Type", "value": "application/json"}]` |
| `inputParamsList` | 否 | `[]` | 请求参数，支持流程变量，如 `[{"key": "name", "value": "${contactName}"}]` |
| `outputParamsList` | 否 | `[]` | 响应结果映射到流程变量，支持 JSONPath，如 `[{"key": "result.records[0].id", "value": "userId"}]` |
| `timeout` | 否 | `30000` | 超时时间（毫秒） |
| `retryCount` | 否 | `3` | 失败重试次数 |

**示例：**

```json
{
  "id": "task_api",
  "type": "apiTask",
  "name": "查询会议室",
  "apiUrl": "/eoa/meeting/eoaMeetingRoom/list",
  "method": "GET",
  "inputParamsList": [
    {"key": "pageNo", "value": "1"},
    {"key": "pageSize", "value": "10"},
    {"key": "name", "value": "${roomName}"}
  ],
  "outputParamsList": [
    {"key": "result.records[0].name", "value": "firstRoomName"}
  ],
  "timeout": 30000,
  "retryCount": 3
}
```

> **`outputParamsList` 的 `key`** 使用 JSONPath 语法引用响应体字段（如 `result.records[0].name`），`value` 是存入流程变量的名称，后续节点可通过 `${firstRoomName}` 引用。
>
> **注意：** `apiTask` 与 `serviceTask` 一样不需要配置审批人，由引擎自动执行后流转。

---

### apiTask 自动创建 API 接口（用户未提供 apiUrl 时）

> **触发条件：** 用户要配置 apiTask 但没有提供 `apiUrl` 时，**必须按以下步骤自动创建后端 Controller 接口**，不能使用占位符或留空。

#### 自动创建流程

**Step A：确定后端项目路径**

从记忆（MEMORY.md）读取后端项目路径。如无记忆，询问用户并保存到记忆。

**Step B：查找业务相关的 Controller**

在后端项目中按流程的业务模块查找已有 Controller：

```
Glob: **/controller/**/*Controller.java  →  找到同业务模块的 Controller
```

优先顺序：
1. 与流程 processKey 同名/同业务的 Controller（如 `oa_doc_countersign_process` → 找 `*DocCountersign*Controller.java`）
2. 同包下其他业务 Controller（如 `/joa/controller/`）作为**新建参考模板**

**Step C：推导接口路径与方法名**

根据流程 processKey 和节点名称推导：

| 要素 | 规则 | 示例 |
|------|------|------|
| Controller 类名 | 业务名大驼峰 + `Controller` | `JoaDocCountersignController` |
| 包路径 | 与同模块已有 Controller 同包 | `org.jeecg.modules.joa.controller` |
| RequestMapping | `/joa/{camelCase业务名}` | `/joa/joaDocCountersign` |
| 方法名 | 根据节点名称推导（`afterSubmit`/`notify`/`callback` 等） | `afterSubmit` |
| 请求方法 | 有副作用操作用 `POST`，纯查询用 `GET` | `POST` |
| 接口路径 | `/{RequestMapping}/{方法名}` | `/joa/joaDocCountersign/afterSubmit` |

**Step D：判断创建还是追加**

- 如果目标 Controller **已存在** → 在文件末尾的 `}` 前追加新方法（用 Edit 工具）
- 如果目标 Controller **不存在** → 用 Write 工具新建 Controller 文件

**新建 Controller 模板：**

```java
package {package};

import lombok.extern.slf4j.Slf4j;
import org.jeecg.common.api.vo.Result;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * {业务中文名} - 流程服务接口
 * 流程编码：{processKey}
 */
@Slf4j
@RestController
@RequestMapping("{requestMapping}")
public class {ClassName} {

    /**
     * {节点名称}回调接口（流程 apiTask 节点调用）
     *
     * @param businessKey       业务主键（流程变量 ${businessKey}）
     * @param processInstanceId 流程实例ID（流程变量 ${processInstanceId}）
     */
    @PostMapping("{methodPath}")
    public Result<?> {methodName}(
            @RequestParam(required = false) String businessKey,
            @RequestParam(required = false) String processInstanceId) {
        log.info("===== {ClassName} {methodName} ===== businessKey={}, processInstanceId={}",
                businessKey, processInstanceId);
        // TODO: 在此处添加业务逻辑
        return Result.OK("处理成功");
    }
}
```

**Step E：配置 apiTask JSON**

接口创建后，自动填入 apiTask 配置：

```json
{
  "id": "api_{processKey_short}",
  "type": "apiTask",
  "name": "{节点名称}",
  "apiUrl": "{接口路径}",
  "method": "POST",
  "inputParamsList": [
    {"key": "businessKey",       "value": "${businessKey}"},
    {"key": "processInstanceId", "value": "${processInstanceId}"}
  ],
  "outputParamsList": [],
  "timeout": 30000,
  "retryCount": 3
}
```

**Step F：告知用户**

流程创建完成后，告知用户已自动创建的接口：

```
已自动创建 API 接口：
  文件路径：{完整文件路径}
  接口地址：POST {apiUrl}
  Controller：{完整类名}#{methodName}
  入参：businessKey（业务主键）、processInstanceId（流程实例ID）

请在方法体中填写您的业务逻辑。
```

---

### scriptTask 配置（脚本节点）

`bpmn_creator.py` 原生支持 `scriptTask`，直接在 nodes 数组中配置即可。

**JSON 节点配置：**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | 是 | - | 节点唯一ID |
| `type` | 是 | - | 固定为 `scriptTask` |
| `name` | 是 | - | 节点名称 |
| `scriptFormat` | 否 | `javascript` | 脚本语言：`javascript` / `groovy` / `juel` |
| `script` | 是 | - | 脚本内容（含 `<` `>` `&` 等特殊字符时自动用 CDATA 包裹） |
| `resultVar` | 否 | - | 把脚本返回值存入该流程变量 |

**示例：**

```json
// JavaScript 脚本
{"id": "script_node", "type": "scriptTask", "name": "脚本节点",
 "scriptFormat": "javascript",
 "script": "var sum = 2 + 9;\nexecution.setVariable(\"myVar\", sum);"}

// Groovy 脚本（带返回值）
{"id": "script_calc", "type": "scriptTask", "name": "计算脚本",
 "scriptFormat": "groovy",
 "script": "execution.getVariable('amount') * 0.1",
 "resultVar": "tax"}

// 含特殊字符（自动 CDATA 包裹）
{"id": "script_cond", "type": "scriptTask", "name": "条件脚本",
 "scriptFormat": "javascript",
 "script": "if (amount > 1000) { execution.setVariable('flag', true); }"}
```

> **支持的脚本语言：** `javascript`（JDK 内置，最常用）、`groovy`（需引入依赖）、`juel`（UEL 表达式语言）
>
> **注意：** scriptTask 与 serviceTask 一样不需要配置审批人，由引擎自动执行后流转。

---

### 信号与消息事件配置

#### 信号事件（Signal Event）概述

信号是**广播**机制，同一信号可以有**多个订阅者**，所有匹配的订阅者都会被触发。信号被捕获后**不会被消耗**。

| 事件类型 | XML 元素 | 触发方式 | 说明 |
|---------|---------|---------|------|
| 信号捕获事件 | `intermediateCatchEvent` + `signalEventDefinition` | 引擎自动（等待匹配信号） | 流程暂停等待信号 |
| 信号抛出事件 | `intermediateThrowEvent` + `signalEventDefinition` | 引擎自动（执行到节点即广播） | 发出信号后继续流转 |
| 信号边界事件 | `boundaryEvent` + `signalEventDefinition` | 引擎自动（等待附属任务期间） | 附加在 userTask 上 |

**信号 vs 消息的关键区别：**

| 特性 | 信号（Signal） | 消息（Message） |
|------|--------------|----------------|
| 订阅者 | **多个**（广播） | **唯一一个** |
| 消耗 | 捕获后**不消耗**，所有订阅者都收到 | 消耗后只有一个订阅者处理 |
| 作用范围 | **全局**（可跨流程实例） | 通过关联规则确定唯一订阅者 |
| 匹配规则 | 可选（匹配规则不同则忽略） | **必选**（`消息名 + 捕获规则` 全局唯一） |

#### 信号捕获事件（Signal Intermediate Catching Event）

执行到此节点时暂停，等待流程内的抛出信号事件或 API 发出匹配信号后继续。

**JSON 节点配置：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 节点唯一ID |
| `type` | 是 | 固定为 `signalCatch` |
| `name` | 是 | 节点名称 |
| `signalName` | 是 | 要订阅的信号名（与抛出事件/API 保持一致） |
| `matchRule` | 否 | 可选匹配规则，如 `vip`；信号名相同但规则不匹配则忽略 |

**JSON 示例：**
```json
{
  "id": "signal_catch_1",
  "type": "signalCatch",
  "name": "等待CRM订单信号",
  "signalName": "CRM-Order",
  "matchRule": "vip"
}
```

> **注意：** 信号捕获事件由引擎自动触发，不需要额外调用 API。

#### 信号抛出事件（Signal Intermediate Throwing Event）

执行到此节点时，向系统内部广播一个信号，所有匹配的订阅者（信号捕获事件、信号边界事件）都会被触发，之后流程继续。

**JSON 节点配置：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 节点唯一ID |
| `type` | 是 | 固定为 `signalThrow` |
| `name` | 是 | 节点名称 |
| `signalName` | 是 | 要发出的信号名 |
| `matchRule` | 否 | 可选匹配规则；订阅者规则不同则不处理 |

**JSON 示例：**
```json
{
  "id": "signal_throw_1",
  "type": "signalThrow",
  "name": "发出审批完成信号",
  "signalName": "ApprovalDone"
}
```

> **同一信号可被多个订阅者接收。** 信号边界事件具有全局作用域（广播），可接收来自任何流程实例发出的信号，甚至跨不同流程实例。

#### 信号边界事件（Signal Boundary Interrupting Event）

附加在 `userTask` 上，在任务执行期间等待匹配信号。收到信号后中断任务（或非中断模式），按后继路线继续。

**在 userTask 节点上添加 `signalBoundary` 字段：**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `signalName` | 是 | — | 要订阅的信号名 |
| `matchRule` | 否 | — | 可选匹配规则 |
| `cancelActivity` | 否 | `true` | `true`=中断型（中断依附的任务），`false`=非中断型 |
| `boundaryTarget` | 否 | — | 触发后路由到的节点 ID |
| `eventId` | 否 | `signal_boundary_{nodeId}` | 边界事件ID |

**JSON 示例：**
```json
{
  "id": "task_approval",
  "type": "userTask",
  "name": "经理审批",
  "assignee": {"type": "role", "value": "manager"},
  "signalBoundary": {
    "signalName": "CancelOrder",
    "cancelActivity": true,
    "boundaryTarget": "end"
  }
}
```

> **重要特性：** 信号边界事件为**全局作用域**，不限于当前流程范围。不同流程实例发出的相同信号也能触发此边界事件。信号被捕获后**不会消耗**，多个活跃的信号边界事件订阅同一信号时，全部都会被触发。

---

#### 消息事件（Message Event）概述

消息是**单播**机制，每条消息只允许**唯一一个**订阅者。通过 `消息名 + 关联规则` 确定唯一订阅者。

**配置消息的前提：** 必须在流程属性的 `消息` 中定义消息变量名，确保消息变量名与订阅/抛出事件一致。

#### 消息捕获事件（Message Intermediate Catch Event）

执行到此节点时暂停，等待匹配消息后继续。与信号不同，每条消息只允许一个订阅者，关联规则用于确定唯一目标。

**JSON 节点配置：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 节点唯一ID |
| `type` | 是 | 固定为 `messageCatch` |
| `name` | 是 | 节点名称 |
| `messageName` | 是 | 要订阅的消息名（需与流程属性中定义的变量名一致） |
| `correlationKey` | 是 | **必选**关联规则，如订单号 `201702040007`，与消息名组合保证全局唯一 |

**JSON 示例：**
```json
{
  "id": "msg_catch_1",
  "type": "messageCatch",
  "name": "等待Alibaba订单消息",
  "messageName": "Alibaba-B2B-Order",
  "correlationKey": "201702040007"
}
```

> **唯一性要求：** `消息名 + 关联规则` 必须全局唯一，否则存在多个订阅者会导致匹配异常。消息捕获事件由引擎自动触发，无需额外 API 调用。

#### 消息抛出事件（Message Intermediate Throwing Event）

执行到此节点时，向系统内部发送一条消息（内部消息）或调用外部系统接口，之后继续流转。

**JSON 节点配置：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 节点唯一ID |
| `type` | 是 | 固定为 `messageThrow` |
| `name` | 是 | 节点名称 |
| `messageName` | 是 | 要发出的消息名（需在流程属性中定义，与订阅事件的消息名一致） |

**JSON 示例：**
```json
{
  "id": "msg_throw_1",
  "type": "messageThrow",
  "name": "发送订单确认消息",
  "messageName": "Alibaba-B2B-Order"
}
```

> **同一消息只允许一个订阅者。** 抛出前必须在流程属性的「消息」中定义消息变量名，并确保消息变量名、关联规则与订阅端完全一致。

#### 消息边界事件（Message Boundary Interrupting Event）

附加在 `userTask` 或子流程上，在任务执行期间等待匹配消息。可以是中断型（默认）或非中断型。

**在 userTask 节点上添加 `messageBoundary` 字段：**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `messageName` | 是 | — | 要订阅的消息名 |
| `correlationKey` | 是 | — | 必选关联规则，保证唯一订阅者 |
| `cancelActivity` | 否 | `true` | `true`=中断型，`false`=非中断型（任务继续，同时也触发边界路线） |
| `boundaryTarget` | 否 | — | 触发后路由到的节点 ID |
| `eventId` | 否 | `message_boundary_{nodeId}` | 边界事件ID |

**JSON 示例：**
```json
{
  "id": "task_wait",
  "type": "userTask",
  "name": "等待付款",
  "assignee": {"type": "role", "value": "finance"},
  "messageBoundary": {
    "messageName": "PaymentReceived",
    "correlationKey": "${orderId}",
    "cancelActivity": true,
    "boundaryTarget": "task_ship"
  }
}
```

> **注意：** 消息边界事件**既可以是中断型（右手边），也可以是非中断型（左手边）**。非中断型触发后依附的任务仍然继续执行，适合并行通知场景。消息边界事件还可以通过 JMS、HTTP/SOAP 等外部系统触发。

---

### Step 2: 展示流程摘要并确认

**必须展示以下内容，等待用户确认后再执行：**

```
## 流程摘要

- 流程名称：员工请假审批流程
- 流程类型：oa
- 目标环境：https://api3.boot.jeecg.com

### 流程节点

| 序号 | 节点名称 | 类型 | 审批人 |
|------|---------|------|--------|
| 1 | 开始 | startEvent | - |
| 2 | 员工提交申请 | userTask | ${applyUserId} |
| 3 | 部门经理审批 | userTask | manager (角色组) |
| 4 | 审批结果 | exclusiveGateway | 条件分支 |
| 5 | HR审批 | userTask | hr (角色组) |
| 6 | 结束 | endEvent | - |

### 连线与条件

开始 → 员工提交申请 → 部门经理审批 → 审批结果
  ├─ 通过 (result==1) → HR审批 → 结束
  └─ 拒绝 (result==0) → 结束

确认以上信息正确？(y/n)
```

### Step 3: 生成 JSON 配置并调用通用脚本

> **重要：优先使用 `scripts/bpmn_creator.py` 通用脚本 + JSON 配置文件的方式，只需生成 JSON 数据即可创建流程，无需每次编写 Python 代码。**

**脚本位置：** `scripts/bpmn_creator.py`

**使用步骤：**
1. 根据用户需求生成 JSON 配置文件（Write 到工作目录的临时 `.json` 文件）
2. 用 Bash 执行脚本：`python "<skill目录>/scripts/bpmn_creator.py" --api-base <URL> --token <TOKEN> --config <config.json>`
3. 删除临时 JSON 配置文件

**脚本自动完成：**
- 生成完整 BPMN XML（含节点、连线、布局）
- 构建 nodes 参数
- 调用 saveProcess API 创建/更新流程
- 关联表单（如配置了 formLink）
- 条件表达式自动 base64 编码（flowUtil.evaluateExpression）
- taskExtendJson 自动生成
- 布局自动计算（垂直排列、绕行连线自动检测）

**JSON 配置格式：**
```json
{
  "processName": "请假审批流程",
  "processKey": "oa_leave_approval",
  "typeId": "oa",
  "nodes": [
    {"id": "start", "type": "startEvent", "name": "开始"},
    {"id": "task_draft", "type": "userTask", "name": "提交申请", "draft": true,
     "assignee": {"type": "expression", "value": "applyUserId"}},
    {"id": "task_manager", "type": "userTask", "name": "部门经理审批",
     "assignee": {"type": "role", "value": "manager"}},
    {"id": "gateway_days", "type": "exclusiveGateway", "name": "请假天数判断",
     "default": "flow_le3_end"},
    {"id": "task_hr", "type": "userTask", "name": "HR审批",
     "assignee": {"type": "role", "value": "hr"}},
    {"id": "end", "type": "endEvent", "name": "结束"}
  ],
  "flows": [
    {"id": "flow_1", "source": "start", "target": "task_draft"},
    {"id": "flow_2", "source": "task_draft", "target": "task_manager"},
    {"id": "flow_3", "source": "task_manager", "target": "gateway_days"},
    {"id": "flow_gt3", "source": "gateway_days", "target": "task_hr", "name": "大于3天",
     "conditions": [{"field": "integer_xxx", "fieldType": "integer", "fieldName": "请假天数", "operator": "gt", "value": "3"}]},
    {"id": "flow_le3_end", "source": "gateway_days", "target": "end", "name": "3天及以内(默认)"},
    {"id": "flow_hr_end", "source": "task_hr", "target": "end"}
  ],
  "formLink": {
    "formType": "2",
    "relationCode": "desform_oa_leave_apply",
    "titleExp": "${select_user_xxx}提交的请假申请",
    "formTableName": "oa_leave_apply"
  }
}
```

**手工分支（意见分支）JSON 示例：**
```json
{
  "processName": "客户申请流程",
  "processKey": "crm_customer_apply",
  "nodes": [
    {"id": "start", "type": "startEvent", "name": "开始"},
    {"id": "task_draft", "type": "userTask", "name": "填写申请", "draft": true,
     "assignee": {"type": "expression", "value": "applyUserId"}},
    {"id": "task_manager", "type": "userTask", "name": "经理审批",
     "assignee": {"type": "assignee", "value": "admin"}},
    {"id": "task_director", "type": "userTask", "name": "总监审批",
     "assignee": {"type": "assignee", "value": "admin"}},
    {"id": "end", "type": "endEvent", "name": "结束"}
  ],
  "flows": [
    {"id": "flow_1", "source": "start", "target": "task_draft"},
    {"id": "flow_2", "source": "task_draft", "target": "task_manager", "name": "经理审批"},
    {"id": "flow_3", "source": "task_draft", "target": "task_director", "name": "总监审批"},
    {"id": "flow_4", "source": "task_manager", "target": "end"},
    {"id": "flow_5", "source": "task_director", "target": "end"}
  ]
}
```
> **自动检测：** 当一个 userTask 有 2+ 条出线且都不带 `conditions` 时，脚本自动识别为手工分支，使用水平布局。无需额外配置。

**手工分支布局规则（避免节点和连线重叠）：**

布局结构：
```
开始 → [前置节点...] → 分支源 ──(第一条线)──→ 结束
                          │                     ↑
                          └──(第二条线)──→ 目标 ─┘
```

- 顶行水平排列：开始 → 前置节点（如草稿、审批节点） → 分支源 → 结束
- 分支源的**第一条出线**（如"拒绝"）：从源右侧**直线水平**连到结束
- 分支源的**后续出线**（如"同意"）：从源**底部向下**，再**向右**连到目标节点（避免与第一条线重叠）
- 目标节点**回到结束**：从目标右侧**向右**，再**向上**连到结束底部（避免与顶部线重叠）
- 支持前置节点（如 start → draft → dept → finance(分支源)），自动计算偏移
- 支持 callActivity / subProcess 等特殊节点作为分支目标

#### JSON 配置字段说明

**顶层字段：**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `processName` | 是 | - | 流程中文名称 |
| `processKey` | 否 | `process_{timestamp}` | 流程唯一标识 |
| `processId` | 否 | `0` | 已有流程ID（编辑时传入） |
| `typeId` | 否 | `oa` | 流程类型 |
| `startType` | 否 | `manual` | 发起方式 |
| `nodes` | 是 | - | 节点数组 |
| `flows` | 是 | - | 连线数组 |
| `formLink` | 否 | - | 表单关联配置（存在则自动关联） |

**节点（nodes）字段：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 节点唯一ID |
| `type` | 是 | `startEvent` / `endEvent` / `userTask` / `exclusiveGateway` / `parallelGateway` / `inclusiveGateway` |
| `name` | 是 | 节点名称 |
| `draft` | 否 | `true` = 首节点提交/填写（sameMode=0 由发起人对自己审批 + AutoSubmitListener 自动提交监听 + **自动设置表单可编辑 formEditStatus=1**）。可通过 `assignee.sameMode` 显式覆盖。**重要：草稿节点只添加 `TaskCreatedAutoSubmitListener`，不添加 `TaskSkipApprovalListener`，否则流程启动失败；非草稿节点只添加 `TaskSkipApprovalListener`，不添加 `TaskCreatedAutoSubmitListener`**。**开启 formEditStatus=1 的节点必须同时设置 PC 和移动端表单地址**，否则表单无法正常打开（见下方「Online/DesForm 表单地址配置」） |
| `default` | 否 | 排他网关的默认流 ID |
| `assignee` | 否 | 审批人配置（见下方） |
| `countersign` | 否 | 会签配置（见下方），设置后节点自动变为多实例会签 userTask |

**会签（countersign）配置：**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `sequential` | 否 | `false` | `true`=串行（顺序逐个），`false`=并行（同时） |
| `rule` | 否 | `countersign_all` | `countersign_all`=全部通过 / `countersign_one`=一人通过 / `countersign_half`=半数通过 / `countersign_proportion`=按比例 / `countersign_custom`=自定义指定人员 |
| `proportion` | 否 | - | 仅 `rule=countersign_proportion` 时有效，如 `"0.6"` |
| `auditorUserType` | 是 | - | `candidateUsers`/`candidatePosts`/`candidateDepts`/`candidateGroups`/`candidateApprovalGroups`/`candidateDeptPositions`/`formData`/`customUser` |
| `auditorUserIds` | 条件 | - | `candidateUsers` 时必填，如 `["admin","jeecg"]` |
| `auditorPostIds` | 条件 | - | `candidatePosts`（职务/职级）时必填，如 `["1958471074953363458"]` |
| `auditorDeptIds` | 条件 | - | `candidateDepts` 时必填 |
| `auditorGroupIds` | 条件 | - | `candidateGroups`（角色）时必填 |
| `auditorApprovalGroupIds` | 条件 | - | `candidateApprovalGroups`（审批角色）时必填 |
| `auditorDeptPositionIds` | 条件 | - | `candidateDeptPositions`（岗位）时必填 |
| `auditorCountersignFormField` | 条件 | - | `formData` 时必填，表单字段 model |
| `auditorCountersignFormFieldType` | 条件 | `select-user` | `formData` 时使用，表单字段类型 |

> **注意：** 配置了 `countersign` 后，`assignee` 中的审批人配置会被忽略（assignee 自动改为 `${assigneeUserId}`），审批人由 `countersign` 中的配置决定。

> **`customUser` 类型（会签自定义-指定人员）说明：**
> - 对应 UI 中的"会签自定义(指定人员)"，`flowable:countersignRule="countersign_custom"`
> - **无 `taskCountersignExtendJson`**（与其他类型不同）
> - collection 自动生成为 `${flowUtil.stringToList(assigneeUserIdList)}`，通过流程变量 `assigneeUserIdList` 动态传入（发起时选人）
> - 完成条件默认 `${nrOfCompletedInstances/nrOfInstances>=1}`（全部通过）
> - JSON 示例：
> ```json
> {
>   "id": "task_countersign",
>   "type": "userTask",
>   "name": "会签自定义(指定人员)",
>   "countersign": {
>     "sequential": false,
>     "rule": "countersign_custom",
>     "auditorUserType": "customUser"
>   }
> }
> ```

**会签 JSON 示例（串行，半数通过，职务总经理）：**
```json
{
  "id": "task_countersign",
  "type": "userTask",
  "name": "总经理会签",
  "countersign": {
    "sequential": true,
    "rule": "countersign_half",
    "auditorUserType": "candidatePosts",
    "auditorPostIds": ["1958471074953363458"]
  }
}
```

**审批人（assignee）配置：**

| type 值 | value 含义 | 生成的 XML | 示例 |
|---------|-----------|-----------|------|
| `assignee` | 固定用户名 | `flowable:assignee="value"` | `"admin"` |
| `expression` | 表达式变量名 | `flowable:assignee="${value}"` | `"applyUserId"` |
| `candidateUsers` | 多候选人（用户名） | `flowable:candidateUsers="value"` | `"qinfeng,test"` |
| `candidateUsersExpression` | 候选人表达式 | `flowable:candidateUsers="value"` | `"${flowNodeExpression.getDepartLeaders(applyUserId)}"` |
| `role` | 角色编码 | `candidateGroups + groupType="role"` | `"admin,vue3"` |
| `approvalRole` | 审批角色 ID | `candidateUsers + 表达式 + groupType="approvalRole"` | `"1979845941985529857"` |
| `dept` | 部门 ID | `candidateGroups + groupType="dept"` | `"6d35e179..."` |
| `deptPosition` | 岗位 ID | `candidateGroups + groupType="deptPosition"` | `"1958497164..."` |
| `position` | 职级 ID | `candidateUsers + 表达式 + groupType="position"` | `"1958470912..."` |

assignee 额外可选参数：`sameMode`, `skipOne`, `skipEmpty`, `skipApproval`, `assignedByPrev`, `emptyAssignedByPrev`

> **注意：** `approvalRole` 和 `position` 自动包装为表达式（`flowUtil.getUsersByApprRole` / `oaFlowExpression.getApplyUserDeptPositionLevel`），只需传 ID。

**节点抄送人（ccConfig）字段：**

在节点 JSON 中通过 `ccConfig` 数组配置抄送人，脚本自动 base64 编码后写入 `<flowable:ccConfigJson>`：

```json
{
  "id": "task_manager",
  "type": "userTask",
  "name": "经理审批",
  "assignee": {"type": "role", "value": "manager"},
  "ccConfig": [
    {
      "type": "candidateUsers",
      "userIds": ["qinfeng"],
      "selectedUsers": [{"value": "qinfeng", "label": "秦峰"}]
    },
    {"type": "submitter_dept_leader"},
    {"type": "dept_leader"}
  ]
}
```

| ccConfig type | 说明 | 附加字段 |
|--------------|------|---------|
| `candidateUsers` | 指定用户 | `userIds`（用户名数组）、`selectedUsers`（`[{value,label}]`） |
| `candidateRoles` | 指定角色 | `roleIds`（角色编码数组）、`selectedRoles`（`[{value,label}]`） |
| `candidateDeptPositions` | 指定岗位 | `deptPositionIds`（岗位ID数组）、`selectedDeptPositions`（`[{value,label}]`） |
| `submitter_user` | 发起人本人 | 无 |
| `submitter_dept_leader` | 发起人的部门负责人 | 无 |
| `submitter_parent_dept_leader` | 发起人的上级部门负责人 | 无 |
| `dept_members` | 发起人所在部门全体成员 | 无 |
| `dept_leader` | 当前节点审批人的部门负责人 | 无 |

> 详细说明及 Python 生成代码见 `references/bpmn-advanced.md` 第2节。

**连线（flows）字段：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 连线唯一ID |
| `source` | 是 | 源节点ID |
| `target` | 是 | 目标节点ID |
| `name` | 否 | 连线名称（分支时显示） |
| `conditions` | 否 | 条件数组（自动 base64 编码为 flowUtil.evaluateExpression） |
| `bypass` | 否 | `true` = 从右侧绕行（自动检测，通常无需手动设） |

**条件（conditions）格式：**
```json
{"field": "integer_xxx", "fieldType": "integer", "fieldName": "请假天数", "operator": "gt", "value": "3"}
```
operator 值：`eq`, `ne`, `gt`, `gte`, `lt`, `lte`/`le`, `in`, `not_in`, `contains`, `is_empty`, `is_not_empty`

**表单类型选择规则（强制）：**

> 用户明确说"online表单"时，表单部分必须使用 **jeecg-onlform** 技能创建，`formType` 填 `"1"`。
> 用户明确说"表单设计器"时，表单部分使用 **jeecg-desform** 技能创建，`formType` 填 `"2"`。
> 两者是完全独立的表单体系，不可混用。

**表单关联（formLink）字段：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `formType` | `1`=Online, `2`=DesForm, `3`=自定义 | `"2"` |
| `relationCode` | Online: `onl_{表名}`, DesForm: `desform_{编码}`, 自定义: 直接写 | `"onl_test_bpm_apply"` |
| `titleExp` | 业务标题 `${字段model}` 引用 | `"${user_xxx}提交的请假"` |
| `formTableName` | DesForm=表单编码, Online=表名 | `"oa_leave"` |
| `formDealStyle` | 处理方式 | `"default"` |
| `flowStatusCol` | 状态字段 | `"bpm_status"` |
| `formUrl` | 自定义表单地址（仅 formType=3，可选，不填则自动推导） | `"visitor/components/BizVisitorRegisterForm?edit=1"` |

**DesForm 表单绑定示例：**
```json
{
  "formLink": {
    "formType": "2",
    "relationCode": "oa_leave",
    "formTableName": "oa_leave",
    "flowStatusCol": "bpm_status",
    "titleExp": "${user_name}提交的请假申请"
  }
}
```

**Online 表单绑定示例：**
```json
{
  "formLink": {
    "formType": "1",
    "relationCode": "test_bpm_apply",
    "formTableName": "test_bpm_apply",
    "flowStatusCol": "bpm_status",
    "titleExp": "BPM测试申请-${title}"
  }
}
```

**自定义开发表单绑定示例（代码生成的表单）：**
```json
{
  "formLink": {
    "formType": "3",
    "relationCode": "dev_demo_all_component_001",
    "formTableName": "demo_all_component",
    "flowStatusCol": "bpm_status",
    "titleExp": "全组件演示-${name}"
  }
}
```

> **自定义开发表单（formType=3）使用场景与规则：**
> - **适用场景：** 通过代码生成器生成的 CRUD 表单（有独立的 Entity/Controller/Service/前端页面），不是 Online 表单也不是 DesForm 设计器表单
> - **relationCode 命名规则：** `dev_{表名}_001`，如 `dev_demo_all_component_001`（参考系统自带示例）
> - **formTableName：** 填数据库表名，如 `demo_all_component`
> - **flowStatusCol：** 必须为 `bpm_status`，表中需有该字段（varchar(10)）
> - **titleExp：** 使用 `${字段名}` 引用表中字段值，如 `全组件演示-${name}`
> - **前缀处理：** `bpmn_creator.py` 对 formType=3 **不自动加前缀**，relationCode 原样使用
> - **发起授权：** formType=3 **不需要**发起授权步骤（不需要调用 saveWorkorderAuth），跳过 Step 5
> - **前置条件：** 生成代码时需确保 Entity 中有 `bpmStatus` 字段（`@Dict(dicCode = "bpm_status")`），建表 DDL 中有 `bpm_status varchar(10)` 列

> **注意：** `relationCode` 无需手动加 `onl_` 前缀，`bpmn_creator.py` 会根据 `formType` 自动补全（`formType=1` 加 `onl_`，`formType=2` 加 `desform_`，`formType=3` 不加前缀）。Online 表单走流程必须在表中包含 `bpm_status` 字段。

**调用示例：**
```bash
python "<skill目录>/scripts/bpmn_creator.py" \
    --api-base <api_base> \
    --token <token> \
    --config leave_process.json

# 只生成 XML 不调用 API（调试用）
python "<skill目录>/scripts/bpmn_creator.py" \
    --api-base <api_base> \
    --token xxx \
    --config leave_process.json \
    --dry-run
```

#### 当通用脚本不满足需求时

对于会签、复杂子流程等场景，通用脚本可能无法覆盖，此时需编写临时 Python 脚本。（serviceTask 已原生支持，无需临时脚本）阅读以下参考文件：
- `references/bpmn-xml-skeleton.md` — XML 骨架 + 基本节点模板
- `references/bpmn-assignee-types.md` — 审批人配置 + groupType
- `references/bpmn-layout.md` — 布局计算
- `references/bpmn-countersign.md` — 会签配置
- `references/bpmn-task-extend.md` — taskExtendJson + 监听器
- `references/bpmn-advanced.md` — 条件表达式 + 抄送 + 按钮 + 服务任务
- `references/bpmn-subprocess-gateway.md` — 网关 + 子流程
- `references/example/*.bpmn` — 生产环境示例

##### saveProcess API 规范（临时脚本必须遵守）

> **重要：** 临时脚本调用 `saveProcess` API 时，必须与 `bpmn_creator.py` 保持一致：

| 项目 | 正确值 | 常见错误 |
|------|--------|---------|
| **请求路径** | `/act/designer/api/saveProcess` | ~~`/act/process/extActProcess/saveProcess`~~ |
| **Content-Type** | `application/x-www-form-urlencoded` | ~~`application/json`~~ |
| **流程Key字段名** | `processkey`（全小写） | ~~`processKey`~~（驼峰） |
| **类型字段名** | `typeid`（全小写） | ~~`typeId`~~（驼峰） |
| **XML字段名** | `processDescriptor` | ~~`processXml`~~ |
| **流程ID字段名** | `processDefinitionId`（新建传`0`） | ~~`id`~~ |
| **返回值中流程ID** | `result['obj']` | ~~`result['result']`~~ |

**saveProcess 请求参数完整列表：**
```python
data = {
    'processDefinitionId': '0',        # 新建传 '0'，编辑传已有流程ID
    'processName': '流程名称',
    'processkey': 'process_key',        # 注意全小写
    'typeid': 'oa',                     # 注意全小写
    'lowAppId': '',
    'params': '',
    'nodes': 'id=task_xxx###nodeName=节点名@@@',  # 节点列表字符串
    'processDescriptor': bpmn_xml,       # 完整 BPMN XML
    'realProcDefId': '',
    'startType': 'manual',
}
result = api_request('/act/designer/api/saveProcess', data,
                     content_type='application/x-www-form-urlencoded')
process_id = result['obj']  # 返回的流程ID在 obj 字段
```

##### BPMN XML 转义规则（临时脚本必须遵守）

> **重要：** 由于 XML 经过 URL 编码传输，必须严格使用 XML 数字实体转义，不能使用 Python 字符串拼接嵌入变量值：

| 字符 | 必须转义为 | 使用场景 | 错误写法 |
|------|----------|---------|---------|
| `"` | `&#34;` | taskExtendJson 的 value 属性中的 JSON 双引号 | ~~`&quot;`~~（虽然语义等价，但推荐用 `&#34;` 与设计器前端保持一致） |
| `'` | `&#39;` | `flowUtil.getAssigneeUsers(execution,'BASE64')` 中的单引号 | ~~字面单引号 `'`~~（URL 编码后可能丢失） |

**正确写法示例（Python）：**
```python
# taskExtendJson — 使用 &#34; 转义双引号
TASK_EXTEND = '{&#34;sameMode&#34;:0,&#34;isSkipAssigneeEmpty&#34;:false,...}'

# collection 表达式 — 使用 &#39; 转义单引号
COLLECTION = '${flowUtil.getAssigneeUsers(execution,&#39;%s&#39;)}' % b64_config

# 拼接 XML（使用 % 格式化，不要用三引号字符串拼接）
xml_parts.append('<flowable:taskExtendJson value="%s" />' % TASK_EXTEND)
xml_parts.append('<bpmn2:multiInstanceLoopCharacteristics flowable:collection="%s" .../>' % COLLECTION)
```

**错误写法（会导致 URL 编码后单引号丢失）：**
```python
# 错误！三引号拼接中的单引号在 URL 编码后会被吞掉
xml = '''...flowable:collection="${flowUtil.getAssigneeUsers(execution,'''' + b64 + '''')}"...'''
```

##### 临时脚本推荐模式

使用 `xml_parts` 列表逐行拼接 XML（压缩格式），最后 `''.join(xml_parts)` 生成完整 XML。这样避免三引号字符串拼接的转义问题：

```python
xml_parts = []
xml_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
xml_parts.append('<bpmn2:definitions ...>')
xml_parts.append('<bpmn2:process id="%s" name="%s">' % (key, name))
# ... 逐行添加节点、连线、布局 ...
xml_parts.append('</bpmn2:definitions>')
bpmn_xml = ''.join(xml_parts)
```

临时脚本执行步骤：
```
1. Write 工具 → 写入 create_process.py（项目根目录）
2. Bash 工具 → python create_process.py
3. Bash 工具 → rm create_process.py（清理）
```

### Step 4: 自动发布流程

流程创建成功后，自动调用发布接口部署流程（无需手动到后台点击发布）：

```python
# 发布流程 — PUT /act/process/extActProcess/deployProcess
deploy_data = json.dumps({'id': process_id}).encode('utf-8')
req = urllib.request.Request(
    f'{API_BASE}/act/process/extActProcess/deployProcess',
    data=deploy_data,
    headers={
        'X-Access-Token': TOKEN,
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Sign': '00000000000000000000000000000000',
        'X-Tenant-Id': '1',
    },
    method='PUT'
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read().decode('utf-8'))
# success: true → 发布成功
```

通用脚本 `bpmn_creator.py` 已内置 `--deploy` 参数自动发布。

### Step 5: 发起授权

流程关联设计器表单（formType=1 或 formType=2）后，需要将表单授权给角色，用户才能在「发起审批」中看到该流程。

**适用范围：**
- `formType=1`（Online 表单）— 需要授权
- `formType=2`（设计器表单 DesForm）— 需要授权
- `formType=3`（自定义表单）— **不需要授权**，跳过此步骤

**授权 API 说明：**

| 步骤 | API | 方法 | 说明 |
|------|-----|------|------|
| 1. 查询已有授权 | `/joa/designform/designFormCommuse/getAuthorizedDesignList?principalId={roleId}&authMode=role&_t={timestamp}` | GET | 获取角色已授权的表单ID列表 |
| 2. 保存授权 | `/joa/designform/designFormCommuse/saveWorkorderAuth/{roleId}` | POST | 追加新表单ID并保存 |

**保存授权请求体：**
```json
{
  "authMode": "role",
  "authId": "id1,id2,id3,...,新表单ID",
  "subDepartIds": ""
}
```

> **重要：** `authId` 必须包含该角色已有的所有授权表单ID + 新表单ID（逗号分隔），否则会覆盖已有授权。

**默认角色ID：** `f6817f48af4fb3af11b9e8bf182f618b`（管理员角色）

**不同表单类型的 form_id 取值（实战验证）：**

| formType | 表单类型 | form_id 取值 | 获取方式 |
|----------|---------|-------------|---------|
| `1` | Online 表单 | Online 表单的 **headId** | 创建 Online 表单时 `onlform_creator.py` 输出的 headId，或通过 `GET /online/cgform/head/list?tableName={表名}` 查询 |
| `2` | 设计器表单 DesForm | DesForm 的**表单 ID** | 创建设计器表单时 `desform_creator.py` 输出的表单 ID，或通过 `GET /desform/queryByIdOrCode?desformCode={编码}` 查询 |

> **踩坑记录：** Online 表单授权时，`form_id` 必须传 Online 表单的 `headId`（如 `a22625df48b0473ea51197fb276eba95`），**不是**流程 ID，也不是数据库表名。DesForm 表单授权时传 DesForm 的表单记录 ID。两者使用**同一套授权 API**（`saveWorkorderAuth`），只是传入的 ID 来源不同。

**Python 示例：**
```python
import json, time, urllib.request

def authorize_form(api_base, token, form_id, role_id='f6817f48af4fb3af11b9e8bf182f618b'):
    """为表单添加发起授权（保留已有授权）"""
    headers = {
        'X-Access-Token': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }

    # 1. 查询已有授权
    ts = str(int(time.time() * 1000))
    url = f'{api_base}/joa/designform/designFormCommuse/getAuthorizedDesignList?principalId={role_id}&authMode=role&_t={ts}'
    req = urllib.request.Request(url, headers=headers)
    result = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    existing_ids = [item['id'] for item in result.get('result', []) or []]

    # 2. 追加新表单ID
    if form_id not in existing_ids:
        existing_ids.append(form_id)

    # 3. 保存授权
    url = f'{api_base}/joa/designform/designFormCommuse/saveWorkorderAuth/{role_id}'
    data = json.dumps({
        'authMode': 'role',
        'authId': ','.join(existing_ids),
        'subDepartIds': '',
    }, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    result = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    return result
```

> **何时执行：** 当流程关联了 Online 表单（formType=1）或设计器表单（formType=2）时，流程创建完成后自动执行发起授权。如果流程关联的是自定义表单（formType=3），则不需要此步骤。

### Step 5.5: Online/DesForm 表单地址配置（重要）

> **开启 `formEditStatus=1` 的节点必须同时设置 PC 和移动端表单地址**，否则表单无法正常打开。仅对表单可编辑的节点（如草稿节点）设置，其他审批节点无需设置。

**不同表单类型的地址：**

| 表单类型 | PC 表单地址 (`modelAndView`) | 移动端表单地址 (`modelAndViewMobile`) |
|---------|---------------------------|-------------------------------------|
| **Online 表单** (formType=1) | `super/bpm/process/components/OnlineFormOpt` | `check/onlineForm/flowedit` |
| **DesForm 表单** (formType=2) | `{{DOMAIN_URL}}/desform/edit/{表单编码}/${BPM_DES_DATA_ID}?token={{TOKEN}}&taskId={{TASKID}}&skip=false` | `check/desForm/flowedit` |
| **自定义开发表单** (formType=3) | `{{viewDir}}/components/{{entityName}}Form?edit=1` | *(同 PC 地址或留空)* |

> **自定义开发表单 PC 表单地址说明：**
> - 地址格式：`{前端视图目录}/components/{实体名}Form?edit=1`
> - 示例：`demo/allComponent/components/DemoAllComponentForm?edit=1`
> - `?edit=1` 参数标识该节点表单可编辑，Form.vue 通过 `props.formData.disabled` 控制
> - 该地址指向代码生成的 `Form.vue` 组件（不是 `Modal.vue`），Form.vue 使用 `defineComponent` + `getBpmFormSchema` 模式
> - **仅在草稿/提交申请节点（formEditStatus=1）设置**，审批节点无需设置

**配置示例（仅对 formEditStatus=1 的节点设置）：**
```python
# Online 表单
edit_node_config(api_base, token, process_id, 'task_draft', {
    'formEditStatus': '1',
    'modelAndView': 'super/bpm/process/components/OnlineFormOpt',
    'modelAndViewMobile': 'check/onlineForm/flowedit',
})

# 自定义开发表单
edit_node_config(api_base, token, process_id, 'task_draft', {
    'formEditStatus': '1',
    'modelAndView': 'demo/allComponent/components/DemoAllComponentForm?edit=1',
    'modelAndViewMobile': '',
})
```

> **注意：** 非表单可编辑节点（如审批节点 formEditStatus=0）**不需要**设置 modelAndView 和 modelAndViewMobile，保持为空即可。
>
> **关闭 formEditStatus 时必须同步清空表单地址：** 将 `formEditStatus` 从 `1` 改为 `0` 时，必须同时将 `modelAndView` 和 `modelAndViewMobile` 清空为 `''`，并重新发布流程。

### Step 6: 节点字段权限配置（可选）

流程创建后，可通过 `bpmn_creator.py` 中的函数配置每个节点上表单字段的可见、可编辑、必填状态。

**两个核心函数：**

#### `edit_node_config(api_base, token, process_id, node_code, node_settings)`

编辑节点级配置（表单可编辑、抄送、转办、加签、驳回等开关）。

```python
from bpmn_creator import edit_node_config

edit_node_config(api_base, token, process_id, 'task_draft', {
    'formEditStatus': '1',   # 表单可编辑
    'ccStatus': '1',          # 启用抄送
    'selnextUserStatus': '1', # 选择下一步处理人
    'msgStatus': '1',         # 消息通知
    'addSignStatus': '1',     # 加签
    'transferStatus': '1',    # 转办
    'rejectStatus': '1',      # 驳回
    'modelAndView': 'PC端表单地址',
    'modelAndViewMobile': '移动端表单地址',
})
```

#### `set_node_field_permissions(api_base, token, process_id, node_code, form_code, field_permissions, form_type='2')`

批量设置节点上每个字段的可见/可编辑/必填权限。支持用**字段中文名**或**字段 model** 引用字段。

```python
from bpmn_creator import set_node_field_permissions

result = set_node_field_permissions(api_base, token, process_id, 'task_draft', 'oa_interview_apply', [
    {"field": "面试地点", "visible": True, "editable": False},              # 可见但禁用
    {"field": "联系电话", "visible": True, "editable": True, "required": True},  # 必填
    {"field": "面试说明", "visible": False},                                # 隐藏
])
# 返回: {"success": True, "updated": 3, "errors": [], "message": "批量保存成功！"}
```

**字段权限配置项：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `field` | string | 必填 | 字段中文名或字段 model |
| `visible` | bool | `true` | 是否可见 |
| `editable` | bool | `true` | 是否可编辑 |
| `required` | bool | `false` | 是否必填 |

> **必填时必须同时显式设 `editable: True`**
>
> `required: true` 会自动强制 `visible=true` + `editable=true`，但生成的 ruleType=2 status 必须为 `'0'`（可编辑勾选）才能在 UI 上正确显示必填。
> `bpmn_creator.py` 中 ruleType=2 的 status 已修正为 `'0' if editable else '1'`（原来写反，导致必填时 UI 可编辑未勾选、必填校验不生效）。
>
> 正确写法：`{"field": "申请日期", "visible": True, "editable": True, "required": True}`
> 错误写法：`{"field": "申请日期", "required": True}` ← 省略 editable 时默认值为 True，代码会自动补，但明确写出更安全

> **联动规则（formEditStatus=1 节点的 API status 值对照，实测验证）：**
>
> **关键：ruleType=2 的 status 与 UI 可编辑勾选状态是反的！**
> - `status='0'` → UI 可编辑**已勾选**（跟随节点默认=可编辑）
> - `status='1'` → UI 可编辑**未勾选**（启用控制=禁用/只读）
>
> | 操作 | UI 可见 | UI 可编辑 | UI 必填 | 可见(ruleType=1) status | 可编辑(ruleType=2) status | required |
> |------|--------|---------|--------|----------------------|------------------------|----------|
> | **隐藏** | ✗ | ✗ | ✗ | `'0'` | `'1'` | `false` |
> | **可见+可编辑**（默认） | ✓ | ✓ | ✗ | `'1'` | `'0'` | `false` |
> | **可见+禁用**（只读） | ✓ | ✗ | ✗ | `'1'` | `'1'` | `false` |
> | **必填** | ✓ | ✓ | ✓ | `'1'` | `'0'` | `true` |

**API 对应关系：**

| UI 列 | API 字段 | 说明 |
|--------|---------|------|
| 可见 | `ruleType='1'` 的 `status` | `'1'`=勾选（可见），`'0'`=未勾选（隐藏） |
| 可编辑 | `ruleType='2'` 的 `status` | **`'0'`=勾选（可编辑），`'1'`=未勾选（禁用）——与直觉相反！** |
| 必填 | `required` (`true`/`false`) | 两行记录都需设置 |

> **重要：ruleType=2 的 status 含义与 ruleType=1 相反（实测验证）：**
>
> 当节点开启了 `formEditStatus=1`（表单可编辑）时，所有字段默认可编辑。此时：
> - `ruleType=2` 的 `status='0'` = UI 可编辑**勾选** = 字段可编辑（跟随节点默认）
> - `ruleType=2` 的 `status='1'` = UI 可编辑**未勾选** = 字段禁用/只读（启用控制覆盖默认）
>
> 这与 `ruleType=1` 的逻辑相反（ruleType=1: status='1'=勾选=可见）。
>
> 各操作的正确 status 值：
> - **必填**：ruleType=1 status=`'1'`，ruleType=2 status=`'0'`，required=`true`
> - **隐藏**：ruleType=1 status=`'0'`，ruleType=2 status=`'1'`，required=`false`
> - **禁用**：ruleType=1 status=`'1'`，ruleType=2 status=`'1'`，required=`false`
> - **可编辑**：ruleType=1 status=`'1'`，ruleType=2 status=`'0'`，required=`false`

**三种表单类型的 ruleCode 格式（实测验证）：**

| 表单类型 | ruleCode 格式 | formBizCode | desformComKey |
|---------|--------------|-------------|---------------|
| Online (formType=1) | `online:{表名}:{字段名}` | 表名 | null |
| DesForm (formType=2) | `{desformComKey}` | 表单编码 | 组件 key |
| **自定义 (formType=3)** | **`{自定义编码}`** | **主表表名（主表字段和子表列都用主表名！）** | null |

**Online 表单子表字段的 ruleName 格式（实测验证）：**

- 主表字段：`ruleName` = 字段中文名，如 `申请标题`
- **子表字段：`ruleName` = `{子表描述}::{字段中文名}`，如 `采购明细::金额`**
- `formBizCode` 填**子表表名**（不是主表表名），`ruleCode` 也用子表表名：`online:{子表表名}:{字段名}`

> **⚠ Online 与自定义表单的子表列 formBizCode 规则相反（实测验证）：**
> - **Online (formType=1)**：子表列 `formBizCode` = **子表表名**
> - **自定义 (formType=3)**：子表列 `formBizCode` = **主表表名**（与主表字段相同！）
>
> 用错会导致权限保存成功但流程节点设计器中看不到配置，`subPermissionList` 也不注入。

**更新已有字段权限时（强制要求）：**

> 调用 `saveOrUpdateBatch` 更新权限时，**必须先查询已有记录**，携带原记录的 `id` 提交，**不得修改 `ruleName`**。直接新建（不带 `id`）会导致重复记录；擅自修改 `ruleName` 会破坏系统中已有的字段名称显示。

```python
# 正确流程：先查 → 取 id + ruleName → 只改 status/required
r = requests.get(f"{BASE}/act/process/extActProcessNodePermission/list",
    headers=headers,
    params={"processId": process_id, "processNodeCode": node_code, "pageNo": 1, "pageSize": 100})
records = r.json()["result"]["records"]
existing = {rec["ruleCode"]: rec for rec in records}

# 更新时保留原 id 和 ruleName，只修改 status/required
payload = []
for rule_code, new_status_1, new_status_2, new_required in fields_to_update:
    rec1 = existing.get(rule_code + ":ruleType1")  # 按实际查询结果匹配
    payload.append({
        "id": rec["id"],           # 必须携带原 id
        "ruleName": rec["ruleName"],  # 保留原 ruleName，不修改
        "ruleType": rec["ruleType"],
        "status": new_status,
        "required": new_required,
        # ... 其他字段不变
    })
```

**自定义开发表单（formType=3）字段权限配置详解（实测验证）：**

> 自定义开发表单的字段权限通过前端 `usePermission` 的 `hasPermission(code)` / `isDisabledAuth(code)` 与后端配置的 `ruleCode` 联动。`ruleCode` 是自定义的权限编码，需要与前端 data.ts 中 formSchema 的 `show`/`dynamicDisabled` 里使用的编码一致。

**ruleCode 命名规则：** `{模块简称}:{字段名}`，如 `demoall:password`、`demoall:remark`

**完整 API 调用流程：**

**第 1 步：编辑节点配置（开启表单可编辑 + 设置表单地址）**

```
PUT /act/process/extActProcessNode/edit

请求体：
{
    "id": "{节点记录ID}",
    "formEditStatus": "1",
    "ccStatus": "1",
    "selnextUserStatus": "1",
    "msgStatus": "1",
    "modelAndView": "{{viewDir}}/components/{{entityName}}Form?edit=1",
    "modelAndViewMobile": "",
    "processId": "{流程ID}",
    "processNodeCode": "task_draft",
    "processNodeName": "提交申请",
    "addSignStatus": "1",
    "transferStatus": "1",
    "rejectStatus": "1"
}

返回：{"success": true, "message": "编辑成功", "code": 200}
```

> **节点记录ID** 通过 `GET /act/process/extActProcessNode/list?processId={流程ID}` 查询获取。

**第 1.5 步：添加授权标识到菜单（前置条件）**

> **重要（实测验证，按表结构区分）：**
>
> | 表类型 | 是否需要 sys_permission | 说明 |
> |--------|----------------------|------|
> | **单表**（formType=3） | ✅ **需要** | `hasPermission`/`isDisabledAuth` 依赖 sys_permission 中的权限编码 |
> | **一对多主子表**（formType=3） | ❌ **不需要** | BPM 引擎直接通过 `formData.permissionList` 注入，前端从中读取，与 sys_permission 无关 |
>
> 一对多场景只需两步：① data.ts 中 `getBpmFormSchema` 加钩子 ② `saveOrUpdateBatch` 写权限记录。

> **重要：** 自定义开发**单表**表单的字段权限编码（ruleCode）必须先作为**按钮/权限**添加到系统菜单中，并授权给 admin 角色，否则 `hasPermission(code)` 和 `isDisabledAuth(code)` 无法识别该权限编码。

```
POST /sys/permission/add

请求体（每个字段权限一条记录）：
{
    "menuType": 2,
    "name": "密码显示",
    "parentId": "{主菜单ID}",
    "perms": "demoall:password",
    "permsType": "1",
    "status": "1"
}

返回：{"success": true, "message": "添加成功！", "code": 200}
```

**字段说明：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `menuType` | 固定 `2`（按钮/权限） | `2` |
| `name` | 权限名称（UI显示） | `"密码显示"` |
| `parentId` | 上级菜单ID（即该模块的主菜单ID，Flyway SQL 中生成的 `{timestamp}01`） | `"177501111975001"` |
| `perms` | 授权标识（与 ruleCode、前端 hasPermission/isDisabledAuth 的参数一致） | `"demoall:password"` |
| `permsType` | 授权策略：`"1"`=可见/可访问，`"2"`=可编辑 | `"1"` |
| `status` | `"1"`=有效 | `"1"` |

**permsType 与前端函数对应关系：**

| permsType | 含义 | 前端对应函数 | 流程节点 ruleType |
|-----------|------|-----------|-----------------|
| `"1"` | 可见/可访问 | `hasPermission(code)` — 控制字段 `show` | ruleType=1（可见性） |
| `"2"` | 可编辑 | `isDisabledAuth(code)` — 控制字段 `dynamicDisabled` | ruleType=2（可编辑性） |

**添加后需授权给 admin 角色：**
```
POST /sys/permission/saveRolePermission

请求体：
{
    "roleId": "f6817f48af4fb3af11b9e8bf182f618b",
    "permissionIds": "{新增的权限ID1},{新增的权限ID2},...",
    "lastpermissionIds": "{原有权限IDs}"
}
```
> 或者通过 Flyway SQL 直接插入 `sys_permission` + `sys_role_permission` 表（参考代码生成的菜单 SQL 格式）。

**第 2 步：保存节点字段权限**

```
POST /act/process/extActProcessNodePermission/saveOrUpdateBatch

请求体（数组，每个字段2条记录：ruleType=1 可见 + ruleType=2 可编辑）：
[
    {
        "ruleType": "1",
        "status": "1",
        "formType": "3",
        "formBizCode": "demo_all_component",
        "processId": "2039187744210108418",
        "processNodeCode": "task_draft",
        "ruleCode": "demoall:password",
        "ruleName": "密码显示隐藏"
    },
    {
        "ruleType": "2",
        "status": "0",
        "formType": "3",
        "formBizCode": "demo_all_component",
        "processId": "2039187744210108418",
        "processNodeCode": "task_draft",
        "ruleCode": "demoall:password",
        "ruleName": "密码显示隐藏"
    }
]

返回：{"success": true, "message": "批量保存成功！", "code": 200}
```

**字段权限记录字段说明：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `ruleType` | `'1'`=可见性规则，`'2'`=可编辑性规则 | `'1'` |
| `status` | ruleType=1: `'1'`=可见/`'0'`=隐藏；ruleType=2: `'0'`=可编辑/`'1'`=禁用 | `'1'` |
| `formType` | `'3'`=自定义开发 | `'3'` |
| `formBizCode` | 数据库表名 | `'demo_all_component'` |
| `processId` | 流程ID | `'2039187744210108418'` |
| `processNodeCode` | 节点编码 | `'task_draft'` |
| `ruleCode` | 权限编码（与前端 hasPermission/isDisabledAuth 的参数一致） | `'demoall:password'` |
| `ruleName` | 权限名称（UI显示用） | `'密码显示隐藏'` |
| `id` | 记录ID（新增不传，编辑传） | `'2039250050830880769'` |

**前端 data.ts 与后端权限编码对应关系：**

```typescript
// data.ts 中 — ruleCode 与 hasPermission/isDisabledAuth 的参数必须一致
{ label: '密码', field: 'password', component: 'InputPassword',
  show: ({ values }) => {
    return hasPermission('demoall:password');  // ← 对应后端 ruleCode: 'demoall:password'
  },
},
{ label: '多行文本', field: 'remark', component: 'InputTextArea',
  dynamicDisabled: ({ values }) => {
    return isDisabledAuth('demoall:demoall');  // ← 对应后端 ruleCode: 'demoall:demoall'
  },
},
```

> **子表字段的 ruleName 格式（实测验证）：**
>
> - **Online (formType=1)**：`ruleName` = `{子表描述}::{字段标签}`，如 `商品明细::小计`；`formBizCode` = 子表表名
> - **自定义 (formType=3)**：`ruleName` = `{子表描述}{字段标签}`（无 `::`，直接拼接），如 `订单明细商品名称`；`formBizCode` = **主表表名**（与主表字段完全相同）；`ruleCode` = `{子表Key前缀}:{columnKey}`，如 `salOrderItemColumns:productName`
>
> 自定义表单子表列权限写入示例：
> ```python
> # formBizCode 统一用主表名，不论主表字段还是子表列！
> {"ruleType":"1","status":"1","formType":"3","formBizCode":"sal_sales_order",
>  "ruleCode":"salOrderItemColumns:productName","ruleName":"订单明细商品名称", ...}
> {"ruleType":"2","status":"1","formType":"3","formBizCode":"sal_sales_order",
>  "ruleCode":"salOrderItemColumns:productName","ruleName":"订单明细商品名称", ...}
> ```

**Online 表单设置必填的完整示例：**
```python
# 为 task_draft 节点的 order_date 字段设置必填
records = [
    {
        'processId': PROCESS_ID,
        'processNodeCode': 'task_draft',
        'ruleCode': 'online:sales_order:order_date',  # online:{表名}:{字段名}
        'ruleName': '下单日期',
        'ruleType': '1',       # 可见
        'status': '1',         # 启用
        'required': 1,         # 必填
        'formType': '1',       # Online 表单
        'formBizCode': 'sales_order'  # 表名
    },
    {
        'processId': PROCESS_ID,
        'processNodeCode': 'task_draft',
        'ruleCode': 'online:sales_order:order_date',
        'ruleName': '下单日期',
        'ruleType': '2',       # 可编辑
        'status': '0',         # 跟随节点默认（formEditStatus=1 时已默认可编辑）
        'required': 1,         # 必填
        'formType': '1',
        'formBizCode': 'sales_order'
    }
]
api_request(api_base, token, '/act/process/extActProcessNodePermission/saveOrUpdateBatch', data=records)
```

> 每个字段在后端存储为两条记录：`ruleType=1`（可见性规则）和 `ruleType=2`（可编辑性规则），批量通过 `POST /act/process/extActProcessNodePermission/saveOrUpdateBatch` 保存。

---

### OA 审批意见字段配置规范（DesForm + 流程节点联动）

> 适用场景：表单使用 `oa-approval-comments`（审批意见控件），需要与流程节点联动——表单上默认禁用，流转到对应节点时才启用并必填。

#### 第一步：表单设计器中设置审批意见为禁用状态

`oa-approval-comments` 控件创建时默认 `disabled: false`，**必须手动将其设为 `disabled: true`**，否则表单上的审批意见框始终可编辑，与流程节点控制失效。

**操作方式（通过 desform_utils）：**

```python
import sys, json
sys.path.insert(0, r'<desform-skill目录>/scripts')
from desform_utils import init_api, export_design_json, save_design_from_file

init_api('<api_base>', '<token>')

# 1. 导出当前设计 JSON
file_path, _ = export_design_json('<form_code>')

# 2. 遍历所有控件，将 oa-approval-comments 的 disabled 设为 True
with open(file_path, 'r', encoding='utf-8') as f:
    design = json.load(f)

def walk(items):
    for w in items:
        if w.get('type') == 'oa-approval-comments':
            w['options']['disabled'] = True
        for child in w.get('list', []):
            walk([child])
        for col in w.get('columns', []):
            walk(col.get('list', []))

walk(design.get('list', []))

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(design, f, ensure_ascii=False)

# 3. 保存回服务器
save_design_from_file('<form_code>', file_path)
```

#### 第二步：每个审批节点配置字段权限

**规则（必须同时满足三点）：**
1. 开启节点表单可编辑（`formEditStatus=1`）并设置 DesForm 表单地址
2. 对应审批意见字段：`editable=True, required=True`（启用并必填）
3. 其他所有字段：`editable=False`（只读，防止审批人篡改申请内容）

**完整 Python 示例：**

```python
import sys
sys.path.insert(0, r'<bpmn-skill目录>/scripts')
from bpmn_creator import edit_node_config, set_node_field_permissions

api_base = '<api_base>'
token = '<token>'
process_id = '<process_id>'
form_code = '<form_code>'
form_url = '{{DOMAIN_URL}}/desform/edit/<form_code>/${BPM_DES_DATA_ID}?token={{TOKEN}}&taskId={{TASKID}}&skip=false'

# 所有表单字段（中文名列表）
all_fields = ['字段A', '字段B', '审批意见1', '审批意见2', ...]

# 每个节点 → 该节点可编辑且必填的审批意见字段
node_editable_fields = {
    'task_node1': {'审批意见1'},
    'task_node2': {'审批意见2'},
}

for node_code, editable_set in node_editable_fields.items():
    # 1. 开启表单可编辑 + 设置表单地址
    edit_node_config(api_base, token, process_id, node_code, {
        'formEditStatus': '1',
        'modelAndView': form_url,
        'modelAndViewMobile': 'check/desForm/flowedit',
    })

    # 2. 设置字段权限：对应审批意见字段必填，其余只读
    perms = []
    for field in all_fields:
        if field in editable_set:
            perms.append({'field': field, 'visible': True, 'editable': True, 'required': True})
        else:
            perms.append({'field': field, 'visible': True, 'editable': False, 'required': False})
    set_node_field_permissions(api_base, token, process_id, node_code, form_code, perms)
```

#### 第三步：节点配置修改后重新发布流程

> **重要：** 修改节点 `formEditStatus`、`modelAndView`、字段权限等配置后，**必须重新发布流程**，否则已发布版本不会生效。

```python
from bpmn_creator import deploy_process
result = deploy_process(api_base, token, process_id)
# success: True → 发布成功
```

---

### Step 7: 输出结果

脚本会自动输出流程 ID、名称、Key、发布状态等信息。

### Step 7.5: 流程高级配置（可选）

流程创建/发布后，可通过以下 API 修改流程的高级配置（通知方式、催办、撤回、督办等）：

**API：** `PUT /act/process/extActProcess/edit`

**请求体（JSON）：**
```json
{
    "id": "{流程ID}",
    "notifyWay": "system,dingtalk,email,wechat_enterprise",
    "urgeStatus": "1",
    "backStatus": "1",
    "graphicStatus": "1",
    "autoSubmitStatus": "0",
    "pcIcon": "",
    "appIcon": "",
    "messageTemplate": "bpm_node_notify",
    "izSupervise": 0
}
```

**字段说明：**

| 字段 | 说明 | 取值 |
|------|------|------|
| `notifyWay` | 通知方式（逗号分隔） | `system`=系统消息, `dingtalk`=钉钉, `email`=邮件, `wechat_enterprise`=企业微信 |
| `urgeStatus` | 允许催办 | `"1"`=开, `"0"`=关 |
| `backStatus` | 允许撤回 | `"1"`=开, `"0"`=关 |
| `graphicStatus` | 显示流程图 | `"1"`=开, `"0"`=关 |
| `autoSubmitStatus` | 自动提交 | `"1"`=开, `"0"`=关 |
| `messageTemplate` | 消息模板 | `bpm_node_notify`（默认） |
| `izSupervise` | 督办 | `1`=开, `0`=关 |
| `pcIcon` | PC 端图标 | 图标路径或留空 |
| `appIcon` | 移动端图标 | 图标路径或留空 |

**Python 示例：**
```python
def edit_process_config(api_base, token, process_id, config):
    """修改流程高级配置"""
    data = {'id': process_id, **config}
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        f'{api_base}/act/process/extActProcess/edit',
        data=body,
        headers={
            'X-Access-Token': token,
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Sign': '00000000000000000000000000000000',
            'X-Tenant-Id': '1',
        },
        method='PUT'
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode('utf-8'))

# 示例：只开启系统消息+钉钉，关闭催办和撤回
edit_process_config(api_base, token, process_id, {
    'notifyWay': 'system,dingtalk',
    'urgeStatus': '0',
    'backStatus': '0',
    'graphicStatus': '1',
    'autoSubmitStatus': '0',
    'messageTemplate': 'bpm_node_notify',
    'izSupervise': 0,
})
```

---

### Step 7.6: 设置报表打印地址（可选）

流程关联了积木报表后，用户可在审批详情页直接打印报表。**仅 formType=3（自定义开发表单）支持此配置。**

**正确 API：** `PUT /act/process/extActProcessForm/edit`（不是 extActProcess/edit）

**reportPrintUrl 格式（通用模板，只替换报表ID）：**
```
{{DOMAIN_URL}}/jmreport/view/{积木报表ID}?id={{DATAID}}&token={{TOKEN}}&procInstId={{PROCINSTID}}
```

**操作步骤：**

1. 查询流程表单绑定记录，获取记录 id
2. 调用 edit 接口更新 `reportPrintUrl` 字段

**Python 示例：**
```python
import json, urllib.request, urllib.parse

def set_report_print_url(api_base, token, process_id, report_id):
    headers = {
        'X-Access-Token': token,
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Sign': '00000000000000000000000000000000',
        'X-Tenant-Id': '1',
    }

    # Step 1: 查询表单绑定记录
    url = f'{api_base}/act/process/extActProcessForm/list?processId={process_id}'
    req = urllib.request.Request(url, headers=headers)
    result = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    records = result.get('result', {}).get('records', [])
    if not records:
        raise Exception('未找到流程表单绑定记录')
    form_record = records[0]

    # Step 2: 更新 reportPrintUrl
    report_print_url = (
        '{{DOMAIN_URL}}/jmreport/view/' + report_id +
        '?id={{DATAID}}&token={{TOKEN}}&procInstId={{PROCINSTID}}'
    )
    edit_data = {
        'id': form_record['id'],
        'processId': process_id,
        'formDealStyle': form_record.get('formDealStyle', 'default'),
        'formType': form_record.get('formType', '3'),
        'relationCode': form_record.get('relationCode', ''),
        'flowStatusCol': form_record.get('flowStatusCol', 'bpm_status'),
        'titleExp': form_record.get('titleExp', ''),
        'formTableName': form_record.get('formTableName', ''),
        'reportPrintUrl': report_print_url,
    }
    body = json.dumps(edit_data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        f'{api_base}/act/process/extActProcessForm/edit',
        data=body, headers=headers, method='PUT'
    )
    return json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
```

> **常见错误：** 用 `/act/process/extActProcess/edit` + `printUrl` 字段无法生效，必须用 `/act/process/extActProcessForm/edit` + `reportPrintUrl` 字段。

---

## 自定义开发表单（代码生成）关联流程时的前端代码变更

> **触发条件：** 当用户的表有 `bpm_status` 字段，或者要求为代码生成的模块创建审批流程时，前端代码需要做以下变更。
>
> **执行方式：**
> - 如果是通过 **Step 0.5 联合创建场景** 进入的，这些变更由 `jeecg-codegen` skill 在第 1 步生成代码时**自动完成**（在调用 jeecg-codegen 时在需求中明确要求包含 bpm_status 字段和 Form.vue）。
> - 如果是已有代码模块补充流程，则通过 `jeecg-codegen` skill 的**增量修改（场景C）**执行，或手动按以下清单逐一修改。

### 需要变更的文件清单

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `Entity.java` | 增量修改 | 添加 `bpmStatus` 字段 + `@Dict(dicCode = "bpm_status")` |
| `Flyway SQL` | 增量修改 | 添加 `bpm_status varchar(10)` 列 |
| `data.ts` | 增量修改 | columns 添加 `bpmStatus_dictText` 列 + 导出 `getBpmFormSchema()` 函数 |
| `List.vue` | **重新生成** | 添加流程提交/审批进度功能 |
| `Modal.vue` | 增量修改 | `import { formSchema }` 改为 `import { getBpmFormSchema }`，`schemas: formSchema` 改为 `schemas: getBpmFormSchema({})` |
| `Form.vue` | **新建** | BPM 流程审批表单组件 |

### 1. Entity.java — 添加 bpmStatus 字段

```java
//update-begin---author:ai ---date:YYYY-MM-DD  for：【xxx】添加流程状态字段-----------
/**流程状态*/
@Excel(name = "流程状态", width = 15, dicCode = "bpm_status")
@Dict(dicCode = "bpm_status")
@Schema(description = "流程状态")
private String bpmStatus;
//update-end---author:ai ---date:YYYY-MM-DD  for：【xxx】添加流程状态字段-----------
```

### 2. data.ts — 添加 usePermission + columns + getBpmFormSchema

**需要添加的 import 和初始化（文件顶部）：**
```typescript
import { usePermission } from '/@/hooks/web/usePermission';
const { isDisabledAuth, hasPermission, initBpmFormData } = usePermission();
```

**三个函数说明（来自 `/@/hooks/web/usePermission.ts`）：**

| 函数 | 用途 | 用法 |
|------|------|------|
| `initBpmFormData(_formData)` | 加载流程节点的字段权限配置到 usePermission 内部 | 在 `getBpmFormSchema` 中调用，传入流程表单的 formData |
| `hasPermission(code)` | 判断字段是否**可见**（type=1） | 用在 formSchema 的 `show` 属性中 |
| `isDisabledAuth(code)` | 判断字段是否**禁用**（type=2） | 用在 formSchema 的 `dynamicDisabled` 属性中 |

**权限控制原理：**
- 流程节点配置的字段权限存储在 `formData.permissionList` 中（由 BPM 引擎注入）
- `initBpmFormData` 将权限列表加载到 `usePermission` 内部
- `hasPermission(code)` 检查 `permissionList` 中 type=1（显示）的 action 是否包含该 code
- `isDisabledAuth(code)` 检查 `permissionList` 中 type=2（禁用）的 action 是否包含该 code
- code 格式：后端 `set_node_field_permissions` 配置的 `ruleCode`（如 `online:表名:字段名` 或自定义编码）

**columns 第一列添加流程状态：**
```typescript
export const columns: BasicColumn[] = [
  { title: '流程状态', align: 'center', dataIndex: 'bpmStatus_dictText' },
  // ... 其他列
];
```

**formSchema 中使用权限控制字段显示/禁用（示例）：**
```typescript
export const formSchema: FormSchema[] = [
  // 通过 hasPermission 控制字段可见性
  {
    label: '密码', field: 'password', component: 'InputPassword',
    show: ({ values }) => {
      return hasPermission('{{entityPackage}}:{{tableName}}:password');
    },
  },
  // 通过 isDisabledAuth 控制字段禁用
  {
    label: '金额', field: 'amount', component: 'InputNumber',
    dynamicDisabled: ({ values }) => {
      return isDisabledAuth('{{entityPackage}}:{{tableName}}:amount');
    },
  },
  // ... 其他字段
];
```

**getBpmFormSchema 函数（文件末尾）：**
```typescript
export function getBpmFormSchema(_formData): FormSchema[] {
  // 加载流程节点权限配置（必须在返回 formSchema 之前调用）
  initBpmFormData(_formData);
  // 默认和原始表单保持一致 如果流程中配置了权限数据，这里需要单独处理formSchema
  return formSchema;
}
```

> **重要：** `initBpmFormData(_formData)` 必须在 `return formSchema` 之前调用，否则 `hasPermission` 和 `isDisabledAuth` 无法读取到流程节点的权限配置。

### 3. Modal.vue — 替换 formSchema 为 getBpmFormSchema

> **重要：** Modal.vue 必须使用 `getBpmFormSchema` 替代 `formSchema`，否则流程节点配置的字段权限（如 `dynamicDisabled`、`show` 中的 `isDisabledAuth`/`hasPermission`）在普通新增/编辑弹窗中不会生效。传 `{}` 空对象时权限函数返回默认值，不影响正常使用。

**需要修改的两处：**

```typescript
// 修改前：
import { formSchema } from '../{{entityName}}.data';
// 修改后：
import { getBpmFormSchema } from '../{{entityName}}.data';

// 修改前：
schemas: formSchema,
// 修改后：
schemas: getBpmFormSchema({}),
```

> **原理：** `getBpmFormSchema({})` 内部调用 `initBpmFormData({})`，空对象不含 `permissionList`，`hasPermission` 返回 `true`（可见），`isDisabledAuth` 返回 `false`（不禁用），与原始 `formSchema` 行为一致。但在 BPM 流程表单（Form.vue）中，`formData` 包含流程注入的 `permissionList`，权限控制才会真正生效。

### 4. List.vue — 完整 BPM 功能变更

**需要添加的 import：**
```typescript
import { startProcess } from '/@/api/common/api';
```

**需要添加的组件（template 中 Modal 后面）：**
```html
<!-- 审批流程图 -->
<BpmPictureModal @register="registerBpmModal" />
```

**需要添加的变量：**
```typescript
const [registerBpmModal, { openModal: bpmPicModal }] = useModal();
```

**操作栏（getDropDownAction）变更 — 添加"发起流程"和"审批进度"：**
```typescript
function getDropDownAction(record) {
  let dropDownAction = [
    { label: '详情', onClick: handleDetail.bind(null, record) },
    { label: '删除', popConfirm: { title: '是否确认删除', confirm: handleDelete.bind(null, record), placement: 'topLeft' }, auth: '{{entityPackage}}:{{tableName}}:delete' },
    {
      label: '审批进度',
      onClick: handlePreviewPic.bind(null, record),
      ifShow: !!record.bpmStatus && record.bpmStatus !== '1',
    }
  ];
  // bpmStatus 为空或 '1'（未提交）时显示"发起流程"按钮
  if (!record.bpmStatus || record.bpmStatus === '1') {
    dropDownAction.push({
      label: '发起流程',
      popConfirm: { title: '确认提交流程吗？', confirm: handleProcess.bind(null, record), placement: 'topLeft' }
    });
  }
  return dropDownAction;
}
```

**需要添加的方法：**
```typescript
/**
 * 提交流程
 */
async function handleProcess(record) {
  let params = {
    flowCode: 'dev_{{tableName}}_001',    // 与流程关联的唯一编码一致
    id: record.id,
    formUrl: '{{viewDir}}/components/{{entityName}}Form',  // 指向 Form.vue（不是 Modal.vue）
    formUrlMobile: ''
  }
  await startProcess(params);
  handleSuccess();
}

/**
 * 审批进度
 */
async function handlePreviewPic(record) {
  bpmPicModal(true, {
    flowCode: 'dev_{{tableName}}_001',
    dataId: record.id,
  });
}
```

### 5. Form.vue — BPM 流程审批表单（新建文件）

路径：`src/views/{{viewDir}}/components/{{entityName}}Form.vue`

**完整模板：**
```vue
<template>
    <div style="min-height: 400px">
        <BasicForm @register="registerForm"></BasicForm>
        <div style="width: 100%;text-align: center" v-if="!formDisabled">
            <a-button @click="submitForm" pre-icon="ant-design:check" type="primary">提 交</a-button>
        </div>
    </div>
</template>

<script lang="ts">
    import {BasicForm, useForm} from '/@/components/Form/index';
    import {computed, defineComponent} from 'vue';
    import {defHttp} from '/@/utils/http/axios';
    import { propTypes } from '/@/utils/propTypes';
    import {getBpmFormSchema} from '../{{entityName}}.data';
    import {saveOrUpdate} from '../{{entityName}}.api';

    export default defineComponent({
        name: "{{entityName}}Form",
        components:{ BasicForm },
        props:{
            formData: propTypes.object.def({}),
            formBpm: propTypes.bool.def(true),
        },
        setup(props){
            const [registerForm, { setFieldsValue, setProps, getFieldsValue }] = useForm({
                labelWidth: 150,
                schemas: getBpmFormSchema(props.formData),
                showActionButtonGroup: false,
                baseColProps: {span: 24}
            });

            const formDisabled = computed(()=>{
                if(props.formData.disabled === false){
                    return false;
                }
                return true;
            });

            let formData = {};
            const queryByIdUrl = '/{{entityPackagePath}}/{{entityName_uncap}}/queryById';
            async function initFormData(){
                let params = {id: props.formData.dataId};
                const data = await defHttp.get({url: queryByIdUrl, params});
                formData = {...data}
                await setFieldsValue(formData);
                await setProps({disabled: formDisabled.value})
            }

            async function submitForm() {
                let data = getFieldsValue();
                let params = Object.assign({}, formData, data);
                console.log('表单数据', params)
                await saveOrUpdate(params, true)
            }

            initFormData();

            return { registerForm, formDisabled, submitForm }
        }
    });
</script>
```

**关键说明：**
- Form.vue 使用 `defineComponent`（Options API），不是 `<script setup>`
- 通过 `props.formData.dataId` 获取数据 ID，`props.formData.disabled` 控制表单禁用
- `getBpmFormSchema` 从 data.ts 导入，默认返回 formSchema
- `queryByIdUrl` 指向后端 `queryById` 接口
- `formUrl` 参数（List.vue 的 handleProcess 中）指向此 Form 组件路径（不含 `.vue` 后缀）

### 5.1 Form.vue（一对多子表）— 含子表节点字段权限控制

> 适用场景：主表 + 一对多子表（JVxeTable），需在流程节点上对主表字段和子表列分别配置显示/禁用权限。

**与单表 Form.vue 的区别：**

| 差异点 | 单表 Form.vue | 一对多 Form.vue |
|--------|--------------|----------------|
| 模板 | 仅 BasicForm | BasicForm + a-tabs + JVxeTable |
| 子表列权限 | 无 | `filterSubTableColnmns` 过滤 `subPermissionList` |
| 子表数据 | 无 | `purXxxTable.dataSource` 绑定，`initFormData` 加载 |
| submit | `getFieldsValue` | `getFieldsValue` + `ref.getTableData()` |

**完整模板：**

```vue
<template>
  <div style="min-height: 400px">
    <BasicForm @register="registerForm"></BasicForm>
    <!-- 子表tabs -->
    <a-tabs v-model:activeKey="activeKey" animated class="jeecg-tab">
      <a-tab-pane tab="{{subTableLabel}}" key="{{subTableKey}}" :forceRender="true">
        <JVxeTable
          keep-source
          resizable
          ref="{{subTableKey}}"
          :loading="{{subTableKey}}Table.loading"
          :columns="{{subTableKey}}Table.columns"
          :dataSource="{{subTableKey}}Table.dataSource"
          :height="300"
          :rowNumber="true"
          :rowSelection="!formDisabled"
          :disabled="formDisabled"
          :toolbar="!formDisabled"
        />
      </a-tab-pane>
    </a-tabs>
    <div style="width: 100%; text-align: center; margin-top: 8px" v-if="!formDisabled">
      <a-button @click="submitForm" pre-icon="ant-design:check" type="primary">提 交</a-button>
    </div>
  </div>
</template>

<script lang="ts">
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { computed, defineComponent, ref, reactive } from 'vue';
  import { defHttp } from '/@/utils/http/axios';
  import { propTypes } from '/@/utils/propTypes';
  import { JVxeTable } from '/@/components/jeecg/JVxeTable';
  import { getBpmFormSchema, {{subTableKey}}Columns } from '../{{entityName}}.data';
  import { saveOrUpdate } from '../{{entityName}}.api';

  export default defineComponent({
    name: '{{entityName}}Form',
    components: { BasicForm, JVxeTable },
    props: {
      formData: propTypes.object.def({}),
      formBpm: propTypes.bool.def(true),
    },
    setup(props) {
      const [registerForm, { setFieldsValue, setProps, getFieldsValue }] = useForm({
        labelWidth: 150,
        schemas: getBpmFormSchema(props.formData),
        showActionButtonGroup: false,
        baseColProps: { span: 24 },
      });

      const formDisabled = computed(() => {
        if (props.formData.disabled === false) {
          return false;
        }
        return true;
      });

      const activeKey = ref('{{subTableKey}}');
      // 子表 JVxeTable 实例引用，名称必须与模板 ref="{{subTableKey}}" 一致
      const {{subTableKey}} = ref();

      let mainFormData: any = {};
      const queryByIdUrl = '/{{entityPackagePath}}/{{entityName_uncap}}/queryById';
      const querySubUrl = '/{{entityPackagePath}}/{{entityName_uncap}}/query{{SubEntityName}}ByMainId';

      const {{subTableKey}}Table = reactive({
        loading: false,
        dataSource: [],
        // filterSubTableColnmns 根据 subPermissionList 过滤列的显示/禁用
        columns: filterSubTableColnmns({{subTableKey}}Columns, '{{permCodePrefix}}:'),
        show: false,
      });

      /**
       * 子表列权限过滤（从 props.formData.subPermissionList 读取节点配置的列权限）
       * @param columns  原始列配置数组
       * @param pre      流程节点上配置的权限编码前缀，如 'purApplyItemColumns:'
       */
      function filterSubTableColnmns(columns, pre) {
        let authList = props.formData.subPermissionList;
        // 未配置子表权限时原样返回
        if (!authList || authList.length === 0) {
          return columns;
        }
        return columns.filter(item => {
          let oneAuthList = authList.filter(auth => auth.action === pre + item.key);
          if (!oneAuthList || oneAuthList.length === 0) {
            return true;
          }
          let oneAuthHidden = oneAuthList.find(auth => auth.type == '1');
          let oneAuthDisable = oneAuthList.find(auth => auth.type == '2');
          // 隐藏逻辑（type=1 且无权限）
          if (oneAuthHidden && !oneAuthHidden.isAuth) {
            return false;
          }
          // 禁用逻辑（type=2 且无权限）
          if (oneAuthDisable && !oneAuthDisable.isAuth) {
            item['disabled'] = true;
          } else {
            item['disabled'] = false;
          }
          return true;
        });
      }

      async function initFormData() {
        let params = { id: props.formData.dataId };
        const data = await defHttp.get({ url: queryByIdUrl, params });
        mainFormData = { ...data };
        await setFieldsValue(mainFormData);
        await setProps({ disabled: formDisabled.value });
        // 加载子表数据
        if (props.formData.dataId) {
          {{subTableKey}}Table.loading = true;
          try {
            const items = await defHttp.get({ url: querySubUrl, params: { id: props.formData.dataId } });
            {{subTableKey}}Table.dataSource = items || [];
          } finally {
            {{subTableKey}}Table.loading = false;
          }
        }
      }

      async function submitForm() {
        let data = getFieldsValue();
        // 优先从 JVxeTable 实例获取含用户编辑的最新数据
        let items: any[] = {{subTableKey}}Table.dataSource;
        if ({{subTableKey}}.value?.getTableData) {
          items = {{subTableKey}}.value.getTableData() || {{subTableKey}}Table.dataSource;
        }
        let params = Object.assign({}, mainFormData, data, {
          {{subTableKey}}List: items,
        });
        await saveOrUpdate(params, true);
      }

      initFormData();

      return {
        registerForm,
        formDisabled,
        activeKey,
        {{subTableKey}},
        {{subTableKey}}Table,
        submitForm,
      };
    },
  });
</script>

<style lang="less" scoped>
  .jeecg-tab { padding: 0 20px; }
  :deep(.ant-input-number) { width: 100%; }
</style>
```

**模板变量说明：**

| 变量 | 示例值 | 说明 |
|------|--------|------|
| `{{subTableLabel}}` | `采购明细` | tab 标签文字 |
| `{{subTableKey}}` | `purPurchaseApplyItem` | ref 名称、reactive key 名，需与 data.ts 中列变量名前缀对应 |
| `{{subTableKey}}Columns` | `purPurchaseApplyItemColumns` | data.ts 导出的子表列配置 |
| `{{permCodePrefix}}` | `purApplyItemColumns` | 流程节点上配置子表列权限时的编码前缀（不含末尾冒号） |
| `{{SubEntityName}}` | `PurPurchaseApplyItem` | 子表实体大驼峰名，用于拼接后端接口路径 |
| `{{subTableKey}}List` | `purPurchaseApplyItemList` | 提交时子表数组的字段名（与后端 DTO 一致） |

**关键注意事项：**

1. `filterSubTableColnmns` 读取 `props.formData.subPermissionList`（由 BPM 引擎注入），`subPermissionList` 为空时不过滤任何列，原样显示
2. 模板中 `ref="{{subTableKey}}"` 与 setup 返回的 `{{subTableKey}}` 变量名**必须一致**，否则 `getTableData()` 拿不到用户编辑的数据
3. 子表数据加载/loading 统一操作 `{{subTableKey}}Table.dataSource` 和 `{{subTableKey}}Table.loading`，不可另建独立 ref（模板绑定的是 reactive 对象）
4. `submitForm` 中优先用 `ref.value.getTableData()` 拿最新数据，降级到 `table.dataSource`
5. `getBpmFormSchema(props.formData)` 内部调用 `initBpmFormData(props.formData)`，确保主表字段的 `show`/`dynamicDisabled` 能读取到节点权限

### 5.2 Form.vue（含一对一子表）— 嵌入 BasicForm 子组件 + 节点字段权限控制

> 适用场景：主表 + 一对一子表（BasicForm 嵌入），需在流程节点上对一对一子表字段配置显示/禁用权限。

#### data.ts 中为一对一子表单独导出 getBpmFormSchemaOne

一对一子表需要独立的 `getBpmFormSchemaOne(formData)` 函数，同样调用 `initBpmFormData`：

```typescript
export function getBpmFormSchemaOne(formData): FormSchema[] {
  const { isDisabledAuth, hasPermission, initBpmFormData } = usePermission();
  initBpmFormData(formData);
  const bpmFormSchemaOne: FormSchema[] = [
    { label: '', field: 'id',     component: 'Input', show: false },
    { label: '', field: 'mainId', component: 'Input', show: false },
    {
      label: '客户名称', field: 'customerName', required: true, component: 'Input',
      dynamicDisabled: ({ values }) => isDisabledAuth('salOne:customerName'),
    },
    {
      label: '联系人', field: 'contactPerson', component: 'Input',
      show: ({ values }) => hasPermission('salOne:contactPerson'),
    },
    // ... 其他字段
  ];
  return bpmFormSchemaOne;
}
```

**ruleCode 命名约定（三类并存时区分前缀）：**

| 子表类型 | ruleCode 前缀 | 示例 |
|---------|--------------|------|
| 主表字段 | `{模块}:` | `sal:orderNo` |
| 一对一子表字段 | `{模块}One:` | `salOne:customerName` |
| 一对多子表列 | `{子表变量名}Columns:` | `salOrderItemColumns:productName` |

**formBizCode 统一用主表名**（三类权限记录的 formBizCode 均相同）：`sal_sales_order`

#### 一对一子表组件（XxxOneForm.vue）

```vue
<template>
  <BasicForm @register="registerForm" name="{{EntityName}}OneForm" class="basic-modal-form" />
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { getBpmFormSchemaOne } from '../{{EntityName}}.data';
  import { defHttp } from '/@/utils/http/axios';
  import { VALIDATE_FAILED } from '/@/utils/common/vxeUtils';
  import { propTypes } from '@/utils/propTypes';

  export default defineComponent({
    name: '{{EntityName}}OneForm',
    components: { BasicForm },
    emits: ['register'],
    props: {
      formData: propTypes.object.def({}),
      disabled: { type: Boolean, default: false },
    },
    setup(props, { emit }) {
      const [registerForm, { setProps, resetFields, setFieldsValue, getFieldsValue, validate, scrollToField }] = useForm({
        schemas: getBpmFormSchemaOne(props.formData),   // ← 传入 formData 激活节点权限
        showActionButtonGroup: false,
        baseColProps: { span: 12 },
      });

      /**
       * 初始化加载数据（由父组件 Form.vue 调用）
       * @param url  子表查询接口，如 /sal/salSalesOrder/querySalCustomerInfoByMainId
       * @param id   主表 ID
       */
      function initFormData(url, id) {
        if (id) {
          defHttp.get({ url, params: { id } }, { isTransformResponse: false }).then((res) => {
            if (res.success && res.result && res.result.length > 0) {
              setFieldsValue({ ...res.result[0] });
            }
          });
        }
        setProps({ disabled: props.disabled });
      }

      /** 获取表单数据（返回数组，与后端 List<Entity> 一致） */
      function getFormData() {
        let formData = getFieldsValue();
        Object.keys(formData).map((k) => {
          if (formData[k] instanceof Array) formData[k] = formData[k].join(',');
        });
        return [formData];
      }

      /** 表单校验 */
      function validateForm(index) {
        return new Promise((resolve, reject) => {
          validate()
            .then(() => resolve(undefined))
            .catch(({ errorFields }) =>
              reject({ error: VALIDATE_FAILED, index, errorFields, scrollToField })
            );
        });
      }

      return { registerForm, resetFields, initFormData, getFormData, validateForm };
    },
  });
</script>

<style lang="less" scoped>
  .basic-modal-form { overflow: auto; height: 280px; }
</style>
```

#### 父级 Form.vue 中嵌入一对一子表组件

在主 Form.vue 的 `<template>` 中通过 `ref` 引用子组件，调用其 `initFormData` / `getFormData` / `validateForm`：

```vue
<template>
  <div>
    <BasicForm @register="registerForm" />
    <!-- 一对一子表 -->
    <{{EntityName}}OneForm ref="oneFormRef" :formData="props.formData" :disabled="formDisabled" />
    <!-- 一对多子表（JVxeTable） -->
    ...
  </div>
</template>

<script lang="ts">
  // initFormData 中加载一对一数据
  const oneFormRef = ref();
  async function initFormData() {
    const data = await defHttp.get({ url: queryByIdUrl, params: { id: props.formData.dataId } });
    await setFieldsValue(data);
    // 加载一对一子表
    oneFormRef.value?.initFormData('/sal/salSalesOrder/querySalCustomerInfoByMainId', props.formData.dataId);
  }

  // submitForm 中收集一对一数据
  async function submitForm() {
    let data = getFieldsValue();
    let oneData = oneFormRef.value?.getFormData() || [];
    let params = Object.assign({}, mainFormData, data, {
      salCustomerInfoList: oneData,       // 一对一子表数据
      salOrderItemList: tableData,        // 一对多子表数据
    });
    await saveOrUpdate(params, true);
  }
</script>
```

#### 节点字段权限配置（一对一子表）

一对一子表字段的权限记录与主表字段写入同一批次，`formBizCode` 统一用主表名：

```python
perms = [
    # 主表字段
    {"ruleCode": "sal:orderNo",         "formBizCode": "sal_sales_order", ...},
    # 一对一子表字段（formBizCode 仍用主表名）
    {"ruleCode": "salOne:customerName", "formBizCode": "sal_sales_order", ...},
    {"ruleCode": "salOne:phone",        "formBizCode": "sal_sales_order", ...},
    # 一对多子表列（formBizCode 仍用主表名）
    {"ruleCode": "salOrderItemColumns:productName", "formBizCode": "sal_sales_order", ...},
]
```

> **是否需要 sys_permission？**
> 含一对多子表的表单（主表 + 一对一 + 一对多）属于"一对多场景"，全部字段（含一对一子表字段）均**不需要**添加 sys_permission，BPM 引擎直接通过 `formData.permissionList` 注入。

---

### flowCode 命名规则

`flowCode` 必须与流程关联表单时的 `relationCode` 一致：
- 自定义开发（formType=3）：`dev_{表名}_001`
- Online（formType=1）：`onl_{表名}`
- DesForm（formType=2）：`desform_{编码}`

---

## OA 应用一键生成（表单 + 流程 + 授权）

> 当用户说"创建审批单"、"创建报销单"、"做一个OA表单带流程"等，使用本章节一次性完成 **表单设计 → 流程创建 → 流程发布 → 表单关联 → 角色授权**。

### OA 交互流程

#### OA Step 0: 解析用户需求

从用户描述中提取：

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 应用名称 | 用户指定 | "费用报销单" |
| 表单编码 | 英文命名，`oa_` 前缀 | `oa_expense_reimbursement` |
| 表单字段 | 从描述中解析 | 申请人、金额、附件等 |
| 流程节点 | 从描述中解析 | 提交→部门审批→财务审核→结束 |
| 审批人 | 从描述中解析 | 角色/指定人/表达式 |

#### OA Step 1: 展示应用摘要并确认

**必须展示以下内容，等待用户确认后再执行：**

```
## OA 应用摘要

- 应用名称：费用报销单
- 表单编码：oa_expense_reimbursement
- 目标环境：<api_base>

### 表单字段

| 序号 | 字段名称 | 控件类型 | 必填 | 说明 |
|------|---------|---------|------|------|
| 1 | 申请人 | select-user | 是 | 标题字段 |
| 2 | 报销金额 | money | 是 | |
| ... | ... | ... | ... | ... |

### 流程节点

| 序号 | 节点名称 | 类型 | 审批人 |
|------|---------|------|--------|
| 1 | 开始 | startEvent | - |
| 2 | 提交申请 | userTask (草稿) | ${applyUserId} |
| ... | ... | ... | ... |

### 连线

开始 → 提交 → 审批 → 结束

确认以上信息正确？(y/n)
```

#### OA Step 2: 一键执行创建

用户确认后，使用 `scripts/bpmn_oa.py` 脚本一次性完成全部操作。

**使用步骤：**
1. 根据用户需求生成 JSON 配置文件（Write 到工作目录的临时 `.json` 文件）
2. 用 Bash 执行脚本：
```bash
python "<jeecg-bpmn skill目录>/scripts/bpmn_oa.py" \
    --api-base <后端地址> \
    --token <TOKEN> \
    --config <config.json>
```
3. 删除临时 JSON 配置文件

**脚本自动完成：**
1. 创建设计器表单（调用 desform_creator）
2. 创建 BPMN 流程（调用 bpmn_creator）
3. 发布流程
4. 关联表单到流程
5. 设置草稿节点表单可编辑 + 表单地址
6. 查询已有授权 → 追加新表单ID → 保存授权给管理员角色

### OA JSON 配置格式

```json
{
  "appName": "费用报销单",
  "form": {
    "formName": "费用报销单",
    "formCode": "oa_expense_reimbursement",
    "layout": "word",
    "titleIndex": 2,
    "fields": [
      {"name": "报销单号", "type": "auto-number", "prefix": "BXBX"},
      {"name": "---", "type": "divider", "text": "基本信息"},
      {"name": "申请人", "type": "select-user", "required": true},
      {"name": "所在部门", "type": "select-depart", "required": true},
      {"name": "申请日期", "type": "date", "required": true},
      {"name": "报销类别", "type": "select", "required": true, "options": ["差旅费", "交通费", "办公用品"]},
      {"name": "---", "type": "divider", "text": "费用明细"},
      {"name": "报销金额", "type": "money", "required": true, "unit": "元"},
      {"name": "费用说明", "type": "textarea"},
      {"name": "发票/凭证", "type": "imgupload", "required": true},
      {"name": "附件", "type": "file-upload"},
      {"name": "---", "type": "divider", "text": "审批信息"},
      {"name": "部门负责人意见", "type": "oa-approval-comments"},
      {"name": "财务审核意见", "type": "oa-approval-comments"}
    ]
  },
  "process": {
    "processName": "费用报销审批流程",
    "processKey": "oa_expense_reimbursement_process",
    "typeId": "oa",
    "nodes": [
      {"id": "start", "type": "startEvent", "name": "开始"},
      {"id": "task_draft", "type": "userTask", "name": "提交报销申请", "draft": true,
       "assignee": {"type": "expression", "value": "applyUserId"}},
      {"id": "task_dept", "type": "userTask", "name": "部门负责人审批",
       "assignee": {"type": "role", "value": "manager"}},
      {"id": "task_finance", "type": "userTask", "name": "财务审核",
       "assignee": {"type": "role", "value": "finance"}},
      {"id": "end", "type": "endEvent", "name": "结束"}
    ],
    "flows": [
      {"id": "flow_1", "source": "start", "target": "task_draft"},
      {"id": "flow_2", "source": "task_draft", "target": "task_dept"},
      {"id": "flow_approve", "source": "task_dept", "target": "task_finance", "name": "通过"},
      {"id": "flow_reject", "source": "task_dept", "target": "end", "name": "拒绝"},
      {"id": "flow_end", "source": "task_finance", "target": "end"}
    ]
  },
  "auth": {
    "roleId": "f6817f48af4fb3af11b9e8bf182f618b",
    "authMode": "role"
  },
  "nodePermissions": {
    "task_draft": [
      {"field": "报销单号", "visible": true, "editable": false},
      {"field": "报销金额", "visible": true, "editable": true, "required": true}
    ],
    "task_dept": [
      {"field": "部门负责人意见", "visible": true, "editable": true}
    ]
  }
}
```

> **nodePermissions（可选）：** 按节点编码配置字段权限。key 为节点 ID（如 `task_draft`），value 为字段权限数组。`field` 支持中文字段名或字段 model。`required=true` 时自动强制 `visible=true` + `editable=true`。

### OA 表单字段类型

| type | 可选参数 | 说明 |
|------|---------|------|
| `input` | `required`, `placeholder`, `unique` | 单行文本 |
| `textarea` | `required` | 多行文本 |
| `number` | `required`, `unit`, `precision` | 数字 |
| `integer` | `required`, `unit` | 整数 |
| `money` | `required`, `unit` | 金额 |
| `date` | `required`, `fmt` | 日期 |
| `time` | `required` | 时间 |
| `radio` | `options`(必填), `required`, `dictCode` | 单选 |
| `select` | `options`(必填), `required`, `multiple`, `dictCode` | 下拉 |
| `checkbox` | `options`(必填), `required`, `dictCode` | 多选 |
| `select-user` | `required`, `multiple` | 选人 |
| `select-depart` | `required`, `multiple` | 选部门 |
| `phone` | `required` | 手机 |
| `email` | `required` | 邮箱 |
| `file-upload` | `required` | 文件上传 |
| `imgupload` | `required` | 图片上传 |
| `hand-sign` | `required` | 手写签名 |
| `auto-number` | `prefix` | 自动编号 |
| `divider` | `text` | 分隔符 |
| `formula` | `mode`, `expression`, `decimal`, `unit` | 公式 |
| `location` | `required` | 定位 |
| `barcode` | `codeType` | 条码 |
| `editor` | `required` | 富文本 |
| `oa-approval-comments` | - | 审批意见（grid 6:18布局，禁用状态） |

> **审批意见组件规则：** 当字段名包含"意见"、"签字"、"审批"等关键词（如"部门负责人意见"、"财务审核签字"），**必须**使用 `oa-approval-comments` 类型，**不要**使用 `hand-sign` 或 `textarea`。该组件自动生成 grid 布局（左侧标签 + 右侧审批意见区域），默认禁用，由流程节点控制启用。

### OA 流程分支规则

> **重要：** 生成流程 JSON 配置时，必须根据表单字段决定分支方式：
> - **表单有 `result` 等可用于条件判断的字段** → 使用 `exclusiveGateway` + `conditions` 条件分支
> - **表单没有 `result` 字段** → 使用**手工分支**（从 userTask 直接引出多条无条件的 sequenceFlow）
>
> **手工分支使用前提：** 仅在通过/拒绝后还需要经过不同的后续处理节点时才使用。如果审批后只有结束节点，不需要手工分支，直接连到结束即可。

### OA callActivity 外部子流程

使用 callActivity 需要**两步创建**：

**第 1 步：先创建并部署外部子流程**（使用 `bpmn_creator.py`）

OA 类子流程（如借款、用车）**不关联独立表单**，draft 节点 PC 地址复用主流程 DesForm：

```json
{
  "processName": "借款申请子流程",
  "processKey": "oa_business_trip_loan_sub",
  "typeId": "oa",
  "isSubProcess": true,
  "draftNodeForm": {
    "formType": "desform",
    "formCode": "oa_business_trip_apply",
    "mode": "edit"
  },
  "nodes": [
    {"id": "start", "type": "startEvent", "name": "开始"},
    {"id": "task_draft", "type": "userTask", "name": "填写借款申请", "draft": true,
     "assignee": {"type": "expression", "value": "applyUserId"}},
    {"id": "task_finance", "type": "userTask", "name": "财务审批",
     "assignee": {"type": "role", "value": "admin"}},
    {"id": "end", "type": "endEvent", "name": "结束"}
  ],
  "flows": [
    {"id": "flow_1", "source": "start", "target": "task_draft"},
    {"id": "flow_2", "source": "task_draft", "target": "task_finance"},
    {"id": "flow_3", "source": "task_finance", "target": "end"}
  ]
}
```

> **关键规则：**
> - `isSubProcess: true` — start 节点纳入 nodes 参数（必须，否则设计器看不到 start 节点）
> - `draftNodeForm` — draft 节点 PC 地址指向**主流程**的 DesForm（不配置则无 PC 表单地址）
> - **不要**加 `formLink` — OA 子流程不需要关联独立表单
> - `draftNodeForm.formCode` 填**主流程**的表单编码（如 `oa_business_trip_apply`）

**第 2 步：创建主 OA 应用**（使用 `bpmn_oa.py`），在主流程 JSON 中用 callActivity 节点引用子流程：
```json
{"id": "call_loan", "type": "callActivity", "name": "借款子流程",
 "calledElement": "oa_business_trip_loan_sub"}
```
`calledElement` 必须与子流程的 `processKey` 一致。

### 会签子流程（自动创建规则）

> **执行规则：当流程中包含会签子流程节点（`callActivity` + `multiInstanceLoopCharacteristics`）时，无需询问用户是否创建子流程，直接按以下步骤自动创建并部署。**

#### 创建步骤

**第 1 步：创建会签子流程**（`bpmn_creator.py`）

```json
{
  "processName": "XXX会签子流程",
  "processKey": "<calledElement值>",
  "typeId": "oa",
  "isCountersignSubProcess": true,
  "nodes": [
    {"id": "start", "type": "startEvent", "name": "开始"},
    {"id": "sub_task_review", "type": "userTask", "name": "会签审核",
     "assignee": {"type": "expression", "value": "assigneeUserId"}},
    {"id": "end", "type": "endEvent", "name": "结束"}
  ],
  "flows": [
    {"id": "f1", "source": "start", "target": "sub_task_review"},
    {"id": "f2", "source": "sub_task_review", "target": "end"}
  ]
}
```

关键规则：
- `isCountersignSubProcess: true` — 自动添加 `SubProcessHqStartListener`，区别于普通子流程的 `SubProcessStartListener`
- 任务节点 assignee 固定用 `assigneeUserId`（由主流程 callActivity 通过 `flowable:in` 传入）
- **不加** `formLink`、**不加** `draftNodeForm`

**第 2 步：配置所有节点表单地址**（发布前，指向主流程表单 detail 模式）

```python
DETAIL_URL = '{{DOMAIN_URL}}/desform/detail/<主流程formCode>/${BPM_DES_DATA_ID}?token={{TOKEN}}&taskId={{TASKID}}&skip=false'
# 通过 /act/process/extActProcessNode/list 查询节点列表
# 逐个调用 /act/process/extActProcessNode/edit 设置 modelAndView + modelAndViewMobile
```

**第 3 步：重新发布子流程**（`deploy_process`）

#### 更新流程 XML 的正确方式

> **重要：** `/act/designer/api/saveProcess` 不会更新 `ext_act_process.process_xml`，必须直接操作数据库：

```python
# 1. 从数据库读取 XML
conn = pymysql.connect(...)
cur.execute('SELECT process_xml FROM ext_act_process WHERE id=%s', (process_id,))
xml = cur.fetchone()[0].decode('utf-8')

# 2. 修改 XML（字符串替换）

# 3. 写回数据库
cur.execute('UPDATE ext_act_process SET process_xml=%s WHERE id=%s', (xml.encode('utf-8'), process_id))
conn.commit()

# 4. 调用 deploy API 重新发布
deploy_process(api_base, token, process_id)
```

---

### 常见 OA 应用模板

#### 费用报销单
- 字段：报销单号、申请人、部门、日期、报销类别、金额、说明、发票、附件、部门负责人意见(审批意见)、财务审核意见(审批意见)
- 流程：提交 → 部门审批 →(手工分支: 通过/拒绝)→ 财务审核 → 结束
- **注意：** 表单无 result 字段，使用手工分支

#### 请假申请单
- 字段：申请人、部门、日期、请假类型、开始/结束日期、天数、说明、附件、部门负责人意见(审批意见)
- 流程：提交 → 部门审批 → 结束
- **注意：** 审批后只有结束节点，不需要手工分支

#### 采购申请单
- 字段：申请人、部门、日期、采购物品、数量、预算金额、供应商、说明、附件、部门负责人意见(审批意见)、总经理意见(审批意见)
- 流程：提交 → 部门审批 →(手工分支: 通过/拒绝)→ 总经理审批 → 结束

#### 出差申请单（含 callActivity 子流程）
- 字段：申请人、部门、出差地点、开始/结束日期、天数、事由、预算、附件、部门负责人意见(审批意见)、总监审批意见(审批意见)、财务审批意见(审批意见)
- 子流程：借款子流程（processKey: oa_business_trip_loan_sub），含财务审批节点
- 主流程：提交 → 部门审批 →(手工分支: 同意/不同意)→ 总监审批 → 借款子流程(callActivity) → 结束
- **注意：** 需先用 `bpmn_creator.py` 创建子流程（设置 `isSubProcess:true` + `draftNodeForm` 指向主流程表单，不加 `formLink`），再用 `bpmn_oa.py` 创建主流程

---

## 编辑已有流程

在 JSON 配置中传入 `"processId": "已有流程ID"` 即可更新流程。

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401/认证失败） | 提示用户重新获取 X-Access-Token |
| `流程ID重复` | 重新生成时间戳作为 processkey |
| `不是最新版本` | 先查询最新的 processDefinitionId 再保存 |
| 中文乱码 | 确认使用 Python urllib（不要用 curl） |
| 连接超时 | 确认后端地址可达，检查网络 |

## 数据库配置表

流程创建后，可通过以下数据库表进一步配置节点行为、表单绑定和字段权限：

| 表名 | 说明 | 用途 |
|------|------|------|
| `ext_act_process` | 流程主表 | 流程属性、XML、发起方式、催办/撤回/通知等 |
| `ext_act_process_form` | 表单绑定 | 流程与业务表单关联，标题表达式，表单类型（1=Online/2=DesForm/3=自定义） |
| `ext_act_process_node` | 节点配置 | 每个审批节点的功能开关（编辑/抄送/转办/加签/驳回等） |
| `ext_act_process_node_auth` | 字段权限 | 每个节点上表单字段的显示/隐藏/可编辑/禁用控制 |

详细的字段说明和取值参见 `references/bpmn-db-config.md`。

## 参考文档

- 阅读 `references/bpmn-call-activity.md` 获取调用子流程（callActivity）详细说明
- 阅读 `references/bpmn-manual-branch.md` 获取手工分支（意见分支）详细说明
- 阅读 `references/bpmn-templates.md` 获取参考文件索引（已拆分为 8 个子文件）

