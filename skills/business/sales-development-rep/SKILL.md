---
name: sales-development-rep
description: Эксперт SDR. Используй для outbound продаж, prospecting, cold outreach и lead qualification.
---

# Sales Development Representative

Expert knowledge in outbound prospecting, cold outreach, and sales development best practices.

## Core Competencies

```yaml
prospecting:
  icp_identification:
    - "Industry verticals"
    - "Company size/revenue"
    - "Technology stack"
    - "Growth signals"
    - "Funding status"

  account_research:
    - "Company news and triggers"
    - "Recent hires"
    - "Tech adoptions"
    - "Financial events"
    - "Competitive displacement"

  contact_identification:
    - "Buying committee mapping"
    - "Title/role matching"
    - "Seniority levels"
    - "Contact validation"
    - "Email verification"

outreach_execution:
  channels:
    - "Cold email"
    - "Cold calling"
    - "LinkedIn"
    - "Video prospecting"
    - "Direct mail"

  cadence_design:
    touches: "8-12 over 3-4 weeks"
    channel_mix: "Multi-channel approach"
    spacing: "Progressive intervals"

qualification:
  frameworks:
    - "BANT (Budget, Authority, Need, Timeline)"
    - "MEDDIC"
    - "CHAMP"
    - "GPCTBA/C&I"
```

## Daily Activity Targets

```yaml
activity_metrics:
  calls:
    target: "50-80 dials"
    connects: "10-15%"
    conversations: "5-10"

  emails:
    target: "30-50 personalized"
    open_rate: ">40%"
    reply_rate: ">5%"

  linkedin:
    target: "20-30 touches"
    connection_rate: ">30%"
    message_rate: ">10%"

  research:
    time: "1-2 hours"
    new_prospects: "25-50"

output_targets:
  meetings_per_week: "8-12"
  pipeline_per_month: "$150K-250K"
  sql_conversion: "60-70%"
```

## Cold Email Framework

```yaml
email_best_practices:
  structure:
    subject_line:
      length: "3-5 words"
      avoid: "Salesy language, all caps"
      include: "Personalization, curiosity"

    opening:
      type: "Personalized hook"
      research: "Show you did homework"
      length: "1-2 sentences"

    body:
      focus: "Their problem, not your product"
      length: "Under 100 words total"
      value: "Insight or relevant stat"

    cta:
      type: "Single, clear ask"
      examples:
        - "Open to a 15-min call?"
        - "Worth a conversation?"
        - "Would this be relevant?"

  templates:
    trigger_based: |
      Subject: {Trigger event}

      Hi {First Name},

      Saw {company} just {trigger event}. When {similar companies}
      hit this milestone, they typically face {challenge}.

      We helped {reference customer} navigate this by {outcome}.

      Worth a quick call to see if we can help?

    problem_focused: |
      Subject: {Pain point} at {Company}

      Hi {First Name},

      {Role} leaders at {industry} companies tell me their biggest
      challenge is {specific pain point}.

      We've helped {customer} reduce {metric} by {result} in {time}.

      Would it make sense to explore if we can do the same for {Company}?

    referral_request: |
      Subject: Quick question

      Hi {First Name},

      I'm trying to connect with whoever handles {function} at {Company}.

      Might that be you, or could you point me to the right person?
```

## Cold Calling Framework

```yaml
call_framework:
  pattern_interrupt:
    examples:
      - "Hi {Name}, this is {Your Name} from {Company}. Did I catch you at a bad time?"
      - "Hi {Name}, we haven't met yet..."
      - "{Name}? This is {Your Name}. Do you have 30 seconds?"

  permission_based:
    script: |
      "The reason I'm calling is {relevant trigger/reason}.
      I have an idea that might help with {challenge}.
      Mind if I take 30 seconds to explain, then you can decide
      if it's worth continuing?"

  value_proposition:
    duration: "30 seconds max"
    structure:
      - "Who we help"
      - "Problem we solve"
      - "Result we deliver"
      - "Social proof"

  objection_responses:
    not_interested:
      response: "I understand. Out of curiosity, is it the timing,
                 or does {challenge} not resonate?"

    send_info:
      response: "Happy to. What specifically would be most relevant
                 so I don't waste your time?"

    already_have_solution:
      response: "That's actually why I called. Companies using
                 {competitor} tell me {pain point}. Is that your
                 experience too?"

    no_time:
      response: "Totally get it. Would {day/time} work better,
                 or should I follow up by email?"

  booking_the_meeting:
    script: |
      "Based on what you've shared, it sounds like this could be
      relevant. Let me suggest we schedule a quick call with
      {AE name} who can dive deeper.

      Do you have your calendar handy? How does {day} at {time} look?"
```

## LinkedIn Prospecting

```yaml
linkedin_strategy:
  profile_optimization:
    headline: "Value proposition, not job title"
    about: "Customer-focused, results-driven"
    experience: "Achievements with metrics"
    media: "Case studies, testimonials"

  engagement_before_connect:
    activities:
      - "Like and comment on posts"
      - "Engage with shared content"
      - "React to company news"
      - "Follow for 1-2 weeks first"

  connection_request:
    length: "Under 300 characters"
    personalization: "Required"
    templates:
      mutual_connection: |
        Hi {Name}, I see we're both connected to {mutual}.
        I work with {role} at {industry} companies and
        would love to connect.

      content_engagement: |
        Hi {Name}, loved your post on {topic}. Your point
        about {insight} really resonated. Would love to connect.

      trigger_event: |
        Hi {Name}, congratulations on {event}. I work with
        companies going through {similar situation}.
        Would love to connect.

  voice_notes:
    when: "After connection accepted"
    length: "30-45 seconds"
    structure:
      - "Personalized opening"
      - "Reason for reaching out"
      - "Value proposition"
      - "Soft CTA"

  inmails:
    subject: "Keep short (3-5 words)"
    length: "Under 100 words"
    cta: "Question, not ask"
```

## Qualification Frameworks

### BANT

```yaml
bant:
  budget:
    questions:
      - "Do you have budget allocated for this initiative?"
      - "What's the typical investment for projects like this?"
      - "Who owns the budget for this?"
    signals:
      green: "Budget allocated, amount known"
      yellow: "Budget possible but not allocated"
      red: "No budget, no path to budget"

  authority:
    questions:
      - "Who else would be involved in this decision?"
      - "Walk me through your typical evaluation process?"
      - "Have you purchased similar solutions before?"
    signals:
      green: "Decision maker or direct access"
      yellow: "Influencer with champion potential"
      red: "No influence on decision"

  need:
    questions:
      - "What's driving this initiative?"
      - "What happens if you don't solve this?"
      - "What have you tried so far?"
    signals:
      green: "Clear pain, articulated impact"
      yellow: "Problem acknowledged, priority unclear"
      red: "No clear pain or nice-to-have"

  timeline:
    questions:
      - "When do you need this solved by?"
      - "What's driving that timeline?"
      - "What could accelerate or delay this?"
    signals:
      green: "Active project, defined timeline"
      yellow: "Exploring options, no deadline"
      red: "No urgency, 12+ months out"
```

### MEDDIC

```yaml
meddic:
  metrics:
    definition: "Quantifiable business outcomes"
    questions:
      - "What does success look like?"
      - "How will you measure ROI?"
      - "What metrics matter most?"

  economic_buyer:
    definition: "Person with budget authority"
    questions:
      - "Who signs off on investments like this?"
      - "Who controls the budget?"
      - "How do they typically evaluate vendors?"

  decision_criteria:
    definition: "How they'll evaluate solutions"
    questions:
      - "What are your must-haves vs nice-to-haves?"
      - "What will you be comparing?"
      - "How will you score vendors?"

  decision_process:
    definition: "Steps to make a decision"
    questions:
      - "Walk me through your typical buying process?"
      - "Who needs to be involved?"
      - "What approvals are required?"

  identify_pain:
    definition: "Business problem driving urgency"
    questions:
      - "What's the impact of this problem?"
      - "What have you tried?"
      - "What happens if you do nothing?"

  champion:
    definition: "Internal advocate"
    questions:
      - "Who's sponsoring this internally?"
      - "What's in it for them personally?"
      - "Will they advocate for us?"
```

## Cadence Design

```yaml
cadence_structure:
  week_1:
    day_1:
      - "Email 1: Trigger-based cold email"
      - "LinkedIn: Connection request"
    day_2:
      - "Call 1: Pattern interrupt"
      - "Voicemail if no answer"
    day_4:
      - "Email 2: Follow-up with value add"
      - "LinkedIn: Engage with content"

  week_2:
    day_8:
      - "Call 2: Reference previous touchpoints"
    day_10:
      - "Email 3: Different angle/pain point"
      - "LinkedIn: Voice note"
    day_12:
      - "Call 3: Final attempt this week"

  week_3:
    day_15:
      - "Email 4: Social proof/case study"
    day_17:
      - "Call 4: Break-up warning"
    day_19:
      - "LinkedIn: Direct message"

  week_4:
    day_22:
      - "Email 5: Break-up email"
      - "Call 5: Final voicemail"

response_handling:
  positive:
    action: "Book meeting within 48 hours"
    calendar: "Send invite immediately"

  objection:
    action: "Address and re-engage"
    follow_up: "Within 24 hours"

  referral:
    action: "Thank and pursue new contact"
    mention: "Reference original contact"

  no_response:
    action: "Move to nurture"
    revisit: "90 days"
```

## Tools Stack

```yaml
tools:
  sequencing:
    - "Outreach"
    - "SalesLoft"
    - "Apollo"
    - "Instantly"

  data_research:
    - "ZoomInfo"
    - "Apollo"
    - "LinkedIn Sales Navigator"
    - "Clearbit"
    - "Lusha"

  calling:
    - "Orum"
    - "ConnectAndSell"
    - "PhoneBurner"
    - "Aircall"

  crm:
    - "Salesforce"
    - "HubSpot"
    - "Pipedrive"

  email_tools:
    - "Lemlist"
    - "Mailshake"
    - "Reply.io"

  linkedin:
    - "Sales Navigator"
    - "Dux-Soup"
    - "Expandi"
```

## Metrics & KPIs

```yaml
sdr_metrics:
  activity:
    calls_per_day: 60
    emails_per_day: 40
    linkedin_per_day: 25

  output:
    meetings_per_week: 10
    sqls_per_month: 15
    pipeline_per_month: "$200K"

  quality:
    show_rate: ">80%"
    sql_rate: ">60%"
    pipeline_accuracy: ">90%"

  efficiency:
    connect_rate: "12-15%"
    email_reply_rate: ">5%"
    meetings_per_100_calls: "3-5"
```

## Лучшие практики

1. **Research before outreach** — 10-15 минут на каждый account
2. **Multi-channel cadences** — комбинируй email, звонки, LinkedIn
3. **Personalization at scale** — уникальные первые строки
4. **Listen more than talk** — 70/30 ratio на discovery
5. **Track everything** — данные = улучшение
6. **Follow up relentlessly** — 80% сделок требуют 5+ touchpoints
