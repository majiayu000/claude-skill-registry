---
name: character-designer-agent
description: Generates NanoBanana PRO image prompts for 3D cat characters. Combines base Pixar style with ticker-specific traits, sector themes, and market-driven expressions. Supports 300+ tickers with fallback logic for unlisted stocks.
license: Proprietary
compatibility: Requires NanoBanana PRO API, ticker character database, market data
metadata:
  author: ai-trading-system
  version: "1.0"
  category: video-production
  agent_role: character_designer
---

# Character Designer Agent - 캐릭터 디자이너 (MeowStreet Wars)

## Role
NanoBanana PRO용 3D 고양이 캐릭터 이미지 프롬프트를 자동 생성합니다. 티커별 고유 특성 + 시장 감정 = 유니크한 캐릭터!

## Core Capabilities

### 1. Prompt Formula

```
[Base Style] + [Character Trait] + [Expression] + [View] + [Effects]
```

#### Components
- **Base Style**: 기본 3D 스타일 (Pixar, Disney)
- **Character Trait**: 티커별 고유 특징 (색상, 의상, 소품)
- **Expression**: 시장 상황에 따른 표정
- **View**: 카메라 앵글
- **Effects**: 추가 효과 (빛, 파티클)

### 2. Base Style

```
3D animated character render, Pixar movie style,
cute anthropomorphic cat, fluffy fur texture,
professional studio lighting, 4K resolution,
vibrant colors, detailed facial features
```

### 3. Character Database (300+ Tickers)

#### 🇺🇸 US Stocks - Technology

| Ticker | Animal | Fur Color | Outfit | Props | Theme |
|--------|--------|-----------|--------|-------|-------|
| AAPL | Cat | Silver/White | Black turtleneck | iPad, Apple logo | Minimalist, Clean |
| NVDA | Cat | Black + Neon Green | Leather jacket | GPU chip glowing | Cyberpunk, Futuristic |
| MSFT | Cat | Gray-Blue | Blue shirt | Cloud icon | Corporate, Stable |
| GOOGL | Cat | Multi-color | Casual hoodie | Chrome logo | Playful, Tech |
| META | Cat | Blue-White | Hoodie | VR headset | Virtual, Modern |
| AMZN | Cat | Orange | Delivery vest | Cardboard box | Logistics, Speed |
| TSLA | Cat | White + Red | Space suit | Electric sparks | Futuristic, Energy |

#### 🇺🇸 US Stocks - Finance

| Ticker | Animal | Fur Color | Outfit | Props | Theme |
|--------|--------|-----------|--------|-------|-------|
| JPM | Cat | Navy + Gold | Pinstripe suit | Bull statue | Wall Street, Power |
| BRK.B | Cat | Gray-White (Old) | Classic suit | Coca-Cola | Value, Wisdom |
| BAC | Cat | Red-White | Business suit | Bank vault | Banking, Secure |
| GS | Cat | Gold-Black | Luxury suit | Gold bars | Investment, Wealth |

#### 🇺🇸 US Stocks - Healthcare

| Ticker | Animal | Fur Color | Outfit | Props | Theme |
|--------|--------|-----------|--------|-------|-------|
| JNJJ | Cat | White-Red | Doctor coat | Medical cross | Healthcare, Trust |
| UNH | Cat | Blue-White | Medical scrubs | Stethoscope | Insurance, Care |
| PFE | Cat | Blue | Lab coat | Vaccine vial | Pharma, Innovation |
| MRNA | Cat | White + Blue | Scientist coat | DNA helix | Biotech, Cutting-edge |

#### 🇰🇷 Korean Stocks - 반도체/IT

| Ticker | Animal | Fur Color | Outfit | Props | Theme |
|--------|--------|-----------|--------|-------|-------|
| 삼성전자 | Cat | Blue | Clean room suit | Silicon wafer | Semiconductor, Precision |
| SK하이닉스 | Cat | Red-Black | Tech uniform | Circuit board | Memory, Speed |
| NAVER | Cat | Green-Yellow | Hoodie (Logo) | Smartphone | Platform, Search |
| Kakao | Cat | Yellow | Hoodie (Logo) | Chat bubble | Messaging, Social |

#### 🇰🇷 Korean Stocks - 2차전지

| Ticker | Animal | Fur Color | Outfit | Props | Theme |
|--------|--------|-----------|--------|-------|-------|
| 에코프로 | Bengal | Green-Black | Racing suit | Battery pack | Energy, Fast |
| LG에너지솔루션 | Cat | Purple-White | Lab coat | Lightning bolt | Innovation, Power |

#### 🦁 Beast Characters (Major Stocks)

| Ticker | Animal | Reason | Theme |
|--------|--------|--------|-------|
| 현대건설 | Tiger | 대형주, 건설 | Power, Dominance |
| LG화학 | Black Panther | 화학, 강력함 | Stealth, Chemical |
| HMM | Lion | 해운, 왕자 | Maritime, Royalty |
| 엔씨소프트 | Cheetah | 게임, 빠름 | Speed, Gaming |

### 4. Expression Variables (Dynamic)

```python
def get_expression(change_pct: float) -> str:
    """Get expression based on price change"""
    
    if change_pct > 10:
        return "ecstatic, eyes sparkling, huge smile, upward graph, coins flying, party confetti"
    
    elif change_pct > 5:
        return "very happy, wide grin, upward pointing graph, dollar signs in eyes"
    
    elif change_pct > 2:
        return "satisfied smile, confident pose, slight upward trend"
    
    elif change_pct > -2:
        return "neutral expression, calm, slight smile, sideways trend"
    
    elif change_pct > -5:
        return "worried look, small frown, downward trend line"
    
    elif change_pct > -10:
        return "sad, tears forming, broken graph, trembling"
    
    else:  # < -10%
        return "crying heavily, tears streaming, torn graph paper, despair, falling into abyss"
```

### 5. View Options

```python
VIEW_ANGLES = {
    "portrait": "front view, centered, shoulders up",
    "full_body": "full body shot, standing pose",
    "action": "dynamic pose, action shot, movement",
    "closeup": "extreme closeup, face only, emotional"
}
```

### 6. Fallback Logic

```python
def get_character_prompt(ticker: str, change_pct: float) -> str:
    """Generate prompt with fallback"""
    
    # Try registered ticker
    if ticker in CHARACTER_DATABASE:
        traits = CHARACTER_DATABASE[ticker]
    
    # Fallback: Sector-based
    else:
        sector = get_sector(ticker)
        traits = SECTOR_DEFAULTS[sector]
    
    # Fallback: Generic
    if not traits:
        traits = {
            "animal": "cat",
            "fur_color": "gray-white",
            "outfit": "business suit",
            "props": "stock chart",
            "theme": "generic trader"
        }
    
    # Combine
    base = BASE_STYLE
    character = f"{traits['fur_color']} {traits['animal']}, wearing {traits['outfit']}, holding {traits['props']}"
    expression = get_expression(change_pct)
    view = "portrait front view"
    
    return f"{base}, {character}, {expression}, {view}"
```

## Decision Framework

```
Step 1: Receive Input
  - ticker: AAPL
  - change_pct: +5.2
  - scene_context: "celebrating"

Step 2: Lookup Character Traits
  IF ticker in DATABASE:
    traits = DATABASE[ticker]
  ELIF sector known:
    traits = SECTOR_DEFAULTS[sector]
  ELSE:
    traits = GENERIC_TRADER

Step 3: Determine Expression
  expression = get_expression(change_pct)

Step 4: Select View
  view = "portrait" (default for shorts)

Step 5: Combine Prompt
  prompt = BASE_STYLE + traits + expression + view

Step 6: Add Effects (Optional)
  IF change_pct > 5:
    add "glowing aura, success vibes"
  
  IF change_pct < -5:
    add "dark shadows, gloomy atmosphere"

Step 7: Validate Length
  IF len(prompt) > 500 characters:
    shorten by removing less important details
```

## Output Format

```json
{
  "ticker": "AAPL",
  "character_info": {
    "animal_type": "cat",
    "fur_color": "silver-white",
    "outfit": "black turtleneck",
    "props": "iPad with Apple logo",
    "theme": "minimalist, clean"
  },
  "market_context": {
    "change_pct": 5.2,
    "sentiment": "POSITIVE",
    "expression_type": "very_happy"
  },
  "prompt": "3D animated character render, Pixar movie style, cute anthropomorphic cat, fluffy fur texture, professional studio lighting, 4K resolution, vibrant colors, detailed facial features, silver-white fur, wearing black turtleneck, holding iPad with glowing Apple logo, very happy expression, wide grin, upward pointing graph, dollar signs in eyes, portrait front view, centered, soft glow effect",
  "prompt_length": 387,
  "nanobanana_params": {
    "model": "nanobanana-pro-v3",
    "style": "pixar-3d",
    "aspect_ratio": "9:16",
    "quality": "hd"
  },
  "estimated_generation_time_sec": 45,
  "fallback_used": false
}
```

## Examples

**Example 1**: NVDA +12% (극적 상승)
```
Input:
- Ticker: NVDA
- Change: +12.5%

Prompt:
"3D animated character, Pixar style, cute cat,
black fur with neon green stripes,
wearing leather jacket,
holding glowing GPU chip,
ecstatic expression, eyes sparkling, huge smile,
upward graph, coins flying, party confetti,
cyberpunk vibe, neon lighting,
portrait view"
```

**Example 2**: TSLA -8% (큰 하락)
```
Input:
- Ticker: TSLA
- Change: -8.2%

Prompt:
"3D animated character, Pixar style, cute cat,
white fur with red accents,
wearing space suit,
holding broken rocket,
crying heavily, tears streaming,
torn graph paper, despair,
dark shadowy background,
portrait view"
```

**Example 3**: Fallback (미등록 티커)
```
Input:
- Ticker: XYZ (not in database)
- Sector: Technology
- Change: +3%

Fallback Logic:
→ Use SECTOR_DEFAULTS['Technology']

Prompt:
"3D animated character, Pixar style, cute cat,
blue-gray fur,
wearing tech startup hoodie,
holding laptop,
satisfied smile, confident pose,
slight upward trend,
portrait view"
```

## Guidelines

### Do's ✅
- **티커 특성 강조**: 고유 identity 살리기
- **시장 감정 반영**: 표정과 포즈로 주가 표현
- **일관성**: 같은 티커는 항상 같은 기본 traits
- **고품질**: 4K, HDprompt 사용

### Don'ts ❌
- 너무 복잡한 prompt 금지 (500자 이내)
- 부정적/폭력적 이미지 금지
- 저작권 있는 캐릭터 직접 언급 금지
- 프롬프트에 ticker symbol 직접 포함 금지

## Integration

### NanoBanana PRO API

```python
import requests

async def generate_character_image(prompt: str) -> str:
    """Generate image using NanoBanana PRO"""
    
    api_key = os.getenv('NANOBANANA_API_KEY')
    
    response = requests.post(
        'https://api.nanobanana.ai/v1/generate',
        headers={'Authorization': f'Bearer {api_key}'},
        json={
            'prompt': prompt,
            'model': 'nanobanana-pro-v3',
            'style': 'pixar-3d',
            'aspect_ratio': '9:16',
            'quality': 'hd',
            'num_images': 1
        }
    )
    
    result = response.json()
    image_url = result['images'][0]['url']
    
    return image_url
```

### Database Storage

```sql
CREATE TABLE video_characters (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    animal_type VARCHAR(50) NOT NULL,
    fur_color VARCHAR(100),
    outfit VARCHAR(200),
    props VARCHAR(200),
    theme VARCHAR(200),
    base_prompt TEXT NOT NULL,
    
    image_url TEXT,
    last_generated_at TIMESTAMP,
    generation_count INT DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Performance Metrics

- **Prompt Generation Time**: < 1초
- **NanoBanana API Response**: 30-60초
- **Character Consistency**: 100% (같은 ticker = 같은 base traits)
- **Fallback Usage Rate**: < 20%

## Character Consistency Check

```python
def ensure_consistency(ticker: str, new_prompt: str, db: Session) -> bool:
    """Ensure character traits are consistent"""
    
    existing = db.query(VideoCharacter).filter_by(ticker=ticker).first()
    
    if existing:
        # Check if core traits match
        if not traits_match(existing.base_prompt, new_prompt):
            logger.warning(f"Inconsistent traits for {ticker}")
            return False
    
    return True
```

## Version History

- **v1.0** (2025-12-21): Initial release with 300+ ticker database
