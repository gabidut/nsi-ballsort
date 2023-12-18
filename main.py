
"""

Notice d'installation : 

- Installer le module pynput avec la commande suivante : pip install pynput

Notice d'execution :

- Executer le fichier game.py avec la commande suivante : python game.py DEPUIS UN TERMINAL. Ne pas executer dans l'interpréteur edupython.

"""


"""

Fonctions du Jeu :

    startgame() : Boucle principale du jeu où le joueur peut saisir des commandes (sel, move, dump) pour interagir avec l'état du jeu.
    checkwin() : Vérifie si le joueur a gagné en correspondant aux motifs.
    moveTube(dest) : Déplace des éléments entre les tubes.
    selectTube(tube) : Sélectionne un tube pour des actions ultérieures.
    generateGameStat(size) : Génère l'état initial du jeu avec un niveau de difficulté spécifié.

Graphiques et Interface :

    Les codes d'échappement ANSI sont utilisés pour imprimer du texte coloré pour une interface graphique basique.
    clearScreen() : Fonction pour effacer l'écran de la console.
    drawMain(), drawOptions(), drawUsernameChange(), drawGame() : Fonctions pour dessiner différentes interfaces en fonction de l'état du jeu.
    reverseList(list) : Inverse une liste.
    pad_list(lst) : S'assure qu'une liste a au moins 4 éléments en les remplissant avec des chaînes vides.

    
Gestion de l'Entrée Clavier :

    on_press(key) : Fonction pour gérer l'entrée clavier. Différentes actions sont effectuées en fonction des touches pressées, telles que la sélection de tubes, le déplacement d'éléments, l'affichage de l'aide, etc.
Boucle du Jeu :

    Boucle infinie vérifiant continuellement les entrées clavier et mettant à jour l'état du jeu en conséquence.
    Mises à jour périodiques de l'écran pour refléter les changements.


"""


import random
import pynput
import os


"""

'gamedata' est une liste qui va contenir les différentes informations du jeu
- Pseudo
- Difficulté
- Bouton sélectionné
- Tubes
...

"""
gamedata = []

COLORS = ("blue", "red")

in_game = True

winpatterns = []

"""

Ici, initialisation des paramètres de base.

"""

def startgame():
    for k in range(len(COLORS)):
        winpatterns.append([COLORS[k],COLORS[k],COLORS[k]])
    while in_game:
        lastaction = input("Action ?")
        lastaction = lastaction.split(" ")
        if (lastaction[0] == "sel"):
            # if is as pasable number
            if (lastaction[1].isdigit()):
                selectTube(lastaction[1])
            else:
                print("Error: Tube must be a number")
        elif (lastaction[0] == "move"):
            moveTube(lastaction[1])
        elif (lastaction[0] == "dump"):
            print(gamedata)


"""
Vérification simple de la victoire du joueur en fonction des patterns de victoire générés préalablement.
"""
def checkwin():
    nbOkay = 0
    for win_pattern in winpatterns:
        if win_pattern in gamedata[2]:
            nbOkay+=1
    if(nbOkay == 2):
        clearScreen()
        print("Congratulations! You have won the game!")
        exit()


"""
Passage d'un tube à un autre
"""
def moveTube(dest):
    checkwin()
    tube = int(dest)
    if (tube < 0 or tube > 2):
        print("Error: Tube must be between 0 and 2")
        return
    if (gamedata[3] == ""):
        print("Error: Tube not selected")
        return

    if (gamedata[3] == tube):
        print("Error: Cannot move to same tube")
        return
    print(gamedata[2][tube])
    if (gamedata[2][tube][-1] != ""):
        print("Error: Tube is full")
        return
    targetColor = gamedata[2][gamedata[3]][len(gamedata[2][gamedata[3]]) - 1]
    gamedata[2][gamedata[3]].pop(len(gamedata[2][gamedata[3]]) - 1)
    gamedata[2][tube].append(targetColor)

    #

    print(targetColor)

"""
Sélection d'un tube
"""

def selectTube(tube):
    tube = int(tube)
    if (tube < 0 or tube > 2):
        print("Error: Tube must be between 0 and 2")
        return
    if (str(tube) != gamedata[3]):
        target = gamedata[2][tube]
        if (target == []):
            print("Error: Tube is empty")
            return

        gamedata[3] = tube
        print("Tube selected")
    else:
        print("Error: Tube already selected")


"""
Génération aléatoire des tubes
"""

def generateGameStat(size):
    assert 0 < size <= 5, "Size must be between 1 and 5"

    if size == 3:
        tlist = [
            [], [], []
        ]

        colorsToAdd = [["blue", 3], ["red", 3]] # Système de répartition des couleurs, ici : 3 bleus et 3 rouges.

        k = 0
        while (colorsToAdd[0][1] != 0 or colorsToAdd[1][1] != 0):
            for i in range(0, 3):
                rand = random.randint(0, 1)
                if (colorsToAdd[rand][1] != 0):
                    tlist[k].append(colorsToAdd[rand][0])
                    colorsToAdd[rand][1] -= 1
                else:
                    tlist[k].append(colorsToAdd[1 - rand][0])
                    colorsToAdd[1 - rand][1] -= 1
            k += 1
        ## check if first list equals second list
        if (tlist[1] == tlist[2]):
            print("Avoid BornWin")
            return generateGameStat(3)
    return tlist


# startgame()

"""

GRAPHICS

"""

red = "\033[31m"
blue = "\033[34m"
white = "\033[37m"
yellow = '\033[33m'
black = "\033[30m"
green = "\033[32m"
yellow = "\033[33m"
purple = "\033[35m"
cyan = "\033[36m"

colors = {"red": "\033[31m", "blue": "\033[34m", "white": "\033[37m", "yellow": "\033[33m", "black": "\033[30m",
          "green": "\033[32m", "purple": "\033[35m", "cyan": "\033[36m"}

from os import system

"""

Cette fonction permet de clear le terminal, de sorte à ce que les prints affichées ne défilent pas,
mais donnent une impression de continuité et de fluiditié.

"""

def clearScreen():
    if os.name == "nt":
        system("cls")
    else:
        system("clear")


from time import *

lastState = ""
state = "main"
selected = 0
isInit = False
debug = False
username = ""

"""

Cette fonction permet d'afficher l'écran de démarrage. L'écran principal.
Il contient trois boutons à savoir : Start (démarrer), Options (options), Quit (quitter)

"""

def drawMain():
    # On supprime l'écran entier pour cette impression de nouvelle fenêtre.
    clearScreen()
    print("+---------------------------------------------------------+")
    print("|                                                         |")
     # Si le bouton "Start" est sélectionné, on affiche le texte en souligné
    if (gamedata[6] == 0):
        print("|                     \033[4mStart\033[0m                               |")
    else:
        print("|                     Start                               |")
    print("|                                                         |")
    if (gamedata[6] == 1):
        print("|                     \033[4mOptions\033[0m                             |")
    else:
        print("|                     Options                             |")
    print("|                                                         |")
    if (gamedata[6] == 2):
        print("|                     \033[4mQuit\033[0m                                |")
    else:
        print("|                     Quit                                |")
    print("|                                                         |")
    print("|                                                         |")
    print("+---------------------------------------------------------+")

ainput = False

"""

Cette fonction est très utile puisqu'elle nous permet d'afficher les écrans sans avoir à
chercher à chaque fois laquelle afficher. L'écran est stocké dans le fameux 'gamedata'.

"""
def drawScreen():
    if (gamedata[5] == "main"):
        drawMain()
    elif (gamedata[5] == "game"):
        drawGame()
    elif (gamedata[5] == "username-change"):
        drawUsernameChange()
    elif (gamedata[5] == "options"):
        drawOptions()

""" Fonction qui affiche l'écran de changement de pseudo """

def drawUsernameChange():
    clearScreen()
    gamedata[7] = ''
    print(gamedata[5])
    gamedata[7] = input("> Veuillez choisir votre nouveau pseudo : ")
    gamedata[5] = "main"

""" Fonction qui affiche les réglages du jeu """

def drawOptions():
    clearScreen()
    print("+---------------------------------------------------------+")
    print("|                                                         |")
    # À chaque fois, on viendra vérifier si le bouton est sélectionné ou non, et on affichera le texte souligné ou non en conséquence.
    if gamedata[0] == 0:
        if gamedata[6] == 0:
            print("| \033[4mDifficulté : " + green + "Facile\033[0m " + white + "                                    |")
        else:
            print("| Difficulté : " + green + "Facile    " + white + "                                 |")
    elif gamedata[0] == 1:
        if gamedata[6] == 0:
            print(
                "| \033[4mDifficulté : " + yellow + "Moyen\033[0m    " + white + "                                  |")
        else:
            print("| Difficulté : " + yellow + "Moyen" + white + "                                      |")
    elif gamedata[0] == 2:
        if gamedata[6] == 0:
            print("| \033[4mDifficulté : " + red + "Difficile\033[0m " + white + "                                 |")
        else:
            print("| Difficulté : " + red + "Difficile    " + white + "                              |")
    if gamedata[6] != 1:
        print("| Changer de pseudo                                       |")
    else:
        print("| \033[4mChanger de pseudo\033[0m                                       |")
    if gamedata[6] != 2:
        print("| Couleur des tubes :", colors[tubecolor], tubecolor, white, "                             |")
    else:
        print("| \033[4mCouleur des tubes :", colors[tubecolor], tubecolor, white,
              "\033[0m                             |")

    if(gamedata[6] != 3):
        print("| Quitter les options                                     |")
    else: 
        print("| \033[4mQuitter les options\033[0m                                     |")
    print("|                                                         |")
    print("+---------------------------------------------------------+")

# Fonction qui renverse une liste

def reverseList(list):
    newList = []
    for i in range(len(list) - 1, -1, -1):
        newList.append(list[i])
    return newList

# Fonction expliquée dans le préambule.
def pad_list(lst):
    while len(lst) < 4:
        lst.append("")
    return lst

word = ""
def drawGame():
    clearScreen()
    print( green + "> Tapez 'help' pour afficher l'aide" + white)
    print("+----------------------------------------------------------+")
    line = ""

    for i in range(0,4):
        line += "|    "
        for k in range(3):
            temp = pad_list(gamedata[2][k])
            temp = reverseList(temp)

            if temp[i] == "":
                line += white + "|   |" + white + "      "
            elif temp[i] == "red":
                line += red + "| x |" + white + "      "
            elif(temp[i] == "blue"):
                line += blue + "| x |" + white + "      "
        if(not i == 3):
            line += "                     |\n"
        else:
            line += "                     |"

    print(line)
    print(white, "|    {colors[tubecolor]}+---+      +---+      +---+",white,"                           |")
    print("| " + word + " " * (56 - len(word)) + " |")
    print(white,"+----------------------------------------------------------+\n")

"""

Fonction qui fonctionne grâce à un Listener. Elle vient permettre
au jeu d'écouter les pressions de touches du clavier.

C'est la pièce maîtresse du jeu, puisque c'est grâce à elle que le jeu peut être joué.

"""
def on_press(key):
    global word
    # print("Key pressed: " + str(key))
    if gamedata[5] == "game":
        try:
            word += key.char
            drawScreen()
        except AttributeError:
            if(str(key) == "Key.backspace"):
                word = word[:-1]
                drawScreen()

            if(str(key) == "Key.space"):
                word += " "
            if(str(key) == "Key.enter"):
                tword = word.split(" ")
                word = ""
                if(tword[0] == "sel"):
                    if(tword[1].isdigit()):
                        selectTube(tword[1])
                        drawScreen()
                        print("Selected tube " + tword[1])
                    else:
                        print("Error: Tube must be a number")
                if(tword[0] == "move"):
                    moveTube(tword[1])
                    drawScreen()
                    print("Moved to tube " + tword[1])
                if(tword[0] == "dump"):
                    print(gamedata)
                    print(COLORS)
                if(tword[0] == "exit"):
                    gamedata[5] = "main"
                    drawScreen()

                if(tword[0] == "help"):
                    print("Commandes disponibles : ")
                    print("sel <tube> : Selectionne un tube")
                    print("move <tube> : Déplace le contenu du tube sélectionné vers le tube spécifié")
                    print("dump : Affiche les données du jeu (attention, la solution est affichée dans les données du jeu !)")
                    print("exit : Quitte le jeu")
            
            # print('special key {0} pressed'.format(
            # key))
        """
    On va aussi regarder la pression des touches pour le menu 'options'
    => Ils sont différents pour éviter de superposer des intéractions.
    """
    if gamedata[5] == "options":
                    """
            
            Les touches gauches et droites sont vérifiées afin de changer la difficulté du jeu,
            uniquement lorsque l'on sélectionne le bouton 'difficulté'
            
            """
        if gamedata[6] == 0:
            clearScreen()
            drawScreen()
            if (str(key) == "Key.left"):
                gamedata[0] -= 1
                if gamedata[0] < 0:
                    gamedata[0] = 2
                drawScreen()

            if (str(key) == "Key.right"):
                gamedata[0] += 1
                if gamedata[0] > 2:
                    gamedata[0] = 0
                drawScreen()
        if str(key) == "Key.up":
            gamedata[6] -= 1
            if gamedata[6] < 0:
                gamedata[6] = 3
            drawScreen()
        if str(key) == "Key.down":
            gamedata[6] += 1
            if gamedata[6] > 3:
                gamedata[6] = 0
            drawScreen()
        if str(key) == "Key.enter":
            if gamedata[6] == 1:
                gamedata[5] = "username-change"
                drawScreen()
            if(gamedata[6] == 3):
                gamedata[5] = "main"
                drawScreen()
    """
    Même chose qu'au-dessus mais pour le menu principal et de façon déstructurée
    """
    if (str(key) == "Key.up"):
        if (gamedata[5] == "main"):
            gamedata[6] -= 1
            if gamedata[6] < 0:
                gamedata[6] = 2
        elif (gamedata[5] == "game"):
            pass
        drawScreen()
    # if key is escape
    if(str(key) == "Key.esc"):
        exit()
    if (str(key) == "Key.down"):
        if (gamedata[5] == "main"):
            gamedata[6] += 1
            if gamedata[6] > 2:
                gamedata[6] = 0
        elif (gamedata[5] == "game"):
            pass
        drawScreen()
    # if ctrl + c 
#    if (str(key) == "Key.ctrl_l"):      

            # Selon le bouton sélectionné on va afficher un certain menu.
            # gamedata[6] == 0 correspond à "Start"
            # gamedata[6] == 1 correspond à "Options"
            # gamedata[6] == 2 correspond à "Quit"
    if (str(key) == "Key.enter"):
        if (gamedata[5] == "main"):
            if (gamedata[6] == 0):
                gamedata[5] = "game"
                clearScreen()
                drawScreen()
            if gamedata[6] == 1:
                gamedata[5] = "options"
                gamedata[6] = 0
                clearScreen()
                drawScreen()
            elif (gamedata[6] == 2):
                clearScreen()
                print(red + "> Fermeture du jeu." + white)
                exit()
                
        elif (gamedata[5] == "game"):
            pass



"""

Boucle infinie qui permet de faire tourner le jeu. :D
Cette fois-ci elle est intentionnelle, et non pas une erreur de programmation.

"""
while True:

    if (not isInit):
                """
        Mise en place des différentes variables qui seront stockées dans 'gamedata'
        
        isInit
        difficulty pour la difficulté
        tubecolor pour la couleur des tubes
        username pour le pseudo fonctionnant grâce à un input
        
        Le tout est rentré dans la liste 'gamedata'
        
        Enfin, on draw le screen pour afficher l'écran principal.
        
        """
        isInit = True
        difficulty = 0
        tubecolor = "blue"
        clearScreen()
        username = input("> Entrez un pseudonyme : ")
        gamedata.extend([difficulty, tubecolor, generateGameStat(3), "", "", state, selected, username])
        drawScreen()
    if (lastState != gamedata[5] and debug == False):
        clearScreen()
        lastState = gamedata[5]
        print("State changed to " + gamedata[5])
        drawScreen()
    current_milli_time = int(round(time() * 1000))

    with pynput.keyboard.Listener(
            on_press=on_press,
    ) as listener:
        listener.join()
    if (current_milli_time % 100 == 0 and debug == False):
        drawScreen()

