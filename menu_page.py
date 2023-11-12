import customtkinter as ctk
from hash_page import HashSect
from cesar_page import CesarSect
from data_page import DataSect


class Menu(ctk.CTkFrame):
    def __init__(self,master:ctk.CTk,*args,**kwargs):
        super().__init__(master,*args,**kwargs)

        self.pack(
            fill="both",
            expand=True,
            padx=20,pady=20,
            anchor="center"
        )

        # Title Label
        self.nameLabel = ctk.CTkLabel(
            self,
            text="Bienvenu aux jeux",
            font=("Ubuntu Mono",50)
        )
        self.nameLabel.place(
            relx=0.5,rely=0.175,
            anchor="center"
        )

        self.prev_frame:ctk.CTkFrame = Menu

        def __change_frame(Sect:type):
            self.destroy()
            h = Sect(master=master)
            h.prev_frame = Menu               


        # Hash button
        self.hashBtn = ctk.CTkButton(
            self,
            text="Jouer Hash",
            font=("Ubuntu Mono",26),
            width=0.5*master._current_width,
            height=50,
            command=lambda:__change_frame(HashSect)
        )
        self.hashBtn.place(
            relx=0.5,rely=0.4,
            anchor="center"
        )

        # Cesar button

        self.cesarBtn = ctk.CTkButton(
            self,
            text="Jouer César",
            font=("Ubuntu Mono",26),
            width=0.5*master._current_width,height=50,
            command=lambda:__change_frame(CesarSect)
        )
        self.cesarBtn.place(
            relx = 0.5,rely= 0.5,
            anchor="center"
        )

        self.dataBtn = ctk.CTkButton(
            self,
            text="Jouer Data",
            font=("Ubuntu Mono",26),
            width=0.5*master._current_width,height=50,
            command=lambda:__change_frame(DataSect)
        )
        self.dataBtn.place(
            relx=0.5,rely=0.6,
            anchor="center"
        )

        self.quitBtn = ctk.CTkButton(
            self,
            text="Quitter",
            font=("Ubuntu Mono",26),
            width=0.5*master._current_width,height=50,
            command=master.destroy
        )
        self.quitBtn.place(
            relx=0.5,rely=0.7,
            anchor="center"
        )

        self.update()
