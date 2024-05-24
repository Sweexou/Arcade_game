import pygame
import sys
from game import Game
from menu import Menu
from database import db


pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

class State:
    MAIN_MENU = 0
    PLAY_MENU = 1
    LEADERBOARD_MENU = 2
    Game = 3
    SELECT_CLASS = 4
class App:
    def __init__(self):
        self.database = db.Database()
        self.leaderboard = self.get_leaderboard()
        self.state = State.MAIN_MENU
        self.classe = 0
        self.game = Game(SCREEN)
        self.menu = Menu()
        self.selected_option = 0
        self.current_player = 1  # Par défaut, le joueur est le joueur 1
        self.player1_menu_position = (100, 100)
        self.player2_menu_position = (500, 100)
        
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(144)
            self.handle_events()
            self.render_menu()
            pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Joystick handling
            if self.joystick:
                if event.type == pygame.JOYAXISMOTION:
                    axis = event.axis
                    value = event.value
                    if axis == 1:  # Vertical axis
                        if value < -0.5:
                            self.selected_option = (self.selected_option - 1) % 3
                        elif value > 0.5:
                            self.selected_option = (self.selected_option + 1) % 3
                    elif axis == 0:  # Horizontal axis (optional, for future use)
                        pass
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:  # Joystick button for selecting
                        if self.state == State.MAIN_MENU:
                            if self.selected_option == 0:
                                self.state = State.PLAY_MENU
                            elif self.selected_option == 1:
                                self.state = State.LEADERBOARD_MENU
                            elif self.selected_option == 2:
                                pygame.quit()
                                sys.exit()
                    elif event.button == 1:  # Joystick button for going back
                        if self.state == State.PLAY_MENU:
                            self.state = State.MAIN_MENU
                        elif self.state == State.LEADERBOARD_MENU:
                            self.state = State.MAIN_MENU
                        elif self.state == State.SELECT_CLASS:
                            self.state = State.PLAY_MENU



    def get_leaderboard(self):
        return self.database.get_top_players()

    def update_score(self, score):
        player1 = self.database.get_id_player_by_username(score[0][0])
        player2 = self.database.get_id_player_by_username(score[1][0])
        print("Player name from score:", score[0][0])
        print("Player ID found in database:", player1)
        if player1 is None:
            print("new player")
            player1 = self.new_player(score[0])
        else:
            self.update_classe(player1, score[0][2])
            score_P1 = self.database.get_score_by_id_player(player1)
            if score_P1 is None:
                score_P1 = 0
            score_P1 += score[0][1]
            self.database.update_score(player1, score_P1)
        if player2 is None:
            player2 = self.new_player(score[1])
        else:
            self.update_classe(player2, score[1][2])
            score_P2 = self.database.get_score_by_id_player(player2)
            if score_P2 is None:
                score_P2 = 0
            score_P2 += score[1][1]
            self.database.update_score(player2, score_P2)

    #method maj classe dans score




    def new_player(self, player):
        self.database.insert_player(player[0], 0, 0, 0, 0)
        id = self.database.get_id_player_by_username(player[0])
        self.database.insert_score(id, player[1], player[2])
        self.update_classe(id, player[2])

    def update_classe(self, id_player, classe):
        player = list(self.database.get_player(id_player))
        if classe == "Tank":
            player[5]+=1
        if classe == "Assassin":
            player[2]+=1
        if classe == "Sniper":
            player[3]+=1
        if classe == "Soldat":
            player[4]+=1
        self.database.update_player(player[1], player[2], player[3], player[4], player[5], player[0])


    def render_menu(self):
        SCREEN.blit(BG, (0, 0))

        if self.state == State.MAIN_MENU:
            self.menu.main_menu(SCREEN, self.selected_option)
        elif self.state == State.PLAY_MENU:

            if self.menu.play_menu(SCREEN) == 0:
                self.state = State.MAIN_MENU

            elif self.menu.play_menu(SCREEN) == 1:
                self.state = State.PLAY_MENU

            else:
                self.state = State.SELECT_CLASS


                if self.menu.classe_menu(SCREEN) == 1:
                    self.state = State.SELECT_CLASS

                else:
                    # Transition to the Game state
                    self.state = State.Game
                    # Retrieve pseudo names from handle_alphabet_events
                    pseudo_names = self.handle_alphabet_events(buttons)
                    if pseudo_names != 1:  # If pseudo names are obtained
                        self.player1_pseudo, self.player2_pseudo = pseudo_names

        elif self.state == State.LEADERBOARD_MENU:
            leaderboard = self.database.get_top_players()
            self.menu.leaderboard_menu(SCREEN, self.selected_option, leaderboard)
        elif self.state == State.Game:
            # recuperer la score + classe a la place d'un bool pour update le leaderboard
            result = self.game.run()
            if result != -1:
                self.update_score(result)
                self.state = State.MAIN_MENU
        elif self.state == State.SELECT_CLASS:
            self.classe = self.menu.classe_menu(SCREEN)
            if self.classe == 1:
                self.state = State.SELECT_CLASS
            elif self.classe == 0:
                self.state = State.MAIN_MENU
            else:
                self.state = State.Game
        elif self.state == State.LEADERBOARD_MENU:
            leaderboard = self.database.get_top_players()
            self.menu.leaderboard_menu(SCREEN, self.selected_option, leaderboard)
        elif self.state == State.Game:
            classe1 = self.database.get_classe(self.classe[1])
            classe2 = self.database.get_classe(self.classe[2])
            game = Game(SCREEN, username_P1=self.player1_pseudo, username_P2=self.player2_pseudo, classe_P1=classe1, classe_P2=classe2)
            result = game.run()
            if result != -1:
                self.update_score(result)
                self.state = State.MAIN_MENU
        elif self.state == State.SELECT_CLASS:
            self.menu.classe_menu(SCREEN)



if __name__ == "__main__":
    app = App()
    app.run()
