---
name: "multi-ai-orchestrator"
description: "Ollama-based multi-AI model orchestration with auto-profiling, smart routing, and ensemble execution"
---

# Multi-AI Orchestrator

## Overview

Ollama 기반 로컬 AI 모델 자동 프로파일링, 스마트 라우팅, 앙상블 실행 스킬.

**핵심 기능**:
- ⚡ 자동 프로파일링: 모델 추가 시 자동 감지/업데이트
- 🎯 스마트 라우팅: 작업 유형별 최적 모델 선택 (정확도 95%+)
- 🚀 병렬 처리: 복잡 작업 시 3+ 모델 동시 실행 후 종합
- 💪 하드웨어 최적화: RTX PRO 6000 기준 8,425 tokens/s

## When to Use

### ✅ 적합한 경우
- 3개+ Ollama 모델 운영
- 다양한 작업 유형 (코딩/분석/번역)
- 고품질 결과 필요 (교차 검증)
- RTX 4090/5090/PRO 6000+ GPU

### ❌ 부적합한 경우
- 1-2개 모델만 사용
- VRAM 16GB 이하
- 실시간 초저지연 요구 (0.2-0.5초 오버헤드)

## Core Capabilities

### 1. 자동 모델 프로파일링
`scripts/auto_model_profiler.py` 실행 → `models_profile.json` 생성

### 2. 스마트 라우팅
| 작업 유형 | 키워드 | 선택 모델 |
|----------|--------|----------|
| 코딩 | 코드, 함수, debug | Codex |
| 분석 | 분석, 비교, 평가 | Claude |
| 번역 | 번역, translate | Gemini |
| 빠른 응답 | 빨리, 요약 | Gemini |
| 수학 | 계산, 증명 | Qwen |

### 3. 앙상블 실행
복잡 작업 → 3개 모델 병렬 → Claude 종합
- 소요: 4-9초 (단일 대비 +2-3초)
- 품질: +30-50%

### 4. MCP 통합
`cli-orchestrator` MCP로 Codex CLI, Gemini CLI 제어 가능
- `ask_codex`: 코드 특화
- `ask_gemini`: 빠른 응답
- `compare_models`: 병렬 비교
- `smart_ask`: 자동 라우팅

## Installation

### Quick Start (Claude Code)
```bash
mkdir -p ~/.claude/skills/multi-ai-orchestrator
cp SKILL.md ~/.claude/skills/multi-ai-orchestrator/
```

### 스크립트 설정
```bash
cd ~/.claude/skills/multi-ai-orchestrator
python3 auto_model_profiler.py  # 프로파일 생성
```

## Usage

### 기본 사용
```python
from smart_router import SmartRouter
router = SmartRouter()
model = router.route("Python 이진 탐색 구현해줘")  # → codex
```

### 앙상블 실행
```python
from ensemble_executor import ModelEnsemble
ensemble = ModelEnsemble()
results = await ensemble.run_parallel("기후변화 경제영향 분석")
final = ensemble.synthesize(results)
```

## Files

| 파일 | 용도 |
|------|------|
| `auto_model_profiler.py` | 모델 프로파일링 |
| `smart_router.py` | 작업→모델 라우팅 |
| `ensemble_executor.py` | 병렬 실행 |
| `mcp_bridge.py` | MCP 통합 |
| `models_profile.json` | 모델 특성 DB |

## References

상세 내용은 다음 파일 참조:
- `references/installation.md` - 상세 설치 가이드
- `references/examples.md` - 사용 예제
- `references/mcp-integration.md` - MCP 통합 상세
- `references/benchmarks.md` - 성능 벤치마크
- `references/algorithms.md` - 알고리즘 상세

## Performance

| 지표 | 값 |
|------|-----|
| 라우팅 정확도 | 95%+ |
| 단일 모델 실행 | 2-5초 |
| 앙상블 (3개) | 4-9초 |
| 품질 향상 | +30-50% |
