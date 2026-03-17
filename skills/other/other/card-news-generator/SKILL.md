---
name: card-news-generator
description: Create 600x600 Instagram-style card news series automatically with optional background images. User provides topic, colors, and optional images - Claude generates content and creates multiple cards with proper text wrapping.
---

# Card News Generator - Auto Mode (V2)

Creates beautiful 600x600 card news series for social media with **background image support**. User can provide topic, colors, and optional background images - Claude handles content generation and multi-card creation automatically.

## When to Use

Use this skill when user requests:
- "카드 뉴스 만들어줘"
- "주제로 카드 시리즈 만들어줘"
- "인스타용 카드 생성해줘"
- Any request for visual card content

## Core Workflow - AUTO MODE

This is the PRIMARY workflow when users request card news:

### Step 1: Get Topic, Colors, and Optional Background Images from User

Ask user for:
- **Topic** (주제): What the card series is about
- **Background RGB** (배경색): e.g., `245,243,238` (optional, default: beige)
- **Background Images** (배경 이미지, 선택사항): Path to folder containing images

Example conversation (Solid Color):
```
Claude: 어떤 주제로 카드 뉴스를 만들까요?
User: Z세대의 특징에 대해서

Claude: 배경색을 선택해주세요 (RGB 형식, 예: 245,243,238)
추천 색상:
• 베이지: 245,243,238
• 핑크: 255,229,229
• 민트: 224,244,241
User: 245,243,238
```

Example conversation (With Background Images):
```
Claude: 어떤 주제로 카드 뉴스를 만들까요?
User: 여행 팁 5가지

Claude: 배경 이미지를 사용하시겠어요? (사용하려면 이미지 폴더 경로 입력)
User: /path/to/travel-images

Claude: 오버레이 불투명도를 선택하세요 (0.0-1.0, 기본값 0.5)
높을수록 어둡게 처리되어 텍스트가 더 잘 보입니다.
User: 0.6
```

### Step 2: Generate Card Content

Create 5-7 cards about the topic. Format output as:

```
1. [제목]
[설명 2-3줄]

2. [제목]
[설명 2-3줄]

3. [제목]
[설명 2-3줄]
```

**CRITICAL Content Guidelines:**
- **Title**: Maximum 20 characters (including spaces)
- **Content**: Maximum 60 characters (including spaces)
- Keep it concise to fit 600x600 canvas
- Use simple, impactful language
- Each card should convey ONE key point

### Step 3: Auto-Generate Cards

#### Option A: Solid Color Background

Use this command to create all cards with solid color background:

```bash
python auto_generator.py \
  --topic "Z세대의 특징" \
  --bg-color "#f5f3ee" \
  --text-color "#1a1a1a" \
  --output-dir /mnt/user-data/outputs \
  --base-filename "zgen" << 'EOF'
1. 디지털 네이티브
태어날 때부터
디지털 환경에 익숙

2. 개인화 중시
나만의 개성과
취향을 중요시

3. 소통 방식
텍스트보다 영상
이모티콘으로 감정 표현
EOF
```

#### Option B: Background Images (V2 Feature)

Use this command to create cards with background images:

```bash
python auto_generator.py \
  --topic "여행 팁" \
  --output-dir /mnt/user-data/outputs \
  --base-filename "travel" \
  --image-folder /path/to/travel-images \
  --overlay-opacity 0.6 << 'EOF'
1. 짐 싸기 팁
최소한의 짐으로
가볍게 여행하기

2. 현지 음식
맛집 찾는
나만의 방법

3. 교통 수단
대중교통 활용
팁과 노하우
EOF
```

**Important Notes:**
- Images in the folder must be sorted alphabetically/numerically (e.g., `01.jpg`, `02.jpg`, `03.jpg`)
- Image count should match card count
- If fewer images than cards, remaining cards will use solid color background
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`
- Text automatically changes to white when using background images

The script will automatically:
- Parse the numbered content
- Load background images from the folder (in sorted order)
- Apply dark overlay for better text visibility
- Create individual cards with proper text wrapping
- Save as `travel_01.png`, `travel_02.png`, etc.

### Step 4: Provide Download Links

After generation, show user:
```
✅ 카드 뉴스 5장이 생성되었습니다!

[View card 1](computer:///mnt/user-data/outputs/zgen_01.png)
[View card 2](computer:///mnt/user-data/outputs/zgen_02.png)
...
```

## RGB to Hex Conversion

Always convert RGB to hex for scripts:

```python
# RGB 245,243,238 → Hex #f5f3ee
hex_color = '#{:02x}{:02x}{:02x}'.format(245, 243, 238)
```

## Recommended Colors (RGB Format)

Show users these options:
- Warm beige: `245,243,238` → `#f5f3ee`
- Soft pink: `255,229,229` → `#ffe5e5`
- Mint green: `224,244,241` → `#e0f4f1`
- Lavender: `232,224,245` → `#e8e0f5`
- Peach: `255,232,214` → `#ffe8d6`
- Sky blue: `227,242,253` → `#e3f2fd`

## Content Generation Best Practices

### Good Card Content Example
```
1. 디지털 네이티브
태어날 때부터
디지털 환경에 익숙
```
✓ Title: 8 characters
✓ Content: 18 characters
✓ Clear and concise

### Bad Card Content Example
```
1. Z세대는 디지털 네이티브 세대입니다
그들은 태어날 때부터 스마트폰과 인터넷을 사용하며 자랐기 때문에 디지털 기술에 매우 능숙합니다
```
✗ Title too long (21 characters)
✗ Content too long (60+ characters)
✗ Will overflow the 600x600 canvas

## Single Card Mode (Manual)

### Solid Color Background

For creating just one card with solid color:

```bash
python generate_card.py \
  --title "제목" \
  --content "내용" \
  --bg-color "#f5f3ee" \
  --text-color "#1a1a1a" \
  --number 1 \
  --output /mnt/user-data/outputs/single.png
```

### With Background Image (V2 Feature)

For creating a card with background image:

```bash
python generate_card.py \
  --title "여행 팁" \
  --content "최소한의 짐으로\n가볍게 여행하기" \
  --bg-image /path/to/image.jpg \
  --overlay-opacity 0.6 \
  --number 1 \
  --output /mnt/user-data/outputs/travel_01.png
```

**Parameters:**
- `--bg-image`: Path to background image file
- `--overlay-opacity`: Opacity of dark overlay (0.0-1.0, default: 0.5)
  - 0.0 = No overlay (original image)
  - 0.5 = 50% dark overlay (default, good balance)
  - 1.0 = Fully black (only for very bright images)

## Technical Details

### Canvas Specifications
- Size: 600x600 pixels (Instagram-optimized)
- Padding: 40px on all sides
- Max text width: 520px (600 - 80)
- Font sizes:
  - Number badge: 60px
  - Title: 48px (bold)
  - Content: 28px (regular)

### Background Image Processing (V2)
- **Resize & Crop**: Images are automatically resized to 600x600px
  - Maintains aspect ratio
  - Center crop if aspect ratio differs
  - Uses high-quality LANCZOS resampling
- **Dark Overlay**: Applied to improve text visibility
  - Default opacity: 0.5 (50% dark)
  - Adjustable via `--overlay-opacity` (0.0-1.0)
  - Higher values = darker overlay = better text contrast
- **Text Color**: Automatically switches to white (#FFFFFF) when using background images
- **Supported Formats**: JPG, JPEG, PNG, WebP, BMP
- **Image Sorting**: Files loaded in alphabetical/numerical order

### Text Wrapping
- Automatic word wrapping at max width
- Preserves manual line breaks
- Centers all text horizontally
- Vertical spacing optimized for readability

### File Naming Convention
- Auto mode: `{base_filename}_{number:02d}.png`
- Example: `card_01.png`, `card_02.png`, `card_03.png`

## Error Handling

If text overflows:
- Reduce title length
- Shorten content
- Use line breaks strategically
- Regenerate with revised content

## Example Workflows

### Example 1: Solid Color Background

User request: "Z세대에 대한 카드 뉴스 5장 만들어줘, 핑크색으로"

Claude response:
1. Confirm: "Z세대 특징에 대한 카드 5장을 핑크 배경(255,229,229)으로 만들겠습니다."
2. Generate 5 cards content (keeping text concise)
3. Run auto_generator.py with heredoc
4. Provide download links to all 5 cards

Total time: ~30 seconds for 5-card series

### Example 2: Background Images (V2)

User request: "여행 팁 카드 뉴스 만들어줘, 배경은 /Users/me/travel-photos 폴더에 있는 이미지 사용"

Claude response:
1. Confirm: "여행 팁 카드 뉴스를 만들겠습니다. /Users/me/travel-photos 폴더의 이미지를 배경으로 사용합니다."
2. Ask: "오버레이 불투명도를 선택하세요 (0.0-1.0, 기본값 0.5). 높을수록 텍스트가 더 잘 보입니다."
3. User: "0.6"
4. Generate 5 cards content (keeping text concise)
5. Run auto_generator.py with --image-folder and --overlay-opacity
6. Provide download links showing cards with background images

**Preparation tips:**
- Rename images in order: `01.jpg`, `02.jpg`, `03.jpg`, `04.jpg`, `05.jpg`
- Ensure image count matches card count
- Use high-quality images (at least 600x600px recommended)
- Test with different overlay opacity values for best results

Total time: ~45 seconds for 5-card series with images
