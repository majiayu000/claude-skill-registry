---
name: dataworks-open-api
description: Operate Alibaba Cloud DataWorks through dynamic API discovery and official SDKs (Node.js, Python, Java). Covers data development, workflow operations, data integration, data quality, metadata lineage, workspace management, and more. APIs are discovered at runtime from official docs and OpenAPI metadata — no hardcoded list.
source: https://github.com/aliyun/alibabacloud-bigdata-skills
homepage: https://github.com/aliyun/alibabacloud-bigdata-skills/tree/main/skills/dataworks/open-api
env:
  - name: ALIBABA_CLOUD_ACCESS_KEY_ID
    description: Alibaba Cloud Access Key ID (required unless using credentials URI or shared config)
    required: false
  - name: ALIBABA_CLOUD_ACCESS_KEY_SECRET
    description: Alibaba Cloud Access Key Secret (required unless using credentials URI or shared config)
    required: false
  - name: ALIBABA_CLOUD_REGION_ID
    description: Target region (e.g. cn-shanghai, cn-beijing). Optional; skill will prompt if unset.
    required: false
  - name: ALIBABA_CLOUD_CREDENTIALS_URI
    description: HTTP endpoint for dynamic AK/SK/STS token (alternative to explicit AK/SK)
    required: false
---

# DataWorks (dataworks-public)

Use Alibaba Cloud OpenAPI (RPC) with official SDKs or OpenAPI Explorer to manage all DataWorks resources. MCP Server is available as an alternative integration.

## Workflow

1. Confirm region, project/resource identifiers, and desired action.
2. Discover available APIs and required parameters (see API discovery below).
3. Call API via SDK.
4. Verify results with describe/list/get APIs.

### Troubleshooting fallback chain (follow this order)

If execution fails at any step, escalate to the next level:

1. **Cookbook** — check `references/cookbook.md` first. It contains verified API patterns, pitfalls, error recovery, the full end-to-end lifecycle (Create → Submit → Deploy → Run → Monitor), and reusable code snippets. Most common issues are already documented there.
2. **Official help docs** — read the API overview and per-API doc pages.
   - If an API call fails or the request/error is not understood, fetch the API directory page to locate the relevant API documentation:
     `https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-dir`
     Browse the category list, find the matching API name, and navigate to its detail page (URL pattern: `https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-{apinameincamelcase}`) for parameter details, error codes, and usage examples.
     For example, if `CreateNode` fails, find it under "数据开发（新版）" in the directory, then read its detail page: `https://help.aliyun.com/zh/dataworks/developer-reference/api-dataworks-public-2024-05-18-createnode`
3. **OpenAPI metadata** — fetch the raw JSON spec for exact parameter names, types, and required fields.
4. **SDK API docs** — check the typed SDK reference for correct method signatures and request classes.

- Java: `https://aliyunsdk-pages.alicdn.com/apidocs/{PRODUCT_CODE}/{API_VERSION}/java-async-tea/8.0.3/index.html`
- Node.js / Python: see `references/sources.md`

5. **GitHub source code** — read the Java SDK source for model/request class definitions: `https://github.com/aliyun/alibabacloud-java-sdk/tree/master/dataworks-public-20240518` (browse `src/main/java/com/aliyun/dataworks_public20240518/` for request/response models).
6. **MCP Server** — use the MCP Server to call APIs directly (see `references/mcp_server.md`).
7. **Browser** — use browser-use to visit the DataWorks Homepage (`https://dataworks.data.aliyun.com/${ALIBABA_CLOUD_REGION_ID}/#/index`) and inspect the UI behavior, network requests, or page content for clues.

## Credentials priority (must follow)

1. Environment variables: `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET` / `ALIBABA_CLOUD_REGION_ID`
2. Credentials URI: `ALIBABA_CLOUD_CREDENTIALS_URI` (e.g. `http://localhost:7002/api/v1/credentials/0`). The SDK credentials provider automatically fetches and refreshes AK/SK/STS tokens from this HTTP endpoint.
3. Shared config file: `~/.alibabacloud/credentials`

Region policy: `ALIBABA_CLOUD_REGION_ID` is an optional default. If unset, decide the most reasonable region for the task; if unclear, ask the user.

## API discovery

Constants (use these values throughout):

- **PRODUCT_CODE**: `dataworks-public`
- **API_VERSION**: `2024-05-18`
- Use OpenAPI metadata endpoints to list APIs and get schemas (see references).

Do NOT rely on a hardcoded API list. Always discover APIs dynamically. Methods are listed in priority order — try them top-down:

### Method 1: Fetch from official help docs

Run the discovery script to curl the official documentation page and extract the complete API overview:

```bash
python scripts/fetch_api_overview.py
```

This fetches `https://help.aliyun.com/zh/dataworks/developer-reference/api-{PRODUCT_CODE}-{API_VERSION}-overview`, extracts the API list from `window.__ICE_PAGE_PROPS__.docDetailData.storeData.data.content`, and parses the HTML tables into a grouped API overview.

### Method 2: Fetch from OpenAPI metadata (full spec with parameters and responses)

Fetch raw API schemas and parameter definitions:

```bash
python scripts/list_openapi_meta_apis.py
```

This calls `https://next.api.aliyun.com/meta/v1/products/{PRODUCT_CODE}/versions/{API_VERSION}/api-docs.json` and outputs the full API docs JSON and a summary list.

To get the schema of a single API (replace `{ApiName}` with a name from the list above, e.g. `ListProjects`):

```
https://next.api.aliyun.com/meta/v1/products/{PRODUCT_CODE}/versions/{API_VERSION}/apis/{ApiName}/api.json
```

### Method 3: MCP Server tools (curated subset with category and parameter-position metadata)

If the MCP Server is running, use the MCP `tools/list` capability, or fetch `https://dataworks.data.aliyun.com/pop-mcp-tools` directly for the tool catalog JSON. Includes some APIs not in Method 2 (e.g. data service, permission approval).

## Calling APIs via SDK

**Recommend using the latest SDK version.** The DataWorks SDK is updated frequently with new APIs, bug fixes, and model changes. Check the latest version from the package registry before installing:

- Node.js: `https://www.npmjs.com/package/@alicloud/dataworks-public20240518`
- Python: `https://pypi.org/project/alibabacloud-dataworks-public20240518/`
- Java: `https://central.sonatype.com/artifact/com.aliyun/alibabacloud-dataworks_public20240518`

Prefer the official Alibaba Cloud SDK. Two styles are supported:

### Style 1: Generalized call (recommended, covers all APIs)

Use `@alicloud/openapi-client` to call any DataWorks API without importing product-specific SDK classes. This is the approach used by the MCP Server source code (`src/tools/callTool.ts`).

```bash
npm install @alicloud/openapi-client @alicloud/openapi-util @alicloud/tea-util @alicloud/credentials
```

```typescript
import OpenApi from "@alicloud/openapi-client";
import Util from "@alicloud/tea-util";

// 1. Create client
const config = new OpenApi.Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
  endpoint: `dataworks.${
    process.env.ALIBABA_CLOUD_REGION_ID || "cn-shanghai"
  }.aliyuncs.com`,
});
const client = new OpenApi.default(config);

// 2. Build request params (RPC style)
const params = new OpenApi.Params({
  style: "RPC",
  action: "ListProjects", // API name
  version: "{API_VERSION}", // see Constants above
  protocol: "HTTPS",
  method: "POST", // GET or POST per API spec
  authType: "AK",
  pathname: "/",
  bodyType: "json",
});

// 3. Build query/body from input
const query = { PageNumber: 1, PageSize: 10 };
const request = new OpenApi.OpenApiRequest({ query });
const runtime = new Util.RuntimeOptions({});

// 4. Call
const res = await client.callApi(params, request, runtime);
console.log(res.body);
```

Key rules from `src/tools/callTool.ts`:

- `style`: `'RPC'` when API has no path; `'ROA'` when it has a path.
- `method`: per API spec (`GET` / `POST` / `PUT` / `DELETE`).
- Parameters with `in: 'query'` go to `query`; `in: 'body'` / `in: 'formData'` go to `body`.
- For `GET` / `DELETE` requests, `body` must be `null` (otherwise signature fails).
- Use `bodyType: 'string'` to avoid precision loss on large numbers.

### Style 2: Product-specific SDK (typed, per-API methods)

```bash
npm install @alicloud/dataworks-public20240518
```

```typescript
import DataWorks from "@alicloud/dataworks-public20240518";
import * as DataWorksClasses from "@alicloud/dataworks-public20240518";
import OpenApi from "@alicloud/openapi-client";

const config = new OpenApi.Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
  endpoint: `dataworks.cn-shanghai.aliyuncs.com`,
});
const client = new DataWorks.default(config);

// Each API has a typed Request class and a method
const request = new DataWorksClasses.ListProjectsRequest({
  pageNumber: 1,
  pageSize: 10,
});
const runtime = new Util.RuntimeOptions({});
const resp = await client.listProjectsWithOptions(request, runtime);
```

API name → SDK method: `ListProjects` → `client.listProjectsWithOptions(request, runtime)`.

### Python SDK

```bash
pip install alibabacloud_dataworks_public20240518
```

```python
import os
from alibabacloud_dataworks_public20240518.client import Client
from alibabacloud_dataworks_public20240518 import models
from alibabacloud_tea_openapi.models import Config

config = Config(
    access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
    access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
    endpoint=f"dataworks.{os.environ.get('ALIBABA_CLOUD_REGION_ID', 'cn-shanghai')}.aliyuncs.com",
)
client = Client(config)
request = models.ListProjectsRequest(page_number=1, page_size=10)
resp = client.list_projects(request)
print(resp.body)
```

### Java SDK

```xml
<dependency>
    <groupId>com.aliyun</groupId>
    <artifactId>alibabacloud-dataworks_public20240518</artifactId>
    <version>8.0.3</version>
</dependency>
```

```java
import com.aliyun.dataworks_public20240518.Client;
import com.aliyun.dataworks_public20240518.models.*;
import com.aliyun.teaopenapi.models.Config;

Config config = new Config()
    .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
    .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"))
    .setEndpoint("dataworks." + System.getenv("ALIBABA_CLOUD_REGION_ID") + ".aliyuncs.com");
Client client = new Client(config);

ListProjectsRequest request = new ListProjectsRequest()
    .setPageNumber(1L)
    .setPageSize(10L);
ListProjectsResponse resp = client.listProjects(request);
System.out.println(resp.getBody());
```

Java SDK API docs: `https://aliyunsdk-pages.alicdn.com/apidocs/{PRODUCT_CODE}/{API_VERSION}/java-async-tea/8.0.3/index.html`

## MCP Server integration (last resort)

Only use MCP when SDK calls keep failing after consulting docs, metadata, and GitHub source:

```bash
npm install -g alibabacloud-dataworks-mcp-server
```

See `references/mcp_server.md` for full configuration.

## API categories

| Category         | Description                                                               | Example APIs                                                                 |
| ---------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 认证文件管理     | Certificate management                                                    | `Import/Get/List/DeleteCertificate`                                          |
| 空间管理         | Workspace, roles, members                                                 | `*Project`, `*ProjectMember`, `*ProjectRole`                                 |
| 数据源           | Data source CRUD and connectivity test                                    | `*DataSource`, `*DataSourceSharedRule`                                       |
| 计算资源         | Compute resource management                                               | `*ComputeResource`                                                           |
| 资源组管理       | Resource groups, routes, networks                                         | `*ResourceGroup`, `*Route`, `*Network`                                       |
| 数据开发（新版） | Nodes, workflows, resources, functions, pipelines                         | `*Node`, `*WorkflowDefinition`, `*Resource`, `*Function`, `*PipelineRun`     |
| 数据集成         | DI sync jobs and alarm rules                                              | `*DIJob`, `*DIAlarmRule`                                                     |
| 数据地图         | Catalogs, databases, tables, columns, lineage, datasets, meta collections | `*Catalog`, `*Table`, `*Column`, `*Lineage*`, `*Dataset*`, `*MetaCollection` |
| 运维中心         | Alerts, tasks, task instances, workflows, workflow instances              | `*AlertRule`, `*Task`, `*TaskInstance*`, `*Workflow`, `*WorkflowInstance*`   |
| 数据质量         | Quality templates, scans, alert rules, scan runs                          | `*DataQualityTemplate`, `*DataQualityScan`, `*DataQualityAlertRule`          |
| 安全中心         | Identity credentials                                                      | `CreateIdentifyCredential`                                                   |
| 标签管理         | Data asset tags                                                           | `*DataAssetTag`, `TagDataAssets`, `UnTagDataAssets`                          |
| 开放平台         | Async job status                                                          | `GetJobStatus`                                                               |

Use dynamic discovery (above) to get the full list and parameter schemas. Common naming patterns:

1. Inventory/list: prefer `List*` / `Get*` / `Describe*` APIs.
2. Create/configure: prefer `Create*` / `Update*` / `Import*` APIs.
3. Remove: prefer `Delete*` / `Remove*` APIs.
4. Lifecycle: prefer `Start*` / `Stop*` / `Suspend*` / `Resume*` / `Rerun*` APIs.

## Destructive operation policy

Before executing delete, stop, or suspend operations, always summarize the affected resources and confirm with the user.

## Timestamp handling

DataWorks APIs use millisecond timestamps. Convert between human-readable dates and timestamps as needed.

## Selection questions (ask when unclear)

1. Which DataWorks project (project ID or name)?
2. Which region? (common: `cn-shanghai`, `cn-beijing`, `cn-hangzhou`, `cn-shenzhen`)
3. What type of operation? (data development / operations / data quality / metadata / workspace)
4. For task operations: target node ID, workflow, or instance ID?

## References

- **Cookbook (verified patterns & pitfalls)**: `references/cookbook.md` — FlowSpec structure for CreateNode, submit-and-deploy flow, data quality rules, bizdate format, response parsing, and FAQ from real-world usage.
- MCP Server integration: `references/mcp_server.md`
- Sources: `references/sources.md`
