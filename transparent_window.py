# TK Experiments - Transparent Window
# The experiments creates a transparent window in tkinter
import tkinter as tk
import random
import platform


class TransparentWindow(tk.Tk):

    def __init__(self, position, size, no_titlebar: bool = True):
        super().__init__()

        self.x = position[0]
        self.y = position[1]
        self.width = size[0]
        self.height = size[1]
        self.wm_geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')

        self.titlebar = no_titlebar
        self.wm_overrideredirect(self.titlebar)

        if platform.platform() != 'Darwin':
            this = self.random_color()
            self.configure(bg=this)
            self.wm_attributes('-transparentcolor', this)

            self.set_color()
        else:
            self.configure(bg='SystemTransparent')
            self.wm_attributes('-transparent', True)

    def random_color(self):
        colorArr = ['1', '2', '3', '4', '5', '6', '7',
                    '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        color = ""
        for i in range(6):
            color += colorArr[random.randint(0, 14)]
        return "#" + color

    def set_color(self):
        this = self.random_color()
        self.configure(bg=this)
        self.wm_attributes('-transparentcolor', this)
        self.after(500, self.set_color)

if __name__ == '__main__':
    root = TransparentWindow([20, 20], [100, 40])
    root.mainloop()