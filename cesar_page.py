import customtkinter as ctk
from tkinter.messagebox import showwarning,askyesnocancel
from pyperclip import copy

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class CesarSect(ctk.CTkFrame):
    def __init__(self,master,*args,**kwargs):
        super().__init__(master,*args,**kwargs)

        self.pack(
            fill="both",
            expand=True,
            padx=20,pady=20
        )

        self.textLb = ctk.CTkLabel(
            self,
            width=0.6*master._current_width,
            height=60,
            font=("Ubuntu Mono",30),
            text="Entrez un mot:"
        )
        self.textLb.place(
            relx=0.37,rely=0.17,
            anchor="center"
        )

        self.textWg = ctk.CTkEntry(
            self,
            width=0.6*master._current_width,
            height=60,
            font=("Ubuntu Mono",30),
            placeholder_text="Mot",
            show=None
        )
        
        self.textWg.place(
            relx=0.5,rely=0.25,
            anchor="center"
        )

        self.modeLb = ctk.CTkLabel(
            self,
            font=("Ubuntu Mono",26),
            text="Mode: ASCII"
        )

        self.modeLb.place(
            relx=0.34,rely=0.35,
            anchor="center"
        )

        self.modeSc = ctk.CTkSwitch(
            self,text="Lettres",
            font=("Ubuntu Mono",26)
        )

        self.modeSc.place(
            relx=0.6,rely=0.35,
            anchor="center"
        )

        self.cleLb = ctk.CTkLabel(
            self,
            font=("Ubuntu Mono",26),
            text="Clé: "
        )

        self.cleLb.place(
            relx=0.28,rely=0.45,
            anchor="center"
        )

        self.cleWg = ctk.CTkEntry(
            self,
            width=0.35*master._current_width,
            height=20,
            font=("Ubuntu Mono",26),
            placeholder_text="Entier ≥ 0"
        )

        self.cleWg.place(
            relx = 0.53,rely=0.45,
            anchor="center"
        )

        def decaler(x:str,cle:int,mode:bool) -> str:
            if mode:
                if x.isalpha():
                    if x.lower():
                        return chr((ord(x) - 97 + cle) % 26 + 97)
                    else:
                        return chr((ord(x) - 65 + cle) % 26 + 65)
                else: return x
            else:
                return chr(ord(x) + cle)
        
        def decaler_tout(signe:int=1):
            mot = self.textWg.get()
            s = self.cleWg.get()
            if s == "" or not s.isnumeric():
                showwarning(
                    title="Invalide!",
                    message="Votre clé est invalide.\nIl faut qu'il soit un entier.",
                    default="ok"
                )
            else:
                cle = int(s)
                mot_ch = "".join([
                    *map(
                        lambda x:decaler(
                            x,
                            signe*cle,
                            bool(self.modeSc.get())
                        ),
                        mot
                    )
                ])
                self.resLb.configure(text=f"Votre mot {'Chiffré' if signe == 1 else 'Déchiffré'} est \n{mot_ch}.")


        self.chBtn = ctk.CTkButton(
            self,
            text="Chiffrer le mot",
            width=0.55*master._current_width,
            height=50,
            font=("Ubuntu Mono",26),
            command=decaler_tout
        )
        
        self.chBtn.place(
            relx=0.5,rely=0.55,
            anchor="center"
        )

        self.dchBtn = ctk.CTkButton(
            self,
            text="Déchiffrer le mot",
            width=0.55*master._current_width,
            height=50,
            font=("Ubuntu Mono",26),
            command=lambda:decaler_tout(-1)
        )
        
        self.dchBtn.place(
            relx=0.5,rely=0.65,
            anchor="center"
        )

        self.prev_frame:ctk.CTkFrame

        def __retourner():
            self.forget()
            m = self.prev_frame(master=master)
            m.prev_frame = CesarSect


        self.retBtn = ctk.CTkButton(
            self,
            text="Retourner",
            width=0.55*master._current_width,
            height=50,
            font=("Ubuntu Mono",26),
            command=__retourner
        )
        
        self.retBtn.place(
            relx=0.5,rely=0.75,
            anchor="center"
        )

        self.resLb = ctk.CTkLabel(
            self,
            width=0.6*master._current_width,
            height=60,
            font=("Ubuntu Mono",30),
            text=""
        )
        self.resLb.place(
            relx=0.5,rely=0.85,
            anchor="center"
        )