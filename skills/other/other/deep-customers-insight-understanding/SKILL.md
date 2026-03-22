---
name: deep-customers-insight-understanding
description: Prompt này yêu cầu AI đóng vai trò chuyên gia chiến lược marketing và nghiên cứu hành vi khách hàng để phân tích insight của tệp khách hàng mục tiêu cho một sản phẩm/dịch vụ cụ thể theo hai khung: tháp nhu cầu Maslow và 6 khía cạnh cuộc sống, từ đó xác định ưu tiên nhu cầu/yếu tố, làm rõ động lực tâm lý và pain point, diễn giải hành vi–niềm tin–rào cản–kỳ vọng, rồi đề xuất các góc độ nội dung cùng định dạng nội dung và kênh triển khai (Facebook, TikTok, Email, SEO website, PR), trình bày kết quả dưới dạng bảng theo ngôn ngữ được chỉ định.
skillVersionId: 0198c184-789c-7191-82bf-6fd057192cbe
---

## What it does

Prompt này yêu cầu AI đóng vai trò chuyên gia chiến lược marketing và nghiên cứu hành vi khách hàng để phân tích insight của tệp khách hàng mục tiêu cho một sản phẩm/dịch vụ cụ thể theo hai khung: tháp nhu cầu Maslow và 6 khía cạnh cuộc sống, từ đó xác định ưu tiên nhu cầu/yếu tố, làm rõ động lực tâm lý và pain point, diễn giải hành vi–niềm tin–rào cản–kỳ vọng, rồi đề xuất các góc độ nội dung cùng định dạng nội dung và kênh triển khai (Facebook, TikTok, Email, SEO website, PR), trình bày kết quả dưới dạng bảng theo ngôn ngữ được chỉ định.

> Requires the **betterprompt** CLI to run. For installation and general CLI usage, refer to the `betterprompt` skill in your skill list or if not yet available in skill list, install via `npx skills add https://github.com/BetterPromptme/betterprompt/skills --skill betterprompt`

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Language` | Optional |  | `English` |
| `Brand_Name` | Optional |  | `Upcontent` |
| `Descriptions` | Optional |  | `Providing graphic design and content marketing solutions for SME businesses including profile design, catalog, menu, advertising images, website banners, fan care and website content` |
| `Target_audience` | Optional |  | `Business owners or general marketing people in small and medium-sized companies  currently do not have design staff or lack a team to plan and implement multi-channel Content Marketing or content staff are not working effectively.` |



### Models and options

This skill's modality is: **`text`**.

To discover which `model` values you can use (and which `options` keys/values are valid for each model), run:

```bash
betterprompt resources --models-only --json
```

Then filter the returned JSON array to entries where `modality` is `"text"`.

## How to run

### Step 1: Collect inputs

First, run `betterprompt resources --models-only --json` and filter to `modality: "text"` to discover valid models and available options:

```bash
betterprompt resources --models-only --json
```

Use only the models and option values that appear in the filtered results.

Then collect all inputs from the human:

- Optional text inputs (use defaults if not provided by the human):
    - `Language` (default: `English`)
  - `Brand_Name` (default: `Upcontent`)
  - `Descriptions` (default: `Providing graphic design and content marketing solutions for SME businesses including profile design, catalog, menu, advertising images, website banners, fan care and website content`)
  - `Target_audience` (default: `Business owners or general marketing people in small and medium-sized companies  currently do not have design staff or lack a team to plan and implement multi-channel Content Marketing or content staff are not working effectively.`)
- Optional: model and options.
  - Present the human with the default model **`gpt-5-mini`** and its available options. Look up `gpt-5-mini` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-5-mini`, options `{}`. Other models from the resources call are also available.


### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `skillVersionId` as the positional argument (for this skill version, use `0198c184-789c-7191-82bf-6fd057192cbe`).

Command form:

```bash
betterprompt generate 0198c184-789c-7191-82bf-6fd057192cbe \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-5-mini`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate 0198c184-789c-7191-82bf-6fd057192cbe \
  --input Language=English \
  --input Brand_Name=Upcontent \
  --input 'Descriptions=Providing graphic design and content marketing solutions for SME businesses including profile design, catalog, menu, advertising images, website banners, fan care and website content' \
  --input 'Target_audience=Business owners or general marketing people in small and medium-sized companies  currently do not have design staff or lack a team to plan and implement multi-channel Content Marketing or content staff are not working effectively.' \
  --model gpt-5-mini \
  --options '{}'
```
