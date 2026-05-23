---
name: process-faq
description: Process and transform FAQ documents (xlsx, word, pdf, txt) into RAG-optimized format. Use when working with FAQ files, knowledge base documents, or when the user needs to analyze and restructure FAQ content for RAG systems.
tools: Read, Write, Bash, AskUserQuestion
---

# Process FAQ - FAQ Knowledge Base Processor

Transform raw FAQ documents into RAG-optimized structured format with intelligent content expansion and analysis.

## What This Skill Does

This skill helps you:

1. **Convert** FAQ documents to readable Markdown format (script)
2. **Analyze** FAQ content and identify expansion opportunities (Claude)
3. **Expand** content: split complex questions, rewrite answers (Claude)
4. **Standardize** format and generate keywords automatically (script)

## Supported Input Formats

- Excel (.xlsx)
- Word (.docx)
- PDF (.pdf)
- Text (.txt)

## Workflow Overview (3-Step Process)

```
Step 1: Convert → Markdown (script)
Step 2: Expand → Enhanced FAQ (Claude - THIS IS THE KEY STEP!)
Step 3: Standardize → Final RAG format (script)
```

## New Workflow (Claude + Script Collaboration)

### Step 1: Convert to Markdown (Script)

First, convert the input file to Markdown so Claude can read and analyze it:

```bash
python process-faq/scripts/convert_to_markdown.py <input_file>
```

This creates a `*_for_analysis.md` file with structured FAQ content.

**Why Markdown?**

- Claude can directly read and understand the content
- Better for analyzing content quality vs just checking format
- Allows for nuanced, intelligent analysis

### Step 2: Claude Analyzes and Expands Content (CRITICAL!)

**This is the most important step where YOU (Claude) create value!**

Read the Markdown file and perform **deep content analysis and expansion**:

#### Phase A: Content Quality Analysis (质量检查)

**IMPORTANT: Do this BEFORE expanding content!**

Identify and document issues:

1. **Logical Issues (逻辑问题)**

   - **Contradictions**: Do different answers give conflicting information?
     - Example: Q1 says "支持退货" but Q2 says "不支持退货"
   - **Inconsistencies**: Do similar questions have different answers?
     - Example: "配送时间 3 天" vs "配送时间 5-7 天"
   - **Outdated Information**: References to old products, prices, or policies?

2. **Duplicate/Redundant Content (重复内容)**

   - **Exact Duplicates**: Same question appears multiple times
   - **Semantic Duplicates**: "如何登录?" vs "怎么登录?" (same meaning)
   - **Overlapping Answers**: Multiple questions share 80%+ identical content

3. **Missing or Incomplete Information (缺失信息)**

   - **Incomplete Answers**: Too brief, missing key steps or details
   - **Missing Context**: Assumes knowledge users may not have
   - **Broken Logic**: Answer doesn't actually address the question

4. **Clarity Issues (表达问题)**
   - **Unclear Questions**: Too vague ("支持什么?")
   - **Ambiguous Terms**: Undefined jargon or acronyms
   - **Poor Structure**: Wall of text without formatting

**Action Required**: Document all issues found and decide:

- ✅ **Fix**: Resolve contradictions, merge duplicates, clarify ambiguities
- ⚠️ **Flag**: Note issues that need user clarification
- ❌ **Remove**: Delete truly useless or incorrect content

#### Phase B: Content Expansion Strategy

**Goal**: Transform a small FAQ into a comprehensive, high-quality knowledge base

**CRITICAL: Expansion must happen AFTER quality analysis!**

**Key expansion techniques:**

1. **Resolve Issues First** (基于 Phase A 的发现)

   - **Fix Contradictions**: Choose the correct information, note uncertainty for user
   - **Merge Duplicates**: Combine semantically identical questions into one best version
   - **Complete Incomplete**: Fill in missing steps, add context
   - **Clarify Ambiguities**: Reword vague questions to be specific

2. **Split Complex Questions**

   - If one question like "如何使用产品?" contains multiple sub-topics
   - Break it into specific questions: "如何安装?", "如何配置?", "如何维护?"

3. **Extract Knowledge Points from Long Answers**

   - If one answer is 500+ characters and covers multiple topics
   - Identify each distinct knowledge point
   - Create a dedicated Q&A for each point
   - **BUT**: Ensure each extracted point is accurate and consistent

4. **Identify Missing Common Questions**

   - Based on the domain, what would users naturally ask?
   - Add questions that should exist but don't
   - Consider user journey: pre-purchase → purchase → usage → troubleshooting

5. **Rewrite Answers for Clarity**
   - Make each answer concise and focused
   - Remove sales language if not appropriate
   - Add structure (numbered lists, bullet points)
   - **Ensure consistency** with other related answers

**Example: Quality Analysis + Expansion**

**Original (with issues):**

```
Q1: 你们是怎么调理睡眠的?
A1: [500字，包含：产品介绍、使用流程、手环说明、"手环180元"、售后政策等]

Q2: 先用后付是什么意思?
A2: [与Q1相同的500字回答]

Q3: 华为手环多少钱？
A3: 手环200元左右
```

**Phase A Analysis - Issues Found:**

- ❌ **Contradiction**: Q1 说"手环 180 元"，Q3 说"手环 200 元左右"
- ❌ **Duplicate**: Q1 和 Q2 的回答完全相同
- ⚠️ **Overlapping**: 三个问题都提到手环，信息散乱

**Phase B Expansion - After Fixes:**

```
Q1: 你们是怎么调理睡眠的？
A1: 我们通过太赫兹能量睡垫来调理睡眠，能帮助疏通经络、改善气血循环...
[简洁，只讲核心调理原理，不再包含价格等无关信息]

Q2: 先用后付是什么意思？
A2: 先用后付就是您可以先把产品拿回家免费体验，有效果再付款...
[独立回答，不再重复Q1的内容]

Q3: 华为手环多少钱？
A3: 华为手环180元左右（已统一价格，解决矛盾）

Q4: 为什么要用华为手环测睡眠？
A4: 手环能精准测出入睡时间、深睡时长等数据...
[新增问题，补充手环相关信息]

Q5: 手环怎么使用？
A5: 充电后戴在手腕上，连接手机APP即可...
[新增问题，完善手环知识点]
```

**Summary:**

- Fixed 1 contradiction (价格统一)
- Merged 1 duplicate (Q1 和 Q2)
- Expanded 3 → 5 FAQs (提取知识点)
- Each answer is now focused and consistent

#### Phase C: Categorization

Design a clear category structure:

- Group related questions together
- Use domain-appropriate category names
- Aim for 5-10 main categories

### Step 3: User Consultation (Optional)

Use the `AskUserQuestion` tool if you need clarification on:

- Domain-specific terminology
- Tone preferences (formal vs casual)
- Whether to keep sales language
- Priority topics to expand

**In most cases, you can proceed directly to Step 4 based on your analysis.**

### Step 4: Generate Expanded FAQ (Excel)

**CRITICAL: This is where you do the actual content expansion!**

Create a new Excel file with the expanded FAQ content:

**File naming**: `<original_name>_expanded.xlsx`

**Required columns**:

- `分类` (Category)
- `问题` (Question)
- `回答` (Answer)

**Optional column** (script will generate if missing):

- `关键词` (Keywords) - you can leave this empty, script will auto-generate

**How to create the file:**

**IMPORTANT (Cross-Platform Compatibility):**

- **DO NOT use `python -c "..."` to run inline Python code** - this causes quote escaping issues on Windows
- **ALWAYS use the Write tool to create a `.py` script file first**, then run it with `python script.py`

**Step-by-step approach:**

1. First, use the **Write tool** to create a Python script (e.g., `create_faq.py`):

```python
# create_faq.py - Use Write tool to create this file
import pandas as pd

data = [
    {
        "分类": "睡眠问题咨询",
        "问题": "你们是怎么调理睡眠的？",
        "回答": "我们通过太赫兹能量睡垫来调理睡眠..."
    },
    {
        "分类": "睡眠问题咨询",
        "问题": "我总是入睡困难怎么办？",
        "回答": "入睡困难通常和气血不畅有关..."
    },
    # ... 添加所有扩展后的FAQ
]

df = pd.DataFrame(data)
df.to_excel("filename_expanded.xlsx", index=False)
print("Successfully created filename_expanded.xlsx")
```

2. Then run the script using Bash:

```bash
python create_faq.py
```

3. Clean up the temporary script after use:

```bash
rm create_faq.py  # or 'del create_faq.py' on Windows CMD
```

**Quality checklist before saving:**

- [ ] Each question is specific and focused
- [ ] Each answer is concise (typically 50-200 characters)
- [ ] Questions are grouped by logical categories
- [ ] All important knowledge points are covered
- [ ] No redundant or duplicate questions

### Step 5: Standardize Format with Script

Use the script to process the expanded file:

```bash
python process-faq/scripts/generate_rag_faq.py <expanded_file> <final_output_file>
```

**What the script does:**

- Auto-generates keywords using jieba TF-IDF
- Applies professional Excel formatting
- Sets proper column widths and styles
- Performs final duplicate check
- Creates the final RAG-optimized knowledge base

**Example:**

```bash
python process-faq/scripts/generate_rag_faq.py 申花太赫兹_expanded.xlsx 申花太赫兹_RAG_优化版.xlsx
```

## Complete Example Workflow

**User:** "Please process 申花太赫兹知识库.xlsx and convert it to RAG format"

**You (Claude):**

**Step 1: Convert to Markdown**

```bash
python process-faq/scripts/convert_to_markdown.py 申花太赫兹知识库.xlsx
```

**Step 2: Read and Analyze**

- Read the generated `申花太赫兹知识库_for_analysis.md` using Read tool
- Analyze: "I found that the original 7 FAQs have very long answers (500+ characters each)"
- Identify: "Each answer actually covers 3-5 different topics"

**Step 3: Expand Content**

- Extract knowledge points from long answers
- Create dedicated Q&A for each point
- Example: From 1 question about "如何调理睡眠", expand to:
  - 你们是怎么调理睡眠的？(调理原理)
  - 我总是入睡困难怎么办？(具体症状)
  - 先用后付是什么意思？(购买政策)
  - 为什么要用华为手环？(设备说明)
  - 手环怎么使用？(使用指南)
  - 等等...

**Step 4: Generate Expanded Excel**
Use pandas to create `申花太赫兹知识库_expanded.xlsx` with 31 focused FAQs (from original 7)

**Step 5: Standardize Format**

```bash
python process-faq/scripts/generate_rag_faq.py 申花太赫兹知识库_expanded.xlsx 申花太赫兹知识库_RAG_优化版.xlsx
```

**Step 6: Report Results**

- "Successfully expanded 7 FAQs into 31 focused entries"
- "Organized into 8 categories"
- "Auto-generated keywords for all entries"
- "Final file ready for RAG system"

## Key Principles

### 1. Content Expansion is Key

The main value you provide is:

- **Expanding** small FAQs into comprehensive knowledge bases
- **Extracting** knowledge points from long answers
- **Creating** focused, specific Q&A pairs
- NOT just cleaning up format or removing duplicates

### 2. Quality Over Quantity (But More is Often Better)

- Each FAQ should be focused and specific
- Better to have 30 focused FAQs than 5 long ones
- Each answer should ideally be 50-200 characters
- Long answers (500+) should be split into multiple FAQs

### 3. Think Like a RAG System

- How would users search for this information?
- What specific questions would they ask?
- Would this answer be found by semantic search?
- Is the question specific enough to match user intent?

### 4. Division of Labor

**Claude does (creative work):**

- Content understanding
- Knowledge point extraction
- Question splitting and rewording
- Answer rewriting
- Category design

**Script does (mechanical work):**

- Keyword extraction (jieba TF-IDF)
- Format standardization
- Excel styling
- Final duplicate check

## Quality Analysis and Expansion Checklist

### Phase A: Quality Analysis (Must do FIRST!)

- [ ] **Check for contradictions**: Do different FAQs give conflicting information?
- [ ] **Identify duplicates**: Exact or semantic duplicates (same meaning, different wording)
- [ ] **Find inconsistencies**: Similar questions with different answers (e.g., different prices, timeframes)
- [ ] **Spot incomplete info**: Answers missing key steps or context
- [ ] **Flag unclear content**: Vague questions, ambiguous terms, undefined jargon
- [ ] **Note outdated info**: References to old products, policies, or prices

**Action**: Document all issues and plan how to resolve them

### Phase B: Content Expansion (After quality fixes!)

- [ ] **Contradictions resolved**: Unified conflicting information
- [ ] **Duplicates merged**: Combined semantically identical questions
- [ ] **Long answers split**: Any answer >300 characters covering multiple topics
- [ ] **Each Q&A focused**: One question = one specific topic
- [ ] **All knowledge points extracted**: No information lost from original
- [ ] **Questions are specific**: Avoided vague questions like "如何使用?"
- [ ] **Answers are concise**: Typically 50-200 characters per answer
- [ ] **Answers are consistent**: Related FAQs give aligned information
- [ ] **Categories are clear**: 5-10 logical categories based on the domain
- [ ] **Common questions added**: Anticipated natural user questions
- [ ] **Proper structure**: Used lists, numbering, or bullet points where appropriate

## Output Format

The final Excel file will have:

| 分类     | 问题     | 回答   | 关键词   |
| -------- | -------- | ------ | -------- |
| Category | Question | Answer | Keywords |

Example:

| 分类     | 问题              | 回答                                            | 关键词           |
| -------- | ----------------- | ----------------------------------------------- | ---------------- |
| 账户管理 | 如何重置密码?     | 1. 点击"忘记密码"\n2. 输入邮箱\n3. 查收重置链接 | 密码,重置,账户   |
| 支付问题 | 支持哪些支付方式? | 我们支持:\n- 支付宝\n- 微信支付\n- 银行卡       | 支付,方式,支付宝 |

## Best Practices

1. **Always Convert First**: Don't try to analyze binary files directly
2. **Read Thoroughly**: Actually read the Markdown file, understand the domain
3. **Quality BEFORE Expansion**: Analyze issues first, then expand
   - Don't expand broken content - fix it first!
   - Resolve contradictions before creating more FAQs
   - Merge duplicates before splitting long answers
4. **Look for Logic Issues**:
   - Contradicting information across FAQs
   - Inconsistent answers to similar questions
   - Missing prerequisites or context
5. **Extract Knowledge Points**: Identify every distinct topic in long answers
6. **Ensure Consistency**: Related FAQs should give aligned, non-conflicting information
7. **Create Focused FAQs**: Each Q&A should cover one specific topic
8. **Think Like Users**: What would they search for? What questions would they ask?
9. **Generate Intermediate File**: Create `*_expanded.xlsx` before running the script
10. **Let Script Handle Keywords**: Don't manually generate keywords, let jieba do it

## Common Expansion Scenarios

### Scenario 1: Long Answer with Multiple Topics

**Original:**

```
Q: 你们的产品怎么样?
A: 我们的产品质量好、价格实惠、支持30天退货、全国包邮、还有24小时客服...
```

**Expanded:**

```
Q1: 你们的产品质量如何?
A1: 产品经过严格质检，质量可靠...

Q2: 产品价格贵吗?
A2: 价格实惠，性价比高...

Q3: 支持退货吗?
A3: 支持30天无理由退货...

Q4: 包邮吗?
A4: 全国包邮，无需额外运费...

Q5: 有客服支持吗?
A5: 提供24小时在线客服...
```

### Scenario 2: Vague Question Needs Specificity

**Original:**

```
Q: 如何使用?
A: [Long explanation covering installation, configuration, daily use, troubleshooting...]
```

**Expanded:**

```
Q1: 如何安装产品?
A1: [Installation steps]

Q2: 如何进行初始配置?
A2: [Configuration guide]

Q3: 日常使用注意事项有哪些?
A3: [Daily usage tips]

Q4: 遇到问题怎么排查?
A4: [Troubleshooting steps]
```

### Scenario 3: Contradictions and Inconsistencies

**Original (with logic issues):**

```
Q1: 配送需要多久?
A1: 一般3-5个工作日送达

Q2: 什么时候能收到货?
A2: 通常7天内送达

Q3: 支持退货吗?
A3: 支持7天无理由退货

Q4: 可以退款吗?
A4: 不支持退款，只能换货
```

**Issues Found:**

- ❌ Contradiction: Q1 说 3-5 天，Q2 说 7 天
- ❌ Contradiction: Q3 支持退货，Q4 说不支持退款
- ⚠️ Semantic duplicate: Q1 和 Q2 问的是同一件事

**Fixed and Expanded:**

```
Q1: 配送需要多久?
A1: 一般3-5个工作日送达（偏远地区可能需要7天）
[统一时间信息，说明例外情况]

Q2: 支持退货吗?
A2: 支持7天无理由退货退款
[解决矛盾：统一退货和退款政策]

Q3: 如何申请退货?
A3: 联系客服说明原因，获得退货地址后寄回即可
[新增：补充退货流程]

Q4: 退货运费谁承担?
A4: 质量问题我们承担，非质量问题需您承担
[新增：补充退货细节]
```

**Summary:**

- Resolved 2 contradictions
- Merged 1 semantic duplicate
- Expanded with 2 new related questions
- All information now consistent

### Scenario 4: Missing Obvious Questions

**Original:** Only has "如何注册账户?"

**Should also add:**

- 注册需要提供哪些信息?
- 可以用手机号注册吗?
- 忘记密码怎么办?
- 如何修改个人信息?
- 如何注销账户?

## Error Handling

If conversion fails:

- Check file format is supported
- Verify file is not corrupted
- Try opening the file manually first
- Check file encoding (should be UTF-8)

If content is unstructured:

- The Markdown will show raw text
- You'll need to manually identify Q&A pairs
- Suggest restructuring the source document

## Dependencies

Required Python packages:

- pandas (data handling)
- openpyxl (Excel support)
- python-docx (Word support)
- PyPDF2 (PDF support)
- jieba (Chinese text processing)

Install with:

```bash
pip install -r process-faq/requirements.txt
```
