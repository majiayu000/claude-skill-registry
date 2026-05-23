---
name: unity-mcp
description: Unity MCP Server 部署指南与 API 使用技巧，包含常见问题排查与解决方案
---

# SKILL: unity-mcp

Unity MCP (Model Context Protocol) Server 的完整部署指南、API 使用技巧和故障排查手册。

## Description

本技能涵盖：
- Unity MCP Server 的启动与连接
- 常用 API 操作（GameObject、Component、Scene、Asset）
- 参数格式规范（Color、Vector3 等特殊类型）
- 常见问题排查与解决思路

## When to Invoke

使用场景：
- 需要通过 AI 控制 Unity 编辑器执行自动化操作
- 批量创建/修改场景物体、组件
- 程序化生成资源或脚本
- 远程调试和场景检查
- 自动化测试工作流

## Prerequisites

**环境要求：**
- Unity 6000+ (或其他支持版本)
- Unity MCP 插件/包已安装
- Python uvx 工具

### 1. 检查 MCP 插件是否安装

在 Unity 编辑器中检查：
- 菜单栏是否有 **MCP** 或 **Window → MCP**
- Project 窗口是否有 `MCP` 或 `McpForUnity` 相关文件夹

**如果未安装 MCP 插件：**

1. **通过 Unity Asset Store 安装:**
   - 打开 **Window → Package Manager**
   - 选择 **Unity Registry** 或 **My Assets**
   - 搜索 **"MCP"** 或 **"MCP for Unity"**
   - 点击 **Install** 安装

2. **或通过 Git URL 安装:**
   - Package Manager → **+** → **Add package from git URL**
   - 输入: `https://github.com/anthropics/unity-mcp.git`
   - 点击 **Add**

3. **安装后重启 Unity**

### 2. 检查 uvx 是否安装

```powershell
# Windows
Test-Path "$env:USERPROFILE\.local\bin\uvx.exe"

# macOS/Linux
which uvx
```

**如果未安装:**
1. 在 Unity 编辑器中打开 **Window → MCP → Local Setup**
2. 点击 **"Install"** 或 **"Setup Environment"**
3. 等待自动下载安装 uvx 和相关依赖
4. 重启终端/IDE 以加载新的环境变量

**插件来源：**
- Unity MCP Server: `mcpforunityserver>=0.0.0a0`

## Deployment

### 1. 启动 MCP Server

#### 检查 uvx 安装位置

uvx 通常安装在以下位置：

**Windows:**
```powershell
# 标准安装路径
$env:USERPROFILE\.local\bin\uvx.exe
# 或
C:\Users\<用户名>\.local\bin\uvx.exe

# 检查是否存在
Test-Path "$env:USERPROFILE\.local\bin\uvx.exe"
```

**macOS/Linux:**
```bash
~/.local/bin/uvx
# 或
/usr/local/bin/uvx
```

#### 如果 uvx 不存在

**⚠️ 提示用户:**
```
未找到 uvx 工具。请在 Unity 编辑器中：
1. 打开 Window → MCP → Local Setup
2. 点击 "Install Dependencies" 或 "Setup Local Environment"
3. 等待安装完成
4. 重新尝试启动 MCP Server
```

#### 启动命令

**Windows (动态路径):**
```powershell
$uvxPath = "$env:USERPROFILE\.local\bin\uvx.exe"
if (Test-Path $uvxPath) {
    & $uvxPath --prerelease explicit --from "mcpforunityserver>=0.0.0a0" mcp-for-unity --transport http --http-url http://localhost:8080 --project-scoped-tools
} else {
    Write-Host "错误: 未找到 uvx。请在 Unity 中点击 MCP → Local Setup 安装依赖。"
}
```

**macOS/Linux:**
```bash
~/.local/bin/uvx --prerelease explicit --from "mcpforunityserver>=0.0.0a0" mcp-for-unity --transport http --http-url http://localhost:8080 --project-scoped-tools
```

**注意：**
- 首次启动会下载 Python 依赖（约 30MB，需要 1-2 分钟）
- 保持运行，不要关闭终端
- 使用 `--project-scoped-tools` 启用项目级工具

### 2. 连接流程

```
1. 初始化会话
   POST http://localhost:8080/mcp
   Headers: Accept: application/json, text/event-stream
   Body: {"jsonrpc":"2.0","id":1,"method":"initialize",...}
   ↓
2. 提取 Session ID (从响应头 mcp-session-id)
   ↓
3. 设置活动 Unity 实例
   ↓
4. 执行工具调用
```

**PowerShell 示例：**
```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Accept" = "application/json, text/event-stream"
    "mcp-session-id" = "your-session-id"
}

# 初始化
$init = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'
$response = Invoke-WebRequest -Uri "http://localhost:8080/mcp" -Method Post -Headers $headers -Body $init
$sessionId = $response.Headers["mcp-session-id"]

# 设置活动实例
$setInstance = '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"set_active_instance","arguments":{"instance":"ProjectName@hash"}}}'
```

## Common Operations

### GameObject 管理

```json
// 创建空物体
{
  "name": "manage_gameobject",
  "arguments": {
    "action": "create",
    "name": "MyObject",
    "position": [0, 0, 0]
  }
}

// 创建 Sprite 物体（2D）
{
  "action": "create",
  "name": "Tree2D",
  "position": [1, 2, 0]
}
// 然后添加 SpriteRenderer 组件

// 删除物体
{
  "action": "delete",
  "name": "MyObject"
}
```

### Component 管理

```json
// 添加组件
{
  "name": "manage_components",
  "arguments": {
    "action": "add",
    "target": "Tree2D",
    "component_type": "SpriteRenderer"
  }
}

// 设置属性 ⚠️ 注意类型格式
{
  "action": "set_property",
  "target": "Tree2D",
  "component_type": "SpriteRenderer",
  "property": "color",
  "value": {"r": 0.1, "g": 0.5, "b": 0.2, "a": 1.0}  // ✅ 对象格式
  // ❌ 错误: [0.1, 0.5, 0.2, 1]
}
```

### Scene 管理

```json
// 创建场景
{
  "name": "manage_scene",
  "arguments": {
    "action": "create",
    "name": "MyScene",
    "path": "MyFolder"
  }
}

// 保存场景
{
  "action": "save"
}

// 获取层级
{
  "action": "get_hierarchy",
  "page_size": 50
}
```

### Asset 管理

```json
// 创建文件夹
{
  "name": "manage_asset",
  "arguments": {
    "action": "create_folder",
    "path": "MyFolder"
  }
}

// 创建纹理
{
  "action": "create",
  "width": 64,
  "height": 64,
  "path": "MyFolder/Texture.png"
}

// 搜索资源
{
  "action": "search",
  "path": "MyFolder",
  "page_size": 50
}
```

## Critical Data Types

### ⚠️ Color 格式

**错误格式（数组）：**
```json
"value": [0.1, 0.5, 0.2, 1.0]
```

**正确格式（对象）：**
```json
"value": {"r": 0.1, "g": 0.5, "b": 0.2, "a": 1.0}
```

**PowerShell 构造：**
```powershell
$color = @{r=0.1; g=0.5; b=0.2; a=1.0} | ConvertTo-Json -Compress
# 结果: {"r":0.1,"g":0.5,"b":0.2,"a":1}
```

### Vector3 格式

```json
"position": [1, 2, 3]
"scale": [1.5, 2, 1]
"rotation": [0, 90, 0]
```

## Common Issues & Solutions

### Issue -1: MCP 插件未安装

**症状：**
- Unity 菜单中没有 **MCP** 或 **Window → MCP**
- Project 中没有 MCP 相关文件夹
- 无法找到 MCP 设置界面

**解决步骤：**
1. **打开 Unity Asset Store:**
   - `Window → Package Manager`
   - 切换到 **Unity Registry** 标签
   - 搜索 **"MCP"** 或 **"MCP for Unity"**

2. **安装插件:**
   - 找到 `MCP for Unity` 包
   - 点击 **Install**
   - 等待安装完成

3. **重启 Unity 编辑器**

4. **验证安装:**
   - 检查菜单栏是否有 `MCP` 或 `Window → MCP`
   - 检查 Project 窗口是否有 `MCP` 文件夹

### Issue 0: uvx 未找到 / 命令不存在

**症状：**
```powershell
The term 'uvx' is not recognized as a cmdlet, function, operable program, or script file.
# 或
无法找到路径 "C:\Users\xxx\.local\bin\uvx.exe" 的一部分
```

**原因：**
- uvx 是 Unity MCP 的依赖工具，尚未安装
- 安装路径因系统/用户而异

**解决步骤：**
1. **在 Unity 中安装:**
   - 菜单: `Window → MCP → Local Setup`
   - 点击: `Install Dependencies` 或 `Setup Local Environment`
   - 等待安装完成（可能需要几分钟）

2. **验证安装:**
   ```powershell
   # Windows
   Get-Command uvx
   # 或
   Test-Path "$env:USERPROFILE\.local\bin\uvx.exe"
   
   # macOS/Linux
   which uvx
   ```

3. **重启终端** 以加载新的 PATH 环境变量

**动态路径检测脚本:**
```powershell
function Get-UvxPath {
    # 尝试常见路径
    $paths = @(
        "$env:USERPROFILE\.local\bin\uvx.exe",
        "$env:LOCALAPPDATA\uv\uvx.exe",
        "C:\Program Files\uv\uvx.exe"
    )
    
    foreach ($path in $paths) {
        if (Test-Path $path) { return $path }
    }
    
    # 尝试从 PATH 查找
    $uvx = Get-Command uvx -ErrorAction SilentlyContinue
    if ($uvx) { return $uvx.Source }
    
    return $null
}

$uvxPath = Get-UvxPath
if (-not $uvxPath) {
    Write-Host "❌ 未找到 uvx。请在 Unity 中点击 Window → MCP → Local Setup 安装。"
    exit 1
}
Write-Host "✅ 找到 uvx: $uvxPath"
```

### Issue 1: 无法设置 SpriteRenderer.sprite

**症状：**
```
Failed to convert value for property 'sprite' to type 'Sprite'
```

**原因：**
- `manage_texture` 创建的是 `Texture2D`，但 `SpriteRenderer` 需要 `Sprite` 类型
- API 不支持直接将路径字符串转为 Sprite 引用

**解决方案：**
1. **手动方式**（推荐）：在 Unity 中将纹理拖到 SpriteRenderer 的 Sprite 字段，Unity 会自动转换
2. **编辑器脚本**：编写 `Editor` 文件夹下的工具脚本批量赋值
3. **预创建 Sprite**：使用 Unity 的 Sprite Editor 将纹理转为 Sprite 资源

### Issue 2: Color 格式错误

**症状：**
```
Error converting token to UnityEngine.Color: Error reading JObject from JsonReader
```

**解决：** 使用对象格式 `{"r":x,"g":y,"b":z,"a":w}` 而非数组 `[x,y,z,w]`

### Issue 3: Session 过期

**症状：**
```
Missing session ID
Bad Request: Missing session ID
```

**解决：** 
- 重新初始化获取新 Session ID
- 确保每个请求都包含 `mcp-session-id` Header

### Issue 4: Unity 实例未找到 / 找不到活跃实例

**症状：**
```json
{
  "instance_count": 0,
  "instances": []
}
```
或
```
Active instance set to ... : false
```

**原因：**
- MCP Server 已启动，但 Unity 编辑器尚未与 Server 建立连接
- Unity 中的 MCP Session 未启动

**解决步骤：**

1. **确保 Unity 编辑器已打开**（且项目已加载）

2. **在 Unity 中启动 MCP Session:**
   - 菜单: `Window → MCP` 或 `MCP → Session`
   - 在 MCP 窗口中找到 **Session** 或 **Connection** 部分
   - 点击 **"Start Session"** 或 **"Connect"** 按钮
   - 等待状态变为 **"Connected"** 或 **"Running"**

3. **检查连接状态:**
   - MCP 窗口应显示: `Status: Connected` 或 `Transport: HTTP`
   - 或显示当前连接的 Server 地址: `http://localhost:8080`

4. **重新获取实例列表:**
   ```json
   {
     "name": "resources/read",
     "params": {
       "uri": "mcpforunity://instances"
     }
   }
   ```

**完整启动流程图:**
```
用户机器
├─ [1] 启动 MCP Server (uvx 命令)
│     └─ 等待连接...
│
└─ [2] 打开 Unity 编辑器
       └─ [3] Window → MCP → Start Session
              └─ 建立连接
                     ↓
              MCP Server 检测到实例
                     ↓
              instance_count: 1
```

**常见问题：**
- **Q: 点击 Start Session 后没有反应？**
  - 检查 MCP Server 是否正在运行（终端窗口是否还在）
  - 检查端口 8080 是否被占用
  - 尝试重启 Unity 和 MCP Server

- **Q: 显示 "Connection Failed"？**
  - 确认 MCP Server 地址配置正确（默认: `http://localhost:8080`）
  - 检查防火墙是否阻止了连接

### Issue 5: 属性参数错误

**症状：**
```
Unexpected keyword argument 'xxx'
```

**解决：** 检查 API 文档，使用正确的参数名：
- ❌ `"component": "SpriteRenderer"` → ✅ `"component_type": "SpriteRenderer"`
- ❌ `"filter": "All"` → ✅ 不支持，省略或使用正确参数

## Workflow Patterns

### Pattern 1: 创建2D物体完整流程

```
1. 创建 GameObject (空物体)
   manage_gameobject: create
   
2. 添加 SpriteRenderer 组件
   manage_components: add, component_type=SpriteRenderer
   
3. 设置颜色
   manage_components: set_property, property=color, value={r,g,b,a}
   
4. 手动赋值 Sprite（API限制）
   或在 Unity 中拖拽纹理到 Sprite 字段
```

### Pattern 2: 批量创建物体

```powershell
$objects = @(
    @{name="Obj1"; pos=@(1,2,0); color=@{r=1;g=0;b=0;a=1}},
    @{name="Obj2"; pos=@(-1,1,0); color=@{r=0;g=1;b=0;a=1}}
)

foreach ($obj in $objects) {
    # 创建物体
    # 添加组件
    # 设置属性
}
```

### Pattern 3: 错误检查流程

```
1. 执行操作
2. 检查控制台日志
   read_console: get
3. 验证结果
   manage_scene: get_hierarchy
4. 如有错误，读取具体组件信息
   resources/read: mcpforunity://scene/gameobject/{id}/components
```

## API Limitations

| 限制 | 说明 | 变通方案 |
|------|------|----------|
| Sprite 赋值 | 无法通过 API 直接设置 Sprite | 手动拖拽或编辑器脚本 |
| 纹理导入设置 | 无法修改 Texture Import Settings | 预配置或在 Unity 中手动设置 |
| 复杂组件 | 部分组件属性不支持 | 使用 Unity 编辑器手动配置 |
| 脚本创建 | 内容需转义 | 使用简单脚本或模板 |

## Best Practices

1. **始终保存场景** 在批量操作后执行 `manage_scene: save`
2. **检查控制台** 定期使用 `read_console` 查看错误
3. **使用 Instance ID** 操作具体物体时使用而非名称
4. **批量操作** 使用循环批量创建，减少 API 调用次数
5. **错误处理** 每个操作后检查 `success` 字段

## Quick Reference

### 常用工具列表

| Tool | Purpose |
|------|---------|
| `manage_gameobject` | CRUD GameObjects |
| `manage_components` | Add/remove/set components |
| `manage_scene` | Scene operations |
| `manage_asset` | Asset operations |
| `manage_texture` | Create textures |
| `read_console` | Get Unity console logs |
| `set_active_instance` | Set target Unity instance |

### HTTP Headers (Required)

```
Content-Type: application/json
Accept: application/json, text/event-stream
mcp-session-id: <session-id>
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{
      "type": "text",
      "text": "{\"success\": true, ...}"
    }]
  }
}
```

## References

- [Unity MCP Server Docs](https://github.com/anthropics/unity-mcp)
- MCP Protocol: https://modelcontextprotocol.io
- Unity Scripting API: https://docs.unity3d.com/ScriptReference/

## Changelog

### v1.0.0 (2026-02-11)
- Initial release
- Documented Color format issue
- Documented Sprite assignment limitation
- Added workflow patterns
