---
name: docs-fetchai-agents-aea
description: The AEA gym skill demonstrates how a custom Reinforcement Learning agent,
  that uses OpenAI's <a href="https://www.gymlibrary.dev/" target="blank">gym</a>
  library, may be embedded into an AEA skill and connection.
---

# Gym Skill

The AEA gym skill demonstrates how a custom Reinforcement Learning agent, that uses OpenAI's <a href="https://www.gymlibrary.dev/" target="_blank">gym</a> library, may be embedded into an AEA skill and connection.

## Discussion

The gym skills demonstrate how to wrap a Reinforcement Learning agent in a skill.
The example decouples the RL agent from the `gym.Env` allowing them to run in separate execution environments, potentially owned by different entities.

## Preparation Instructions

### Dependencies

Follow the <a href="../quickstart/#preliminaries">Preliminaries</a> and <a href="../quickstart/#installation">Installation</a> sections from the AEA quick start.

Download the necessary directories into your working directory:

``` bash
mkdir gym_skill_agent
svn export https://github.com/fetchai/agents-aea.git/trunk/examples
```

Install the `gym` and `numpy` library.

``` bash
pip install numpy gym
```

## Demo Instructions

### Create the AEA

First, fetch the gym AEA:

``` bash
aea fetch fetchai/gym_aea:0.26.5 --alias my_gym_aea
cd my_gym_aea
aea install
```

??? note "Alternatively, create from scratch:"

    ### Create the AEA

    In the root directory, create the gym AEA and enter the project.

    ``` bash
    aea create my_gym_aea
    cd my_gym_aea
    ```

    ### Add the gym skill

    ``` bash
    aea add skill fetchai/gym:0.21.6
    ```

    ### Set gym connection as default

    ``` bash
    aea config set agent.default_connection fetchai/gym:0.20.6
    ```

    ### Install the skill dependencies

    To install the `gym` package, a dependency of the gym skill, from PyPI run

    ``` bash
    aea install
    ```

### Set up the Training Environment

#### Copy the Gym Environment to the AEA Directory

``` bash
mkdir gyms
cp -a ../examples/gym_ex/gyms/. gyms/
```

#### Update the Connection Configuration

``` bash
aea config set vendor.fetchai.connections.gym.config.env 'gyms.env.BanditNArmedRandom'
```

#### Create and Add a Private Key

``` bash
aea generate-key fetchai
aea add-key fetchai
```

### Run the AEA with the Gym Connection

``` bash
aea run
```

You will see the gym training logs.

<img src="../assets/gym-training.png" alt="AEA gym training logs" class="center">

### Delete the AEA

When you're done, you can go up a level and delete the AEA.

``` bash
cd ..
aea delete my_gym_aea
```

## Communication

This diagram shows the communication between the AEA and the gym environment

``` mermaid
    sequenceDiagram
        participant AEA
        participant Environment

        activate AEA
        activate Environment
        AEA->>Environment: reset
        loop learn
            AEA->>Environment: act
            Environment->>AEA: percept
        end
        AEA->>Environment: close

        deactivate AEA
        deactivate Environment
```

## Skill Architecture

The skill consists of two core components: `GymHandler` and `GymTask`.

In the `setup` method of the `GymHandler` the `GymTask` is initialized, as well as its `setup` and `execute` methods called. The handler, which is registered against the `GymMessage.protocol_id` then filters for messages of that protocol with the performative `GymMessage.Performative.PERCEPT`. These messages are passed to the `proxy_env_queue` of the task.

The `GymTask` is responsible for training the RL agent. In particular, `MyRLAgent` is initialized and trained against `ProxyEnv`. The `ProxyEnv` instantiates a `gym.Env` class and therefore implements its API. This means the proxy environment is compatible with any `gym` compatible RL agent. However, unlike other environments it only acts as a proxy and does not implement an environment of its own. It allows for the decoupling of the process environment of the `gym.env` from the process environment of the RL agent. The actual `gym.env` against which the agent is trained is wrapped by the `gym` connection. The proxy environment and gym connection communicate via a protocol, the `gym` protocol. Note, it would trivially be possible to implement the `gym` environment in another AEA; this way one AEA could provide `gym` environments as a service. Naturally, the overhead created by the introduction of the extra layers causes a higher latency when training the RL agent.

In this particular skill, which chiefly serves for demonstration purposes, we implement a very basic RL agent. The agent trains a model of price of `n` goods: it aims to discover the most likely price of each good. To this end, the agent randomly selects one of the `n` goods on each training step and then chooses as an `action` the price which it deems is most likely accepted. Each good is represented by an id and the possible price range `[1,100]` divided into 100 integer bins. For each price bin, a `PriceBandit` is created which models the likelihood of this price. In particular, a price bandit maintains a <a href="https://en.wikipedia.org/wiki/Beta_distribution" target="_blank">beta distribution</a>. The beta distribution is initialized to the uniform distribution. Each time the price associated with a given `PriceBandit` is accepted or rejected the distribution maintained by the `PriceBandit` is updated. For each good, the agent can therefore over time learn which price is most likely.

<img src="../assets/gym-skill.jpg" alt="Gym skill illustration" class="center" style="display: block; margin-left: auto; margin-right: auto;width:80%;">

The illustration shows how the RL agent only interacts with the proxy environment by sending it `action (A)` and receiving `observation (O)`, `reward (R)`, `done (D)` and  `info (I)`.
