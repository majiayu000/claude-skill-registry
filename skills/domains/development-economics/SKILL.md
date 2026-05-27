---
name: development-economics
description: Economics of low-income countries and the structural transformation from agrarian poverty to industrial prosperity. Covers growth models (Solow, endogenous growth, unified growth theory), the role of institutions (inclusive vs. extractive), inequality measurement and dynamics (Gini, Lorenz curve, Kuznets), poverty traps and their mechanisms (nutritional, financial, geographical), foreign aid debates, and the capability approach as an alternative development metric. Use when analyzing why some countries are rich and others poor, evaluating development interventions, or reasoning about the relationships between growth, inequality, institutions, and human well-being.
type: skill
category: economics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/economics/development-economics/SKILL.md
superseded_by: null
---
# Development Economics

Development economics studies why most of the world's people live in poverty and what can be done about it. It is the most consequential branch of economics: the difference between South Korea and North Korea, between Botswana and Zimbabwe, between the lives of people born in Denmark and people born in the Democratic Republic of Congo, is a matter of institutions, policies, geography, and history that development economics attempts to understand and influence.

**Agent affinity:** sen (capability approach, welfare beyond GDP, Nobel 1998), ostrom (institutional analysis, community governance, Nobel 2009), keynes (demand-side development, public investment)

**Concept IDs:** econ-gdp-growth, econ-trade-offs, econ-scarcity-choice, econ-comparative-advantage, econ-market-failures

## The Development Economics Toolbox at a Glance

| # | Topic | Core question | Key framework |
|---|---|---|---|
| 1 | Growth models | What drives long-run economic growth? | Solow, endogenous growth, institutions |
| 2 | Institutions | Why do institutions matter more than geography? | Inclusive vs. extractive, property rights |
| 3 | Inequality | How is inequality measured and what drives it? | Gini, Lorenz curve, Kuznets hypothesis |
| 4 | Poverty traps | Why do some countries stay poor? | Nutritional, financial, geographical traps |
| 5 | Human capital | What role does education and health play? | Returns to schooling, disease burden |
| 6 | Aid and intervention | Does foreign aid work? | Big push, piecemeal, RCTs |
| 7 | The capability approach | Is GDP the right metric for development? | Sen's functionings and capabilities |

## Topic 1 -- Growth Models

**The Solow model.** Robert Solow's (1956) neoclassical growth model explains output as a function of capital, labor, and technology. Capital accumulation is subject to diminishing returns: each additional unit of capital produces less additional output. In the long run, growth per capita comes entirely from technological progress, which the model treats as exogenous. The key prediction is conditional convergence: poor countries should grow faster than rich ones, conditional on similar savings rates, population growth, and technology.

**Does convergence happen?** Unconditionally, no -- there is no general tendency for poor countries to catch up. Conditionally, yes -- among countries with similar institutions and policies (e.g., OECD members, East Asian tigers), convergence is strong. The gap between conditional and unconditional convergence is the central puzzle of development economics.

**Endogenous growth.** Romer (1990) and Lucas (1988) made technology endogenous by modeling R&D investment and human capital accumulation. Ideas are non-rival -- one person's use does not diminish another's -- which creates increasing returns at the aggregate level. Countries that invest in R&D and education can sustain growth without hitting diminishing returns. This explains why the growth slowdown predicted by Solow has not materialized in innovation-intensive economies.

**Unified growth theory.** Galor (2011) bridges the Malthusian stagnation of pre-modern economies and the sustained growth of the modern era. The demographic transition (from high birth rates to low birth rates as income rises) is the critical mechanism: it shifts parental investment from quantity to quality of children, driving human capital accumulation and growth take-off.

**Worked Solow convergence example.** Consider two countries with identical saving rates (20%), depreciation (5%), population growth (2%), and technology growth (1%). Country A starts at $2,000 GDP per capita; Country B starts at $20,000. Both converge to the same steady-state income per effective worker, but Country A grows faster because it is further from the steady state. At a convergence rate of 2% per year (the standard empirical estimate), Country A closes half the gap to its steady state in 35 years. But if Country A has extractive institutions that redirect investment to elite consumption, its effective saving rate is lower, and it converges to a lower steady state -- or does not converge at all. This is why convergence is conditional on institutions: the Solow model's predictions hold only when the structural parameters (saving, depreciation, institutions) are comparable.

**The Lewis model.** Arthur Lewis (1954) modeled the structural transformation from traditional (agricultural) to modern (industrial) economies. The traditional sector has surplus labor at subsistence wages. The modern sector draws workers from the traditional sector at a wage just above subsistence. As long as surplus labor remains, the modern sector can expand without raising wages -- all productivity gains accrue to capitalists, who reinvest them. The "Lewis turning point" occurs when surplus labor is exhausted and wages begin to rise, shifting the economy from labor-surplus to labor-scarce dynamics. China appears to have passed its Lewis turning point around 2010, as evidenced by rapidly rising wages in coastal factories.

**Growth accounting.** Decomposing GDP growth into contributions from capital, labor, and total factor productivity (TFP). For most developing countries, capital accumulation and labor force growth explain the majority of growth during the early phase of industrialization. TFP growth -- reflecting technology adoption, institutional improvement, and resource reallocation -- becomes dominant at higher income levels. East Asia's high TFP growth distinguished it from Latin America, where capital-intensive growth without productivity gains led to stagnation.

## Topic 2 -- Institutions

**Acemoglu, Johnson, and Robinson.** In a series of influential papers (2001, 2002, 2005), they argued that institutions are the fundamental cause of long-run economic development. They distinguished between inclusive institutions (secure property rights, rule of law, competitive markets, constraints on political power) and extractive institutions (insecure property, arbitrary expropriation, restricted markets, concentrated political power).

**The natural experiment.** European colonizers imposed different institutions depending on settler mortality. Where settlers could survive (temperate colonies like the US, Australia, New Zealand), they built inclusive institutions for themselves. Where settlers died in large numbers (tropical colonies), they built extractive institutions to extract resources. These institutional differences persist centuries after independence and explain much of the current income gap.

**North and the transaction cost approach.** Douglass North (Nobel 1993) argued that institutions reduce the transaction costs of economic exchange. Secure property rights make investment possible. Contract enforcement makes trade possible. Constraint on government makes policy stable. Without these, the gains from specialization and trade cannot be realized, no matter how talented or hardworking the population.

**Ostrom's challenge.** Ostrom demonstrated that formal institutions (state property rights, government regulation) are not the only viable governance structures. Community-based institutions with locally crafted rules, monitoring, and graduated sanctions can govern common pool resources effectively. Her work expanded the institutional toolkit beyond the state-vs.-market binary.

## Topic 3 -- Inequality

**Measurement.** The Gini coefficient ranges from 0 (perfect equality) to 1 (one person has everything). The Lorenz curve plots the cumulative share of income against the cumulative share of population. The Gini is twice the area between the Lorenz curve and the 45-degree line of perfect equality.

**Global inequality.** Roughly two-thirds of global inequality is between countries (where you are born matters more than your position within your country). The remaining third is within countries. Between-country inequality has declined since 1990 as China and India grew rapidly. Within-country inequality has increased in most developed countries since the 1980s.

**The Kuznets hypothesis.** Simon Kuznets (1955) proposed that inequality first rises and then falls during economic development -- an inverted-U shape. The logic: early industrialization creates a high-wage urban sector alongside a low-wage rural sector, increasing inequality. As development proceeds, more workers move to the high-wage sector and inequality falls. The empirical evidence for the Kuznets curve is weak, but the framework highlights the structural transformation at the heart of development.

**Piketty's contribution.** Thomas Piketty (2014) documented the long-run evolution of income and wealth inequality across developed countries. His central claim: when the rate of return on capital (r) exceeds the growth rate (g), wealth concentrates because capital income compounds faster than labor income grows. The implication is that high inequality is the default outcome of capitalism absent redistributive institutions. The empirical work is more robust than the theoretical claim, but both have reshaped the inequality debate.

## Topic 4 -- Poverty Traps

**What they are.** A poverty trap is a self-reinforcing mechanism that keeps individuals, households, or countries in poverty. The defining feature is a threshold: below the threshold, forces push you further down; above it, forces push you up. Without a large enough push past the threshold, escape is impossible through incremental improvement alone.

**Nutritional trap.** Workers who cannot afford enough calories cannot work productively enough to earn enough to afford enough calories. Dasgupta and Ray (1986) formalized this: below a critical caloric intake, the relationship between nutrition and productivity creates a trap.

**Financial trap.** The poor cannot save enough to invest, and they lack access to credit because they have no collateral. Without investment, productivity stays low, income stays low, and saving remains impossible. Microfinance (Yunus, Nobel 2006) attempts to break this trap by providing small loans without collateral. The evidence on microfinance is mixed: it helps with consumption smoothing and small enterprise but rarely generates transformative growth.

**Geographical trap.** Sachs (2005) argued that geography imposes poverty traps through disease burden (malaria), low agricultural productivity (poor soils, unreliable rainfall), landlocked status (high transport costs), and resource curses (Dutch disease). Others (Acemoglu and Robinson) counter that geography operates through institutions -- it is not the tropics that are cursed but the institutions that colonizers built there.

**The big push.** Rosenstein-Rodan (1943) and Murphy, Shleifer, and Vishny (1989) argued that coordinated investment across sectors can push an economy past the poverty trap threshold. If all sectors invest simultaneously, each creates demand for the others' products, making all investments profitable. Individually, none would be profitable. The policy implication: large-scale public investment or foreign aid concentrated enough to achieve critical mass.

**Behavioral poverty traps.** Mullainathan and Shafir (2013) added a psychological dimension: scarcity itself imposes a "bandwidth tax" that reduces cognitive capacity for planning, self-control, and forward-looking decisions. The poor are not less capable -- they face heavier cognitive loads because managing scarcity consumes mental resources. This implies that simplifying financial decisions (automatic savings, default enrollment, simplified forms) can have disproportionate effects on the poor, not because the poor are irrational but because scarcity makes complex decisions harder for everyone.

**Worked poverty trap example.** A subsistence farmer earns $500/year. Basic food costs $400. The remaining $100 is not enough to buy fertilizer ($150) that would double crop yields. Without fertilizer, next year's income is again $500. With fertilizer, next year's income would be $1,000 -- more than enough to buy fertilizer the following year and break the cycle. The farmer is trapped below the threshold. A one-time transfer of $150 could permanently lift the farmer out of the trap. This is the logic behind targeted asset transfers: not ongoing welfare but a push past a critical threshold. Evidence from programs in Bangladesh (BRAC) and Ethiopia shows that well-targeted asset transfers can produce permanent income gains.

**Political poverty traps.** Extractive political institutions can create poverty traps at the national level. Elites who control the state have no incentive to invest in public goods (education, infrastructure, rule of law) that would empower citizens to challenge their power. The poverty of the majority sustains the power of the minority. Breaking this trap requires institutional change -- which is precisely what the entrenched elite will resist. The difficulty of institutional reform in the absence of a crisis is a central puzzle of development economics.

## Topic 5 -- Human Capital

**Returns to education.** Mincer's (1974) human capital earnings function estimates that each additional year of schooling increases earnings by 6-13%, varying by country and context. The returns are particularly high for primary education in developing countries, suggesting that basic literacy and numeracy are binding constraints.

**Health and development.** Disease burden reduces productivity, shortens planning horizons (why invest in education if life expectancy is 40?), and absorbs resources that could go to investment. Malaria alone is estimated to reduce GDP growth by 1.3 percentage points per year in affected countries (Gallup and Sachs, 2001). Deworming, bed nets, and vaccination campaigns have some of the highest benefit-cost ratios of any development intervention.

**The quality-quantity trade-off.** As parents have fewer children, they invest more in each child's education and health. This is the demographic transition mechanism that drives the growth take-off in unified growth theory. Policies that reduce fertility (female education, family planning access, old-age security) therefore have growth effects far beyond their direct costs.

**Worked human capital example.** In rural India, the average return to an additional year of primary schooling is approximately 10% in increased earnings. A girl who completes primary school (vs. dropping out at age 8) earns roughly 50% more over her lifetime. She also: has 2.3 fewer children on average, experiences 50% lower infant mortality for her children, and is 30% less likely to be in an abusive relationship. The social return exceeds the private return because of these externalities -- which is why public investment in primary education has benefit-cost ratios of 10:1 or higher in developing countries. Yet 57 million primary-age children remain out of school, disproportionately girls and disproportionately in sub-Saharan Africa and South Asia. The barrier is not the economic case (which is overwhelming) but institutional failure: weak school systems, corruption in teacher hiring, insecurity, and cultural barriers to female education.

**Migration and brain drain.** Skilled emigration from developing countries ("brain drain") has traditionally been viewed as harmful -- the country invests in education and loses the returns when graduates leave. But the evidence is more nuanced. Remittances (money sent home by emigrants) often exceed foreign aid. The prospect of emigration increases the return to education, encouraging more people to invest in schooling than would otherwise (a "brain gain" effect). Diaspora networks facilitate trade, investment, and knowledge transfer. The optimal policy is not to prevent emigration (which restricts freedom) but to create conditions that make staying attractive -- which requires the institutional reforms that development economics recommends on other grounds.

## Topic 6 -- Aid and Intervention

**The Easterly-Sachs debate.** Jeffrey Sachs argues that the extreme poor are trapped and that large, well-targeted foreign aid can push them past the threshold. William Easterly argues that aid has a dismal track record because it ignores local incentives, institutional constraints, and the knowledge problem. Both have evidence on their side; the truth is likely that some types of aid work in some contexts and others do not.

**The RCT revolution.** Banerjee, Duflo, and Kremer (Nobel 2019) transformed development economics by applying randomized controlled trials to evaluate specific interventions: deworming, conditional cash transfers, microcredit, teacher incentives, bed nets. Their approach rejects grand theories in favor of "what works" pragmatism. The evidence shows that cheap, simple interventions (deworming, bed nets, cash transfers) often have large effects, while more ambitious programs (microfinance, job training) have modest effects.

**Cash transfers.** Direct cash transfers to the poor -- conditional (school attendance, health visits) or unconditional -- have emerged as one of the most effective and cost-efficient development tools. GiveDirectly and Brazil's Bolsa Familia demonstrate that the poor generally spend cash wisely and that administrative costs are low relative to in-kind alternatives.

**Industrial policy and structural transformation.** The East Asian miracle (Japan, South Korea, Taiwan, Singapore) involved extensive government intervention: export promotion, targeted credit allocation, technology transfer, and protection of infant industries. These countries violated the Washington Consensus prescription of free markets and minimal government, yet achieved the fastest sustained growth in history. The lesson is not that industrial policy always works (it failed spectacularly in many African and Latin American countries) but that the quality of implementation -- institutional capacity, accountability, feedback loops, and willingness to withdraw support from failures -- matters more than the policy itself.

**The resource curse.** Countries rich in natural resources (oil, minerals) often have slower growth, more corruption, and worse institutions than resource-poor countries. Mechanisms include: Dutch disease (resource exports appreciate the currency, making other exports uncompetitive), rent-seeking (political elites capture resource rents rather than investing them), volatility (commodity price swings destabilize fiscal planning), and institutional weakening (governments funded by resource rents do not need to tax citizens and therefore face less accountability pressure). Botswana and Norway are notable exceptions -- both managed resource wealth through strong institutions and sovereign wealth funds.

**Worked development example.** South Korea in 1960 had a GDP per capita comparable to Ghana's (~$1,000 in 2005 PPP dollars). By 2020, South Korea's GDP per capita exceeded $40,000 while Ghana's was approximately $5,000. What explains the divergence? Capital accumulation (South Korea invested 30-40% of GDP for decades). Human capital (universal education, high literacy). Institutions (land reform, export discipline, bureaucratic quality). Industrial policy (targeted support for steel, shipbuilding, electronics, then exit from declining sectors). Geographic luck (proximity to Japan as a technology source and the US as an export market). No single factor explains it -- development is a system, not a silver bullet.

## Topic 7 -- The Capability Approach

**Sen's framework.** Amartya Sen (Nobel 1998) argued that development should be measured not by income or utility but by the substantive freedoms -- capabilities -- that people have to live lives they value. A person who is well-nourished, educated, healthy, and free to participate in political life is better off than one who is wealthy but oppressed, even if the latter has higher income.

**Functionings and capabilities.** Functionings are beings and doings (being well-nourished, being educated, participating in community life). Capabilities are the real freedoms to achieve these functionings. The distinction matters: two people may achieve the same functioning (both eat enough) but one may have the capability to eat more and chooses not to (fasting) while the other is at the limit of what they can afford. Their situations are different even though the observed outcome is the same.

**Policy implications.** The capability approach shifts focus from GDP growth to the expansion of substantive freedoms. Health, education, political participation, and gender equality become development objectives in their own right, not merely instruments for growth. The Human Development Index (HDI) -- which combines income, life expectancy, and education -- is a partial operationalization of Sen's framework, though Sen himself cautions against reducing capabilities to a single index.

**Poverty as capability deprivation.** Sen redefines poverty not as low income but as the deprivation of basic capabilities. A person who is income-poor but healthy, educated, and socially connected is less poor than one who has slightly more income but is illiterate, chronically ill, and socially excluded. This reframing has practical consequences: it directs policy toward capability-expanding interventions rather than income transfers alone.

**Gender and development.** Sen's concept of "missing women" (1990) estimated that 100 million women were "missing" from the world population due to sex-selective abortion, differential nutrition, and unequal healthcare access. The number has since grown. Female education is the single most powerful development intervention: it reduces fertility, improves child health, increases household income, and strengthens political participation. Countries that neglect female capabilities (health, education, economic participation) forfeit roughly half their development potential.

## Decision Heuristics

When approaching a development economics problem:

1. **Is it about why a country is poor?** Check institutions (Acemoglu-Robinson), geography (Sachs), human capital (education and health), and policy (trade openness, fiscal management). Most cases involve multiple causes.
2. **Is it about a specific intervention?** Look for RCT evidence (Banerjee-Duflo). If no RCT exists, use quasi-experimental methods. Be skeptical of cross-country regressions.
3. **Is it about growth vs. welfare?** GDP growth is necessary but not sufficient. Check whether growth translates into capability expansion (health, education, freedom). Use Sen's framework.
4. **Is it about institutions?** Distinguish inclusive from extractive. Ask whether institutional change is feasible or whether working within existing institutions is more realistic.
5. **Is it about inequality?** Measure both income inequality (Gini) and multidimensional inequality (health, education, gender). Check Piketty's r > g dynamic.
6. **Is it about aid?** Ask what type of aid, in what institutional context, with what evaluation design. Grand generalizations ("aid works" / "aid fails") are unhelpful.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Monocausal explanations | Development failures rarely have a single cause | Consider institutions, geography, policy, and history together |
| Equating GDP growth with development | Growth can leave capabilities unimproved or worsen inequality | Supplement GDP with HDI, capability measures, and distributional analysis |
| Ignoring institutional context when transplanting policies | A policy that works in Sweden may fail in South Sudan | Evaluate institutional capacity before recommending interventions |
| Treating the poor as irrational | The poor make remarkably good decisions given their constraints | Analyze constraints before attributing behavior to irrationality |
| Assuming convergence is automatic | Poor countries do not automatically catch up | Convergence is conditional on institutions, policy, and human capital |
| Silver-bullet thinking | No single intervention (aid, trade, education, institutions) is sufficient | Development requires progress on multiple fronts simultaneously |

## Cross-References

- **sen agent:** Capability approach, welfare measurement, development as freedom. Primary agent for development questions.
- **ostrom agent:** Institutional analysis, community governance, common pool resources in developing countries.
- **keynes agent:** Public investment, demand-side development, the case for the big push.
- **macroeconomics skill:** Growth theory, fiscal policy for development, structural transformation.
- **international-trade skill:** Trade and development, comparative advantage in poor countries, infant industry debate.
- **public-policy skill:** Aid effectiveness, cash transfers, institutional reform.
- **hayek agent:** Knowledge problem in development planning, critique of top-down interventions.
- **behavioral-economics skill:** Scarcity mindset, present bias, and behavioral barriers in developing countries.
- **microeconomics skill:** Market failures in developing-country contexts -- information asymmetry, thin markets, missing institutions.
- **robinson agent:** Market power and monopsony in developing-country labor markets and commodity markets.
- **smith agent:** Comparative advantage and trade as engines of development -- how specialization drives growth.
- **varian agent:** Pedagogical exposition of development concepts, mechanism design for aid distribution.
- **keynes agent:** Demand-side constraints on development, public investment, and the big push argument.
- **macroeconomics skill:** Growth theory fundamentals -- Solow, endogenous growth, convergence dynamics.

## Historical Context

Development economics as a field was born with decolonization. In the 1940s-1960s, newly independent countries faced the question of how to transform from agrarian poverty to industrial prosperity. Early development economists (Rosenstein-Rodan, Lewis, Hirschman, Myrdal, Prebisch) advocated state-led industrialization, import substitution, and the "big push." These ideas influenced policy in India, Latin America, and Africa, with mixed results -- some successes (South Korea, Taiwan) but many failures (import substitution stagnation in Latin America, state failure in Africa).

The Washington Consensus (1980s-1990s) swung the pendulum toward markets: fiscal discipline, trade liberalization, privatization, deregulation, and secure property rights. The structural adjustment programs of the World Bank and IMF imposed these policies as conditions for lending. Results were again mixed -- some countries benefited (Chile, Poland), others suffered (many sub-Saharan African countries where institutional capacity was too weak to implement reforms effectively).

The institutional turn (Acemoglu, North, Ostrom) showed that neither markets nor states work without appropriate institutions. The RCT revolution (Banerjee, Duflo, Kremer) shifted methodology from grand theory to granular evidence about what works. The current field synthesizes all of these insights: institutions matter (Acemoglu), capabilities matter (Sen), evidence matters (Banerjee-Duflo), and context matters (one-size-fits-all prescriptions fail).

The frontier questions include: how to build institutions in fragile states, how to manage the climate-development trade-off (developing countries need energy but carbon-intensive energy accelerates climate change), how to harness digital technology for financial inclusion and service delivery, and how to address the middle-income trap that has stalled many countries' progress.

## Study Path

**Beginner.** Banerjee and Duflo, *Poor Economics* (2011) -- accessible, evidence-based, and humane. Covers nutrition, education, health, microfinance, and governance through the lens of specific interventions and their evaluations. Then Sen, *Development as Freedom* (1999) -- the philosophical foundation.

**Intermediate.** Acemoglu and Robinson, *Why Nations Fail* (2012) -- the institutional argument with historical case studies. Easterly, *The White Man's Burden* (2006) -- the skeptical counterpoint on foreign aid. Collier, *The Bottom Billion* (2007) -- why the poorest countries are stuck and what might work.

**Advanced.** Ray, *Development Economics* (1998) -- the standard graduate textbook. Piketty, *Capital in the Twenty-First Century* (2014) -- inequality dynamics. Galor, *Unified Growth Theory* (2011) -- the mathematical framework bridging Malthusian stagnation and modern growth.

**Graduate.** The primary literature: Acemoglu, Johnson, and Robinson (2001) on colonial institutions. Banerjee, Duflo, and Kremer on RCTs. Solow (1956), Romer (1990), and Lucas (1988) on growth theory. The *Handbook of Development Economics* (Rodrik and Rosenzweig, eds.) for comprehensive coverage.

## References

- Sen, A. (1999). *Development as Freedom*. Oxford University Press.
- Acemoglu, D., & Robinson, J. A. (2012). *Why Nations Fail*. Crown Business.
- Banerjee, A. V., & Duflo, E. (2011). *Poor Economics*. PublicAffairs.
- Sachs, J. D. (2005). *The End of Poverty*. Penguin.
- Easterly, W. (2006). *The White Man's Burden*. Penguin.
- Piketty, T. (2014). *Capital in the Twenty-First Century*. Harvard University Press.
- Galor, O. (2011). *Unified Growth Theory*. Princeton University Press.
- Lewis, W. A. (1954). "Economic Development with Unlimited Supplies of Labour." *Manchester School*, 22(2), 139-191.
- North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.
- Mincer, J. (1974). *Schooling, Experience, and Earnings*. National Bureau of Economic Research.
- Rosenstein-Rodan, P. N. (1943). "Problems of Industrialisation of Eastern and South-Eastern Europe." *Economic Journal*, 53(210/211), 202-211.
- Dasgupta, P., & Ray, D. (1986). "Inequality as a Determinant of Malnutrition and Unemployment: Theory." *Economic Journal*, 96(384), 1011-1034.
- Kuznets, S. (1955). "Economic Growth and Income Inequality." *American Economic Review*, 45(1), 1-28.
- Duflo, E. (2012). "Women Empowerment and Economic Development." *Journal of Economic Literature*, 50(4), 1051-1079.
- Sen, A. (1990). "More Than 100 Million Women Are Missing." *New York Review of Books*, 37(20), 61-66.
