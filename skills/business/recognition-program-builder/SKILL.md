---
name: recognition-program-builder
description: Эксперт employee recognition. Используй для программ признания, награждения и employee engagement.
---

# Recognition Program Builder

Expert in creating and optimizing employee recognition programs that drive engagement, retention, and performance.

## Core Principles

```yaml
recognition_principles:
  timely: "Recognize immediately after achievement"
  specific: "Detail exactly what was recognized"
  personal: "Tailored to individual preferences"
  visible: "Public recognition amplifies impact"
  valuable: "Meaningful to the recipient"

recognition_types:
  formal:
    - "Awards and ceremonies"
    - "Performance bonuses"
    - "Promotions"
    - "Public announcements"

  informal:
    - "Verbal praise"
    - "Thank you notes"
    - "Peer shoutouts"
    - "Small gifts"

  social:
    - "Team celebrations"
    - "Company-wide recognition"
    - "Social media highlights"
```

## Program Framework

```yaml
implementation_phases:
  phase_1_foundation:
    duration: "2-4 weeks"
    activities:
      - "Stakeholder alignment"
      - "Needs assessment"
      - "Budget allocation"
      - "Platform selection"
    deliverables:
      - "Program charter"
      - "Success metrics"
      - "Communication plan"

  phase_2_design:
    duration: "4-6 weeks"
    activities:
      - "Recognition criteria"
      - "Reward catalog"
      - "Nomination process"
      - "Platform configuration"
    deliverables:
      - "Program guidelines"
      - "Manager toolkit"
      - "Employee handbook"

  phase_3_pilot:
    duration: "4-8 weeks"
    scope: "20-30% of organization"
    activities:
      - "Soft launch"
      - "Feedback collection"
      - "Process refinement"
    deliverables:
      - "Pilot report"
      - "Updated processes"

  phase_4_scale:
    duration: "Ongoing"
    activities:
      - "Company-wide rollout"
      - "Training sessions"
      - "Continuous improvement"
```

## Recognition Tiers

```yaml
recognition_structure:
  tier_1_social:
    name: "Thank You"
    cost: "Free"
    frequency: "Daily"
    examples:
      - "Slack kudos"
      - "Email appreciation"
      - "Verbal recognition"
    approver: "Any employee"

  tier_2_points:
    name: "Points Award"
    cost: "$5-25 value"
    frequency: "Weekly"
    examples:
      - "Peer points"
      - "Manager spot awards"
      - "Team recognition"
    approver: "Manager"

  tier_3_achievement:
    name: "Achievement Award"
    cost: "$50-200 value"
    frequency: "Monthly"
    examples:
      - "Project completion"
      - "Innovation award"
      - "Customer hero"
    approver: "Director"

  tier_4_excellence:
    name: "Excellence Award"
    cost: "$500-2000 value"
    frequency: "Quarterly"
    examples:
      - "Quarterly MVP"
      - "Leadership award"
      - "Value champion"
    approver: "VP/Executive"

  tier_5_transformational:
    name: "Transformational"
    cost: "$5000+ or promotion"
    frequency: "Annual"
    examples:
      - "President's award"
      - "Career achievement"
      - "Innovation of the year"
    approver: "CEO/Board"
```

## Recognition Frequency Matrix

```yaml
frequency_guide:
  daily:
    type: "Peer appreciation"
    channel: "Slack/Teams"
    impact: "Maintains engagement"

  weekly:
    type: "Team shoutouts"
    channel: "Team meetings"
    impact: "Builds team culture"

  monthly:
    type: "Performance recognition"
    channel: "All-hands/Newsletter"
    impact: "Drives results"

  quarterly:
    type: "Achievement awards"
    channel: "Town hall"
    impact: "Celebrates milestones"

  annually:
    type: "Major recognition"
    channel: "Awards ceremony"
    impact: "Career highlight"
```

## Nomination System

```yaml
nomination_workflow:
  submission:
    fields:
      - "Nominee name"
      - "Recognition category"
      - "Achievement description"
      - "Business impact"
      - "Company value demonstrated"
    guidelines:
      - "Be specific about the achievement"
      - "Quantify impact when possible"
      - "Connect to company values"

  review:
    criteria:
      - "Achievement significance"
      - "Value alignment"
      - "Business impact"
      - "Behavior repeatability"
    timeline: "5 business days max"

  approval_routing:
    tier_1_2: "Auto-approve"
    tier_3: "Manager approval"
    tier_4: "Director + HR approval"
    tier_5: "Executive committee"
```

## Reward Catalog

```yaml
reward_categories:
  experiences:
    examples:
      - "Extra PTO day"
      - "Lunch with leadership"
      - "Conference attendance"
      - "Learning subscription"
    appeal: "High engagement, memorable"

  merchandise:
    examples:
      - "Company swag"
      - "Tech gadgets"
      - "Gift cards"
      - "Custom awards"
    appeal: "Tangible, collectible"

  wellness:
    examples:
      - "Gym membership"
      - "Spa voucher"
      - "Wellness app subscription"
      - "Health equipment"
    appeal: "Shows care for wellbeing"

  charitable:
    examples:
      - "Donation to charity of choice"
      - "Volunteer time off"
      - "Matched giving"
    appeal: "Aligns with values"

  professional:
    examples:
      - "Training course"
      - "Certification funding"
      - "Book allowance"
      - "Mentorship program"
    appeal: "Career growth focused"
```

## Platform Integration

### Slack Integration

```javascript
// Slack workflow for peer recognition
const recognitionWorkflow = {
  trigger: {
    type: "shortcut",
    callback_id: "give_recognition"
  },

  steps: [
    {
      type: "form",
      block_id: "recognition_form",
      elements: [
        {
          type: "users_select",
          action_id: "recipient",
          placeholder: "Select colleague"
        },
        {
          type: "static_select",
          action_id: "category",
          options: [
            { text: "Innovation", value: "innovation" },
            { text: "Teamwork", value: "teamwork" },
            { text: "Customer Focus", value: "customer" },
            { text: "Excellence", value: "excellence" }
          ]
        },
        {
          type: "plain_text_input",
          action_id: "message",
          multiline: true,
          placeholder: "Describe the achievement..."
        }
      ]
    }
  ],

  onSubmit: async (payload) => {
    const recognition = {
      recipient: payload.recipient,
      giver: payload.user,
      category: payload.category,
      message: payload.message,
      timestamp: new Date().toISOString()
    };

    // Save to database
    await saveRecognition(recognition);

    // Post to recognition channel
    await postToChannel('#recognition', formatRecognition(recognition));

    // Award points if applicable
    await awardPoints(recognition.recipient, getCategoryPoints(recognition.category));

    // Notify recipient
    await notifyRecipient(recognition);
  }
};
```

### Service Anniversary Automation

```yaml
anniversary_workflow:
  triggers:
    - "1 year"
    - "3 years"
    - "5 years"
    - "10 years"
    - "15+ years"

  automation:
    30_days_before:
      - "Notify manager"
      - "Prepare certificate"
      - "Order gift (5+ years)"

    7_days_before:
      - "Schedule announcement"
      - "Confirm celebration plans"

    day_of:
      - "Post company-wide announcement"
      - "Send personalized message from CEO"
      - "Deliver gift and certificate"

  rewards_by_tenure:
    1_year:
      - "Digital certificate"
      - "100 points"
      - "Social recognition"
    3_years:
      - "Physical certificate"
      - "250 points"
      - "Gift ($50 value)"
    5_years:
      - "Framed certificate"
      - "500 points"
      - "Gift ($200 value)"
      - "Extra PTO day"
    10_years:
      - "Crystal award"
      - "1000 points"
      - "Gift ($500 value)"
      - "Week extra PTO"
```

## Metrics & Measurement

```yaml
program_metrics:
  participation:
    recognitions_given:
      target: "3+ per employee per month"
      measurement: "Count of recognitions"
    recognitions_received:
      target: "1+ per employee per month"
      measurement: "Unique recipients"
    manager_participation:
      target: "100%"
      measurement: "Managers giving recognition"

  impact:
    engagement_correlation:
      measurement: "Recognition vs engagement scores"
      target: "Positive correlation >0.5"
    retention_impact:
      measurement: "Turnover recognized vs non-recognized"
      target: "20% lower turnover"
    performance_correlation:
      measurement: "Recognition vs performance ratings"
      target: "Higher performers = more recognition"

  quality:
    message_specificity:
      target: ">50 words average"
      measurement: "Character count"
    value_alignment:
      target: "80% tag company values"
      measurement: "Value tag usage"
```

## ROI Calculation

```yaml
roi_model:
  inputs:
    program_cost:
      platform: "$X/employee/year"
      rewards: "$Y/employee/year"
      administration: "Z hours × hourly rate"

  benefits:
    retention_savings:
      formula: |
        (Turnover reduction %) ×
        (Number of employees) ×
        (Cost per turnover)
      example:
        turnover_reduction: "5%"
        employees: 500
        cost_per_turnover: "$15,000"
        savings: "$375,000"

    productivity_gains:
      formula: |
        (Engagement increase %) ×
        (Productivity correlation) ×
        (Total payroll)
      example:
        engagement_increase: "10%"
        productivity_correlation: "0.2"
        payroll: "$50,000,000"
        gains: "$1,000,000"

    recruitment_savings:
      formula: |
        (Referral increase %) ×
        (Hires per year) ×
        (Agency fee avoided)
      example:
        referral_increase: "15%"
        hires: 100
        agency_fee: "$10,000"
        savings: "$150,000"

  roi_calculation:
    total_benefits: "$1,525,000"
    total_costs: "$150,000"
    roi: "917%"
```

## Manager Toolkit

```yaml
manager_guide:
  recognition_opportunities:
    daily:
      - "Task completion"
      - "Helpful behavior"
      - "Problem solving"
    weekly:
      - "Project milestones"
      - "Team collaboration"
      - "Customer feedback"
    monthly:
      - "Goal achievement"
      - "Process improvement"
      - "Mentoring others"

  recognition_tips:
    do:
      - "Be specific about what was achieved"
      - "Recognize promptly"
      - "Match recognition to achievement"
      - "Know individual preferences"
      - "Recognize effort, not just results"
    dont:
      - "Give generic praise"
      - "Wait for annual reviews"
      - "Only recognize top performers"
      - "Ignore small wins"
      - "Make it about you"

  scripts:
    peer_recognition: |
      "I want to recognize [Name] for [specific achievement].
      This demonstrates our value of [value] and had a real
      impact on [business outcome]. Thank you, [Name]!"

    team_recognition: |
      "The [team name] team achieved [milestone] this week.
      Special thanks to [names] for [specific contributions].
      This is a great example of [value] in action."
```

## Common Challenges

```yaml
challenges_solutions:
  manager_resistance:
    symptoms:
      - "Low manager participation"
      - "Generic recognition messages"
      - "Delegation to HR"
    solutions:
      - "Include in manager KPIs"
      - "Provide recognition training"
      - "Share manager leaderboards"
      - "Simplify recognition process"

  recognition_inflation:
    symptoms:
      - "Everyone gets awards"
      - "Awards feel meaningless"
      - "Budget overruns"
    solutions:
      - "Clear criteria for each tier"
      - "Calibration sessions"
      - "Limited high-value awards"
      - "Focus on quality over quantity"

  inequitable_distribution:
    symptoms:
      - "Same people always recognized"
      - "Remote workers overlooked"
      - "Support roles ignored"
    solutions:
      - "Recognition equity dashboard"
      - "Manager prompts for overlooked"
      - "Category for each role type"
      - "Anonymous nomination option"
```

## Лучшие практики

1. **Timely recognition** — признавай сразу после достижения
2. **Be specific** — конкретно описывай за что признание
3. **Match to values** — связывай с ценностями компании
4. **Variety matters** — используй разные формы признания
5. **Measure impact** — отслеживай ROI программы
6. **Train managers** — обучай менеджеров давать признание
