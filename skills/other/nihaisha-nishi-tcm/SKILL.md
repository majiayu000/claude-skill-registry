---
name: nihaisha
description: Use this skill when the user asks about Ni Haisha / 倪海厦 TCM course material, especially Shang Han Lun / 伤寒论, Jingui / 金匮要略, Zhongjing Xinfa / 仲景心法, clinical cases / 临床案例 / 倪师医案, Bagang Bianzheng / 八纲辨证, Fuyang Forum / 扶阳论坛, Yijinjing / 易筋经, Liang Dong dialogue / 梁冬对话倪师, Stanford lecture / 斯坦福大学演讲, Tianji / 天纪 / 易经 / 阳宅 / 紫微斗数, Huangdi Neijing / 黄帝内经, Shennong Bencao / 神农本草, acupuncture / 针灸, meridians, acupoints, six-channel pattern identification, symptom-to-formula routing, formula comparison, lesson review, board/PPT screenshot evidence, or course-derived study notes. This skill is for educational distillation and study support only, not medical diagnosis, prescriptions, dosage, or individualized treatment.
metadata:
  short-description: 倪海厦《伤寒论》《金匮要略》《仲景心法》《临床案例》《八纲辨证》《扶阳论坛》《易筋经》《梁冬对话》《斯坦福演讲》《天纪》《黄帝内经》《神农本草》《针灸》课程学习、方证穴位辨析和板书证据索引
---

# Nihaisha 中医课程资料

## Scope

Use this skill to answer study, organization, retrieval, and evidence-index requests based on 倪海厦中医课程资料. Keep responses grounded in the bundled references and clearly distinguish course-derived claims from general reasoning.

This skill is educational. Do not present content as diagnosis, prescription, or individualized medical advice. For urgent, severe, pregnancy-related, pediatric, medication-interaction, or unclear clinical situations, tell the user to consult a licensed clinician.

## Workflow

1. Identify the user's entry point: symptom, formula, six-channel pattern, disease name, lesson number, or study objective.
2. Open `references/index.md` first, then load only the relevant module:
   - User-facing learning entry: `references/learning-entry.md`.
   - Beginner/plain-language questions: `references/beginner-questions.md`.
   - Detailed scenario routing: `references/usage-scenarios.md`.
   - Symptoms or cases: `references/symptom-index.md`, then `references/six-channel.md`, then `references/formula-patterns.md` if a formula comparison is needed.
   - Formula queries: `references/formula-patterns.md`, with `references/six-channel.md` for context.
   - Six-channel review: `references/six-channel.md`.
   - Lesson review or learning plans: `references/lesson-map.md`.
   - Jingui / 金匮要略 questions: `references/jingui.md`; use `references/jingui-screenshot-evidence.md` for board, acupuncture-demo, or source-evidence lookups.
   - Zhongjing Xinfa / 仲景心法 questions: `references/zhongjing-xinfa.md`; use `references/zhongjing-xinfa-screenshot-evidence.md` for pathogenesis diagrams, formula/herb boards, eye diagnosis, organ relations, cancer/severe-disease views, or source-evidence lookups.
   - Clinical cases / 临床案例 / 倪师医案 questions: `references/clinical-cases.md`; use `references/clinical-cases-screenshot-evidence.md` for case board, formula, pathogenesis, tumor, heart, liver, kidney, breast cancer, lupus, or severe-disease evidence lookups.
   - Bagang Bianzheng / 八纲辨证 questions: `references/bagang.md`; use `references/bagang-screenshot-evidence.md` for representative lecture frames/subtitle evidence. This module has no board/PPT screenshots because the source video is mostly lecturer half-body footage with subtitles.
   - Fuyang Forum / 扶阳论坛 questions: `references/fuyang.md`; use `references/fuyang-screenshot-evidence.md` for board, PPT, case slide, severe-disease, yang-supporting theory, or source-evidence lookups.
   - Yijinjing / 易筋经 questions: `references/yijinjing.md`; use `references/yijinjing-screenshot-evidence.md` for movement demo, posture, breathing cue, five-zang detox method, Wen-style/Yang-style exercise, or source-evidence lookups.
   - Liang Dong dialogue / 梁冬对话倪师 questions: `references/liangdong.md`; this module currently has text distillation only, with no screenshot evidence because the visual model quota was exhausted during ingestion.
   - Stanford lecture / 斯坦福大学演讲 questions: `references/stanford.md`; this module currently has text distillation only, with no screenshot evidence because the visual model quota was exhausted during ingestion.
   - Tianji / 天纪 / 易经 / 阳宅 / 紫微斗数 questions: `references/tianji.md`; use `references/tianji-screenshot-evidence.md` for board, Yi Jing, Bagua, Yangzhai, Feng Shui, Ziwei Doushu, minggong, four transformations, pre-heaven/post-heaven trigrams, heavenly stems/earthly branches, or divination evidence lookups. Lessons 1-3 have LLM summaries; lessons 4-24 use transcript-based extractive summaries.
   - Huangdi Neijing / 黄帝内经 questions: `references/huangdi.md`; use `references/huangdi-screenshot-evidence.md` for board, PPT, five-phase, seasonal cultivation, pulse, zangxiang, meridian, or pathogenesis evidence lookups.
   - Huangdi Neijing notes / 黄帝内经笔记 / 讲稿 / 原著 questions: `references/notes-huangdi.md`; use after `references/huangdi.md` when the user asks specifically for written notes, handouts, or source-text supplements.
   - Shennong Bencao / 神农本草 questions: `references/bencao.md`; use `references/bencao-screenshot-evidence.md` for herb, flavor/nature/channel tropism, dosage form, dose unit, compatibility, or medicinal theory evidence lookups.
   - Shennong Bencao notes / 神农本草笔记 / 单味药图文笔记 questions: `references/notes-bencao.md`; use after `references/bencao.md` for written note or herb-note supplement lookups.
   - Acupuncture / 针灸 questions: `references/acupuncture.md`; use `references/acupuncture-screenshot-evidence.md` for meridian, acupoint, needling, moxibustion, board, or demo evidence lookups.
   - Acupuncture Dacheng notes / 针灸大成笔记 / 针灸讲稿 questions: `references/notes-acupuncture-dacheng.md`; use after `references/acupuncture.md` for written note or handout supplement lookups.
   - Shang Han Lun notes / 伤寒论笔记 / 伤寒讲稿 questions: `references/notes-shanghan.md`; use after `references/shanghanlun.md` or formula references when the user asks specifically for written notes or handouts.
   - Jingui notes / 金匮要略笔记 / 金匮讲稿 questions: `references/notes-jingui.md`; use after `references/jingui.md` when the user asks specifically for written notes or handouts.
   - Hantang TCM / 汉唐中医 / 汉唐文章 / 汉唐处方 / 事实评论 questions: `references/hantang.md`; use for Hantang article and formula-commentary archive lookups, keeping course-video references as primary when they overlap.
   - Diagnostic logs / 诊疗日志 / 病案记录 / 人纪班案例 questions: `references/diagnostic-logs.md`; use for case-log and follow-up-note lookups, with a strong educational-only safety frame.
   - Ebooks / 电子书合集 / 原著 / 秘方手法 / 大合集 questions: `references/ebooks.md`; use as a broad inventory and extracted-text supplement, not as the primary authority over course references.
   - Audio collection / 倪师音频合集 / MP3 / 录音 questions: `references/audio-collection.md`; use to map local audio files to already-distilled course modules.
   - Course overview or older all-in-one lookup: `references/shanghanlun.md`.
   - Board/PPT/source evidence: prefer `python scripts/search_screenshots.py <terms...>` for ranked results; use `rg` on `references/screenshot-evidence.md` only for quick manual lookup.
3. Answer in the structure that matches the task:
   - Symptom or case: pattern differentiation, missing evidence, possible course方证, cautions, and no personal prescription.
   - Formula: course方证, symptom cluster, course方义, contraindications/cautions, related formulas, lesson labels.
   - Lesson study: chapter outline, key concepts, formulas, review questions, and screenshot evidence keywords.
   - Evidence request: return course, timestamp, brief note, and absolute screenshot path. Prefer results that match all important query terms. If the environment can display a local image and the user asks to see it, open the relevant screenshot path.
   - Knowledge organization: tables by 六经, 方证, 症状, course sequence, or user workflow.
4. Cite the reference module, lesson label, and screenshot path when possible.

When the user asks whether the structure is suitable, or what the learner's purpose is, prefer the user-facing structure in `learning-entry.md` over the course sequence. Treat the course sequence as traceability, not the primary user interface.

If the user uses plain everyday language rather than TCM terms, open `references/beginner-questions.md` first. Translate the question into simple differentiating questions before using 六经 or 方证 terminology.

## Safety Requirements

- Always frame the content as 倪海厦课程学习 or 中医理论整理, not medical diagnosis.
- Do not provide an individualized prescription, dosage, or instruction that a user can directly self-administer.
- For 四逆汤辈, 附子类, 大承气汤/急下存阴, 抵当汤, 大陷胸汤, 癌症/肿瘤/阴实, pregnancy, pediatric cases, severe pain, chest pain, altered consciousness, dehydration, or other urgent signs, add a clear warning to seek professional care immediately.
- If the user describes real symptoms, first state what information is missing before comparing course方证.

## Style

Prefer compact Chinese explanations with tables when comparing formulas or patterns. Use the original course terminology where it is useful, but normalize obvious transcript errors and note uncertainty when a term may be mis-transcribed.

When the user wants a reusable artifact, produce Markdown that can be appended back into the relevant reference file.
