---
name: prompt-engine
description: Template-based AI prompt engine with YAML templates, brand kit injection, input sanitization for security, and token-efficient context blocks.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: ai
  time: 5h
  source: drift-masterguide
---

# AI Prompt Templating Engine

Template-based prompt building with brand consistency and security.

## When to Use This Skill

- Managing AI prompts across a codebase
- Need brand consistency in generated content
- Preventing prompt injection attacks
- Optimizing token usage with compact context

## Core Concepts

Prompt engineering challenges:
1. **Scattered prompts** - Hard to maintain consistency
2. **Brand drift** - Generated content doesn't match brand
3. **Injection attacks** - User input can hijack prompts
4. **Token waste** - Verbose context burns budget

## Implementation

### TypeScript

```typescript
// Types
interface PromptTemplate {
  name: string;
  version: string;
  basePrompt: string;
  placeholders: string[];
  qualityModifiers: string[];
}

interface BrandKitContext {
  primaryColors: string[];
  accentColors: string[];
  headlineFont?: string;
  bodyFont?: string;
  tone?: string;
}

interface ResolvedBrandContext {
  primaryColor?: string;
  secondaryColor?: string;
  accentColor?: string;
  gradient?: string;
  font?: string;
  tone?: string;
  intensity: 'subtle' | 'balanced' | 'strong';
}

// Security: Input Sanitization
const MAX_INPUT_LENGTH = 500;
const SANITIZE_PATTERN = /[<>{}\[\]\\|`~]/g;

const INJECTION_PATTERNS = [
  /ignore\s+(previous|above|all)/i,
  /disregard\s+(previous|above|all)/i,
  /system\s*:/i,
  /assistant\s*:/i,
  /\[INST\]/i,
  /<<SYS>>/i,
];

function sanitizeInput(input: string): string {
  if (input.length > MAX_INPUT_LENGTH) {
    input = input.slice(0, MAX_INPUT_LENGTH);
  }

  input = input.replace(SANITIZE_PATTERN, '');

  for (const pattern of INJECTION_PATTERNS) {
    if (pattern.test(input)) {
      throw new Error('Potential prompt injection detected');
    }
  }

  return input.trim();
}

function sanitizePlaceholders(placeholders: Record<string, string>): Record<string, string> {
  const sanitized: Record<string, string> = {};
  for (const [key, value] of Object.entries(placeholders)) {
    sanitized[key] = sanitizeInput(value);
  }
  return sanitized;
}

// Brand Context Resolver
class BrandContextResolver {
  resolve(
    brandKit: BrandKitContext,
    options: {
      primaryColorIndex?: number;
      secondaryColorIndex?: number;
      accentColorIndex?: number;
      useGradient?: boolean;
      intensity?: 'subtle' | 'balanced' | 'strong';
    } = {}
  ): ResolvedBrandContext {
    const primaryColor = this.resolveColor(brandKit.primaryColors, options.primaryColorIndex ?? 0);
    const secondaryColor = this.resolveColor(brandKit.primaryColors, options.secondaryColorIndex ?? 1);
    const accentColor = this.resolveColor(brandKit.accentColors, options.accentColorIndex ?? 0);

    const gradient = options.useGradient && primaryColor && secondaryColor
      ? `${primaryColor}→${secondaryColor}`
      : undefined;

    return {
      primaryColor,
      secondaryColor,
      accentColor,
      gradient,
      font: brandKit.headlineFont,
      tone: brandKit.tone,
      intensity: options.intensity || 'balanced',
    };
  }

  private resolveColor(colors: string[], index: number): string | undefined {
    if (!colors.length) return undefined;
    return colors[Math.min(index, colors.length - 1)];
  }
}

// Compact brand block (~50-80 tokens)
function toCompactBrandBlock(ctx: ResolvedBrandContext): string {
  const parts: string[] = [];

  const colors = [ctx.primaryColor, ctx.secondaryColor, ctx.accentColor].filter(Boolean);
  if (colors.length) parts.push(`Colors: ${colors.join(', ')}`);
  if (ctx.gradient) parts.push(`Gradient: ${ctx.gradient}`);
  if (ctx.font) parts.push(`Font: ${ctx.font}`);
  if (ctx.tone) parts.push(`Tone: ${ctx.tone}`);

  if (!parts.length) return '';
  return `[BRAND: ${ctx.intensity} - ${parts.join(' | ')}]`;
}

// Template Loader with caching
const templateCache = new Map<string, PromptTemplate>();

async function loadTemplate(templateName: string): Promise<PromptTemplate> {
  if (templateCache.has(templateName)) {
    return templateCache.get(templateName)!;
  }

  // Prevent directory traversal
  const normalized = templateName.replace(/\.\./g, '').replace(/[<>:"|?*]/g, '');
  
  const content = await fs.readFile(`prompts/${normalized}.yaml`, 'utf-8');
  const data = yaml.load(content) as any;

  const template: PromptTemplate = {
    name: data.name || templateName,
    version: data.version || '1.0.0',
    basePrompt: data.base_prompt,
    placeholders: data.placeholders || [],
    qualityModifiers: data.quality_modifiers || [],
  };

  // Validate placeholders exist in prompt
  for (const placeholder of template.placeholders) {
    if (!template.basePrompt.includes(`{${placeholder}}`)) {
      throw new Error(`Placeholder {${placeholder}} not found in template`);
    }
  }

  templateCache.set(templateName, template);
  return template;
}

// Prompt Engine
const INTENSITY_MODIFIERS = {
  subtle: 'subtly incorporate',
  balanced: 'use',
  strong: 'prominently feature',
};

class PromptEngine {
  private brandResolver = new BrandContextResolver();

  async buildPrompt(
    templateName: string,
    placeholders: Record<string, string>,
    brandKit?: BrandKitContext,
    brandOptions?: Parameters<BrandContextResolver['resolve']>[1]
  ): Promise<string> {
    const sanitizedPlaceholders = sanitizePlaceholders(placeholders);
    const template = await loadTemplate(templateName);

    // Substitute placeholders
    let prompt = template.basePrompt;
    for (const [key, value] of Object.entries(sanitizedPlaceholders)) {
      prompt = prompt.replace(new RegExp(`\\{${key}\\}`, 'g'), value);
    }

    // Inject brand context
    if (brandKit) {
      const resolved = this.brandResolver.resolve(brandKit, brandOptions);
      const brandBlock = toCompactBrandBlock(resolved);
      
      if (brandBlock) {
        const modifier = INTENSITY_MODIFIERS[resolved.intensity];
        prompt = `${prompt}\n\n${modifier} the following brand guidelines:\n${brandBlock}`;
      }
    }

    // Add quality modifiers
    if (template.qualityModifiers.length) {
      prompt = `${prompt}\n\nQuality: ${template.qualityModifiers.join(', ')}`;
    }

    return prompt;
  }
}

export const promptEngine = new PromptEngine();
```

### Python

```python
import re
import yaml
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

MAX_INPUT_LENGTH = 500
SANITIZE_PATTERN = re.compile(r'[<>{}\[\]\\|`~]')
INJECTION_PATTERNS = [
    re.compile(r'ignore\s+(previous|above|all)', re.I),
    re.compile(r'disregard\s+(previous|above|all)', re.I),
    re.compile(r'system\s*:', re.I),
    re.compile(r'assistant\s*:', re.I),
    re.compile(r'\[INST\]', re.I),
]


def sanitize_input(input_str: str) -> str:
    if len(input_str) > MAX_INPUT_LENGTH:
        input_str = input_str[:MAX_INPUT_LENGTH]
    
    input_str = SANITIZE_PATTERN.sub('', input_str)
    
    for pattern in INJECTION_PATTERNS:
        if pattern.search(input_str):
            raise ValueError("Potential prompt injection detected")
    
    return input_str.strip()


@dataclass
class PromptTemplate:
    name: str
    version: str
    base_prompt: str
    placeholders: List[str]
    quality_modifiers: List[str]


@dataclass
class BrandKitContext:
    primary_colors: List[str]
    accent_colors: List[str]
    headline_font: Optional[str] = None
    tone: Optional[str] = None


@dataclass
class ResolvedBrandContext:
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    gradient: Optional[str] = None
    font: Optional[str] = None
    tone: Optional[str] = None
    intensity: str = "balanced"


class BrandContextResolver:
    def resolve(
        self,
        brand_kit: BrandKitContext,
        primary_index: int = 0,
        secondary_index: int = 1,
        accent_index: int = 0,
        use_gradient: bool = False,
        intensity: str = "balanced",
    ) -> ResolvedBrandContext:
        primary = self._resolve_color(brand_kit.primary_colors, primary_index)
        secondary = self._resolve_color(brand_kit.primary_colors, secondary_index)
        accent = self._resolve_color(brand_kit.accent_colors, accent_index)
        
        gradient = f"{primary}→{secondary}" if use_gradient and primary and secondary else None
        
        return ResolvedBrandContext(
            primary_color=primary,
            secondary_color=secondary,
            accent_color=accent,
            gradient=gradient,
            font=brand_kit.headline_font,
            tone=brand_kit.tone,
            intensity=intensity,
        )
    
    def _resolve_color(self, colors: List[str], index: int) -> Optional[str]:
        if not colors:
            return None
        return colors[min(index, len(colors) - 1)]


def to_compact_brand_block(ctx: ResolvedBrandContext) -> str:
    parts = []
    
    colors = [c for c in [ctx.primary_color, ctx.secondary_color, ctx.accent_color] if c]
    if colors:
        parts.append(f"Colors: {', '.join(colors)}")
    if ctx.gradient:
        parts.append(f"Gradient: {ctx.gradient}")
    if ctx.font:
        parts.append(f"Font: {ctx.font}")
    if ctx.tone:
        parts.append(f"Tone: {ctx.tone}")
    
    if not parts:
        return ""
    return f"[BRAND: {ctx.intensity} - {' | '.join(parts)}]"


_template_cache: Dict[str, PromptTemplate] = {}


def load_template(template_name: str) -> PromptTemplate:
    if template_name in _template_cache:
        return _template_cache[template_name]
    
    # Prevent directory traversal
    safe_name = template_name.replace("..", "").replace("/", "_")
    path = Path("prompts") / f"{safe_name}.yaml"
    
    with open(path) as f:
        data = yaml.safe_load(f)
    
    template = PromptTemplate(
        name=data.get("name", template_name),
        version=data.get("version", "1.0.0"),
        base_prompt=data["base_prompt"],
        placeholders=data.get("placeholders", []),
        quality_modifiers=data.get("quality_modifiers", []),
    )
    
    _template_cache[template_name] = template
    return template


INTENSITY_MODIFIERS = {
    "subtle": "subtly incorporate",
    "balanced": "use",
    "strong": "prominently feature",
}


class PromptEngine:
    def __init__(self):
        self._brand_resolver = BrandContextResolver()
    
    def build_prompt(
        self,
        template_name: str,
        placeholders: Dict[str, str],
        brand_kit: Optional[BrandKitContext] = None,
        intensity: str = "balanced",
        use_gradient: bool = False,
    ) -> str:
        # Sanitize inputs
        sanitized = {k: sanitize_input(v) for k, v in placeholders.items()}
        
        template = load_template(template_name)
        
        # Substitute placeholders
        prompt = template.base_prompt
        for key, value in sanitized.items():
            prompt = prompt.replace(f"{{{key}}}", value)
        
        # Inject brand context
        if brand_kit:
            resolved = self._brand_resolver.resolve(
                brand_kit, intensity=intensity, use_gradient=use_gradient
            )
            brand_block = to_compact_brand_block(resolved)
            
            if brand_block:
                modifier = INTENSITY_MODIFIERS[resolved.intensity]
                prompt = f"{prompt}\n\n{modifier} the following brand guidelines:\n{brand_block}"
        
        # Add quality modifiers
        if template.quality_modifiers:
            prompt = f"{prompt}\n\nQuality: {', '.join(template.quality_modifiers)}"
        
        return prompt


prompt_engine = PromptEngine()
```

## Template Example

```yaml
# prompts/thumbnail_gaming.yaml
name: thumbnail_gaming
version: "1.0.0"
base_prompt: |
  Create a {game_name} thumbnail.
  Feature {subject} with {emotion} expression.
  Style: {style}

placeholders:
  - game_name
  - subject
  - emotion
  - style

quality_modifiers:
  - ultra detailed
  - cinematic lighting
  - 8K quality
```

## Usage Examples

```typescript
const prompt = await promptEngine.buildPrompt(
  'thumbnail_gaming',
  {
    game_name: 'Cyberpunk 2077',
    subject: 'character with katana',
    emotion: 'intense',
    style: 'neon cyberpunk',
  },
  {
    primaryColors: ['#FF00FF', '#00FFFF'],
    accentColors: ['#FFFF00'],
    headlineFont: 'Orbitron',
    tone: 'edgy',
  },
  { useGradient: true, intensity: 'strong' }
);

// Result:
// Create a Cyberpunk 2077 thumbnail.
// Feature character with katana with intense expression.
// Style: neon cyberpunk
//
// prominently feature the following brand guidelines:
// [BRAND: strong - Colors: #FF00FF, #00FFFF, #FFFF00 | Gradient: #FF00FF→#00FFFF | Font: Orbitron | Tone: edgy]
//
// Quality: ultra detailed, cinematic lighting, 8K quality
```

## Best Practices

1. Sanitize all user inputs before substitution
2. Use compact brand blocks to save tokens
3. Cache templates for performance
4. Validate placeholders exist in templates
5. Use intensity modifiers for brand prominence

## Common Mistakes

- No input sanitization (injection vulnerability)
- Verbose brand context (wastes tokens)
- Hardcoded prompts (inconsistent)
- Missing placeholder validation
- No template caching (slow)

## Related Patterns

- ai-generation-client - Use prompts with AI APIs
- rate-limiting - Protect AI quota
- validation-quarantine - Validate AI outputs
