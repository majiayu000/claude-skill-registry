---
name: source-verification
description: Journalism source verification and fact-checking workflows. Use when verifying claims, checking source credibility, investigating social media accounts, reverse image searching, or building verification trails. Essential for reporters, fact-checkers, and researchers working with unverified information.
---

# Source verification methodology

Systematic approaches for verifying sources, claims, and digital content in journalism and research.

## Verification framework

### The SIFT method

**S - Stop**: Don't immediately share or use unverified information
**I - Investigate the source**: Who is behind the information?
**F - Find better coverage**: What do other reliable sources say?
**T - Trace claims**: Find the original source of the claim

### Source credibility checklist

```markdown
## Source evaluation template

### Basic identification
- [ ] Full name/organization identified
- [ ] Contact information verifiable
- [ ] Professional credentials checkable
- [ ] Online presence consistent across platforms

### Expertise assessment
- [ ] Relevant expertise for the claim being made
- [ ] Track record in this subject area
- [ ] Recognized by peers in the field
- [ ] No history of spreading misinformation

### Motivation analysis
- [ ] Potential conflicts of interest identified
- [ ] Financial stake in the outcome?
- [ ] Political or ideological motivation?
- [ ] Personal grievance involved?

### Corroboration
- [ ] Can claims be independently verified?
- [ ] Do other credible sources confirm?
- [ ] Is documentary evidence available?
- [ ] Are there contradicting sources?
```

## Digital verification techniques

### Social media account analysis

```markdown
## Account verification checklist

### Account age and history
- Creation date (older accounts more credible)
- Posting frequency and patterns
- Gaps in activity (dormant then suddenly active?)
- Language consistency over time

### Network analysis
- Follower/following ratio
- Quality of followers (real accounts vs. bots)
- Interaction patterns (who engages with them?)
- Mutual connections with verified accounts

### Content patterns
- Original content vs. reshares only
- Topics discussed consistently
- Geographic indicators in posts
- Time zone of posting activity

### Red flags
- Recently created account making bold claims
- Sudden pivot in topics or tone
- Coordinated behavior with other accounts
- Stock photo profile picture
- Generic bio with no specifics
```

### Reverse image search workflow

```markdown
## Image verification process

### Step 1: Reverse image search
Tools to use:
- Google Images (images.google.com)
- TinEye (tineye.com)
- Yandex Images (yandex.com/images) - best for faces
- Bing Visual Search

### Step 2: Check metadata (EXIF)
- Original capture date/time
- Camera/device information
- GPS coordinates (if available)
- Software used to edit

Tools:
- Jeffrey's EXIF Viewer (exif.regex.info)
- FotoForensics (fotoforensics.com)
- InVID verification plugin

### Step 3: Analyze image content
- Weather conditions (match reported date?)
- Shadows (consistent with time of day?)
- Signage/text (correct language for location?)
- Architecture (matches claimed location?)
- Clothing (seasonal appropriateness?)

### Step 4: Find original source
- Earliest appearance online
- Original photographer/source
- Context of first publication
- Has it been used in other contexts?
```

### Video verification

```markdown
## Video verification checklist

### Technical analysis
- [ ] Resolution consistent throughout
- [ ] Audio sync matches video
- [ ] No visible editing artifacts
- [ ] Lighting consistent across frames
- [ ] Shadows behave naturally

### Content analysis
- [ ] Location identifiable and verifiable
- [ ] Time indicators (sun position, shadows)
- [ ] Weather matches historical records
- [ ] Background details consistent
- [ ] People's clothing appropriate for context

### Metadata check
- [ ] Upload date vs. claimed event date
- [ ] Original source identified
- [ ] Chain of custody traceable
- [ ] Multiple angles available?

### Tools
- InVID/WeVerify browser extension
- YouTube DataViewer (citizenevidence.amnestyusa.org)
- Frame-by-frame analysis tools
```

## Document verification

### PDF and document analysis

```markdown
## Document verification steps

### Metadata examination
- Creation date and modification history
- Author information
- Software used to create
- Embedded fonts and images

### Visual inspection
- Consistent formatting throughout
- Font matching (no spliced text)
- Alignment of text and images
- Quality consistent across pages
- Signatures appear authentic

### Content verification
- Dates internally consistent
- Names spelled correctly throughout
- Reference numbers valid
- Contact information verifiable
- Letterhead matches known examples

### Provenance
- How was document obtained?
- Chain of custody documented?
- Original vs. copy?
- Can source provide additional context?
```

## Building a verification trail

### Documentation template

```markdown
## Verification record

**Claim being verified:**
[State the specific claim]

**Source of claim:**
- Name/account:
- Platform:
- Date first seen:
- URL (archived):

**Verification steps taken:**

### Step 1: [Description]
- Action taken:
- Tool/method used:
- Result:
- Screenshot/evidence saved: [filename]

### Step 2: [Description]
- Action taken:
- Tool/method used:
- Result:
- Screenshot/evidence saved: [filename]

[Continue for each step]

**Corroborating sources:**
1. [Source 1] - [What it confirms]
2. [Source 2] - [What it confirms]
3. [Source 3] - [What it confirms]

**Contradicting information:**
1. [Source] - [What it contradicts]

**Confidence assessment:**
- [ ] Verified true
- [ ] Likely true (high confidence)
- [ ] Unverified (insufficient evidence)
- [ ] Likely false (contradicting evidence)
- [ ] Verified false

**Reasoning:**
[Explain your conclusion based on evidence]

**Verification completed by:**
**Date:**
```

## Archiving evidence

### Web archiving best practices

```python
# Save URLs to multiple archives for redundancy
ARCHIVE_SERVICES = [
    'https://web.archive.org/save/',           # Internet Archive
    'https://archive.ph/',                      # Archive.today
    'https://perma.cc/',                        # Perma.cc (requires account)
]

def archive_url(url: str) -> dict:
    """Archive URL to multiple services."""
    results = {}

    # Internet Archive
    try:
        response = requests.get(f'https://web.archive.org/save/{url}')
        if response.status_code == 200:
            results['wayback'] = response.url
    except Exception as e:
        results['wayback_error'] = str(e)

    # Archive.today (requires different approach)
    # ... implementation

    return results
```

### Screenshot documentation

```markdown
## Screenshot best practices

1. **Full page capture**: Use browser extensions for full-page screenshots
2. **Include URL bar**: Shows the source URL
3. **Include timestamp**: System clock visible or add manually
4. **Save metadata**: Note when and how captured
5. **Multiple formats**: Save as PNG (lossless) and PDF
6. **Secure storage**: Hash files and store securely

Recommended tools:
- Hunchly (hunch.ly) - automatic capture and logging
- Screenpresso - full page with annotations
- Browser print-to-PDF - includes URL and date
```

## Interview verification

### Pre-interview source check

```markdown
## Source background check

### Public records
- [ ] Professional licenses verified
- [ ] Court records checked
- [ ] Business registrations confirmed
- [ ] Property records (if relevant)
- [ ] Campaign finance records (if political)

### Professional background
- [ ] LinkedIn profile reviewed
- [ ] Employer confirmed
- [ ] Previous employers contacted
- [ ] Published work reviewed
- [ ] Conference appearances verified

### Social media audit
- [ ] All platforms identified
- [ ] Post history reviewed
- [ ] Connections/followers analyzed
- [ ] Previous statements on topic
- [ ] Any deleted content found?

### Media appearances
- [ ] Previous interviews found
- [ ] Consistency with current claims
- [ ] Other journalists' assessments
- [ ] Any retractions or corrections?
```

### During interview verification

```markdown
## Real-time verification techniques

### Document requests
- Ask for documentation during interview
- Verify documents aren't altered
- Request originals, not copies when possible
- Note document condition and provenance

### Specific detail probing
- Ask for specific dates, names, locations
- Request corroborating witnesses
- Ask "How do you know that?"
- Follow up on vague answers

### Consistency checks
- Note initial version of story
- Return to key points later
- Compare details across tellings
- Flag inconsistencies for follow-up

### Recording best practices
- Get consent (check local laws)
- Use reliable recording equipment
- Backup recording in real-time
- Note non-verbal cues separately
```

## Verification resources

### Essential tools

| Tool | Purpose | URL |
|------|---------|-----|
| InVID/WeVerify | Video verification plugin | weverify.eu |
| TinEye | Reverse image search | tineye.com |
| Wayback Machine | Web archives | web.archive.org |
| CrowdTangle | Social media tracking | crowdtangle.com |
| Hoaxy | Claim spread visualization | hoaxy.osome.iu.edu |
| Media Bias/Fact Check | Source reliability | mediabiasfactcheck.com |
| OpenCorporates | Company records | opencorporates.com |
| OCCRP Aleph | Document search | aleph.occrp.org |

### Training resources

- First Draft News (firstdraftnews.org)
- Bellingcat guides (bellingcat.com/resources)
- Google News Initiative (newsinitiative.withgoogle.com)
- Verification Handbook (verificationhandbook.com)
- SPJ ethics resources (spj.org/ethics)
