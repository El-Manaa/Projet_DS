# Projet_cred_jeu
Cette application contient ces pages:<br>
&emsp;1- Enregistement et authentification<br>
&emsp;&emsp;a - S'enregistrer en introduisant l'email et le mot de passe et les enregistrer dans le fichier _Enregistrements.txt_.<br>
&emsp;&emsp;b - S'authentifier en introduisant l'email et le mot de passe, mais cette fois il les cherche dans le même fichier _Enregistrements.txt_. Si les données sont trouvées alors le programme déclanche le jeu; sinon il affiche que les données sont érronés et il faut s'enregistrer.<br><br>
&emsp;2- Menu des jeux:<br>
&emsp;&emsp;a- Jeu d'Hachage :<br>
&emsp;&emsp;&emsp;Entrer un mot puis l'hacher avec la fonction sha256 ou l'attaquer par dictionnaire<br>
&emsp;&emsp;b- Jeu de César :<br> 
&emsp;&emsp;&emsp;Entrer un mot avec un clé et un mode de chiffrement ou de déchiffrement (ASCII ou Lettres alphabétiques)<br>
&emsp;&emsp;c- Jeu des Données:<br>
&emsp;&emsp;&emsp;D'abord on choisit le source d'un dataset puis son nom et on l'importe.<br>
&emsp;&emsp;&emsp;&emsp;Sources : Rdatasets, Sci-kit et CSV.<br>
&emsp;&emsp;&emsp;i - _Affichage du dataset_ sous le format __JSON__.<br>
&emsp;&emsp;&emsp;ii - _Traçage d'une courbe_ dans une page web créée avec __Shiny__ (avec Python et pas avec ~~R~~) en intégrant la création des courbes avec __Plotly__. On peut aussi faire des requêtes avec SQL tant que le dataset/dataframe est enregistré dans un fichier de base des données intitulé **data_tab.db**.<br>
&emsp;&emsp;&emsp;


Le **Programme Principal** est: app.py

