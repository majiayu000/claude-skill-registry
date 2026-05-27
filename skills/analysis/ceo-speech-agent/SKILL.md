---
name: ceo-speech-agent
description: CEO statement tone shift analyzer for /ceo-analysis page. Analyzes CEO quotes from SEC filings, earnings calls to detect tone changes (positive→cautious, cautious→aggressive) and finds historical similar patterns. Generates news articles when significant shifts detected.
license: Proprietary
compatibility: Requires SEC filings, earnings transcripts, NLP tone analysis, historical pattern database
metadata:
  author: ai-trading-system
  version: "1.0"
  category: analysis
  agent_role: ceo_analyst
---

# CEO Speech Agent - CEO 발언 Tone Shift 분석

## Role
`/ceo-analysis` 페이지에서 CEO 발언의 **Tone Shift**(어조 변화)를 감지하여 숨겨진 trading signals를 찾습니다.

## Core Capabilities

### 1. Tone Detection

#### Tone Levels
```python
TONE_LEVELS = {
    "VERY_POSITIVE": 2,      # 매우 자신감, aggressive 투자
    "POSITIVE": 1,           # 긍정적, 안정적
    "NEUTRAL": 0,            # 중립, 사실 나열
    "CAUTIOUS": -1,          # 신중, 보수적, hedging
    "NEGATIVE": -2           # 부정적, 우려 표명
}
```

#### Key Indicators

**VERY_POSITIVE Signals**:
- "record", "unprecedented", "exceptional"
- "doubling down", "aggressive expansion"
- "confident", "optimistic outlook"
- Specific numbers (positive guidance)

**CAUTIOUS Signals**:
- "uncertain environment", "challenging"
- "monitoring closely", "prudent approach"
- "headwinds", "macro pressures"
- Vague guidance, hedging language

**NEGATIVE Signals**:
- "disappointed", "below expectations"
- "restructuring", "cost-cutting"
- "difficult decisions ahead"
- Guidance cuts

### 2. Tone Shift Detection

```python
def detect_tone_shift(
    previous_tone: int,
    current_tone: int
) -> Dict:
    """Detect significant tone changes"""
    
    shift = current_tone - previous_tone
    
    if abs(shift) >= 2:
        significance = "MAJOR"
    elif abs(shift) == 1:
        significance = "MODERATE"
    else:
        significance = "NONE"
    
    if shift > 0:
        direction = "UPGRADE"
        signal = "BULLISH"
    elif shift < 0:
        direction = "DOWNGRADE"
        signal = "BEARISH"
    else:
        direction = "STABLE"
        signal = "NEUTRAL"
    
    return {
        "shift_magnitude": abs(shift),
        "significance": significance,
        "direction": direction,
        "trading_signal": signal,
        "confidence": min(0.9, 0.5 + abs(shift) * 0.2)
    }
```

**Example**:
```
Previous (Q3): POSITIVE (+1)
  "We're seeing steady growth..."

Current (Q4): VERY_POSITIVE (+2)
  "Record demand! Doubling capex for aggressive expansion!"

Shift: +1 (UPGRADE)
→ Significance: MODERATE
→ Signal: BULLISH
→ Confidence: 0.7
```

### 3. Historical Pattern Matching

```python
def find_similar_patterns(
    ticker: str,
    current_tone_shift: Dict,
    lookback_years: int = 5
) -> List[Dict]:
    """Find past instances of similar tone shifts"""
    
    # Query historical filings
    past_filings = db.query(CEOAnalysis).filter(
        CEOAnalysis.ticker == ticker,
        CEOAnalysis.created_at >= datetime.now() - timedelta(days=365*lookback_years)
    ).all()
    
    similar_patterns = []
    
    for filing in past_filings:
        if filing.shift_direction == current_tone_shift['direction']:
            if filing.shift_magnitude >= current_tone_shift['shift_magnitude']:
                # Calculate subsequent price change
                price_change = get_price_change(
                    ticker,
                    filing.date,
                    filing.date + timedelta(days=90)
                )
                
                similar_patterns.append({
                    "date": filing.date,
                    "quarter": filing.quarter,
                    "shift": filing.shift_magnitude,
                    "subsequent_price_change_3m": price_change,
                    "quote": filing.ceo_quote
                })
    
    return similar_patterns
```

**Example Output**:
```json
{
  "similar_past_instances": [
    {
      "date": "2022-Q2",
      "shift": "UPGRADE (+1)",
      "ceo_quote": "Doubling R&D investment...",
      "subsequent_price_change_3m": "+12.5%"
    },
    {
      "date": "2020-Q4",
      "shift": "UPGRADE (+1)",
      "ceo_quote": "Record pipeline, aggressive hiring...",
      "subsequent_price_change_3m": "+18.2%"
    }
  ],
  "average_price_change": "+15.4%",
  "pattern_reliability": 0.75
}
```

### 4. News Article Generation

When significant tone shift detected:

```python
async def generate_news_article(
    ticker: str,
    ceo_analysis: Dict
) -> int:
    """Generate news article for tone shift"""
    
    if ceo_analysis['shift']['significance'] in ['MAJOR', 'MODERATE']:
        # Create article
        article = NewsArticle(
            ticker=ticker,
            article_type='ceo_speech',
            headline=f"{ticker} CEO Tone Shift: {ceo_analysis['shift']['direction']}",
            content=format_ceo_analysis_article(ceo_analysis),
            sentiment_score=calculate_sentiment(ceo_analysis),
            source='ceo_analysis_agent',
            created_at=datetime.now()
        )
        
        db.add(article)
        db.commit()
        
        # Trigger trading signal
        create_trading_signal(
            ticker=ticker,
            action=derive_action(ceo_analysis['shift']['trading_signal']),
            source='ceo_analysis',
            confidence=ceo_analysis['shift']['confidence'],
            reasoning=ceo_analysis['summary']
        )
        
        return article.id
```

## Decision Framework

```
Step 1: Extract CEO Quotes
  sources = [
    "10-K", "10-Q" SEC filings,
    "Earnings Call Transcripts",
    "Shareholder Letters",
    "Conference Presentations"
  ]
  
  FOR each source:
    extract_ceo_statements()

Step 2: Analyze Current Tone
  current_tone = analyze_tone(current_quotes)
  
  indicators = {
    "positive_words": count(["record", "strong", "confident"]),
    "cautious_words": count(["uncertain", "challenging"]),
    "specific_numbers": extract_guidance(),
    "hedging_language": detect_hedges()
  }
  
  current_tone_level = calculate_tone_level(indicators)

Step 3: Compare to Previous Tone
  previous_tone = get_previous_quarter_tone(ticker)
  
  tone_shift = detect_tone_shift(previous_tone, current_tone)

Step 4: IF Significant Shift:
  # Find historical patterns
  similar_patterns = find_similar_patterns(ticker, tone_shift)
  
  # Estimate impact
  expected_price_impact = average(similar_patterns.price_changes)
  
  # Generate news article
  IF tone_shift.significance in ['MAJOR', 'MODERATE']:
    article_id = generate_news_article(ticker, analysis)

Step 5: Generate Trading Signal
  action = derive_action_from_shift(tone_shift)
  
  create_trading_signal(
    ticker=ticker,
    action=action,
    source='ceo_analysis',
    confidence=tone_shift.confidence,
    metadata={
      "tone_shift": tone_shift,
      "historical_patterns": similar_patterns,
      "article_id": article_id
    }
  )
```

## Output Format

```json
{
  "ticker": "AAPL",
  "ceo_name": "Tim Cook",
  "filing_type": "10-Q",
  "filing_date": "2025-10-31",
  "quarter": "2025-Q3",
  "analysis_timestamp": "2025-12-21T13:00:00Z",
  
  "current_quarter_analysis": {
    "ceo_quotes": [
      {
        "quote": "We are doubling down on AI investments and see unprecedented demand",
        "source": "Earnings Call",
        "timestamp": "2025-11-01 16:00",
        "tone": "VERY_POSITIVE",
        "key_phrases": ["doubling down", "unprecedented demand"]
      },
      {
        "quote": "iPhone sales exceeded our most optimistic projections",
        "source": "10-Q Filing",
        "tone": "VERY_POSITIVE",
        "key_phrases": ["exceeded", "optimistic"]
      }
    ],
    "aggregated_tone": "VERY_POSITIVE",
    "tone_level": 2,
    "confidence": 0.90
  },
  
  "previous_quarter_analysis": {
    "quarter": "2025-Q2",
    "aggregated_tone": "POSITIVE",
    "tone_level": 1
  },
  
  "tone_shift": {
    "shift_magnitude": 1,
    "significance": "MODERATE",
    "direction": "UPGRADE",
    "trading_signal": "BULLISH",
    "confidence": 0.70,
    "interpretation": "CEO 어조가 긍정에서 매우 긍정으로 상향. 공격적 투자 시사."
  },
  
  "historical_pattern_analysis": {
    "similar_past_instances": [
      {
        "date": "2022-02-01",
        "quarter": "2022-Q1",
        "shift": "UPGRADE",
        "ceo_quote": "Aggressive R&D expansion...",
        "subsequent_price_change_3m": "+12.5%",
        "subsequent_price_change_6m": "+18.2%"
      },
      {
        "date": "2020-11-01",
        "quarter": "2020-Q4",
        "shift": "UPGRADE",
        "ceo_quote": "Record pipeline...",
        "subsequent_price_change_3m": "+15.8%",
        "subsequent_price_change_6m": "+22.1%"
      }
    ],
    "pattern_count": 2,
    "average_price_change_3m": "+14.2%",
    "average_price_change_6m": "+20.2%",
    "pattern_reliability": 0.75,
    "interpretation": "과거 유사 패턴에서 평균 3개월 +14% 상승"
  },
  
  "trading_recommendation": {
    "action": "BUY",
    "confidence": 0.75,
    "reasoning": "CEO tone upgrade (POSITIVE → VERY_POSITIVE) + 과거 패턴 평균 +14% (3M)",
    "target_price_3m": 205.00,
    "expected_return_3m": 0.14,
    "stop_loss": 185.00
  },
  
  "news_article_generated": {
    "article_id": 789,
    "headline": "AAPL CEO Tone Shift: 공격적 AI 투자 암시",
    "summary": "Tim Cook CEO가 실적 발표에서 '전례 없는 수요'와 'AI 투자 배가' 언급. 과거 유사 패턴 분석 시 평균 +14% 상승.",
    "sentiment_score": 0.8
  },
  
  "key_risks": [
    "과거 패턴이 반복되지 않을 수 있음",
    "거시경제 환경 변화",
    "경쟁사 동향"
  ]
}
```

## Examples

**Example 1**: Major Upgrade (CAUTIOUS → VERY_POSITIVE)
```
Previous Q: "Uncertain macro environment, prudent approach..."
  Tone: CAUTIOUS (-1)

Current Q: "Record demand! Doubling capex, aggressive hiring!"
  Tone: VERY_POSITIVE (+2)

Shift: +3 (MAJOR UPGRADE)
→ Signal: STRONG_BUY
→ Confidence: 0.90
→ Expected: +20% (based on 2018 similar pattern)
```

**Example 2**: Moderate Downgrade
```
Previous Q: "Strong performance, confident outlook..."
  Tone: POSITIVE (+1)

Current Q: "Monitoring headwinds closely, cautious on guidance..."
  Tone: CAUTIOUS (-1)

Shift: -2 (MODERATE DOWNGRADE)
→ Signal: BEARISH
→ Confidence: 0.75
→ Expected: -8% (based on 2019, 2021 patterns)
```

## Guidelines

### Do's ✅
- **Context 중시**: 동일 단어도 문맥에 따라 다름
- **Historical Pattern 확인**: 과거 유사 사례 필수
- **Quote 원문 보존**: 해석 편향 방지
- **News Article 생성**: 중요한 shift는 기사화

### Don'ts ❌
- 단일 문장으로 판단 금지
- 과거 패턴 무시 금지
- CEO 개인 성향 고려 안 함 금지 (Musk vs Cook)
- Pattern reliability < 60% 시 과신 금지

## Integration

### SEC Filings Extraction

```python
from backend.data.sec_client import SECClient

sec = SECClient()

# Get latest 10-Q
filing = sec.get_latest_filing(ticker='AAPL', form_type='10-Q')

# Extract MD&A section (Management Discussion & Analysis)
mda_section = sec.extract_section(filing, section='MDNA')

# Extract CEO quotes
ceo_quotes = extract_ceo_statements(mda_section)
```

### Earnings Call Transcripts

```python
from backend.data.earnings_call_client import EarningsCallClient

earnings = EarningsCallClient()

# Get latest transcript
transcript = earnings.get_latest_transcript(ticker='AAPL')

# Extract CEO portion
ceo_remarks = transcript.get_executive_remarks(executive='CEO')
```

## Performance Metrics

- **Tone Detection Accuracy**: > 85%
- **Pattern Matching Recall**: > 80% (주요 패턴 포착)
- **Generated Signal Accuracy**: > 70%
- **News Article Usefulness**: > 4/5

## Version History

- **v1.0** (2025-12-21): Initial release with tone shift detection and historical pattern matching
