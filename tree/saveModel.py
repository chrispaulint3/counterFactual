import pickle


class Node:
    def __init__(self, data, left_child=None, right_child=None):
        self.data = data
        self.left_child = left_child
        self.right_child = right_child

    def addLeftChild(self, left_child):
        self.left_child = left_child

    def addRightChild(self, right_child):
        self.right_child = right_child


def saveModel(variable, file_path="model.pkl"):
    # mode：write only and open as binary file
    with open(file_path, "wb") as f:
        pickle.dump(variable, f)


def loadModel(file_path):
    # mode: read only and open as binary file
    with open(file_path, "rb") as f:
        result = pickle.load(f)
    return result


if __name__ == "__main__":
    # orange = Node("Orange")
    # melon = Node("melon")
    # apple = Node("apple",orange,melon)
    # saveModel(apple)
    a = loadModel("model.pkl")
    print(a.data)
    print(a.left_child.data)

