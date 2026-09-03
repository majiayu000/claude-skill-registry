---
name: quant-validation
description: 'The methods a financial-ML result has to survive before it is evidence — purged cross-validation with an embargo, triple-barrier labelling, sample uniqueness under overlapping labels, fractional differentiation, meta-labelling, and multiple-testing correction. Written because the invariants were required of quant-researcher and nothing in the project explained how to satisfy them: a rule without a method produces either an invention or a block. Applied whenever a backtest, a feature or a label is being designed or judged.'
when_to_use: |
  Apply when work touches the validity of a financial model, not its returns:
  - quant-researcher designs or judges a backtest, a feature set, or a labelling scheme
  - anyone reports a Sharpe ratio, a hit rate, or an out-of-sample figure
  - a cross-validation scheme is being chosen for a time series with overlapping labels
  Do NOT apply to execution, order routing or market microstructure — that is a
  different body of knowledge and this pack does not cover it.
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/research/**"
  - "docs/architecture/**"
---

# Validating a financial model — the five ways the number lies

A backtest that looks excellent and loses money live is not usually a bad
strategy. It is a good measurement of the wrong thing. Each section below is one
mechanism by which a number becomes convincing without becoming true.

**On sourcing.** The methods here are standard and attributable — most of them to
Marcos López de Prado's *Advances in Financial Machine Learning*, with the
information-ratio framing from Grinold & Kahn. This file states the MECHANISM and
what to check, and deliberately does not restate formulas from memory. Where an
implementation needs an exact expression — the deflated Sharpe ratio in
particular — verify it against the primary source before shipping a number that
depends on it. A formula recalled approximately is worse here than no formula:
it produces a specific, wrong, confident figure.

## 1. Purged cross-validation with an embargo

**The leak.** In a normal k-fold split, training and test rows are disjoint. In a
financial series they are not independent: a label at time *t* is computed from
data spanning *t* to *t+h*. A training observation inside that window has seen the
future the test observation is being asked to predict.

**Purging.** Drop from the training set every observation whose label window
overlaps the label window of any test observation. Not the observation's
timestamp — its *label window*. This is the step people skip, because a plain
timestamp split looks like it already separates them.

**The embargo.** Purging is not enough when features are serially correlated: a
training row immediately AFTER the test set still carries information about it.
Drop a further band after each test fold. The band is a fraction of the total
sample; there is no universal value, so state the one used and why.

**Combinatorial purged CV.** A single train/test split yields one backtest path
and one Sharpe. Splitting combinatorially yields many paths and therefore a
*distribution*, which is what you actually want: a strategy whose single path
looks good and whose distribution straddles zero has told you something a point
estimate hid.

**What to check:** is the split purged, is there an embargo, is its size stated,
and is the reported figure a distribution or a single draw.

## 2. Triple-barrier labelling

**The problem with fixed-horizon returns.** Labelling "the return over the next
five days" assumes you would have held for five days. You would not: a stop-loss
would have taken you out on day two. The model is trained on an outcome that
could not have happened.

**The method.** Three barriers per observation — a profit-take level, a stop-loss
level, and a time limit. The label is *which barrier was touched first*. Levels
are usually set from a volatility estimate rather than fixed, because a 2% move
means different things in different regimes.

**What to check:** are the barriers volatility-scaled, is the time limit stated,
and does the label record which barrier ended the observation rather than only
the sign.

## 3. Sample uniqueness under overlapping labels

**The problem.** Overlapping label windows mean two rows can describe largely the
same outcome. Standard learning assumes independent draws; here they are not, so
the effective sample is far smaller than the row count and every confidence
interval computed from that count is too narrow.

**Two responses:** weight each observation by its average uniqueness (how much of
its label window it does not share), or draw with a sequential bootstrap that
prefers observations overlapping little with those already drawn.

**What to check:** is a uniqueness weighting or effective sample size reported. A
row count offered as a sample size is a wrong number, not a rough one.

## 4. Fractional differentiation

**The dilemma.** Price levels are non-stationary; a model fitted to them learns a
level that will not recur. The reflex is a first difference — returns — which is
stationary and has thrown away the memory the signal lived in.

**The method.** Difference by the smallest order `d`, generally fractional, at
which the series passes a stationarity test while retaining maximum correlation
with the undifferenced series. `d` is a result, not a setting: it is searched for,
and it is reported.

**What to check:** is `d` reported at all, was it searched rather than assumed,
and was correlation with the original series measured — not just the stationarity
test passed. Passing the test is the constraint; keeping the memory is the
objective.

## 5. Meta-labelling

**What it is.** Two models rather than one. The primary decides the SIDE — long,
short, flat. The secondary decides only whether to ACT on that call, as a binary:
take this bet or pass.

**Why it helps.** The two tasks have different error costs. A side model tuned for
accuracy tends to trade too often; a secondary model can raise precision — fewer,
better-founded bets — without touching the side logic. It also gives a natural
place to size a bet by confidence, which a single model conflates with direction.

**What to check:** if a model both picks the side and decides whether to trade,
say whether those were separated. If not, the reported precision is measuring two
decisions at once.

## 6. The multiple-testing problem

**The mechanism.** Try enough configurations and one will look excellent by
chance. The reported Sharpe of the best of N trials is not an estimate of that
strategy's Sharpe — it is the maximum of N draws, and its expectation rises with
N even when every strategy is worthless.

**The minimum honest response:** report N. How many feature sets, parameter
values, and universes were tried to reach the reported one. A Sharpe without a
trials count cannot be interpreted, and the count is usually much larger than
people remember — every abandoned variant counts.

**The correction:** the deflated Sharpe ratio adjusts for the number of trials and
for the non-normality of returns. Its exact expression is not restated here (see
the sourcing note above); implement it from the primary source.

**What to check:** is N reported, and if a correction is claimed, does the
implementation cite where the expression came from.

## What this pack does not cover

Execution, order routing, market microstructure, and portfolio construction. The
installed quant command set covers those well — measured: order-book, VWAP/TWAP
and implementation-shortfall material across eighteen files, and nothing on any
method above. This pack exists to fill exactly that hole, not to duplicate what
is already there.
