---
name: virtual-environment
description: Check and create virtual environments for projects that need them. Use when starting Python/Node projects, or when dependency isolation is needed. Activates for Python, Node.js, and similar ecosystems.
allowed-tools: Read, Glob, Grep, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# Virtual Environment Management

가상환경이 필요한 프로젝트에서 환경을 체크하고 생성하는 스킬입니다.

## When This Skill Activates

다음 파일 발견 시 가상환경 필요 여부 체크:

| 파일 | 프로젝트 유형 | 가상환경 |
|------|-------------|----------|
| `requirements.txt` | Python | venv/virtualenv |
| `pyproject.toml` | Python (Poetry/PDM) | Poetry/PDM 내장 |
| `Pipfile` | Python (Pipenv) | Pipenv 내장 |
| `setup.py` | Python 패키지 | venv |
| `package.json` | Node.js | node_modules (자동) |
| `Gemfile` | Ruby | bundler |
| `go.mod` | Go | 모듈 시스템 (자동) |

## Detection Workflow

### 1. 프로젝트 유형 감지

```bash
# 프로젝트 루트에서 실행
ls -la | grep -E "requirements|pyproject|Pipfile|package\.json|Gemfile|go\.mod"
```

### 2. 가상환경 존재 확인

```bash
# Python venv 확인
ls -la | grep -E "^d.*(venv|\.venv|env|\.env)$"

# Python - 활성화 여부
echo $VIRTUAL_ENV

# Node - node_modules 확인
ls -d node_modules 2>/dev/null
```

## Python Projects

### venv (표준 라이브러리)

```bash
# 가상환경 생성
python -m venv .venv

# 활성화 (macOS/Linux)
source .venv/bin/activate

# 활성화 (Windows)
.venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 비활성화
deactivate
```

### Poetry (권장)

```bash
# Poetry 설치 확인
poetry --version

# 가상환경 자동 생성 + 의존성 설치
poetry install

# 가상환경 내에서 실행
poetry run python script.py

# 쉘 진입
poetry shell
```

### Pipenv

```bash
# 가상환경 생성 + 의존성 설치
pipenv install

# 가상환경 쉘 진입
pipenv shell

# 가상환경 내에서 실행
pipenv run python script.py
```

### Conda

```bash
# 환경 생성
conda create -n myenv python=3.11

# 활성화
conda activate myenv

# 의존성 설치
conda install --file requirements.txt
# 또는
pip install -r requirements.txt
```

## Node.js Projects

```bash
# 의존성 설치 (node_modules 자동 생성)
npm install
# 또는
yarn install
# 또는
pnpm install

# 확인
ls node_modules
```

## Workflow: 프로젝트 시작 시

### Python 프로젝트

```
1. 프로젝트 유형 확인
   - pyproject.toml → Poetry/PDM
   - Pipfile → Pipenv
   - requirements.txt → venv

2. 가상환경 존재 확인
   ls -la | grep -E "venv|\.venv"

3. 없으면 생성
   python -m venv .venv

4. 활성화 + 의존성 설치
   source .venv/bin/activate
   pip install -r requirements.txt
```

### Node.js 프로젝트

```
1. package.json 확인
   cat package.json | head -20

2. node_modules 확인
   ls node_modules 2>/dev/null

3. 없으면 설치
   npm install
```

## Naming Conventions

| 이름 | 권장 | 비고 |
|------|------|------|
| `.venv` | ✅ 권장 | 숨김 폴더, 일반적 |
| `venv` | ✅ 허용 | 명시적 |
| `.env` | ⚠️ 주의 | 환경변수 파일과 혼동 |
| `env` | ⚠️ 주의 | 너무 일반적 |

## .gitignore 설정

```gitignore
# Python virtual environments
.venv/
venv/
env/
.env/

# Node
node_modules/

# Python cache
__pycache__/
*.pyc
.pytest_cache/

# IDE
.idea/
.vscode/
```

## Quick Reference

### Python 프로젝트 시작

```bash
# 1. 가상환경 체크 및 생성
[ -d ".venv" ] || python -m venv .venv

# 2. 활성화
source .venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt
```

### Node.js 프로젝트 시작

```bash
# 1. node_modules 체크 및 설치
[ -d "node_modules" ] || npm install
```

## Troubleshooting

| 문제 | 해결 |
|------|------|
| `python: command not found` | Python 설치 또는 PATH 확인 |
| `pip: command not found` | 가상환경 활성화 확인 |
| Permission denied | `sudo` 사용 금지, venv 재생성 |
| 패키지 충돌 | 가상환경 삭제 후 재생성 |
| node_modules 오류 | `rm -rf node_modules && npm install` |

## Checklist

프로젝트 시작 전:

- [ ] 프로젝트 유형 확인 (Python/Node/etc.)
- [ ] 가상환경 존재 여부 확인
- [ ] 없으면 생성
- [ ] 활성화 (Python)
- [ ] 의존성 설치
- [ ] .gitignore에 가상환경 폴더 포함 확인
