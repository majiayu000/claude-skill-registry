# GROVE：一种用于学习开放词汇物理技能的通用奖励机制

发布时间：2025年04月05日

`Agent` `机器人` `自动化`

> GROVE: A Generalized Reward for Learning Open-Vocabulary Physical Skill

# 摘要

> 模拟代理学习开放词汇的物理技能是一项重大的技术挑战。现有的强化学习方法存在明显局限：人工设计的奖励函数难以在多样化任务中扩展，基于演示的方法也难以突破其训练分布进行泛化。为此，我们提出了GROVE，一个无需人工工程设计或任务特定演示的通用奖励框架，实现开放词汇的物理技能学习。我们的核心发现是：大型语言模型（LLMs）和视觉语言模型（VLMs）能够提供互补的指导——LLMs生成精确的物理约束以捕捉任务需求，而VLMs则评估动作语义和自然性。通过迭代设计过程，基于VLM的反馈持续优化LLM生成的约束，从而构建一个自我改进的奖励系统。为弥合模拟与自然图像之间的领域差距，我们开发了Pose2CLIP，一个轻量级映射器，能够直接将代理姿态高效投影到语义特征空间，而无需进行计算昂贵的渲染。在多种身体形态和学习范式下的广泛实验表明，GROVE具有显著有效性，实现的动作自然度提升22.2%，任务完成度提高25.7%，同时训练速度比现有方法快8.4倍。这些成果为模拟环境中可扩展物理技能的获取奠定了新的基础。

> Learning open-vocabulary physical skills for simulated agents presents a significant challenge in artificial intelligence. Current reinforcement learning approaches face critical limitations: manually designed rewards lack scalability across diverse tasks, while demonstration-based methods struggle to generalize beyond their training distribution. We introduce GROVE, a generalized reward framework that enables open-vocabulary physical skill learning without manual engineering or task-specific demonstrations. Our key insight is that Large Language Models(LLMs) and Vision Language Models(VLMs) provide complementary guidance -- LLMs generate precise physical constraints capturing task requirements, while VLMs evaluate motion semantics and naturalness. Through an iterative design process, VLM-based feedback continuously refines LLM-generated constraints, creating a self-improving reward system. To bridge the domain gap between simulation and natural images, we develop Pose2CLIP, a lightweight mapper that efficiently projects agent poses directly into semantic feature space without computationally expensive rendering. Extensive experiments across diverse embodiments and learning paradigms demonstrate GROVE's effectiveness, achieving 22.2% higher motion naturalness and 25.7% better task completion scores while training 8.4x faster than previous methods. These results establish a new foundation for scalable physical skill acquisition in simulated environments.

[Arxiv](https://arxiv.org/abs/2504.04191)