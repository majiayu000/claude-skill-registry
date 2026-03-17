---
name: learning-development-plan
description: Эксперт по планам развития. Используй для создания IDP, competency mapping, skill assessments и learning pathways.
---

# Learning Development Plan Designer

Expert in creating comprehensive, personalized learning development plans with skills assessment, goal setting, and progress tracking frameworks.

## Core Principles

### Competency-Based Frameworks
- Map competencies to proficiency levels (Novice → Expert)
- Align with role requirements and career paths
- Define behavioral indicators for each level
- Establish prerequisite relationships between competencies

### Adult Learning Theory
- Apply 70-20-10 model (experiential, social, formal)
- Incorporate spaced repetition and microlearning
- Support varied learning modalities
- Include reflection and application opportunities

## Competency Framework Template

```yaml
competency_framework:
  name: "Software Engineering Competencies"
  version: "1.0"

  levels:
    - id: 1
      name: "Novice"
      description: "Learning fundamentals with guidance"
      indicators:
        - "Requires detailed instructions"
        - "Completes basic tasks with support"
        - "Asks clarifying questions"

    - id: 2
      name: "Developing"
      description: "Applies knowledge with moderate guidance"
      indicators:
        - "Works independently on familiar tasks"
        - "Seeks help for complex problems"
        - "Starts applying best practices"

    - id: 3
      name: "Proficient"
      description: "Consistently applies skills independently"
      indicators:
        - "Handles complex tasks independently"
        - "Mentors novice team members"
        - "Contributes to process improvements"

    - id: 4
      name: "Advanced"
      description: "Expert who guides others"
      indicators:
        - "Solves novel and complex problems"
        - "Designs systems and processes"
        - "Recognized as subject matter expert"

    - id: 5
      name: "Expert"
      description: "Industry-recognized authority"
      indicators:
        - "Shapes industry practices"
        - "Innovates in the domain"
        - "Thought leader externally"

  competencies:
    technical:
      - id: "TECH-001"
        name: "Programming Languages"
        description: "Proficiency in relevant programming languages"
        levels:
          1: "Understands basic syntax and concepts"
          2: "Writes functional code with guidance"
          3: "Writes clean, tested, maintainable code"
          4: "Architects complex solutions"
          5: "Contributes to language/framework development"

      - id: "TECH-002"
        name: "System Design"
        description: "Ability to design scalable systems"
        levels:
          1: "Understands basic architecture patterns"
          2: "Designs simple systems with guidance"
          3: "Designs moderately complex systems"
          4: "Designs enterprise-scale systems"
          5: "Creates novel architectural patterns"
        prerequisites:
          - "TECH-001:3"  # Requires programming at level 3

    soft_skills:
      - id: "SOFT-001"
        name: "Communication"
        description: "Written and verbal communication skills"
        levels:
          1: "Communicates basic information clearly"
          2: "Adapts style to audience"
          3: "Facilitates effective team discussions"
          4: "Presents to executive audiences"
          5: "Influential communicator externally"

      - id: "SOFT-002"
        name: "Collaboration"
        description: "Ability to work effectively with others"
        levels:
          1: "Works well in defined team structure"
          2: "Actively contributes to team success"
          3: "Builds relationships across teams"
          4: "Leads cross-functional initiatives"
          5: "Builds organization-wide partnerships"
```

## Skills Assessment Matrix

```yaml
skills_assessment:
  employee:
    name: "John Smith"
    role: "Senior Software Engineer"
    manager: "Jane Doe"
    assessment_date: "2024-01-15"

  technical_skills:
    - skill: "Python Development"
      current_level: 3
      target_level: 4
      gap: 1
      priority: "High"
      assessment_method: "Technical review + portfolio"
      evidence:
        - "Code samples from recent projects"
        - "Architecture decisions documented"
      development_activities:
        - "Advanced Python design patterns course"
        - "Lead architecture review for Q2 project"
        - "Contribute to open source Python project"

    - skill: "Cloud Architecture (AWS)"
      current_level: 2
      target_level: 4
      gap: 2
      priority: "High"
      assessment_method: "Certification + practical assessment"
      evidence:
        - "AWS Solutions Architect certification"
        - "Designed production infrastructure"
      development_activities:
        - "AWS Solutions Architect Professional cert"
        - "Shadow senior architect on cloud migration"
        - "Design DR strategy for core systems"

    - skill: "Machine Learning"
      current_level: 1
      target_level: 2
      gap: 1
      priority: "Medium"
      assessment_method: "Project completion"
      evidence:
        - "Completed ML training module"
        - "Built basic recommendation model"
      development_activities:
        - "Complete ML fundamentals course"
        - "Implement ML feature with team support"

  soft_skills:
    - skill: "Technical Leadership"
      current_level: 2
      target_level: 3
      gap: 1
      priority: "High"
      assessment_method: "360-degree feedback"
      evidence:
        - "Led 2 successful project teams"
        - "Positive peer feedback on mentoring"
      development_activities:
        - "Leadership development program"
        - "Mentor 2 junior engineers"
        - "Present at team tech talks monthly"

    - skill: "Stakeholder Management"
      current_level: 2
      target_level: 3
      gap: 1
      priority: "Medium"
      assessment_method: "Manager observation + stakeholder feedback"
      development_activities:
        - "Lead requirements gathering sessions"
        - "Present project updates to leadership"

  summary:
    total_gaps: 6
    high_priority_gaps: 3
    target_completion: "2024-12-31"
    review_frequency: "Quarterly"
```

## Individual Development Plan (IDP)

```yaml
individual_development_plan:
  header:
    employee_name: "John Smith"
    employee_id: "EMP-12345"
    current_role: "Senior Software Engineer"
    target_role: "Staff Engineer"
    manager: "Jane Doe"
    hr_partner: "Bob Wilson"
    plan_period: "2024-01-01 to 2024-12-31"
    created_date: "2024-01-10"
    last_updated: "2024-01-15"

  career_aspirations:
    short_term: "Become Staff Engineer within 12-18 months"
    long_term: "Principal Engineer / Engineering Director in 5 years"
    interests:
      - "Distributed systems"
      - "Technical leadership"
      - "Mentoring and coaching"
    values:
      - "Continuous learning"
      - "Work-life balance"
      - "Impact at scale"

  development_goals:
    - id: "GOAL-001"
      title: "Achieve Staff Engineer technical proficiency"
      business_impact: "Lead larger initiatives, reduce architecture review bottlenecks"
      success_metrics:
        - "Complete 2 system design reviews independently"
        - "Achieve level 4 in System Design competency"
        - "Receive positive 360 feedback on technical leadership"
      target_date: "2024-09-30"
      status: "In Progress"

      activities:
        - type: "Experiential (70%)"
          items:
            - activity: "Lead architecture for Q2 platform migration"
              deadline: "2024-06-30"
              support_needed: "Pairing with principal engineer"
              status: "Planned"

            - activity: "Own technical direction for 2 cross-team initiatives"
              deadline: "2024-09-30"
              support_needed: "Manager sponsorship"
              status: "Not Started"

        - type: "Social (20%)"
          items:
            - activity: "Monthly 1:1 with Staff Engineer mentor"
              deadline: "Ongoing"
              support_needed: "Mentor assignment"
              status: "In Progress"

            - activity: "Participate in architecture review board"
              deadline: "2024-03-01"
              support_needed: "Board nomination"
              status: "Pending"

        - type: "Formal (10%)"
          items:
            - activity: "Complete System Design interview prep course"
              deadline: "2024-02-28"
              support_needed: "Training budget approval"
              status: "In Progress"

            - activity: "Attend distributed systems conference"
              deadline: "2024-06-15"
              support_needed: "Conference budget"
              status: "Approved"

    - id: "GOAL-002"
      title: "Develop technical leadership capabilities"
      business_impact: "Improve team productivity, better talent retention"
      success_metrics:
        - "Mentor 2 junior engineers to promotion"
        - "Receive 4.5+ leadership rating in reviews"
        - "Present 4 tech talks to broader org"
      target_date: "2024-12-31"
      status: "In Progress"

      activities:
        - type: "Experiential (70%)"
          items:
            - activity: "Lead weekly team technical discussions"
              deadline: "Ongoing"
              status: "In Progress"

            - activity: "Own team's technical interview process"
              deadline: "2024-04-01"
              status: "Planned"

        - type: "Social (20%)"
          items:
            - activity: "Join engineering leadership community of practice"
              deadline: "2024-02-01"
              status: "Completed"

            - activity: "Shadow director in leadership meetings"
              deadline: "2024-06-30"
              status: "Pending Approval"

        - type: "Formal (10%)"
          items:
            - activity: "Complete leadership development program"
              deadline: "2024-08-31"
              status: "Enrolled"

  resources_needed:
    budget:
      training: "$3,000"
      conferences: "$2,500"
      books_subscriptions: "$500"
      total: "$6,000"

    time:
      formal_learning: "2 hours/week"
      mentoring_received: "1 hour/week"
      mentoring_given: "2 hours/week"

    support:
      - "Staff Engineer mentor assignment"
      - "Manager sponsorship for stretch assignments"
      - "Protected learning time"

  check_ins:
    frequency: "Bi-weekly with manager"
    quarterly_review_dates:
      - "2024-03-31"
      - "2024-06-30"
      - "2024-09-30"
      - "2024-12-31"

    review_agenda:
      - "Progress on development goals"
      - "Blockers and support needed"
      - "Feedback on recent activities"
      - "Adjustments to plan"
```

## Learning Pathway Design

```yaml
learning_pathway:
  name: "Senior to Staff Engineer Track"
  duration: "12-18 months"
  target_audience: "Senior Engineers with 3+ years experience"

  phases:
    - phase: 1
      name: "Foundation"
      duration: "3 months"
      objectives:
        - "Deepen system design knowledge"
        - "Begin mentoring practice"
        - "Expand influence beyond team"

      modules:
        - module: "System Design Fundamentals"
          format: "Online course + practice"
          hours: 20
          deliverables:
            - "Complete 5 system design exercises"
            - "Document design for current project"
          assessment: "Design review with senior engineer"

        - module: "Mentoring Basics"
          format: "Workshop + practice"
          hours: 8
          deliverables:
            - "Begin mentoring 1 junior engineer"
            - "Complete mentoring reflection journal"
          assessment: "Mentee feedback + manager observation"

      milestones:
        - "Design review completed and approved"
        - "Mentoring relationship established"
        - "First cross-team collaboration initiated"

    - phase: 2
      name: "Growth"
      duration: "6 months"
      objectives:
        - "Lead complex technical initiatives"
        - "Develop organizational influence"
        - "Deepen expertise in chosen domain"

      modules:
        - module: "Technical Leadership"
          format: "Cohort-based program"
          hours: 40
          deliverables:
            - "Lead 1 cross-team technical initiative"
            - "Present 2 tech talks"
            - "Contribute to architecture decisions"
          assessment: "360 feedback + project outcomes"

        - module: "Domain Expertise Deep Dive"
          format: "Self-directed + mentoring"
          hours: 50
          deliverables:
            - "Complete specialization coursework"
            - "Publish internal technical blog posts"
            - "Build proof-of-concept in domain"
          assessment: "Expert review + practical demonstration"

      milestones:
        - "Successfully delivered cross-team initiative"
        - "Recognized as go-to person in domain"
        - "Positive stakeholder feedback collected"

    - phase: 3
      name: "Mastery"
      duration: "3-6 months"
      objectives:
        - "Demonstrate Staff-level impact"
        - "Solidify organizational influence"
        - "Prepare for promotion review"

      modules:
        - module: "Strategic Impact"
          format: "Project-based"
          hours: 60
          deliverables:
            - "Lead org-wide technical initiative"
            - "Influence technical strategy"
            - "Build lasting processes/systems"
          assessment: "Leadership review + business impact metrics"

        - module: "Promotion Preparation"
          format: "Coaching + portfolio development"
          hours: 20
          deliverables:
            - "Compile promotion packet"
            - "Gather supporting evidence"
            - "Practice calibration presentation"
          assessment: "Manager readiness assessment"

      milestones:
        - "Promotion packet complete"
        - "Clear evidence of Staff-level impact"
        - "Manager endorsement received"

  support_structure:
    mentor: "Assigned Staff/Principal Engineer"
    manager: "Regular check-ins and sponsorship"
    cohort: "Peer group of 5-8 on same track"
    community: "Engineering leadership community"
```

## Assessment & Feedback Framework

```yaml
feedback_framework:
  multi_source_feedback:
    self_assessment:
      frequency: "Monthly"
      format: "Reflection template"
      focus_areas:
        - "Progress on development goals"
        - "New skills applied"
        - "Challenges encountered"
        - "Support needed"

    manager_feedback:
      frequency: "Bi-weekly 1:1"
      format: "Structured discussion"
      focus_areas:
        - "Performance observations"
        - "Behavioral feedback"
        - "Guidance on priorities"
        - "Career coaching"

    peer_feedback:
      frequency: "Quarterly"
      format: "360 survey + 1:1 discussions"
      focus_areas:
        - "Collaboration effectiveness"
        - "Technical contributions"
        - "Communication quality"
        - "Leadership behaviors"

    mentor_feedback:
      frequency: "Weekly/bi-weekly"
      format: "Mentoring session"
      focus_areas:
        - "Skill development progress"
        - "Career advice"
        - "Industry perspective"
        - "Network building"

  progress_tracking:
    metrics:
      - metric: "Competency progression"
        measurement: "Level advancement in framework"
        target: "Advance 1 level in 2+ competencies"

      - metric: "Learning activity completion"
        measurement: "% of planned activities completed"
        target: ">80% completion rate"

      - metric: "Goal achievement"
        measurement: "% of development goals met"
        target: ">70% goals achieved"

      - metric: "Feedback scores"
        measurement: "360 feedback ratings"
        target: "Improvement trend quarter-over-quarter"

    review_template:
      sections:
        - "Executive summary"
        - "Goal progress dashboard"
        - "Key accomplishments"
        - "Challenges and blockers"
        - "Feedback highlights"
        - "Adjusted priorities"
        - "Support requests"
```

## 70-20-10 Activity Examples

```yaml
learning_activities_by_type:
  experiential_70_percent:
    description: "On-the-job experiences and challenges"
    examples:
      - category: "Stretch assignments"
        activities:
          - "Lead a project outside comfort zone"
          - "Own a high-visibility initiative"
          - "Take on temporary leadership role"
          - "Solve a complex technical problem"

      - category: "Job rotation"
        activities:
          - "Shadow different role for 2 weeks"
          - "Rotate to adjacent team temporarily"
          - "Take on responsibilities from leaving peer"

      - category: "New responsibilities"
        activities:
          - "Own a new domain area"
          - "Lead cross-functional initiative"
          - "Represent team in leadership forums"

  social_20_percent:
    description: "Learning from and with others"
    examples:
      - category: "Mentoring"
        activities:
          - "Regular 1:1 with mentor"
          - "Mentoring junior colleague"
          - "Reverse mentoring (teaching senior)"

      - category: "Communities"
        activities:
          - "Join professional community of practice"
          - "Participate in guild/chapter meetings"
          - "Attend industry meetups"

      - category: "Feedback"
        activities:
          - "Seek regular feedback from peers"
          - "Participate in code reviews"
          - "Request 360 feedback"

      - category: "Networking"
        activities:
          - "Coffee chats with leaders"
          - "Build cross-team relationships"
          - "Connect with industry peers"

  formal_10_percent:
    description: "Structured learning programs"
    examples:
      - category: "Courses"
        activities:
          - "Online courses (Coursera, LinkedIn Learning)"
          - "Internal training programs"
          - "Certification preparation"

      - category: "Events"
        activities:
          - "Industry conferences"
          - "Internal tech talks"
          - "Workshops and bootcamps"

      - category: "Self-study"
        activities:
          - "Technical books"
          - "Research papers"
          - "Documentation deep-dives"
```

## Лучшие практики

1. **Manager involvement** — руководители должны участвовать в создании IDP
2. **Business alignment** — связывайте развитие с бизнес-целями
3. **Learning style assessment** — учитывайте предпочтения в обучении
4. **Multiple modalities** — предлагайте разные форматы обучения
5. **Progress tracking** — отслеживайте корреляцию активностей и результатов
6. **Realistic timelines** — избегайте чрезмерно амбициозных сроков
