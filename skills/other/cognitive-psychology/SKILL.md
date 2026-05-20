---
name: cognitive-psychology
description: Core cognitive processes underlying human thought and behavior. Covers attention (selective, divided, sustained), memory systems (sensory, working, long-term, encoding, retrieval, forgetting), perception (top-down, bottom-up, Gestalt principles, perceptual constancy), decision-making (heuristics, biases, prospect theory, bounded rationality), language processing (comprehension, production, Broca/Wernicke, bilingualism), and problem-solving (algorithms, heuristics, insight, functional fixedness, mental set). Use when analyzing how people think, attend, remember, perceive, decide, or solve problems.
type: skill
category: psychology
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/psychology/cognitive-psychology/SKILL.md
superseded_by: null
---
# Cognitive Psychology

Cognitive psychology is the scientific study of mental processes -- how people attend to information, encode and retrieve memories, perceive the world, make decisions, understand and produce language, and solve problems. It emerged as a distinct discipline in the 1950s and 1960s when researchers rejected strict behaviorism's refusal to study internal mental states and began modeling the mind as an information-processing system. The "cognitive revolution" drew on information theory (Shannon), linguistics (Chomsky), and early computer science to build testable models of thought.

**Agent affinity:** kahneman (decision-making, heuristics, biases), james (attention, stream of consciousness)

**Concept IDs:** psych-perception-construction, psych-attention-memory, psych-cognitive-biases, psych-brain-structure

## The Cognitive Architecture at a Glance

| # | Domain | Core Questions | Key Figures |
|---|---|---|---|
| 1 | Attention | How do we select what to process? Why do we miss things in plain sight? | Broadbent, Treisman, Posner |
| 2 | Memory | How do we encode, store, and retrieve information? Why do we forget? | Atkinson & Shiffrin, Baddeley, Tulving, Ebbinghaus |
| 3 | Perception | How does the brain construct a stable world from ambiguous sensory data? | Gibson, Gregory, Gestalt school |
| 4 | Decision-making | How do we choose under uncertainty? What systematic errors do we make? | Kahneman & Tversky, Simon, Gigerenzer |
| 5 | Language | How do we understand and produce speech? What is the structure of linguistic knowledge? | Chomsky, Pinker, Broca, Wernicke |
| 6 | Problem-solving | How do we reach goals when the path is not obvious? | Newell & Simon, Duncker, Wertheimer |

## Domain 1 -- Attention

**Core principle:** Attention is the cognitive bottleneck. The world presents far more information than the brain can process, so attention selects what gets through and what is ignored.

### Selective attention

The ability to focus on one source of information while filtering others. Broadbent's (1958) filter model proposed that unattended information is blocked early -- before meaning is extracted. Treisman's (1964) attenuation model modified this: unattended information is turned down, not blocked, so personally relevant stimuli (your name) can break through. The cocktail party effect demonstrates this daily.

**Experiment to know.** Cherry (1953) -- dichotic listening. Participants heard different messages in each ear and repeated one aloud (shadowing). They could report almost nothing about the unattended ear except gross physical changes (gender of speaker). But Moray (1959) showed that the participant's own name in the unattended ear was detected about one-third of the time.

### Divided attention

Performing two tasks simultaneously. Performance depends on task difficulty, practice, and resource overlap. Kahneman's (1973) capacity model treats attention as a limited pool of mental energy allocated flexibly. Tasks that draw on different processing resources (e.g., driving and talking) interfere less than tasks that share resources (e.g., reading and listening to speech).

**Practical implication.** Multitasking is mostly rapid task-switching, not true parallel processing. Each switch incurs a cognitive cost, which is why texting while driving is dangerous even when the driver believes they are managing both tasks.

### Sustained attention (vigilance)

Maintaining focus over extended periods. Vigilance declines within 15-30 minutes on monotonous detection tasks (Mackworth, 1948 -- the clock test). Signal detection theory (Green & Swets, 1966) formalizes this as changes in the criterion (beta) rather than sensitivity (d-prime): people become more conservative about reporting signals rather than losing the ability to detect them.

### Inattentional blindness and change blindness

Simons and Chabris (1999) showed that roughly 50% of observers fail to notice a person in a gorilla suit walking through a basketball-passing scene. Change blindness (Rensink, O'Regan, & Clark, 1997) shows that large changes in visual scenes go undetected when the change occurs during a brief disruption. These findings demonstrate that attention is not merely helpful but *constitutive* of conscious perception.

## Domain 2 -- Memory

**Core principle:** Memory is not a single system but a collection of interacting systems with different capacities, durations, and encoding mechanisms.

### The multi-store model

Atkinson and Shiffrin (1968) proposed three stores:

1. **Sensory memory.** Brief (<1 second for iconic/visual, ~3 seconds for echoic/auditory) high-capacity storage of raw sensory input. Demonstrated by Sperling's (1960) partial report procedure.
2. **Short-term memory (STM).** Limited capacity (~7 plus/minus 2 items, Miller 1956), duration ~15-30 seconds without rehearsal. Maintained by rehearsal.
3. **Long-term memory (LTM).** Essentially unlimited capacity and duration. Requires encoding (elaborative rehearsal is more effective than maintenance rehearsal).

### Working memory

Baddeley and Hitch (1974) replaced the passive STM concept with working memory -- an active workspace with multiple components:

- **Central executive** -- attentional control system that directs processing
- **Phonological loop** -- maintains verbal/acoustic information via subvocal rehearsal
- **Visuospatial sketchpad** -- maintains visual and spatial information
- **Episodic buffer** (added 2000) -- integrates information across subsystems and links to LTM

Working memory capacity predicts academic achievement, reading comprehension, and fluid intelligence more strongly than IQ in many studies (Alloway & Alloway, 2010).

### Long-term memory systems

Tulving (1972) distinguished:

- **Episodic memory** -- personal events ("my 10th birthday party")
- **Semantic memory** -- general knowledge ("Paris is the capital of France")

Squire (1992) broadened the taxonomy:

- **Declarative (explicit)** -- episodic + semantic, requires conscious recall
- **Non-declarative (implicit)** -- procedural skills, priming, classical conditioning, does not require conscious recall

Patient H.M. (Scoville & Milner, 1957) demonstrated the dissociation: after bilateral hippocampal removal, H.M. could not form new declarative memories but could learn new motor skills.

### Forgetting

Ebbinghaus (1885) established the forgetting curve: rapid initial loss followed by a gradual plateau. Theories of forgetting include:

- **Decay** -- trace deteriorates over time (weak evidence for LTM)
- **Interference** -- proactive (old memories block new) and retroactive (new memories block old)
- **Retrieval failure** -- the memory exists but the cue is insufficient (Tulving's encoding specificity principle)
- **Motivated forgetting** -- suppression (conscious) and repression (unconscious, contested)

### Encoding strategies

- **Levels of processing** (Craik & Lockhart, 1972) -- deeper (semantic) processing produces stronger memories than shallow (structural) processing
- **Elaboration** -- connecting new information to existing knowledge
- **Spacing effect** -- distributed practice beats massed practice (Cepeda et al., 2006)
- **Testing effect** -- retrieval practice strengthens memory more than re-study (Roediger & Karpicke, 2006)

## Domain 3 -- Perception

**Core principle:** Perception is construction, not recording. The brain actively interprets incomplete and ambiguous sensory data to build a coherent model of the world.

### Bottom-up vs. top-down processing

Gibson's (1979) ecological approach emphasizes bottom-up processing: the environment provides rich, sufficient information (affordances) and the perceiver picks it up directly. Gregory's (1970) constructivist approach emphasizes top-down processing: perception requires inference, expectation, and prior knowledge to fill in gaps. Both contribute. The Muller-Lyer illusion persists even when you know the lines are equal (bottom-up dominance), but your ability to read degraded handwriting depends on context (top-down dominance).

### Gestalt principles

The Gestalt school (Wertheimer, Koffka, Kohler, 1912-1935) identified organizational principles the brain uses to group sensory elements:

- **Proximity** -- elements close together are grouped
- **Similarity** -- similar elements are grouped
- **Closure** -- incomplete figures are perceived as complete
- **Continuity** -- smooth, continuous patterns are preferred
- **Common fate** -- elements moving together are grouped
- **Figure-ground** -- the visual field is divided into a figure (focus) and a ground (background)

### Perceptual constancy

Despite constant changes in retinal image, we perceive objects as stable:

- **Size constancy** -- a person walking away does not appear to shrink
- **Shape constancy** -- a door opening does not appear to change shape
- **Color constancy** -- a white shirt appears white in sunlight and shadow

These constancies are achievements of the visual system, not properties of the retinal image. They break down under unusual conditions (Ames room, Ponzo illusion).

## Domain 4 -- Decision-Making

**Core principle:** Human decision-making is systematically different from the rational-agent model assumed by classical economics. We use heuristics that are usually efficient but produce predictable errors.

### Dual-process theory

Kahneman (2011) organized decades of research into a two-system framework:

- **System 1** -- fast, automatic, intuitive, effortless, prone to bias. Recognizes faces, reads emotional expressions, completes "2 + 2 = ?" without effort.
- **System 2** -- slow, deliberate, analytical, effortful, lazy. Computes "17 x 24", evaluates logical arguments, resists temptation. System 2 often accepts System 1's output without checking.

### Heuristics and biases

Tversky and Kahneman (1974) identified three major heuristics:

- **Availability** -- judging probability by how easily examples come to mind. We overestimate the frequency of dramatic events (plane crashes) and underestimate common ones (car accidents).
- **Representativeness** -- judging probability by similarity to a prototype. The "Linda problem": people rate "Linda is a bank teller and a feminist" as more probable than "Linda is a bank teller," violating the conjunction rule.
- **Anchoring** -- estimates are biased toward initial values. Spin a wheel, then estimate a quantity -- the random wheel number pulls the estimate.

### Prospect theory

Kahneman and Tversky (1979) showed that people evaluate outcomes relative to a reference point, not absolute wealth:

- **Loss aversion** -- losses loom larger than equivalent gains (~2:1 ratio)
- **Diminishing sensitivity** -- the difference between $100 and $200 feels larger than $1100 and $1200
- **Probability weighting** -- small probabilities are overweighted (lottery tickets), large probabilities are underweighted (insurance for rare events)

Prospect theory won Kahneman the 2002 Nobel Prize in Economics (Tversky had died in 1996).

### Bounded rationality

Simon (1955) argued that organisms do not optimize -- they *satisfice*, choosing the first option that meets a minimum threshold. Gigerenzer and colleagues extended this with the "fast and frugal heuristics" program, showing that simple rules (take-the-best, recognition heuristic) can outperform complex models in uncertain environments.

## Domain 5 -- Language

**Core principle:** Language is a species-specific cognitive capacity with dedicated neural architecture. Understanding language requires integrating phonology, syntax, semantics, and pragmatics in real time.

### Neural basis

- **Broca's area** (left inferior frontal gyrus) -- speech production. Damage produces Broca's aphasia: effortful, telegraphic speech with intact comprehension ("tan, tan").
- **Wernicke's area** (left posterior superior temporal gyrus) -- speech comprehension. Damage produces Wernicke's aphasia: fluent but meaningless speech ("I called my mother on the television and did not understand the door").
- **Arcuate fasciculus** -- fiber tract connecting Broca's and Wernicke's areas. Damage produces conduction aphasia: intact production and comprehension but inability to repeat heard speech.

### Language acquisition

Chomsky (1965) proposed that children possess an innate Language Acquisition Device (LAD) with Universal Grammar -- a set of structural principles common to all human languages. The poverty of the stimulus argument: children produce grammatical sentences they have never heard, implying they are not simply imitating. The critical period hypothesis (Lenneberg, 1967) holds that language acquisition must occur before puberty for native-level competence.

### Bilingualism

Bilingual individuals show executive function advantages (Bialystok, 2001): better inhibitory control, cognitive flexibility, and conflict monitoring. The bilingual advantage is debated (Paap & Greenberg, 2013), but the finding replicates in many (not all) populations.

## Domain 6 -- Problem-Solving

**Core principle:** Problem-solving is goal-directed cognition in situations where the path from the current state to the goal state is not immediately obvious.

### Problem space theory

Newell and Simon (1972) modeled problem-solving as search through a problem space:

- **Initial state** -- where you are now
- **Goal state** -- where you want to be
- **Operators** -- legal moves that transform one state into another
- **Constraints** -- restrictions on which operators can be applied

The problem-solver searches the space using strategies (algorithms, heuristics, means-ends analysis, working backward).

### Barriers to problem-solving

- **Functional fixedness** (Duncker, 1945) -- seeing an object only in its typical function. The candle problem: participants fail to see the box of tacks as a shelf because they see it as a container.
- **Mental set** (Luchins, 1942) -- applying a previously successful strategy even when a simpler one works. The water jar problem: after solving several problems with a complex formula, participants fail to see a trivial solution.
- **Confirmation bias** -- searching for evidence that supports the current hypothesis rather than evidence that would refute it (Wason, 1960 -- the 2-4-6 task).

### Insight

Insight problems are solved by sudden restructuring rather than incremental search. Metcalfe and Wiebe (1987) showed that insight solutions are preceded by a feeling of impasse followed by an "aha!" moment, while algebra problems show steady warmth-of-feeling ratings. Neuroimaging (Jung-Beeman et al., 2004) associates insight with right anterior temporal lobe activation.

## Common Misconceptions

| Misconception | Reality | Key evidence |
|---|---|---|
| "We only use 10% of our brain." | Virtually all brain regions have known functions. Damage to any area produces deficits. | Neuroimaging (PET, fMRI) shows widespread activation. |
| "Multitasking is efficient." | Task-switching incurs cognitive costs. Dual-task performance is almost always worse than single-task. | Pashler (1994) -- psychological refractory period. |
| "Memory works like a video recorder." | Memory is reconstructive. We fill in gaps, blend memories, and are vulnerable to suggestion. | Loftus (1974) -- misinformation effect. |
| "Left brain = logical, right brain = creative." | Both hemispheres contribute to virtually all cognitive functions. Lateralization exists but is far more nuanced. | Split-brain studies (Gazzaniga, 1967) show lateralization for specific tasks, not general modes. |
| "Subliminal messages control behavior." | Subliminal priming effects are small, short-lived, and do not override conscious goals. | Greenwald et al. (1996) meta-analysis. |

## Cross-References

- **kahneman agent:** Decision-making heuristics and biases, System 1/2 framework. Primary agent for decision analysis and behavioral economics.
- **james agent:** Attention as the foundational cognitive process, stream of consciousness, pragmatic approach to mental life.
- **piaget agent:** Cognitive development -- how the cognitive architecture described here develops across the lifespan.
- **developmental-psychology skill:** Lifespan development of cognitive capacities, including Piagetian stages.
- **behavioral-neuroscience skill:** Neural substrates of the cognitive processes described here -- brain regions, neurotransmitters, plasticity.
- **research-methods-psych skill:** Experimental methods used to study cognition, including reaction time paradigms, signal detection theory, and neuroimaging.

## References

- Atkinson, R. C., & Shiffrin, R. M. (1968). Human memory: A proposed system and its control processes. *Psychology of Learning and Motivation*, 2, 89-195.
- Baddeley, A. D., & Hitch, G. (1974). Working memory. *Psychology of Learning and Motivation*, 8, 47-89.
- Broadbent, D. E. (1958). *Perception and Communication*. Pergamon Press.
- Ebbinghaus, H. (1885). *Memory: A Contribution to Experimental Psychology*. (Trans. 1913).
- Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
- Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-291.
- Newell, A., & Simon, H. A. (1972). *Human Problem Solving*. Prentice-Hall.
- Simons, D. J., & Chabris, C. F. (1999). Gorillas in our midst: Sustained inattentional blindness for dynamic events. *Perception*, 28(9), 1059-1074.
- Tulving, E. (1972). Episodic and semantic memory. In E. Tulving & W. Donaldson (Eds.), *Organization of Memory*. Academic Press.
- Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124-1131.
