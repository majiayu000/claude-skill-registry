---
name: cantonese-understanding
description: Parse and understand Cantonese user input. ALWAYS use this skill first when user writes in Cantonese or uses Cantonese vocabulary. This skill translates Cantonese to standard Chinese/English for LLM comprehension.
---

# 粵語理解技能 (Cantonese Understanding Skill)

當用戶使用粵語輸入時，你必須首先使用此技能來理解其含義。

## 觸發條件

當檢測到以下情況時自動啟用：
- 用戶輸入包含粵語特有詞彙（如：係、唔、嘅、咗、緊、啦、喇、囉、咩、嘢、乜、點解、邊個、幾時、邊度）
- 用戶輸入包含粵語口語表達
- 用戶輸入無法用普通話/國語直接理解

## 工作流程

1. **識別粵語成分**: 找出輸入中的粵語詞彙和表達
2. **查詢字典**: 使用 `cantonese-dictionary` MCP 查詢不確定的詞彙
3. **語義轉換**: 將粵語轉換為標準漢語或英語
4. **意圖識別**: 判斷用戶的真實意圖（提問、指令、閒聊等）

## 常見粵語詞彙對照

### 代詞和疑問詞
| 粵語 | 普通話 | 英語 |
|------|--------|------|
| 我 | 我 | I/me |
| 你 | 你 | you |
| 佢 | 他/她/它 | he/she/it |
| 我哋 | 我們 | we |
| 你哋 | 你們 | you (plural) |
| 佢哋 | 他們 | they |
| 乜/乜嘢 | 什麼 | what |
| 邊個 | 誰 | who |
| 邊度 | 哪裡 | where |
| 幾時 | 什麼時候 | when |
| 點解 | 為什麼 | why |
| 點/點樣 | 怎樣 | how |

### 常用動詞
| 粵語 | 普通話 | 英語 |
|------|--------|------|
| 係 | 是 | is/am/are |
| 唔係 | 不是 | is not |
| 有冇 | 有沒有 | have/has? |
| 食 | 吃 | eat |
| 飲 | 喝 | drink |
| 睇 | 看 | look/watch |
| 聽 | 聽 | listen |
| 講 | 說 | speak/say |
| 話 | 說/告訴 | tell/say |
| 諗 | 想 | think |
| 知 | 知道 | know |
| 識 | 認識/會 | know/can |
| 俾 | 給 | give |
| 攞 | 拿 | take |
| 搵 | 找 | find/look for |
| 做 | 做 | do/make |
| 去 | 去 | go |
| 嚟 | 來 | come |
| 返 | 回 | return |
| 行 | 走 | walk |
| 企 | 站 | stand |
| 坐 | 坐 | sit |
| 瞓 | 睡 | sleep |
| 起身 | 起床 | get up |

### 副詞和助詞
| 粵語 | 普通話 | 用法 |
|------|--------|------|
| 唔 | 不 | 否定 |
| 冇 | 沒有 | 否定 |
| 好 | 很 | 程度副詞 |
| 都 | 也/都 | 副詞 |
| 仲 | 還 | 副詞 |
| 先 | 才/先 | 時間副詞 |
| 就 | 就 | 副詞 |
| 咗 | 了 | 完成態 |
| 緊 | 正在 | 進行態 |
| 過 | 過 | 經歷態 |
| 嘅 | 的 | 結構助詞 |
| 啦/喇 | 了/啦 | 語氣詞 |
| 囉/咯 | 囉 | 語氣詞 |
| 啩 | 吧 | 推測語氣 |
| 咩 | 嗎 | 疑問語氣 |
| 呀 | 啊 | 語氣詞 |
| 噃 | 的嘛 | 強調語氣 |
| 添 | 還/再 | 追加義 |

### 常見表達
| 粵語 | 普通話 |
|------|--------|
| 唔該 | 請/謝謝/勞駕 |
| 多謝 | 謝謝 |
| 早晨 | 早上好 |
| 你好 | 你好 |
| 拜拜 | 再見 |
| 得唔得 | 行不行/可以嗎 |
| 冇問題 | 沒問題 |
| 係咁先 | 就這樣 |
| 唔緊要 | 沒關係 |
| 點算 | 怎麼辦 |
| 搞掂 | 搞定了 |
| 唔知 | 不知道 |
| 明唔明 | 明白嗎 |
| 係咪 | 是不是 |

## 使用 MCP 查詢

對於不認識的粵語詞彙，使用 cantonese-dictionary MCP：

```
lookup_phrase: 查詢整句或詞組
lookup_character: 查詢單個字
search_definition: 根據上下文搜索可能的意思
```

## 輸出格式

理解用戶輸入後，在內部記錄：

```
【粵語理解】
原文: [用戶原始輸入]
理解: [標準漢語/英語翻譯]
意圖: [用戶意圖：提問/指令/閒聊/其他]
關鍵詞: [提取的關鍵信息]
```

然後根據理解的內容進行回應。
