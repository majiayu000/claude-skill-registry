---
name: fix-chinese-garbled
description: 智能检测和修复中文乱码内容。支持识别和修复 8 种常见乱码类型（古文码、口字码、符号码、拼音码、问句码、锟拷码、烫烫烫、屯屯屯）。当遇到中文文件显示异常、字符串乱码、需要判断编码问题或修复乱码文本时使用此技能。
---

# 中文乱码修复

## 快速开始

使用修复脚本自动处理乱码：

```bash
# 检测乱码类型
python scripts/detect_garbled.py "锟斤拷锟斤拷要好好学习"

# 修复乱码文本
python scripts/fix_garbled.py "鐢辨湀瑕佸ソ濂藉涔犲ぉ澶╁悜涓?"

# 修复文件
python scripts/fix_garbled.py --file /path/to/garbled.txt --output /path/to/fixed.txt

# 使用编码提示加速修复
python scripts/fix_garbled.py "ç\"Æœè\|å¥½å¥½å-\ä¹" --encoding iso8859-1
```

## 工作流程

### 步骤 1：检测乱码类型

使用 `scripts/detect_garbled.py` 识别乱码类型：

```python
from scripts.detect_garbled import GarbledDetector

detector = GarbledDetector()
result = detector.detect("鐢辨湀瑕佸ソ濂藉涔犲ぉ澶╁悜涓?")
# 返回: {"type": "古文码", "description": "...", "fix_method": "gbk_to_utf8", "confidence": 0.95}
```

### 步骤 2：修复乱码

使用 `scripts/fix_garbled.py` 修复：

```python
from scripts.fix_garbled import GarbledFixer

fixer = GarbledFixer(verbose=True)
fixed_text, method = fixer.fix("鐢辨湀瑕佸ソ濂藉涔犲ぉ澶╁悜涓?")
# 返回: ("由月要好好学习天天向上", "GBK -> UTF-8")
```

### 步骤 3：验证结果

检查修复后的文本是否包含正常的中文字符。脚本会自动计算中文得分，只有得分 > 0.6 才会返回结果。

## 乱码类型速查

| 类型 | 特征 | 修复方法 |
| ------ | ------ | ---------- |
| 古文码 | 不认识的古文字符 | GBK → UTF-8 |
| 口字码 | 大量 `�` 字符 | UTF-8 → GBK |
| 符号码 | 各种符号 `ç"`®¯` | ISO8859-1 → UTF-8 |
| 拼音码 | 带声调符号的字母 `óéàü` | ISO8859-1 → GBK |
| 问句码 | 奇数长度以 `?` 结尾 | GBK → UTF-8 → GBK |
| 锟拷码 | 大量 `锟斤拷` | UTF-8 → GBK → UTF-8 |
| 烫烫烫/屯屯屯 | 重复的 `烫` 或 `屯` | 需修复源码 |

详细说明请参考 [references/garbled_types.md](references/garbled_types.md)

## 常见场景

### 场景 1：修复整个文件

```bash
# 当文件打开时显示乱码
python scripts/fix_garbled.py --file garbled.txt --output fixed.txt
```

### 场景 2：修复字符串

```bash
# 当日志或输出中有乱码字符串
python scripts/fix_garbled.py "锟斤拷锟斤拷要锟矫猴拷学习锟斤拷"
```

### 场景 3：仅检测不修复

```bash
# 判断乱码类型但不修改
python scripts/detect_garbled.py "烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫"
```

## 注意事项

1. **烫烫烫 / 屯屯屯**：这是内存未初始化问题，无法通过编码转换修复，需要检查源码
2. **低置信度**：如果修复得分 < 0.6，脚本会返回结果但标记为"低置信度"，可能需要手动验证
3. **编码提示**：如果知道原始编码类型，使用 `--encoding` 参数可以提高修复成功率

## 资源

### scripts/

- `detect_garbled.py` - 乱码类型检测器，返回乱码类型、描述、修复方法和置信度
- `fix_garbled.py` - 智能乱码修复器，自动尝试多种编码组合

### references/

- `garbled_types.md` - Unicode 中文乱码速查表，包含各类型乱码的特征、产生原因和修复建议
