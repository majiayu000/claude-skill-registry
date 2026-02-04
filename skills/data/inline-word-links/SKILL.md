---
name: inline-word-links
description: Guidelines for adding inline cross-reference links to example sentences and notes. Includes common word reference table.
---

# Inline Word Links

This skill covers how to add cross-reference links within example sentences and notes. These links allow users to click on any word in an example to navigate to its dictionary entry.

## Link Format

The link format uses special Unicode delimiters:

```
⟦{surface|reading}→baseform：entry_id⟧
```

**Components:**
- `⟦` (U+27E6) - Opening bracket
- `surface` - The word as it appears in the sentence (may include furigana notation)
- `→` (U+2192) - Arrow separator
- `baseform` - The dictionary form of the word (for tooltip display)
- `：` (U+FF1A) - Fullwidth colon separator
- `entry_id` - The dictionary entry ID (e.g., `00111_hon`)
- `⟧` (U+27E7) - Closing bracket

## CRITICAL: Semantic Verification

**Links MUST be verified semantically, not programmatically.**

Before adding any link, you MUST:

1. **Understand the word's role** in the sentence
2. **Confirm the correct meaning** - many words are homographs with different entries
3. **Identify correct word boundaries** - particles attach to words differently
4. **Match to the correct entry** - verify the gloss matches the intended meaning

### Common Semantic Errors to Avoid

| Error Type | Example | Problem |
|------------|---------|---------|
| Wrong homograph | の → 野 (field) | の in most contexts is the particle, not the noun 野 |
| Wrong word boundary | ものです → もの + です | May need to link as a single grammatical pattern |
| Conjugated form mismatch | 食べました → 食べる | Correct, but verify the verb is the intended one |
| Compound splitting | 日本語 → 日本 + 語 | Should link as single compound if entry exists |

### Verification Process

For each word you intend to link:

1. Read the full sentence to understand context
2. Identify the word's grammatical function
3. Look up the entry ID (use reference table below for common words)
4. Verify the entry's gloss matches the word's meaning in context
5. Only then add the link markup

## Link Guidelines

### DO Link:
- Content words (nouns, verbs, adjectives, adverbs)
- Particles when they have dedicated entries
- Words that appear in the dictionary

### DO NOT Link:
- The headword of the entry in its own examples (no self-reference)
- Punctuation marks (。、？！「」)
- Words not in the dictionary - use `noentry` instead
- Names unless they have entries

### Using `noentry`

For words without dictionary entries:

```
⟦{矍鑠|かくしゃく}→矍鑠：noentry⟧
```

This preserves the markup for future linking but renders as plain text.

## Examples

### Basic Example

Original:
```json
"japanese": "{本|ほん}を{読|よ}む。"
```

With links:
```json
"japanese": "⟦{本|ほん}→本：00111_hon⟧⟦を→を：00422_wo⟧⟦{読|よ}む→読む：00426_yomu⟧。"
```

### Example with Particles

Original:
```json
"japanese": "{私|わたし}は{日本語|にほんご}が{分|わ}かります。"
```

With links:
```json
"japanese": "⟦{私|わたし}→私：02988_watashi⟧⟦は→は：00079_ha⟧⟦{日本語|にほんご}→日本語：00614_nihongo⟧⟦が→が：00051_ga⟧⟦{分|わ}かります→分かる：00463_wakaru⟧。"
```

### Example with Conjugation

Original:
```json
"japanese": "{彼|かれ}は{来|き}ませんでした。"
```

With links (note: conjugated forms link to dictionary form):
```json
"japanese": "⟦{彼|かれ}→彼：01292_kare⟧⟦は→は：00079_ha⟧⟦{来|き}ませんでした→来る：00254_kuru⟧。"
```

## Common Words Reference Table

Use this table for quick reference. For words not listed, search the dictionary.

### Particles

| Entry ID | Word | Reading | Gloss |
|----------|------|---------|-------|
| 00051_ga | が | が | subject marker |
| 00079_ha | は | は | topic marker |
| 00314_ni | に | に | location/direction/time marker |
| 00422_wo | を | を | direct object marker |
| 00484_mo | も | も | also, too, even |
| 00490_made | まで | まで | until, to, as far as |
| 00502_de | で | で | at, by, with (location/means) |
| 00504_kara | から | から | from, because |
| 00512_to | と | と | and, with, quotation |
| 02473_he | へ | へ | direction marker (toward) |
| 09472_no | の | の | possessive marker, nominalizer |
| 09473_ka | か | か | question marker, or |
| 09474_ne | ね | ね | confirmation particle |
| 09475_yo | よ | よ | emphasis particle |
| 09476_yori | より | より | than, from (comparison) |
| 09477_kedo | けど | けど | but, although |

### Pronouns and Demonstratives

| Entry ID | Word | Reading | Gloss |
|----------|------|---------|-------|
| 00534_dare | 誰 | だれ | who |
| 00536_itsu | いつ | いつ | when |
| 00539_doko | どこ | どこ | where |
| 00543_dou | どう | どう | how, in what way |
| 00547_dore | どれ | どれ | which one |
| 00551_dono | どの | どの | which (+ noun) |
| 00498_nani | 何 | なに | what |
| 02988_watashi | 私 | わたし | I, me |
| 00915_ano | あの | あの | that (over there) |
| 00919_asoko | あそこ | あそこ | over there |
| 00961_koko | ここ | ここ | here |
| 00962_kono | この | この | this |
| 00991_soko | そこ | そこ | there |
| 00993_sono | その | その | that |
| 00994_sore | それ | それ | that (thing) |
| 01292_kare | 彼 | かれ | he, him |
| 01286_kanojo | 彼女 | かのじょ | she, her |

### Common Verbs

| Entry ID | Word | Reading | Gloss |
|----------|------|---------|-------|
| 00006_aru | ある | ある | to exist (inanimate) |
| 00119_iku | 行く | いく | to go |
| 00254_kuru | 来る | くる | to come |
| 00283_miru | 見る | みる | to see, look, watch |
| 00322_nomu | 飲む | のむ | to drink |
| 00392_suru | する | する | to do, to make |
| 00396_taberu | 食べる | たべる | to eat |
| 00426_yomu | 読む | よむ | to read |
| 00458_shiru | 知る | しる | to know, to learn |
| 00463_wakaru | 分かる | わかる | to understand |
| 00467_hanasu | 話す | はなす | to speak, talk |
| 00469_matsu | 待つ | まつ | to wait |
| 00470_neru | 寝る | ねる | to sleep |
| 00473_tsukau | 使う | つかう | to use |
| 00474_wasureru | 忘れる | わすれる | to forget |
| 00477_kaku | 書く | かく | to write |
| 00478_motsu | 持つ | もつ | to hold, have |
| 00481_tsukuru | 作る | つくる | to make, create |
| 00482_au | 会う | あう | to meet |
| 00483_kiku | 聞く | きく | to hear, listen, ask |
| 00489_kau | 買う | かう | to buy |
| 00492_omou | 思う | おもう | to think, feel |
| 00494_hairu | 入る | はいる | to enter |
| 00495_iru | いる | いる | to exist (animate) |
| 00503_hataraku | 働く | はたらく | to work |
| 00508_kaeru | 帰る | かえる | to return home |
| 00511_noru | 乗る | のる | to ride, get on |
| 00513_deru | 出る | でる | to go out, leave |
| 00515_iu | 言う | いう | to say, tell |
| 00519_hashiru | 走る | はしる | to run |
| 00520_morau | もらう | もらう | to receive |
| 00521_okiru | 起きる | おきる | to wake up |
| 00526_oshieru | 教える | おしえる | to teach |
| 00527_benkyousuru | 勉強する | べんきょうする | to study |
| 00531_hajimeru | 始める | はじめる | to begin |
| 00538_aruku | 歩く | あるく | to walk |
| 00546_ageru | あげる | あげる | to give, raise |
| 00550_asobu | 遊ぶ | あそぶ | to play |
| 00557_dekiru | できる | できる | to be able to |
| 00567_owaru | 終わる | おわる | to end |
| 01970_naru | なる | なる | to become |

### Common Adjectives

| Entry ID | Word | Reading | Gloss |
|----------|------|---------|-------|
| 00025_chiisai | 小さい | ちいさい | small, little |
| 00118_ii | いい | いい | good, fine |
| 00335_ookii | 大きい | おおきい | big, large |
| 00464_yasui | 安い | やすい | cheap |
| 00488_furui | 古い | ふるい | old |
| 00491_nagai | 長い | ながい | long |
| 00500_takai | 高い | たかい | high, expensive |
| 00506_atarashii | 新しい | あたらしい | new |
| 00510_mijikai | 短い | みじかい | short |
| 00514_hayai | 速い/早い | はやい | fast, early |
| 00517_muzukashii | 難しい | むずかしい | difficult |
| 00529_tooi | 遠い | とおい | far |
| 00530_chikai | 近い | ちかい | near |
| 00533_osoi | 遅い | おそい | slow, late |
| 00585_akai | 赤い | あかい | red |
| 00586_aoi | 青い | あおい | blue |
| 00587_shiroi | 白い | しろい | white |
| 00588_kuroi | 黒い | くろい | black |
| 00589_omoshiroi | 面白い | おもしろい | interesting |
| 00591_isogashii | 忙しい | いそがしい | busy |
| 01107_hoshii | 欲しい | ほしい | wanted, desired |
| 01118_nai | ない | ない | nonexistent |

### Common Nouns

| Entry ID | Word | Reading | Gloss |
|----------|------|---------|-------|
| 00111_hon | 本 | ほん | book |
| 00468_jikan | 時間 | じかん | time, hour |
| 00476_hito | 人 | ひと | person |
| 00480_shigoto | 仕事 | しごと | work, job |
| 00486_toshi | 年 | とし | year, age |
| 00487_yoru | 夜 | よる | night |
| 00496_kyou | 今日 | きょう | today |
| 00497_mise | 店 | みせ | store, shop |
| 00499_sakana | 魚 | さかな | fish |
| 00501_ashita | 明日 | あした | tomorrow |
| 00505_michi | 道 | みち | road, way |
| 00507_heya | 部屋 | へや | room |
| 00516_kuruma | 車 | くるま | car |
| 00522_densha | 電車 | でんしゃ | train |
| 00523_hana | 花 | はな | flower |
| 00524_ki | 木 | き | tree |
| 00525_me | 目 | め | eye |
| 00558_kao | 顔 | かお | face |
| 00560_kuchi | 口 | くち | mouth |
| 00569_te | 手 | て | hand |
| 00574_atama | 頭 | あたま | head |
| 00575_ashi | 足 | あし | foot, leg |
| 00576_ocha | お茶 | おちゃ | tea |
| 00577_byouin | 病院 | びょういん | hospital |
| 00578_ginkou | 銀行 | ぎんこう | bank |
| 00580_toshokan | 図書館 | としょかん | library |
| 00581_kouen | 公園 | こうえん | park |
| 00582_tenki | 天気 | てんき | weather |
| 00583_ame | 雨 | あめ | rain |
| 00607_kaisha | 会社 | かいしゃ | company |
| 00608_daigaku | 大学 | だいがく | university |
| 00609_sensei | 先生 | せんせい | teacher |
| 00610_gakusei | 学生 | がくせい | student |
| 00611_okane | お金 | おかね | money |
| 00612_ie | 家 | いえ | house, home |
| 00614_nihongo | 日本語 | にほんご | Japanese language |
| 00682_ue | 上 | うえ | above, up |
| 00670_shita | 下 | した | below, down |
| 00710_kaigi | 会議 | かいぎ | meeting |
| 00762_tsukue | 机 | つくえ | desk |
| 00888_shitsumon | 質問 | しつもん | question |
| 02180_eki | 駅 | えき | station |

### Common Adverbs

| Entry ID | Word | Reading | Gloss |
|----------|------|---------|-------|
| 00593_totemo | とても | とても | very |
| 00595_chotto | ちょっと | ちょっと | a little |
| 00596_sukoshi | 少し | すこし | a little, few |
| 00597_takusan | たくさん | たくさん | a lot, many |
| 00598_zenzen | 全然 | ぜんぜん | not at all |
| 00599_itsumo | いつも | いつも | always |
| 00600_tokidoki | 時々 | ときどき | sometimes |
| 00601_yoku | よく | よく | often, well |
| 00602_mou | もう | もう | already |
| 00603_mada | まだ | まだ | still, not yet |
| 00604_amari | あまり | あまり | not very |
| 00814_sugu | すぐ | すぐ | immediately |
| 00881_saikin | 最近 | さいきん | recently, lately |
| 01284_moshi | もし | もし | if, in case |

### Additional Common Words

These are frequently encountered words not in the categories above:

| Entry ID | Word | Reading | Gloss |
|----------|------|---------|-------|
| 00164_kamoshirenai | かもしれない | かもしれない | might, perhaps |
| 00554_kodomo | 子供 | こども | child |
| 00673_sumu | 住む | すむ | to live, reside |
| 00755_shizuka | 静か | しずか | quiet, calm |
| 00791_kowareru | 壊れる | こわれる | to break |
| 00823_wakai | 若い | わかい | young |
| 00846_hitsuyou | 必要 | ひつよう | necessary |
| 01098_ireru | 入れる | いれる | to put in |
| 01127_ooi | 多い | おおい | many, much |
| 01137_tokoro | ところ | ところ | place, point |
| 01165_mieru | 見える | みえる | to be visible |
| 01179_keiken | 経験 | けいけん | experience |
| 01430_juusho | 住所 | じゅうしょ | address |
| 01458_tatemono | 建物 | たてもの | building |
| 01636_shippai | 失敗 | しっぱい | failure |
| 01932_kiku | 効く | きく | to be effective |
| 01970_naru | なる | なる | to become |
| 02355_suki | 好き | すき | like, fond of |
| 02444_hiku | 弾く | ひく | to play (instrument) |
| 02514_kekkon | 結婚 | けっこん | marriage |
| 02848_issho | 一緒 | いっしょ | together |
| 02899_kudasai | ください | ください | please (do) |
| 03036_machigau | 間違う | まちがう | to make a mistake |
| 03093_dake | だけ | だけ | only, just |
| 03290_seichou | 成長 | せいちょう | growth |
| 03823_senshu | 選手 | せんしゅ | player, athlete |

### Conjunctions

| Entry ID | Word | Reading | Gloss |
|----------|------|---------|-------|
| 00031_daga | だが | だが | but, however |
| 00033_dakedo | だけど | だけど | but, however |
| 00379_sokode | そこで | そこで | so, therefore |
| 00382_soredemo | それでも | それでも | but still |

## Workflow for Adding Links

1. **Read the sentence** - Understand the full meaning
2. **Identify each word** - Note word boundaries carefully
3. **Look up entry IDs** - Use reference table or search dictionary
4. **Verify semantically** - Confirm each link matches intended meaning
5. **Add markup** - Apply the link format carefully
6. **Validate immediately** - Run validation to catch ID errors early:
   ```bash
   python3 build/validate.py 2>&1 | grep -A5 "Word link"
   ```
7. **Review** - Read through the linked sentence to verify

## Tracking `noentry` Words

When you mark a word with `noentry`, consider tracking it for potential future entry creation. In your session log, include:

```markdown
### Words marked noentry (candidates for future entries)
- ランナー (runner)
- セーフ (safe - sports)
- 丁目 (district number)
```

This helps identify gaps in the dictionary that may need filling.

## Quality Checklist

Before finalizing links:

- [ ] Every link has been semantically verified
- [ ] No self-references (headword linking to itself)
- [ ] Punctuation is not linked
- [ ] Conjugated forms link to dictionary forms
- [ ] All entry IDs are valid
- [ ] Furigana is preserved correctly within links
- [ ] No spacing artifacts between links
