# Counterfactual Regret Minimization
## 1 regret matching algorithm
1. For each player, initialize all cumulative regrets to 0
2.  For some number of iterations:
    1. Compute a regret-matching strategy profile. (If all regrets for a player are non-positive, use
    a uniform random strategy.)
    2. Add the strategy profile to the strategy profile sum.
    3. Select each player action profile according the strategy profile
    4. Compute player regrets.
    5. Add player regrets to player cumulative regrets.
    6. Return the average strategy profile, i.e. the strategy profile sum divided by the number of
iterations.
## 2 counterfactual regret minimization in kuhn poker
Node
* kuhn node definition
* get current information set
* get average information set strategy
* get information set string representation  

CFR
* get current player
* calculate the payoff values
* cecursively call cfr
* compute and accumulate counterfactual regret

