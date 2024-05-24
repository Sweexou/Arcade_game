import pygame
from button_menu import Button

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

pygame.joystick.init()


class Menu:
    selected_index = 0
    player1_position = (0, 0)
    player2_position = (0, 0)
    last_player1_position = (0, 0)
    last_player2_position = (0, 0)
    current_player = 1
    player1_pseudo = ""
    player2_pseudo = ""

    def main_menu(self, screen, selected_option):
        buttons = self.create_buttons(["PLAY", "LEADERBOARD", "QUIT"], screen)
        self.render_buttons(screen, buttons, selected_option)
        


    def play_menu(self, screen):
        alphabet = [["A", "B", "C", "D", "E", "F", "G", "H", "I"], ["J", "K", "L", "M", "N", "O", "P", "Q", "R"],
                    ["S", "T", "U", "V", "W", "X", "Y", "Z", "←"]]

        buttons = self.create_alphabet_buttons(alphabet, screen)
        
        # Rendre les boutons des lettres de l'alphabet
        self.render_alphabet_buttons(screen, buttons)

        # Afficher les zones des pseudos des joueurs
        self.render_player_pseudo_boxes(screen)

        # Gérer les événements
        selected_option = self.handle_alphabet_events(buttons)

        return selected_option
    


    def classe_menu(self, screen):
        alphabet = [["Assassin", "Sniper", "Soldat", "Tank"]]

        buttons = self.create_classes_buttons(alphabet, screen, width=0, height=50, margin=250)
        
        self.render_alphabet_buttons(screen, buttons)
        
        self.render_player_pseudo_boxes(screen)

        selected_option = self.handle_classes_events(buttons)

        return selected_option

    def render_player_pseudo_boxes(self, screen):
        # Définir les dimensions et les positions des rectangles
        rect_width = 400
        rect_height = 50
        margin = 300

        player1_rect_x = (screen.get_width() - rect_width) // 2 - 300
        player1_rect_y = margin

        player2_rect_x = (screen.get_width() - rect_width) // 2 + 300
        player2_rect_y = margin

        # Dessiner les rectangles blancs
        pygame.draw.rect(screen, (255, 255, 255), (player1_rect_x, player1_rect_y, rect_width, rect_height))
        pygame.draw.rect(screen, (255, 255, 255), (player2_rect_x, player2_rect_y, rect_width, rect_height))

        # Définir la couleur du texte (noir pour contraste)
        text_color = (0, 0, 0)

        # Rendre les pseudos des joueurs
        font = get_font(30)
        player1_text = font.render(self.player1_pseudo, True, text_color)
        player2_text = font.render(self.player2_pseudo, True, text_color)

        # Afficher le texte des pseudos dans les rectangles
        screen.blit(player1_text,
                    (player1_rect_x + 10, player1_rect_y + (rect_height - player1_text.get_height()) // 2))
        screen.blit(player2_text,
                    (player2_rect_x + 10, player2_rect_y + (rect_height - player2_text.get_height()) // 2))

        # Dessiner les étiquettes "Player 1" et "Player 2"
        label_font = get_font(24)
        player1_label_text = label_font.render("Player 1", True, "Purple")
        player2_label_text = label_font.render("Player 2", True, "Green")

        # Positionner les étiquettes au-dessus des rectangles
        player1_label_x = (screen.get_width() - rect_width) // 2 - 300
        player1_label_y = player1_rect_y - 30

        player2_label_x = (screen.get_width() - rect_width) // 2 + 300
        player2_label_y = player2_rect_y - 30

        # Afficher les étiquettes
        screen.blit(player1_label_text, (player1_label_x, player1_label_y))
        screen.blit(player2_label_text, (player2_label_x, player2_label_y))


    def render_alphabet_buttons(self, screen, buttons):
        for row in buttons:
            for button in row:
                if button.grid_pos == self.player1_position:
                    button.base_color = "Violet"  # Couleur violette pour le joueur 1
                elif button.grid_pos == self.player2_position:
                    button.base_color = "Green"  # Couleur verte pour le joueur 2
                else:
                    button.base_color = "White"  # Couleur par défaut
                button.update(screen)
                
    def create_classes_buttons(self, alphabet, screen, width=50, height=50, margin=30):
        buttons_key = []
        button_width = width
        button_height = height
        margin = margin

        # Calculer le nombre de colonnes nécessaire pour afficher les boutons en fonction de la longueur de l'alphabet
        num_cols = len(alphabet[0])
        
        # Calculer la largeur totale occupée par les boutons et les marges
        total_width = num_cols * (button_width + margin) - margin

        # Position x pour centrer les boutons horizontalement
        start_x = (screen.get_width() - total_width) // 2  

        # Position y pour centrer les boutons verticalement
        start_y = (screen.get_height() - (len(alphabet) * (button_height + margin))) // 2  

        for row_index, row in enumerate(alphabet):
            button_row = []
            for col_index, letter in enumerate(row):
                x = start_x + col_index * (button_width + margin)

                button = Button(image=pygame.image.load("assets/CLASSE_Rect.png"), pos=(x, 500), text_input=letter,
                                font=get_font(30), base_color="White", selected_color="Green", hovering_color="Green",
                                grid_pos=(row_index, col_index))  # Assign grid position
                button_row.append(button)
            buttons_key.append(button_row)

        # Ajouter le bouton "BACK" à la liste des boutons de l'alphabet
        back_button_width = 200
        back_button_height = 50
        back_button_x = (screen.get_width() - back_button_width) // 2 - 100  # Légèrement à gauche du centre
        back_button_y = screen.get_height() - back_button_height - 20  # En bas de l'écran avec une petite marge
        back_button = Button(image=pygame.image.load("assets/BACK_Rect.png"),
                            pos=(back_button_x, back_button_y),
                            text_input="BACK", font=get_font(30), base_color="White", selected_color="Green",
                            hovering_color="Green", grid_pos=(3, 0))

        continue_button_width = 200
        continue_button_height = 50
        continue_button_x = (screen.get_width() - continue_button_width) // 2 + 300  # Légèrement à droite du centre
        continue_button_y = screen.get_height() - continue_button_height - 20  # En bas de l'écran avec une petite marge
        continue_button = Button(image=pygame.image.load("assets/CONTINUE_Rect.png"),
                                pos=(continue_button_x, continue_button_y),
                                text_input="CONTINUE", font=get_font(30), base_color="White", selected_color="Green",
                                hovering_color="Green", grid_pos=(3, 1))

        buttons_key.append(
            [back_button, continue_button])  # Ajouter les boutons "BACK" et "CONTINUER" à la fin de la liste
        return buttons_key



    def create_alphabet_buttons(self, alphabet, screen, width = 50, height = 50, margin = 20):
        buttons_key = []
        button_width = width
        button_height = height
        margin = margin
        start_x = (screen.get_width() - (
                9 * (button_width + margin))) // 2  # Position x pour centrer les boutons horizontalement
        start_y = (screen.get_height() - (
                3 * (button_height + margin))) // 2  # Position y pour centrer les boutons verticalement

        for row_index, row in enumerate(alphabet):
            button_row = []
            for col_index, letter in enumerate(row):
                x = start_x + col_index * (button_width + margin)
                y = start_y + row_index * (button_height + margin)
                button = Button(image=pygame.image.load("assets/LETTER_Rect.png"), pos=(x, y), text_input=letter,
                                font=get_font(30), base_color="White", selected_color="Green", hovering_color="Green",
                                grid_pos=(row_index, col_index))  # Assign grid position
                button_row.append(button)
            buttons_key.append(button_row)

        # Ajouter le bouton "BACK" à la liste des boutons de l'alphabet
        back_button_width = 200
        back_button_height = 50
        back_button_x = (screen.get_width() - back_button_width) // 2 - 100  # Légèrement à gauche du centre
        back_button_y = screen.get_height() - back_button_height - 20  # En bas de l'écran avec une petite marge
        back_button = Button(image=pygame.image.load("assets/BACK_Rect.png"),
                             pos=(back_button_x, back_button_y),
                             text_input="BACK", font=get_font(30), base_color="White", selected_color="Green",
                             hovering_color="Green", grid_pos=(3, 0))

        continue_button_width = 200
        continue_button_height = 50
        continue_button_x = (screen.get_width() - continue_button_width) // 2 + 300  # Légèrement à droite du centre
        continue_button_y = screen.get_height() - continue_button_height - 20  # En bas de l'écran avec une petite marge
        continue_button = Button(image=pygame.image.load("assets/CONTINUE_Rect.png"),
                                 pos=(continue_button_x, continue_button_y),
                                 text_input="CONTINUE", font=get_font(30), base_color="White", selected_color="Green",
                                 hovering_color="Green",grid_pos=(3, 1))

        buttons_key.append(
            [back_button, continue_button])  # Ajouter les boutons "BACK" et "CONTINUER" à la fin de la liste
        return buttons_key
    
    def handle_classes_events(self, buttons):
        rows = len(buttons)
        cols = len(buttons[0])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.current_player = 1
                elif event.key in [pygame.K_g, pygame.K_d, pygame.K_q, pygame.K_s, pygame.K_z]:
                    self.current_player = 2
                if self.current_player == 1:
                    current_position = self.player1_position
                    current_pseudo = self.player1_pseudo
                else:
                    current_position = self.player2_position
                    current_pseudo = self.player2_pseudo

                row, col = current_position

                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    col = min(col + 1, cols - 1)
                elif event.key in [pygame.K_LEFT, pygame.K_q]:
                    col = max(col - 1, 0)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    row = min(row + 1, rows - 1)
                    if row > 1:
                        row, col = 1, 0
                elif event.key in [pygame.K_UP, pygame.K_z]:
                    row = max(row - 1, 0)
                    if row > 1:
                        row, col = 1, 0
                elif event.key in [pygame.K_RETURN, pygame.K_g]:
                    selected_button = buttons[row][col]

                    if selected_button.text_input not in ["BACK", "CONTINUE"]:
                        current_pseudo = selected_button.text_input

                if self.current_player == 1:
                    self.last_player1_position = self.player1_position
                    self.player1_position = (row, col)
                    self.player1_pseudo = current_pseudo

                else:
                    self.last_player2_position = self.player2_position
                    self.player2_position = (row, col)
                    self.player2_pseudo = current_pseudo

                
                if event.key in [pygame.K_RETURN, pygame.K_g]:
                    selected_button2 = buttons[row][col]
                    if selected_button2.text_input == "BACK":
                        return 0
                    elif (self.current_player == 1 or self.current_player == 2) and selected_button2.text_input == "CONTINUE" and len(self.player1_pseudo) >= 3 and len(
                            self.player2_pseudo) >= 3:
                        self.player1_position = (0, 0)
                        self.player2_position = (0, 0)
                        return [self.player1_pseudo, self.player2_pseudo]

        # Default return value if no specific action is taken
        return 1


    def handle_alphabet_events(self, buttons):
        rows = len(buttons)
        cols = len(buttons[0])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.current_player = 1
                elif event.key in [pygame.K_g, pygame.K_d, pygame.K_q, pygame.K_s, pygame.K_z]:
                    self.current_player = 2
                if self.current_player == 1:
                    current_position = self.player1_position
                    current_pseudo = self.player1_pseudo
                else:
                    current_position = self.player2_position
                    current_pseudo = self.player2_pseudo

                row, col = current_position

                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    col = (col + 1) % cols
                elif event.key in [pygame.K_LEFT, pygame.K_q]:
                    col = (col - 1) % cols
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    row = (row + 1) % rows
                    if row == 3:
                        row, col = 3, 0
                elif event.key in [pygame.K_UP, pygame.K_z]:
                    row = (row - 1) % rows
                    if row == 3:
                        row, col = 3, 0
                elif event.key in [pygame.K_RETURN, pygame.K_g]:
                    selected_button = buttons[row][col]
                    if selected_button.text_input == "←":
                        if len(current_pseudo) > 0:
                            current_pseudo = current_pseudo[:-1]
                    elif selected_button.text_input not in ["BACK", "CONTINUE"]:
                        if len(current_pseudo) < 5:
                            current_pseudo += selected_button.text_input

                if self.current_player == 1:
                    self.last_player1_position = self.player1_position
                    self.player1_position = (row, col)
                    self.player1_pseudo = current_pseudo

                else:
                    self.last_player2_position = self.player2_position
                    self.player2_position = (row, col)
                    self.player2_pseudo = current_pseudo

                
                if event.key in [pygame.K_RETURN, pygame.K_g]:
                    selected_button2 = buttons[row][col]
                    if selected_button2.text_input == "BACK":
                        return 0
                    elif (self.current_player == 1 or self.current_player == 2) and selected_button2.text_input == "CONTINUE" and len(self.player1_pseudo) >= 3 and len(
                            self.player2_pseudo) >= 3:
                        self.player1_position = (0, 0)
                        self.player2_position = (0, 0)
                        return [self.player1_pseudo, self.player2_pseudo]
        # Default return value if no specific action is taken
        return 1


    def leaderboard_menu(self, screen, selected_option, leaderboard):
        tableau_width = 1000
        tableau_height = 500
        tableau_x = (screen.get_width() - tableau_width) // 2
        tableau_y = (screen.get_height() - tableau_height) // 2
        pygame.draw.rect(screen, (255, 255, 255), (tableau_x, tableau_y, tableau_width, tableau_height), 2)

        font = get_font(30)
        for i, entry in enumerate(leaderboard):
            pseudo_text = font.render(entry[0], True, (255, 255, 255))
            score_text = font.render(str(entry[2]), True, (255, 255, 255))
            classe_text = font.render(entry[1], True, (255, 255, 255))
            text_x = tableau_x + 100
            text_y = tableau_y + 50 + i * 50
            screen.blit(pseudo_text, (text_x + 50, text_y))
            screen.blit(score_text, (text_x + 650, text_y))
            screen.blit(classe_text, (text_x + 300, text_y))

        back_button = Button(image=pygame.image.load("assets/BACK_Rect.png"),
                            pos=(screen.get_width() // 2, screen.get_height() - 50),
                            text_input="BACK", font=get_font(30), base_color="White", selected_color="Green",
                            hovering_color="Green")
        back_button.rect.centerx = screen.get_width() // 2
        back_button.update(screen)





    def create_buttons(self, options, screen):
        buttons = []
        total_height = sum([75 + 20 for _ in options])  # Total height of all buttons
        start_y = (screen.get_height() - total_height) // 2  # Center vertically
        for i, option in enumerate(options):
            button = Button(image=pygame.image.load(f"assets/{option}_Rect.png"),
                            pos=(screen.get_width() // 2, start_y + i * (120 + 20)),
                            text_input=option, font=get_font(75), base_color="White", selected_color="Green",
                            hovering_color="Green")
            buttons.append(button)
        return buttons


    def render_buttons(self, screen, buttons, selected_option):
        for i, button in enumerate(buttons):
            if i == selected_option:
                button.select()
            else:
                button.deselect()
            button.update(screen)
