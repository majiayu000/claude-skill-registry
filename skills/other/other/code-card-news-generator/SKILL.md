---
name: code-card-news-generator
description: Generate code explanation cards with syntax highlighting for tutorials and education. Creates title cards and explanation cards with Korean descriptions and code examples.
---

# Code Card News Generator

코드 설명용 카드 뉴스를 생성하는 스킬입니다. 제목 카드와 함수/개념 설명 카드를 자동으로 만듭니다.

## When to Use

Use this skill when user requests:
- "코드 설명 카드 만들어줘"
- "React Hook 설명 카드 생성해줘"
- "코드 튜토리얼 카드 뉴스 만들어줘"
- Any request for code tutorial/explanation cards

## Core Workflow

### Step 1: Get Topic and Content from User

Ask user for:
- **Topic** (주제): What library/framework/concept (e.g., "React Router Hooks")
- **Functions/Concepts**: List of items to explain (e.g., "useNavigate, useParams, useLocation")

Example conversation:
```
Claude: 어떤 주제로 코드 카드를 만들까요?
User: React Router Hooks

Claude: 어떤 Hook들을 설명할까요?
User: useNavigate, useParams, useLocation
```

### Step 2: Generate Content

For each function/concept, create:
1. **Description** (한국어 설명): Brief explanation in Korean/English
2. **Code Example**: Working code snippet
3. **Explanation**: What the code does

Example:
```
1. useNavigate
Description: It's used for programmatic navigation, allowing you to redirect users or change routes without needing to render a <Link> component.
Code:
const navigate = useNavigate();

const handleClick = () => {
  navigate('/home');
};
Explanation: In this example, calling handleClick will navigate the user to the /home route.
```

### Step 3: Auto-Generate Cards

Use this command:

```bash
python3 auto_code_generator.py \
  --topic "React Router Hooks" \
  --output-dir ./output \
  --base-filename "react_router" << 'EOF'
TITLE: React|Router|Hooks

1. useNavigate
Description: It's used for programmatic navigation, allowing you to redirect users or change routes without needing to render a <Link> component.
Code:
const navigate = useNavigate();

const handleClick = () => {
  navigate('/home');
};
Explanation: In this example, calling handleClick will navigate the user to the /home route.

2. useParams
Description: useParams is used to access dynamic parameters from the current URL.
Code:
const { id } = useParams();

console.log(id); // Outputs the 'id' from URL
Explanation: If the route is /user/:id and you visit /user/123, useParams will return { id: '123' }.
EOF
```

The script will generate:
- `react_router_00_title.png` - Title card
- `react_router_01.png` - useNavigate explanation
- `react_router_02.png` - useParams explanation

### Step 4: Provide Download Links

After generation, show user:
```
✅ 코드 카드 3장이 생성되었습니다!

[View title card](computer:///path/to/react_router_00_title.png)
[View card 1](computer:///path/to/react_router_01.png)
[View card 2](computer:///path/to/react_router_02.png)
```

## Input Format

### Title Card

```
TITLE: Part1|Part2|Part3
```

Parts separated by `|` will alternate colors (white/pink). Example:
- `React|Router|Hooks` → "React" (white), "Router" (pink), "Hooks" (white)

Optional subtitle:
```
TITLE: React|Router|Hooks
SUBTITLE: Navigation Made Easy
```

### Explanation Cards

```
1. functionName
Description: Korean or English description...
Code:
code line 1
code line 2
code line 3
Explanation: Additional explanation about what the code does...

2. nextFunction
Description: ...
Code:
...
Explanation: ...
```

**Important:**
- Each card starts with a number (1., 2., etc.)
- `Description:` - The main explanation
- `Code:` - Code example (starts on next line)
- `Explanation:` - Optional additional context

## Design Specifications

### Colors
- Background: `#1a1a1a` (Dark)
- Text: `#ffffff` (White)
- Accent: `#ff6b9d` (Pink)
- Code Background: `#2d2d2d`
- Code Border: `#ff6b9d` (Pink)

### Canvas
- Size: 1080x1080 pixels (Instagram optimized)
- Padding: 60px

### Fonts
- General Text: Cafe24Ssurround (bundled)
- Code: Menlo/Monaco (monospace, system font)

### Layout
- Title Card: Large centered title with optional subtitle
- Explanation Card:
  - Number + Function name (top, pink)
  - Description (white)
  - Code box (pink border, dark background)
  - Explanation (white, with pink highlights)

## Content Guidelines

### Good Code Example
```
1. useState
Description: useState is a Hook that lets you add state to functional components.
Code:
const [count, setCount] = useState(0);

setCount(count + 1);
Explanation: This creates a state variable 'count' with initial value 0.
```
✓ Clear function name
✓ Concise description
✓ Simple, working code
✓ Helpful explanation

### Bad Code Example
```
1. This is a very long function name that explains everything
Description: This is a very long description that goes on and on explaining every single detail about how this function works in various scenarios and edge cases...
Code:
// 50 lines of complex code
...
```
✗ Too verbose
✗ Code too long/complex
✗ Won't fit in 1080x1080 canvas

## Manual Single Card Creation

### Create Title Card Only

```bash
python3 generate_code_card.py title \
  --title "React|Router|Hooks" \
  --subtitle "Navigation Made Easy" \
  --output ./title.png
```

### Create Explanation Card Only

```bash
python3 generate_code_card.py explain \
  --number "1" \
  --function "useNavigate" \
  --description "It's used for programmatic navigation..." \
  --code "const navigate = useNavigate();" \
  --explanation "This allows navigation without Link component." \
  --output ./card_01.png
```

## Example Topics

- React Hooks (useState, useEffect, useContext)
- React Router Hooks (useNavigate, useParams, useLocation)
- Array Methods (map, filter, reduce)
- Python Built-ins (enumerate, zip, lambda)
- CSS Flexbox (flex-direction, justify-content, align-items)
- Git Commands (commit, push, pull, merge)

## Tips for Good Cards

1. **Keep It Simple**: One concept per card
2. **Code Length**: Max 5-7 lines of code
3. **Use Comments**: Add helpful comments in code
4. **Highlight Keywords**: Important terms will be auto-highlighted
5. **Test Code**: Make sure code examples actually work

## Error Handling

If text overflows:
- Shorten description
- Reduce code lines
- Simplify explanation
- Use more concise language

## Example Workflow

User request: "React Router Hooks 설명 카드 3개 만들어줘"

Claude response:
1. Confirm: "React Router Hooks에 대한 코드 카드를 만들겠습니다. useNavigate, useParams, useLocation을 설명하겠습니다."
2. Generate content for 3 hooks
3. Run auto_code_generator.py with heredoc
4. Provide download links

Total time: ~1 minute for 4-card series (1 title + 3 explanations)
