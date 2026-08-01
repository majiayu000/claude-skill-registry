---
name: jurisdictions-zadorian-search-engineer
description: '> Style/formatting: Follow ~/.claude/skills/word-doc-generator/SKILL.md'
---

# SOUTH KOREA JURISDICTION TEMPLATE

> **Style/formatting:** Follow `~/.claude/skills/word-doc-generator/SKILL.md`

## Registry: Supreme Court Internet Registry Office

**URL:** http://www.iros.go.kr/ / https://www.ftc.go.kr/
**Free Access:** Limited (requires Korean ID for full access)
**Data Available:** Company details, directors, capital (limited for foreigners)

---

## TEMPLATE

```markdown
### South Korean Corporate Records

**[COMPANY - ENGLISH]** ([COMPANY - 한국어]) (Registration Number [NUMBER]) is registered in South Korea.[^X]

| | |
|---|---|
| **Business Registration Number** | [NUMBER] |
| **Corporate Registration Number** | [NUMBER] |
| **Status** | [Active / Dissolved] |
| **Incorporated** | [DATE] |
| **Legal Form** | [주식회사 / 유한회사] |
| **Registered Office** | [ADDRESS], South Korea |
| **Stated Capital** | KRW [AMOUNT] |

#### Representative Director (대표이사)

**[NAME - Korean]** ([NAME - Romanized]) serves as representative director.[^X]

#### Directors

| Name | Position |
|------|----------|
| **[NAME]** | [이사 / 감사] |
```

---

## STANDARD PHRASES

**Company status:**
> **[COMPANY]** is registered in South Korea as a [chusik hoesa / yuhan hoesa].[^X]

**Directors:**
> Korean corporate records identify **[NAME]** as representative director (대표이사).[^X]

**Listed company:**
> **[COMPANY]** is listed on the Korea Exchange (KOSPI/KOSDAQ: [CODE]).[^X]

**Chaebol connection:**
> **[COMPANY]** is affiliated with the [CHAEBOL NAME] business group.[^X]

---

## LEGAL FORMS

| Korean | Romanization | English | Min Capital |
|--------|--------------|---------|-------------|
| **주식회사** | Chusik Hoesa | Stock Company | KRW 100M |
| **유한회사** | Yuhan Hoesa | Limited Company | KRW 10M |
| **유한책임회사** | Yuhan Chaegim Hoesa | Limited Liability Company | KRW 1 |
| **합명회사** | Hapmyeong Hoesa | General Partnership | None |
| **합자회사** | Hapja Hoesa | Limited Partnership | None |

---

## CHAEBOLS (Major Business Groups)

| Group | Primary Business |
|-------|------------------|
| **Samsung** | Electronics, shipbuilding, construction |
| **Hyundai** | Automotive, heavy industry, retail |
| **SK** | Energy, telecom, semiconductors |
| **LG** | Electronics, chemicals |
| **Lotte** | Retail, hospitality, food |
| **Hanwha** | Defense, solar, insurance |
| **CJ** | Food, entertainment, logistics |

---

## REGULATORS

| Regulator | Full Name | Covers |
|-----------|-----------|--------|
| **FSC** | Financial Services Commission | Financial institutions |
| **KFTC** | Korea Fair Trade Commission | Competition, chaebol |
| **KRX** | Korea Exchange | Stock markets |

---

## SOURCES

| Source | URL | Data |
|--------|-----|------|
| IROS | http://www.iros.go.kr/ | Commercial registry |
| DART | https://dart.fss.or.kr/ | Listed company filings |
| KRX | http://www.krx.co.kr/ | Stock exchange |
| KFTC | https://www.ftc.go.kr/ | Business group info |

---

## NOTES

- Full registry access requires Korean ID (resident registration)
- DART provides good disclosure for listed companies
- Chaebol relationships important for understanding Korean business
- Consider cross-shareholding structures in business groups

---

## FOOTNOTE EXAMPLES

```markdown
[^1]: http://www.iros.go.kr/

[^2]: https://dart.fss.or.kr/

[^3]: Korea Fair Trade Commission
```

---

## SOURCES BY SECTION

_Automatically mapped from IO Matrix_

### Corporate Registry

**Cookbooks:** `company/COMPANY_OVERVIEW.cookbook.md, company/DIRECTORS_OFFICERS.cookbook.md, company/OWNERSHIP_SHAREHOLDERS.cookbook.md`

**Actions:** `SEARCH_REGISTRY, CORPORELLA_LOOKUP`

| Source | URL |
|--------|-----|
| Searches company disclosure documents from] the pr | http://dart.fss.or.kr/dsab001/main.do |
| The Data Analysis, Retrieval and] Transfer System | http://englishdart.fss.or.kr/dsbc001/main.do |
| Saramin is a Korean job] listings site that also p | https://s3.amazonaws.com/kraken-sta |
| Korean online government platform launched] in 201 | http://startbiz.go.kr/index.do |
| BizInKorea provides information about Korean] comp | http://www.bizinkorea.org/main.jsp |

### Land Registry

**Cookbooks:** `company/PROPERTY_REAL_ESTATE.cookbook.md`

**Actions:** `SEARCH_LAND_REGISTRY`

| Source | URL |
|--------|-----|
| Korea Intellectual Property Office patent] search | http://lod.kipo.kr/data/search |

