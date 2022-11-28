import copy
import random
import saveModel
import numpy as np

ACTION_SET = ["p", "b"]
CARDS_SET = ["1", "2", "3"]
ROOT_MAP = {}
PASS = 0
BET = 1
PLAYER_1 = 0
PLAYER_2 = 1


class Node:
    def __init__(self, info_set, parent=None, left_child=None, right_child=None):
        self.data = info_set
        self.utility = np.array([0.0, 0.0])
        self.regret_sum = np.array([0.0, 0.0])
        self.strategy = np.array([0.0, 0.0])
        self.parent = parent
        self.left_child_p = left_child
        self.right_child_b = right_child
        self.player_id = (len(self.data) - 2) % 2 if not isLeaf(self.data) else -1

    def chooseAction(self, action: str):
        info_set = self.data + action
        node = Node(info_set, None, None)
        if action == "p":
            self.left_child_p = node
        elif action == "b":
            self.right_child_b = node

    def getStrategy(self) -> np.ndarray:
        total_regret = sum(self.regret_sum)
        if total_regret > 0:
            self.strategy  = self.regret_sum/total_regret
        else:
            self.strategy = np.array([0.5, 0.5])
        return self.strategy


def cfr(root, p0, p1):
    root.getStrategy()
    if root.player_id == -1:
        return root.utility
    if root.left_child_p:
        child_utility_p = cfr(root.left_child_p, p0 * root.strategy[0], p1)
    if root.right_child_b:
        child_utility_b = cfr(root.right_child_b, p0, p1 * root.strategy[1])
    # calculate the counterfactual value of current node
    node_util_player1 = \
        child_utility_p[PLAYER_1] * root.strategy[PASS] \
        + child_utility_b[PLAYER_1] * root.strategy[BET]
    node_util_player2 = \
        child_utility_p[PLAYER_2] * root.strategy[PASS] \
        + child_utility_b[PLAYER_2] * root.strategy[BET]
    utility = np.array([node_util_player1, node_util_player2], dtype=float)
    node_util = utility[root.player_id]
    '''
    counterfactual value for history h
    '''
    # counterfactual value
    prior_probability = p0 * p1
    counterfactual_value = prior_probability * node_util
    # counterfactual value intended play choose action pass or bet
    counterfactual_play_pass = child_utility_p[root.player_id] * prior_probability
    counterfactual_play_bet = child_utility_b[root.player_id] * prior_probability
    regret_value = np.array([counterfactual_play_pass, counterfactual_play_bet]) - counterfactual_value
    nonnegative_regret_value = np.maximum(regret_value, 0)
    root.regret_sum += nonnegative_regret_value
    print("node name: {}".format(root.data))
    print("regret: {}".format(root.regret_sum))
    # print("player 1 utility: {}".format(node_util_player1))
    # print("counterfactual value: {}".format(utility[root.player_id]*prior_probability))
    # print("counterfactual play pass: {}".format(counterfactual_play_pass))
    # print("counterfactual play bet: {}".format(counterfactual_play_bet))
    # print("regret value: {}".format(regret_value))
    print()
    # print("node util: {}".format(node_util))
    # print("regret: {}".format(regret_vector))
    # print("p0: {p0} p1: {p1}".format(p0=p0,p1=p1))
    # print("child_util_p: {}".format(child_utility_p))
    # print("child_util_b: {}".format(child_utility_b))
    '''
    calculate the return value
    '''
    return utility


def createTree(node):
    if isLeaf(node.data):
        node.utility = getPayoff(node.data)
        return
    for action in ACTION_SET:
        node.chooseAction(action)
    createTree(node.left_child_p)
    createTree(node.right_child_b)


def getPayoff(history: str, player_1=0, player_2=1) -> np.ndarray:
    rank_1 = int(history[0])
    rank_2 = int(history[1])
    if rank_1 > rank_2:
        isPlayer1CardHigher = True
    else:
        isPlayer1CardHigher = False
    if history[-2:] == "bb":
        util = np.array([2, -2]) if isPlayer1CardHigher else np.array([-2, 2])
    elif history[-2:] == "pp":
        util = np.array([1, -1]) if isPlayer1CardHigher else np.array([-1, 1])
    elif history[-3:] == "pbp":
        util = np.array([-1, 1])
    else:
        util = np.array([1, -1])
    return util


def isLeaf(data):
    return data[-2:] in ["pp", "pbp", "pbb", "bb", "bp"]


def playGame(root_map=ROOT_MAP):
    for i in range(10000):
        # deal the card to player1 and player 2
        hand_card = cards_dealer(CARDS_SET)
        # hand_card = "12"
        if hand_card not in root_map:
            node = Node(hand_card)
            root_map[hand_card] = node
            createTree(node)
        else:
            node = root_map[hand_card]
        cfr(node, 1.0, 1.0)


def cards_dealer(cards):
    temp = copy.deepcopy(cards)
    random.shuffle(temp)
    result = temp[0] + temp[1]
    return result


def main():
    playGame()
    saveModel.saveModel(variable=ROOT_MAP)


def postOrder(root):
    if root.player_id == -1:
        return
    if root.left_child_p:
        postOrder(root.left_child_p)
    if root.right_child_b:
        postOrder(root.right_child_b)
    print(root.data)


if __name__ == "__main__":
    main()
    # a = saveModel.loadModel("model.pkl")
    # postOrder(a["21"])
