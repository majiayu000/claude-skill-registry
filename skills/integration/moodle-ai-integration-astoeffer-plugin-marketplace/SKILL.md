---
name: moodle-ai-subsystem
description: Moodle AI Subsystem integration for providers and actions. Use when integrating AI capabilities into Moodle, creating AI providers, or implementing AI actions.
---

# Moodle AI Subsystem Integration

Integrate AI capabilities into Moodle 4.5+ using the AI Subsystem.

## When to Use This Skill

- Creating AI providers (Ollama, Anthropic, OpenAI)
- Implementing AI actions
- Building AI placements in courses
- Text generation and summarization

See [reference.md](reference.md) for complete patterns.

## Provider Implementation

```php
namespace aitool_ollama;

class provider extends \core_ai\provider {
    public function get_action_list(): array {
        return [
            \core_ai\aiactions\generate_text::class,
            \core_ai\aiactions\summarise_text::class,
        ];
    }
}
```

## Action Usage

```php
$manager = \core_ai\manager::get_manager();
$action = new \core_ai\aiactions\generate_text(
    contextid: $context->id,
    userid: $USER->id,
    prompttext: $prompt
);
$response = $manager->process_action($action);
```

## Key Concepts

- **Provider**: Connection to AI service (API)
- **Action**: Specific AI capability (generate, summarize)
- **Placement**: Where AI appears in Moodle UI
