---
name: bolton-rapid-software-testing
description: Test software in the style of Michael Bolton, Rapid Software Testing co-creator with James Bach. Emphasizes the distinction between testing and checking, critical thinking, oracles, and the social nature of quality. Use when designing test strategies, evaluating test automation, or developing critical thinking in testers.
---

# Michael Bolton Rapid Software Testing Style Guide

## Overview

Michael Bolton is the co-creator of Rapid Software Testing (with James Bach) and one of the most influential voices in the testing community. He is known for making crucial distinctions—most famously between "testing" (a human cognitive activity) and "checking" (a machine-executable verification). His work emphasizes that quality is a relationship between people, and that testing is fundamentally about critical thinking and learning.

## Core Philosophy

> "Testing is the process of evaluating a product by learning about it through experiencing, exploring, and experimenting."

> "Checking is the process of making evaluations by applying algorithmic decision rules to specific observations of a product."

> "Quality is value to some person(s) who matter(s)."

Bolton argues that much of what we call "automated testing" is actually "automated checking"—valuable, but not the same as the skilled cognitive work of testing. Real testing requires a human mind to recognize problems that we couldn't specify in advance.

## Design Principles

1. **Testing ≠ Checking**: Distinguish human investigation from algorithmic verification.

2. **Quality Is Relational**: Quality means value to someone who matters—understand who.

3. **Oracles Are Heuristic**: We recognize problems through fallible principles, not perfect rules.

4. **Testing Is Social**: Communicate findings in terms stakeholders understand and care about.

5. **Critical Thinking First**: Question everything, including your own assumptions.

## Testing vs. Checking

```
┌─────────────────────────────────────────────────────────────┐
│                     TESTING                                  │
│                                                              │
│  Human cognitive activity:                                   │
│  • Learning about the product                                │
│  • Exploring unknown territories                             │
│  • Recognizing problems we couldn't predict                  │
│  • Applying judgment and sapience                            │
│  • Adapting to what we discover                              │
│  • Modeling and questioning                                  │
│                                                              │
│  Cannot be automated (requires human mind)                   │
├─────────────────────────────────────────────────────────────┤
│                     CHECKING                                 │
│                                                              │
│  Algorithmic verification:                                   │
│  • Confirming expected behaviors                             │
│  • Applying decision rules                                   │
│  • Binary pass/fail outcomes                                 │
│  • Repeatable observations                                   │
│  • Regression detection                                      │
│  • Fast feedback on known behaviors                          │
│                                                              │
│  CAN be automated (but requires human design and oversight)  │
└─────────────────────────────────────────────────────────────┘

CRITICAL: "Automated testing" is mostly automated checking.
          A human DESIGNS the checks.
          A human INTERPRETS the results.
          A human DECIDES what problems matter.
```

## When Testing

### Always

- Distinguish what you're testing from what you're checking
- Identify who cares about quality and what they value
- Apply multiple oracles to recognize problems
- Report problems in terms of risk and stakeholder impact
- Question the requirements—they're someone's best guess
- Document your mental model of the product
- Learn continuously throughout testing

### Never

- Confuse "tests passed" with "product is good"
- Assume automation replaces testing
- Report only binary pass/fail without context
- Stop exploring when you find one problem
- Trust that absence of failures means absence of problems
- Ignore problems because they're not in requirements
- Treat testing as a phase that ends

### Prefer

- Exploring over scripted confirmation
- Learning over executing
- Thinking over clicking
- Questioning over accepting
- Modeling over listing
- Communicating over documenting
- Understanding over measuring

## Code Patterns

### Testing vs. Checking in Practice

```python
# This is a CHECK - algorithmic verification
def check_login_returns_token():
    """
    A check: Confirms a specific expected behavior.
    Valuable, but not testing.
    """
    response = api.login(username="valid", password="valid")
    assert response.status_code == 200
    assert "token" in response.json()


# This is TESTING - requires human cognition
class LoginTesting:
    """
    Testing: A human explores, learns, and discovers.
    Cannot be fully automated.
    """
    
    def explore_login_behavior(self):
        """
        A tester might wonder:
        - What happens with Unicode usernames?
        - What if I login from two devices simultaneously?
        - What if the password is extremely long?
        - What if I include SQL in the username?
        - What happens under high load?
        - What does the UI do while waiting?
        - How does a confused user perceive this?
        
        These questions emerge from a human mind engaging
        with the product. The answers require judgment to evaluate.
        """
        pass
    
    def recognize_problems(self, observation):
        """
        Applying oracles - human judgment about what's problematic.
        
        Is a 3-second login response time a problem?
        - For a banking app: probably yes
        - For a first login setting up encryption: probably fine
        
        Context and stakeholder value matter.
        """
        pass


# The distinction in automation strategy
class TestingStrategy:
    """
    Bolton's approach: automate checking, support testing.
    """
    
    def __init__(self):
        self.checks = []      # Automate these
        self.test_ideas = []  # Human explores these
    
    def automate_check(self, check_function):
        """
        Checks: Automate because they're algorithmic.
        - Regression checks
        - Smoke checks
        - Unit checks
        - Integration checks
        
        These verify known behaviors haven't broken.
        """
        self.checks.append(check_function)
    
    def add_test_idea(self, idea: str, oracles: list):
        """
        Test ideas: Human explores with oracles.
        
        These require judgment, creativity, and learning.
        They cannot be reduced to pass/fail.
        """
        self.test_ideas.append({
            'idea': idea,
            'oracles': oracles,
            'status': 'unexplored',
            'findings': []
        })
    
    def support_testing(self):
        """
        Automation should SUPPORT human testing, not replace it.
        
        Examples:
        - Test data generators
        - Log analyzers
        - State visualizers
        - Session recorders
        - Comparison tools
        """
        pass
```

### Quality as Value to Stakeholders

```python
class QualityPerspective:
    """
    Quality is relational: value to some person(s) who matter(s).
    Different stakeholders have different quality criteria.
    """
    
    def __init__(self, product: str):
        self.product = product
        self.stakeholders = {}
    
    def identify_stakeholder(self, 
                              name: str, 
                              role: str,
                              values: list,
                              fears: list):
        """
        Identify what quality means to each stakeholder.
        """
        self.stakeholders[name] = {
            'role': role,
            'values': values,    # What they want
            'fears': fears,      # What they worry about
        }
    
    def analyze_quality_dimensions(self):
        """
        Example stakeholder analysis for a banking app.
        """
        stakeholders = {
            'end_user': {
                'values': ['fast transactions', 'easy to use', 'works offline'],
                'fears': ['losing money', 'confusing interface', 'downtime'],
            },
            'security_officer': {
                'values': ['encryption', 'audit trails', 'compliance'],
                'fears': ['breaches', 'regulatory fines', 'reputation damage'],
            },
            'operations': {
                'values': ['reliability', 'easy deployment', 'monitoring'],
                'fears': ['3am pages', 'cascading failures', 'data loss'],
            },
            'product_manager': {
                'values': ['features ship on time', 'user satisfaction', 'metrics'],
                'fears': ['missed deadlines', 'bad reviews', 'churn'],
            },
            'ceo': {
                'values': ['revenue', 'reputation', 'growth'],
                'fears': ['lawsuits', 'headline failures', 'losing market'],
            },
        }
        
        return stakeholders
    
    def frame_bug_report(self, 
                          bug: str, 
                          affected_stakeholders: list) -> str:
        """
        Frame bug reports in terms of stakeholder impact.
        
        Not: "Button color is wrong"
        But: "Brand inconsistency may confuse users and concern 
             marketing about brand perception"
        """
        impacts = []
        for stakeholder in affected_stakeholders:
            impact = self.assess_impact(bug, stakeholder)
            impacts.append(f"{stakeholder}: {impact}")
        
        return f"Bug: {bug}\nStakeholder Impact:\n" + "\n".join(impacts)
```

### Oracle Design

```python
class OracleFramework:
    """
    Oracles: Principles by which we recognize problems.
    Bolton emphasizes that all oracles are heuristic (fallible).
    """
    
    def __init__(self):
        self.applied_oracles = []
    
    # Bolton's Oracle Categories
    ORACLE_CATEGORIES = {
        'reference': {
            'description': 'Compare to authoritative sources',
            'examples': [
                'Requirements documents',
                'Specifications',
                'Standards (ISO, RFC)',
                'Regulations (GDPR, HIPAA)',
                'Contracts',
            ],
            'fallibility': 'Requirements can be wrong or incomplete'
        },
        'comparable': {
            'description': 'Compare to similar things',
            'examples': [
                'Previous versions',
                'Competitor products',
                'Similar features in same product',
                'Industry norms',
            ],
            'fallibility': 'Similar is not identical; context differs'
        },
        'model': {
            'description': 'Compare to mental or formal models',
            'examples': [
                'User mental models',
                'Developer mental models',
                'State machines',
                'Mathematical models',
            ],
            'fallibility': 'Models are simplifications of reality'
        },
        'consistent': {
            'description': 'Compare to itself',
            'examples': [
                'Different parts of the product',
                'Different states of the product',
                'Different user paths to same result',
            ],
            'fallibility': 'Inconsistency might be intentional'
        },
        'claims': {
            'description': 'Compare to what was promised',
            'examples': [
                'Marketing materials',
                'Help documentation',
                'Error messages',
                'UI labels and tooltips',
            ],
            'fallibility': 'Claims might be aspirational'
        },
        'feeling': {
            'description': 'Compare to what feels right',
            'examples': [
                'User experience intuition',
                'Performance perception',
                'Aesthetic sense',
                'Emotional response',
            ],
            'fallibility': 'Feelings are personal and variable'
        },
    }
    
    def apply_oracle(self,
                      observation: str,
                      category: str,
                      reference: str) -> dict:
        """
        Apply an oracle and record the reasoning.
        """
        return {
            'observation': observation,
            'oracle_category': category,
            'reference': reference,
            'evaluation': None,  # Human judgment required
            'confidence': None,  # How reliable is this oracle here?
            'fallibility_note': self.ORACLE_CATEGORIES[category]['fallibility']
        }
    
    def question_oracle(self, oracle_application: dict) -> list:
        """
        Bolton's approach: Always question the oracle itself.
        """
        questions = [
            f"Is '{oracle_application['reference']}' a reliable reference?",
            f"Could {oracle_application['oracle_category']} mislead us here?",
            "What would make this oracle fail?",
            "Are there other oracles that might disagree?",
            "Who would this evaluation matter to?",
        ]
        return questions
```

### Critical Thinking in Testing

```python
class CriticalThinkingFramework:
    """
    Bolton emphasizes critical thinking as the core testing skill.
    """
    
    # Questions to ask about any claim
    CRITICAL_QUESTIONS = {
        'source': [
            "Who is making this claim?",
            "What is their expertise?",
            "What might they be wrong about?",
            "What might they not know?",
        ],
        'evidence': [
            "What evidence supports this?",
            "How was the evidence gathered?",
            "Could the evidence be misleading?",
            "What evidence would contradict this?",
        ],
        'assumptions': [
            "What assumptions does this rely on?",
            "Are the assumptions valid?",
            "What if the assumptions are wrong?",
        ],
        'implications': [
            "If this is true, what follows?",
            "If this is false, what follows?",
            "What are the consequences of being wrong?",
        ],
        'alternatives': [
            "What other explanations are possible?",
            "What are we not considering?",
            "What would someone who disagrees say?",
        ],
    }
    
    def analyze_test_result(self, result: dict) -> dict:
        """
        Apply critical thinking to a test result.
        """
        analysis = {
            'result': result,
            'questions': [],
            'alternative_explanations': [],
            'confidence': None,
        }
        
        if result['status'] == 'pass':
            analysis['questions'] = [
                "Does passing this test mean the feature works?",
                "What problems might exist that this test wouldn't catch?",
                "Is the test checking the right thing?",
                "Could the test pass for the wrong reasons?",
            ]
        else:
            analysis['questions'] = [
                "Is this a product problem or a test problem?",
                "What is the actual behavior vs. expected?",
                "Who would care about this problem?",
                "How severe is this really?",
            ]
        
        return analysis
    
    def question_metric(self, metric_name: str, value: float) -> list:
        """
        Bolton is skeptical of metrics. Question them.
        """
        return [
            f"What does '{metric_name} = {value}' actually tell us?",
            f"What doesn't it tell us?",
            f"How could this metric mislead us?",
            f"What behavior might it incentivize?",
            f"Is the target (if any) meaningful?",
            f"Who chose this metric and why?",
        ]
    
    def question_coverage(self, coverage_percent: float) -> list:
        """
        Code coverage is often misunderstood.
        """
        return [
            f"{coverage_percent}% of what? Lines? Branches? Paths?",
            "Does covering a line mean testing it?",
            "What about the uncovered code?",
            "Are the assertions meaningful?",
            "Is coverage a goal or an indicator?",
            "100% coverage with bad tests = false confidence",
        ]
```

### Bug Advocacy

```python
class BugAdvocacy:
    """
    Bolton's approach: Advocate for bugs to be understood and fixed.
    A bug report is a work of technical writing.
    """
    
    def write_bug_report(self,
                          summary: str,
                          observation: str,
                          oracles: list,
                          stakeholder_impact: str,
                          reproduction: str = None) -> dict:
        """
        A good bug report tells a story.
        """
        return {
            'summary': summary,  # Short, descriptive, searchable
            
            'what_i_did': reproduction or "See attached session notes",
            
            'what_happened': observation,
            
            'why_this_matters': stakeholder_impact,  # The key part!
            
            'oracles_applied': oracles,  # How I recognized this as a problem
            
            'additional_context': {
                'environment': "...",
                'related_observations': [],
                'questions': [],  # Things I'm unsure about
            },
            
            'suggested_priority': None,  # "I suggest, you decide"
        }
    
    def frame_bug_for_stakeholder(self,
                                   bug: dict,
                                   stakeholder: str) -> str:
        """
        Frame the same bug differently for different audiences.
        """
        frames = {
            'developer': f"""
                Bug: {bug['summary']}
                Repro: {bug['what_i_did']}
                Observed: {bug['what_happened']}
                Logs: [attached]
            """,
            
            'product_manager': f"""
                Issue: {bug['summary']}
                Impact: {bug['why_this_matters']}
                User experience: [description]
                Recommendation: [priority suggestion]
            """,
            
            'executive': f"""
                Risk: {bug['summary']}
                Business impact: {bug['why_this_matters']}
                Recommendation: [action needed]
            """,
        }
        
        return frames.get(stakeholder, frames['developer'])
```

### Session-Based Testing with RST

```python
class RapidTestingSession:
    """
    A Rapid Software Testing session combines
    exploration, checking, and critical thinking.
    """
    
    def __init__(self, 
                 charter: str,
                 time_box_minutes: int = 90):
        self.charter = charter
        self.time_box = time_box_minutes
        self.notes = []
        self.checks_performed = []
        self.oracles_applied = []
        self.problems_found = []
        self.questions_raised = []
    
    def record_observation(self, 
                            what_i_did: str,
                            what_happened: str,
                            my_interpretation: str):
        """
        Record observations with interpretation.
        """
        self.notes.append({
            'time': datetime.now(),
            'action': what_i_did,
            'result': what_happened,
            'interpretation': my_interpretation,
            'oracle_used': None,  # To be filled
        })
    
    def recognize_problem(self,
                           observation: str,
                           oracle: str,
                           stakeholders_affected: list,
                           my_reasoning: str):
        """
        Document problem recognition with full reasoning.
        """
        self.problems_found.append({
            'observation': observation,
            'oracle': oracle,
            'reasoning': my_reasoning,
            'stakeholders': stakeholders_affected,
            'confidence': None,  # How sure am I?
            'questions': [],     # What am I unsure about?
        })
    
    def distinguish_testing_from_checking(self):
        """
        At the end, review: what was testing vs. checking?
        """
        return {
            'testing_activities': [
                n for n in self.notes 
                if 'explored' in n['action'].lower() or
                   'discovered' in n['interpretation'].lower()
            ],
            'checking_activities': self.checks_performed,
            'ratio': f"Testing: {len(self.notes) - len(self.checks_performed)}, "
                    f"Checking: {len(self.checks_performed)}",
        }
    
    def debrief(self) -> dict:
        """
        Post-session debrief.
        """
        return {
            'charter': self.charter,
            'time_spent': self.time_box,
            
            'what_i_tested': [n['action'] for n in self.notes],
            
            'what_i_learned': [
                n['interpretation'] for n in self.notes
                if 'learned' in n['interpretation'].lower() or
                   'surprised' in n['interpretation'].lower()
            ],
            
            'problems_found': self.problems_found,
            
            'questions_for_stakeholders': self.questions_raised,
            
            'suggested_next_sessions': [],
            
            'coverage_assessment': {
                'what_i_covered': "...",
                'what_i_didnt_cover': "...",
                'what_i_couldnt_cover': "...",
            },
        }
```

## Mental Model

Bolton approaches testing by asking:

1. **Am I testing or checking?** Know the difference
2. **Who matters?** Quality is value to someone
3. **How do I recognize problems?** Apply oracles consciously
4. **What am I assuming?** Question everything
5. **How do I communicate this?** Frame for your audience

## The RST Checklist

```
□ Charter defined with clear scope
□ Stakeholders identified (who cares?)
□ Oracles selected (how will I recognize problems?)
□ Testing distinguished from checking
□ Observations recorded with interpretation
□ Problems framed in stakeholder terms
□ Questions captured for follow-up
□ Session debriefed and learnings captured
```

## Signature Bolton Moves

- Testing vs. Checking distinction
- Quality as value to stakeholders
- Oracles are heuristic (fallible)
- Critical thinking as core skill
- Bug advocacy (not just reporting)
- Framing problems for audiences
- Questioning metrics and coverage
- Testing is a social activity
