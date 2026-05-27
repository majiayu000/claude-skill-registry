---
name: director-agent
description: Final video assembly coordinator. Matches scripts with character images, orchestrates scene transitions, timing, effects, and creates rendering-ready storyboard JSON for HeyGen/Pika/D-ID video generation platforms.
license: Proprietary
compatibility: Requires Story Writer and Character Designer outputs, video rendering API
metadata:
  author: ai-trading-system
  version: "1.0"
  category: video-production
  agent_role: director
---

# Director Agent - 영상 감독 (MeowStreet Wars)

## Role
대본 + 캐릭터 이미지 + 효과 → 최종 Storyboard.json 생성. 렌더링 엔진에 바로 투입 가능한 완성품!

## Core Capabilities

### 1. Final Assembly

#### Components Integration
```python
# Input from other agents
script = StoryWriterAgent.output  # 대본
characters = CharacterDesignerAgent.output  # 캐릭터 이미지
news_context = NewsCollectorAgent.output  # 뉴스 컨텍스트

# Assembly
storyboard = assemble_storyboard(script, characters, news_context)
```

#### Quality Checks
- **Duration**: 총 길이 30-60초 이내
- **Scene Count**: 쇼츠 기준 2-4개
- **Character Availability**: 모든 캐릭터 이미지 생성 완료
- **Dialogue Sync**: 대사 길이와 duration 매칭

### 2. Scene Composition

#### Layout Templates

**Template 1: Debate (1:1 대결)**
```json
{
  "layout": "split_screen",
  "character_positions": {
    "left": {"ticker": "NVDA", "size": "50%", "align": "center"},
    "right": {"ticker": "TSLA", "size": "50%", "align": "center"}
  },
  "camera": "medium_shot"
}
```

**Template 2: Celebration/Crying (솔로)**
```json
{
  "layout": "full_screen",
  "character_positions": {
    "center": {"ticker": "AAPL", "size": "80%", "align": "center"}
  },
  "camera": "closeup"
}
```

**Template 3: Group (3개 이상)**
```json
{
  "layout": "grid",
  "character_positions": {
    "top_left": {"ticker": "AAPL", "size": "33%"},
    "top_right": {"ticker": "MSFT", "size": "33%"},
    "bottom_center": {"ticker": "GOOGL", "size": "33%"}
  },
  "camera": "wide_shot"
}
```

### 3. Timing & Pacing

```python
def calculate_scene_timing(dialogue: List[Dict]) -> float:
    """Calculate scene duration based on dialogue"""
    
    total_duration = 0
    
    for line in dialogue:
        # Korean: ~2 characters per second
        # English: ~3 words per second
        text_length = len(line['text'])
        
        if is_korean(line['text']):
            duration = text_length / 2
        else:
            duration = len(line['text'].split()) / 3
        
        # Add reading buffer (20%)
        duration *= 1.2
        
        # Add emotion pause
        if line['emotion'] in ['CRYING', 'DESPERATE']:
            duration += 1.0  # Extra pause for effect
        
        total_duration += duration
    
    return total_duration
```

### 4. Effects & Transitions

#### Visual Effects
```python
EFFECTS_LIBRARY = {
    "price_up": {
        "particles": "coins_falling",
        "overlay": "green_upward_arrow",
        "glow": "success_aura"
    },
    "price_down": {
        "particles": "tears_dropping",
        "overlay": "red_downward_arrow",
        "background": "dark_vignette"
    },
    "neutral": {
        "overlay": "stock_ticker_banner"
    }
}
```

#### Transitions
```python
TRANSITIONS = {
    "cut": {"duration": 0},  # Instant
    "fade": {"duration": 0.5},
    "slide": {"duration": 0.3, "direction": "left"},
    "zoom": {"duration": 0.4}
}
```

#### Sound Effects (SFX)
```python
SFX_LIBRARY = {
    "happy": ["success_fanfare.mp3", "coins_clinking.mp3"],
    "sad": ["sad_violin.mp3", "crying.mp3"],
    "action": ["whoosh.mp3", "impact.mp3"],
    "transition": ["page_turn.mp3"]
}
```

### 5. Background Assets

```python
BACKGROUNDS = {
    "stock_chart_board": "assets/backgrounds/trading_floor.png",
    "han_river_bridge": "assets/backgrounds/han_river.png",
    "moon": "assets/backgrounds/to_the_moon.png",
    "trading_room": "assets/backgrounds/war_room.png",
    "generic": "assets/backgrounds/gradient_blue.png"
}
```

## Decision Framework

```
Step 1: Validate Inputs
  - Script 존재 확인
  - 모든 character images 준비 확인
  - News context 유효성 확인

Step 2: Scene Assembly
  FOR each scene in script:
    - Match characters to images
    - Calculate timing
    - Select layout template
    - Add effects based on sentiment

Step 3: Timing Optimization
  total_duration = sum(scene_durations)
  
  IF total_duration > 60:
    → Compress scenes (remove pauses)
  
  IF total_duration < 30:
    → Add pauses or intro/outro

Step 4: Quality Check
  - All images loaded?
  - Dialogue within time limits?
  - Transitions smooth?
  - Effects appropriate?

Step 5: Generate Storyboard JSON
  storyboard = {
    "title": ...,
    "scenes": [...],
    "total_duration": ...,
    "assets": {...}
  }

Step 6: Rendering Metadata
  Add platform-specific parameters:
    - HeyGen: avatar_id, voice_id
    - Pika: style_preset, motion_settings
    - D-ID: presenter_id, driver_settings
```

## Output Format

```json
{
  "title": "떡락한 엔비디아 vs 날아오르는 테슬라",
  "description": "Tech 섹터의 희비가 엇갈리는 하루",
  "aspect_ratio": "9:16",
  "target_platform": "youtube_shorts",
  "total_duration_sec": 45,
  "frame_rate": 30,
  "resolution": "1080x1920",
  
  "metadata": {
    "date": "2025-12-21",
    "tickers": ["NVDA", "TSLA"],
    "theme": "sector_rotation",
    "humor_level": "high"
  },
  
  "assets": {
    "characters": {
      "NVDA": {
        "image_url": "https://cdn.example.com/nvda_sad.png",
        "voice_id": "korean_male_01"
      },
      "TSLA": {
        "image_url": "https://cdn.example.com/tsla_happy.png",
        "voice_id": "korean_male_02"
      }
    },
    "backgrounds": {
      "stock_board": "assets/backgrounds/trading_floor.png",
      "han_river": "assets/backgrounds/han_river.png"
    },
    "sfx": {
      "sad_violin": "assets/sfx/sad_violin.mp3",
      "success_fanfare": "assets/sfx/fanfare.mp3"
    }
  },
  
  "scenes": [
    {
      "scene_id": 1,
      "duration_sec": 10,
      "start_time": 0,
      "end_time": 10,
      
      "background": {
        "type": "image",
        "src": "assets/backgrounds/trading_floor.png",
        "filter": "none"
      },
      
      "layout": "split_screen",
      
      "characters": [
        {
          "ticker": "NVDA",
          "image_url": "https://cdn.example.com/nvda_sad.png",
          "position": "left",
          "size": "50%",
          "animation": "fade_in",
          "animation_duration": 0.5
        },
        {
          "ticker": "TSLA",
          "image_url": "https://cdn.example.com/tsla_happy.png",
          "position": "right",
          "size": "50%",
          "animation": "fade_in",
          "animation_duration": 0.5
        }
      ],
      
      "dialogue": [
        {
          "character": "NVDA",
          "text": "야옹... 오늘 -5.2%...",
          "emotion": "SAD",
          "voice_id": "korean_male_01",
          "start_time": 1.0,
          "duration": 3.0,
          "volume": 0.8
        },
        {
          "character": "TSLA",
          "text": "ㅋㅋㅋ 나는 +3.4% 돔황챠!",
          "emotion": "HAPPY",
          "voice_id": "korean_male_02",
          "start_time": 4.5,
          "duration": 3.0,
          "volume": 0.9
        }
      ],
      
      "effects": [
        {
          "type": "text_overlay",
          "text": "NVDA -5.2%",
          "position": "bottom_left",
          "color": "#FF0000",
          "font_size": 24,
          "animation": "slide_in_down",
          "start_time": 1.0,
          "duration": 2.0
        },
        {
          "type": "text_overlay",
          "text": "TSLA +3.4%",
          "position": "bottom_right",
          "color": "#00FF00",
          "font_size": 24,
          "animation": "slide_in_down",
          "start_time": 4.5,
          "duration": 2.0
        },
        {
          "type": "particle",
          "name": "sad_rain",
          "target": "NVDA",
          "start_time": 1.0,
          "duration": 8.0
        },
        {
          "type": "particle",
          "name": "confetti",
          "target": "TSLA",
          "start_time": 4.5,
          "duration": 5.0
        }
      ],
      
      "sfx": [
        {
          "file": "assets/sfx/sad_violin.mp3",
          "start_time": 1.0,
          "duration": 3.0,
          "volume": 0.3
        },
        {
          "file": "assets/sfx/success_fanfare.mp3",
          "start_time": 4.5,
          "duration": 2.0,
          "volume": 0.5
        }
      ],
      
      "transition_out": {
        "type": "fade",
        "duration": 0.5
      }
    },
    
    {
      "scene_id": 2,
      "duration_sec": 25,
      "start_time": 10,
      "end_time": 35,
      
      "background": {
        "type": "image",
        "src": "assets/backgrounds/han_river.png",
        "filter": "dark_overlay"
      },
      
      "layout": "full_screen_duet",
      
      "characters": [
        {
          "ticker": "NVDA",
          "image_url": "https://cdn.example.com/nvda_crying.png",
          "position": "left",
          "size": "60%",
          "animation": "shake"
        },
        {
          "ticker": "TSLA",
          "image_url": "https://cdn.example.com/tsla_flying.png",
          "position": "top_right",
          "size": "40%",
          "animation": "float_up"
        }
      ],
      
      "dialogue": [
        {
          "character": "NVDA",
          "text": "AI 거품론 때문에... 나 한강 가야 할 것 같아...",
          "emotion": "CRYING",
          "voice_id": "korean_male_01",
          "start_time": 11.0,
          "duration": 5.0
        },
        {
          "character": "TSLA",
          "text": "나는 화성 갈끄니까~! 로봇택시 규제 완화!",
          "emotion": "ARROGANT",
          "voice_id": "korean_male_02",
          "start_time": 17.0,
          "duration": 5.0
        },
        {
          "character": "NVDA",
          "text": "야옹야옹야옹!!!",
          "emotion": "DESPERATE",
          "voice_id": "korean_male_01",
          "start_time": 23.0,
          "duration": 3.0
        },
        {
          "character": "TSLA",
          "text": "존버 못하면 한강이지~ ㅋㅋㅋ",
          "emotion": "MOCKING",
          "voice_id": "korean_male_02",
          "start_time": 27.0,
          "duration": 4.0
        }
      ],
      
      "effects": [
        {
          "type": "overlay",
          "name": "rain",
          "opacity": 0.5,
          "start_time": 10,
          "duration": 25
        },
        {
          "type": "text_overlay",
          "text": "한강 다리",
          "position": "top_center",
          "font_size": 18,
          "start_time": 11,
          "duration": 3
        },
        {
          "type": "particle",
          "name": "rocket_trail",
          "target": "TSLA",
          "start_time": 17,
          "duration": 8
        }
      ],
      
      "sfx": [
        {
          "file": "assets/sfx/crying.mp3",
          "start_time": 11,
          "duration": 12,
          "volume": 0.4
        },
        {
          "file": "assets/sfx/rocket_launch.mp3",
          "start_time": 17,
          "duration": 3,
          "volume": 0.6
        }
      ],
      
      "transition_out": {
        "type": "zoom",
        "duration": 0.4
      }
    },
    
    {
      "scene_id": 3,
      "duration_sec": 10,
      "start_time": 35,
      "end_time": 45,
      
      "background": {
        "type": "image",
        "src": "assets/backgrounds/war_room.png",
        "filter": "none"
      },
      
      "layout": "centered",
      
      "characters": [
        {
          "ticker": "BOTH",
          "image_url": "https://cdn.example.com/group_waving.png",
          "position": "center",
          "size": "70%",
          "animation": "wave"
        }
      ],
      
      "dialogue": [
        {
          "character": "NARRATOR",
          "text": "오늘도 주식판은 전쟁이다냥!",
          "emotion": "ENERGETIC",
          "voice_id": "korean_narrator",
          "start_time": 36,
          "duration": 4
        },
        {
          "character": "ALL",
          "text": "냥개미들 화이팅!",
          "emotion": "CHEERFUL",
          "voice_id": "korean_chorus",
          "start_time": 41,
          "duration": 2
        }
      ],
      
      "effects": [
        {
          "type": "text_overlay",
          "text": "다음 영상도 기대하세냥~!",
          "position": "bottom_center",
          "font_size": 20,
          "color": "#FFFF00",
          "start_time": 41,
          "duration": 3
        }
      ],
      
      "sfx": [
        {
          "file": "assets/sfx/applause.mp3",
          "start_time": 41,
          "duration": 4,
          "volume": 0.5
        }
      ],
      
      "transition_out": {
        "type": "fade_to_black",
        "duration": 1.0
      }
    }
  ],
  
  "rendering_config": {
    "engine": "heygen",
    "voice_synthesis": "elevenlabs",
    "music_track": "assets/music/upbeat_bg.mp3",
    "music_volume": 0.2,
    "export_format": "mp4",
    "bitrate": "8000k"
  }
}
```

## Guidelines

### Do's ✅
- **Timing 정확**: 대사와 duration 완벽 매칭
- **효과 적절**: 과하지 않게, 내용 보완용
- **전환 부드럽게**: Jarring한 cut 최소화
- **품질 체크**: 모든 asset 로드 확인

### Don'ts ❌
- 60초 초과 금지 (쇼츠 기준)
- 너무 많은 효과 금지 (집중도 하락)
- 대사 겹침 금지
- 미완성 scene 포함 금지

## Integration

### Rendering Platform APIs

#### HeyGen
```python
import requests

async def render_with_heygen(storyboard: Dict) -> str:
    """Render video using HeyGen API"""
    
    api_key = os.getenv('HEYGEN_API_KEY')
    
    response = requests.post(
        'https://api.heygen.com/v1/video/generate',
        headers={'X-Api-Key': api_key},
        json={
            'title': storyboard['title'],
            'scenes': convert_to_heygen_format(storyboard['scenes']),
            'aspect_ratio': storyboard['aspect_ratio']
        }
    )
    
    video_id = response.json()['video_id']
    
    # Poll for completion
    video_url = await wait_for_video(video_id)
    
    return video_url
```

## Performance Metrics

- **Assembly Time**: < 5초
- **Storyboard Validation**: 100% (모든 필수 필드)
- **Rendering Success Rate**: > 95%
- **Average Video Generation Time**: 2-5분 (platform dependent)

## Version History

- **v1.0** (2025-12-21): Initial release with HeyGen/Pika integration
