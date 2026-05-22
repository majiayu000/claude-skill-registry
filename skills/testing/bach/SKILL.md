---
name: bach-exploratory-testing
description: Test software in the style of James Bach, pioneer of exploratory testing and context-driven testing. Emphasizes skilled human investigation, heuristics-based test design, and adapting to context rather than following rigid scripts. Use when designing test strategies, performing exploratory testing, or building thinking testers.
---

# James Bach Exploratory Testing Style Guide

## Overview

James Bach is a pioneer of exploratory testing and co-founder of the context-driven testing movement. A self-taught software tester who became one of the most influential voices in the field, he advocates for testing as a skilled intellectual activity rather than a mechanical process. His Rapid Software Testing methodology, developed with Michael Bolton, emphasizes simultaneous learning, test design, and execution.

## Core Philosophy

> "Testing is not a phase. Testing is not a checklist. Testing is the infinite process of comparing a product to what it ought to be."

> "Exploratory testing is simultaneous learning, test design, and test execution."

> "A good tester is not a person who follows scripts. A good tester is a person who can think."

Bach rejects the notion that testing can be reduced to following predetermined steps. Real testing requires sapient (thinking) humans who adapt their approach based on what they discover. The tester's mind is the primary testing tool.

## Design Principles

1. **Context Drives Practice**: There is no universal best practice—only practices that fit the context.

2. **Heuristics, Not Rules**: Use fallible methods that usually work, but remain aware they can fail.

3. **Skill Over Process**: Invest in tester skill development, not just test process documentation.

4. **Oracles Are Human Judgments**: We recognize problems through principles and heuristics, not just requirements.

5. **Testing Is Investigation**: Approach testing as a detective, not a factory worker.

## The Seven Principles of Context-Driven Testing

```
1. The value of any practice depends on its context.
2. There are good practices in context, but no best practices.
3. People, working together, are the most important part of any project's context.
4. Projects unfold over time in ways that are often not predictable.
5. The product is a solution. If the problem isn't solved, the product doesn't work.
6. Good software testing is a challenging intellectual process.
7. Only through judgment and skill can we do the right things at the right times.
```

## Heuristic Test Strategy Model (HTSM)

Bach's framework for thinking about test strategy:

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT ENVIRONMENT                       │
│  Customers, Information, Developer Relations, Test Team,    │
│  Equipment & Tools, Schedule, Test Items, Deliverables      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCT ELEMENTS                          │
│  Structure, Function, Data, Platform, Operations             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    QUALITY CRITERIA                          │
│  Capability, Reliability, Usability, Charisma,              │
│  Security, Scalability, Compatibility, Performance,          │
│  Installability, Maintainability                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    TEST TECHNIQUES                           │
│  Function, Domain, Stress, Flow, Scenario, Claims,          │
│  User, Risk, Automatic                                       │
└─────────────────────────────────────────────────────────────┘
```

## When Testing

### Always

- Begin with a testing charter or mission
- Document your mental model of the product
- Use oracles to identify potential problems
- Take notes during sessions (not after)
- Time-box exploratory sessions (60-90 minutes)
- Debrief after sessions to capture learnings
- Question requirements—they are often incomplete

### Never

- Follow scripts blindly without thinking
- Assume requirements are complete or correct
- Confuse test execution with testing
- Believe that passing tests means quality
- Stop exploring when you find one bug
- Treat automation as a replacement for thinking
- Assume absence of evidence is evidence of absence

### Prefer

- Questions over assumptions
- Exploration over confirmation
- Learning over procedure
- Skill over certification
- Models over checklists
- Collaboration over documentation
- Oracles over expected results

## Code Patterns

### Session-Based Test Management

```python
class ExploratorySession:
    """
    A time-boxed exploratory testing session.
    Bach's SBTM: structured freedom for skilled testers.
    """
    
    def __init__(self,
                 charter: str,
                 duration_minutes: int = 90,
                 tester: str = None):
        self.charter = charter
        self.duration = duration_minutes
        self.tester = tester
        self.start_time = None
        self.end_time = None
        self.notes = []
        self.bugs = []
        self.questions = []
        self.risks = []
        self.areas_explored = []
        self.session_metrics = {}
    
    def start(self):
        """Begin the session."""
        self.start_time = datetime.now()
        self.log(f"Session started. Charter: {self.charter}")
    
    def log(self, observation: str, category: str = 'note'):
        """
        Log observations during the session.
        Categories: note, bug, question, risk, idea
        """
        entry = {
            'timestamp': datetime.now(),
            'elapsed': self.elapsed_minutes(),
            'category': category,
            'content': observation
        }
        
        self.notes.append(entry)
        
        if category == 'bug':
            self.bugs.append(entry)
        elif category == 'question':
            self.questions.append(entry)
        elif category == 'risk':
            self.risks.append(entry)
    
    def elapsed_minutes(self) -> float:
        """Time elapsed since session start."""
        if not self.start_time:
            return 0
        return (datetime.now() - self.start_time).total_seconds() / 60
    
    def remaining_minutes(self) -> float:
        """Time remaining in session."""
        return max(0, self.duration - self.elapsed_minutes())
    
    def end(self):
        """
        End the session and calculate metrics.
        """
        self.end_time = datetime.now()
        
        self.session_metrics = {
            'duration_planned': self.duration,
            'duration_actual': self.elapsed_minutes(),
            'bugs_found': len(self.bugs),
            'questions_raised': len(self.questions),
            'risks_identified': len(self.risks),
            'areas_explored': len(self.areas_explored),
            'note_count': len(self.notes)
        }
        
        self.log("Session ended.")
        return self.generate_report()
    
    def generate_report(self) -> SessionReport:
        """
        Generate session report for debrief.
        """
        return SessionReport(
            charter=self.charter,
            tester=self.tester,
            duration=self.session_metrics['duration_actual'],
            bugs=self.bugs,
            questions=self.questions,
            risks=self.risks,
            areas=self.areas_explored,
            notes=self.notes,
            metrics=self.session_metrics
        )


class TestCharter:
    """
    A testing charter defines the mission for an exploratory session.
    
    Format: Explore <target> with <resources> to discover <information>
    """
    
    def __init__(self,
                 target: str,
                 resources: List[str],
                 information_sought: str,
                 time_box: int = 90,
                 priority: str = 'medium'):
        self.target = target
        self.resources = resources
        self.information = information_sought
        self.time_box = time_box
        self.priority = priority
    
    def __str__(self) -> str:
        return (f"Explore {self.target} "
                f"with {', '.join(self.resources)} "
                f"to discover {self.information}")
    
    @classmethod
    def from_risk(cls, risk: Risk, product_area: str) -> 'TestCharter':
        """
        Generate charter from identified risk.
        """
        return cls(
            target=product_area,
            resources=['boundary analysis', 'error guessing', risk.related_technique],
            information_sought=f"whether {risk.description} can occur",
            priority=risk.severity
        )
```

### Oracle Heuristics

```python
class OracleHeuristics:
    """
    Oracles: principles or mechanisms by which we recognize problems.
    Bach's FEW HICCUPPS mnemonic for consistency oracles.
    """
    
    # FEW HICCUPPS - Consistency Heuristics
    CONSISTENCY_ORACLES = {
        'Familiarity': 'Consistent with what testers have seen before',
        'Explainability': 'Consistent with what can be explained/documented',
        'World': 'Consistent with how the real world works',
        
        'History': 'Consistent with past versions of the product',
        'Image': 'Consistent with the organization\'s desired image',
        'Comparable_Products': 'Consistent with similar products',
        'Claims': 'Consistent with documentation, ads, specs',
        'User_Expectations': 'Consistent with what users want/expect',
        'Product': 'Consistent with itself (internal consistency)',
        'Purpose': 'Consistent with the explicit/implicit purpose',
        'Statutes': 'Consistent with laws, regulations, standards',
    }
    
    def __init__(self):
        self.oracle_applications = []
    
    def apply_oracle(self, 
                     observation: str, 
                     oracle_type: str,
                     expected_consistency: str,
                     actual_behavior: str) -> OracleResult:
        """
        Apply an oracle to evaluate observed behavior.
        """
        is_consistent = self.evaluate_consistency(
            expected_consistency, 
            actual_behavior
        )
        
        result = OracleResult(
            oracle=oracle_type,
            observation=observation,
            expected=expected_consistency,
            actual=actual_behavior,
            consistent=is_consistent,
            confidence=self.assess_confidence(oracle_type),
            notes=[]
        )
        
        self.oracle_applications.append(result)
        return result
    
    def evaluate_consistency(self, expected: str, actual: str) -> bool:
        """
        This requires human judgment—cannot be fully automated.
        Returns a preliminary assessment.
        """
        # This is where human thinking is essential
        # Automation can only flag for review
        return None  # Requires human judgment
    
    def assess_confidence(self, oracle_type: str) -> str:
        """
        Some oracles are more reliable than others.
        """
        high_confidence = ['Claims', 'Statutes', 'Product']
        medium_confidence = ['User_Expectations', 'Comparable_Products', 'History']
        low_confidence = ['Familiarity', 'World', 'Image']
        
        if oracle_type in high_confidence:
            return 'HIGH'
        elif oracle_type in medium_confidence:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def generate_test_ideas(self, product_element: str) -> List[str]:
        """
        Generate test ideas by applying each oracle.
        """
        ideas = []
        
        for oracle, description in self.CONSISTENCY_ORACLES.items():
            ideas.append(
                f"Test {product_element} for {oracle} consistency: "
                f"Is it {description.lower()}?"
            )
        
        return ideas


class ProductCoverageModel:
    """
    Model the product to guide exploration.
    SFDPOT: Structure, Function, Data, Platform, Operations, Time
    """
    
    ELEMENTS = {
        'Structure': [
            'Code modules',
            'Database schemas', 
            'File systems',
            'Configuration files',
            'Dependencies',
            'Interfaces'
        ],
        'Function': [
            'Features',
            'Error handling',
            'Calculations',
            'Transformations',
            'Workflows',
            'Business rules'
        ],
        'Data': [
            'Input data',
            'Output data',
            'Stored data',
            'Data states',
            'Data flows',
            'Data constraints'
        ],
        'Platform': [
            'Operating systems',
            'Browsers',
            'Hardware',
            'Networks',
            'External services',
            'Configurations'
        ],
        'Operations': [
            'User scenarios',
            'Startup/shutdown',
            'Recovery',
            'Maintenance',
            'Updates',
            'Integration'
        ],
        'Time': [
            'Concurrent usage',
            'Timeouts',
            'Date/time handling',
            'Scheduling',
            'Sequences',
            'Race conditions'
        ]
    }
    
    def __init__(self, product_name: str):
        self.product = product_name
        self.coverage_map = {element: [] for element in self.ELEMENTS}
        self.explored_areas = set()
    
    def map_product(self, element: str, specifics: List[str]):
        """
        Map specific product elements for coverage tracking.
        """
        if element in self.coverage_map:
            self.coverage_map[element].extend(specifics)
    
    def mark_explored(self, element: str, specific: str, session_id: str):
        """
        Mark an area as explored.
        """
        self.explored_areas.add((element, specific, session_id))
    
    def coverage_gaps(self) -> Dict[str, List[str]]:
        """
        Identify areas not yet explored.
        """
        gaps = {}
        explored_specifics = {(e, s) for e, s, _ in self.explored_areas}
        
        for element, specifics in self.coverage_map.items():
            unexplored = [s for s in specifics if (element, s) not in explored_specifics]
            if unexplored:
                gaps[element] = unexplored
        
        return gaps
    
    def suggest_charters(self) -> List[str]:
        """
        Suggest test charters based on coverage gaps.
        """
        charters = []
        gaps = self.coverage_gaps()
        
        for element, specifics in gaps.items():
            for specific in specifics[:3]:  # Top 3 per element
                charters.append(
                    f"Explore {specific} ({element}) to discover potential problems"
                )
        
        return charters
```

### Test Heuristics

```python
class TestHeuristics:
    """
    Heuristics are fallible methods for solving problems.
    Bach's testing heuristics for generating test ideas.
    """
    
    # ZOMBIE heuristic for boundaries
    ZOMBIE = {
        'Zero': 'Test with zero, empty, null, none',
        'One': 'Test with one, single, first, minimum',
        'Many': 'Test with many, multiple, maximum, large',
        'Boundary': 'Test at boundaries, edges, limits',
        'Interface': 'Test at interfaces, handoffs, integrations',
        'Exceptions': 'Test error conditions, invalid inputs, edge cases'
    }
    
    # CRUSSPIC STMPL for quality criteria
    QUALITY_CRITERIA = {
        'Capability': 'Can it perform its functions?',
        'Reliability': 'Will it work consistently?',
        'Usability': 'Can real users use it?',
        'Security': 'Is it protected from threats?',
        'Scalability': 'Does it handle growth?',
        'Performance': 'Is it fast enough?',
        'Installability': 'Can it be deployed?',
        'Compatibility': 'Does it work with other things?',
        'Supportability': 'Can it be maintained?',
        'Testability': 'Can it be tested effectively?',
        'Maintainability': 'Can it be changed?',
        'Portability': 'Does it work in different environments?',
        'Localizability': 'Can it be adapted for different locales?'
    }
    
    def generate_boundary_tests(self, variable: str, data_type: str) -> List[str]:
        """
        Generate test ideas using ZOMBIE heuristic.
        """
        tests = []
        
        if data_type == 'numeric':
            tests.extend([
                f"{variable} = 0 (Zero)",
                f"{variable} = 1 (One)",
                f"{variable} = -1 (Negative one)",
                f"{variable} = MAX_INT (Many/Boundary)",
                f"{variable} = MIN_INT (Many/Boundary)",
                f"{variable} = MAX + 1 (Boundary overflow)",
                f"{variable} = decimal value (Interface)",
                f"{variable} = null/undefined (Exception)",
                f"{variable} = NaN (Exception)",
            ])
        elif data_type == 'string':
            tests.extend([
                f"{variable} = '' (Zero/Empty)",
                f"{variable} = single char (One)",
                f"{variable} = very long string (Many)",
                f"{variable} = max length (Boundary)",
                f"{variable} = max + 1 (Boundary)",
                f"{variable} = special characters (Interface)",
                f"{variable} = unicode (Interface)",
                f"{variable} = null (Exception)",
                f"{variable} = SQL injection (Exception/Security)",
            ])
        elif data_type == 'collection':
            tests.extend([
                f"{variable} = [] empty (Zero)",
                f"{variable} = [1 item] (One)",
                f"{variable} = [many items] (Many)",
                f"{variable} = [max items] (Boundary)",
                f"{variable} = [duplicate items] (Interface)",
                f"{variable} = null (Exception)",
                f"{variable} = nested collections (Interface)",
            ])
        
        return tests
    
    def generate_quality_tests(self, feature: str) -> Dict[str, List[str]]:
        """
        Generate test ideas for each quality criterion.
        """
        tests = {}
        
        for criterion, question in self.QUALITY_CRITERIA.items():
            tests[criterion] = [
                f"{feature}: {question}",
                f"What would make {feature} fail {criterion.lower()}?",
                f"How would a user judge {feature}'s {criterion.lower()}?",
            ]
        
        return tests
    
    def soap_opera_testing(self, workflow: str) -> List[str]:
        """
        Soap Opera Testing: dramatic, complex, intertwined scenarios.
        Bach's technique for finding interaction bugs.
        """
        return [
            f"Start {workflow}, interrupt midway, start another",
            f"Run {workflow} with minimum permissions",
            f"Run {workflow} with conflicting concurrent users",
            f"Start {workflow}, lose connection, reconnect",
            f"Run {workflow} with corrupted cache/state",
            f"Complete {workflow}, immediately undo, redo",
            f"Run {workflow} at system resource limits",
            f"Interleave {workflow} with upgrade/migration",
        ]
    
    def touring_heuristics(self, application: str) -> Dict[str, str]:
        """
        Touring: systematic exploration strategies.
        Different "tours" reveal different problems.
        """
        return {
            'Guidebook Tour': f"Follow the documentation exactly for {application}",
            'Money Tour': f"Test the features that sell {application}",
            'Landmark Tour': f"Navigate between major features of {application}",
            'Intellectual Tour': f"Find the most complex parts of {application}",
            'FedEx Tour': f"Follow data through {application} end to end",
            'Garbage Tour': f"Look for dead code and unused features in {application}",
            'Bad Neighborhood Tour': f"Focus on historically buggy areas of {application}",
            'Museum Tour': f"Test legacy code and old features in {application}",
            'Back Alley Tour': f"Test least-used features of {application}",
            'All-Nighter Tour': f"Test {application} over extended time periods",
        }
```

### Rapid Software Testing Session

```python
class RapidTestingSession:
    """
    Rapid Software Testing: Bach & Bolton's methodology.
    Testing as a performance, not a procedure.
    """
    
    def __init__(self, 
                 product: str,
                 tester: 'SkilledTester',
                 stakeholder_info: Dict):
        self.product = product
        self.tester = tester
        self.stakeholder = stakeholder_info
        self.mental_model = ProductCoverageModel(product)
        self.oracles = OracleHeuristics()
        self.heuristics = TestHeuristics()
        self.sessions = []
        self.findings = []
    
    def analyze_context(self) -> ContextAnalysis:
        """
        Understand the project context before testing.
        """
        return ContextAnalysis(
            who_is_the_customer=self.stakeholder.get('customer'),
            what_is_the_mission=self.stakeholder.get('mission'),
            what_does_quality_mean=self.stakeholder.get('quality_definition'),
            what_threatens_quality=self.stakeholder.get('risks'),
            what_resources_exist=self.stakeholder.get('resources'),
            what_constraints_exist=self.stakeholder.get('constraints'),
            what_has_been_done=self.stakeholder.get('prior_testing'),
        )
    
    def create_test_strategy(self, context: ContextAnalysis) -> TestStrategy:
        """
        Build a test strategy based on context.
        No best practices—only practices that fit this context.
        """
        strategy = TestStrategy(product=self.product)
        
        # Prioritize based on risks
        for risk in context.what_threatens_quality:
            strategy.add_focus_area(
                area=risk.area,
                priority=risk.severity,
                techniques=self.select_techniques(risk),
                time_allocation=self.estimate_time(risk)
            )
        
        # Generate charters for each focus area
        for area in strategy.focus_areas:
            charters = self.generate_charters(area)
            strategy.add_charters(area.name, charters)
        
        return strategy
    
    def select_techniques(self, risk: Risk) -> List[str]:
        """
        Select testing techniques based on risk characteristics.
        """
        techniques = []
        
        if risk.involves_boundaries:
            techniques.append('Boundary Analysis (ZOMBIE)')
        if risk.involves_user_interaction:
            techniques.append('Scenario Testing')
            techniques.append('Touring')
        if risk.involves_data:
            techniques.append('Data Flow Testing')
            techniques.append('CRUD Testing')
        if risk.involves_integration:
            techniques.append('Interface Testing')
            techniques.append('Soap Opera Testing')
        if risk.involves_time:
            techniques.append('Stress Testing')
            techniques.append('Longevity Testing')
        
        # Always include exploratory
        techniques.append('Exploratory Testing')
        
        return techniques
    
    def run_session(self, charter: TestCharter) -> SessionReport:
        """
        Run a time-boxed exploratory testing session.
        """
        session = ExploratorySession(
            charter=str(charter),
            duration_minutes=charter.time_box,
            tester=self.tester.name
        )
        
        session.start()
        
        # The actual testing happens here—human cognition
        # This framework supports but doesn't replace the tester
        
        self.sessions.append(session)
        return session  # Tester controls when to end
    
    def debrief(self, session: ExploratorySession) -> DebriefNotes:
        """
        Post-session debrief: capture learnings and adjust strategy.
        """
        report = session.generate_report()
        
        debrief = DebriefNotes(
            session_id=id(session),
            what_was_tested=session.areas_explored,
            what_was_found=session.bugs,
            what_was_learned=self.extract_learnings(session),
            what_should_change=self.recommend_changes(session),
            new_questions=session.questions,
            new_risks=session.risks,
        )
        
        # Update mental model based on session
        for area in session.areas_explored:
            self.mental_model.mark_explored(
                area['element'],
                area['specific'],
                str(id(session))
            )
        
        return debrief
    
    def extract_learnings(self, session: ExploratorySession) -> List[str]:
        """
        What did we learn about the product?
        """
        learnings = []
        
        for note in session.notes:
            if 'learned' in note['content'].lower():
                learnings.append(note['content'])
            if 'realized' in note['content'].lower():
                learnings.append(note['content'])
            if 'discovered' in note['content'].lower():
                learnings.append(note['content'])
        
        return learnings
    
    def recommend_changes(self, session: ExploratorySession) -> List[str]:
        """
        What should we do differently next?
        """
        recommendations = []
        
        if session.session_metrics['bugs_found'] > 3:
            recommendations.append(
                "High bug density—consider deeper exploration of this area"
            )
        
        if session.session_metrics['questions_raised'] > 5:
            recommendations.append(
                "Many questions—schedule stakeholder discussion"
            )
        
        return recommendations
```

## Mental Model

Bach approaches testing by asking:

1. **What is the mission?** Who cares, and what do they need to know?
2. **What could go wrong?** Risks drive test focus
3. **How will I recognize a problem?** Which oracles apply?
4. **What have I covered?** Maintain a mental model of the product
5. **What did I learn?** Each test teaches something

## The Session Checklist

```
□ Charter defined (Explore X with Y to discover Z)
□ Time-box set (60-90 minutes typical)
□ Oracles identified (how will I recognize problems?)
□ Note-taking ready (real-time, not after)
□ Product model in mind (SFDPOT coverage)
□ Heuristics available (ZOMBIE, touring, soap opera)
□ Questions captured (for stakeholder follow-up)
□ Debrief scheduled (capture learnings immediately)
```

## Signature Bach Moves

- Session-Based Test Management (SBTM)
- Heuristic Test Strategy Model (HTSM)
- FEW HICCUPPS consistency oracles
- SFDPOT product coverage model
- Exploratory testing charters
- Context-driven approach (no best practices)
- Soap Opera Testing for complex scenarios
- Touring heuristics for systematic exploration
