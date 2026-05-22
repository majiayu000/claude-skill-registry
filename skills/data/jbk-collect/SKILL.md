---
name: jbk-collect
description: 전반꿀 연구소 데이터 수집. 전인구경제연구소 유튜브 영상을 수집하고 전반꿀 지수를 계산한다. 기간을 지정하면 해당 기간의 영상을 수집하고, 6개 종목(KOSPI, S&P500, NASDAQ, 삼성전자, SK하이닉스, 엔비디아)에 대한 예측을 분석하고, 시장 데이터를 조회해 전반꿀 지수를 산출한다.
---

# 전반꿀 데이터 수집

## 개요

전인구경제연구소 유튜브 영상 제목을 분석해 전반꿀 지수를 계산한다.

**전반꿀 지수** = 예측의 역방향 적중률
- 전인구가 "오른다" → 실제 하락 = 🍯 꿀
- 전인구가 "떨어진다" → 실제 상승 = 🍯 꿀

## 사용법

```bash
cd ~/.openclaw/workspace/projects/junbankkullab

# 연도/월 지정
npx tsx skills/jbk-collect/scripts/collect.ts --year 2025 --month 12

# 또는 시작일 지정 (해당 월 전체 수집)
npx tsx skills/jbk-collect/scripts/collect.ts --start 2025-12-01
```

## 출력 구조

```
data/
├── {year}/
│   └── {month}/
│       ├── videos.json       # 원본 영상 목록
│       └── predictions.json  # 분석된 예측
├── stats/
│   └── overall.json          # 전체 통계
└── api/
    └── latest.json           # 웹 API용
```

### predictions.json 형식

```json
{
  "period": { "year": 2025, "month": 12 },
  "stats": {
    "totalVideos": 45,
    "validPredictions": 12,
    "honeyCount": 5,
    "honeyIndex": 41.7,
    "assetStats": [...]
  },
  "predictions": [...]
}
```

## 종목

| 종목 | 티커 | 패턴 |
|------|------|------|
| KOSPI | ^KS11 | 코스피 |
| S&P500 | ^GSPC | s&p, 에스앤피 |
| NASDAQ | ^IXIC | 나스닥 |
| 삼성전자 | 005930.KS | 삼성전자, 삼전 |
| SK하이닉스 | 000660.KS | 하이닉스 |
| 엔비디아 | NVDA | 엔비디아, nvidia |

## 필수 환경

- `YOUTUBE_API_KEY` in `.env.local`
- Python venv with `yfinance` at `./venv`
