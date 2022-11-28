from enum import Enum
from Client import *
from Serveur import *
from puissance4C import p4c
from puissance4C_IA import p4c_ia
from Score import *

class Menu:
    def __init__(self):
        class state(Enum):
            MENU = 1
            LOCAL = 2
            RESEAU = 3
            JVSJ = 4
            JVSIA = 5
            CLIENT = 7
            SERVEUR = 8
            ACCUEIL = 9
            HISTORIQUE = 10

        self.isRunning = True
        self.gameState = state.MENU
        self.gameState = self.gameState.ACCUEIL
        self.init_serveur = False
        self.init_client = False

    def start(self):
        while self.isRunning:
            if self.gameState == self.gameState.ACCUEIL:
                self.id = input("Entrez votre nom de joueur >> ")
                self.gameState = self.gameState.MENU

            elif self.gameState == self.gameState.MENU:
                st = int(input("--- Menu ---\n 1-Local\n 2-Réseau\n 3-Voir l'historique des parties\n 4-Quitter\n >> "))
                if st == 1:
                    self.gameState = self.gameState.LOCAL
                elif st == 2:
                    self.gameState = self.gameState.RESEAU
                elif st == 3:
                    self.gameState = self.gameState.HISTORIQUE
                elif st == 4:
                    break
                else:
                    print("Mauvaise saisie")
            elif self.gameState == self.gameState.HISTORIQUE:
                s = Score()
                s.start(self.id)
                self.gameState = self.gameState.MENU

            elif self.gameState == self.gameState.LOCAL:
                st = int(input("--- LOCAL ---\n 1-Joueur vs Joueur\n 2-Joueur vs IA\n 3-Retour\n >> "))
                if st == 1:
                    self.gameState = self.gameState.JVSJ
                elif st == 2:
                    self.gameState = self.gameState.JVSIA
                elif st == 3:
                    self.gameState = self.gameState.MENU
                else:
                    print("Mauvaise saisie")
            elif self.gameState == self.gameState.RESEAU:
                st = int(input("--- RESEAU ---\n 1-Rejoindre une partie\n 2-Heberger une partie\n 3-Retour\n >> "))
                if st == 1:
                    self.gameState = self.gameState.CLIENT
                elif st == 2:
                    self.gameState = self.gameState.SERVEUR
                elif st == 3:
                    self.gameState = self.gameState.MENU
                else:
                    print("Mauvaise saisie")
            elif self.gameState == self.gameState.JVSJ:
                p4c()
                self.gameState = self.gameState.MENU

            elif self.gameState == self.gameState.JVSIA:
                p4c_ia(self.id)
                self.gameState = self.gameState.MENU

            elif self.gameState == self.gameState.CLIENT:
                clientThread = Client(self.id)
                clientThread.start()
                while clientThread.is_alive():
                    pass

                self.gameState = self.gameState.MENU

            elif self.gameState == self.gameState.SERVEUR:
                self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.tcpsock.bind(("", 1111))

                self.tcpsock.listen(10)
                print("En attente de la connexion de l'autre joueur...")
                (clientsocket, (ip, port)) = self.tcpsock.accept()
                serverThread = Serveur(ip, port, clientsocket, self.id)
                serverThread.start()

                while serverThread.is_alive():
                    pass

                self.tcpsock.close()
                self.gameState = self.gameState.MENU

