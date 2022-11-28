from tkinter import *
from baseWindow import BaseWindow


class Dealer(BaseWindow):
    def __init__(self):
        super().__init__()
        self.card_list = []
        # 洗牌区域初始化
        self.box = Frame(self.root_frame, relief="groove", borderwidth=5, bg="green")
        self.box.pack(pady=50)
        self.back_img = PhotoImage(file="./img/back.png")
        self.create_card(self.box,self.back_img)

    def create_card(self, parent_frame, img):
        for j in range(3):
            card_back_label = Label(parent_frame, image=img)
            card_back_label.pack(side="left", padx=40)
            self.card_list.append(card_back_label)
        # self.card_list[0].bind("<Button-1>", self.click_card)
        # self.card_list[1].bind("<Button-1>", self.click_card)
        # self.card_list[2].bind("<Button-1>", self.click_card)
        # self.card_list[0].bind("<Enter>", self.hover1)
        # self.card_list[1].bind("<Enter>", self.hover2)
        # self.card_list[2].bind("<Enter>", self.hover3)

    def open_window(self):
        self.root_win.mainloop()


dealer = Dealer()
dealer.open_window()
