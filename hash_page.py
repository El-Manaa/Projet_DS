import customtkinter as ctk
from tkinter.messagebox import askquestion,showwarning
from hashlib import sha256
from pyperclip import copy

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")




class HashSect(ctk.CTkFrame):
    def __init__(self,master:ctk.CTk,*args,**kwargs):
        super().__init__(master,*args,**kwargs)

        self.pack(
            fill="both",
            expand=True,
            padx=20,pady=20,
            anchor="center"
        )

        self.nameLabel = ctk.CTkLabel(
            self,
            text="Hachage",
            font=("Ubuntu Mono",50)
        )
        self.nameLabel.place(
            relx=0.5,rely=0.07,
            anchor="center"
        )

        self.textLb = ctk.CTkLabel(
            self,
            font=("Ubuntu Mono",30),
            text="Veuillez entrer un mot"
        )
        self.textLb.place(
            relx=0.5,rely=0.17,
            anchor="center"
        )


        self.textWg = ctk.CTkEntry(
            self,
            width=0.6*master._current_width,
            height=60,
            font=("Ubuntu Mono",30),
            placeholder_text="Mot",
            show="*"
        )
        
        self.textWg.place(
            relx=0.5,rely=0.25,
            anchor="center"
        )

        # Section : Fonction d'actions des boutons

        def __hacher():
            mot = self.textWg.get()
            mot_h = sha256(mot.encode()).hexdigest()
            resp = askquestion(
                title="Hacher avec sha256",
                message=f"Votre mot haché est {mot_h}\nVoulez-vous le copier?",
                default="yes"
            )
            if resp == "yes":
                copy(mot_h)
                self.resLb.configure(text="Le mot haché est copié.")
            else:
                self.resLb.configure(text="")


        def __attaquer():
            mot = self.textWg.get()
            with open("Dictionnaire.txt","r") as f:
                words = f.read().split("\n")
                if any(sha256(mot.encode()).hexdigest() == sha256(w.encode()).hexdigest() for w in words):
                    text = "J\'ai trouvé votre mot\ndans mon dictionnaire 💀💀💀"
                else:
                    text = "Je n\'ai pas trouvé votre mot\ndans mon dictionnaire 😠😠😠"
                self.resLb.configure(text=text)

        
        self.prev_frame:ctk.CTkFrame

        def __retourner():
            self.forget()
            m = self.prev_frame(master=master)
            m.prev_frame = HashSect

        # Section : Widgets boutons

        self.shaBtn = ctk.CTkButton(
            self,
            text="Hacher avec sha256",
            width=0.55*master._current_width,
            height=50,
            font=("Ubuntu Mono",26),
            command=__hacher
        )
        self.shaBtn.place(
            relx=0.5,rely=0.4,
            anchor="center"
        )

        self.atdBtn = ctk.CTkButton(
            self,
            text="Attaquer par dictionnaire",
            width=0.55*master._current_width,
            height=50,
            font=("Ubuntu Mono",26),
            command=__attaquer
        )
        self.atdBtn.place(
            relx=0.5,rely=0.55,
            anchor="center"
        )

        self.retBtn = ctk.CTkButton(
            self,
            text="Retourner",
            width=0.55*master._current_width,
            height=50,
            font=("Ubuntu Mono",26),
            command=__retourner
        )

        self.retBtn.place(
            relx=0.5,rely=0.70,
            anchor="center"
        )

        # Section : Label notificateur

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

        self.update()

