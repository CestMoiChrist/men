import csv


class Score:
    def __init__(self):
        self.fieldnames = ['Id_Joueur1', 'Nb_win_j1', 'Nb_win_j2', "Id_Joueur2"]

    def print_historique_score_joueur(self, joueur):
        matchup = False
        print("Historique de partie du joueur :", joueur)

        with open("Scores/score.csv", "r") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            for line in csv_reader:
                if line['Id_Joueur1'] == joueur or line['Id_Joueur2'] == joueur:
                    matchup = True
                    print(line['Id_Joueur1'],line['Nb_win_j1'], "-", line['Nb_win_j2'], line['Id_Joueur2'])

            print('\n')
            csv_file.close()
        if matchup == False :
            print("Aucune partie n'a été trouvé pour ce joueur")

    def print_score_joueurs(self, joueur1, joueur2):
        matchup = False
        print("Historique de partie de ", joueur1, " contre ", joueur2)
        with open("Scores/score.csv", "r") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")

            for line in csv_reader:
                if line['Id_Joueur1'] == joueur1 and line['Id_Joueur2'] == joueur2:
                    matchup = True
                    print(line['Id_Joueur1'],line['Nb_win_j1'], "-", line['Nb_win_j2'], line['Id_Joueur2'])

            csv_file.close()
        if matchup == False:
            print("Aucune partie n'a été joué contre ce joueur")

    def add_winner(self, joueur1, joueur2, winner):
        new_list = list()
        matchup = False
        with open("Scores/score.csv", "r+") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")# , ['id_j1','pt_j1', 'pt_j2', 'id_j2'])
            for line in csv_reader:

                if line['Id_Joueur1'] == joueur1 and line['Id_Joueur2'] == joueur2:
                    if winner == 1:
                        new_line = {'Id_Joueur1': joueur1, 'Nb_win_j1': int(line['Nb_win_j1'])+1,'Nb_win_j2': line['Nb_win_j2'], 'Id_Joueur2': joueur2}
                    else:
                        new_line = {'Id_Joueur1': joueur1, 'Nb_win_j1': line['Nb_win_j1'], 'Nb_win_j2': int(line['Nb_win_j2'])+1, 'Id_Joueur2': joueur2}
                    matchup = True
                elif line['Id_Joueur1'] == joueur2 and line['Id_Joueur2'] == joueur1:
                    if winner == 1:
                        new_line = {'Id_Joueur1': joueur2, 'Nb_win_j1': line['Nb_win_j1'], 'Nb_win_j2': int(line['Nb_win_j2'])+1, 'Id_Joueur2': joueur1}
                    else:
                        new_line = {'Id_Joueur1': joueur1, 'Nb_win_j1': int(line['Nb_win_j1'])+1, 'Nb_win_j2': line['Nb_win_j2'], 'Id_Joueur2': joueur2}
                    matchup = True
                else:
                    new_line = {'Id_Joueur1': line['Id_Joueur1'], 'Nb_win_j1': line['Nb_win_j1'], 'Nb_win_j2': line['Nb_win_j2'], 'Id_Joueur2': line['Id_Joueur2']}

                new_list.append(new_line)

            if matchup == False:
                new_line = {'Id_Joueur1': joueur1, 'Nb_win_j1': 1 , 'Nb_win_j2': 0, 'Id_Joueur2': joueur2}
                new_list.append(new_line)

            csv_file.close()

        with open("Scores/score.csv", "w") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writeheader()
            for l in new_list:
                csv_writer.writerow(l)
            csv_file.close()

    def start(self, id):
        run = True
        while run:
            print("--- Historique des scores de ", id," ---")
            st = int(input(" 1-Voir mon historique complet\n 2-Voir mon historique contre un certain joueur\n 3-Quitter\n >> "))
            if st == 1:
                self.print_historique_score_joueur(id)
            elif st == 2:
                id2 = input(" Entrez le nom d'un joueur >>")
                self.print_score_joueurs(id, id2)
            elif st == 3:
                run = False