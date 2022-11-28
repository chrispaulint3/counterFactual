import pickle
import tree.saveModel as saveModel


class Animal:
    def __init__(self):
        self.live = 5
        self.__my_self = 6


def saveObject(obj):
    with open("model.pkl", "wb") as f:
        pickle.dump([obj],f)


if __name__ == "__main__":
    # animal = Animal()
    # saveObject(animal)
    # with open("model.pkl","rb") as f:
    #     a = pickle.load(f)
    # print(a[0].live)
    c = saveModel.loadModel("model1.pkl")
    print(c)

