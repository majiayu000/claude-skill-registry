---
name: claude-code-reverse
description: 对用户拥有或明确获授权的本机可执行文件、应用二进制和版本产物做只读静态逆向，包括 Claude Code 及其他 CLI、Mach-O、ELF、PE、Wasm 或打包应用。仅在用户明确要求“逆向、扒实现、查二进制字符串/符号/依赖、验证内部行为、比较两个版本”时使用；不要因普通提及软件而触发，也不要用于执行未知样本、绕过授权/计费、破解或再分发。
---

# Local Binary Reverse

对明确指定的本机目标做证据优先的静态分析。默认只读，不执行目标，也不把“可见字符串”夸大为“已证明运行时行为”。

## 自主边界

- 可直接执行：读取用户指定的单个本机文件；运行 `file`、哈希、`strings`、符号表、依赖表、段表和只读反汇编工具；把分析缓存写入当前用户的私有 cache。
- 先征得同意：运行目标、附加调试器、注入/hook、解包到用户目录、安装分析工具、上传样本、分析未获授权的软件或受保护数据。
- 直接拒绝：绕过许可证、计费或访问控制，提取凭据，制作破解补丁，规避检测，或再分发专有代码/资源。
- 不确定所有权、目标路径或交付问题时先澄清，不要扫描整台机器寻找“可能的目标”。

## 1. 锁定目标与问题

先记录：

1. 精确目标路径或命令名。
2. 用户要验证的具体问题，例如 UI 文案来源、功能开关、网络端点、依赖或版本差异。
3. 对比版本的两个精确文件（如适用）。

不要把进程名、应用名或猜测路径当成已确认目标。不要运行目标来“看看会发生什么”。

## 2. 建立文件身份

使用同目录的 `extract.sh`。它只接受普通文件或可由 `command -v` 解析的命令，缓存按内容 SHA-256 隔离并存放在 `${XDG_CACHE_HOME:-$HOME/.cache}/claude-code-reverse/`。

```bash
SKILL_DIR=/path/to/claude-code-reverse
bash "$SKILL_DIR/extract.sh" info --target /absolute/path/to/target
bash "$SKILL_DIR/extract.sh" dump --target /absolute/path/to/target
bash "$SKILL_DIR/extract.sh" search --target /absolute/path/to/target "literal anchor"
bash "$SKILL_DIR/extract.sh" diff --target-a /path/to/v1 --target-b /path/to/v2 "literal anchor"
```

`info` 必须先给出规范化路径、文件类型、字节数和 SHA-256。若目标在分析期间发生变化，重新执行 `info` 和 `dump`；不要复用旧缓存作结论。

## 3. 按格式选择只读工具

先用 `command -v <tool>` 验证工具存在。缺失时报告缺失项，不要悄悄换成会执行目标的方案。

| 格式 | 首选证据 | 可选深入工具 |
|---|---|---|
| Mach-O | `file`、`otool -L`、`otool -l`、`nm` | `otool -tvV`、已安装的反编译器 |
| ELF | `file`、`readelf -h -l -d -s`、`objdump -x` | `objdump -d`、已安装的反编译器 |
| PE/COFF | `file`、`objdump -x`、ASCII/UTF 字符串 | `objdump -d`、已安装的 PE 工具 |
| Wasm | `file`、`wasm-objdump -x` | `wasm2wat` |
| ZIP/JAR/APK/打包资源 | 先列目录，不落盘解包 | 在用户批准的临时目录中解包后逐件分析 |

不要对不可信目标使用 `ldd`，因为某些实现可能通过加载器执行代码。不要对大文件直接输出完整反汇编、完整字符串或完整符号表；先用字面锚点缩小范围，把原始大输出留在 cache 或单独 artifact 中。

## 常见失败信号

- `strings` 几乎没有输出：目标可能被剥离、压缩、加密或只是启动器；先检查文件类型和段表，不要据此断言“没有实现”。
- 刚 dump 后却提示 cache 不存在：内容哈希已经变化，说明目标文件被更新；重新执行 `info` 和 `dump`，不要复用旧版本结论。
- 同一字符串重复出现：universal/fat binary 可能包含多个架构切片；先按架构检查，不能把重复次数直接解释为调用次数。
- ASCII 搜索无命中：PE 或资源文件可能使用 UTF-16；确认本机 `strings` 实现支持相应编码选项后再查，不要假定跨平台参数一致。

## 4. 从证据到结论

按以下顺序收敛：

1. 用产品文案、端点、配置键、错误消息或符号名做字面锚点。
2. 截取锚点附近上下文，并记录来源文件和 SHA-256。
3. 交叉检查符号、导入依赖、相邻常量或两个版本的差异。
4. 区分结论等级：`已观察`（文件中直接存在）、`强推断`（多项静态证据一致）、`未知`（需要运行时或服务端证据）。

字符串存在不等于代码路径可达，导入存在不等于功能被调用，客户端文案也不能证明服务端策略。

## 5. Claude Code 兼容模式

不提供 `--target` 时，脚本保留原来的 Claude Code 快捷模式：

```bash
bash "$SKILL_DIR/extract.sh" dump
bash "$SKILL_DIR/extract.sh" search "usage limit reached"
bash "$SKILL_DIR/extract.sh" diff 2.1.190 2.1.191 "literal anchor"
```

需要 Claude Code 的安装位置、锚点地图和特有限制时，读取 [references/claude-code.md](references/claude-code.md)。其他目标不要套用 Claude 专用锚点。

## 静态分析边界

静态分析通常无法证明服务端下发内容、运行时生成值、加密后数据、动态加载路径、优化掉的逻辑或混淆变量的真实语义。需要越过这些边界时，明确说明缺少的证据和下一步会产生的副作用，再请求许可。

## 完成标准

- 报告目标规范化路径、文件类型、字节数和 SHA-256。
- 列出本次真实运行的命令和关键输出位置。
- 每项结论附直接证据，并标记 `已观察`、`强推断` 或 `未知`。
- 说明未覆盖的静态分析边界。
- 确认没有执行或修改目标，也没有把样本上传到外部服务。
