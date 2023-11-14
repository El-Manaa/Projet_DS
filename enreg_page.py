import customtkinter as ctk
from re import compile,match,findall
from string import punctuation
from os import system
from time import sleep
from menu_page import Menu

class EnregAuthSect(ctk.CTkFrame):
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
            text="S'enregistrer ou s'authentifier",
            font=("Ubuntu Mono",45)
        )
        self.nameLabel.place(
            relx=0.5,rely=0.1,
            anchor="center"
        )

        self.loginLb = ctk.CTkLabel(
            self,
            font=("Ubuntu Mono",30),
            text="Login"
        )
        self.loginLb.place(
            relx=0.5,rely=0.2,
            anchor="center"
        )

        self.loginWg = ctk.CTkEntry(
            self,
            width=0.6*master._current_width,
            height=60,
            font=("Ubuntu Mono",30),
            placeholder_text="Login"
        )
        
        self.loginWg.place(
            relx=0.5,rely=0.27,
            anchor="center"
        )

        # Mot de passe

        self.pwdLb = ctk.CTkLabel(
            self,
            font=("Ubuntu Mono",30),
            text="Mot de passe"
        )
        self.pwdLb.place(
            relx=0.5,rely=0.33,
            anchor="center"
        )

        self.pwdWg = ctk.CTkEntry(
            self,
            width=0.6*master._current_width,
            height=60,
            font=("Ubuntu Mono",30),
            placeholder_text="Mot de passe",
            show="*"
        )
        
        self.pwdWg.place(
            relx=0.5,rely=0.4,
            anchor="center"
        )

        self.prev_frame:ctk.CTkFrame = Menu

        def __change_frame(Sect:type):
            self.destroy()
            h = Sect(master=master)
            h.prev_frame = EnregAuthSect              


        def __login():
            email_re = compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
            password_re = compile(rf"^([A-Z]{{1,}}|[a-z]{{1,}}|[0-9]{{1,}}|[{punctuation}]{{1,}}){{8}}$")
            email = self.loginWg.get()
            password = self.pwdWg.get()
            if (match(email_re,email) != None) and (match(password_re,password)):
                cred_re = compile(r"[0-9]+\.  Login : (.+)\n    Mot de passe : (.+)")
                with open("Enregistrements.txt","r+") as f:
                    groups = findall(cred_re,f.read())
                    emails = (x[0] for x in groups)
                    if groups != []:
                        if email in emails:
                            self.resLb.configure(text="Vous êtes déjà enregistré(e).")
                        else:
                            f.write(f"\n\n{len(groups) + 1}.  Login : {email}\n    Mot de passe : {password}")
                            self.resLb.configure(text="Félicitations. Vous êtes enregistré(e).")
                    else:
                        f.write(f"1.  Login : {email}\n    Mot de passe : {password}")
                        self.resLb.configure(text="Félicitations. Vous êtes enregistré(e).")
            else:
                self.resLb.configure(text="Le login ou le mot de passe\nou les deux sont invalides")
            self.loginWg.delete(0,'end')
            self.pwdWg.delete(0,'end')


        self.enregBtn = ctk.CTkButton(
            self,
            text="S'enregistrer",
            font=("Ubuntu Mono",26),
            width=0.5*master._current_width,height=50,
            command=__login
        )

        self.enregBtn.place(
            relx=0.5,rely=0.5,
            anchor="center"
        )

        def __auth():
            email = self.loginWg.get()
            password = self.pwdWg.get()
            cred_re = compile(r"[0-9]+\.  Login : (.+)\n    Mot de passe : (.+)")
            with open("Enregistrements.txt","r+") as f:
                groups = findall(cred_re,f.read())
                if groups != []:
                    if any(x[0] == email for x in groups):
                        if all(x[1] != password for x in groups):
                            self.resLb.configure(text="Mot de passe invalide")                     
                        else:
                            self.resLb.configure(text="Vous êtes bienvenu(e)(s)!")
                            sleep(0.75)
                            __change_frame(Menu)
                    else:
                        self.resLb.configure(text="Vous n'êtes pas enregistré(e).\nVeuillez s'enregistrer.")
                else:
                    self.resLb.configure(text="Vous n'êtes pas enregistré(e)")
            self.loginWg.delete(0,'end')
            self.loginWg._activate_placeholder()
            self.pwdWg.delete(0,'end')
            self.pwdWg._activate_placeholder()
            self.pwdWg._entry_focus_out()

        self.authBtn = ctk.CTkButton(
            self,
            text="S'authentifier",
            font=("Ubuntu Mono",26),
            width=0.5*master._current_width,height=50,
            command=__auth
        )

        self.authBtn.place(
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

        self.resLb = ctk.CTkLabel(
            self,
            width=0.6*master._current_width,
            height=60,
            font=("Ubuntu Mono",30),
            text=""
        )
        self.resLb.place(
            relx=0.5,rely=0.8,
            anchor="center"
        )

