---
name: agent-swarm-orchestrator
description: Designs multi-agent systems with coordinated agent swarms, task distribution, inter-agent communication, and emergent collective behavior.
license: MIT
---

# Agent Swarm Orchestrator

This skill provides guidance for designing multi-agent systems where multiple AI agents coordinate to accomplish complex tasks through distributed execution and emergent behavior.

## Core Competencies

- **Swarm Architecture**: Agent topologies, communication patterns
- **Task Distribution**: Work allocation, load balancing
- **Coordination Protocols**: Consensus, voting, delegation
- **Emergent Behavior**: Collective intelligence from simple rules

## Multi-Agent Fundamentals

### Why Multi-Agent Systems

```
Single Agent:                    Multi-Agent Swarm:
┌─────────────────┐             ┌─────────────────────────────┐
│                 │             │  ┌───┐ ┌───┐ ┌───┐ ┌───┐   │
│   One Agent     │             │  │ A │ │ A │ │ A │ │ A │   │
│   Sequential    │     vs      │  └───┘ └───┘ └───┘ └───┘   │
│   Single POV    │             │  Parallel, Diverse POV     │
│                 │             │  Specialization possible    │
└─────────────────┘             └─────────────────────────────┘

Benefits:
- Parallelism: Multiple agents work simultaneously
- Specialization: Agents can have different capabilities
- Resilience: System continues if one agent fails
- Diverse perspectives: Multiple approaches to problems
```

### Agent Roles

| Role | Responsibility | Characteristics |
|------|----------------|-----------------|
| Orchestrator | Coordinate swarm | Global view, task assignment |
| Worker | Execute tasks | Specialized skills, focused |
| Supervisor | Quality control | Review, approve, redirect |
| Specialist | Domain expertise | Deep knowledge, narrow scope |
| Scout | Exploration | Information gathering, research |

## Swarm Topologies

### Hierarchical

```
                    ┌──────────────┐
                    │ Orchestrator │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────┴─────┐    ┌─────┴─────┐    ┌─────┴─────┐
    │Supervisor │    │Supervisor │    │Supervisor │
    └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
          │                │                │
    ┌─────┼─────┐    ┌─────┼─────┐    ┌─────┼─────┐
    │     │     │    │     │     │    │     │     │
   ┌┴┐   ┌┴┐   ┌┴┐  ┌┴┐   ┌┴┐   ┌┴┐  ┌┴┐   ┌┴┐   ┌┴┐
   │W│   │W│   │W│  │W│   │W│   │W│  │W│   │W│   │W│
   └─┘   └─┘   └─┘  └─┘   └─┘   └─┘  └─┘   └─┘   └─┘
         Workers

Best for: Clear task decomposition, quality control needed
```

### Peer-to-Peer

```
        ┌───┐───────────────┌───┐
        │ A │               │ A │
        └───┘               └───┘
          │ \             / │
          │   \         /   │
          │     \     /     │
          │       \ /       │
        ┌───┐     ╳       ┌───┐
        │ A │   /   \     │ A │
        └───┘ /       \   └───┘
            /           \
        ┌───┐           ┌───┐
        │ A │───────────│ A │
        └───┘           └───┘

Best for: Collaborative problem-solving, no single point of failure
```

### Blackboard

```
┌─────────────────────────────────────────────────────┐
│                     Blackboard                       │
│  ┌─────────────┐ ┌─────────────┐ ┌───────────────┐ │
│  │ Problem     │ │ Partial     │ │ Solutions     │ │
│  │ State       │ │ Results     │ │               │ │
│  └─────────────┘ └─────────────┘ └───────────────┘ │
└───────────────────────┬─────────────────────────────┘
                        │
    ┌───────────────────┼───────────────────┐
    │         Read/Write│                   │
    ▼                   ▼                   ▼
┌───────┐          ┌───────┐          ┌───────┐
│Agent A│          │Agent B│          │Agent C│
│Analyst│          │Builder│          │Critic │
└───────┘          └───────┘          └───────┘

Best for: Complex problems, agents contribute asynchronously
```

## Agent Implementation

### Base Agent Structure

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, List
from enum import Enum
import asyncio

class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class AgentMessage:
    sender_id: str
    recipient_id: str  # Or "broadcast"
    message_type: str
    content: Any
    timestamp: float = field(default_factory=lambda: time.time())
    correlation_id: Optional[str] = None

@dataclass
class Task:
    id: str
    description: str
    priority: int = 0
    dependencies: List[str] = field(default_factory=list)
    assigned_to: Optional[str] = None
    status: str = "pending"
    result: Any = None


class BaseAgent(ABC):
    """Base class for swarm agents"""

    def __init__(self, agent_id: str, capabilities: List[str]):
        self.id = agent_id
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.current_task: Optional[Task] = None

    @abstractmethod
    async def process_task(self, task: Task) -> Any:
        """Process assigned task - implement in subclass"""
        pass

    @abstractmethod
    def can_handle(self, task: Task) -> bool:
        """Check if agent can handle this task type"""
        pass

    async def receive_message(self, message: AgentMessage):
        """Add message to queue for processing"""
        await self.message_queue.put(message)

    async def run(self):
        """Main agent loop"""
        while True:
            # Check for messages
            try:
                message = await asyncio.wait_for(
                    self.message_queue.get(),
                    timeout=0.1
                )
                await self._handle_message(message)
            except asyncio.TimeoutError:
                pass

            # Work on current task
            if self.current_task and self.status == AgentStatus.WORKING:
                await self._work_on_task()

    async def _handle_message(self, message: AgentMessage):
        """Handle incoming message"""
        if message.message_type == "assign_task":
            self.current_task = message.content
            self.status = AgentStatus.WORKING
        elif message.message_type == "cancel_task":
            self.current_task = None
            self.status = AgentStatus.IDLE
        elif message.message_type == "status_request":
            await self._send_status(message.sender_id)

    async def _work_on_task(self):
        """Execute current task"""
        try:
            result = await self.process_task(self.current_task)
            self.current_task.result = result
            self.current_task.status = "completed"
            self.status = AgentStatus.COMPLETED
        except Exception as e:
            self.current_task.status = "failed"
            self.status = AgentStatus.FAILED
```

### Specialized Agents

```python
class ResearchAgent(BaseAgent):
    """Agent specialized for information gathering"""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, ["research", "search", "analyze"])
        self.search_tools = []

    def can_handle(self, task: Task) -> bool:
        return any(cap in task.description.lower()
                   for cap in ["research", "find", "search", "investigate"])

    async def process_task(self, task: Task) -> dict:
        # Research implementation
        results = await self._search(task.description)
        analysis = await self._analyze(results)
        return {
            "sources": results,
            "analysis": analysis,
            "confidence": self._calculate_confidence(results)
        }


class CodeAgent(BaseAgent):
    """Agent specialized for code generation"""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, ["code", "implement", "debug"])

    def can_handle(self, task: Task) -> bool:
        return any(cap in task.description.lower()
                   for cap in ["implement", "code", "write", "fix", "debug"])

    async def process_task(self, task: Task) -> dict:
        # Code generation implementation
        code = await self._generate_code(task.description)
        tests = await self._generate_tests(code)
        return {
            "code": code,
            "tests": tests,
            "language": self._detect_language(code)
        }


class ReviewAgent(BaseAgent):
    """Agent specialized for quality review"""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, ["review", "critique", "approve"])

    def can_handle(self, task: Task) -> bool:
        return "review" in task.description.lower()

    async def process_task(self, task: Task) -> dict:
        artifact = task.content  # What to review
        issues = await self._find_issues(artifact)
        suggestions = await self._generate_suggestions(issues)
        return {
            "approved": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions
        }
```

## Orchestration Patterns

### Task-Based Orchestration

```python
class SwarmOrchestrator:
    """Coordinate agent swarm for task completion"""

    def __init__(self):
        self.agents: dict[str, BaseAgent] = {}
        self.task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.completed_tasks: dict[str, Task] = {}
        self.message_bus = MessageBus()

    def register_agent(self, agent: BaseAgent):
        """Add agent to swarm"""
        self.agents[agent.id] = agent

    async def submit_task(self, task: Task):
        """Submit task for processing"""
        # Calculate effective priority (lower = higher priority)
        priority = -task.priority  # Negate for min-heap behavior
        await self.task_queue.put((priority, task))

    async def run(self):
        """Main orchestration loop"""
        while True:
            # Get highest priority task
            _, task = await self.task_queue.get()

            # Check dependencies
            if not self._dependencies_met(task):
                # Re-queue with lower priority
                await self.task_queue.put((1, task))
                continue

            # Find suitable agent
            agent = await self._find_available_agent(task)
            if agent:
                await self._assign_task(agent, task)
            else:
                # No agent available, re-queue
                await asyncio.sleep(0.1)
                await self.task_queue.put((0, task))

    def _dependencies_met(self, task: Task) -> bool:
        """Check if all dependencies are completed"""
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False
            if self.completed_tasks[dep_id].status != "completed":
                return False
        return True

    async def _find_available_agent(self, task: Task) -> Optional[BaseAgent]:
        """Find an idle agent that can handle the task"""
        for agent in self.agents.values():
            if agent.status == AgentStatus.IDLE and agent.can_handle(task):
                return agent
        return None

    async def _assign_task(self, agent: BaseAgent, task: Task):
        """Assign task to agent"""
        task.assigned_to = agent.id
        task.status = "assigned"

        message = AgentMessage(
            sender_id="orchestrator",
            recipient_id=agent.id,
            message_type="assign_task",
            content=task
        )
        await agent.receive_message(message)
```

### Workflow Orchestration

```python
from dataclasses import dataclass
from typing import Callable, List

@dataclass
class WorkflowStep:
    name: str
    agent_type: str
    input_transform: Callable[[dict], dict] = lambda x: x
    required_approval: bool = False

class WorkflowOrchestrator:
    """Execute multi-step workflows with agent swarm"""

    def __init__(self, swarm: SwarmOrchestrator):
        self.swarm = swarm
        self.workflows: dict[str, List[WorkflowStep]] = {}

    def register_workflow(self, name: str, steps: List[WorkflowStep]):
        """Register a multi-step workflow"""
        self.workflows[name] = steps

    async def execute_workflow(
        self,
        workflow_name: str,
        initial_input: dict
    ) -> dict:
        """Execute workflow through agent swarm"""
        steps = self.workflows[workflow_name]
        current_data = initial_input
        results = []

        for i, step in enumerate(steps):
            # Transform input for this step
            step_input = step.input_transform(current_data)

            # Create task
            task = Task(
                id=f"{workflow_name}_{i}_{step.name}",
                description=f"Execute {step.name}",
                context=step_input
            )

            # Submit and wait for completion
            await self.swarm.submit_task(task)
            result = await self._wait_for_completion(task.id)

            # Handle approval if required
            if step.required_approval:
                approved = await self._request_approval(step, result)
                if not approved:
                    return {"status": "rejected", "step": step.name}

            results.append(result)
            current_data = {**current_data, **result}

        return {
            "status": "completed",
            "results": results,
            "final_output": current_data
        }
```

## Inter-Agent Communication

### Message Patterns

```python
class MessageBus:
    """Central message routing for swarm communication"""

    def __init__(self):
        self.subscribers: dict[str, List[BaseAgent]] = {}
        self.message_history: List[AgentMessage] = []

    def subscribe(self, topic: str, agent: BaseAgent):
        """Subscribe agent to topic"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(agent)

    async def publish(self, topic: str, message: AgentMessage):
        """Publish message to topic subscribers"""
        self.message_history.append(message)

        for agent in self.subscribers.get(topic, []):
            if agent.id != message.sender_id:  # Don't send to self
                await agent.receive_message(message)

    async def send_direct(self, message: AgentMessage):
        """Send message to specific agent"""
        # Route to recipient
        pass

    async def broadcast(self, message: AgentMessage):
        """Broadcast to all agents"""
        for topic_subscribers in self.subscribers.values():
            for agent in topic_subscribers:
                if agent.id != message.sender_id:
                    await agent.receive_message(message)
```

### Consensus Protocol

```python
class ConsensusProtocol:
    """Achieve consensus among agents"""

    def __init__(self, agents: List[BaseAgent], threshold: float = 0.66):
        self.agents = agents
        self.threshold = threshold

    async def vote(self, proposal: Any) -> dict:
        """Collect votes from agents"""
        votes = {}

        for agent in self.agents:
            message = AgentMessage(
                sender_id="consensus",
                recipient_id=agent.id,
                message_type="vote_request",
                content=proposal
            )
            response = await self._request_vote(agent, message)
            votes[agent.id] = response

        return self._tally_votes(votes)

    def _tally_votes(self, votes: dict) -> dict:
        """Calculate consensus result"""
        approve_count = sum(1 for v in votes.values() if v.get("approve"))
        total = len(votes)

        consensus_reached = (approve_count / total) >= self.threshold

        return {
            "consensus_reached": consensus_reached,
            "approve_count": approve_count,
            "reject_count": total - approve_count,
            "threshold": self.threshold,
            "votes": votes
        }
```

## Emergent Behavior

### Stigmergy Pattern

Indirect coordination through environment modification:

```python
class SharedWorkspace:
    """Shared environment for stigmergic coordination"""

    def __init__(self):
        self.artifacts: dict[str, Any] = {}
        self.pheromones: dict[str, float] = {}  # Strength indicators
        self.decay_rate = 0.1

    def deposit(self, key: str, artifact: Any, strength: float = 1.0):
        """Add artifact to shared space"""
        self.artifacts[key] = artifact
        self.pheromones[key] = strength

    def sense(self, pattern: str) -> List[tuple[str, Any, float]]:
        """Find artifacts matching pattern"""
        matches = []
        for key, artifact in self.artifacts.items():
            if pattern in key:
                strength = self.pheromones.get(key, 0)
                matches.append((key, artifact, strength))
        return sorted(matches, key=lambda x: -x[2])  # Highest strength first

    def decay(self):
        """Reduce pheromone strengths over time"""
        for key in self.pheromones:
            self.pheromones[key] *= (1 - self.decay_rate)
            if self.pheromones[key] < 0.01:
                del self.pheromones[key]
                del self.artifacts[key]

    def reinforce(self, key: str, amount: float = 0.1):
        """Strengthen pheromone trail"""
        if key in self.pheromones:
            self.pheromones[key] = min(1.0, self.pheromones[key] + amount)
```

### Ant Colony Optimization

```python
class AntColonyTaskAllocator:
    """Allocate tasks using ant colony optimization"""

    def __init__(self, agents: List[BaseAgent], tasks: List[Task]):
        self.agents = agents
        self.tasks = tasks
        self.pheromones = {}  # (agent_id, task_id) -> strength
        self.alpha = 1.0  # Pheromone importance
        self.beta = 2.0   # Heuristic importance
        self.evaporation = 0.1

    def _calculate_probability(
        self,
        agent: BaseAgent,
        task: Task
    ) -> float:
        """Calculate probability of assigning task to agent"""
        key = (agent.id, task.id)

        # Pheromone component
        pheromone = self.pheromones.get(key, 0.1)

        # Heuristic: agent capability match
        heuristic = 1.0 if agent.can_handle(task) else 0.1

        return (pheromone ** self.alpha) * (heuristic ** self.beta)

    def allocate(self) -> dict[str, str]:
        """Generate task allocation"""
        allocation = {}
        available_tasks = set(t.id for t in self.tasks)

        for agent in self.agents:
            if not available_tasks:
                break

            # Calculate probabilities for available tasks
            probs = {}
            for task in self.tasks:
                if task.id in available_tasks:
                    probs[task.id] = self._calculate_probability(agent, task)

            # Normalize and select
            total = sum(probs.values())
            if total > 0:
                selected = self._weighted_choice(probs, total)
                allocation[agent.id] = selected
                available_tasks.remove(selected)

        return allocation

    def update_pheromones(self, allocation: dict, quality: dict):
        """Update pheromones based on solution quality"""
        # Evaporation
        for key in self.pheromones:
            self.pheromones[key] *= (1 - self.evaporation)

        # Deposit based on quality
        for agent_id, task_id in allocation.items():
            key = (agent_id, task_id)
            deposit = quality.get(task_id, 0.1)
            self.pheromones[key] = self.pheromones.get(key, 0) + deposit
```

## Best Practices

### Design Guidelines

1. **Keep agents simple**: Complex behavior emerges from simple rules
2. **Define clear interfaces**: Message formats, task structures
3. **Plan for failure**: Agents will fail; system should continue
4. **Monitor collective behavior**: Individual agents may be fine but swarm stuck
5. **Version coordination protocols**: Agents may run different versions

### Anti-Patterns to Avoid

- **God orchestrator**: One agent that does everything
- **Chatty agents**: Too much inter-agent communication
- **Tight coupling**: Agents depending on specific other agents
- **Missing deadlines**: No timeouts on task completion
- **State explosion**: Agents maintaining too much state

## References

- `references/swarm-topologies.md` - Detailed topology patterns
- `references/coordination-protocols.md` - Consensus and voting algorithms
- `references/emergent-patterns.md` - Stigmergy and self-organization
