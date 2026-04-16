---
name: microeconomics
description: Foundations of individual economic decision-making, market structures, and strategic interaction. Covers supply and demand analysis, price elasticity, consumer and producer surplus, market structures (perfect competition, monopoly, oligopoly, monopolistic competition), game theory (Nash equilibrium, dominant strategies, repeated games), and welfare economics. Use when analyzing individual markets, firm behavior, pricing strategies, consumer choice, or strategic interactions between economic agents.
type: skill
category: economics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/economics/microeconomics/SKILL.md
superseded_by: null
---
# Microeconomics

Microeconomics studies how individual agents -- consumers, firms, and governments -- make decisions under scarcity and how those decisions interact through markets. Where macroeconomics examines aggregate outcomes, microeconomics examines the mechanisms that produce them: why prices move, why firms enter or exit industries, why some markets work well and others fail. This skill covers supply and demand, elasticity, market structures, game theory, and welfare analysis with worked examples and decision heuristics.

**Agent affinity:** smith (market coordination, invisible hand), robinson (imperfect competition, monopsony), varian (pedagogical exposition)

**Concept IDs:** econ-supply-demand, econ-price-mechanism, econ-market-structures, econ-marginal-thinking, econ-opportunity-cost

## The Microeconomics Toolbox at a Glance

| # | Topic | Core question | Key tool |
|---|---|---|---|
| 1 | Supply and demand | How do prices emerge? | Equilibrium analysis |
| 2 | Elasticity | How sensitive are quantities to price changes? | Percentage change ratios |
| 3 | Consumer choice | How do individuals maximize utility? | Budget constraints + indifference curves |
| 4 | Producer theory | How do firms minimize cost and maximize profit? | Production functions + cost curves |
| 5 | Market structures | How does industry structure affect outcomes? | Structure-conduct-performance framework |
| 6 | Game theory | How do strategic agents interact? | Nash equilibrium, dominant strategies |
| 7 | Welfare economics | When are markets efficient? When do they fail? | Surplus analysis, Pareto efficiency |

## Topic 1 -- Supply and Demand

**The fundamental model.** Supply and demand is the workhorse of microeconomics. A demand curve shows the quantity buyers are willing to purchase at each price. A supply curve shows the quantity sellers are willing to offer at each price. The intersection is the equilibrium -- the price at which quantity demanded equals quantity supplied.

**Why it works.** Prices coordinate information. When price is above equilibrium, surplus accumulates and sellers compete the price down. When price is below equilibrium, shortage emerges and buyers bid the price up. No central planner is needed -- Smith's "invisible hand" operates through price adjustment.

**Worked example.** Suppose demand is Q_d = 100 - 2P and supply is Q_s = 3P - 25. Setting Q_d = Q_s: 100 - 2P = 3P - 25, so 125 = 5P, giving P* = 25 and Q* = 50. At any price above 25, quantity supplied exceeds quantity demanded (surplus); at any price below 25, quantity demanded exceeds quantity supplied (shortage).

**Shifts vs. movements.** A change in the good's own price causes movement along a curve. A change in anything else (income, preferences, input costs, technology) shifts the entire curve. Confusing these is the single most common error in introductory economics.

**Applications.** Price ceilings (rent control), price floors (minimum wage), tax incidence, subsidy analysis, import quotas.

**Tax incidence worked example.** A $1 per-unit tax is imposed on sellers. Supply shifts up by $1 (from Q_s = 3P - 25 to Q_s = 3(P-1) - 25 = 3P - 28). New equilibrium: 100 - 2P = 3P - 28, so 128 = 5P, giving P* = 25.60. Consumers pay $25.60 (up $0.60), producers receive $24.60 after tax (down $0.40). The burden is split roughly 60/40 because demand (slope -2) is more inelastic than supply (slope 3) at this equilibrium. The tax raises $1 * 48.80 = $48.80 in revenue, but total surplus falls -- the deadweight loss triangle equals 0.5 * $1 * 1.20 = $0.60.

**Price ceiling worked example.** A rent ceiling of $20 in the market above yields Q_d = 100 - 2(20) = 60 and Q_s = 3(20) - 25 = 35. Shortage: 60 - 35 = 25 units. Twenty-five people who want housing at the controlled price cannot find it. The visible effect is "affordable rent"; the invisible effect is 25 unhoused people, reduced housing quality (landlords underinvest), and black markets.

## Topic 2 -- Elasticity

**Definition.** Price elasticity of demand measures the responsiveness of quantity demanded to a change in price: E_d = (% change in Q_d) / (% change in P). Analogous elasticities exist for supply, income, and cross-price relationships.

**Classification.** |E_d| > 1 is elastic (quantity responds more than proportionally to price). |E_d| < 1 is inelastic (quantity responds less than proportionally). |E_d| = 1 is unit elastic.

**Why it matters.** Elasticity determines who bears a tax. When demand is inelastic relative to supply, consumers bear most of the burden. When supply is inelastic relative to demand, producers bear most. Elasticity also determines whether a price increase raises or lowers total revenue: if demand is elastic, raising price reduces revenue because the quantity drop dominates.

**Determinants of elasticity.** Availability of substitutes (more substitutes = more elastic), time horizon (longer run = more elastic), necessity vs. luxury (necessities are more inelastic), share of budget (larger share = more elastic).

**Worked example.** If a 10% increase in the price of coffee leads to a 20% decrease in quantity demanded, E_d = -20%/10% = -2.0. Demand is elastic. A coffee shop raising prices by 10% would see revenue fall because the 20% drop in quantity more than offsets the higher price per unit.

## Topic 3 -- Consumer Choice

**The framework.** Consumers have preferences (represented by utility functions or indifference curves) and face budget constraints. Optimal choice occurs where the budget line is tangent to the highest achievable indifference curve -- equivalently, where the marginal rate of substitution equals the price ratio.

**Marginal utility.** The additional satisfaction from one more unit of a good. The law of diminishing marginal utility states that each successive unit provides less additional satisfaction, which is why demand curves slope downward.

**Income and substitution effects.** When the price of a good falls, two things happen: the good becomes relatively cheaper (substitution effect, always increases quantity demanded) and the consumer's real purchasing power increases (income effect, direction depends on whether the good is normal or inferior).

**Giffen goods.** The theoretical edge case where the income effect is so strong and negative that it overwhelms the substitution effect, causing quantity demanded to rise when price rises. Empirically rare but theoretically important for understanding the decomposition. Jensen and Miller (2008) found evidence of Giffen behavior for rice in Hunan, China -- extremely poor households that spent most of their budget on rice increased rice consumption when its price rose because the price increase reduced their real income so much that they could no longer afford more expensive foods and substituted toward more rice.

**Revealed preference.** Samuelson's alternative to utility theory: instead of assuming consumers maximize an unobservable utility function, infer preferences from observed choices. If a consumer chooses bundle A when bundle B was affordable, then A is revealed preferred to B. The Weak Axiom of Revealed Preference (WARP) states that if A is revealed preferred to B, then B is never revealed preferred to A. Violations of WARP indicate either irrational behavior or changing preferences -- which is where behavioral economics enters.

**Behavioral departures.** Standard consumer theory assumes rational, consistent preferences. Behavioral economics documents systematic departures: the endowment effect (people value what they own more than what they don't), framing effects (choices depend on how options are described), and present bias (people overweight immediate gratification). These departures matter for policy design -- see the behavioral-economics skill for the full treatment.

## Topic 4 -- Producer Theory

**Production functions.** A firm transforms inputs (labor, capital, materials) into outputs. The production function Q = f(L, K) describes this relationship. Returns to scale describe what happens when all inputs are scaled: increasing (output grows faster), constant (proportional), or decreasing (output grows slower).

**Cost curves.** Total cost = fixed cost + variable cost. Average total cost (ATC) is U-shaped due to spreading fixed costs (declining) competing with diminishing returns (increasing). Marginal cost (MC) intersects ATC at its minimum.

**Profit maximization.** The competitive firm produces where marginal cost equals price (MC = P). The monopolist produces where marginal revenue equals marginal cost (MR = MC) but charges the demand-curve price for that quantity. The gap between price and MC under monopoly is the source of deadweight loss.

**Short run vs. long run.** In the short run, at least one input is fixed (typically capital). In the long run, all inputs are variable. Firms can enter and exit only in the long run, which is why long-run competitive equilibrium drives economic profit to zero.

**Worked producer theory example.** A firm has total cost TC = 100 + 10Q + Q^2. Fixed cost = 100. Variable cost = 10Q + Q^2. Marginal cost: MC = dTC/dQ = 10 + 2Q. Average total cost: ATC = 100/Q + 10 + Q. ATC is minimized where MC = ATC: 10 + 2Q = 100/Q + 10 + Q, so Q = 100/Q, giving Q = 10. At Q = 10, ATC = 10 + 10 + 10 = 30 and MC = 30. If the market price is $40, the firm produces where MC = P: 10 + 2Q = 40, so Q = 15. Profit = (40 - ATC(15)) * 15 = (40 - 100/15 - 10 - 15) * 15 = (40 - 31.67) * 15 = $125. If price falls below $30, the firm makes losses but continues producing in the short run as long as price covers average variable cost.

**Economies of scope.** Beyond economies of scale (cost falls as output of one product rises), economies of scope arise when producing multiple products together is cheaper than producing them separately. A dairy farm producing both milk and cheese exploits scope economies because both use the same raw material and some of the same equipment. Scope economies drive diversification in business strategy and explain why conglomerates can sometimes outperform specialized firms.

**Creative destruction.** Schumpeter argued that the most important form of competition is not price competition within a static market structure but the dynamic process of innovation that creates new products, new processes, and new industries -- destroying old ones in the process. Static deadweight loss from monopoly may be a small price to pay for the dynamic innovation incentives that monopoly profits provide. This tension between static efficiency and dynamic innovation is unresolved in industrial organization.

## Topic 5 -- Market Structures

**The spectrum.** Market structures range from perfect competition to monopoly, with monopolistic competition and oligopoly in between. The key variables are: number of firms, product differentiation, barriers to entry, and price-setting power.

| Structure | Firms | Product | Entry | Price power | Real-world analog |
|---|---|---|---|---|---|
| Perfect competition | Many | Identical | Free | None (price taker) | Agricultural commodities |
| Monopolistic competition | Many | Differentiated | Low | Some | Restaurants, retail |
| Oligopoly | Few | Similar or differentiated | High | Significant | Airlines, auto manufacturers |
| Monopoly | One | Unique | Blocked | Full (price maker) | Local utilities, patents |

**Robinson's contribution.** Joan Robinson's *The Economics of Imperfect Competition* (1933) formalized the analysis of markets between the polar cases. She introduced the concept of monopsony (single buyer with market power over sellers -- the labor-market analog of monopoly) and demonstrated that the marginal revenue product framework applies to input markets as well as output markets.

**Oligopoly models.** Cournot (firms choose quantities simultaneously), Bertrand (firms choose prices simultaneously), Stackelberg (sequential quantity choice with a leader). Each produces different equilibrium predictions. Game theory provides the unifying framework.

## Topic 6 -- Game Theory

**What it is.** Game theory studies strategic interaction -- situations where each agent's optimal action depends on what others do. The fundamental concept is Nash equilibrium: a set of strategies where no player can improve their payoff by unilaterally changing their strategy.

**The Prisoner's Dilemma.** Two suspects face the choice to cooperate (stay silent) or defect (confess). The dominant strategy for each is to defect, leading to an outcome worse for both than mutual cooperation. This is the core model for understanding why individually rational behavior can produce collectively irrational outcomes -- and why institutions, contracts, and norms exist to solve this problem.

| | B cooperates | B defects |
|---|---|---|
| **A cooperates** | (-1, -1) | (-10, 0) |
| **A defects** | (0, -10) | (-5, -5) |

Nash equilibrium: (Defect, Defect) with payoffs (-5, -5), even though (Cooperate, Cooperate) with payoffs (-1, -1) is Pareto superior.

**Repeated games.** When the game is played repeatedly with no known endpoint, cooperation can be sustained through strategies like tit-for-tat. The folk theorem states that any individually rational payoff can be sustained as a Nash equilibrium of the infinitely repeated game, given sufficiently patient players. This provides the theoretical basis for understanding trade relationships, business partnerships, and international agreements.

**Applications.** Auction design, mechanism design (Vickrey, Myerson), bargaining (Nash, Rubinstein), signaling (Spence), screening (Rothschild-Stiglitz).

**Coordination games.** Not all strategic interactions are zero-sum or adversarial. In a coordination game, both players benefit from choosing the same action (e.g., which side of the road to drive on, which technology standard to adopt). Multiple Nash equilibria exist and the outcome depends on expectations, conventions, or focal points (Schelling, 1960). Network effects in technology markets are coordination games at scale -- everyone benefits from being on the same platform, but which platform wins is path-dependent.

**Mixed strategies.** When no pure-strategy Nash equilibrium exists (e.g., matching pennies, penalty kicks in soccer), players randomize. A mixed strategy Nash equilibrium specifies probabilities over actions such that each player is indifferent between their options, given the other player's mix. Empirical evidence from professional sports confirms that players randomize approximately as game theory predicts (Walker and Wooders, 2001; Chiappori, Levitt, and Groseclose, 2002).

**Signaling and screening.** When one party has private information (education, quality, type), strategic communication arises. Spence (1973) showed that education can function as a signal of ability even if it has no direct productive value -- high-ability workers find education less costly and use it to separate themselves from low-ability workers. Rothschild and Stiglitz (1976) showed that uninformed parties (insurers) can design menus of contracts that induce self-selection: high-risk individuals choose full coverage at a high price; low-risk individuals choose partial coverage at a low price. These models are foundational for understanding labor markets, insurance markets, and financial markets.

## Topic 7 -- Welfare Economics

**Pareto efficiency.** An allocation is Pareto efficient if no one can be made better off without making someone else worse off. The First Welfare Theorem states that competitive equilibria are Pareto efficient under standard assumptions (complete markets, no externalities, no public goods, no market power).

**Consumer and producer surplus.** Consumer surplus is the difference between willingness to pay and market price, summed over all buyers. Producer surplus is the difference between market price and willingness to sell, summed over all sellers. Total surplus is maximized at the competitive equilibrium.

**Deadweight loss.** When a market is distorted (by taxes, monopoly, price controls, or externalities), total surplus is reduced. The lost surplus that goes to nobody is deadweight loss. It measures the efficiency cost of the distortion.

**Market failures.** The First Welfare Theorem fails when its assumptions are violated:
- **Externalities:** Costs or benefits not captured in prices (pollution, network effects). Pigouvian taxes or cap-and-trade systems can restore efficiency.
- **Public goods:** Non-rival, non-excludable goods (national defense, clean air). Private markets underprovide because of free riding.
- **Information asymmetry:** When one party knows more than the other (used cars, insurance). Leads to adverse selection and moral hazard.
- **Market power:** When firms can influence price, they restrict output below the efficient level.

**The Second Welfare Theorem.** Any Pareto-efficient allocation can be achieved as a competitive equilibrium with appropriate lump-sum transfers. This separates efficiency from equity: markets can achieve any efficient distribution, but the initial endowment determines which one results. Redistribution through lump-sum transfers is theoretically ideal but practically difficult -- real-world redistribution (taxes, subsidies) introduces distortions.

**Worked welfare example.** A monopolist faces demand P = 100 - Q with constant MC = 20. Monopoly output: MR = 100 - 2Q = 20, so Q_m = 40, P_m = 60. Competitive output: P = MC, so Q_c = 80, P_c = 20. Consumer surplus under monopoly: 0.5 * (100 - 60) * 40 = 800. Under competition: 0.5 * (100 - 20) * 80 = 3,200. Producer surplus under monopoly: (60 - 20) * 40 = 1,600. Under competition: 0. Total surplus under monopoly: 2,400. Under competition: 3,200. Deadweight loss: 800. The monopolist's gain (1,600) does not fully compensate for the consumers' loss (2,400), leaving 800 in surplus that simply vanishes.

**Coase theorem and property rights.** When transaction costs are zero and property rights are well-defined, private bargaining will reach the efficient outcome regardless of the initial assignment of rights (Coase, 1960). The theorem does not say regulation is unnecessary -- it identifies the conditions under which it might be: few parties, low transaction costs, clear property rights. When these conditions fail (as they usually do for pollution, congestion, and other large-number externalities), the theorem explains why government intervention may be needed.

## Decision Heuristics

When approaching a microeconomics problem:

1. **Is it about a single market?** Start with supply and demand. Draw the diagram. Identify equilibrium.
2. **Is it about price sensitivity?** Calculate or estimate elasticity. Determine implications for revenue and tax incidence.
3. **Is it about a firm's decision?** Identify the market structure. Apply the appropriate profit-maximization rule (MC = P for competition, MR = MC for monopoly/oligopoly).
4. **Is it about strategic interaction?** Set up the game. Identify players, strategies, and payoffs. Find Nash equilibria.
5. **Is it about efficiency?** Check the welfare theorems' assumptions. Identify market failures. Evaluate policy interventions by comparing surplus changes.
6. **Is it about a policy?** Trace through the supply-demand effects. Who gains? Who loses? What is the deadweight loss?

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Confusing shifts and movements | A price change moves along the curve; other changes shift it | Ask: "Is this a change in the good's own price?" |
| Ignoring elasticity in policy analysis | Tax incidence depends on relative elasticities, not who writes the check | Always compute or estimate both demand and supply elasticity |
| Assuming competitive behavior in concentrated markets | Oligopolists and monopolists face different incentive structures | Identify market structure before applying models |
| Confusing accounting profit and economic profit | Economic profit includes opportunity cost of owner's resources | Always account for implicit costs |
| Treating efficiency as the only criterion | Pareto efficiency says nothing about equity or distribution | State efficiency and distribution conclusions separately |
| Assuming rationality without checking | Behavioral economics shows systematic departures from rational choice | Consider whether behavioral factors matter for the context |

## Cross-References

- **smith agent:** Market coordination, invisible hand, price mechanism analysis. Primary agent for supply and demand questions.
- **robinson agent:** Imperfect competition, monopsony, market power analysis. Primary agent for market structure questions.
- **varian agent:** Pedagogical exposition, textbook-level explanation. Primary agent for teaching microeconomics concepts.
- **macroeconomics skill:** Aggregate-level counterpart. Micro foundations underpin macro models.
- **behavioral-economics skill:** Challenges rational-agent assumptions with empirical findings on heuristics and biases.
- **public-policy skill:** Policy interventions in markets -- taxes, regulation, externalities.

## Historical Context

Microeconomics has developed through several distinct phases. Adam Smith (1776) provided the intuitive foundation -- the invisible hand, the division of labor, the coordination of self-interested behavior through markets. Alfred Marshall (1890) formalized supply and demand with partial equilibrium analysis. Leon Walras and Vilfredo Pareto developed general equilibrium theory -- the analysis of all markets simultaneously. The marginalist revolution (Jevons, Menger, Walras, 1870s) replaced classical value theory (labor theory of value) with marginal utility theory. The imperfect competition revolution (Robinson, Chamberlin, 1933) filled the gap between the polar cases. Von Neumann and Morgenstern (1944) launched game theory. Arrow and Debreu (1954) proved the existence of general competitive equilibrium and established the welfare theorems. The information economics revolution (Akerlof, Spence, Stiglitz, 2001 Nobel) showed how asymmetric information fundamentally changes market outcomes.

Each phase expanded the toolkit. Modern microeconomics synthesizes all of them and adds behavioral and experimental methods. The field is not a fixed body of doctrine but an evolving analytical framework that grows more powerful as it incorporates new phenomena.

## References

- Varian, H. R. (2014). *Intermediate Microeconomics*. 9th edition. W. W. Norton.
- Robinson, J. (1933). *The Economics of Imperfect Competition*. Macmillan.
- Smith, A. (1776). *An Inquiry into the Nature and Causes of the Wealth of Nations*.
- Mas-Colell, A., Whinston, M. D., & Green, J. R. (1995). *Microeconomic Theory*. Oxford University Press.
- Tirole, J. (1988). *The Theory of Industrial Organization*. MIT Press.
- Osborne, M. J. (2004). *An Introduction to Game Theory*. Oxford University Press.
- Akerlof, G. A. (1970). "The Market for 'Lemons': Quality Uncertainty and the Market Mechanism." *Quarterly Journal of Economics*, 84(3), 488-500.
- Spence, M. (1973). "Job Market Signaling." *Quarterly Journal of Economics*, 87(3), 355-374.
- Coase, R. H. (1960). "The Problem of Social Cost." *Journal of Law and Economics*, 3, 1-44.
- Jensen, R. T., & Miller, N. H. (2008). "Giffen Behavior and Subsistence Consumption." *American Economic Review*, 98(4), 1553-1577.
- Schelling, T. C. (1960). *The Strategy of Conflict*. Harvard University Press.
- Rothschild, M., & Stiglitz, J. E. (1976). "Equilibrium in Competitive Insurance Markets." *Quarterly Journal of Economics*, 90(4), 629-649.
- Marshall, A. (1890). *Principles of Economics*. Macmillan.
- Arrow, K. J., & Debreu, G. (1954). "Existence of an Equilibrium for a Competitive Economy." *Econometrica*, 22(3), 265-290.
