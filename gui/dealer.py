from tkinter import *
from baseWindow import BaseWindow
from game import GameWindow
import random
import game


class Dealer:
    def __init__(self, master):
        self.root_win = master
        self.root_frame = Frame(master,bg="green")
        self.root_frame.pack()
        self.card_list = []
        # 加载图片资源
        self.chosen_img_index = 0
        self.img_list = [PhotoImage(file="./img/1.png"), PhotoImage(file="./img/2.png"), PhotoImage(file="./img/3.png")]
        # 洗牌区域初始化
        self.box = Frame(self.root_frame, relief="groove", borderwidth=5, bg="green")
        self.box.pack(pady=50)
        self.back_img = PhotoImage(file="./img/back.png")
        self.create_card(self.box, self.back_img)
        # 提示区域与明牌区域初始化
        self.box_introduction = Frame(self.root_frame, relief="groove", borderwidth=5, bg="green")
        self.box_introduction.pack()
        self.intro_string = "请选择手牌"
        self.intro_label = Label(self.box_introduction, text=self.intro_string, font="楷体 60 bold", bg="green")
        self.intro_label.pack()
        # 明牌区域
        self.open_deal_box = self.open_deal_box = Frame(self.root_frame, relief="groove", borderwidth=5, bg="green",
                                                        height=200)
        self.open_deal_box.pack(pady=120)
        self.hand_card_label = Label(self.open_deal_box, bg="green")

    def create_card(self, parent_frame, img):
        for j in range(3):
            card_back_label = Label(parent_frame, image=img)
            card_back_label.pack(side="left", padx=40)
            card_back_label.bind("<Leave>", self.leave)
            self.card_list.append(card_back_label)
        self.card_list[0].bind("<Button-1>", self.click_card)
        self.card_list[1].bind("<Button-1>", self.click_card)
        self.card_list[2].bind("<Button-1>", self.click_card)
        self.card_list[0].bind("<Enter>", self.hover1)
        self.card_list[1].bind("<Enter>", self.hover2)
        self.card_list[2].bind("<Enter>", self.hover3)

    def click_card(self, event):
        a = random.randint(0, 2)
        self.chosen_img_index = a
        info_string = "您的手牌是: {}".format(a + 1)
        self.intro_label.config(text=info_string)
        self.intro_label.pack()
        self.hand_card_label.config(image=self.img_list[a])
        self.hand_card_label.pack()
        for i in range(3):
            self.card_list[i].unbind("<Enter>")
            self.card_list[i].unbind("<Button-1>")
        self.to_game_win()

    def hover1(self, event):
        self.intro_label.config(text="选择牌1")

    def hover2(self, event):
        self.intro_label.config(text="选择牌2")

    def hover3(self, event):
        self.intro_label.config(text="选择牌3")

    def leave(self, event):
        self.intro_label.config(text="请选择手牌")

    def to_game_win(self):
        # self.dealer_win.
        self.root_frame.destroy()
        # self.root_win.destroy()
        # game_window = GameWindow()
        # game_window.mainLoop()
        self.root_frame = Frame(self.root_win)
        self.root_frame.pack()
        GameWindow(self.root_win, self.chosen_img_index)
        pass


if __name__ == "__main__":
    base_window = BaseWindow()
    dealer_window = Dealer(base_window.root_win)
    base_window.mainLoop()
