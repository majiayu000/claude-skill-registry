---
name: captures
description: Generate Liquid capture blocks from rough notes. Use when starting a book review to turn voice-transcribed notes into template variables for books, authors, and series mentioned.
---

# Captures Skill

Generate `{% capture %}` blocks for book reviews from rough notes.

## Usage

`/captures` --- Pass your rough notes (often voice-transcribed) and get back the capture blocks needed for books, authors, and series you reference.

## What This Skill Does

1. **Parse rough notes** for mentions of books, authors, series, short stories, movies, games
2. **Fix common voice transcription errors** (see below)
3. **Generate capture blocks** following the site's naming conventions
4. **Validate against existing content** when possible

## Output Format

For **each book referenced**, generate the full bundle:

1. Author link
2. Author possessive
3. Author lastname
4. Author lastname possessive
5. Series link (if part of a series)
6. Book link

Group by book:

```liquid
{% capture banks %}{% author_link "Iain M. Banks" %}{% endcapture %}
{% capture bankss %}{% author_link "Iain M. Banks" possessive %}{% endcapture %}
{% capture banks_lastname %}{% author_link "Iain M. Banks" link_text="Banks" %}{% endcapture %}
{% capture bankss_lastname %}{% author_link "Iain M. Banks" link_text="Banks" possessive %}{% endcapture %}
{% capture culture %}{% series_link "Culture" %}{% endcapture %}
{% capture surface_detail %}{% book_link "Surface Detail" %}{% endcapture %}

{% capture stross %}{% author_link "Charles Stross" %}{% endcapture %}
{% capture strosss %}{% author_link "Charles Stross" possessive %}{% endcapture %}
{% capture stross_lastname %}{% author_link "Charles Stross" link_text="Stross" %}{% endcapture %}
{% capture strosss_lastname %}{% author_link "Charles Stross" link_text="Stross" possessive %}{% endcapture %}
{% capture a_colder_war %}{% short_story_link "A Colder War" %}{% endcapture %}

{% capture terminator %}{% movie_title "Terminator" %}{% endcapture %}
{% capture fallout %}{% game_title "Fallout" %}{% endcapture %}
```

If multiple books share the same author, only include the author bundle once (with the first book):

```liquid
{% capture banks %}{% author_link "Iain M. Banks" %}{% endcapture %}
{% capture bankss %}{% author_link "Iain M. Banks" possessive %}{% endcapture %}
{% capture banks_lastname %}{% author_link "Iain M. Banks" link_text="Banks" %}{% endcapture %}
{% capture bankss_lastname %}{% author_link "Iain M. Banks" link_text="Banks" possessive %}{% endcapture %}
{% capture culture %}{% series_link "Culture" %}{% endcapture %}
{% capture surface_detail %}{% book_link "Surface Detail" %}{% endcapture %}
{% capture use_of_weapons %}{% book_link "Use of Weapons" %}{% endcapture %}
{% capture look_to_windward %}{% book_link "Look to Windward" %}{% endcapture %}
```

## Voice Transcription Errors

These notes are often voice-transcribed and will contain errors:
- Misspellings ("shriek" for "Shrike", "telehard" for "Teilhard")
- Wrong words ("forecaster" for "farcaster")
- Missing capitals or articles
- Phonetic spellings ("bobiberse" for "Bobiverse")

**Figure out the correct titles, authors, and series from context.** Check existing reviews in `_books/` for correct spellings. Use your knowledge of sci-fi literature to resolve ambiguities. If you're unsure, ask.

**Special case**: Disco Elysium is treated as a book, not a game.

## Naming Conventions

### Authors

```liquid
{% capture banks %}{% author_link "Iain M. Banks" %}{% endcapture %}
{% capture bankss %}{% author_link "Iain M. Banks" possessive %}{% endcapture %}
{% capture banks_lastname %}{% author_link "Iain M. Banks" link_text="Banks" %}{% endcapture %}
{% capture bankss_lastname %}{% author_link "Iain M. Banks" link_text="Banks" possessive %}{% endcapture %}
```

Variable naming:
- `banks` --- full name
- `bankss` --- full name possessive (double s for names ending in s)
- `banks_lastname` --- lastname only
- `bankss_lastname` --- lastname possessive

### Multiple Authors

For books with multiple authors, generate captures for each author separately, plus combined versions:

```liquid
{% capture el_mohtar %}{% author_link "Amal El-Mohtar" %}{% endcapture %}
{% capture el_mohtars %}{% author_link "Amal El-Mohtar" possessive %}{% endcapture %}
{% capture el_mohtar_lastname %}{% author_link "Amal El-Mohtar" link_text="El-Mohtar" %}{% endcapture %}
{% capture el_mohtars_lastname %}{% author_link "Amal El-Mohtar" link_text="El-Mohtar" possessive %}{% endcapture %}
{% capture gladstone %}{% author_link "Max Gladstone" %}{% endcapture %}
{% capture gladstones %}{% author_link "Max Gladstone" possessive %}{% endcapture %}
{% capture gladstone_lastname %}{% author_link "Max Gladstone" link_text="Gladstone" %}{% endcapture %}
{% capture gladstones_lastname %}{% author_link "Max Gladstone" link_text="Gladstone" possessive %}{% endcapture %}
{% capture el_mohtar_and_gladstone %}{% author_link "Amal El-Mohtar" %} and {% author_link "Max Gladstone" %}{% endcapture %}
{% capture el_mohtar_and_gladstones %}{% author_link "Amal El-Mohtar" %} and {% author_link "Max Gladstone" possessive %}{% endcapture %}
```

For siblings or similar (like the Strugatsky brothers), you might use first names:

```liquid
{% capture arkady_and_boris %}{% author_link "Arkady Strugatsky" link_text="Arkady" %} and {% author_link "Boris Strugatsky" %}{% endcapture %}
{% capture arkady_and_boriss %}{% author_link "Arkady Strugatsky" link_text="Arkady" %} and {% author_link "Boris Strugatsky" possessive %}{% endcapture %}
```

For 3+ authors (anthologies), use `author_` prefix and create captures as needed:

```liquid
{% capture author_evans %}{% author_link "Linda Evans" %}{% endcapture %}
{% capture author_evans_lastname %}{% author_link "Linda Evans" link_text="Evans" %}{% endcapture %}
{% capture author_hollingsworth %}{% author_link "Robert R. Hollingsworth" %}{% endcapture %}
{% capture author_weber %}{% author_link "David Weber" %}{% endcapture %}
{% capture author_weber_lastname %}{% author_link "David Weber" link_text="Weber" %}{% endcapture %}
```

### Books

```liquid
{% capture surface_detail %}{% book_link "Surface Detail" %}{% endcapture %}
{% capture the_player_of_games %}{% book_link "The Player of Games" %}{% endcapture %}
```

Variable naming: snake_case of the title, including "the" if in title.

### Series

```liquid
{% capture culture %}{% series_link "Culture" %}{% endcapture %}
{% capture hyperion_cantos %}{% series_link "Hyperion Cantos" %}{% endcapture %}
{% capture botns %}{% series_link "The Book of the New Sun" %}{% endcapture %}
```

Common abbreviations are fine in the variable name: `botns`, `cantos`.

### Movies, Games, Other Media

These don't have link tags, so use raw HTML:

```liquid
{% capture terminator %}{% movie_title "Terminator" %}{% endcapture %}
{% capture fallout %}{% game_title "Fallout" %}{% endcapture %}
{% capture ds9 %}{% tv_show_title "Deep Space Nine" %}{% endcapture %}
```

**Exception**: Disco Elysium is treated as a book and uses `{% book_link "Disco Elysium" %}`.

## Checking Spelling

Check existing files for correct spellings:

- `_books/` for book titles
- `books/authors/` for author names
- `books/series/` for series names

**Always generate captures even if we don't have a review yet.** The plugins handle missing content gracefully and will create proper links when the content exists.

## Standard Captures (always included)

Every review starts with captures for the book being reviewed, the author, and series (from `_books/_template/book_template.md`):

Don't duplicate these. Only generate captures for *other* books/authors mentioned in the notes.

## Example

**Input notes:**
```
- like Time War there's a planet called garden
- The core representative references the three laws of robotics
- very much surface detail
- reminds me of Stross's a colder war
```

**Output:**
```liquid
{% capture el_mohtar %}{% author_link "Amal El-Mohtar" %}{% endcapture %}
{% capture el_mohtars %}{% author_link "Amal El-Mohtar" possessive %}{% endcapture %}
{% capture el_mohtar_lastname %}{% author_link "Amal El-Mohtar" link_text="El-Mohtar" %}{% endcapture %}
{% capture el_mohtars_lastname %}{% author_link "Amal El-Mohtar" link_text="El-Mohtar" possessive %}{% endcapture %}
{% capture gladstone %}{% author_link "Max Gladstone" %}{% endcapture %}
{% capture gladstones %}{% author_link "Max Gladstone" possessive %}{% endcapture %}
{% capture gladstone_lastname %}{% author_link "Max Gladstone" link_text="Gladstone" %}{% endcapture %}
{% capture gladstones_lastname %}{% author_link "Max Gladstone" link_text="Gladstone" possessive %}{% endcapture %}
{% capture time_war %}{% book_link "This Is How You Lose the Time War" %}{% endcapture %}

{% capture asimov %}{% author_link "Isaac Asimov" %}{% endcapture %}
{% capture asimovs %}{% author_link "Isaac Asimov" possessive %}{% endcapture %}
{% capture asimov_lastname %}{% author_link "Isaac Asimov" link_text="Asimov" %}{% endcapture %}
{% capture asimovs_lastname %}{% author_link "Isaac Asimov" link_text="Asimov" possessive %}{% endcapture %}
{% capture i_robot %}{% book_link "I, Robot" %}{% endcapture %}

{% capture banks %}{% author_link "Iain M. Banks" %}{% endcapture %}
{% capture bankss %}{% author_link "Iain M. Banks" possessive %}{% endcapture %}
{% capture banks_lastname %}{% author_link "Iain M. Banks" link_text="Banks" %}{% endcapture %}
{% capture bankss_lastname %}{% author_link "Iain M. Banks" link_text="Banks" possessive %}{% endcapture %}
{% capture culture %}{% series_link "Culture" %}{% endcapture %}
{% capture surface_detail %}{% book_link "Surface Detail" %}{% endcapture %}

{% capture stross %}{% author_link "Charles Stross" %}{% endcapture %}
{% capture strosss %}{% author_link "Charles Stross" possessive %}{% endcapture %}
{% capture stross_lastname %}{% author_link "Charles Stross" link_text="Stross" %}{% endcapture %}
{% capture strosss_lastname %}{% author_link "Charles Stross" link_text="Stross" possessive %}{% endcapture %}
{% capture a_colder_war %}{% short_story_link "A Colder War" %}{% endcapture %}
```
