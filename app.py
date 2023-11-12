import customtkinter as ctk
from enreg_page import EnregAuthSect
from data_page import DataSect


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resizable(False,False)
        self.title("App")
        self.geometry("800x900")

        m = EnregAuthSect(self)

if __name__=="__main__":
    app = App()
    app.mainloop()