from tkinter import *
from tkinter.messagebox import *


class BaseWindow:
    def __init__(self):
        self.root_win = Tk()
        self.root_win.title("poker game")
        self.root_win.geometry("1440x920+0+0")
        self.root_win.configure(bg="green")
        self.root_win.resizable(False, False)
        self.root_frame = Frame(self.root_win,bg="green")
        self.root_frame.pack()
        # 菜单组件
        self.menu = Menu(self.root_win)
        self.menu.add_command(label="游戏")
        self.menu.add_command(label="帮助")
        self.menu.add_command(label="退出",command=self.quitMessage)
        self.root_win.config(menu=self.menu)


    def quitMessage(self):
        boo = askokcancel("退出提醒","您将要退出游戏，点击确定即可退出")
        if boo:
            self.root_win.quit()

    def mainLoop(self):
        self.root_win.mainloop()



