# TK Experiments - FakeNestedWindow
# This experiment creates a fake, cross-platform and customizable nested window in tkinter.

import tkinter as tk
import resources.common.tttk as tttk


class FakeNestedWindow(tk.Frame):
    def __init__(self,parent,initial_pos=(10,10),title="Untitled Nested Window"):
        """This is a nested window based on tk.Frame, which is cross-platform and cusomizable."""
        self.parent=parent
        self.title_str=title
        self.state="normal"
        self.width=300
        self.height=300
        # Things for internal use
        self._pointerdown_x=0
        self._pointerdown_y=0
        self._is_zoomed=False
        self._last_normal_w=self.width
        self._last_normal_h=self.height
        self._last_normal_x=0
        self._last_normal_y=0
        self._original_w=0
        self._original_h=0
        self._resize_dragger_using=False
        # UI
        #Titlebar
        self.base_frame=tk.Frame(parent,width=300,height=300)
        tk.Frame.__init__(self,self.base_frame,relief="solid",bd=2)
        self.titlebar=tk.Frame(self.base_frame,bg="#000000")
        self.titletxt=tk.Label(self.titlebar,bg="#000000",fg="#ffffff",text=self.title)
        self.titletxt.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        self.titlebar.pack(fill=tk.X)
        #Action buttons
        self.action_btns=tk.Frame(self.titlebar)
        self.minimize_btn=tttk.FlatButton(self.action_btns,text="0",font=("webdings",10),bg="#000000",fg="#ffffff",floatingbg="#303030",command=self.iconify)
        self.maximize_btn=tttk.FlatButton(self.action_btns,text="1",font=("webdings",10),bg="#000000",fg="#ffffff",floatingbg="#303030",command=self.toggle_normal_zoomed)
        self.close_btn=tttk.FlatButton(self.action_btns,text="r",font=("webdings",10),bg="#000000",fg="#ffffff",floatingbg="#ff0000",command=self.destroy)
        self.minimize_btn.pack(side=tk.LEFT,fill=tk.Y)
        self.maximize_btn.pack(side=tk.LEFT,fill=tk.Y)
        self.close_btn.pack(side=tk.LEFT,fill=tk.Y)
        self.action_btns.pack(side=tk.RIGHT,fill=tk.Y)
        #Main part
        tk.Frame.pack(self,fill=tk.BOTH,expand=True)
        #self.pack_propagate(False)
        #Resize dragger
        self.resize_dragger=tk.Frame(self.base_frame,bg="#99ccff",width=2,height=2,cursor="sizing")
        self.resize_dragger.place(x=self.base_frame.winfo_width()-2,y=self.base_frame.winfo_height()-2,width=2,height=2)
        self.resize_dragger.lift()
        self.after(50,self.nested_win_update)
        # Initialize
        self.base_frame.place(x=initial_pos[0],y=initial_pos[0],width=self.width,height=self.height)
        #Bind events
        self.titletxt.bind("<B1-Motion>",self._move)
        self.titletxt.bind("<Button-1>",self._on_button_down)
        self.resize_dragger.bind("<Enter>",lambda event:self._set_resize_dragger_size(big=True))
        self.resize_dragger.bind("<Leave>",lambda event:self._set_resize_dragger_size(big=False))
        self.resize_dragger.bind("<Button-1>",self._on_button_down)
        self.resize_dragger.bind("<B1-Motion>",self._on_drag_resize)
        self.resize_dragger.bind("<ButtonRelease-1>",self._on_resize_button_release)
    def iconify(self):
        self.pack_forget()
        self.base_frame.place(x=self.base_frame.winfo_x(),y=self.base_frame.winfo_y(),width=self.width,height=self.titlebar.winfo_height())
        self.minimize_btn["text"]="6"
        self.minimize_btn.unbind("<ButtonRelease-1>")
        self.minimize_btn.bind("<ButtonRelease-1>",lambda event:self.deiconify())
        self.state="iconify"
    def withdraw():
        self.base_frame.place_forget()
        self.state="hidden"
    def destroy(self):
        tk.Frame.destroy(self)
        self.base_frame.destroy()
    def deiconify(self):
        if self.state=="iconify":
            tk.Frame.pack(self,fill=tk.BOTH,expand=True)
            self.minimize_btn["text"]="0"
            self.minimize_btn.unbind("<ButtonRelease-1>")
            self.minimize_btn.bind("<ButtonRelease-1>",lambda event:self.iconify())
            self.base_frame.place(x=self.base_frame.winfo_x(),y=self.base_frame.winfo_y(),width=self.width,height=self.height)
        elif self.state=="hidden":
            self.base_frame.place(x=self._last_normal_x,y=self._last_normal_y,width=self.width,height=self.height)
    def _on_button_down(self,event):
        self._pointerdown_x=event.x#-self.base_frame.winfo_x()
        self._pointerdown_y=event.y#-self.base_frame.winfo_x()
        self._original_w=self.base_frame.winfo_width()
        self._original_h=self.base_frame.winfo_height()
    def _move(self, event, coords: list = [0, 0]):
        if self._is_zoomed:
            self.make_normal(sizeonly=True)
        if event.type.__str__() == '4':
            coords[0], coords[1] = event.x, event.y
        else:
            x, y = event.x - coords[0], event.y - coords[1]
            self.base_frame.place(x=event.x+self.base_frame.winfo_x()-self._pointerdown_x, y=event.y+self.base_frame.winfo_y()-self._pointerdown_y,
                                  width=self.base_frame.winfo_width(),height=self.base_frame.winfo_height())
    def make_zoomed(self):
        self._last_normal_w=self.base_frame.winfo_width()
        self._last_normal_h=self.base_frame.winfo_height()
        self._last_normal_x=self.base_frame.winfo_x()
        self._last_normal_y=self.base_frame.winfo_y()
        self.base_frame.place(x=0,y=0,width=self.parent.winfo_width(),height=self.parent.winfo_height())
        self.lift()
        self.maximize_btn["text"]="2"
        self._is_zoomed=True
    def make_normal(self,sizeonly=False):
        if sizeonly:
            self._last_normal_x=self.base_frame.winfo_x()
            self._last_normal_y=self.base_frame.winfo_y()
        self.base_frame.place(x=self._last_normal_x,y=self._last_normal_y,width=self._last_normal_w,height=self._last_normal_h)
        self.maximize_btn["text"]="1"
        self._is_zoomed=False
    def toggle_normal_zoomed(self):
        if self._is_zoomed:
            self.make_normal()
        else:
            self.make_zoomed()
    def nested_win_update(self):
        #print(self.base_frame.winfo_width()-2,self.base_frame.winfo_height()-2)
        if not self._resize_dragger_using:
            self.resize_dragger.place(x=self.base_frame.winfo_width()-2,y=self.base_frame.winfo_height()-2,width=2,height=2)
            self.resize_dragger.lift()
        self.titletxt["text"]=self.title_str
        self.after(50,self.nested_win_update)
        #tk.Frame.update(self)
    def title(self,new_title:str):
        self.title_str=new_title
    def resize(self,w,h):
        self.width=w
        self.height=h
        self.base_frame.place(width=w,height=h)
    def _set_resize_dragger_size(self,big=False):
        if big:
            self._resize_dragger_using=True
            self.resize_dragger.place(x=self.base_frame.winfo_width()-12,y=self.base_frame.winfo_height()-12,width=12,height=12)
        else:
            self._resize_dragger_using=False
            self.resize_dragger.place(x=self.base_frame.winfo_width()-2,y=self.base_frame.winfo_height()-2,width=2,height=2)
    def _on_drag_resize(self,event):
        self._resize_dragger_using=True
        self.base_frame.place(width=event.x+self._original_w+self._pointerdown_x if \
                              event.x+self._original_w+self._pointerdown_x>=300 else self.base_frame.winfo_width(),
                              height=event.y+self._original_h+self._pointerdown_y if \
                              event.y+self._original_h+self._pointerdown_y>=300 else self.base_frame.winfo_height())
    def _on_resize_button_release(self,event):
        self._resize_dragger_using=False


if __name__=="__main__":
    from PIL import Image, ImageTk
    import tkinter.ttk as ttk
    root=tk.Tk()
    root.title("FakeNestedWindow Test")
    #root.geometry("720x480")
    img=Image.open("./resources/common/background.jpg")
    img_resized=img.resize((int(img.size[0]*0.7),int(img.size[1]*0.7)))
    img_tk=ImageTk.PhotoImage(img_resized)
    tk.Label(root,image=img_tk).place(x=0,y=0)
    root.geometry(str(img_resized.size[0])+"x"+str(img_resized.size[1]))
    nested=FakeNestedWindow(root,title="Nested Window")
    img_illust=Image.open("./resources/fake_nested_window/illust.png")
    img_illust_resized=img_illust.resize((int(img_illust.size[0]*0.3),int(img_illust.size[1]*0.3)))
    img_illust_tk=ImageTk.PhotoImage(img_illust_resized)
    tk.Label(nested,image=img_illust_tk).pack(padx=20,pady=20,side=tk.LEFT)
    tk.Label(nested,text="Hello World",font=("Times New Roman",24,"bold"),anchor="w").pack(pady=15,fill=tk.X)
    tk.Label(nested,text="The quick brown fox jumps over the lazy dog.",anchor="w",wraplength=270,justify="left").pack(pady=5,fill=tk.X)
    nineteen_eightyfour_sel="""It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled \
into his breast in an effort to escape the vile wind,slipped quickly through the glass doors of Victory Mansions, though not quickly enough \
to prevent a swirl of gritty dust from entering along with him."""
    nineteen_eightyfour_frame=tk.Frame(nested)
    tk.Label(nineteen_eightyfour_frame,text=nineteen_eightyfour_sel,anchor="w",wraplength=270,justify="left").pack(fill=tk.X)
    ttk.Button(nineteen_eightyfour_frame,text="Text above copied from 1984",command=lambda:webbrowser.open("https://george-orwell.org/1984/")).pack(pady=2,anchor="e")
    nineteen_eightyfour_frame.pack(pady=5,anchor="w")
    title_input=tttk.TipEnter(nested,text="Title",command=lambda:None,btntxt="Change")
    title_input.command=lambda:nested.title(title_input.get())
    title_input.refresh()
    title_input.set("Nested Window")
    title_input.pack(pady=5,anchor="w")
    nested.resize(540,360)
    #root.update()
    #nested.update()
    root.mainloop()
