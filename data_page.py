import customtkinter as ctk
from customtkinter import filedialog
from rdatasets import data,items
from sklearn import datasets as skd
import statsmodels.datasets as stsd
from pandas import DataFrame,read_csv,read_sql_query
from json import dump
from webbrowser import open_new,open as open_t
# Pour Data
from shiny import App,ui,render,reactive
from shinywidgets import output_widget,render_widget
import plotly.express as px,plotly.graph_objs as go
from plotly.subplots import make_subplots
import sqlite3
# Autres
import asyncio



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class DataSect(ctk.CTkFrame):
    def __init__(self,master,*args,**kwargs):
        super().__init__(master,*args,**kwargs)

        self.pack(
            fill="both",
            expand=True,
            padx=20,pady=20,
            anchor="center"
        )

        self.nameLabel = ctk.CTkLabel(
            self,
            text="Data",
            font=("Ubuntu Mono",50)
        )
        self.nameLabel.place(
            relx=0.5,rely=0.1,
            anchor="center"
        )

        self.textLb = ctk.CTkLabel(
            self,
            font=("Ubuntu Mono",30),
            text="Veuillez introduire le source\net le nom d'un dataset"
        )
        self.textLb.place(
            relx=0.5,rely=0.2,
            anchor="center"
        )

        self.srcOpt = ctk.CTkComboBox(
            self,
            width=0.2*master._current_width,
            height=60,
            font=("Ubuntu Mono",26),
            values=("-source","Rdatasets","Sci-kit","CSV","Stats"),
            dropdown_font=("Ubuntu Mono",26),
            command=lambda event:self.dtOpt.configure(
                values=options[self.srcOpt.get()]
            )
        )

        self.srcOpt.place(
            relx=0.25,rely=0.35,
            anchor="center"
        )

        options = {
            "-source" : ("-nom",),
            "CSV": ("-local",),
            "Rdatasets" : tuple(items()),
            "Sci-kit" : ("iris","diabetes","digits","linnerud","wine","breast_cancer"),
            "Stats" : ('anes96', 'cancer', 'committee', 'ccard', 'copper', 'cpunish', 'elnino', 'engel', 'grunfeld', 'interest_inflation', 'longley', 'macrodata', 'modechoice', 'nile', 'randhie', 'scotland', 'spector', 'stackloss', 'star98', 'strikes', 'sunspots', 'fair', 'heart', 'statecrime', 'co2', 'fertility', 'china_smoking', 'danish_data')
        }

        self.dtOpt = ctk.CTkComboBox(
            self,
            width=0.2*master._current_width,
            height=60,
            font=("Ubuntu Mono",26),
            values=options[self.srcOpt.get()],
            dropdown_font=("Ubuntu Mono",26)
        )

        self.dtOpt.place(
            relx=0.5,rely=0.35,
            anchor="center"
        )
        self.srcOpt.update()
        self.dtOpt.configure(values=options[self.srcOpt.get()])


        self.__df = DataFrame()
        def __get_dataset():
            src = self.srcOpt.get()
            nom = self.dtOpt.get()
            text = ""
            match src:
                case '-source':
                    text = "Vous n'avez pas introduit le source"
                case 'Rdatasets':
                    if nom != '-nom':
                        self.__df = data(nom)
                        text = "Dataset enregistré"
                    else: text=f"Vous n'avez pas introduit\nun dataset de {src}"
                case 'Sci-kit':
                    if nom != '-nom':
                        self.__df = eval(f"skd.load_{nom}(as_frame=True).data")
                        text = "Dataset enregistré"
                    else: text=f"Vous n'avez pas introduit\nun dataset de {src}"
                case 'Stats':
                    if nom != '-nom':
                        self.__df = eval(f"stsd.{nom}.load_pandas().data")
                        text = "Dataset enregistré"
                    else:
                        text=f"Vous n'avez pas introduit\nun dataset de {src}"
                case 'CSV':
                    fp = filedialog.askopenfile("r")
                    if not fp:
                        text = f"Vous n'avez pas introduit\nun dataset sous forme de CSV"
                    else:
                        self.__df = read_csv(fp.name)
            with sqlite3.connect("data_tab.db") as conn:
                self.__df.to_sql("it",conn,if_exists="replace",index=False)
            self.resLb.configure(text=text)



        self.srcBtn = ctk.CTkButton(
            self,text="Importer",
            width=0.2*master._current_width,
            height=60,
            font=("Ubuntu Mono",26),
            command=__get_dataset
        )

        self.srcBtn.place(
            relx=0.75,rely=0.35,
            anchor="center"
        )

        def afficher_data():
            if not self.__df.empty:
                s = self.__df.to_dict("list")
                with open("aff_data.json","w") as f:
                    dump(s,fp=f,indent=4)
                
                open_new("aff_data.json")
            else:
                self.resLb.configure(
                    text="Aucun dataset affiché"
                )
                


        self.affBtn = ctk.CTkButton(
            self,
            text="Afficher comme dictionnaire",
            width=0.55*master._current_width,
            height=50,
            font=("Ubuntu Mono",26),
            command=afficher_data
        )

        self.affBtn.place(
            relx=0.5,rely=0.5,
            anchor="center"
        )

        def tracer_courbe():            
            app_ui = ui.page_fluid(
                ui.tags.h3("Requêtes (SQL)"),
                ui.div(
                    ui.input_text_area(
                        "query",label="Requêtes",
                        width="16cm",height="4cm"
                    ),
                    class_= "d-flex gap-3"
                ),
                ui.input_switch(
                    "swt",label = "Mélanger",
                    value=False
                ),
                
                ui.output_data_frame("my_widget"),
                ui.tags.br(),
                ui.tags.h3("Courbes"),
                ui.input_action_button("tracer","Tracer une courbe"),
                ui.div(
                    ui.input_selectize("Y",label="Colonnes Y",choices=[],multiple=True),
                    ui.input_selectize("X",label="Colonnes X",choices=[],multiple=False),
                    class_ = "d-flex gap-3"
                ),
                output_widget("plots")
            )

            def server(input_,output,session):

                df = reactive.Value(self.__df)
                async def logg():
                    master.destroy()
                    exit()
                    await app.stop()
                session.on_ended(logg)

                @output
                @render.data_frame
                @reactive.event(input_.query)
                def my_widget():
                    
                    with sqlite3.connect("data_tab.db") as conn:
                        s = input_.query()
                        try:
                            if s == "":raise
                            self.__df = read_sql_query(s,con=conn)
                        except:
                            self.__df = read_sql_query("select * from it",con=conn)
                    if input_.swt(): self.__df = self.__df.sample(frac=1)
                    df.set(self.__df)
                    return self.__df
                

                @output
                @render_widget
                @reactive.event(input_.tracer,input_.query)
                async def plots():
                    await asyncio.sleep(2)
                    ui.update_selectize(id="Y",label="Colonne Y",choices=[*df().columns])
                    ui.update_selectize(id="X",label="Colonne X",choices=[*df().columns])
                    fig = make_subplots(
                        specs=[[{"secondary_y":True}]],
                        x_title=input_.X()
                    )
                    for y in input_.Y():
                        g =  go.Scatter(
                            x = df()[input_.X()].sort_values(),y = df()[y].sort_values(),
                            mode="markers",
                            name=y
                        )
                        fig.add_trace(g)
                    fig.update_layout(height=600,width=900)
                    return fig
            
            app = App(ui=app_ui,server=server)
            app.run(launch_browser=True,port=8080)
            


        self.crbBtn = ctk.CTkButton(
            self,
            text="Tracer un graphe",
            width=0.55*master._current_width,
            height=50,
            font=("Ubuntu Mono",26),
            command=tracer_courbe
        )

        self.crbBtn.place(
            relx=0.5,rely=0.6,
            anchor="center"
        )

        self.prev_frame:ctk.CTkFrame

        def __retourner():
            self.forget()
            m = self.prev_frame(master=master)
            m.prev_frame = DataSect
        
        self.retBtn = ctk.CTkButton(
            self,
            text="Retourner",
            width=0.55*master._current_width,
            height=50,
            font=("Ubuntu Mono",26),
            command=__retourner
        )

        self.retBtn.place(
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


