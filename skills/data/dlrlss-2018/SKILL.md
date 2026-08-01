---
name: dlrlss-2018
description: '- RL with policy advice. Azar et al., ECML 2013.'
---

# Transfer / meta / lifelong learning

- RL with policy advice. Azar et al., ECML 2013.

        - Reduction from RL to bandit problem.

- Regret bounds: sum of differences between actual policy and optimal policy.

- Regret scales with the number of tasks \sqrt(M), rather than the state and
  action space.

- Brunskill and Li, UAI 2013. Reduce from RL to (active) classification
  problem.

- https://cs.stanford.edu/people/ebrun

- Provably speeding multitask RL. Guo and Brunskill, AAAI 2015. K tasks sampled
  from M tasks. Evaluation goal: provably improve performance. Approach:
  quickly cluster, then share.

- Killian et al., NIPS 2017. Bayesian NNs for modeling MDP dynamics.

- Smooth latent policy space for crossdomain transfer.
  Anmar et al., IJCAI 2015. Limited theoretical results (some nice convergence
  results).

- Model-agnostic meta-learning. Finn et al., ICML 2017.
