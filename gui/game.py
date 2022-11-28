from tkinter import *
import winsound
from baseWindow import BaseWindow


class GameWindow:
    def __init__(self, master, chosen_img_index):
        self.master = master
        self.root_frame = Frame(master=master, bg="green")
        self.root_frame.pack()
        self.img_list = [PhotoImage(file="./img/1.png"), PhotoImage(file="./img/2.png"), PhotoImage(file="./img/3.png")]
        self.chosen_img_index = chosen_img_index

        # 用户头像
        self.open_deal_box = Frame(self.root_frame, borderwidth=5, bg="green")
        self.open_deal_box.pack(side="bottom", pady=40)
        self.user_img = PhotoImage(file="./img/user.png")
        self.user_label = Label(self.open_deal_box, image=self.user_img, bg="green")
        self.user_label.pack(side="left",padx=30)
        self.hand_card_img = self.img_list[self.chosen_img_index]
        self.hand_card_label = Label(self.open_deal_box, image=self.hand_card_img)
        self.hand_card_label.pack(side="left",padx=30)

        # 对手牌区
        self.opponent_img = PhotoImage(file="./img/back.png")
        self.opponent_user_img = PhotoImage(file="./img/robot.png")
        self.opponent_card_box = Frame(self.root_frame, relief="groove", borderwidth=5, bg="green")
        self.opponent_card_box.pack(pady=60)
        self.robot_label = Label(self.opponent_card_box,image=self.opponent_user_img)
        self.robot_label.pack()
        self.opponent_card_label = Label(self.opponent_card_box, image=self.opponent_img)
        self.opponent_card_label.pack()
        # 定时器
        self.timer = 15
        self.time_info = "剩余时间：{} s".format(15)
        self.time_label = Label(self.root_frame, text=self.time_info, font="楷体 20 bold", bg="green")
        self.time_label.pack(pady=120)
        self.root_frame.after(1000, self.updateTime)
        # 播放音乐
        path = "sound/pokerGame.wav"
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def updateTime(self):
        self.timer -= 1
        self.time_info = "剩余时间：{} s".format(self.timer)
        self.time_label.config(text=self.time_info)
        self.root_frame.after(1000, self.updateTime)


if __name__ == "__main__":
    win = BaseWindow()
    game_win = GameWindow(win.root_win,0)
    win.mainLoop()
