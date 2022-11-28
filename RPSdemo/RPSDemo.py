import random
import numpy as np

'''
global variable in RPS game
'''
# macro define the regret position of the score
ACTION_MAP = {"rock": 0, "paper": 1, "scissor": 2}
# time step T
T = 100
# the payoff table rock paper scissor
PAYOFF_TABLE = np.array([
    [(0, 0), (-1, 1), (1, -1)],
    [(1, -1), (0, 0), (-1, 1)],
    [(-1, 1), (1, -1), (0, 0)]])

'''
global variable for player1
'''
PLAYER1_STRATEGY = {"rock": 0.8, "paper": 0.2, "scissor": 0}
PLAYER1_REGRET_SUM = np.array([0, 0, 0])
PLAYER1_STRATEGY_SUM = {"rock": 0, "paper": 0, "scissor": 0}

'''
global variable for player2
'''
PLAYER2_STRATEGY = {"rock": 0.2, "paper": 0.1, "scissor": 0.7}
PLAYER2_REGRET_SUM = np.array([0, 0, 0])
PLAYER2_STRATEGY_SUM = {"rock": 0, "paper": 0, "scissor": 0}


# this function change the PLAYER_STRATEGY in place
def strategyDistribution(regret_sum: np.ndarray, strategy_list: dict) -> dict:
    normalization = sum(regret_sum)
    if normalization <= 0:
        strategy_list["rock"] = 1 / 3
        strategy_list["paper"] = 1 / 3
        strategy_list["scissor"] = 1 / 3
    else:
        strategy_list["rock"] = regret_sum[ACTION_MAP["rock"]] / normalization
        strategy_list["paper"] = regret_sum[ACTION_MAP["paper"]] / normalization
        strategy_list["scissor"] = regret_sum[ACTION_MAP["scissor"]] / normalization
    return strategy_list


def getStrategy(strategy_list: dict) -> str:
    r = random.random()
    cumulative_probability = 0
    for strategy, probability in strategy_list.items():
        cumulative_probability += probability
        if cumulative_probability >= r:
            return strategy


def getRegretList(my_action: str, opponent_action: str) -> np.ndarray:
    global PAYOFF_TABLE
    global ACTION_MAP
    utility_list = PAYOFF_TABLE[:, ACTION_MAP[opponent_action]][:, 0]
    actual_action_utility = PAYOFF_TABLE[ACTION_MAP[my_action], ACTION_MAP[opponent_action]][0]
    regret_list = utility_list - actual_action_utility
    return regret_list


def updateStrategySum(player_strategy: dict, player_strategy_sum: dict):
    for key, value in player_strategy.items():
        if key in player_strategy:
            player_strategy_sum[key] += value


def agentPipeline(player_regret_sum, player_strategy) -> str:
    player_strategy1 = getStrategy(player_strategy)
    strategyDistribution(player_regret_sum, player_strategy)
    return player_strategy1


def twoPlayerZeroSumGame(t):
    for i in range(t):
        global PLAYER1_REGRET_SUM
        global PLAYER2_REGRET_SUM
        global PLAYER1_STRATEGY
        global PLAYER2_STRATEGY
        print("player 1 strategy profile: {}".format(PLAYER1_STRATEGY))
        print("player 2 strategy profile: {}".format(PLAYER2_STRATEGY))
        player1_strategy = agentPipeline(PLAYER1_REGRET_SUM, PLAYER1_STRATEGY)
        player2_strategy = agentPipeline(PLAYER2_REGRET_SUM, PLAYER2_STRATEGY)
        print("player 1 strategy: {}".format(player1_strategy))
        print("player 2 strategy: {}".format(player2_strategy))
        player1_regret_list = getRegretList(player1_strategy, player2_strategy)
        player2_regret_list = getRegretList(player2_strategy, player1_strategy)
        print("player 1 regret list: {}".format(player1_regret_list))
        PLAYER1_REGRET_SUM += np.maximum(player1_regret_list, 0)
        print("player 1 regret sum: {}".format(PLAYER1_REGRET_SUM))
        PLAYER2_REGRET_SUM += np.maximum(player2_regret_list, 0)
        updateStrategySum(PLAYER1_STRATEGY, PLAYER1_STRATEGY_SUM)
        updateStrategySum(PLAYER2_STRATEGY, PLAYER2_STRATEGY_SUM)
        print("-------------------------")


def gameWithFixedStrategy(t):
    for i in range(t):
        global PLAYER1_REGRET_SUM
        global PLAYER2_REGRET_SUM
        global PLAYER1_STRATEGY
        global PLAYER2_STRATEGY
        print("player 1 strategy profile: {}".format(PLAYER1_STRATEGY))
        print("player 2 strategy profile: {}".format(PLAYER2_STRATEGY))
        player1_strategy = agentPipeline(PLAYER1_REGRET_SUM, PLAYER1_STRATEGY)
        player2_strategy = getStrategy(PLAYER2_STRATEGY)
        player1_regret_list = getRegretList(player1_strategy, player2_strategy)
        print("player 1 regret list: {}".format(player1_regret_list))
        PLAYER1_REGRET_SUM += np.maximum(player1_regret_list, 0)
        print("player 1 regret sum: {}".format(PLAYER1_REGRET_SUM))
        updateStrategySum(PLAYER1_STRATEGY, PLAYER1_STRATEGY_SUM)
        print("-------------------------")


# definition of action
if __name__ == "__main__":
    #twoPlayerZeroSumGame(T)
    gameWithFixedStrategy(T)
    average_regret = PLAYER1_REGRET_SUM / T
    average_strategy = np.array(list(PLAYER1_STRATEGY_SUM.values())) / T
    print("average regret: {}".format(average_regret))
    print("average strategy: {}".format(average_strategy))

