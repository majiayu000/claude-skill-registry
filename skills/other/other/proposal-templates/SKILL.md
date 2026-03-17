name: proposal-templates
description: Build and manage reusable proposal templates and content libraries. Use when creating, updating, or applying standardized proposal content.
---

# Proposal Templates Skill

This skill provides guidance for building a proposal acceleration system with reusable templates and content libraries.

## Template Structure

### Formal RFP Response Template

Standard sections for government/enterprise RFP responses:

```markdown
# [RFP Title] - Proposal Response

## 1. Cover Letter
- Personalized to agency/client
- Key differentiators highlighted
- Contact information

## 2. Executive Summary
- Understanding of the requirement
- Proposed solution overview
- Key benefits and value proposition
- Why Nebula Logix

## 3. Understanding of Requirements
- Paraphrase of RFP requirements
- Interpretation of scope
- Assumptions and clarifications

## 4. Technical Approach
### 4.1 Architecture Overview
- System architecture diagram
- Technology stack justification
- Integration points

### 4.2 Solution Details
- Feature-by-feature approach
- Technical specifications
- Security considerations

### 4.3 Delivery Methodology
- Development phases
- Agile approach
- Communication plan

## 5. Project Plan
### 5.1 Timeline
- Milestone schedule
- Deliverables per phase
- Dependencies

### 5.2 Risk Management
- Identified risks
- Mitigation strategies

## 6. Team & Roles
- Organization chart
- Key personnel resumes
- Subcontractor information (if applicable)

## 7. Past Performance
- Case study 1
- Case study 2
- Case study 3
- References

## 8. Compliance Matrix
- Requirement → Response section mapping

## 9. Pricing
- Cost breakdown structure
- Rate card
- Payment terms

## 10. Appendices
- Certifications
- Insurance certificates
- Additional documentation
```

## Content Library Structure

Organize reusable content blocks:

```
content-library/
├── capability-blocks/
│   ├── serverless-development.md
│   ├── cloud-migration.md
│   ├── react-frontend.md
│   ├── api-integration.md
│   ├── data-platforms.md
│   └── devsecops.md
├── case-studies/
│   ├── template.md
│   ├── project-alpha.md
│   └── project-beta.md
├── team/
│   ├── bios/
│   │   ├── john-doe.md
│   │   └── jane-smith.md
│   └── resumes/
│       ├── john-doe-resume.pdf
│       └── jane-smith-resume.pdf
├── diagrams/
│   ├── reference-architecture.png
│   ├── delivery-lifecycle.png
│   └── org-chart.png
├── compliance/
│   ├── security-posture.md
│   ├── quality-assurance.md
│   └── accessibility-508.md
└── boilerplate/
    ├── company-overview.md
    ├── insurance-info.md
    └── certifications.md
```

## Capability Block Template

```markdown
# [Capability Name]

## Overview
Brief description of the capability and when it's applicable.

## Our Approach
How Nebula Logix delivers this capability.

## Technologies
- Technology 1
- Technology 2

## Key Benefits
- Benefit 1
- Benefit 2

## Typical Deliverables
- Deliverable 1
- Deliverable 2

## Related Experience
Reference to case studies.
```

## Case Study Template

```markdown
# [Project Name] Case Study

## Client
- Organization name
- Industry/sector
- Size/scale

## Challenge
What problem did the client face?

## Solution
What did Nebula Logix deliver?

### Technologies Used
- Tech 1
- Tech 2

### Approach
How was it delivered?

## Results
- Quantifiable outcome 1
- Quantifiable outcome 2
- Qualitative outcome

## Timeline
Project duration and key milestones.

## Testimonial (if available)
> "Quote from client"
> — Client Name, Title
```

## Pursuit Brief Generator

Quick summary for bid/no-bid decisions:

```typescript
interface PursuitBrief {
  rfpId: string;
  title: string;
  client: string;
  
  // Quick facts
  deadline: Date;
  budget: string;
  duration: string;
  
  // Fit assessment
  primaryCapabilities: string[];    // Our relevant capabilities
  gapAreas: string[];               // Where we may need partners
  competitiveAdvantages: string[];  // Why we'd win
  risks: string[];                  // Key concerns
  
  // Strategy
  winThemes: string[];              // 2-3 key messages
  partnerNeeded: boolean;
  partnerType?: string;             // e.g., "Content strategy firm"
  
  // Resources
  estimatedBidEffort: string;       // e.g., "20-40 hours"
  keyPersonnel: string[];           // Who would work on this
  
  // Decision
  recommendation: 'pursue' | 'no_bid' | 'conditional';
  conditions?: string[];
}

function generatePursuitBrief(rfp: RFPWithEvaluation): PursuitBrief {
  // Auto-populate based on evaluation results
  const brief: PursuitBrief = {
    rfpId: rfp.id,
    title: rfp.title,
    client: extractClient(rfp),
    deadline: new Date(rfp.deadline),
    budget: rfp.budget || 'Not specified',
    duration: extractDuration(rfp),
    
    primaryCapabilities: mapEvaluationToCapabilities(rfp.evaluation),
    gapAreas: identifyGaps(rfp.evaluation),
    competitiveAdvantages: generateAdvantages(rfp),
    risks: identifyRisks(rfp),
    
    winThemes: generateWinThemes(rfp),
    partnerNeeded: rfp.evaluation?.eligibility === 'partner_needed',
    
    estimatedBidEffort: estimateBidEffort(rfp),
    keyPersonnel: suggestPersonnel(rfp),
    
    recommendation: determineRecommendation(rfp.evaluation),
  };
  
  return brief;
}
```

## Compliance Matrix Template

Track requirements vs responses:

```typescript
interface ComplianceItem {
  requirementId: string;
  requirementText: string;
  section: string;          // Section in RFP
  responseSection: string;  // Section in our response
  status: 'met' | 'partial' | 'not_met' | 'not_applicable';
  evidence: string;         // Brief description of how we meet it
  owner: string;            // Who's responsible for this section
  notes?: string;
}

interface ComplianceMatrix {
  rfpId: string;
  items: ComplianceItem[];
  completionPercentage: number;
}
```

## Submission Checklist

```markdown
# Submission Checklist

## Pre-Submission
- [ ] All RFP requirements addressed
- [ ] Compliance matrix complete
- [ ] All sections reviewed by second set of eyes
- [ ] Pricing reviewed and approved

## Formatting
- [ ] Page limits verified
- [ ] Font size/type correct
- [ ] Margins per specification
- [ ] Headers/footers as required
- [ ] Table of contents updated

## Required Documents
- [ ] Cover letter signed
- [ ] All required forms completed
- [ ] Certifications included
- [ ] Insurance certificates current
- [ ] Required signatures obtained

## Submission
- [ ] File format correct (PDF/Word/etc.)
- [ ] File naming convention followed
- [ ] Portal account verified working
- [ ] Upload all files
- [ ] Confirmation received
- [ ] Save submission confirmation

## Post-Submission
- [ ] Archive all proposal files
- [ ] Log in tracking system
- [ ] Calendar follow-up reminders
```

## Integration with App

### Proposal Storage Schema (Convex)

```typescript
// Add to convex/schema.ts
proposals: defineTable({
  rfpId: v.id("rfps"),
  pursuitId: v.id("pursuits"),
  userId: v.string(),
  
  // Content
  sections: v.array(v.object({
    name: v.string(),
    content: v.string(),
    status: v.union(v.literal("draft"), v.literal("review"), v.literal("final")),
    lastModified: v.number(),
    modifiedBy: v.string(),
  })),
  
  // Compliance
  complianceMatrix: v.optional(v.string()), // JSON
  
  // Files
  attachments: v.array(v.object({
    name: v.string(),
    url: v.string(),
    type: v.string(),
  })),
  
  // Status
  status: v.union(
    v.literal("drafting"),
    v.literal("review"),
    v.literal("final"),
    v.literal("submitted")
  ),
  
  // Timestamps
  createdAt: v.number(),
  updatedAt: v.number(),
  submittedAt: v.optional(v.number()),
}).index("by_rfp", ["rfpId"])
  .index("by_pursuit", ["pursuitId"]),
```

### UI Component Sketch

```tsx
function ProposalBuilder({ rfpId }: { rfpId: string }) {
  const proposal = useQuery(api.proposals.getByRfp, { rfpId });
  const updateSection = useMutation(api.proposals.updateSection);
  
  return (
    <div className="proposal-builder">
      <aside className="template-library">
        <h3>Content Library</h3>
        <ContentBlockList onInsert={handleInsert} />
      </aside>
      
      <main className="proposal-editor">
        {proposal?.sections.map(section => (
          <SectionEditor
            key={section.name}
            section={section}
            onSave={(content) => updateSection({ 
              proposalId: proposal._id, 
              sectionName: section.name, 
              content 
            })}
          />
        ))}
      </main>
      
      <aside className="compliance-tracker">
        <h3>Compliance Matrix</h3>
        <ComplianceChecklist proposalId={proposal?._id} />
      </aside>
    </div>
  );
}
```
