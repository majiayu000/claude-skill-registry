---
name: rag-quality
description: RAG 시스템 품질 평가 및 개선을 위한 스킬입니다. RAGAS 기반 LLM-as-Judge 평가, 사용자 페르소나 시뮬레이션, 합성 데이터 생성, 평가 결과 저장 및 분석 기능을 제공합니다.

version: 1.0.0
category: domain
status: active
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob

triggers:
  keywords:
    - "RAG 평가"
    - "품질 평가"
    - "answer quality"
    - "evaluation"
    - "metrics"
    - "faithfulness"
    - "relevancy"
    - "hallucination"
    - "persona"
    - "test query"
  agents:
    - rag-quality-evaluator
  phases:
    - run
    - sync
  languages:
    - python
---

# RAG Quality Evaluation Skill

RAG 시스템의 품질을 평가하고 개선하기 위한 포괄적인 스킬입니다.

## 핵심 기능

### 1. RAGAS 기반 자동 평가

```python
from src.rag.domain.evaluation import RAGQualityEvaluator
from src.rag.infrastructure.storage import EvaluationStore

# 평가기 초기화
evaluator = RAGQualityEvaluator(judge_model="gpt-4o")
store = EvaluationStore()

# 단일 턴 평가
result = evaluator.evaluate_single_turn(
    query="휴학 절차가 어떻게 되나요?",
    contexts=["학칙 제15조에 따르면..."],
    answer="학칙 제15조에 따라 휴학 신청은..."
)

# 결과 저장 및 분석
store.save_evaluation(result)
print(f"전체 점수: {result.overall_score:.2f}")
print(f"합격 여부: {result.passed}")
```

### 2. 사용자 페르소나 테스트

```python
from src.rag.domain.evaluation.personas import PersonaManager

persona_mgr = PersonaManager()

# 특정 페르소나로 테스트
freshman_queries = persona_mgr.generate_queries(
    persona="freshman",
    count=10,
    topic="휴학"
)

# 모든 페르소나로 통합 테스트
all_queries = persona_mgr.generate_all_personas_queries(
    queries_per_persona=5
)
```

### 3. 합성 테스트 데이터 생성

```python
from src.rag.domain.evaluation.synthetic_data import SyntheticDataGenerator
from src.rag.infrastructure.json_loader import JSONDocumentLoader

loader = JSONDocumentLoader("data/output/규정집.json")
generator = SyntheticDataGenerator(loader)

# 문서에서 질문 자동 생성
queries = generator.generate_queries_from_documents(
    num_questions=50,
    difficulty="mixed"
)

# 규정 기반 시나리오 생성
scenarios = generator.generate_scenarios_from_regulations(
    regulation="학칙",
    num_scenarios=10
)
```

### 4. 평가 결과 분석

```python
from src.rag.domain.evaluation.quality_analyzer import QualityAnalyzer

analyzer = QualityAnalyzer()

# 약점 분석
weaknesses = analyzer.analyze_weaknesses(evaluation_results)

# 기준선과 비교
improvement = analyzer.compare_results(baseline_results, new_results)

# 개선 권장사항 생성
recommendations = analyzer.generate_recommendations(weaknesses)
```

## 워크플로우

### 기준선 평가 실행

```bash
# 전체 페르소나로 기준선 평가
uv run python -c "
from src.rag.domain.evaluation import RAGQualityEvaluator
from src.rag.domain.evaluation.personas import PersonaManager
from src.rag.infrastructure.storage import EvaluationStore

evaluator = RAGQualityEvaluator()
store = EvaluationStore()
persona_mgr = PersonaManager()

# 기준선 평가 실행
for persona_id in persona_mgr.list_personas():
    queries = persona_mgr.generate_queries(persona_id, count=5)
    for query in queries:
        # RAG 시스템 실행
        answer, contexts = run_rag_query(query)
        result = evaluator.evaluate_single_turn(query, contexts, answer)
        result.persona = persona_id
        store.save_evaluation(result)

# 통계 출력
stats = store.get_statistics()
print(f'평균 점수: {stats.avg_overall_score:.2f}')
print(f'합격률: {stats.pass_rate:.1%}')
"
```

### 개선 루프 실행

```bash
# 자동 평가 및 개선
uv run regulation --loop --auto

# 특정 메트릭 집중
uv run regulation --loop --focus faithfulness

# 특정 페르소나만 테스트
uv run regulation --loop --persona freshman
```

### 대시보드 실행

```bash
# Gradio 대시보드 시작
uv run gradio src.rag.interface.web.quality_dashboard:app

# 또는 스크립트 실행
python scripts/launch_quality_dashboard.py
```

## 4가지 핵심 메트릭

| 메트릭 | 목표 | 설명 |
|--------|------|------|
| Faithfulness | 0.90+ | 할루시네이션 감지 |
| Answer Relevancy | 0.85+ | 답변 관련성 |
| Contextual Precision | 0.80+ | 검색 정확도 |
| Contextual Recall | 0.80+ | 정보 완전성 |

## 사용자 페르소나

1. **freshman** (신입생) - 초급, 간단한 용어
2. **graduate** (대학원생) - 고급, 학술적 용어
3. **professor** (교수) - 고급, 공식적 용어
4. **staff** (교직원) - 중급, 행정적 용어
5. **parent** (학부모) - 초급, 일상적 용어
6. **international** (외국인 유학생) - 초급, 간단한 한국어/영어

## 출력 파일

- `data/evaluations/eval_YYYYMMDD_HHMMSS.json` - 평가 결과
- `data/evaluations/statistics.json` - 통계 요약
- `data/test_queries/synthetic_queries.json` - 합성 데이터
- `data/test_queries/persona_queries_*.json` - 페르소나별 쿼리
