---
name: engineering-ethics
description: Engineering ethics covering safety, professional codes of conduct, public welfare responsibility, whistleblowing, case studies (Challenger, Columbia, Hyatt Regency, Bhopal, Therac-25), and the ethical dimensions of design decisions. Includes the NSPE Code of Ethics, the iron ring tradition, risk communication, informed consent in engineering, and the duty to dissent. Use when analyzing ethical dimensions of engineering decisions, teaching professional responsibility, or reviewing designs for safety and public welfare.
type: skill
category: engineering
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/engineering/engineering-ethics/SKILL.md
superseded_by: null
---
# Engineering Ethics

Engineering is a profession of public trust. Engineers design the bridges people drive across, the buildings people live in, the aircraft people fly in, and the software that controls medical devices. When engineering fails, people die. Engineering ethics is not an abstract philosophical exercise -- it is the operational framework that prevents harm, guides difficult decisions under pressure, and defines the professional identity of the engineer. This skill covers codes of ethics, case studies of ethical failure, the duty to dissent, and the integration of ethical reasoning into the design process.

**Agent affinity:** brunel (design review leadership, integrated accountability), roebling (structural safety, public infrastructure)

**Concept IDs:** engr-codes-of-ethics, engr-safety-risk, engr-environmental-impact, engr-inclusive-design

## The First Canon

The National Society of Professional Engineers (NSPE) Code of Ethics begins:

> "Engineers, in the fulfillment of their professional duties, shall hold paramount the safety, health, and welfare of the public."

This is Canon 1, and it overrides all other professional obligations. When safety conflicts with schedule, budget, or management direction, safety wins. This is not aspirational -- it is the defining obligation of the profession.

## Codes of Ethics

### NSPE Code of Ethics -- Fundamental Canons

1. Hold paramount the safety, health, and welfare of the public.
2. Perform services only in areas of their competence.
3. Issue public statements only in an objective and truthful manner.
4. Act for each employer or client as faithful agents or trustees.
5. Avoid deceptive acts.
6. Conduct themselves honorably, responsibly, ethically, and lawfully.

### The Iron Ring (Canada)

Canadian engineers receive an iron ring upon graduation, worn on the working hand's little finger. It symbolizes the engineer's obligation to live by a high standard of professional conduct. The ring is a physical reminder -- every time you pick up a pen or a tool, you see it.

### Order of the Engineer (United States)

The American equivalent of the iron ring. Engineers take an oath: "I shall not undertake... any work which I believe will be of harm to the welfare or safety of the public."

## Case Study 1 -- Challenger Disaster (1986)

### What happened

Space Shuttle Challenger broke apart 73 seconds after launch on January 28, 1986, killing all seven crew members. The failure was caused by O-ring seal erosion in the right solid rocket booster, exacerbated by cold launch-day temperatures (36 degrees F, well below the O-ring qualification range).

### The ethical dimension

Engineers at Morton Thiokol (the SRB manufacturer) recommended against launch. Roger Boisjoly and Allan McDonald presented data showing O-ring erosion at temperatures below 53 degrees F. NASA managers pushed back, asking Thiokol to reconsider. Under pressure, Thiokol management overrode their engineers and recommended launch.

### The lesson

- **The duty to dissent is real.** Boisjoly and McDonald were right, and they said so. Their professional obligation under Canon 1 was clear.
- **Management override of engineering judgment kills.** When non-engineers overrule engineers on safety-critical technical judgments, the safety system has failed.
- **Data presentation matters.** The Rogers Commission found that the data was presented in a way that obscured the temperature-erosion correlation. Clear technical communication is an ethical obligation.

### Aftermath

Boisjoly became a whistleblower advocate. He spent the rest of his career teaching engineering ethics. He was awarded the Prize for Scientific Freedom and Responsibility by the AAAS in 1988.

## Case Study 2 -- Columbia Disaster (2003)

### What happened

Space Shuttle Columbia disintegrated during re-entry on February 1, 2003, killing all seven crew members. Foam insulation from the external tank struck the left wing's leading edge during launch, creating a breach. During re-entry, superheated gas entered the wing through the breach and caused structural failure.

### The ethical dimension

Engineers at NASA requested imaging of the wing in orbit (satellite or ground-based telescope) to assess damage. Management declined the request, judging the foam strike as a "turnaround issue" rather than a safety-of-flight concern. The Columbia Accident Investigation Board (CAIB) found that NASA's organizational culture had normalized deviations from design specifications -- foam strikes had occurred on previous flights without catastrophic failure, so they were reclassified from "anomaly" to "accepted risk."

### The lesson

- **Normalization of deviance.** When an anomaly occurs and nothing bad happens, there is pressure to accept it as normal. Each acceptance moves the boundary of acceptable risk further from the original design intent. This is organizational, not individual, failure.
- **Request for information is not dissent.** The engineers who requested imaging were not opposing a launch decision -- they were asking for data. The organizational culture treated the data request as an implicit criticism of management's risk assessment.
- **Organizational culture is a safety system.** Technical competence without organizational support for dissent is insufficient.

## Case Study 3 -- Hyatt Regency Walkway Collapse (1981)

### What happened

Two suspended walkways in the Kansas City Hyatt Regency hotel collapsed during a dance, killing 114 people and injuring 216. The original design used a single continuous rod from the ceiling through both walkway levels. During construction, the connection was changed to two separate rods (offset connection), which doubled the load on the upper walkway's connection. The connection failed under the weight of dancers.

### The ethical dimension

The design change was made for constructability (the original continuous rod was difficult to thread through both walkways). The change was communicated by telephone and was not formally reviewed by the engineer of record. The engineer of record's professional engineering license was revoked.

### The lesson

- **Every design change must be analyzed.** A change that seems minor (shorter rods) can fundamentally alter the load path.
- **Verbal approvals are not engineering review.** Changes to safety-critical connections require documented analysis and formal approval.
- **The engineer of record is responsible.** Delegating review does not delegate responsibility.

## Case Study 4 -- Therac-25 (1985-1987)

### What happened

The Therac-25 radiation therapy machine delivered massive radiation overdoses to six patients, killing three, due to software errors combined with the removal of hardware safety interlocks present in earlier models.

### The ethical dimension

The manufacturer (AECL) removed hardware safety interlocks from earlier Therac models, relying entirely on software for safety. When a race condition in the software allowed the high-energy beam to fire without the beam spreader in place, there was no physical failsafe to prevent overdose. The manufacturer initially dismissed reports, attributing incidents to operator error.

### The lesson

- **Software is not inherently safer than hardware.** Replacing hardware interlocks with software requires the software to be held to the same safety standards -- formal verification, independent review, and fault-tolerant design.
- **Defense in depth.** Safety-critical systems must have multiple independent layers of protection. No single failure (hardware or software) should lead to harm.
- **Incident response is an ethical obligation.** Dismissing reports of harm to protect the product's reputation violates Canon 1.

## The Duty to Dissent

### When to speak up

An engineer has an obligation to speak up when:

1. They believe a decision will endanger public safety.
2. They have evidence that a design, process, or operation does not meet safety requirements.
3. They are asked to certify work they believe is inadequate.
4. They observe falsification of test data or analysis.

### How to dissent effectively

1. **Document.** Put your concerns in writing with supporting data.
2. **Use the chain.** Start with your immediate supervisor. If unheard, escalate through management.
3. **Use safety reporting systems.** Many organizations have anonymous safety reporting channels.
4. **Involve professional societies.** NSPE, ASCE, IEEE, and others provide ethics consultation.
5. **Whistleblower protections.** Federal and state laws protect engineers who report safety concerns.

### The cost of dissent

Whistleblowers face real consequences: reassignment, demotion, termination, ostracism. Boisjoly was isolated at Thiokol after Challenger. This is why organizational culture matters -- an organization that punishes dissent will suppress the very signals it needs to prevent disaster.

## Risk Communication

Engineers have an obligation to communicate risk accurately. This means:

- **Quantify when possible.** "There is a 1-in-10,000 probability of failure per mission" is better than "it's very safe."
- **Acknowledge uncertainty.** "Our analysis assumes the following conditions; if those conditions are not met, the risk increases."
- **Use the right audience model.** Risk communication to fellow engineers, to management, and to the public requires different levels of technical detail and different framing.
- **Never understate risk to protect a schedule.** This is the Challenger lesson.

## Factor of Safety as Ethical Decision

The factor of safety (structural-analysis skill) is simultaneously a technical and ethical choice. A low FOS reduces cost but increases risk. A high FOS increases safety but consumes more resources. The engineer who selects the FOS is making a value judgment about the acceptable probability of harm, informed by codes but ultimately an exercise of professional judgment.

## Inclusive Design

Engineering ethics extends beyond preventing catastrophic failure to ensuring that designs serve all users:

- **Accessibility.** Curb cuts, automatic doors, visual and auditory signals in elevators.
- **Universal design.** Products usable by people with the widest range of abilities, without adaptation.
- **Environmental justice.** Infrastructure decisions affect communities unequally. Siting a waste facility in a low-income neighborhood may be economically efficient but ethically problematic.

## Cross-References

- **brunel agent:** Design review leadership where ethical issues surface. CAPCOM responsibility for safety decisions.
- **roebling agent:** Structural safety in public infrastructure. Brooklyn Bridge completion as an example of perseverance under adversity.
- **johnson-k agent:** NASA safety culture, mission risk assessment, and the lessons of Challenger and Columbia.
- **design-process skill:** Ethics integrated into design reviews (SRR, PDR, CDR).
- **systems-engineering skill:** Configuration management and change control as safety mechanisms.
- **structural-analysis skill:** Factor of safety as an ethical decision.
- **technical-communication skill:** Risk communication and the obligation to present data clearly.

## References

- NSPE. (2019). *NSPE Code of Ethics for Engineers*. National Society of Professional Engineers.
- Vaughan, D. (1996). *The Challenger Launch Decision: Risky Technology, Culture, and Deviance at NASA*. University of Chicago Press.
- CAIB. (2003). *Columbia Accident Investigation Board Report*. NASA.
- Leveson, N. G., & Turner, C. S. (1993). "An Investigation of the Therac-25 Accidents." *IEEE Computer*, 26(7), 18-41.
- Petroski, H. (1985). *To Engineer Is Human: The Role of Failure in Successful Design*. St. Martin's Press.
- Harris, C. E., Pritchard, M. S., Rabins, M. J., James, R., & Englehardt, E. (2019). *Engineering Ethics: Concepts and Cases*. 6th edition. Cengage.
- Martin, M. W., & Schinzinger, R. (2010). *Introduction to Engineering Ethics*. 2nd edition. McGraw-Hill.
