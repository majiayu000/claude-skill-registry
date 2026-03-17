---
name: pptx
description: "演示文稿创建、编辑和分析。当 Claude 需要处理演示文稿（.pptx 文件）时使用，包括：(1) 创建新演示文稿，(2) 修改或编辑内容，(3) 处理版式，(4) 添加批注或演讲者备注，或其他任何演示文稿任务"
license: 专有。LICENSE.txt 包含完整条款
---

# PPTX 创建、编辑和分析

## 概述

用户可能会要求您创建、编辑或分析 .pptx 文件的内容。.pptx 文件本质上是一个包含 XML 文件和其他资源的 ZIP 压缩包，您可以读取或编辑。不同的任务有不同的工具和工作流程可用。

## 读取和分析内容

### 文本提取
如果您只需要读取演示文稿的文本内容，应将文档转换为 markdown：

```bash
# 将文档转换为 markdown
python -m markitdown path-to-file.pptx
```

### 原始 XML 访问
您需要原始 XML 访问来处理：批注、演讲者备注、幻灯片版式、动画、设计元素和复杂格式。对于这些功能，您需要解压演示文稿并读取其原始 XML 内容。

#### 解压文件
`python ooxml/scripts/unpack.py <office_file> <output_dir>`

**注意**：unpack.py 脚本位于相对于项目根目录的 `skills/pptx/ooxml/scripts/unpack.py`。如果脚本不在此路径，请使用 `find . -name "unpack.py"` 来定位它。

#### 关键文件结构
* `ppt/presentation.xml` - 主演示文稿元数据和幻灯片引用
* `ppt/slides/slide{N}.xml` - 单个幻灯片内容（slide1.xml、slide2.xml 等）
* `ppt/notesSlides/notesSlide{N}.xml` - 每个幻灯片的演讲者备注
* `ppt/comments/modernComment_*.xml` - 特定幻灯片的批注
* `ppt/slideLayouts/` - 幻灯片版式模板
* `ppt/slideMasters/` - 母版幻灯片模板
* `ppt/theme/` - 主题和样式信息
* `ppt/media/` - 图片和其他媒体文件

#### 排版和颜色提取
**当提供了要模仿的示例设计时**：始终先使用以下方法分析演示文稿的排版和颜色：
1. **读取主题文件**：检查 `ppt/theme/theme1.xml` 中的颜色（`<a:clrScheme>`）和字体（`<a:fontScheme>`）
2. **采样幻灯片内容**：检查 `ppt/slides/slide1.xml` 中的实际字体使用（`<a:rPr>`）和颜色
3. **搜索模式**：使用 grep 在所有 XML 文件中查找颜色（`<a:solidFill>`、`<a:srgbClr>`）和字体引用

## 创建新 PowerPoint 演示文稿 **不使用模板**

从头开始创建新 PowerPoint 演示文稿时，使用 **html2pptx** 工作流程将 HTML 幻灯片转换为具有精确定位的 PowerPoint。

### 设计原则

**关键**：在创建任何演示文稿之前，分析内容并选择适当的设计元素：
1. **考虑主题**：这个演示文稿是关于什么的？它暗示什么语气、行业或情绪？
2. **检查品牌**：如果用户提到公司/组织，考虑其品牌颜色和形象
3. **将调色板与内容匹配**：选择反映主题的颜色
4. **说明您的方法**：在编写代码之前解释您的设计选择

**要求**：
- ✅ 在编写代码之前说明您基于内容的设计方法
- ✅ 仅使用网页安全字体：Arial、Helvetica、Times New Roman、Georgia、Courier New、Verdana、Tahoma、Trebuchet MS、Impact
- ✅ 通过大小、粗细和颜色创建清晰的视觉层次
- ✅ 确保可读性：强烈对比、适当大小的文本、整洁的对齐
- ✅ 保持一致性：在幻灯片之间重复模式、间距和视觉语言

#### 调色板选择

**创造性地选择颜色**：
- **跳出默认思维**：什么颜色真正匹配这个特定主题？避免自动选择。
- **考虑多个角度**：主题、行业、情绪、能量水平、目标受众、品牌形象（如有提及）
- **大胆尝试**：尝试意想不到的组合 - 医疗保健演示文稿不必是绿色的，金融不必是海军蓝
- **构建调色板**：选择 3-5 种配合良好的颜色（主色 + 辅助色 + 强调色）
- **确保对比**：文本必须在背景上清晰可读

**示例调色板**（用于激发创意 - 选择一个、调整它或创建自己的）：

1. **经典蓝**：深海军蓝（#1C2833）、石板灰（#2E4053）、银色（#AAB7B8）、米白（#F4F6F6）
2. **青绿与珊瑚**：青绿（#5EA8A7）、深青绿（#277884）、珊瑚（#FE4447）、白色（#FFFFFF）
3. **大胆红色**：红色（#C0392B）、亮红（#E74C3C）、橙色（#F39C12）、黄色（#F1C40F）、绿色（#2ECC71）
4. **暖腮红**：灰褐色（#A49393）、腮红（#EED6D3）、玫瑰（#E8B4B8）、奶油（#FAF7F2）
5. **酒红奢华**：酒红（#5D1D2E）、深红（#951233）、铁锈（#C15937）、金色（#997929）
6. **深紫与翡翠**：紫色（#B165FB）、深蓝（#181B24）、翡翠（#40695B）、白色（#FFFFFF）
7. **奶油与森林绿**：奶油（#FFE1C7）、森林绿（#40695B）、白色（#FCFCFC）
8. **粉色与紫色**：粉色（#F8275B）、珊瑚（#FF574A）、玫瑰（#FF737D）、紫色（#3D2F68）
9. **青柠与梅色**：青柠（#C5DE82）、梅色（#7C3A5F）、珊瑚（#FD8C6E）、蓝灰（#98ACB5）
10. **黑与金**：金色（#BF9A4A）、黑色（#000000）、奶油（#F4F6F6）
11. **鼠尾草与赤陶**：鼠尾草（#87A96B）、赤陶（#E07A5F）、奶油（#F4F1DE）、炭灰（#2C2C2C）
12. **炭灰与红**：炭灰（#292929）、红色（#E33737）、浅灰（#CCCBCB）
13. **活力橙**：橙色（#F96D00）、浅灰（#F2F2F2）、炭灰（#222831）
14. **森林绿**：黑色（#191A19）、绿色（#4E9F3D）、深绿（#1E5128）、白色（#FFFFFF）
15. **复古彩虹**：紫色（#722880）、粉色（#D72D51）、橙色（#EB5C18）、琥珀（#F08800）、金色（#DEB600）
16. **复古大地**：芥末（#E3B448）、鼠尾草（#CBD18F）、森林绿（#3A6B35）、奶油（#F4F1DE）
17. **海岸玫瑰**：老玫瑰（#AD7670）、海狸（#B49886）、蛋壳（#F3ECDC）、灰绿（#BFD5BE）
18. **橙与青绿**：浅橙（#FC993E）、灰青绿（#667C6F）、白色（#FCFCFC）

#### 视觉细节选项

**几何图案**：
- 对角线分隔代替水平分隔
- 不对称列宽（30/70、40/60、25/75）
- 90° 或 270° 旋转的文本标题
- 图片的圆形/六边形框架
- 角落的三角形装饰形状
- 重叠形状增加深度

**边框和框架处理**：
- 仅一侧的粗单色边框（10-20pt）
- 对比色的双线边框
- 角括号代替完整框架
- L 形边框（上+左或下+右）
- 标题下方的下划线强调（3-5pt 粗）

**排版处理**：
- 极端大小对比（72pt 标题 vs 11pt 正文）
- 大写标题配宽字母间距
- 超大显示字体的编号章节
- 等宽字体（Courier New）用于数据/统计/技术内容
- 窄体字体（Arial Narrow）用于密集信息
- 轮廓文本强调

**图表和数据样式**：
- 单色图表配单一强调色用于关键数据
- 水平条形图代替垂直条形图
- 点图代替条形图
- 最少或无网格线
- 数据标签直接在元素上（无图例）
- 关键指标的超大数字

**布局创新**：
- 带文本叠加的满版图片
- 侧边栏列（20-30% 宽度）用于导航/上下文
- 模块化网格系统（3×3、4×4 块）
- Z 形或 F 形内容流
- 浮动文本框覆盖在彩色形状上
- 杂志风格多栏布局

**背景处理**：
- 占幻灯片 40-60% 的纯色块
- 渐变填充（仅垂直或对角线）
- 分割背景（两种颜色，对角线或垂直）
- 边到边的色带
- 负空间作为设计元素

### 布局提示
**创建带图表或表格的幻灯片时**：
- **两栏布局（推荐）**：使用跨越全宽的标题，然后下方两栏 - 一栏放文本/要点，另一栏放主要内容。这提供更好的平衡，使图表/表格更易读。使用不等列宽的 flexbox（例如 40%/60% 分割）来优化每种内容类型的空间。
- **全幻灯片布局**：让主要内容（图表/表格）占据整个幻灯片以获得最大影响力和可读性
- **切勿垂直堆叠**：不要将图表/表格放在单列中的文本下方 - 这会导致可读性差和布局问题

### 工作流程
1. **必须 - 完整阅读整个文件**：完整阅读 [`html2pptx.md`](html2pptx.md)，从头到尾。**阅读此文件时切勿设置任何范围限制。** 在开始创建演示文稿之前，阅读完整文件内容以了解详细语法、关键格式规则和最佳实践。
2. 为每个幻灯片创建具有正确尺寸的 HTML 文件（例如 16:9 为 720pt × 405pt）
   - 使用 `<p>`、`<h1>`-`<h6>`、`<ul>`、`<ol>` 处理所有文本内容
   - 对将添加图表/表格的区域使用 `class="placeholder"`（渲染灰色背景以便可见）
   - **关键**：首先使用 Sharp 将渐变和图标光栅化为 PNG 图片，然后在 HTML 中引用
   - **布局**：对于带图表/表格/图片的幻灯片，使用全幻灯片布局或两栏布局以获得更好的可读性
3. 创建并运行使用 [`html2pptx.js`](scripts/html2pptx.js) 库的 JavaScript 文件，将 HTML 幻灯片转换为 PowerPoint 并保存演示文稿
   - 使用 `html2pptx()` 函数处理每个 HTML 文件
   - 使用 PptxGenJS API 将图表和表格添加到占位符区域
   - 使用 `pptx.writeFile()` 保存演示文稿
4. **视觉验证**：生成缩略图并检查布局问题
   - 创建缩略图网格：`python scripts/thumbnail.py output.pptx workspace/thumbnails --cols 4`
   - 阅读并仔细检查缩略图图片：
     - **文本截断**：文本被标题栏、形状或幻灯片边缘截断
     - **文本重叠**：文本与其他文本或形状重叠
     - **定位问题**：内容太靠近幻灯片边界或其他元素
     - **对比问题**：文本和背景之间对比不足
   - 如果发现问题，调整 HTML 边距/间距/颜色并重新生成演示文稿
   - 重复直到所有幻灯片视觉正确

## 编辑现有 PowerPoint 演示文稿

编辑现有 PowerPoint 演示文稿中的幻灯片时，您需要使用原始 Office Open XML（OOXML）格式。这涉及解压 .pptx 文件、编辑 XML 内容，然后重新打包。

### 工作流程
1. **必须 - 完整阅读整个文件**：完整阅读 [`ooxml.md`](ooxml.md)（约 500 行），从头到尾。**阅读此文件时切勿设置任何范围限制。** 在编辑任何演示文稿之前，阅读完整文件内容以获取有关 OOXML 结构和编辑工作流程的详细指导。
2. 解压演示文稿：`python ooxml/scripts/unpack.py <office_file> <output_dir>`
3. 编辑 XML 文件（主要是 `ppt/slides/slide{N}.xml` 和相关文件）
4. **关键**：每次编辑后立即验证，并在继续之前修复任何验证错误：`python ooxml/scripts/validate.py <dir> --original <file>`
5. 打包最终演示文稿：`python ooxml/scripts/pack.py <input_directory> <office_file>`

## 使用模板创建新 PowerPoint 演示文稿

当您需要创建遵循现有模板设计的演示文稿时，您需要复制和重新排列模板幻灯片，然后替换占位符内容。

### 工作流程
1. **提取模板文本并创建可视化缩略图网格**：
   * 提取文本：`python -m markitdown template.pptx > template-content.md`
   * 阅读 `template-content.md`：阅读整个文件以了解模板演示文稿的内容。**阅读此文件时切勿设置任何范围限制。**
   * 创建缩略图网格：`python scripts/thumbnail.py template.pptx`
   * 有关更多详细信息，请参阅[创建缩略图网格](#创建缩略图网格)部分

2. **分析模板并将清单保存到文件**：
   * **视觉分析**：查看缩略图网格以了解幻灯片版式、设计模式和视觉结构
   * 创建并保存模板清单文件到 `template-inventory.md`，包含：
     ```markdown
     # 模板清单分析
     **总幻灯片数：[count]**
     **重要：幻灯片从 0 开始索引（第一张幻灯片 = 0，最后一张幻灯片 = count-1）**

     ## [类别名称]
     - 幻灯片 0：[版式代码（如有）] - 描述/用途
     - 幻灯片 1：[版式代码] - 描述/用途
     - 幻灯片 2：[版式代码] - 描述/用途
     [... 每个幻灯片都必须单独列出其索引 ...]
     ```
   * **使用缩略图网格**：参考可视化缩略图来识别：
     - 版式模式（标题幻灯片、内容版式、章节分隔）
     - 图片占位符位置和数量
     - 幻灯片组之间的设计一致性
     - 视觉层次和结构
   * 此清单文件是下一步选择适当模板所必需的

3. **根据模板清单创建演示文稿大纲**：
   * 查看步骤 2 中的可用模板。
   * 为第一张幻灯片选择介绍或标题模板。这应该是最前面的模板之一。
   * 为其他幻灯片选择安全的、基于文本的版式。
   * **关键：将版式结构与实际内容匹配**：
     - 单列版式：用于统一叙述或单一主题
     - 两列版式：仅当您有正好 2 个不同的项目/概念时使用
     - 三列版式：仅当您有正好 3 个不同的项目/概念时使用
     - 图片+文本版式：仅当您有实际图片要插入时使用
     - 引用版式：仅用于实际的人物引用（带归属），切勿用于强调
     - 切勿使用占位符比内容多的版式
     - 如果您有 2 个项目，不要强行放入 3 列版式
     - 如果您有 4+ 个项目，考虑分成多张幻灯片或使用列表格式
   * 在选择版式之前计算您的实际内容数量
   * 验证所选版式中的每个占位符都将填充有意义的内容
   * 为每个内容部分选择一个代表**最佳**版式的选项。
   * 保存 `outline.md`，包含内容和利用可用设计的模板映射
   * 示例模板映射：
      ```
      # 要使用的模板幻灯片（0 基索引）
      # 警告：验证索引在范围内！有 73 张幻灯片的模板索引为 0-72
      # 映射：大纲中的幻灯片编号 -> 模板幻灯片索引
      template_mapping = [
          0,   # 使用幻灯片 0（标题/封面）
          34,  # 使用幻灯片 34（B1：标题和正文）
          34,  # 再次使用幻灯片 34（复制用于第二个 B1）
          50,  # 使用幻灯片 50（E1：引用）
          54,  # 使用幻灯片 54（F2：结束语+文本）
      ]
      ```

4. **使用 `rearrange.py` 复制、重新排序和删除幻灯片**：
   * 使用 `scripts/rearrange.py` 脚本创建具有所需顺序幻灯片的新演示文稿：
     ```bash
     python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
     ```
   * 该脚本自动处理重复幻灯片的复制、删除未使用的幻灯片和重新排序
   * 幻灯片索引从 0 开始（第一张幻灯片是 0，第二张是 1，等等）
   * 同一幻灯片索引可以出现多次以复制该幻灯片

5. **使用 `inventory.py` 脚本提取所有文本**：
   * **运行清单提取**：
     ```bash
     python scripts/inventory.py working.pptx text-inventory.json
     ```
   * **阅读 text-inventory.json**：阅读整个 text-inventory.json 文件以了解所有形状及其属性。**阅读此文件时切勿设置任何范围限制。**

   * 清单 JSON 结构：
      ```json
        {
          "slide-0": {
            "shape-0": {
              "placeholder_type": "TITLE",  // 或非占位符为 null
              "left": 1.5,                  // 位置（英寸）
              "top": 2.0,
              "width": 7.5,
              "height": 1.2,
              "paragraphs": [
                {
                  "text": "段落文本",
                  // 可选属性（仅在非默认时包含）：
                  "bullet": true,           // 检测到显式项目符号
                  "level": 0,               // 仅在 bullet 为 true 时包含
                  "alignment": "CENTER",    // CENTER、RIGHT（非 LEFT）
                  "space_before": 10.0,     // 段前间距（磅）
                  "space_after": 6.0,       // 段后间距（磅）
                  "line_spacing": 22.4,     // 行间距（磅）
                  "font_name": "Arial",     // 来自第一个运行
                  "font_size": 14.0,        // 磅
                  "bold": true,
                  "italic": false,
                  "underline": false,
                  "color": "FF0000"         // RGB 颜色
                }
              ]
            }
          }
        }
      ```

   * 关键特性：
     - **幻灯片**：命名为"slide-0"、"slide-1"等。
     - **形状**：按视觉位置（从上到下、从左到右）排序为"shape-0"、"shape-1"等。
     - **占位符类型**：TITLE、CENTER_TITLE、SUBTITLE、BODY、OBJECT 或 null
     - **默认字体大小**：从版式占位符提取的 `default_font_size`（磅，如可用）
     - **幻灯片编号被过滤**：具有 SLIDE_NUMBER 占位符类型的形状自动从清单中排除
     - **项目符号**：当 `bullet: true` 时，`level` 始终包含（即使是 0）
     - **间距**：`space_before`、`space_after` 和 `line_spacing`（磅，仅在设置时包含）
     - **颜色**：RGB 的 `color`（例如"FF0000"），主题颜色的 `theme_color`（例如"DARK_1"）
     - **属性**：输出中仅包含非默认值

6. **生成替换文本并将数据保存到 JSON 文件**
   根据上一步的文本清单：
   - **关键**：首先验证清单中存在哪些形状 - 只引用实际存在的形状
   - **验证**：replace.py 脚本将验证替换 JSON 中的所有形状都存在于清单中
     - 如果引用不存在的形状，您将收到显示可用形状的错误
     - 如果引用不存在的幻灯片，您将收到指示该幻灯片不存在的错误
     - 所有验证错误在脚本退出前一次性显示
   - **重要**：replace.py 脚本内部使用 inventory.py 来识别所有文本形状
   - **自动清除**：清单中的所有文本形状都将被清除，除非您为它们提供"paragraphs"
   - 为需要内容的形状添加"paragraphs"字段（不是"replacement_paragraphs"）
   - 替换 JSON 中没有"paragraphs"的形状将自动清除其文本
   - 带项目符号的段落将自动左对齐。当 `"bullet": true` 时不要设置 `alignment` 属性
   - 为占位符文本生成适当的替换内容
   - 使用形状大小来确定适当的内容长度
   - **关键**：包含原始清单中的段落属性 - 不要只提供文本
   - **重要**：当 bullet: true 时，不要在文本中包含项目符号符号（•、-、*）- 它们会自动添加
   - **基本格式规则**：
     - 标题通常应有 `"bold": true`
     - 列表项应有 `"bullet": true, "level": 0`（bullet 为 true 时需要 level）
     - 保留任何对齐属性（例如居中文本的 `"alignment": "CENTER"`）
     - 与默认不同时包含字体属性（例如 `"font_size": 14.0`、`"font_name": "Lora"`）
     - 颜色：RGB 使用 `"color": "FF0000"`，主题颜色使用 `"theme_color": "DARK_1"`
     - 替换脚本期望**正确格式的段落**，而不仅仅是文本字符串
     - **重叠形状**：优先选择 default_font_size 更大或 placeholder_type 更合适的形状
   - 将带有替换的更新清单保存到 `replacement-text.json`
   - **警告**：不同的模板版式有不同的形状数量 - 在创建替换之前始终检查实际清单

   显示正确格式的示例 paragraphs 字段：
   ```json
   "paragraphs": [
     {
       "text": "新演示文稿标题文本",
       "alignment": "CENTER",
       "bold": true
     },
     {
       "text": "章节标题",
       "bold": true
     },
     {
       "text": "第一个要点，不带项目符号符号",
       "bullet": true,
       "level": 0
     },
     {
       "text": "红色文本",
       "color": "FF0000"
     },
     {
       "text": "主题颜色文本",
       "theme_color": "DARK_1"
     },
     {
       "text": "没有特殊格式的普通段落文本"
     }
   ]
   ```

   **替换 JSON 中未列出的形状将自动清除**：
   ```json
   {
     "slide-0": {
       "shape-0": {
         "paragraphs": [...] // 此形状获得新文本
       }
       // 清单中的 shape-1 和 shape-2 将自动清除
     }
   }
   ```

   **演示文稿的常见格式模式**：
   - 标题幻灯片：粗体文本，有时居中
   - 幻灯片内的章节标题：粗体文本
   - 项目符号列表：每个项目需要 `"bullet": true, "level": 0`
   - 正文文本：通常不需要特殊属性
   - 引用：可能有特殊的对齐或字体属性

7. **使用 `replace.py` 脚本应用替换**
   ```bash
   python scripts/replace.py working.pptx replacement-text.json output.pptx
   ```

   该脚本将：
   - 首先使用 inventory.py 的函数提取所有文本形状的清单
   - 验证替换 JSON 中的所有形状都存在于清单中
   - 清除清单中识别的所有形状的文本
   - 仅对替换 JSON 中定义了"paragraphs"的形状应用新文本
   - 通过应用 JSON 中的段落属性来保留格式
   - 自动处理项目符号、对齐、字体属性和颜色
   - 保存更新后的演示文稿

   示例验证错误：
   ```
   错误：替换 JSON 中的无效形状：
     - 'slide-0' 上未找到形状 'shape-99'。可用形状：shape-0、shape-1、shape-4
     - 清单中未找到幻灯片 'slide-999'
   ```

   ```
   错误：替换文本使以下形状的溢出更严重：
     - slide-0/shape-2：溢出加剧 1.25"（原为 0.00"，现为 1.25"）
   ```

## 创建缩略图网格

要创建 PowerPoint 幻灯片的可视化缩略图网格以便快速分析和参考：

```bash
python scripts/thumbnail.py template.pptx [output_prefix]
```

**功能**：
- 创建：`thumbnails.jpg`（或大型演示文稿为 `thumbnails-1.jpg`、`thumbnails-2.jpg` 等）
- 默认：5 列，每个网格最多 30 张幻灯片（5×6）
- 自定义前缀：`python scripts/thumbnail.py template.pptx my-grid`
  - 注意：如果您想要输出到特定目录，输出前缀应包含路径（例如 `workspace/my-grid`）
- 调整列数：`--cols 4`（范围：3-6，影响每个网格的幻灯片数）
- 网格限制：3 列 = 12 张幻灯片/网格，4 列 = 20，5 列 = 30，6 列 = 42
- 幻灯片从零开始索引（幻灯片 0、幻灯片 1 等）

**用例**：
- 模板分析：快速了解幻灯片版式和设计模式
- 内容审查：整个演示文稿的视觉概览
- 导航参考：通过外观找到特定幻灯片
- 质量检查：验证所有幻灯片格式正确

**示例**：
```bash
# 基本用法
python scripts/thumbnail.py presentation.pptx

# 组合选项：自定义名称、列数
python scripts/thumbnail.py template.pptx analysis --cols 4
```

## 将幻灯片转换为图片

要可视化分析 PowerPoint 幻灯片，使用两步过程将其转换为图片：

1. **将 PPTX 转换为 PDF**：
   ```bash
   soffice --headless --convert-to pdf template.pptx
   ```

2. **将 PDF 页面转换为 JPEG 图片**：
   ```bash
   pdftoppm -jpeg -r 150 template.pdf slide
   ```
   这会创建 `slide-1.jpg`、`slide-2.jpg` 等文件。

选项：
- `-r 150`：设置分辨率为 150 DPI（调整以平衡质量/大小）
- `-jpeg`：输出 JPEG 格式（如需要可使用 `-png` 输出 PNG）
- `-f N`：要转换的第一页（例如 `-f 2` 从第 2 页开始）
- `-l N`：要转换的最后一页（例如 `-l 5` 在第 5 页停止）
- `slide`：输出文件的前缀

特定范围示例：
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 template.pdf slide  # 仅转换第 2-5 页
```

## 代码风格指南
**重要**：生成 PPTX 操作代码时：
- 编写简洁的代码
- 避免冗长的变量名和冗余操作
- 避免不必要的 print 语句

## 依赖项

必需的依赖项（应该已经安装）：

- **markitdown**：`pip install "markitdown[pptx]"`（用于从演示文稿提取文本）
- **pptxgenjs**：`npm install -g pptxgenjs`（用于通过 html2pptx 创建演示文稿）
- **playwright**：`npm install -g playwright`（用于 html2pptx 中的 HTML 渲染）
- **react-icons**：`npm install -g react-icons react react-dom`（用于图标）
- **sharp**：`npm install -g sharp`（用于 SVG 光栅化和图片处理）
- **LibreOffice**：`sudo apt-get install libreoffice`（用于 PDF 转换）
- **Poppler**：`sudo apt-get install poppler-utils`（用于 pdftoppm 将 PDF 转换为图片）
- **defusedxml**：`pip install defusedxml`（用于安全的 XML 解析）
