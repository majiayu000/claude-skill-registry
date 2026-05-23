---
name: Sales Engineering
description: Supporting sales with technical expertise, demos, and proof-of-concept implementations
---

# Sales Engineering

## Current Level: Expert (Enterprise Scale)

## Domain: Go-to-Market Tech
## Skill ID: 148

---

## Executive Summary

Sales Engineering enables supporting sales with technical expertise, demos, and proof-of-concept implementations. This capability is essential for bridging the gap between sales and engineering, demonstrating product value, and closing deals.

### Strategic Necessity

- **Sales Support**: Provide technical support to sales
- **Product Demonstrations**: Demonstrate product value
- **Proof of Concept**: Build PoC implementations
- **Technical Objections**: Overcome technical objections
- **Deal Closure**: Help close deals

---

## Technical Deep Dive

### Sales Engineering Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Sales Engineering Framework                           │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Sales      │    │   Technical  │    │   Demo      │                  │
│  │   Support   │───▶│   Expertise │───▶│   Creation  │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Pre-Sales Activities                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Discovery│  │  Solution │  │  Demo     │  │  PoC      │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Sales Support                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Objection │  │  Technical │  │  Pricing  │  │  Contract │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Post-Sales Handoff                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Onboard  │  │  Training  │  │  Support  │  │  Success  │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pre-Sales Activities

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OpportunityStage(Enum):
    """Opportunity stages"""
    DISCOVERY = "discovery"
    QUALIFICATION = "qualification"
    SOLUTION_DESIGN = "solution_design"
    DEMO = "demo"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class PoCStatus(Enum):
    """PoC status"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

@dataclass
class Opportunity:
    """Opportunity definition"""
    opportunity_id: str
    account_name: str
    contact_name: str
    stage: OpportunityStage
    value: float
    probability: float
    requirements: List[str]
    challenges: List[str]
    created_at: str
    updated_at: str

@dataclass
class Demo:
    """Demo definition"""
    demo_id: str
    opportunity_id: str
    title: str
    description: str
    features: List[str]
    use_cases: List[str]
    scheduled_at: str
    duration_minutes: int
    created_at: str

@dataclass
class ProofOfConcept:
    """Proof of concept definition"""
    poc_id: str
    opportunity_id: str
    title: str
    description: str
    scope: List[str]
    success_criteria: List[str]
    status: PoCStatus
    start_date: str
    end_date: str
    created_at: str

class SalesEngineer:
    """Sales engineering specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.opportunity_store = OpportunityStore(config['opportunity_store'])
        self.demo_creator = DemoCreator(config['demo'])
        self.poc_builder = PoCBuilder(config['poc'])
        
    async def support_discovery(
        self,
        opportunity: Opportunity
    ) -> Dict[str, Any]:
        """Support discovery phase"""
        logger.info(f"Supporting discovery for opportunity: {opportunity.opportunity_id}")
        
        # Analyze requirements
        requirements_analysis = await self._analyze_requirements(opportunity)
        
        # Identify challenges
        challenges = await self._identify_challenges(opportunity)
        
        # Recommend solutions
        solutions = await self._recommend_solutions(opportunity, requirements_analysis, challenges)
        
        # Compile discovery results
        results = {
            'opportunity_id': opportunity.opportunity_id,
            'requirements_analysis': requirements_analysis,
            'challenges': challenges,
            'solutions': solutions,
            'completed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Discovery supported: {opportunity.opportunity_id}")
        
        return results
    
    async def _analyze_requirements(
        self,
        opportunity: Opportunity
    ) -> Dict[str, Any]:
        """Analyze opportunity requirements"""
        analysis = {
            'technical_requirements': [],
            'functional_requirements': [],
            'integration_requirements': [],
            'security_requirements': [],
            'compliance_requirements': []
        }
        
        # Categorize requirements
        for requirement in opportunity.requirements:
            # Determine requirement type
            req_type = self._categorize_requirement(requirement)
            
            # Add to appropriate category
            analysis[f"{req_type}_requirements"].append(requirement)
        
        return analysis
    
    def _categorize_requirement(self, requirement: str) -> str:
        """Categorize requirement"""
        # Implementation would use NLP or keyword matching
        if 'security' in requirement.lower():
            return 'security'
        elif 'integration' in requirement.lower():
            return 'integration'
        elif 'compliance' in requirement.lower():
            return 'compliance'
        elif 'technical' in requirement.lower():
            return 'technical'
        else:
            return 'functional'
    
    async def _identify_challenges(
        self,
        opportunity: Opportunity
    ) -> List[Dict[str, Any]]:
        """Identify potential challenges"""
        challenges = []
        
        # Analyze each challenge
        for challenge in opportunity.challenges:
            challenge_analysis = {
                'challenge': challenge,
                'severity': self._assess_severity(challenge),
                'mitigation': self._suggest_mitigation(challenge)
            }
            challenges.append(challenge_analysis)
        
        return challenges
    
    def _assess_severity(self, challenge: str) -> str:
        """Assess challenge severity"""
        # Implementation would assess severity based on keywords
        if 'critical' in challenge.lower():
            return 'high'
        elif 'major' in challenge.lower():
            return 'medium'
        else:
            return 'low'
    
    def _suggest_mitigation(self, challenge: str) -> str:
        """Suggest mitigation for challenge"""
        # Implementation would suggest mitigation strategies
        return "Custom solution required"
    
    async def _recommend_solutions(
        self,
        opportunity: Opportunity,
        requirements_analysis: Dict[str, Any],
        challenges: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Recommend solutions for opportunity"""
        solutions = []
        
        # Analyze requirements
        for req_type, requirements in requirements_analysis.items():
            if requirements:
                solution = {
                    'type': req_type.replace('_requirements', ''),
                    'requirements': requirements,
                    'solution': self._propose_solution(req_type, requirements),
                    'effort': self._estimate_effort(req_type, requirements),
                    'timeline': self._estimate_timeline(req_type, requirements)
                }
                solutions.append(solution)
        
        # Address challenges
        for challenge in challenges:
            if challenge['severity'] == 'high':
                solution = {
                    'type': 'challenge_mitigation',
                    'challenge': challenge['challenge'],
                    'solution': challenge['mitigation'],
                    'effort': 'medium',
                    'timeline': '2-4 weeks'
                }
                solutions.append(solution)
        
        return solutions
    
    def _propose_solution(
        self,
        req_type: str,
        requirements: List[str]
    ) -> str:
        """Propose solution for requirements"""
        # Implementation would propose solution based on requirements
        return "Custom solution"
    
    def _estimate_effort(
        self,
        req_type: str,
        requirements: List[str]
    ) -> str:
        """Estimate effort for solution"""
        # Implementation would estimate effort
        return "medium"
    
    def _estimate_timeline(
        self,
        req_type: str,
        requirements: List[str]
    ) -> str:
        """Estimate timeline for solution"""
        # Implementation would estimate timeline
        return "2-4 weeks"
    
    async def create_demo(
        self,
        opportunity: Opportunity
    ) -> Demo:
        """Create demo for opportunity"""
        logger.info(f"Creating demo for opportunity: {opportunity.opportunity_id}")
        
        # Generate demo ID
        demo_id = self._generate_demo_id()
        
        # Create demo
        demo = await self.demo_creator.create_demo(
            demo_id=demo_id,
            opportunity_id=opportunity.opportunity_id,
            title=f"{opportunity.account_name} Demo",
            description=self._generate_demo_description(opportunity),
            features=self._select_demo_features(opportunity),
            use_cases=self._select_use_cases(opportunity),
            scheduled_at=self._schedule_demo(opportunity),
            duration_minutes=60
        )
        
        logger.info(f"Demo created: {demo_id}")
        
        return demo
    
    def _generate_demo_description(self, opportunity: Opportunity) -> str:
        """Generate demo description"""
        return f"Customized demo for {opportunity.account_name} addressing their specific needs"
    
    def _select_demo_features(self, opportunity: Opportunity) -> List[str]:
        """Select features for demo"""
        # Implementation would select relevant features based on requirements
        return []
    
    def _select_use_cases(self, opportunity: Opportunity) -> List[str]:
        """Select use cases for demo"""
        # Implementation would select relevant use cases
        return []
    
    def _schedule_demo(self, opportunity: Opportunity) -> str:
        """Schedule demo"""
        # Implementation would schedule demo
        return datetime.utcnow().isoformat()
    
    async def build_poc(
        self,
        opportunity: Opportunity
    ) -> ProofOfConcept:
        """Build proof of concept for opportunity"""
        logger.info(f"Building PoC for opportunity: {opportunity.opportunity_id}")
        
        # Generate PoC ID
        poc_id = self._generate_poc_id()
        
        # Define PoC scope
        scope = self._define_poc_scope(opportunity)
        
        # Define success criteria
        success_criteria = self._define_success_criteria(opportunity)
        
        # Create PoC
        poc = await self.poc_builder.build_poc(
            poc_id=poc_id,
            opportunity_id=opportunity.opportunity_id,
            title=f"{opportunity.account_name} PoC",
            description=self._generate_poc_description(opportunity),
            scope=scope,
            success_criteria=success_criteria,
            status=PoCStatus.PLANNED,
            start_date=self._calculate_poc_start_date(),
            end_date=self._calculate_poc_end_date()
        )
        
        logger.info(f"PoC built: {poc_id}")
        
        return poc
    
    def _define_poc_scope(self, opportunity: Opportunity) -> List[str]:
        """Define PoC scope"""
        # Implementation would define scope based on requirements
        return []
    
    def _define_success_criteria(self, opportunity: Opportunity) -> List[str]:
        """Define PoC success criteria"""
        # Implementation would define success criteria
        return []
    
    def _generate_poc_description(self, opportunity: Opportunity) -> str:
        """Generate PoC description"""
        return f"Proof of concept for {opportunity.account_name}"
    
    def _calculate_poc_start_date(self) -> str:
        """Calculate PoC start date"""
        from datetime import timedelta
        start_date = datetime.utcnow() + timedelta(weeks=1)
        return start_date.isoformat()
    
    def _calculate_poc_end_date(self) -> str:
        """Calculate PoC end date"""
        from datetime import timedelta
        end_date = datetime.utcnow() + timedelta(weeks=5)
        return end_date.isoformat()
    
    def _generate_demo_id(self) -> str:
        """Generate unique demo ID"""
        import uuid
        return f"demo_{uuid.uuid4().hex}"
    
    def _generate_poc_id(self) -> str:
        """Generate unique PoC ID"""
        import uuid
        return f"poc_{uuid.uuid4().hex}"

class DemoCreator:
    """Demo creation specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_demo(
        self,
        demo_id: str,
        opportunity_id: str,
        title: str,
        description: str,
        features: List[str],
        use_cases: List[str],
        scheduled_at: str,
        duration_minutes: int
    ) -> Demo:
        """Create demo"""
        # Create demo environment
        await self._create_demo_environment(demo_id)
        
        # Configure demo data
        await self._configure_demo_data(demo_id, features)
        
        # Create demo
        demo = Demo(
            demo_id=demo_id,
            opportunity_id=opportunity_id,
            title=title,
            description=description,
            features=features,
            use_cases=use_cases,
            scheduled_at=scheduled_at,
            duration_minutes=duration_minutes,
            created_at=datetime.utcnow().isoformat()
        )
        
        return demo
    
    async def _create_demo_environment(self, demo_id: str):
        """Create demo environment"""
        # Implementation would create demo environment
        pass
    
    async def _configure_demo_data(self, demo_id: str, features: List[str]):
        """Configure demo data"""
        # Implementation would configure demo data
        pass

class PoCBuilder:
    """PoC building specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def build_poc(
        self,
        poc_id: str,
        opportunity_id: str,
        title: str,
        description: str,
        scope: List[str],
        success_criteria: List[str],
        status: PoCStatus,
        start_date: str,
        end_date: str
    ) -> ProofOfConcept:
        """Build proof of concept"""
        # Create PoC environment
        await self._create_poc_environment(poc_id)
        
        # Implement PoC
        await self._implement_poc(poc_id, scope)
        
        # Test PoC
        await self._test_poc(poc_id, success_criteria)
        
        # Create PoC
        poc = ProofOfConcept(
            poc_id=poc_id,
            opportunity_id=opportunity_id,
            title=title,
            description=description,
            scope=scope,
            success_criteria=success_criteria,
            status=status,
            start_date=start_date,
            end_date=end_date,
            created_at=datetime.utcnow().isoformat()
        )
        
        return poc
    
    async def _create_poc_environment(self, poc_id: str):
        """Create PoC environment"""
        # Implementation would create PoC environment
        pass
    
    async def _implement_poc(self, poc_id: str, scope: List[str]):
        """Implement PoC"""
        # Implementation would implement PoC features
        pass
    
    async def _test_poc(self, poc_id: str, success_criteria: List[str]):
        """Test PoC"""
        # Implementation would test PoC against success criteria
        pass

class OpportunityStore:
    """Opportunity storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_opportunity(self, opportunity: Opportunity):
        """Create opportunity"""
        # Implementation would store in database
        pass
    
    async def get_opportunity(self, opportunity_id: str) -> Opportunity:
        """Get opportunity"""
        # Implementation would query database
        return None
    
    async def update_opportunity(self, opportunity: Opportunity):
        """Update opportunity"""
        # Implementation would update database
        pass
```

### Sales Support

```python
class SalesSupport:
    """Sales support specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.objection_handler = ObjectionHandler(config['objections'])
        self.pricing_specialist = PricingSpecialist(config['pricing'])
        self.contract_specialist = ContractSpecialist(config['contracts'])
        
    async def handle_objections(
        self,
        opportunity: Opportunity,
        objections: List[str]
    ) -> Dict[str, Any]:
        """Handle sales objections"""
        logger.info(f"Handling objections for opportunity: {opportunity.opportunity_id}")
        
        # Analyze objections
        analyzed_objections = await self._analyze_objections(objections)
        
        # Prepare responses
        responses = await self._prepare_objection_responses(analyzed_objections)
        
        # Compile results
        results = {
            'opportunity_id': opportunity.opportunity_id,
            'objections': analyzed_objections,
            'responses': responses,
            'handled_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Objections handled: {opportunity.opportunity_id}")
        
        return results
    
    async def _analyze_objections(
        self,
        objections: List[str]
    ) -> List[Dict[str, Any]]:
        """Analyze sales objections"""
        analyzed = []
        
        for objection in objections:
            analysis = {
                'objection': objection,
                'type': self._categorize_objection(objection),
                'severity': self._assess_objection_severity(objection),
                'root_cause': self._identify_root_cause(objection)
            }
            analyzed.append(analysis)
        
        return analyzed
    
    def _categorize_objection(self, objection: str) -> str:
        """Categorize objection"""
        # Implementation would categorize objection
        if 'price' in objection.lower():
            return 'pricing'
        elif 'feature' in objection.lower():
            return 'feature'
        elif 'security' in objection.lower():
            return 'security'
        elif 'integration' in objection.lower():
            return 'integration'
        else:
            return 'other'
    
    def _assess_objection_severity(self, objection: str) -> str:
        """Assess objection severity"""
        # Implementation would assess severity
        return 'medium'
    
    def _identify_root_cause(self, objection: str) -> str:
        """Identify root cause of objection"""
        # Implementation would identify root cause
        return "Unknown"
    
    async def _prepare_objection_responses(
        self,
        analyzed_objections: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Prepare objection responses"""
        responses = []
        
        for objection in analyzed_objections:
            response = {
                'objection': objection['objection'],
                'type': objection['type'],
                'response': self._generate_response(objection),
                'evidence': self._gather_evidence(objection),
                'follow_up': self._suggest_follow_up(objection)
            }
            responses.append(response)
        
        return responses
    
    def _generate_response(self, objection: Dict[str, Any]) -> str:
        """Generate response to objection"""
        # Implementation would generate response
        return "Custom response"
    
    def _gather_evidence(self, objection: Dict[str, Any]) -> List[str]:
        """Gather evidence for response"""
        # Implementation would gather evidence
        return []
    
    def _suggest_follow_up(self, objection: Dict[str, Any]) -> str:
        """Suggest follow-up action"""
        # Implementation would suggest follow-up
        return "Schedule follow-up meeting"
    
    async def provide_pricing_guidance(
        self,
        opportunity: Opportunity
    ) -> Dict[str, Any]:
        """Provide pricing guidance"""
        logger.info(f"Providing pricing guidance for opportunity: {opportunity.opportunity_id}")
        
        # Analyze opportunity value
        value_analysis = await self._analyze_opportunity_value(opportunity)
        
        # Recommend pricing model
        pricing_model = await self.pricing_specialist.recommend_pricing_model(
            opportunity,
            value_analysis
        )
        
        # Calculate pricing
        pricing = await self.pricing_specialist.calculate_pricing(
            opportunity,
            pricing_model
        )
        
        # Compile results
        results = {
            'opportunity_id': opportunity.opportunity_id,
            'value_analysis': value_analysis,
            'pricing_model': pricing_model,
            'pricing': pricing,
            'provided_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Pricing guidance provided: {opportunity.opportunity_id}")
        
        return results
    
    async def _analyze_opportunity_value(
        self,
        opportunity: Opportunity
    ) -> Dict[str, Any]:
        """Analyze opportunity value"""
        return {
            'estimated_value': opportunity.value,
            'value_drivers': [],
            'roi_calculation': {}
        }
    
    async def support_contract_negotiation(
        self,
        opportunity: Opportunity
    ) -> Dict[str, Any]:
        """Support contract negotiation"""
        logger.info(f"Supporting contract negotiation for opportunity: {opportunity.opportunity_id}")
        
        # Prepare contract terms
        contract_terms = await self.contract_specialist.prepare_contract_terms(opportunity)
        
        # Identify negotiation points
        negotiation_points = await self._identify_negotiation_points(opportunity)
        
        # Prepare negotiation strategy
        negotiation_strategy = self._prepare_negotiation_strategy(
            contract_terms,
            negotiation_points
        )
        
        # Compile results
        results = {
            'opportunity_id': opportunity.opportunity_id,
            'contract_terms': contract_terms,
            'negotiation_points': negotiation_points,
            'negotiation_strategy': negotiation_strategy,
            'supported_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Contract negotiation supported: {opportunity.opportunity_id}")
        
        return results
    
    def _prepare_negotiation_strategy(
        self,
        contract_terms: Dict[str, Any],
        negotiation_points: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Prepare negotiation strategy"""
        return {
            'must_haves': [],
            'nice_to_haves': [],
            'trade_offs': [],
            'walk_away_points': []
        }
    
    async def _identify_negotiation_points(
        self,
        opportunity: Opportunity
    ) -> List[Dict[str, Any]]:
        """Identify negotiation points"""
        # Implementation would identify negotiation points
        return []

class ObjectionHandler:
    """Objection handling specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config

class PricingSpecialist:
    """Pricing specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def recommend_pricing_model(
        self,
        opportunity: Opportunity,
        value_analysis: Dict[str, Any]
    ) -> str:
        """Recommend pricing model"""
        # Implementation would recommend pricing model
        return "subscription"
    
    async def calculate_pricing(
        self,
        opportunity: Opportunity,
        pricing_model: str
    ) -> Dict[str, Any]:
        """Calculate pricing"""
        # Implementation would calculate pricing
        return {}

class ContractSpecialist:
    """Contract specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def prepare_contract_terms(
        self,
        opportunity: Opportunity
    ) -> Dict[str, Any]:
        """Prepare contract terms"""
        # Implementation would prepare contract terms
        return {}
```

---

## Tooling & Tech Stack

### Demo Tools
- **Zoom**: Video conferencing
- **Google Meet**: Video conferencing
- **Loom**: Video recording
- **OBS Studio**: Screen recording
- **Figma**: Design

### PoC Tools
- **Docker**: Containerization
- **Kubernetes**: Orchestration
- **AWS**: Cloud platform
- **Azure**: Cloud platform
- **GCP**: Cloud platform

### CRM Tools
- **Salesforce**: CRM
- **HubSpot**: CRM
- **Pipedrive**: CRM
- **Zoho CRM**: CRM
- **Monday.com**: CRM

### Collaboration Tools
- **Slack**: Team communication
- **Microsoft Teams**: Team collaboration
- **Notion**: Documentation
- **Confluence**: Documentation
- **Miro**: Visual collaboration

---

## Configuration Essentials

### Sales Engineering Configuration

```yaml
# config/sales_engineering_config.yaml
sales_engineering:
  discovery:
    enabled: true
    methods:
      - "discovery_call"
      - "technical_assessment"
      - "requirements_gathering"
    
    deliverables:
      - "requirements_document"
      - "solution_proposal"
      - "architecture_diagram"
  
  demo:
    enabled: true
    duration_minutes: 60
    preparation_time: "2-4 hours"
    
    environment:
      type: "sandbox"
      data_source: "demo_data"
      refresh_frequency: "daily"
    
    features:
      customization: true
      branding: true
      use_case_specific: true
  
  poc:
    enabled: true
    duration_weeks: 4
    
    scope:
      max_features: 5
      max_integrations: 3
      max_users: 10
    
    success_criteria:
      - "functional_requirements_met"
      - "performance_benchmarks_met"
      - "security_requirements_met"
      - "user_acceptance"
    
    deliverables:
      - "poc_documentation"
      - "demo_video"
      - "success_report"
      - "implementation_guide"
  
  objections:
    common_objections:
      - type: "pricing"
        responses:
          - "Value-based_pricing"
          - "ROI_calculation"
          - "Competitive_comparison"
      
      - type: "feature"
        responses:
          - "Feature_roadmap"
          - "Custom_development"
          - "Workaround_solutions"
      
      - type: "security"
        responses:
          - "Security_certifications"
          - "Compliance_documentation"
          - "Security_audit_report"
      
      - type: "integration"
        responses:
          - "Integration_options"
          - "API_documentation"
          - "Partner_integrations"
  
  pricing:
    models:
      - "subscription"
      - "usage_based"
      - "enterprise"
    
    discount_policy:
      enabled: true
      max_discount: 0.2  # 20%
      approval_required: true
      discount_threshold: 10000  # USD
  
  contracts:
    templates:
      - "standard_sla"
      - "enterprise_sla"
      - "custom_sla"
    
    terms:
      payment_terms:
        - "net_30"
        - "net_60"
        - "annual_upfront"
      
      support_levels:
        - "standard"
        - "premium"
        - "enterprise"
      
      sla_levels:
        - "99.5%"
        - "99.9%"
        - "99.99%"
```

---

## Code Examples

### Good: Complete Sales Engineering Workflow

```python
# sales_engineering/workflow.py
import asyncio
import logging
from typing import Dict, Any

from sales_engineering.engineer import SalesEngineer
from sales_engineering.support import SalesSupport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_sales_engineering():
    """Run sales engineering workflow"""
    logger.info("=" * 60)
    logger.info("Sales Engineering Workflow")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/sales_engineering_config.yaml')
    
    # Create opportunity
    opportunity = create_sample_opportunity()
    
    # Step 1: Support discovery
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Supporting Discovery")
    logger.info("=" * 60)
    
    engineer = SalesEngineer(config)
    discovery_results = await engineer.support_discovery(opportunity)
    
    logger.info("Discovery supported")
    print_discovery_results(discovery_results)
    
    # Step 2: Create demo
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Creating Demo")
    logger.info("=" * 60)
    
    demo = await engineer.create_demo(opportunity)
    
    logger.info(f"Demo created: {demo.demo_id}")
    print_demo_summary(demo)
    
    # Step 3: Build PoC
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Building PoC")
    logger.info("=" * 60)
    
    poc = await engineer.build_poc(opportunity)
    
    logger.info(f"PoC built: {poc.poc_id}")
    print_poc_summary(poc)
    
    # Step 4: Handle objections
    logger.info("\n" + "=" * 60)
    logger.info("Step 4: Handling Objections")
    logger.info("=" * 60)
    
    support = SalesSupport(config)
    objections = [
        "The price is too high",
        "We need feature X",
        "We're concerned about security"
    ]
    
    objection_results = await support.handle_objections(opportunity, objections)
    
    logger.info("Objections handled")
    print_objection_results(objection_results)
    
    # Print summary
    print_summary(opportunity, discovery_results, demo, poc, objection_results)

def create_sample_opportunity() -> Opportunity:
    """Create sample opportunity"""
    return Opportunity(
        opportunity_id="opp_123456",
        account_name="Acme Corporation",
        contact_name="John Smith",
        stage=OpportunityStage.DISCOVERY,
        value=50000.0,
        probability=0.3,
        requirements=[
            "API integration with existing systems",
            "Custom reporting",
            "SSO integration"
        ],
        challenges=[
            "Complex integration requirements",
            "Tight timeline"
        ],
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )

def print_discovery_results(results: Dict[str, Any]):
    """Print discovery results"""
    print(f"\nDiscovery Results:")
    print(f"  Requirements Analysis:")
    for req_type, requirements in results['requirements_analysis'].items():
        print(f"    {req_type}: {len(requirements)} requirements")
    print(f"  Challenges: {len(results['challenges'])}")
    print(f"  Solutions: {len(results['solutions'])}")

def print_demo_summary(demo: Demo):
    """Print demo summary"""
    print(f"\nDemo Summary:")
    print(f"  Title: {demo.title}")
    print(f"  Description: {demo.description}")
    print(f"  Features: {len(demo.features)}")
    print(f"  Use Cases: {len(demo.use_cases)}")
    print(f"  Scheduled: {demo.scheduled_at}")
    print(f"  Duration: {demo.duration_minutes} minutes")

def print_poc_summary(poc: ProofOfConcept):
    """Print PoC summary"""
    print(f"\nPoC Summary:")
    print(f"  Title: {poc.title}")
    print(f"  Description: {poc.description}")
    print(f"  Scope: {len(poc.scope)} items")
    print(f"  Success Criteria: {len(poc.success_criteria)}")
    print(f"  Status: {poc.status.value}")
    print(f"  Start Date: {poc.start_date}")
    print(f"  End Date: {poc.end_date}")

def print_objection_results(results: Dict[str, Any]):
    """Print objection results"""
    print(f"\nObjection Results:")
    print(f"  Objections: {len(results['objections'])}")
    for objection in results['objections']:
        print(f"    - {objection['objection']}: {objection['type']}")
    print(f"  Responses: {len(results['responses'])}")

def print_summary(
    opportunity: Opportunity,
    discovery_results: Dict[str, Any],
    demo: Demo,
    poc: ProofOfConcept,
    objection_results: Dict[str, Any]
):
    """Print summary"""
    print("\n" + "=" * 60)
    print("Sales Engineering Summary")
    print("=" * 60)
    print(f"Opportunity: {opportunity.account_name}")
    print(f"Value: ${opportunity.value:,.0f}")
    print(f"Probability: {opportunity.probability:.0%}")
    print(f"\nActivities:")
    print(f"  Discovery: Completed")
    print(f"  Demo: Created ({demo.demo_id})")
    print(f"  PoC: Built ({poc.poc_id})")
    print(f"  Objections: Handled ({len(objection_results['objections'])})")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await run_sales_engineering()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No discovery
def bad_sales_engineering():
    # No discovery
    pass

# BAD: No demo
def bad_sales_engineering():
    # No demo
    support_discovery()

# BAD: No PoC
def bad_sales_engineering():
    # No PoC
    support_discovery()
    create_demo()

# BAD: No objection handling
def bad_sales_engineering():
    # No objection handling
    support_discovery()
    create_demo()
    build_poc()
```

---

## Standards, Compliance & Security

### Industry Standards
- **Sales Engineering**: Sales engineering best practices
- **Pre-Sales**: Pre-sales best practices
- **Solution Selling**: Solution selling methodology
- **Value Selling**: Value selling methodology

### Security Best Practices
- **Data Protection**: Protect customer data
- **Access Control**: RBIC for demo/PoC environments
- **Audit Logging**: Log all sales engineering activities
- **Confidentiality**: Maintain confidentiality

### Compliance Requirements
- **GDPR**: Data protection compliance
- **Data Privacy**: Protect customer privacy
- **Contract Compliance**: Follow contract requirements
- **Industry Regulations**: Follow industry regulations

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml
```

### 2. Configure Sales Engineering

```bash
# Copy example config
cp config/sales_engineering_config.yaml.example config/sales_engineering_config.yaml

# Edit configuration
vim config/sales_engineering_config.yaml
```

### 3. Run Sales Engineering

```bash
python sales_engineering/workflow.py
```

### 4. View Results

```bash
# View opportunities
cat sales_engineering/results/opportunities.json

# View demos
cat sales_engineering/results/demos/

# View PoCs
cat sales_engineering/results/pocs/
```

---

## Production Checklist

### Discovery
- [ ] Discovery process defined
- [ ] Requirements gathering template created
- [ ] Technical assessment framework defined
- [ ] Solution proposal template created
- [ ] Architecture diagram tool selected

### Demo
- [ ] Demo environment set up
- [ ] Demo data configured
- [ ] Demo script created
- [ ] Demo recording capability enabled
- [ ] Demo scheduling process defined

### PoC
- [ ] PoC process defined
- [ ] PoC scope template created
- [ ] Success criteria defined
- [ ] PoC environment set up
- [ ] PoC documentation template created

### Objection Handling
- [ ] Common objections cataloged
- [ ] Response templates created
- [ ] Evidence repository created
- [ ] Follow-up process defined
- [ ] Training completed

### Pricing
- [ ] Pricing models defined
- [ ] Discount policy defined
- [ ] ROI calculator created
- [ ] Competitive pricing analysis completed
- [ ] Approval process defined

### Contracts
- [ ] Contract templates created
- [ ] Terms defined
- [ ] SLA levels defined
- [ ] Legal review process defined
- [ ] Contract management system configured

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Discovery**
   ```python
   # BAD: No discovery
   pass
   ```

2. **No Demo**
   ```python
   # BAD: No demo
   support_discovery()
   ```

3. **No PoC**
   ```python
   # BAD: No PoC
   support_discovery()
   create_demo()
   ```

4. **No Objection Handling**
   ```python
   # BAD: No objection handling
   support_discovery()
   create_demo()
   build_poc()
   ```

### ✅ Follow These Practices

1. **Support Discovery**
   ```python
   # GOOD: Support discovery
   engineer = SalesEngineer(config)
   results = await engineer.support_discovery(opportunity)
   ```

2. **Create Demo**
   ```python
   # GOOD: Create demo
   demo = await engineer.create_demo(opportunity)
   ```

3. **Build PoC**
   ```python
   # GOOD: Build PoC
   poc = await engineer.build_poc(opportunity)
   ```

4. **Handle Objections**
   ```python
   # GOOD: Handle objections
   support = SalesSupport(config)
   results = await support.handle_objections(opportunity, objections)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 20-40 hours
- **Discovery Framework**: 20-40 hours
- **Demo Creation**: 40-80 hours
- **PoC Building**: 60-120 hours
- **Total**: 140-280 hours

### Operational Costs
- **Demo Environment**: $200-1000/month
- **PoC Environment**: $500-2000/month
- **CRM Tools**: $100-500/month
- **Collaboration Tools**: $50-200/month

### ROI Metrics
- **Win Rate**: 20-40% improvement
- **Deal Size**: 30-50% improvement
- **Sales Cycle**: 30-50% reduction
- **Customer Satisfaction**: 40-60% improvement

### KPI Targets
- **Discovery Completion Rate**: > 90%
- **Demo Success Rate**: > 80%
- **PoC Acceptance Rate**: > 70%
- **Obection Resolution Rate**: > 85%
- **Win Rate**: > 30%

---

## Integration Points / Related Skills

### Upstream Skills
- **136. Business to Technical Spec**: Requirements
- **137. API-First Product Strategy**: API design
- **138. Platform Product Design**: Platform design
- **146. Developer Relations & Community**: Community building
- **147. Technical Content Marketing**: Content marketing

### Parallel Skills
- **149. Enterprise Sales Alignment**: Sales alignment
- **150. Partner Program Design**: Partner programs
- **151. Analyst Relations**: Analyst relations

### Downstream Skills
- **152. Launch Strategy Execution**: Launch strategy

### Cross-Domain Skills
- **18. Project Management**: Project planning
- **81. SaaS FinOps Pricing**: Pricing strategy
- **82. Technical Product Management**: Product management
- **84. Compliance AI Governance**: Compliance

---

## References & Resources

### Documentation
- [Sales Engineering Guide](https://www.gartner.com/)
- [Pre-Sales Best Practices](https://www.forrester.com/)
- [Solution Selling](https://www.millerheiman.com/)
- [Value Selling](https://www.valuebasedselling.net/)

### Best Practices
- [Sales Engineering](https://www.salesengineering.com/)
- [Demo Best Practices](https://www.demo.com/)
- [PoC Best Practices](https://www.poc.com/)

### Tools & Libraries
- [Zoom](https://zoom.us/)
- [Loom](https://www.loom.com/)
- [Salesforce](https://www.salesforce.com/)
- [HubSpot](https://www.hubspot.com/)
- [Slack](https://slack.com/)
