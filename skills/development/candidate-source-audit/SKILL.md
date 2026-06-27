---
name: candidate-source-audit
description: >-
  源码级候选人尽调 SOP——评估工程/AI 岗候选人时,不采信简历措辞,而是 clone 他们的 GitHub
  逐行读真实源码、用 git 核实代码到底谁写的、对照岗位反指标清单证伪,区分"真系统 vs 套壳玩具",
  评估 AI-Native 思维,结合年级×专业判断潜力与投入度,产出带证据链的排序结论 + 针对其真实项目
  设计的面试题 + 评分表 + 预筛话术。Use this WHENEVER the user is screening / evaluating /
  vetting / comparing / ranking job candidates, applicants, interns, or résumés —— especially
  AI / Agent / 工程岗,或任何时候用户贴出候选人的简历、GitHub、作品集并问"这人是真的吗/行不行/
  适配吗""分析一下这个候选人""这些项目是真做的还是套壳""帮我准备面试题/预筛话术"。哪怕用户只是
  甩一张简历图片/PDF + 一段 JD,也要触发。核心信条:简历是包装,代码是真相。
---

# Candidate Source Audit · 源码级候选人尽调

**核心信条:简历是包装,代码是真相(Resume is packaging; code is truth)。**

人人都会包装简历。只读简历下结论 = 让候选人自己给自己打分。本 skill 把评估的第一性原理
从"他声称做了什么"转成"**哪句经得起源码对质,哪句一查就垮**"。AI(你)是放大尽调效率的工具;
最终判断尺度由用户来把(见 [references/rubric.md](references/rubric.md) 的"不可验证≠造假"与"复核 AI 自己的结论")。

> 责任声明:仅用于正当招聘/评估;只用候选人**公开**的资料;尊重隐私,结论要基于证据、对人公平。

---

## 完整流程 SOP

按顺序做。每一步都先收集证据,最后才下判断。

### 0. 起手:抽取简历主张 + 锁定可验证物
- 读简历(PDF/图片均可),抽出:学校/专业/年级/毕业时间、声称的项目与"我负责的部分"、声称的指标、GitHub/作品链接。
- **把简历当"待证伪的主张清单",不是事实。** 标出最唬人、最该验的几条(通常是"旗舰项目"和精确指标)。

### 1. 锁定真实 GitHub 账号
简历上的链接是第一可验证物,但常常**失效或改名**——这本身就是信号。
- 跑 `python scripts/find_github.py <简历handle> <邮箱> <姓名拼音>`:直连核验 handle、从邮箱前缀派生 handle、按姓名/变体搜索用户。
- 注意:① handle 404(死链)② 账号名与简历真名不符 ③ 账号是上个月才建 ④ 真号是 `<handle>-commits` 或邮箱派生名。**这些都要记进结论。**
- 找不到≠造假,但要先穷尽再下"不可验证"的结论(见 rubric 的"不可验证≠造假")。

### 2. 枚举仓库,先读元数据(元数据本身就会暴露很多)
- 跑 `python scripts/github_enum.py <handle>`:打印账号年龄、仓库数、followers + 每个仓库的 fork?/语言/体积/star/创建/更新/描述。
- 元数据级"照妖镜":
  - **fork 占比**:一堆仓库大多是知名项目的 fork(框架、知名库、甚至学习资料)→ 把 GitHub 当书签,不是 builder。
  - **体积**:号称复杂系统/平台却只有几十 KB → 大概率套壳玩具。
  - **新鲜度**:账号/全部仓库都是最近一个月建的 → 可能临投简历突击包装。
  - **简历里的"代表作"在不在**:精选项目一个都不在 GitHub 上 → 不可验证 / 注水。

### 3. Clone 实质仓库,逐行读真实源码
- 只 clone **OWN + 有代码量 + 与岗位相关**的:`git clone --depth 1 <url>`。
- **跳过**:知名项目的 fork、纯数据/资源仓库、模板套壳。大仓库用 `--filter=blob:none` 或只看代码目录。
- 读核心源码,别读 README 话术、别看 star。看架构是否真实落地(详见判断要点)。

### 4. 核实代码到底谁写的(关键)
- `git log --pretty='%an %ad %s' --date=short`、`git shortlog -sne`、`git log --author=<name>`、`git blame` 关键文件。
- 揪出:① 旗舰/论文代码挂在**合作者**账号下、候选人 0 commit ② AI 生成(署名异常、分支名带工具名、一天内突击 commit、全是 "Add files via upload" 网页拖传)③ 一次性 dump vs 真迭代。

### 5. 逐仓库定性:真系统 vs 套壳?命中反指标?AI-Native?
对照 [references/rubric.md](references/rubric.md) 的三张清单逐条打钩:
- **真系统 vs 套壳玩具的"tells"**(如声明却从不使用的依赖/调度字段 = 假调度)。
- **岗位反指标清单**(RAG/低代码/纯 API/CRUD/框架依赖/纯微调)——主动去抓。
- **AI-Native 真假**(把模型当成"在自建环境里干活的 Agent" vs 裸调 API 拿文本)。

### 6. 年级 × 专业 → 潜力与"能否用心 commit"
能力之外,种子岗要"能长期投入、能自己定义系统、留得住"。按 rubric 的"潜力与投入度"维度判断:
runway(剩余在校时间)、方向自洽(专业/研究方向/项目是否都指向岗位)、竞争性拉力(读研/创业/主业无关/出国)、内在动机 vs 工具性动机。

### 7. 综合:排序 + 证据链 + "不可验证≠造假"复核
- 按 [输出格式](#输出格式) 产出排序与逐人定性。
- 每条结论都挂**代码级证据**(文件路径/片段/commit 归属/LOC)。
- **复核自己的结论**:把"搜不到""没做完"误判成"造假"了吗?严格区分「私有/未完成」与「夸大/不存在」(absence of evidence ≠ evidence of absence)。

### 8. 若进入面试:面试准备 + 评分表 + 预筛
见 [references/interview-and-prescreen.md](references/interview-and-prescreen.md):
针对候选人**真实做过的项目**设计面试题(附✅好答案/🚩危险信号)、一页纸评分表、以及非正式预筛(吸引 + 摸底,不是把人聊死)。

---

## 判断要点速查(完整版见 references/rubric.md)

**套壳的铁证(看到就警惕):** 声明却从不使用的字段(假调度/假依赖)· N 个"Agent"=同一执行函数换不同 system prompt · 低代码平台=一行 `<script>` CDN · 假 RAG=if-else 写死答案 · "爬虫/采集"实为对粘贴文本做正则切分、并无真正抓取 · 旗舰代码在合作者账号下而本人 0 commit。

**真 builder 的正面信号:** 手写底层不套框架(自写 LLM 抽象层而非现成框架)· 有界并发/失败降级/部分失败继续 · 真记忆/状态机/工具系统 · **给模型造环境**(模拟器/沙盒/工具系统)· 研读 harness 内部 · 真迭代史。

**岗位反指标(命中越多越不适配):** RAG/向量库/知识库 · Dify/LangFlow/Flowise/Coze/n8n 低代码 · prompt 编排 · 纯调 API · 纯 CRUD · 框架依赖不懂底层 · 纯模型微调。岗位标准见 [references/role-bar.md](references/role-bar.md)(**按岗位替换**)。

---

## 输出格式

ALWAYS 用这个结构,且每条结论必须挂证据:

```
# <岗位> · 候选人源码尽调(N 人)
> 审计方法:克隆全部可访问仓库逐行读源码;git log/blame 核实代码归属;对照反指标清单证伪。

## 总览(排序表)
| 排序 | 候选人 | 穿透本质后的真身 | 岗位适配/10 | 验证状态 | 诚信 |

## 逐人深析(每人)
- 年级专业(→潜力/投入度)
- 本质定性(真系统/套壳/研究脚本/模板/通才…)
- 代码级铁证(文件路径 + 片段 + commit 归属 + LOC)
- AI-Native 真假
- 命中哪些反指标
- 潜力 & 能否用心 commit
- 给决策者的话 + 一道"当面就能戳穿/验证"的穿透题

## 行动建议:谁进面(+验什么)、谁直接 pass、特殊处理(如:先要私有代码再判断)
```

向上级/决策者汇报时:**凸显用户本人的判断框架**,把 AI 定位成"放大判断力的尽调工具",而非"我让 AI 自己判断"。

---

## 复用脚本
- `scripts/find_github.py <handle|email|name>` — 锁定/核验真实 GitHub 账号(死链、改名、邮箱派生、变体搜索)。
- `scripts/github_enum.py <handle>` — 枚举仓库 + 元数据照妖镜(fork 比/体积/新鲜度/代表作在不在)。
- 两脚本均无需鉴权(GitHub API 未鉴权 60 次/小时,够用);Windows 下已处理 UTF-8 输出。

## 参考文件
- [references/rubric.md](references/rubric.md) — 判断核心:5+1 维度 · 套壳 tells · 反指标 · AI-Native · 年级×专业潜力 · "不可验证≠造假" · 复核 AI 结论。
- [references/role-bar.md](references/role-bar.md) — 岗位标尺模板(示例填了一个通用 "AI Agent Harness" 岗,**按你的岗位替换**)。
- [references/interview-and-prescreen.md](references/interview-and-prescreen.md) — 面试题设计 + 一页纸评分表 + 非正式预筛话术。
