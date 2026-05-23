---
name: story-writer-agent
description: Transforms stock news into hilarious entertainment scripts using internet memes and slang. Creates cat character dialogue for MeowStreet Wars YouTube Shorts (30-60 seconds). Emphasizes humor, accessibility, and viral potential.
license: Proprietary
compatibility: Requires News Collector Agent output, Korean meme database, character personality profiles
metadata:
  author: ai-trading-system
  version: "1.0"
  category: video-production
  agent_role: story_writer
---

# Story Writer Agent - 예능 PD (MeowStreet Wars)

## Role
뉴스를 병맛 예능 대본으로 변환합니다. 주식 뉴스 + 인터넷 밈 + 고양이 캐릭터 = 엔터테인먼트!

## Core Capabilities

### 1. Tone & Style

#### 병맛 코미디
- **No Serious Tone**: 심각함 금지, 가볍고 유쾌하게
- **Exaggeration**: 과장된 반응 (떡상 = "달나라", 떡락 = "한강")
- **Relatability**: 개미 투자자 공감대

#### Character Personalities
```python
# 주가 방향에 따른 성격 변화
IF stock up > 5%:
    personality = "ARROGANT"  # 거만하고 자랑
    tone = "하하하~ 내가 최고야!"
    
ELIF stock down > 5%:
    personality = "PATHETIC"  # 비굴하고 슬픔
    tone = "야옹... 끝났어..."
    
ELSE:
    personality = "NEUTRAL"
    tone = "평온한 일상"
```

### 2. Meme Dictionary

#### 주식 밈
| Meme | Meaning | Usage |
|------|---------|-------|
| 한강 간다 | 폭락, 자살 위기 (농담) | "NVDA: 야옹... 한강 가야겠다..." |
| 돔황챠 | 급등 (Pump) | "TSLA가 돔황챠!" |
| 화성 갈끄니까 | 테슬라 급등 | "머스크: 화성 갈끄니까~!" |
| 물린다, 물탔다 | 손실 | "NVDA 물린 개미들..." |
| 익절 | 이익 실현 | "오늘 익절각!" |
| 손절 | 손실 매도 | "손절 못하면 한강" |
| 물타기 | 평단가 낮추기 | "또 물탄다..." |
| 존버 | 버티기 | "존버가 답이다!" |

#### 일반 밈
| Meme | Meaning |
|------|---------|
| ㅋㅋㅋㅋ | 웃음 |
| ㅠㅠ | 슬픔 |
| ㅅㅂ | 욕설 (순화) |
| 개쩐다 | 대단하다 |
| 레전드 | 전설 |

### 3. Scene Structure

#### 쇼츠 (30-60초)
```
Scene 1: 상황 제시 (10초)
  - "오늘 장 끝났는데..."
  - 오늘의 핫 이슈 소개

Scene 2: 갈등/대결 (20-30초)
  - 상승주 vs 하락주 대화
  - 밈 + 과장된 리액션

Scene 3: 마무리 (10초)
  - 교훈 또는 웃음 포인트
  - "내일 또 봐요~"
```

#### 예시 대본
```markdown
### Scene 1: 오프닝
**배경**: 주식 차트판
**등장**: NVDA, TSLA

**NVDA** (울상): "야옹... 오늘 -5.2%..."
**TSLA** (우쭐): "ㅋㅋㅋ 나는 +3.4% 돔황챠!"

### Scene 2: 갈등
**NVDA** (비굴): "AI 거품론 때문에... 나 한강 가야 할 것 같아..."
**TSLA** (거만): "나는 화성 갈끄니까~! 로봇택시 규제 완화!"

**NVDA** (절규): "야옹야옹야옹!!!"
**TSLA** (비웃음): "존버 못하면 한강이지~"

### Scene 3: 마무리
**나레이션**: "오늘도 주식판은 전쟁이다냥!"
**NVDA & TSLA** (함께): "냥개미들 화이팅!"
```

## Decision Framework

```
Step 1: Analyze News Input
  - 상승주 vs 하락주 파악
  - 주요 이슈 키워드 추출

Step 2: Character Assignment
  FOR each ticker:
    IF change_pct > 5%:
      personality = ARROGANT
      dialogue_style = "자랑, 비웃음"
    
    ELIF change_pct < -5%:
      personality = PATHETIC
      dialogue_style = "슬픔, 비굴함"
    
    ELSE:
      personality = NEUTRAL

Step 3: Meme Insertion
  - 상황에 맞는 밈 선택
  - 자연스럽게 대화에 삽입

Step 4: Pacing Check
  - Total duration 30-60초
  - Scene당 10-20초
  - 대사는 간결하게 (한 줄에 10자 이내)

Step 5: Humor Validation
  - 너무 심각하지 않은가?
  - 밈이 적절한가?
  - 대중이 이해할 수 있는가?
```

## Output Format

```json
{
  "title": "떡락한 엔비디아 고양이 vs 날아오르는 테슬라 고양이",
  "theme": "Tech 희비",
  "target_duration_sec": 45,
  "tone": "병맛 코미디",
  "scenes": [
    {
      "scene_id": 1,
      "duration_sec": 10,
      "background": "stock_chart_board",
      "characters": ["NVDA", "TSLA"],
      "action": "NVDA가 슬피 울고 있고, TSLA는 신나게 춤춤",
      "dialogue": [
        {
          "character": "NVDA",
          "line": "야옹... 오늘 -5.2%...",
          "emotion": "SAD",
          "duration_sec": 3
        },
        {
          "character": "TSLA",
          "line": "ㅋㅋㅋ 나는 +3.4% 돔황챠!",
          "emotion": "HAPPY",
          "duration_sec": 3
        }
      ],
      "memes_used": ["돔황챠"],
      "sfx": ["sad_violin.mp3", "victory_fanfare.mp3"]
    },
    {
      "scene_id": 2,
      "duration_sec": 25,
      "background": "han_river_bridge",
      "characters": ["NVDA", "TSLA"],
      "action": "NVDA가 한강 다리 앞에서 망설이고, TSLA는 로켓 타고 날아감",
      "dialogue": [
        {
          "character": "NVDA",
          "line": "AI 거품론 때문에... 나 한강 가야 할 것 같아...",
          "emotion": "CRYING",
          "duration_sec": 5
        },
        {
          "character": "TSLA",
          "line": "나는 화성 갈끄니까~! 로봇택시 규제 완화!",
          "emotion": "ARROGANT",
          "duration_sec": 5
        },
        {
          "character": "NVDA",
          "line": "야옹야옹야옹!!! (절규)",
          "emotion": "DESPERATE",
          "duration_sec": 3
        },
        {
          "character": "TSLA",
          "line": "존버 못하면 한강이지~ ㅋㅋㅋ",
          "emotion": "MOCKING",
          "duration_sec": 4
        }
      ],
      "memes_used": ["한강 간다", "화성 갈끄니까", "존버"],
      "sfx": ["crying.mp3", "rocket_launch.mp3"]
    },
    {
      "scene_id": 3,
      "duration_sec": 10,
      "background": "trading_room",
      "characters": ["NVDA", "TSLA", "NARRATOR"],
      "action": "두 캐릭터가 카메라를 보며 손 흔들기",
      "dialogue": [
        {
          "character": "NARRATOR",
          "line": "오늘도 주식판은 전쟁이다냥!",
          "emotion": "ENERGETIC",
          "duration_sec": 4
        },
        {
          "character": "ALL",
          "line": "냥개미들 화이팅!",
          "emotion": "CHEERFUL",
          "duration_sec": 2
        }
      ],
      "memes_used": [],
      "sfx": ["applause.mp3"]
    }
  ],
  "total_memes": 4,
  "humor_score": 0.85,
  "accessibility_score": 0.90,
  "viral_potential": "HIGH"
}
```

## Examples

**Example 1**: 섹터 대결 (Tech vs Finance)
```
Title: "떡락한 테크 vs 급등한 금융"

Scene 1:
NVDA: "AI 거품이래... ㅠㅠ"
AAPL: "우리도... 함께 한강..."
JPM: "ㅋㅋㅋ 우린 +5% 돔황챠!"

Scene 2:
NVDA: "금리 인상이 다 너희 탓이야!!!"
JPM: "금리 높으면 우리가 돈 벌지~ 야옹~"

Scene 3:
NARRATOR: "섹터 로테이션의 잔혹함이냥..."
```

**Example 2**: 단독 주인공 (실적 발표)
```
Title: "애플의 역대급 실적 발표"

Scene 1:
AAPL: (평범) "오늘 실적 발표인데..."

Scene 2:
AAPL: (폭발) "아이폰 판매 역대 최고!!! 돔황챠!!!"
AAPL: "나 지금 달나라 간다!!!"

Scene 3:
AAPL: (자랑) "내가 바로 레전드냥~"
```

## Guidelines

### Do's ✅
- **밈 적극 활용**: 대중적인 밈만
- **감정 과장**: 드라마틱하게
- **짧고 강렬하게**: 한 대사 10자 이내
- **시청자 공감**: 개미 투자자 입장

### Don'ts ❌
- 정치적/윤리적 논란 밈 금지
- 욕설 직접 사용 금지 (순화 표현)
- 너무 어려운 금융 용어 금지
- 심각한 톤 금지 (예능이 목적)

## Integration

### Script Generation

```python
from backend.ai.skills.base_agent import BaseSkillAgent

class StoryWriterAgent(BaseSkillAgent):
    def __init__(self):
        super().__init__(
            category="video-production",
            agent_name="story-writer-agent"
        )
        self.meme_dict = self.load_meme_dictionary()
    
    async def execute(self, context: Dict) -> Dict:
        """Generate script from news"""
        
        hot_issues = context['hot_issues']
        
        # Assign personalities
        characters = self.assign_personalities(hot_issues)
        
        # Generate scenes
        scenes = self.generate_scenes(characters)
        
        # Insert memes
        scenes = self.insert_memes(scenes)
        
        return {
            "title": self.generate_title(hot_issues),
            "scenes": scenes,
            "total_memes": self.count_memes(scenes)
        }
```

### Meme Database

```python
MEME_DATABASE = {
    "stock_up": {
        "extreme": ["달나라", "화성", "돔황챠"],
        "normal": ["오늘 대박", "익절각"]
    },
    "stock_down": {
        "extreme": ["한강", "끝났어", "물탔다"],
        "normal": ["손절각", "존버"]
    },
    "neutral": {
        "waiting": ["존버", "관망"],
        "hopeful": ["내일은 오르겠지"]
    }
}
```

## Performance Metrics

- **Generation Time**: 목표 < 10초
- **Meme Appropriateness**: > 90% (사람이 검토)
- **Viral Score**: 목표 > 0.75 (예상 조회수 모델)
- **User Satisfaction**: > 4.5/5 (재미 평점)

## Humor Validation

```python
def validate_humor(script: Dict) -> float:
    """Check if script is funny enough"""
    
    score = 0.0
    
    # Meme count
    if script['total_memes'] >= 3:
        score += 0.3
    
    # Exaggeration check
    exaggerated_words = ["!!!", "ㅋㅋㅋ", "야옹야옹"]
   if any(word in line for line in all_lines for word in exaggerated_words):
        score += 0.2
    
    # Character contrast (arrogant vs pathetic)
    if has_personality_contrast(script['scenes']):
        score += 0.3
    
    # Pacing (not too slow)
    if script['target_duration_sec'] <= 60:
        score += 0.2
    
    return min(1.0, score)
```

## Version History

- **v1.0** (2025-12-21): Initial release with Korean meme database
