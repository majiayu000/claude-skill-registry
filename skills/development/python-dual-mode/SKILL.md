---
name: python-dual-mode
description: 将既有或新编写的 Python 脚本重构为双模式模块，用于稳定、可维护的数据处理流。
---
# 指令

## 触发条件（When to use）

* 仅在**编写或改写 Python 代码为数据处理流**时使用。
* 输入包含：现有脚本、需求描述，或需要从零生成脚本，但明确要求**双模式模块化**。

## 能力范围（Must / Must Not）

* **必须**生成一个可被 `import` 调用且可通过 CLI 运行的 Python 模块。
* **必须**提供一个 `run()`（或语义等价命名）函数，参数**覆盖原脚本全部输入**。
* **必须**使用 `argparse` 解析命令行参数，并在 `main()` 中调用 `run()`。
* **必须**保留 `if __name__ == "__main__":`，且仅在其中调用 `main()`。
* **必须**将硬编码路径与环境依赖参数化，不得写死路径。
* **不得**在 `run()` 中读取全局变量、环境变量或命令行状态。
* **不得**在 import 时触发主流程执行。
* **不得**假设未声明的外部资源、权限或运行环境。

## 结构与实现要求

* **模块结构**：

  * `run(...)`：纯函数式主流程，显式参数输入，返回结构化结果或状态码。
  * `build_parser()`（可选）：集中定义 CLI 参数，避免散落。
  * `main(argv=None)`：解析参数并调用 `run()`；`argv` 可注入以便测试。
* **错误处理**：

  * 预期错误（参数缺失、文件不存在、格式错误）**必须**抛出可读异常或返回非 0 状态码。
  * 不确定性（外部 I/O、第三方库行为）**必须**有失败策略（重试/降级/明确失败）。
* **日志**：

  * **应当**使用 `logging`，不得使用 `print` 作为主要日志。
* **可测试性**：

  * `run()` **应当**可被单元测试直接调用。

## 失败策略与不确定性处理

* 参数校验失败：立即失败，给出最小可行动错误信息。
* I/O 失败：明确失败原因；如允许重试，需显式声明次数与退避策略。
* 第三方依赖异常：捕获并封装为领域错误，避免泄露内部栈信息（调试模式除外）。

## 安全与合规

* **不得**执行越权操作（如未声明的网络访问、系统修改）。
* **不得**隐式调用外部命令或下载资源，除非明确声明并获得输入授权。

## 输出物

* 生成的 Python 文件必须：

  * 可被 `import` 使用；
  * 可通过 `python module.py --args` 运行；
  * 文档化参数与示例用法。

## 示例骨架（非实现，仅结构）

```python
import argparse
import logging

log = logging.getLogger(__name__)

def run(input_path: str, output_path: str, **kwargs):
    """Pure entry point."""
    # ...
    return 0


def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--input-path", required=True)
    p.add_argument("--output-path", required=True)
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return run(**vars(args))


if __name__ == "__main__":
    raise SystemExit(main())
```
