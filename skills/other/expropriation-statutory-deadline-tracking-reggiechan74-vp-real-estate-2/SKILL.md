---
name: expropriation-statutory-deadline-tracking
description: Expert in managing critical statutory timelines under Ontario Expropriations Act including 3-month registration window, Form 2/7 service timing, and escalation protocols by timeline urgency. Use when tracking expropriation deadlines, calculating notice periods, or managing timeline-critical acquisitions. Key terms include statutory deadlines, 3-month registration, Form 2 service, Form 7 notice, approval expiry, escalation protocols
tags: [statutory-deadlines, expropriations-act, timeline-management, registration-window, notice-requirements, escalation-protocols]
capability: Provides systematic deadline tracking framework including Ontario Expropriations Act statutory windows (3-month registration per s.9, Form 2 service timing 30 days pre-registration, Form 7 notice 30-day minimum per s.11), calculation methodologies (approval date + 90 days, business days vs. calendar days), and escalation protocols (green >60 days, yellow 30-60, orange 15-30, red 7-15, critical <7 days with emergency procedures)
proactive: true
---

You are an expert in tracking and managing statutory deadlines under the Ontario Expropriations Act, ensuring procedural compliance and avoiding approval expiry through systematic monitoring and escalation.

## Granular Focus

Managing critical statutory timelines (subset of Stevi's capabilities). This skill provides operational deadline tracking - NOT legal interpretation of expropriation law.

## Ontario Expropriations Act Deadlines

Key statutory windows that cannot be extended and result in approval expiry if missed.

### 3-Month Registration Window (s.9)

**Statute**: Expropriation plan must be registered within 3 months of approval.

**s.9(2)**: "Where an expropriation plan is not registered within three months after the approval becomes final, the approval expires and is of no effect."

**Countdown calculation**:
- **Approval date**: Date approving authority signs approval certificate (not application date)
- **Expiry date**: Approval date + 90 days (calendar days, not business days)
- **Critical**: If day 90 falls on weekend/holiday, deadline does NOT extend - must register before weekend

**Example**:
- **Approval date**: March 15, 2025 (Saturday)
- **Expiry date**: March 15 + 90 days = **June 13, 2025** (Friday)
- **Registration deadline**: **June 13, 2025 by 4:00 PM** (Land Registry Office closing time)
- **No extension**: If June 13 falls on a holiday (e.g., Good Friday), deadline is June 12 (previous business day)

**Calculation methodology**:
- Use calendar calculator (Excel, Google Sheets, project management software)
- Formula: `=DATE(approval_year, approval_month, approval_day) + 90`
- Verify manually (count days on calendar to avoid software errors)
- **Contingency**: Calculate as 85 days (5-day buffer for unforeseen issues)

**Municipal clerk coordination**:
- **Expropriation plan preparation**: Surveyor prepares plan (2-4 weeks)
- **Plan review**: Municipal clerk reviews plan for compliance with O.Reg. 363/90 Form 6 requirements (1 week)
- **Corrections**: If plan defects identified, surveyor corrects and resubmits (1-2 weeks)
- **Final approval**: Municipal solicitor approves plan for registration (1 week)
- **Total**: 5-8 weeks from approval to plan ready for registration

**Timeline example**:
- **Week 0** (March 15): Approval received
- **Weeks 1-3**: Surveyor prepares expropriation plan
- **Week 4**: Municipal clerk reviews plan - **identifies error** (property description inconsistent with legal description)
- **Week 5**: Surveyor corrects plan, resubmits
- **Week 6**: Municipal solicitor reviews and approves
- **Weeks 7-9**: Wait for land registry office appointment (backlog)
- **Week 10** (May 24): Plan registered - **65 days after approval** (25-day buffer remaining)

**Contingency planning if deadline at risk**:
- **Option 1**: Obtain second approval (re-apply if first approval will expire)
  - Risk: Approving authority may deny second application
- **Option 2**: Register plan with minor defects, correct via amendment
  - Risk: Registry office may reject plan
- **Option 3**: Abandon expropriation, re-apply after approval expires
  - Cost: Delay, additional approval fees, political risk

### Form 2 Service Timing

**Best practice**: Serve Form 2 (Notice of Application for Approval) 30 days before plan registration.

**Not statutory requirement**, but:
- **Natural justice**: Owners should have notice of expropriation before plan registered
- **Reduces challenges**: Serving Form 2 post-registration invites procedural challenges
- **Practical**: Allows owners to contact authority, ask questions, prepare

**Service method requirements** (s.11):
- **Personal service**: Deliver Form 2 directly to owner (preferred method)
- **Registered mail**: Mail to owner's address (requires 5 days delivery time)
- **Substituted service**: If owner cannot be located, court order for alternative service (post on property, publish in newspaper)

**Timing calculation**:
- **Registration date**: June 13, 2025
- **Form 2 service**: 30 days prior = **May 14, 2025**
- **Service method**: Personal service (same day) or registered mail (allow 5 days delivery = serve by May 9)

**Proof of service documentation**:
- **Affidavit of service**: Sworn statement by process server confirming date/time/method of service
- **Registered mail receipt**: Canada Post tracking showing delivery date
- **Keep records**: File affidavits with municipal clerk (proof of compliance)

### Form 7 Notice (30 Days Minimum)

**Statute**: Form 7 (Notice of Expropriation) must be served at least 30 days before possession (s.11).

**s.11(1)**: "At least thirty days before the date fixed for taking possession, the expropriating authority shall serve notice of the expropriation on the owner of the land."

**Calculation**:
- **Possession date**: July 15, 2025 (date authority takes possession)
- **Form 7 service**: 30 days prior = **June 15, 2025 or earlier**
- **Service method**: Personal service or registered mail (allow 5 days delivery = serve by June 10)

**Payment timing coordination**:
- **Best practice**: Pay compensation before or concurrent with Form 7 service
- **Statute** (s.14): Compensation payable "on the date of registration" (but can be paid later if negotiated)
- **Practical**: Paying at Form 7 service demonstrates good faith, reduces opposition

**Possession timing**:
- **Standard**: 30 days after Form 7 service (minimum statutory period)
- **Extended**: Can give owners more time (e.g., 60-90 days) if requested and project schedule allows
- **Example**: Form 7 served June 15 states possession date of **September 1** (75 days) - accommodates owner's request to relocate during summer

## Escalation Protocols by Timeline

Color-coded monitoring system with increasing urgency and oversight as deadlines approach.

### Green (>60 Days to Deadline)

**Status**: Routine monitoring, no escalation required.

**Actions**:
- **Weekly status check**: Project manager reviews progress
- **Milestone tracking**: Ensure surveyor, municipal clerk, land registry office on schedule
- **No escalation**: Standard project management

**Example**:
- **Approval date**: March 15, 2025
- **Current date**: April 1, 2025 (77 days to deadline)
- **Status**: Green - plan preparation in progress, surveyor on schedule

### Yellow (30-60 Days to Deadline)

**Status**: Moderate concern, weekly status checks required.

**Actions**:
- **Weekly status meetings**: Project manager + surveyor + municipal clerk
- **Identify risks**: Any delays in plan preparation, corrections needed?
- **Executive notification**: Update senior management (director level) on timeline status
- **No critical actions yet**: Still time to resolve issues

**Example**:
- **Approval date**: March 15, 2025
- **Current date**: May 1, 2025 (43 days to deadline)
- **Status**: Yellow - plan submitted to land registry office, awaiting appointment
- **Action**: Weekly check-ins with land registry office, confirm appointment scheduled

### Orange (15-30 Days to Deadline)

**Status**: Significant concern, daily monitoring, executive escalation.

**Actions**:
- **Daily status checks**: Project manager contacts surveyor, municipal clerk, land registry office daily
- **Executive escalation**: VP/CAO briefed on timeline risk
- **Mitigation planning**: Develop contingency plans
  - **Option 1**: Expedite land registry appointment (senior staff contacts registry office manager)
  - **Option 2**: Prepare second approval application (if first will expire)
- **Communication**: Notify council, approving authority of timeline risk

**Example**:
- **Approval date**: March 15, 2025
- **Current date**: May 28, 2025 (16 days to deadline)
- **Status**: Orange - land registry office backlog, no appointment yet
- **Action**: CAO contacts Land Registrar directly, requests priority appointment
- **Result**: Appointment scheduled for June 6 (7 days before deadline)

### Red (7-15 Days to Deadline)

**Status**: Critical, crisis mode, all-hands coordination.

**Actions**:
- **Twice-daily updates**: Morning and afternoon status calls
- **Executive involvement**: CAO/CEO directly manages timeline
- **All-hands**: Cancel other meetings, prioritize expropriation plan registration
- **Contingencies activated**:
  - **Expedited approval**: Contact approving authority, request expedited second approval if needed
  - **Legal review**: Solicitor reviews plan for any defects (correct before registration)
  - **Land registry**: Senior management contacts Land Registrar for emergency appointment
- **Council briefing**: Inform council of timeline risk, prepare for potential approval expiry

**Example**:
- **Approval date**: March 15, 2025
- **Current date**: June 6, 2025 (7 days to deadline)
- **Status**: Red - land registry appointment on June 6, but plan has minor defects
- **Action**:
  - **Morning**: Solicitor reviews plan, identifies corrections needed
  - **Afternoon**: Surveyor makes corrections (priority work)
  - **Evening**: Corrected plan submitted to municipal clerk
  - **Next morning**: Municipal clerk approves, plan ready for registration
  - **June 6 PM**: Plan registered at land registry office (7 days before deadline)

### Critical (<7 Days to Deadline)

**Status**: Emergency, weekend work, highest executive priority.

**Actions**:
- **Emergency procedures**: Weekend work authorized, overtime approved
- **CEO/Mayor involvement**: Highest political/administrative level engaged
- **Legal escalation**: External counsel engaged if needed
- **Parallel tracks**:
  - **Track 1**: Register current plan (even if minor defects)
  - **Track 2**: Apply for second approval (if Track 1 fails)
- **Communication**: Daily briefings to council, approving authority
- **Post-mortem**: After deadline met (or missed), conduct lessons-learned review

**Example**:
- **Approval date**: March 15, 2025
- **Current date**: June 11, 2025 (2 days to deadline)
- **Status**: Critical - land registry office appointment on June 13 (last possible day)
- **Action**:
  - **June 11**: CEO contacts Land Registrar, confirms appointment for 9 AM June 13
  - **June 12**: Legal team pre-registers plan documents, ensures no issues
  - **June 13, 9 AM**: Municipal clerk attends land registry office in person
  - **June 13, 10 AM**: Plan registered (3 hours before 4 PM deadline)
  - **Post-mortem**: Review why timeline became critical, implement process improvements

---

**This skill activates when you**:
- Track expropriation statutory deadlines (3-month registration, Form 2/7 service)
- Calculate deadline expiry dates accounting for weekends and holidays
- Coordinate plan preparation with surveyors and municipal clerks
- Escalate timeline risks using color-coded protocols (green, yellow, orange, red, critical)
- Manage emergency situations when deadlines at imminent risk
- Conduct post-project reviews to improve deadline management processes
