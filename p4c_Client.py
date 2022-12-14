#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  puissance4C.py
#
#  Copyright 2019 Robert Sebille <robert@sebille.name>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

# An IA can implement this script with this:
# Input: choose a name, eg, "ordi" and return var col to play, when
# it's the "ordi" turn
# Output: convert_integer(grille) and teste_fin_jeu(res_gagnant, nom, matrice)

"""
    Puissance4C est un module puissance 4 en console et en couleur,
    à jouer à 2.
    Usage:
    from puissance4C import p4c
    p4c()
"""

import time
from Score import *

Csbr = "\033[1m"  # bright
# resets
Cbrs = "\033[49m"  # reset background
Cfrs = "\033[39m"  # reset foreground
Csrs = "\033[0m"  # reset all
# foreground
Cfw = "\033[37m"  # white
Cfy = "\033[33m"  # yellow
Cfba = "\033[30m"  # black
# background
Cby = "\033[43m"  # yellow
Cbw = "\033[47m"  # white
Cbbu = "\033[44m"  # blue
Cbr = "\033[41m"  # red
Cbba = "\033[40m"  # black
Cbg = "\033[42m"  # green
# clear the screen
Ccls = "\033[2J"


def ccxy2(x, y):  # position cursor at x across, y down
    return "\033[" + str(y) + ";" + str(x) + "f"


backsombre = [Cbba, Cbbu, Cbg]
pionjaune = Cby + Cfba + Csbr  # pion jaune
pionrouge = Cbr + Cfw + Csbr  # pion rouge
reset = Cbrs + Cfrs + Csrs
pionvide = Cbw + Cfw + Csbr
couljeu = Cbbu + Cfy + Csbr

delai = 1

# For debug
matrice0 = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]
# For debug
matrice_orig = [
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."]
]


###############
# Utilitaires #
###############
def _a(s, nb_blancs):
    return s + ' ' * (nb_blancs - len(s))


########################
# Recherche du gagnant #
########################
candidates = []  # globale


def gagnant(grille):
    def convert_integer(grille):
        """convertit la matrice des jetons en matrice numérique
        pour faciliter les analyses

        . = 0, "O" = +1, "X" = -1 """
        mat = []
        for i in range(6):
            mat.append([])
            for j in range(7):
                if grille[i][j] == ".":
                    mat[i].append(0)
                if grille[i][j] == "O":
                    mat[i].append(1)
                if grille[i][j] == "X":
                    mat[i].append(-1)
        return mat

    def qui_gagne(somme):
        """Détermine qui gagne en résultat des analyse de la matrice
        numérique"""

        if somme == -4:
            return "X", True
        elif somme == 4:
            return "O", True
        else:
            return None, False

    def candidate(liste):
        """Définit une liste de listes gagnantes potentiellement

        c-à-d de diagonales, colonnes ou rangées ayant + de 4
        ou - de -4 comme somme dans la matrice convertie en numérique.
        On les appelle ici listes candidates.
        """
        global candidates
        sompos = 0
        somneg = 0
        for i in liste:
            if i == -1:
                somneg += i
            if i == 1:
                sompos += i
        if sompos >= 4 or somneg <= -4:
            candidates.append(liste)

    def analyse_candidate(liste):
        """ Recois la liste des listes candidates

        Retourne -4/+4 = si il y a 1 liste gagnante
        (n'importe laquelle, la première)
        """
        somme = 0
        for i in range(1, len(liste)):
            if liste[i] != 0 and liste[i] == liste[i - 1]:
                if somme == 0:
                    somme += liste[i]
                somme += liste[i]
            else:
                if somme > -4 and somme < 4:
                    somme = 0
            if somme == -4 or somme == 4:
                break
            # print(liste, somme)
        return somme

    #################################
    # Core de la fonction gagnant() #
    #################################

    # calculs + aisés
    mat = convert_integer(grille)
    # print_mat(mat)
    res = None
    somme = 0

    ################################################################
    # Diag gagnantes (4): 20-53-26, 30-03-36                       #
    # Elles retournent directement si elles gagnent et qui gagnent #
    ################################################################
    somme = mat[2][0] + mat[3][1] + mat[4][2] + mat[5][3]
    retour = qui_gagne(somme)
    if retour[1]:
        return retour[0]
    somme = mat[5][3] + mat[4][4] + mat[3][5] + mat[2][6]
    retour = qui_gagne(somme)
    if retour[1]:
        return retour[0]
    somme = mat[3][0] + mat[2][1] + mat[1][2] + mat[0][3]
    retour = qui_gagne(somme)
    if retour[1]:
        return retour[0]
    somme = mat[0][3] + mat[1][4] + mat[2][5] + mat[3][6]
    retour = qui_gagne(somme)
    if retour[1]:
        return retour[0]

    ###################################################################
    # Listes candidates à gagner. Elles ont plus de 4 jetons chacunes #
    # On isole celle qui sont potentiellement gagnantes, moins de -4  #
    # plus de plus 4 dans la matrice numériques. On évite ainsi de    #
    # nombreux calculs.                                               #
    ###################################################################

    # Diag (5): 10-54, 02-46, 40-04, 52-16
    candidate([mat[1][0], mat[2][1], mat[3][2], mat[4][3], mat[5][4]])
    candidate([mat[0][2], mat[1][3], mat[2][4], mat[3][5], mat[4][6]])
    candidate([mat[4][0], mat[3][1], mat[2][2], mat[1][3], mat[0][4]])
    candidate([mat[5][2], mat[4][3], mat[3][4], mat[2][5], mat[1][6]])

    # Diag (6): 50-05, 51-06, 00-55, 01-56
    candidate([mat[5][0], mat[4][1], mat[3][2], mat[2][3], mat[1][4],
               mat[0][5]])
    candidate([mat[5][1], mat[4][2], mat[3][3], mat[2][4], mat[1][5],
               mat[0][6]])
    candidate([mat[0][0], mat[1][1], mat[2][2], mat[3][3], mat[4][4],
               mat[5][5]])
    candidate([mat[0][1], mat[1][2], mat[2][3], mat[3][4], mat[4][5],
               mat[5][6]])

    # Colonnes (6): 00-60, 01-61, 02-62, 03-63, 04-64, 05-65, 06-66
    for i in range(len(mat[0])):
        poub = []
        for j in range(len(mat)):
            poub.append(mat[j][i])
        candidate(poub)

    # Lignes (7): 00-06, 10-16, 20-26, 30-36, 40-46, 50-56, 60-66
    for i in mat:
        candidate(i)

    # print(candidates)
    ####################################################################
    # On a construit les listes candidates (hors diagonales gagnantes) #
    # on regarde si il y a un gagnant dans ces listes, et qui il est   #
    ####################################################################
    for i in candidates:
        somme = analyse_candidate(i)
        retour = qui_gagne(somme)
        if retour[1]:
            return retour[0]
    return res


##############
# Affichages #
##############
def print_mat(matrice):
    """Imprime la matrice sous forme numérique. Pour debug"""

    m = len(matrice)
    n = len(matrice[0])
    for i in range(m - 1, -1, -1):
        for j in range(n):
            print("%02d" % matrice[i][j], " ", end='')
        print()
    print("------------------------")


def print_mat_str(matrice):
    """Imprime la matrice du jeu """
    m = len(matrice)
    n = len(matrice[0])
    print(ccxy2(0, 0) + Ccls, end='')
    print(couljeu + "··+", "+" * 28, "··", sep='')
    print("··|****** [PUISSANCE 4] ******|··")
    print("··C 1 | 2 | 3 | 4 | 5 | 6 | 7 |··")
    print("·/+", "---+" * 7, "\\·", sep='')
    for i in range(m - 1, -1, -1):
        print("·||", sep='', end='')
        for j in range(n):
            caractere = ' ' + matrice[i][j] + ' '
            if caractere == ' . ':
                caractere = pionvide + caractere + couljeu
            if caractere == ' O ':
                caractere = pionjaune + caractere + couljeu
            if caractere == ' X ':
                caractere = pionrouge + caractere + couljeu
            if j == n - 1:
                print(caractere, "|", sep='', end='')
            else:
                print(caractere, "|", sep='', end='')

        print("|·")
        print("·|+", "---+" * 7, "|·", sep='')
    # print("  /+", "---+"*7, "\\" + reset, sep='')
    print("/ C 1 | 2 | 3 | 4 | 5 | 6 | 7 | \\")
    print("|-+", "---+" * 7, "-|", sep='')
    print("+", "-" * 31, "+", sep='')


###############################
# Place un pion sur la grille #
###############################
def placer_pion(couleur, colonne, grille):
    """Place un pion sur la grille

    retourne un tuple (True/False si le placement du pion était
    possible, la grille modifiée ou pas)"""

    jeu = False
    i = -1
    while i < 5:
        i += 1
        if grille[i][colonne] == ".":
            grille[i][colonne] = couleur
            jeu = True
            i = 5
    return jeu, grille


def teste_fin_jeu(res_gagnant, nom1, nom2, data, matrice):
    """Si il y a un gagnant, stoppe le programme après avoir
    printé le gagnant"""

    if res_gagnant == "X" or res_gagnant == "O":
        print_mat_str(matrice)
        print()
        print("*********************************")
        print("* Le grand gagnant du jeu est : *")
        print("*********************************")
        print()
        if data[1] == 1:
            print(">>> " + nom1[0] + " avec 4 " + nom1[1] + " ! <<<\n")
        else:
            print(">>> " + nom2[0] + " avec 4 " + nom2[1] + " ! <<<\n")
        return True


def add_score(nom1, nom2, winner):
    s = Score()
    if nom1[1] == winner:
        s.add_winner(nom1[0], nom2[0], 1)
    else:
        s.add_winner(nom1[0], nom2[0], 2)


def send(self, data):
    data = str(data)
    self.clientsocket.send((data.encode()))


def receive(self):
    data = self.clientsocket.recv(2048).decode()
    data = eval(data)
    return data


#############################################################################################
#                                               JEU                                         #
#############################################################################################
def p4c(self, idServer, idClient, isServer):
    """Lance le jeu"""
    data = ["wait", "O", "0"]

    matrice = [
        [".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "."]
    ]

    print_mat_str(matrice)

    nom1 = [idServer]
    nom2 = [idClient]

    nom1.append("X")
    nom2.append("O")

    nom = nom2

    message_fin = "\n\nAu revoir, " + \
        nom1[0] + " et " + nom2[0] + ",\nà bientôt !"
    joue = True
    print(nom1[0], " Commence")

    while joue:
        # print("data[0] :", data[0], " data[1] :", data[1])
        if data[0] == "client":
            if data[1] != "0":
                mat = placer_pion(nom1[1], int(data[1]) - 1, matrice)
                matrice = mat[1]
                data[1] = "0"

            print_mat_str(matrice)

            col = ""
            while col not in ["1", "2", "3", "4", "5", "6", "7", "f", "F"]:
                col = input("Quelle colonne 1-7 joues-tu, " + nom[0] + " ? ")
                if col.lower() == "f":
                    print(reset + message_fin)
                    joue = False
                    break

            mat = placer_pion(nom[1], int(col) - 1, matrice)
            matrice = mat[1]

            if gagnant(matrice) == "O":
                data[0] = "gagnant"
                data[1] = "2"
                data[2] = col
                send(self, data)
            else:
                if mat[0]:
                    print_mat_str(matrice)
                    print("Au tour de " + nom1[0])
                    data[0] = "server"
                    data[1] = col
                    send(self, data)
                    data[0] = "wait"
                else:
                    print("Impossible de jouer cette colonne, " +
                          nom[0] + ", elle est pleine.")
                    time.sleep(delai)

        elif data[0] == "gagnant":
            if teste_fin_jeu(gagnant(matrice), nom1, nom2, data, matrice):

                print("Attendre que ", nom1[0],
                      "lance ou non une autre partie")
                data[0] = "wait"
            else:
                mat = placer_pion(nom1[1], int(data[2]) - 1, matrice)
                matrice = mat[1]

        elif data[0] == "wait":
            data = receive(self)
        elif data[0] == "exit":
            print(reset + message_fin)
            joue = False
        elif data[0] == "newGame":
            matrice = [
                [".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", "."]
            ]
            data[0] = "client"
            data[1] = "0"
            data[2] = "0"
