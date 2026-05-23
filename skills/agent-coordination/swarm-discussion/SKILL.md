---
name: swarm-discussion
description: |
  Exploratory discussion pattern for unsolved problems.
  Replicate the thinking of Staff+ engineers: "When there's no clear answer, expose blind spots by confronting diverse perspectives."
  True multi-agent discussions where experts directly engage with each other through team-based + messaging architecture.
---

# swarm-discussion

**"Deep-dive into problems as if multiple experts were debating"**

## Staff+ Engineer Thinking Pattern

> "When there's no clear answer, expose blind spots by confronting diverse perspectives."

For unsolved problems or unprecedented challenges, multiple experts participate as a **team**,
engaging in "true discussions" through messaging where they challenge and supplement each other.

## Features

- **Team-based Architecture**: Compose teams using the Teammate API
- **Messaging-based Dialogue**: Experts communicate directly with each other
- **Statement → Rebuttal → Counter-rebuttal**: True discussion, not just parallel statements
- **Dynamic Expert Generation**: Automatically define appropriate experts based on the topic
- **Complete Evidence Preservation**: Save all messages
- **User Participation**: Use AskUserQuestion for direction confirmation

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Discussion Team                                 │
│                  team_name: discussion-{id}                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │ Expert 1   │ │ Expert 2   │ │ Contrarian │ │Cross-Domain│   │
│  │            │◄──────────────►│            │◄─────────────►│   │
│  │  inbox ◄───┼──── messages ──┼──► inbox   │  messages    │   │
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘   │
│        │              │              │              │            │
│        └──────────────┴──────┬───────┴──────────────┘            │
│                              │                                   │
│                    ┌─────────▼─────────┐                         │
│                    │    Moderator      │                         │
│                    │  - Present topics │                         │
│                    │  - Facilitate     │                         │
│                    │  - Convergence    │                         │
│                    └─────────┬─────────┘                         │
│                              │                                   │
│                    ┌─────────▼─────────┐                         │
│                    │    Historian      │                         │
│                    │  - Record         │                         │
│                    │  - Synthesize     │                         │
│                    └───────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

## Role Design

### Fixed Roles

| Role | Responsibility | Characteristic |
|------|----------------|----------------|
| **Moderator** | Facilitate discussion, present topics, determine convergence | Discussion facilitator |
| **Historian** | Record statements, synthesize, generate summaries | Record keeper |
| **Contrarian** | Question assumptions, present counterarguments | Always seeks opposing views |
| **Cross-Domain** | Provide analogies from other fields | Brings alternative perspectives |

### Dynamically Generated Roles (3-4 based on topic)

Analyze the topic and define appropriate experts. Each expert has the following attributes:

```json
{
  "id": "database-expert",
  "name": "Database Expert",
  "expertise": ["RDB", "NoSQL", "Distributed DB"],
  "thinkingStyle": "pragmatic",
  "bias": "Prioritizes practicality and performance",
  "replyTendency": "Shows concrete implementation examples"
}
```

## Discussion Flow

### Phase 1: Initialization

```javascript
// 1. Generate discussion ID
const discussionId = slugify(topic);  // e.g., "microservice-transaction"

// 2. Create team
Teammate({
  operation: "spawnTeam",
  team_name: `discussion-${discussionId}`
})

// 3. Create directory structure
Bash({
  command: `mkdir -p ~/.claude/discussions/${discussionId}/{personas,rounds,artifacts,context}`
})

// 4. Analyze topic and define experts (executed by Orchestrator)
const dynamicExperts = analyzeTopicAndDefineExperts(topic);
// → [{ id, name, expertise, thinkingStyle, bias, replyTendency }, ...]

// 5. Add fixed roles
const fixedRoles = [
  { id: "moderator", name: "Moderator", role: "Discussion facilitator" },
  { id: "historian", name: "Historian", role: "Record keeper" },
  { id: "contrarian", name: "Contrarian", role: "Devil's advocate" },
  { id: "cross-domain", name: "Cross-Domain", role: "Alternative perspective" }
];

const allExperts = [...dynamicExperts, ...fixedRoles];

// 6. Confirm expert composition with user
AskUserQuestion({
  questions: [{
    question: `Start discussion with the following experts?\n${allExperts.map(e => `- ${e.name}`).join('\n')}`,
    header: "Confirm Experts",
    options: [
      { label: "Start (Recommended)", description: "Begin with this composition" },
      { label: "Modify", description: "Add or change experts" }
    ],
    multiSelect: false
  }]
})

// 7. Save manifest.json
Write(`~/.claude/discussions/${discussionId}/manifest.json`, {
  id: discussionId,
  title: topic,
  created: new Date().toISOString(),
  status: "active",
  currentPhase: "initial",
  currentRound: 0,
  team_name: `discussion-${discussionId}`,
  personas: allExperts
})

// 8. Save each expert definition
for (const expert of allExperts) {
  Write(`~/.claude/discussions/${discussionId}/personas/${expert.id}.json`, expert)
}

// 9. Create discussion task
TaskCreate({
  subject: `Discussion: ${topic}`,
  description: `Experts: ${allExperts.map(e => e.name).join(", ")}`,
  activeForm: "Preparing discussion team"
})
```

### Phase 2: Round Execution (Statement → Rebuttal → Convergence)

```javascript
async function executeRound(discussionId, roundNum, roundTopic) {
  const teamName = `discussion-${discussionId}`;
  const experts = loadPersonas(discussionId);

  // 1. Create round task
  TaskCreate({
    subject: `Round ${roundNum}: ${roundTopic}`,
    description: "Experts are discussing",
    activeForm: `Round ${roundNum} in progress`
  })
  TaskUpdate({ taskId: roundTaskId, status: "in_progress" })

  // 2. Array to store all messages
  const allMessages = [];

  // ========== Step 1: Initial Statement Phase ==========
  // Moderator presents the topic
  const moderatorOpening = await Task({
    team_name: teamName,
    name: "moderator",
    subagent_type: "general-purpose",
    prompt: `
You are the Moderator. Please start the discussion on the following topic.

【Topic】
${roundTopic}

【Previous Discussion】
${previousRoundsSummary || "(New discussion)"}

【Task】
1. Clearly present the topic
2. Suggest 2-3 discussion angles
3. Include questions for each expert
    `
  });

  allMessages.push({
    from: "moderator",
    type: "opening",
    content: moderatorOpening,
    timestamp: new Date().toISOString()
  });

  // Send Moderator's opening message to all experts
  for (const expert of experts.filter(e => e.id !== "moderator" && e.id !== "historian")) {
    Teammate({
      operation: "write",
      target_agent_id: expert.id,
      value: JSON.stringify({
        type: "round_start",
        topic: roundTopic,
        moderator_opening: moderatorOpening
      })
    })
  }

  // Dynamic experts make initial statements (parallel)
  const initialStatements = [];
  for (const expert of experts.filter(e => !["moderator", "historian", "contrarian", "cross-domain"].includes(e.id))) {
    Task({
      team_name: teamName,
      name: expert.id,
      subagent_type: "general-purpose",
      prompt: buildExpertPrompt(expert, {
        phase: "initial",
        topic: roundTopic,
        moderatorOpening: moderatorOpening,
        instruction: "Share your perspective on this topic from your area of expertise."
      }),
      run_in_background: true
    })
  }

  // Collect statements
  for (const expert of dynamicExperts) {
    const statement = await collectStatement(expert.id);
    initialStatements.push({
      from: expert.id,
      type: "initial_statement",
      content: statement,
      timestamp: new Date().toISOString()
    });
    allMessages.push(initialStatements[initialStatements.length - 1]);

    // Share statement with other experts
    broadcastMessage(teamName, expert.id, statement, experts);
  }

  // ========== Step 2: Rebuttal Phase ==========
  // Contrarian provides counterarguments
  const contrarianResponse = await Task({
    team_name: teamName,
    name: "contrarian",
    subagent_type: "general-purpose",
    prompt: `
You are the Contrarian.

【Topic】
${roundTopic}

【Previous Statements】
${formatStatements(initialStatements)}

【Task】
1. Question the assumptions of each statement
2. Point out overlooked risks or exceptions
3. Challenge from a "Is that really true?" perspective
4. Raise constructive questions
    `
  });

  allMessages.push({
    from: "contrarian",
    type: "counterpoint",
    content: contrarianResponse,
    timestamp: new Date().toISOString()
  });

  // Share Contrarian's rebuttal with everyone
  broadcastMessage(teamName, "contrarian", contrarianResponse, experts);

  // ========== Step 3: Counter-Rebuttal Phase ==========
  // Dynamic experts respond to Contrarian (parallel)
  for (const expert of dynamicExperts) {
    Task({
      team_name: teamName,
      name: expert.id,
      subagent_type: "general-purpose",
      prompt: buildExpertPrompt(expert, {
        phase: "rebuttal",
        topic: roundTopic,
        previousStatements: initialStatements,
        contrarianResponse: contrarianResponse,
        instruction: "Respond to Contrarian's rebuttal - either counter or accept. Make your position clear."
      }),
      run_in_background: true
    })
  }

  // Collect rebuttals
  const rebuttals = [];
  for (const expert of dynamicExperts) {
    const rebuttal = await collectStatement(expert.id);
    rebuttals.push({
      from: expert.id,
      type: "rebuttal",
      content: rebuttal,
      timestamp: new Date().toISOString()
    });
    allMessages.push(rebuttals[rebuttals.length - 1]);
  }

  // ========== Step 4: Cross-Domain Perspective ==========
  const crossDomainResponse = await Task({
    team_name: teamName,
    name: "cross-domain",
    subagent_type: "general-purpose",
    prompt: `
You are the Cross-Domain Thinker.

【Topic】
${roundTopic}

【Discussion So Far】
${formatStatements(allMessages)}

【Task】
1. Draw analogies from other fields (biology, economics, physics, etc.)
2. Show how similar problems have been solved in other domains
3. Propose new frameworks or perspectives
    `
  });

  allMessages.push({
    from: "cross-domain",
    type: "analogy",
    content: crossDomainResponse,
    timestamp: new Date().toISOString()
  });

  // ========== Step 5: Convergence ==========
  // Moderator synthesizes the discussion
  const synthesis = await Task({
    team_name: teamName,
    name: "moderator",
    subagent_type: "general-purpose",
    prompt: `
Synthesize this round's discussion.

【All Statements】
${formatStatements(allMessages)}

【Output Format】
{
  "summary": "Summary of this round (about 200 characters)",
  "agreements": ["Agreement 1", "Agreement 2"],
  "disagreements": ["Disagreement 1", "Disagreement 2"],
  "insights": ["Discovered insight 1", "Insight 2"],
  "openQuestions": ["Unresolved question 1", "Question 2"],
  "nextTopicSuggestions": ["Next topic candidate 1", "Candidate 2"]
}
    `
  });

  // ========== Step 6: Record ==========
  // Historian creates complete record
  const roundRecord = {
    roundId: roundNum,
    topic: roundTopic,
    timestamp: new Date().toISOString(),
    messages: allMessages,  // Save all messages
    synthesis: JSON.parse(synthesis),
    metadata: {
      messageCount: allMessages.length,
      participants: [...new Set(allMessages.map(m => m.from))]
    }
  };

  Write(`~/.claude/discussions/${discussionId}/rounds/${String(roundNum).padStart(3, '0')}.json`, roundRecord)

  // Complete task
  TaskUpdate({ taskId: roundTaskId, status: "completed" })

  // ========== Step 7: Confirm Next Action ==========
  AskUserQuestion({
    questions: [{
      question: "What would you like to do next?",
      header: "Progress",
      options: [
        { label: "Deep dive", description: synthesis.nextTopicSuggestions[0] || "Most important topic" },
        { label: "Different topic", description: "Select another topic" },
        { label: "Another round", description: "Continue on same topic" },
        { label: "Synthesis phase", description: "Summarize the discussion" },
        { label: "Pause", description: "Resume later" }
      ],
      multiSelect: false
    }]
  })

  return roundRecord;
}

// Helper function: Broadcast message
function broadcastMessage(teamName, fromId, message, experts) {
  for (const expert of experts) {
    if (expert.id !== fromId && expert.id !== "historian") {
      Teammate({
        operation: "write",
        target_agent_id: expert.id,
        value: JSON.stringify({
          type: "message",
          from: fromId,
          content: message
        })
      })
    }
  }
}
```

### Phase 3: Synthesis

```javascript
async function synthesizeDiscussion(discussionId) {
  const teamName = `discussion-${discussionId}`;
  const allRounds = loadAllRounds(discussionId);

  // Historian synthesizes everything
  const finalSynthesis = await Task({
    team_name: teamName,
    name: "historian",
    subagent_type: "general-purpose",
    prompt: `
You are the Historian. Synthesize the entire discussion.

【All Round Records】
${JSON.stringify(allRounds, null, 2)}

【Output Format】
{
  "executiveSummary": "Summary of the entire discussion (about 500 characters)",
  "insights": [
    {
      "title": "Insight title",
      "description": "Detailed description",
      "confidence": "high/medium/low",
      "supportingEvidence": ["Supporting statements"],
      "dissentingViews": ["Dissenting views if any"]
    }
  ],
  "agreements": [
    { "point": "Agreement point", "supporters": ["Supporters"] }
  ],
  "unresolvedDebates": [
    {
      "topic": "Point of contention",
      "positions": [
        { "stance": "Position A", "advocates": ["Advocates"], "arguments": ["Arguments"] },
        { "stance": "Position B", "advocates": ["Advocates"], "arguments": ["Arguments"] }
      ]
    }
  ],
  "openQuestions": ["Unresolved questions"],
  "recommendations": ["Recommended actions"]
}
    `
  });

  // Save artifacts
  const synthesis = JSON.parse(finalSynthesis);

  Write(`~/.claude/discussions/${discussionId}/artifacts/synthesis.json`, synthesis)
  Write(`~/.claude/discussions/${discussionId}/artifacts/synthesis.md`, formatSynthesisAsMarkdown(synthesis))
  Write(`~/.claude/discussions/${discussionId}/artifacts/open-questions.md`, formatOpenQuestions(synthesis))

  return synthesis;
}
```

### Phase 4: Checkpoint / Termination

```javascript
async function checkpointDiscussion(discussionId) {
  const teamName = `discussion-${discussionId}`;

  // 1. Generate resume context
  const resumeContext = await Task({
    team_name: teamName,
    name: "historian",
    subagent_type: "general-purpose",
    prompt: `
Generate the minimum context needed to resume this discussion later.

Items to include:
1. Discussion theme and purpose (1 paragraph)
2. Key progress so far (bullet points)
3. Current topics and state
4. Summary of participants' main positions
5. Issues to address next time

Length: 1000-2000 characters
Format: Markdown
    `
  });

  Write(`~/.claude/discussions/${discussionId}/context/summary.md`, resumeContext)

  // 2. Update manifest
  updateManifest(discussionId, {
    lastActive: new Date().toISOString(),
    status: "paused",
    currentPhase: "checkpoint"
  })

  // 3. Shutdown all workers
  const experts = loadPersonas(discussionId);
  for (const expert of experts) {
    Teammate({
      operation: "requestShutdown",
      target_agent_id: expert.id
    })
  }

  // 4. Cleanup
  Teammate({ operation: "cleanup" })
}

async function resumeDiscussion(discussionId) {
  // 1. Load manifest
  const manifest = Read(`~/.claude/discussions/${discussionId}/manifest.json`)

  // 2. Recreate team
  Teammate({
    operation: "spawnTeam",
    team_name: manifest.team_name
  })

  // 3. Load resume context
  const context = Read(`~/.claude/discussions/${discussionId}/context/summary.md`)

  // 4. Update manifest
  updateManifest(discussionId, {
    lastActive: new Date().toISOString(),
    status: "active"
  })

  // 5. Notify Moderator of resumption
  const reopening = await Task({
    team_name: manifest.team_name,
    name: "moderator",
    subagent_type: "general-purpose",
    prompt: `
Resuming the discussion.

【Previous Context】
${context}

【Participants】
${manifest.personas.map(p => `- ${p.name}`).join('\n')}

Review the previous state and suggest next steps.
    `
  })

  return reopening;
}
```

## Data Structure

```
~/.claude/discussions/{discussion-id}/
├── manifest.json           # Metadata
├── personas/               # Expert definitions
│   ├── expert-1.json
│   ├── contrarian.json
│   └── ...
├── rounds/                 # Complete record of each round
│   ├── 001.json            # Contains all messages
│   ├── 002.json
│   └── ...
├── artifacts/              # Outputs
│   ├── synthesis.json      # Structured synthesis
│   ├── synthesis.md        # Markdown format
│   └── open-questions.md   # Unresolved questions
└── context/
    └── summary.md          # Resume context
```

### Round JSON Structure (Message-based)

```json
{
  "roundId": 2,
  "topic": "Microservice Transaction Management",
  "timestamp": "2026-01-29T10:30:00Z",
  "messages": [
    {
      "from": "moderator",
      "type": "opening",
      "content": "In this round...",
      "timestamp": "2026-01-29T10:30:00Z"
    },
    {
      "from": "database-expert",
      "type": "initial_statement",
      "content": {
        "position": "I recommend the Saga pattern",
        "reasoning": "Distributed transactions are...",
        "proposals": ["Choreography-based Saga", "Orchestration-based Saga"],
        "codeExample": "..."
      },
      "timestamp": "2026-01-29T10:31:00Z"
    },
    {
      "from": "contrarian",
      "type": "counterpoint",
      "content": "The Saga pattern has the problem of compensating transaction complexity...",
      "timestamp": "2026-01-29T10:33:00Z"
    },
    {
      "from": "database-expert",
      "type": "rebuttal",
      "content": "True it's complex, but with proper design...",
      "timestamp": "2026-01-29T10:35:00Z"
    },
    {
      "from": "cross-domain",
      "type": "analogy",
      "content": "This is similar to settlement systems in finance...",
      "timestamp": "2026-01-29T10:37:00Z"
    }
  ],
  "synthesis": {
    "summary": "General agreement on adopting Saga pattern, but compensating transaction design remains a challenge",
    "agreements": ["Distributed transactions should be avoided"],
    "disagreements": ["Choreography vs Orchestration"],
    "insights": ["Financial settlement patterns are a useful reference"],
    "openQuestions": ["Is automatic generation of compensating transactions possible?"]
  }
}
```

## Prompt Templates

### Dynamic Expert Prompt

```javascript
function buildExpertPrompt(expert, options) {
  return `
You are participating in the discussion as "${expert.name}".

【Your Profile】
- Areas of expertise: ${expert.expertise.join(", ")}
- Thinking style: ${expert.thinkingStyle}
- Natural bias: ${expert.bias}
- Response tendency: ${expert.replyTendency}

【Current Phase】
${options.phase}

【Topic】
${options.topic}

【Previous Statements】
${options.previousStatements ? formatStatements(options.previousStatements) : "(First statement)"}

${options.contrarianResponse ? `
【Contrarian's Rebuttal】
${options.contrarianResponse}
` : ""}

【Task】
${options.instruction}

【Output Format】
{
  "position": "Your stance on this topic (1-2 sentences)",
  "reasoning": "Detailed analysis",
  "proposals": ["Concrete proposals"],
  "counterpoints": ["Rebuttals or supplements to others"],
  "questions": ["Additional questions to consider"],
  "codeOrDiagrams": "Code examples or diagrams (optional)"
}
  `;
}
```

## Important Notes

### Cost Awareness
- Team-based approach has **higher overhead** than direct launch
- 5-10 Task/Teammate calls per round
- Use only when deep discussion is needed

### Leveraging Messaging
- Use `Teammate({ operation: "write" })` to share statements
- Experts can respond based on received messages
- Enables **true dialogue**

### Importance of Cleanup
- Always `requestShutdown` → `cleanup` when discussion ends
- Leaving teams running wastes resources

### Importance of Evidence
- Save **all statements chronologically** in the `messages` array
- Enables complete reconstruction of discussion flow later

## Usage Example

```
User: /swarm-discussion "Microservice Transaction Management"

System:
1. Create team: discussion-microservice-transaction
2. Define experts:
   - Distributed Systems Designer
   - Database Expert
   - Operations Engineer
   - Contrarian (fixed)
   - Cross-Domain (fixed)
3. Confirm with user → "Start"
4. Round 1:
   - Moderator: Present topic
   - Experts: Initial statements (parallel)
   - Contrarian: Rebuttal
   - Experts: Counter-rebuttals
   - Cross-Domain: Alternative perspective
   - Moderator: Convergence/synthesis
5. Confirm next action with user
6. Round 2, 3, ...
7. Synthesis phase → artifacts/synthesis.md
8. Checkpoint → cleanup
```
