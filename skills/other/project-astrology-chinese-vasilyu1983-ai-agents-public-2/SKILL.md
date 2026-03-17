---
name: project-astrology-chinese
description: Use when users ask about Chinese astrology, zodiac compatibility, BaZi (Four Pillars) birth charts, Five Elements, Zi Wei Dou Shu, Flying Stars Feng Shui, or Qi Men Dun Jia timing. Calculates signs from birth data, interprets charts, and provides forecasts. (project)
---

# Chinese Astrology

Provide Chinese zodiac, BaZi, Zi Wei Dou Shu, Feng Shui, and Qi Men Dun Jia guidance with explicit inputs, assumptions, and uncertainty.

## Scope and routing

- If the user wants Western astrology, route to Western resources (do not improvise).
- If the user wants Jyotish/Vedic, use `../project-astrology-vedic/SKILL.md`.
- If the user wants Tarot or I Ching, use `../project-astrology-tarot-divination/SKILL.md`.
- If the user wants numerology, use `../project-astrology-numerology/SKILL.md`.

## Core workflow

1. Collect inputs:
   - Birth date (Gregorian), birth time (local), birth place (city/country), timezone/DST at birth.
   - Zi Wei Dou Shu: also ask for sex at birth (some schools differ), and confirm lunar date conversion + leap month handling.
   - Feng Shui: building facing direction (degrees), period (move-in / last major renovation year), and the target room/sector.
   - Qi Men: the exact date/time (to the hour) and the question (goal, constraints, time horizon).
2. Choose the system based on the question:
   - Zodiac/compatibility: year animal + year stem element.
   - BaZi: Four Pillars, Day Master, Ten Gods, luck pillars.
   - Zi Wei: 12-palace chart + key stars + decade/year luck.
   - Feng Shui/Flying Stars: time + space sectors.
   - Ze Ri / timing: auspicious day/hour selection.
3. Apply accuracy rules (do not guess):
   - Zodiac animal year switches at Chinese New Year; Jan/Feb births must be checked.
   - BaZi year/month pillars use solar terms (Jie Qi); year pillar often switches near Li Chun (around Feb 4), not Chinese New Year.
   - Timezone/DST and birth location matter for hour pillar and solar term boundaries.
4. Produce the output:
   - State what was calculated (system, calendar basis, boundaries used).
   - If birth time is unknown, give a range or a partial reading and explain what changes with different hours.
   - Keep predictions non-deterministic; frame as tendencies and planning guidance, not guarantees.
5. Data handling:
   - Treat birth data as sensitive; do not store it and do not echo it back unnecessarily.

## Request-to-resource map

- Compatibility: `references/compatibility-guide.md`
- Zodiac calculations: `references/zodiac-calculations.md` and `references/chinese-calendar.md`
- BaZi: `references/bazi-guide.md` and `references/bazi-day-master-analysis.md`
- Zi Wei Dou Shu: `references/zi-wei-dou-shu.md`
- Flying Stars / Feng Shui: `references/flying-stars-feng-shui.md` and `references/timing-fengshui.md`
- Qi Men timing: `references/qi-men-dun-jia.md`
- Annual forecast: `references/annual-forecast.md`
- Animal profiles: `references/animal-personalities.md`
- Five Elements: `references/five-elements-guide.md`

## Common pitfalls

- Using Chinese New Year boundaries for BaZi pillars (BaZi uses Jie Qi solar terms).
- Assigning an animal year for Jan/Feb births without checking the Chinese New Year date.
- Treating a missing birth time as "close enough" for BaZi, Zi Wei, or Qi Men (it is not).
- Mixing schools without stating assumptions (for example, Zi Wei lunar conversion rules, Feng Shui period rules).

## Templates

- `assets/template-chinese-reading.md`
- `assets/template-compatibility.md`

## Sources (non-authoritative)

Use these for cross-checking only; do not treat them as canonical when dates/solar terms matter.
- https://www.chinesefortunecalendar.com/
- https://www.yourchineseastrology.com/
