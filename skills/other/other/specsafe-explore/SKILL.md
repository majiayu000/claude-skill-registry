---
name: specsafe-explore
description: Pre-spec exploration. Research and spike before creating formal spec.
disable-model-invocation: true
---

Pre-specification exploration mode - research and spike before creating formal spec.

**When to use:**
- Unclear requirements or scope
- Need to research technical approach
- Want to prototype before committing
- Evaluating feasibility of a feature
- Comparing alternative solutions

**Input**: Feature idea or problem statement

**Steps**

1. **Understand the problem**

   Clarify with user:
   - What problem are we solving?
   - Who are the stakeholders?
   - What are the constraints?
   - What's the expected timeline?

2. **Research existing solutions**

   Explore:
   - Industry best practices
   - Similar features in other products
   - Open source libraries available
   - Design patterns applicable

3. **Spike/prototype (optional)**

   If technical feasibility is uncertain:
   - Create minimal proof-of-concept
   - Test critical assumptions
   - Measure performance characteristics
   - Document findings

   Keep spike code separate:
   ```
   spikes/
   └── <feature-name>-exploration/
       ├── README.md
       └── [prototype files]
   ```

4. **Document findings**

   Create exploration notes:
   ```markdown
   # Exploration: [Feature Name]
   
   ## Problem Statement
   [Clear description of the problem]
   
   ## Research Findings
   - [Finding 1]
   - [Finding 2]
   
   ## Options Considered
   
   ### Option A: [Name]
   - Pros: ...
   - Cons: ...
   - Effort: [Estimate]
   
   ### Option B: [Name]
   - Pros: ...
   - Cons: ...
   - Effort: [Estimate]
   
   ## Recommendation
   [Recommended approach with justification]
   
   ## Open Questions
   - [Question 1]
   - [Question 2]
   
   ## Next Steps
   - [ ] Get stakeholder feedback
   - [ ] Create formal spec
   - [ ] Break down into smaller specs
   ```

5. **Evaluate feasibility**

   Assess:
   - Technical complexity
   - Resource requirements
   - Timeline feasibility
   - Risk factors
   - Dependencies

6. **Recommend path forward**

   Decide:
   - ✅ **Create spec**: Ready to formalize
   - 🔄 **More exploration**: Need additional research
   - ❌ **Not viable**: Too complex or not aligned
   - ✂️ **Split**: Break into multiple smaller specs

7. **Transition to formal spec (if ready)**

   If exploration yields clear requirements:
   ```
   Exploration complete → /specsafe:new <feature-name>
   ```

**Output**

After exploration:
- 📋 Exploration notes documented
- 🔍 Research findings recorded
- 💡 Options compared with pros/cons
- 🎯 Feasibility assessment
- 📊 Effort estimates
- 🚦 Recommendation (proceed/pivot/abandon)

**If proceeding:**
- 📋 Prompt: "Ready to create spec? Run `/specsafe:new <feature-name>`"

**If more exploration needed:**
- 📋 Prompt: "Continue exploration or schedule spike?"

**Guardrails**
- Exploration is time-boxed (suggest 2-4 hours max)
- Document everything for future reference
- Don't over-engineer prototypes (throwaway code OK)
- Be honest about risks and unknowns
- Involve stakeholders before committing to spec
- Exploration ≠ Implementation (no production code)

**Example**
```
User: /specsafe:explore "real-time collaboration"
→ Problem: Users need simultaneous editing
→ Research: Operational Transform vs CRDT
→ Spike: Prototype OT implementation
→ Findings: CRDT better for our use case
→ Options:
→   A: Use Yjs library (3 days)
→   B: Build custom CRDT (2 weeks)
→   C: Use Liveblocks SaaS (1 day + ongoing cost)
→ Recommendation: Option A (Yjs)
→ 
→ 📋 Ready to spec? /specsafe:new real-time-collaboration
```

**vs Formal Spec**

| Exploration | Formal Spec |
|-------------|-------------|
| Unclear requirements | Clear requirements |
| Research needed | Research done |
| May be discarded | Committed to implement |
| Spike code OK | Production code only |
| Time-boxed | Fully estimated |
| Optional artifact | Required artifact |