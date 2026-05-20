---
name: human-computer-interaction
description: Human-computer interaction (HCI) as a discipline -- usability heuristics, interaction paradigms (CLI, GUI, touch, voice, gesture, spatial), accessibility, cognitive load theory, Fitts's law, user research methods, and the evolution of interfaces from punchcards to spatial computing. Use when evaluating interface usability, choosing interaction paradigms, applying accessibility standards, or understanding why some interfaces work and others fail. Broader than design-thinking -- this skill covers the science of how humans and computers communicate.
type: skill
category: technology
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/technology/human-computer-interaction/SKILL.md
superseded_by: null
---
# Human-Computer Interaction

Human-computer interaction (HCI) is the study of how people use computers and how computers can be designed to be useful and usable. It draws on computer science, cognitive psychology, design, and sociology. This skill covers the science behind good interfaces: why some are intuitive and others are hostile, how human cognition constrains interface design, and how interaction paradigms have evolved.

**Agent affinity:** norman (HCI founder, affordances, usability heuristics), resnick (creative learning interfaces, constructionism), borg (accessible and equitable systems)

**Concept IDs:** tech-computer-architecture, tech-software-concepts, tech-design-brief

## Part I -- Interaction Paradigms

### A Brief History

| Era | Paradigm | Input | Users |
|---|---|---|---|
| 1950s-60s | Batch processing | Punch cards, paper tape | Specialists |
| 1960s-70s | Command-line interface (CLI) | Keyboard | Technical professionals |
| 1970s-80s | Graphical user interface (GUI) | Mouse + keyboard | General public (Xerox PARC, Mac, Windows) |
| 2000s | Touch | Fingers on screen | Everyone (iPhone, 2007) |
| 2010s | Voice | Speech | Hands-free contexts (Siri, Alexa) |
| 2020s | Spatial / Mixed reality | Gesture, gaze, voice | Emerging (AR/VR headsets) |
| 2020s | Conversational AI | Natural language text | Emerging (chatbots, LLM interfaces) |

Each new paradigm does not replace the previous ones. CLIs remain essential for system administration. GUIs dominate productivity work. Touch dominates mobile. The right paradigm depends on the context, not the era.

### Choosing an Interaction Paradigm

| Factor | Favors |
|---|---|
| Precision and repeatability | CLI (scriptable, exact) |
| Discoverability and exploration | GUI (visible options) |
| Mobility and casual use | Touch (portable, no peripherals) |
| Hands-busy contexts | Voice (cooking, driving) |
| Spatial tasks (3D modeling, navigation) | Spatial / gesture |
| Complex, open-ended queries | Conversational AI |

## Part II -- Usability Heuristics

### Nielsen's 10 Usability Heuristics (1994)

Jakob Nielsen's heuristics remain the most widely used framework for evaluating interface quality.

1. **Visibility of system status.** The system should always keep users informed about what is going on, through appropriate feedback within reasonable time.

2. **Match between system and the real world.** The system should speak the users' language, with words, phrases, and concepts familiar to the user, rather than system-oriented terms.

3. **User control and freedom.** Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave the unwanted action without having to go through an extended process. Support undo and redo.

4. **Consistency and standards.** Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions.

5. **Error prevention.** Even better than good error messages is a careful design which prevents a problem from occurring in the first place. Eliminate error-prone conditions or check for them and present users with a confirmation option.

6. **Recognition rather than recall.** Minimize the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the interface to another.

7. **Flexibility and efficiency of use.** Accelerators -- unseen by the novice user -- may speed up interaction for the expert. Allow users to tailor frequent actions.

8. **Aesthetic and minimalist design.** Interfaces should not contain information which is irrelevant or rarely needed. Every extra unit of information in an interface competes with the relevant units of information and diminishes their relative visibility.

9. **Help users recognize, diagnose, and recover from errors.** Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution.

10. **Help and documentation.** Even though it is better if the system can be used without documentation, it may be necessary to provide help and documentation. Any such information should be easy to search, focused on the user's task, list concrete steps, and not be too large.

### Applying Heuristics

Heuristic evaluation is a usability inspection method where evaluators examine an interface against these heuristics. Each violation is rated by severity (cosmetic, minor, major, catastrophic). Three to five evaluators typically find 75% of usability problems. The method is fast, cheap, and effective for catching obvious issues before user testing.

## Part III -- Cognitive Foundations

### Cognitive Load Theory

Human working memory can hold approximately 4 +/- 1 chunks of information simultaneously (Cowan, 2001, revising Miller's classic 7 +/- 2). Interface design must respect this limit.

- **Intrinsic load:** Complexity inherent to the task itself. Cannot be reduced by design.
- **Extraneous load:** Complexity added by poor design. Can and should be eliminated.
- **Germane load:** Mental effort devoted to learning. Should be supported.

Good interface design minimizes extraneous load so that the user's limited working memory is available for intrinsic and germane processing.

### Fitts's Law

The time to move to a target is a function of the distance to the target divided by the size of the target:

MT = a + b * log2(D/W + 1)

Where MT is movement time, D is distance, W is target width, and a and b are empirically determined constants.

**Design implications:**
- Make frequently-used targets large.
- Place related controls close together.
- Use screen edges and corners (infinite width targets on a bounded display).
- Avoid tiny click targets, especially on touch devices.

### Hick's Law

The time to make a decision increases logarithmically with the number of choices:

RT = a + b * log2(n)

Where RT is reaction time and n is the number of equally probable choices.

**Design implications:**
- Reduce the number of options presented at once (progressive disclosure).
- Group related options into categories.
- Provide defaults for common cases.

### Recognition vs Recall

Recognition (seeing an option and selecting it) is cognitively easier than recall (generating an answer from memory). This is why dropdown menus are easier than text fields for known-set inputs, why command palettes supplement keyboard shortcuts, and why autocomplete is universally helpful.

## Part IV -- Accessibility

### Why Accessibility Matters

Approximately 15% of the world's population has some form of disability. Accessible design is not a special accommodation -- it is a design discipline that benefits everyone. Curb cuts were designed for wheelchairs but are used by strollers, bicycles, and delivery carts. Captions were designed for deaf users but are used in noisy environments and by language learners.

### WCAG Principles (POUR)

The Web Content Accessibility Guidelines organize requirements around four principles:

| Principle | Meaning | Examples |
|---|---|---|
| **Perceivable** | Users can perceive the content | Alt text for images, captions for video, sufficient contrast |
| **Operable** | Users can interact with the interface | Keyboard navigation, sufficient time, no seizure triggers |
| **Understandable** | Users can understand the content | Clear language, predictable behavior, error guidance |
| **Robust** | Content works with assistive technologies | Semantic HTML, ARIA labels, standards compliance |

### Assistive Technologies

- **Screen readers:** Convert visual content to speech or braille (JAWS, NVDA, VoiceOver).
- **Switch access:** Single-switch or sip-and-puff input for users with severe motor impairments.
- **Eye tracking:** Gaze-based input for users who cannot use hands.
- **Magnification:** Enlarges portions of the screen for low-vision users.

Designing for assistive technology compatibility is not an afterthought. It requires semantic structure (headings, lists, labels) from the start. Retrofitting accessibility is expensive and incomplete.

## Part V -- User Research Methods

| Method | Stage | Data type | Best for |
|---|---|---|---|
| Contextual inquiry | Early (empathy) | Qualitative | Understanding current practices |
| Card sorting | Early (information architecture) | Qualitative + quantitative | Organizing content categories |
| Usability testing | Mid (prototype) | Qualitative + quantitative | Finding interaction problems |
| A/B testing | Late (production) | Quantitative | Optimizing specific metrics |
| Analytics | Ongoing | Quantitative | Understanding real usage patterns |
| Surveys | Any | Quantitative | Measuring satisfaction at scale |
| Diary studies | Longitudinal | Qualitative | Understanding behavior over time |

**The golden rule of user research:** Watch what people do, not what they say they do. Self-reported behavior is unreliable. Observation reveals the truth.

## Cross-References

- **norman agent:** Primary agent for HCI questions. Norman founded the field and applies these principles.
- **resnick agent:** Creative learning interfaces and constructionist environments.
- **borg agent:** Accessible and equitable systems. Borg ensures technology serves all users.
- **design-thinking skill:** The design process that produces interfaces evaluated by HCI methods.
- **digital-systems skill:** The technical substrate on which interfaces are built.

## References

- Norman, D. A. (2013). *The Design of Everyday Things*. Revised edition. Basic Books.
- Nielsen, J. (1994). "10 Usability Heuristics for User Interface Design." Nielsen Norman Group.
- Shneiderman, B., Plaisant, C., Cohen, M., Jacobs, S., & Elmqvist, N. (2016). *Designing the User Interface*. 6th edition. Pearson.
- Krug, S. (2014). *Don't Make Me Think, Revisited*. 3rd edition. New Riders.
- W3C. (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*. World Wide Web Consortium.
- Card, S. K., Moran, T. P., & Newell, A. (1983). *The Psychology of Human-Computer Interaction*. Lawrence Erlbaum.
