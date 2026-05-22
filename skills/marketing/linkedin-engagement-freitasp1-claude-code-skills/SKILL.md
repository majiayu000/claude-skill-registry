---
name: linkedin-engagement
description: LinkedIn Content-Erstellung, Engagement und Monitoring für B2B/Manufacturing. Regionale Anpassung (US/EU/Asien), Artikel mit Teasern, Bildgenerierung via Gemini, Kommentar-Monitoring.
---

# LinkedIn Engagement Skill

## Konfiguration

**LinkedIn-Profil:** Lara Knuth (echtes Profil)
**Unternehmen:** fabrikIQ / Dresden AI Insights
**Fokus:** MES, OEE, Fertigungsdatenanalyse, KMU-Digitalisierung

**Ziel-Regionen:**
- **Primär:** DACH (DE/AT/CH), USA, Kanada
- **Sekundär:** UK, Nordics, Benelux
- **Tertiär:** Japan, Südkorea, Südostasien

**Fokus-Hashtags:**
- DE: #Fertigung #Industrie40 #OEE #MES #Digitalisierung #KMU #Qualitaetssicherung
- EN: #Manufacturing #Industry40 #SmartFactory #MES #OEE #DigitalTransformation #LeanManufacturing

---

## Slash-Commands

### /linkedin-post [region]
**Zweck:** Generiert regionsspezifischen LinkedIn-Post

**Parameter:**
- `region`: us | eu | asia (default: eu)
- `type`: text | article-teaser | poll (default: text)
- `image`: true | false (default: false)

**Workflow:**
1. Erfasse Thema/Kernaussage
2. Wähle Template basierend auf Region
3. Generiere Post mit Anti-AI-Detection
4. Optional: Generiere Bild via Gemini
5. Füge optimierte Hashtags hinzu
6. Zeige Vorschau zur Freigabe

**Ausgabeformat:**
```
## LinkedIn Post [Region: EU]

### Post-Text:
[Generierter Text]

### Hashtags (5):
#Hashtag1 #Hashtag2 ...

### Bild-Prompt (falls angefordert):
[Gemini-Prompt für Bildgenerierung]

### Beste Posting-Zeit:
[Region-spezifische Empfehlung]

### Checkliste:
- [ ] Kein AI-Slop?
- [ ] Erste 2 Zeilen = Hook?
- [ ] CTA vorhanden?
```

---

### /linkedin-article [region]
**Zweck:** Erstellt LinkedIn-Artikel MIT Teaser-Post

**Workflow:**
1. Erfasse Artikel-Thema und Kernpunkte
2. Generiere Artikel-Struktur (800-1500 Wörter)
3. Erstelle separaten Teaser-Post (max 300 Zeichen vor "...mehr")
4. Generiere Header-Bild via Gemini
5. Optimiere SEO (Titel, Beschreibung)

**Ausgabeformat:**
```
## LinkedIn Artikel: [Titel]

### Teaser-Post (für Feed):
[Hook-Text, max 300 Zeichen]

[Link zum Artikel]

#Hashtags

---

### Artikel-Inhalt:

**Titel:** [SEO-optimiert]

**Intro:** [Hook, 2-3 Sätze]

**Hauptteil:**
[Strukturierter Content mit Zwischenüberschriften]

**Fazit:** [Call-to-Action]

---

### Header-Bild Prompt:
[Gemini-Prompt für 1200x627 Header]

### SEO-Daten:
- Titel: [max 60 Zeichen]
- Beschreibung: [max 160 Zeichen]
- Keywords: [...]
```

---

### /linkedin-comment [url]
**Zweck:** Generiert Value-First Kommentar für fremden Post

**Workflow:**
1. Lade Post-Inhalt (via URL oder Beschreibung)
2. Analysiere Autor-Region (Name, Sprache, Unternehmen)
3. Generiere Kommentar angepasst an Region
4. Prüfe Anti-AI-Detection

**Regeln:**
- Erst Mehrwert, dann (optional) eigene Erfahrung
- Keine direkte Werbung
- Authentische Reaktion auf Inhalt
- Frage stellen fördert Engagement

**Ausgabeformat:**
```
## Kommentar für: [Post-Titel/Autor]

**Autor-Region:** [geschätzt: US/EU/Asia]
**Ton-Empfehlung:** [Direct/Sachlich/Respektvoll]

### Vorgeschlagener Kommentar:
[Text, 50-150 Wörter]

### Alternative (kürzer):
[Text, 20-50 Wörter]
```

---

### /linkedin-scan
**Zweck:** Scannt relevante Hashtags/Influencer nach Engagement-Opportunities

**Workflow:**
1. Durchsuche Hashtags: #Manufacturing, #MES, #OEE, #Industrie40
2. Identifiziere Posts mit hohem Engagement-Potenzial
3. Priorisiere nach: Relevanz, Autor-Reichweite, Aktualität
4. Zeige Top 10 mit Kommentar-Empfehlung

**Ausgabeformat:**
```
## LinkedIn Scan: [Datum]

### Engagement-Opportunities (Top 10)

1. **[Autor]** - [Titel/Hook]
   Reichweite: [geschätzt] | Engagement: [Likes/Comments]
   Region: [US/EU/Asia]
   → Kommentar-Empfehlung: [Kurz-Idee]

2. ...

### Trending Topics diese Woche:
- [Topic 1]: [Warum relevant]
- [Topic 2]: ...
```

---

### /linkedin-monitor
**Zweck:** Überwacht eigene Posts auf neue Kommentare, schlägt Antworten vor

**Workflow:**
1. Lade Liste eigener geposteter Inhalte (aus tracking.md)
2. Prüfe jeden Post auf neue Kommentare
3. Analysiere Kommentar-Inhalt und Autor
4. Generiere Antwort-Vorschläge

**Ausgabeformat:**
```
## LinkedIn Monitor: [Datum]

### Neue Kommentare (seit letztem Check)

**Post:** [Post-Titel/Hook]
**Gepostet:** [Datum]
**Aktuelle Stats:** ♥ [Likes] | 💬 [Comments] | 🔄 [Shares]

#### Neuer Kommentar von [Name] ([Position]):
> "[Kommentar-Text]"

**Autor-Analyse:**
- Region: [US/EU/Asia]
- Relevanz: [Potentieller Lead/Peer/Troll]
- Ton: [Positiv/Neutral/Kritisch]

**Antwort-Vorschlag:**
[Generierte Antwort, regional angepasst]

**Alternative (kürzer):**
[Kürzere Version]

---

### Antwort-Priorität:
1. 🔴 DRINGEND: [Kritische Fragen, potentielle Leads]
2. 🟡 WICHTIG: [Fachliche Diskussionen]
3. 🟢 OPTIONAL: [Einfache Zustimmungen]
```

---

### /linkedin-image [prompt]
**Zweck:** Generiert LinkedIn-optimiertes Bild via Gemini

**Integration mit gemini-image-gen Skill:**
```python
# Verwendet GOOGLE_AI_API_KEY aus Environment
from google import genai
client = genai.Client(api_key=os.environ.get("GOOGLE_AI_API_KEY"))

# Modelle:
# - gemini-2.5-flash-image: Schnell, gut für einfache Grafiken
# - gemini-3-pro-image-preview: Höhere Qualität, komplexere Szenen
```

**LinkedIn Bild-Formate:**
| Typ | Größe | Verwendung |
|-----|-------|------------|
| Post-Bild | 1200x1200 | Quadratisch, Feed-optimiert |
| Artikel-Header | 1200x627 | 1.91:1 Ratio |
| Carousel-Slide | 1080x1080 | PDF-Upload |

**Optimierte Prompts für Manufacturing:**
```
"Clean, professional infographic showing [TOPIC].
Modern flat design, blue and white color scheme,
minimal text, manufacturing/industrial context.
LinkedIn business style, 1200x1200px"
```

**Ausgabeformat:**
```
## LinkedIn Bild generiert

**Prompt verwendet:**
[Optimierter Prompt]

**Modell:** gemini-2.5-flash-image
**Format:** 1200x1200 (Post) / 1200x627 (Article)

**Datei:** [Pfad zur generierten Datei]

**Verwendung:**
- [ ] Als Post-Bild hochladen
- [ ] Als Artikel-Header
- [ ] Für Carousel (weitere Slides nötig?)
```

---

### /linkedin-analytics
**Zweck:** Zeigt Performance-Übersicht der geposteten Inhalte

**Metriken:**
- Impressions
- Engagement Rate (Likes + Comments + Shares / Impressions)
- Click-Through Rate (für Artikel)
- Follower-Wachstum

**Ausgabeformat:**
```
## LinkedIn Analytics: [Zeitraum]

### Top Performer

| Post | Datum | 👁 Impressions | ♥ Likes | 💬 Comments | ER% |
|------|-------|---------------|---------|-------------|-----|
| [Titel] | [Datum] | [X] | [Y] | [Z] | [%] |

### Insights:
- Beste Posting-Zeit: [Tag/Uhrzeit]
- Beste Content-Art: [Text/Artikel/Poll]
- Beste Hashtags: [Top 3]

### Empfehlungen:
- [Konkrete Handlungsempfehlung basierend auf Daten]
```

---

## Regionale Templates

### US/Kanada Template

**Stil:** Direct, Story-driven, Personal Brand
**Sprache:** Englisch
**Hashtags:** 3-5, am Ende

**Struktur:**
```
[Hook - kontrovers oder überraschend, 1 Zeile]

[Leerzeile - wichtig für Mobile!]

[Personal Story mit konkreten Zahlen, 2-3 Sätze]

[Insight/Lesson, Bullet Points OK aber nicht genau 3]

[Vulnerable Admission - was ging schief]

[Soft CTA - Frage an Community]

#Manufacturing #MES #OEE #DigitalTransformation
```

**Verboten:**
- "I'm thrilled to announce"
- "Excited to share"
- "I'm humbled"
- Mehr als 5 Emojis

**Funktioniert:**
- Konkrete Zahlen: "Reduced downtime by 23%"
- Hot Takes: "Unpopular opinion: MES is overkill for most SMBs"
- Lessons learned mit Vulnerabilität
- "Here's what I learned after..."

---

### EU/DACH Template

**Stil:** Sachlich, Fakten-basiert, Understatement
**Sprache:** Deutsch oder Englisch (je nach Zielgruppe)
**Hashtags:** 3-5, DE-Varianten

**Struktur:**
```
[Sachliche Eröffnung - Thema klar benennen]

[Kontext mit Daten/Zahlen aus echten Projekten]

[Pragmatischer Insight - was funktioniert, was nicht]

[Optional: Normen-Referenz (DIN, ISO, VDI)]

[Offene Frage - keine rhetorische]

#Fertigung #OEE #Industrie40 #MES #Digitalisierung
```

**Verboten:**
- Übertreibungen ("revolutionär", "game-changer")
- Zu viel Selbst-Promotion
- Amerikanische Hustle-Culture
- "Ich hab alles richtig gemacht"

**Funktioniert:**
- Case Studies mit Methodik
- Normative Referenzen
- "So haben wir es gemacht" (Team-Fokus)
- Kritische Reflexion

---

### Asien Template (Japan, Korea, Südostasien)

**Stil:** Respektvoll, Beziehungs-first, indirekt
**Sprache:** Englisch (international)
**Hashtags:** 3-4, konservativ

**Struktur:**
```
[Höfliche Einleitung - Beobachtung, nicht Belehrung]

[Gemeinsames Lernen - "I noticed...", "I was impressed by..."]

[Eigene Erfahrung als Angebot, nicht als Expertise]

[Respektvolle Frage - Interesse an lokaler Perspektive]

#Manufacturing #Industry40 #QualityManagement
```

**Verboten:**
- Direkte Kritik
- "Ich weiß es besser"
- Zu schnelle Geschäftsanbahnung
- Kulturelle Stereotypen

**Funktioniert:**
- Kaizen/Monozukuri als Anknüpfungspunkt (Japan)
- Respekt für lokale Expertise
- Langfristiger Beziehungsaufbau
- Fragen statt Aussagen

---


## Menschliche Authentizität vs KI-Sprache

### Wissenschaftlich belegte KI-Marker (2024/2025 Research)

**Typische KI-Signale die VERMIEDEN werden müssen:**

| Merkmal | KI-typisch | Menschlich |
|---------|-----------|------------|
| Satzlänge | Gleichmäßig 15-20 Wörter | Variiert stark: 3 bis 40+ Wörter |
| Absätze | Identische Länge | Chaotisch, unterschiedlich |
| Satzzeichen | Perfekt, viele Em-Dashes (—) | Gelegentlich falsch, Kommafehler |
| Vokabular | "Furthermore", "Moreover", "Delve" | Umgangssprache, Füllwörter |
| Struktur | Immer Hook-Body-CTA | Manchmal kein Fazit, abrupt |
| Emotion | "I'm excited", "I'm thrilled" | Nüchtern oder echt frustriert |
| Listen | Exakt 3 oder 5 Punkte | 2, 4, 7 - ungerade Zahlen OK |
| Formatierung | Perfekte Markdown-Struktur | Inkonsistent |

### MENSCHLICHE UNPERFEKTION EINBAUEN

**Gezielt menschliche Marker setzen (subtil, nicht übertrieben):**

1. **Rechtschreibung/Tippfehler (max 1-2 pro Post, natürlich):**
   - "Mitarbeier" statt "Mitarbeiter"
   - "das" vs "dass" Verwechslung
   - Doppelte Buchstaben: "Maschiene"
   - Fehlender Buchstabe: "Frtigung"
   - WICHTIG: Nur plausible Tippfehler, keine absichtlich dummen Fehler

2. **Zeichensetzung-Varianten:**
   - Fehlendes Komma: "Aber naja das ist ein anderes Thema"
   - Punkt statt Fragezeichen: "Was denkt ihr."
   - Kein Punkt am Ende (informell)
   - Doppeltes Leerzeichen (passiert beim Tippen)

3. **Grammatik-Abweichungen (natürlich, nicht falsch):**
   - Satzabbrüche: "Das Problem war... egal."
   - Nachgeschobene Gedanken: "Achso, hab ich vergessen:"
   - Umgangssprache: "Ist halt so" statt "Es ist so"
   - Gedankensprünge ohne Überleitung

4. **Strukturelle Unperfektion:**
   - Absätze unterschiedlich lang (2 Zeilen, dann 5, dann 1)
   - Manchmal nur 1 Zeile als Absatz
   - Kein offensichtliches Muster
   - Abruptes Ende OK (kein Zwangs-CTA)
   - Manchmal vergessener Absatz-Umbruch

### VERBOTENE FORMATIERUNG

**KEINE dieser Elemente in Posts verwenden:**

- Emojis als Aufzählungspunkte (Rakete vor Punkt 1 etc)
- Perfekte Emoji-Listen mit gleichen Abständen
- Checkboxen als Listenpunkte
- Icons/Symbole am Zeilenanfang
- Horizontale Trenner (--- oder ===)
- Überschriften in Posts (## Titel)
- Code-Blöcke oder Backticks
- Perfekt ausgerichtete Tabellen
- Fettdruck für jeden wichtigen Begriff

**ERLAUBT (sehr sparsam):**
- 1-2 Emojis am Ende oder als Akzent (nicht in jedem Post)
- Normale Zahlen für Listen (1. 2. 3.)
- Bullet Points ohne Emojis (- Punkt)
- Gelegentlich ein Pfeil (->)

### KI-PHRASEN: TOTALE BLACKLIST

**Deutsche KI-Marker:**
- "In der heutigen Zeit"
- "Wie wir alle wissen"
- "Es ist allgemein bekannt"
- "Zusammenfassend lässt sich sagen"
- "Es bleibt festzuhalten"
- "Abschließend möchte ich betonen"
- "Dies führt uns zu der Erkenntnis"
- "In diesem Zusammenhang"
- "Darüber hinaus"
- "Des Weiteren"
- "Schlussendlich"
- "Es ist von entscheidender Bedeutung"

**Englische KI-Marker:**
- "Delve into" / "Delve deeper"
- "Leverage synergies"
- "In today's fast-paced world"
- "It's important to note that"
- "Furthermore" / "Moreover" / "Additionally"
- "This begs the question"
- "Needless to say"
- "At the end of the day"
- "Game-changer" / "Revolutionary"
- "Seamlessly integrate"
- "Navigate the complexities"
- "Unlock the potential"
- "Fostering innovation"

**Em-Dash Überverwendung (—):**
- KI nutzt exzessiv Em-Dashes zwischen Satzteilen
- Menschen nutzen eher Gedankenstriche (-) oder einfach Kommas
- Oder Klammern (so wie hier)
- Max 1 Em-Dash pro Post wenn überhaupt

### AUTHENTISCHE ALTERNATIVEN

| KI-Phrase | Menschliche Alternative |
|-----------|------------------------|
| "I'm thrilled to announce" | "Endlich fertig:" oder direkt ins Thema |
| "Here are 5 key takeaways" | "Was hat funktioniert?" |
| "Let me share my journey" | "Kurze Geschichte dazu:" |
| "This changed everything" | "Hat geholfen" |
| "You won't believe" | "Überraschend war:" |
| "In der heutigen Zeit" | "Momentan" / "Gerade" / weglassen |
| "Zusammenfassend" | "Also:" / "Heißt:" |
| "Darüber hinaus" | "Außerdem" / "Und noch:" |
| "Key learnings" | "Was wir gelernt haben" |
| "Moving forward" | weglassen oder "als nächstes" |
| "It's worth noting" | einfach direkt sagen |
| "I'm excited to" | weglassen, direkt zur Sache |

### BEISPIELE: KI vs MENSCH

**KI-generiert (SCHLECHT):**
```
I'm thrilled to announce that we've successfully implemented a new OEE tracking system!

Here are 5 key takeaways:

Punkt 1 Real-time visibility
Punkt 2 23% efficiency gain
Punkt 3 Data-driven decisions
Punkt 4 Seamless integration
Punkt 5 Team empowerment

This truly changed everything for us. What's your experience with OEE?

#Manufacturing #Industry40 #OEE #DigitalTransformation #SmartFactory
```

**Menschlich geschrieben (GUT):**
```
Letzte Woche endlich unser OEE-Tracking live geschaltet.

Ehrlich gesagt war der Weg dahin holprig - erste Excel-Version hat keiner benutzt, zu kompliziert. Jetzt simpler und die Schichtleiter tragen tatsächlich ein.

23% weniger Stillstand seit dem. Ob das so bleibt weiß ich nicht, Anfangs-Effekt vielleicht

Was mich interessiert: wie kriegt ihr eure Leute dazu, sowas auch wirklich zu nutzen.

#Fertigung #OEE #MES
```

---
## Anti-AI-Detection Regeln (LinkedIn-spezifisch)

### VERBOTEN (LinkedIn AI-Slop):

**Phrasen:**
- "I'm thrilled to announce..."
- "Excited to share that..."
- "I'm humbled and honored..."
- "Here are 5 key takeaways:"
- "Let me tell you a story..."
- "If you found this valuable, like and share"
- "Agree? 👇"
- "DM me 'STRATEGY' for..."
- "I helped 100+ companies achieve..."
- "This changed everything for me"
- "You won't believe what happened next"

**Strukturen:**
- Exakt 5 Bullet Points
- Perfekte Emoji-Zeilen (🎯 Point 1 / 🚀 Point 2)
- Identische Absatzlängen
- "Hook → Story → Lesson → CTA" zu offensichtlich
- Jeder Satz neue Zeile (Poetry-Style Spam)

**Emojis:**
- 🚀🔥💡🎯💪 Combo
- Mehr als 3-4 pro Post
- Emoji am Zeilenanfang (Liste)

### AUTHENTIZITÄTS-SIGNALE:

**Sprachlich:**
1. Variierende Satzlängen - kurz. Dann länger, weil der Gedanke es braucht.
2. Unvollständige Gedanken - "Aber naja, das ist ein anderes Thema."
3. Regionale Ausdrücke - DE: "Naja", "halt", "irgendwie" / US: "tbh", "ngl"
4. Nachträgliche Korrekturen - "Edit: Forgot to mention..."
5. Genuine Fragen ohne offensichtliche Antwort

**Inhaltlich:**
1. Spezifische Kontexte statt generischer Claims
2. Fehler zugeben - "Unser erster Versuch war ein Reinfall"
3. Nuancierte Meinungen - "Kommt drauf an..."
4. Lokale Referenzen (Messen, Verbände, Städte)
5. Zeitliche Einordnung - "Letzte Woche bei einem Kunden in Sachsen..."

**Strukturell:**
1. Nicht jeder Post braucht CTA
2. Manchmal nur Frage, keine Antwort
3. Absätze unterschiedlich lang
4. Gelegentlich Typos (max 1-2)

---

## Hashtag-Strategie

### Deutsch (DACH)
| Reichweite | Hashtags |
|------------|----------|
| Hoch (>100k) | #Industrie40 #Digitalisierung #KMU |
| Mittel (10-100k) | #Fertigung #OEE #MES #Produktion |
| Nische (<10k) | #Qualitaetssicherung #Maschinendaten #SmartFactory |

**Empfehlung:** 1 Hoch + 2 Mittel + 2 Nische = 5 Hashtags

### Englisch (International)
| Reichweite | Hashtags |
|------------|----------|
| Hoch (>500k) | #Manufacturing #Industry40 #DigitalTransformation |
| Mittel (50-500k) | #SmartFactory #LeanManufacturing #OEE |
| Nische (<50k) | #MES #ManufacturingExcellence #ShopFloor |

### Hashtag-Regeln:
- Hashtags am Ende des Posts (nicht inline)
- Keine Hashtags im ersten Absatz (stört Hook)
- Max 5 Hashtags (mehr = spammy)
- Mix aus Reichweite-Stufen
- Keine erfundenen Hashtags

---

## Posting-Zeiten

### Optimal nach Region:

| Region | Beste Tage | Beste Zeiten (lokal) |
|--------|-----------|---------------------|
| DACH | Di-Do | 08:00-09:00, 17:00-18:00 |
| USA East | Di-Do | 08:00-10:00, 17:00-18:00 |
| USA West | Di-Do | 07:00-09:00, 16:00-17:00 |
| UK | Di-Do | 08:00-09:00, 17:00-18:00 |
| Asien | Mi-Fr | 09:00-11:00 (lokale Zeit) |

### Vermeiden:
- Montag Morgen (zu viel Noise)
- Freitag Nachmittag (Wochenend-Modus)
- Wochenende (außer Sonntag Abend für Montag-Sichtbarkeit)

---

## Artikel-Teaser Formel

### Hook-Struktur (max 300 Zeichen vor "...mehr"):
```
[Provokante These oder überraschende Zahl]

[1 Satz Kontext]

[Neugier wecken: "Im Artikel zeige ich..." oder "3 Dinge, die wir gelernt haben:"]
```

### Beispiel:
```
85% der OEE-Implementierungen liefern nicht den erwarteten ROI.

Wir haben 12 Projekte analysiert und die 3 häufigsten Fehler identifiziert.

Im Artikel: Konkrete Zahlen und wie ihr sie vermeidet 👇

[LINK]

#OEE #Manufacturing #Fertigung
```

---

## Tracking-Log

### Gepostete Inhalte

| Datum | Typ | Titel/Hook | Region | URL | Status |
|-------|-----|------------|--------|-----|--------|
| [Datum] | Post/Artikel | [Kurztitel] | EU/US | [URL] | ✅ Gepostet |

### Performance-Historie

| Datum | Post | 👁 Impressions | ♥ Likes | 💬 Comments | 🔄 Shares | ER% |
|-------|------|---------------|---------|-------------|-----------|-----|
| [Datum] | [Titel] | [X] | [Y] | [Z] | [W] | [%] |

### Kommentar-Queue (eigene Posts)

| Post | Neuer Kommentar von | Inhalt (Kurz) | Beantwortet? |
|------|--------------------|--------------:|--------------|
| [Titel] | [Name] | [Kurzzitat] | ⏳/✅ |

---

## Gemini-Integration für Bilder

### Setup
```bash
# Environment Variable setzen
export GOOGLE_AI_API_KEY="your-key-here"

# Dependencies
pip install google-genai pillow python-dotenv
```

### LinkedIn-optimierte Prompts

**Infografik (OEE/Daten):**
```
Professional infographic showing OEE calculation breakdown.
Clean flat design, blue (#0077B5 LinkedIn blue) and white.
Icons for Availability, Performance, Quality.
Minimal text, data visualization style.
1200x1200px, white background.
```

**Header für Artikel:**
```
Modern manufacturing facility abstract visualization.
Digital data overlay, blue tones, professional look.
No text, suitable for article header.
1200x627px, LinkedIn article format.
```

**Carousel-Slide:**
```
Single slide for LinkedIn carousel about [TOPIC].
Large bold headline area, clean infographic style.
Blue and white, professional B2B manufacturing.
1080x1080px square format.
```

### Generierungs-Workflow:
1. `/linkedin-image [Thema]`
2. Skill generiert optimierten Prompt
3. Aufruf von Gemini API
4. Speichern mit Timestamp
5. Anzeige Vorschau + Verwendungshinweise

---

## Persona: Lara Knuth

**LinkedIn-Profil:**
- Name: Lara Knuth (echt)
- Position: Gründerin fabrikIQ / Dresden AI Insights
- Standort: Dresden, Sachsen
- Hintergrund: MES-Expertin, COO/CEO Erfahrung in KMU

**Authentizitäts-Elemente:**
- Zwillinge (Zeitmangel, Multitasking - sparsam erwähnen)
- Praktische Erfahrung aus echten Projekten
- Sachsen/DACH-Perspektive
- Kritisch gegenüber Hype, pragmatisch

**Schreibstil LinkedIn:**
- Professioneller als Reddit, aber nicht steif
- Deutsch für DACH, Englisch für International
- Zahlen und Fakten, aber mit Storytelling
- Fehler zugeben, Learnings teilen

---

## Qualitäts-Checkliste vor Posting

### Post/Artikel:
- [ ] Keine AI-Slop Phrasen?
- [ ] Hook in ersten 2 Zeilen?
- [ ] Satzlängen variieren?
- [ ] Authentische Stimme (Lara)?
- [ ] Regional passend (US/EU/Asia)?
- [ ] Hashtags am Ende (max 5)?
- [ ] Bild falls sinnvoll?
- [ ] Keine übertriebenen Claims?

### Kommentar:
- [ ] Value-First (nicht Werbung)?
- [ ] Passend zur Autor-Region?
- [ ] Unter 150 Wörter?
- [ ] Genuine Reaktion auf Inhalt?

### Antwort auf eigene Posts:
- [ ] Zeitnah (< 24h)?
- [ ] Persönlich, nicht generisch?
- [ ] Diskussion weiterführend?
- [ ] Bei Kritik: sachlich bleiben?
