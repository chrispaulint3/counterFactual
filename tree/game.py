import random
import saveModel
import numpy as np
import saveModel
from kuhnPoker import Node

TEST_STRATEGY = {"12": "x", "32": "B", "33": "P"}

'''
load the model and use the strategy
the player represents the player in the game,player=0:first player,player=1:second player
'''


class PokerAgent:
    def __init__(self, strategy_map, info_set, player):
        self.strategy_map = strategy_map
        self.player = player
        self.info_set = info_set
        self.selected_game_tree = self.selectTree()

    def selectTree(self) -> list:
        tree_list = []
        for key in self.strategy_map.keys():
            if key[self.player] == self.info_set[0]:
                tree_list.append(self.strategy_map[key])
        return tree_list

    def chooseAction(self):
        decision_point = []
        strategy_sum = np.array([0.0, 0.0])
        for tree in self.selected_game_tree:
            node = tree
            for action in self.info_set:
                if action == "p":
                    node = tree.left_child_p
                elif action == "b":
                    node = tree.right_child_b
            decision_point.append(node)
        for i in decision_point:
            i.getStrategy()
            print(i.data)
            strategy_sum += i.strategy
        strategy_sum = strategy_sum / 2
        print(strategy_sum)
        action = self.roulette(strategy_sum)
        self.info_set += action
        return action

    def roulette(self, probability: np.ndarray) -> str:
        """
        :param probability:
        :return: the index 0 represent the action p and index 1 represent the action b
        """
        random_value = random.random()
        print("random calue: {}".format(random_value))
        temp = 0.0
        action_map = {0: "p", 1: "b"}
        action_index = -1
        for index, prob in enumerate(probability):
            temp += prob
            if temp < random_value:
                continue
            else:
                action_index = index
                break
        return action_map[action_index]

    def addOpponentAction(self, action: str):
        self.info_set += action


class Referee:
    def __init__(self):
        self.history = ""
        self.cards = np.array(["1", "2", "3"])

    def updateHistory(self, action: str):
        self.history += action

    def dealer(self):
        random.shuffle(self.cards)
        self.history = self.history + str(self.cards[0]) + str(self.cards[1])

    def isGameOver(self):
        return self.history[-2:] in ["pp", "bb", "bp"] or self.history[-3:] in ["pbp", "pbb"]

    def winnerReward(self):
        rank_1 = int(self.history[0])
        rank_2 = int(self.history[1])
        if rank_1 > rank_2:
            isPlayer1CardHigher = True
        else:
            isPlayer1CardHigher = False
        if self.history[-2:] == "bb":
            util = np.array([2, -2]) if isPlayer1CardHigher else np.array([-2, 2])
        elif self.history[-2:] == "pp":
            util = np.array([1, -1]) if isPlayer1CardHigher else np.array([-1, 1])
        elif self.history[-3:] == "pbp":
            util = np.array([-1, 1])
        else:
            util = np.array([1, -1])
        return util


def postOrder(root: Node):
    if root.player_id == -1:
        return
    if root.left_child_p:
        postOrder(root.left_child_p)
    if root.right_child_b:
        postOrder(root.right_child_b)
    print(root.data)
    print(root.regret_sum)
    print(root.getStrategy())


def main():
    # 加载模型
    strategy_map = saveModel.loadModel("model.pkl")
    # 游戏裁判初始化并进行发牌
    referee = Referee()
    referee.dealer()
    # 游戏机器人进行初始化
    agent = PokerAgent(strategy_map, referee.history[1], 1)
    # 开始游戏
    while 1:
        print("你的手牌是：{}".format(referee.history[0]))
        player1_action = input("输入你的行动")
        # 裁判对玩家行动进行记录
        referee.updateHistory(player1_action)
        #
        if referee.isGameOver():
            break
        # 机器人对玩家的行为进行记录
        agent.addOpponentAction(player1_action)
        player2_action = agent.chooseAction()
        print("机器人的行动为：{}".format(player2_action))
        # 裁判对玩家的行为进行记录
        referee.updateHistory(player2_action)
        if referee.isGameOver():
            break
    result = referee.winnerReward()
    if result[0] < 0:
        print("你输了")
    else:
        print("你赢了")
    print("比赛结果： {}".format(result[0]))
    print()
    print("总结：")
    print("机器人手牌：{}".format(referee.history[1]))

    # human_card = "1"
    # agent_card = "2"
    # agent = PokerAgent(strategy_map,"1",1)
    # human_action1 = "b"
    # agent.addOpponentAction(human_action1)
    # for i in agent.selected_game_tree:
    #     print(i.data)
    # print(agent.chooseAction())
    # postOrder(strategy_map["31"])
    # postOrder(strategy_map["21"])


if __name__ == "__main__":
    main()
    # agent = PokerAgent(TEST_STRATEGY, "1", 1)
    # print(agent.roulette(np.array([0.4,0.6])))


