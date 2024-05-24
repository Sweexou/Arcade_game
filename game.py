import pygame
from player import Player
from projectile import Projectile


class GameState:
    PLAYING = 1
    GAME_OVER = 2

class Game:
    def __init__(self, screen, username_P1 = "guest01", username_P2 = "guest02", rank_P1 = "Soldat", rank_P2 = "Soldat"):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.rank_P1 = rank_P1
        self.rank_P2 = rank_P2
        self.player = self.create_player(200, 540, "ROUGE", 50, 50, username_P1, rank_P1)
        self.player2 = self.create_player(1720, 540, "BLEU", 50, 50, username_P2, rank_P2)
        #self.area = pygame.Rect(300, 150, 300, 300)
        #self.area_color = "red"
        self.remaining_time = 0
        self.timer_start = 99
        self.start_ticks = pygame.time.get_ticks()
        self.end_game = False
        self.walls = []
        self.bullets = []
        self.win_player1 = 0
        self.win_player2 = 0
        self.player1_score = 0
        self.player2_score = 0
        
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()
        
    def create_player(self, x, y, color, width, height, username, rank):
        if rank == "guest":
            return Player(x, y, color, width, height, username)
        return Player(x, y, color, width, height, username, 100 , 10, 25, 0.3, 3)
        
        
    def score(self):
        self.player1_score = 0
        self.player2_score = 0
        if self.win_player1 > self.win_player2:
            self.player1_score += 500
            if self.win_player1 - self.win_player2 >=2:
                self.player1_score += 100
            if self.remaining_time > 60:
                self.player1_score += round(self.remaining_time)
        elif self.win_player1 < self.win_player2:
            self.player2_score += 500
            if self.win_player2 - self.win_player1 >=2:
                self.player2_score += 100
            if self.remaining_time > 60:
                self.player1_score += round(self.remaining_time)
        else:
            self.player1_score += 200
            self.player2_score += 200
        self.player1_score += self.win_player1 * 100
        self.player2_score += self.win_player2 * 100
        print(f"Score Player 1: {self.player1_score}")
        print(f"Score Player 2: {self.player2_score}")
        
    def draw_health_bar(self, player, x, y):
        health_ratio = player.hp / player.hp_max
        bar_width = 800  # Largeur de la barre de vie
        bar_height = 40  # Hauteur de la barre de vie
        border_color = (0, 0, 0)  # Couleur du contour de la barre de vie
        background_color = (128, 128, 128)  # Couleur de fond de la barre de vie

        # Dessiner le contour de la barre de vie
        pygame.draw.rect(self.screen, border_color, (x - 5, y - 5, bar_width + 10, bar_height + 10))

        # Dessiner la barre de vie de fond
        pygame.draw.rect(self.screen, background_color, (x, y, bar_width, bar_height))

        # Déterminer la couleur de la barre de vie en fonction du ratio de santé
        if health_ratio > 0.75:
            color = (0, 255, 0)
        elif health_ratio > 0.5:
            color = (255, 255, 0)
        elif health_ratio > 0.25:
            color = (255, 165, 0)
        else:
            color = (255, 0, 0)

        # Dessiner la barre de vie
        pygame.draw.rect(self.screen, color, (x, y, bar_width * health_ratio, bar_height))
        
        #username
        font = pygame.font.Font(None, 36)
        username_surface = font.render(player.username, True, (0, 0, 0))
        username_rect = username_surface.get_rect(midtop=(x + bar_width / 2, y + bar_height + 5)) 
        self.screen.blit(username_surface, username_rect)

    def draw_score_point(self, x, y, team):
        pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 10)
        pygame.draw.circle(self.screen, (0, 0, 0), (x+30, y), 10)
        if team == 1:
            color = (255, 215, 0)
            color2 = (155, 155, 155)
        elif team == 2:
            color = (255, 215, 0)
            color2 = (255, 215, 0)
        else:
            color = (155, 155, 155)
            color2 = color
            
        pygame.draw.circle(self.screen, color, (x, y), 8)
        pygame.draw.circle(self.screen, color2, (x+30, y), 8)
        
    def game_over(self):
        if self.end_game == True:
            return True
        if self.win_player1 == 3 or self.win_player2 == 3:
            return True
        if self.timer_start == 0:
            return True
        return False
        

    def respawn_player(self, player, x, y):
        player.rect.topleft = (x, y)
        player.velocity = [0, 0]

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Handle joystick button presses
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.joy == 0:  # Joystick 1
                    if event.button == 0:  # Button 0 for shooting by player 1
                        if self.player.can_shoot():
                            self.shoot2(self.player)
                    elif event.button == 1:  # Button 1 for dash by player 1
                        self.player.dash()
                elif event.joy == 1:  # Joystick 2
                    if event.button == 0:  # Button 0 for shooting by player 2
                        if self.player2.can_shoot():
                            self.shoot2(self.player2)
                    elif event.button == 1:  # Button 1 for dash by player 2
                        self.player2.dash()

        # Update player movements based on joystick axes
        # Player 1
        if len(self.joysticks) >= 1:
            self.player.velocity[0] = round(self.joysticks[0].get_axis(0))  # Horizontal movement
            self.player.velocity[1] = round(self.joysticks[0].get_axis(1))  # Vertical movement

        # Player 2
        if len(self.joysticks) >= 2:
            self.player2.velocity[0] = round(self.joysticks[1].get_axis(0))  # Horizontal movement
            self.player2.velocity[1] = round(self.joysticks[1].get_axis(1))


        

            
            
    def shoot2(self, player):
        player_center = player.get_center()
        bullet = Projectile(player_center[0], player_center[1], player.last_direction, player.damage, player)
        self.bullets.append(bullet)    

    def update(self):
        self.player.move()
        self.player2.move()
        #if self.area.colliderect(self.player.rect):
        #    self.area_color = "blue"
        #else:
        #    self.area_color = "red"
        for bullet in self.bullets[:]:
            if bullet.rect.colliderect(self.player.rect) and bullet.shooter != self.player:
                self.player.take_damage(bullet.damage)
                self.bullets.remove(bullet)
            elif bullet.rect.colliderect(self.player2.rect) and bullet.shooter != self.player2:
                self.player2.take_damage(bullet.damage)
                self.bullets.remove(bullet)
            if bullet.move() == False:
                self.bullets.remove(bullet)
            bullet.move()
            
        if self.player.hp <= 0:
            self.win_player2 += 1
            self.player.heal()
            self.respawn_player(self.player, 200, 540)
            self.respawn_player(self.player2, 1720, 540)
            self.remove_bullet()
        if self.player2.hp <= 0:
            self.win_player1 += 1
            self.player2.heal()
            self.respawn_player(self.player2, 1720, 540)
            self.respawn_player(self.player, 200, 540)
            self.remove_bullet()
        
    def remove_bullet(self):
        for bullet in self.bullets[:]:
            self.bullets.remove(bullet)
    
    def display(self):
        background = pygame.image.load("IMAGE/sand_ground.jpg")
        background = pygame.transform.scale(background, (1920, 1080))
        screen.blit(background,(0,0))
        self.player.draw(self.screen)
        self.player2.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.draw_health_bar(self.player, 50, 30)
        self.draw_health_bar(self.player2, 1070, 30)

        elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.remaining_time = max(0, self.timer_start - elapsed_seconds)
        if self.remaining_time == 0:
            self.end_game = True
        timer_text = f"{self.remaining_time:02.0f}"
        font = pygame.font.Font(None, 74)
        timer_surface = font.render(timer_text, True, (0, 0, 0))
        timer_rect = timer_surface.get_rect(center=(self.screen.get_width() / 2, 50))
        self.screen.blit(timer_surface, timer_rect)
        
        self.draw_score_point(805, 90, self.win_player1)
        self.draw_score_point(1085, 90, self.win_player2)
        
        
        pygame.display.flip()
        
        
    def display_losing_screen(self):
        background = pygame.image.load("IMAGE/sand_ground.jpg")
        background = pygame.transform.scale(background, (1920, 1080))
        self.screen.blit(background, (0, 0))  # Draw the background image

        # Create a black rectangle in the center
        rect_width = 800
        rect_height = 200
        rect_x = (self.screen.get_width() - rect_width) // 2
        rect_y = (self.screen.get_height() - rect_height) // 2
        pygame.draw.rect(self.screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))

        # Determine the losing text
        font = pygame.font.Font("assets/font.ttf", 25)
        if self.win_player1 > self.win_player2:
            score_text = f"{self.player.username} won with {self.player1_score} points!"
        elif self.win_player1 < self.win_player2:
            score_text = f"{self.player2.username} won with {self.player2_score} points!"
        else :
            score_text = "It's a draw"
            
        losing_surface = font.render(score_text, True, (255, 0, 0))
        losing_rect = losing_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(losing_surface, losing_rect)  # Draw the losing text

        pygame.display.flip()
        pygame.time.wait(3000)  # Display for 3 seconds

    def get_font(size):
        return pygame.font.Font("assets/font.ttf", size)

    def run(self):
        if self.game_over():
            self.score()
            self.display_losing_screen()  # Call the losing screen display method
            return [(self.player.username, self.player1_score, self.rank_P1), (self.player2.username, self.player2_score, self.rank_P2)]
        self.handling_events()
        self.update()
        self.display()
        return -1


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
game = Game(screen)
game.run()