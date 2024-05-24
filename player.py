import pygame
import Constants


class Player:
    def __init__(self, x, y, color, width, height, username, hp_max=100, speed=10, damage=25, cd_reload=0.25, cd_dash=5):
        scaled_width = 100
        scaled_height = 100

        self.images_left = [pygame.transform.scale(pygame.image.load(f"assets/player_movements/{color}_gauche1.png"), (scaled_width, scaled_height)),
                            pygame.transform.scale(pygame.image.load(f"assets/player_movements/{color}_gauche2.png"), (scaled_width, scaled_height))]
        self.images_right = [pygame.transform.scale(pygame.image.load(f"assets/player_movements/{color}_droite1.png"), (scaled_width, scaled_height)),
                             pygame.transform.scale(pygame.image.load(f"assets/player_movements/{color}_droite2.png"), (scaled_width, scaled_height))]
        self.images_up = [pygame.transform.scale(pygame.image.load(f"assets/player_movements/{color}_arriere1.png"), (scaled_width, scaled_height)),
                          pygame.transform.scale(pygame.image.load(f"assets/player_movements/{color}_arriere2.png"), (scaled_width, scaled_height))]
        self.images_down = [pygame.transform.scale(pygame.image.load(f"assets/player_movements/{color}_avant1.png"), (scaled_width, scaled_height)),
                            pygame.transform.scale(pygame.image.load(f"assets/player_movements/{color}_avant2.png"), (scaled_width, scaled_height))]

        self.image_index = 0
        self.animation_speed = 0.1
        self.last_animation_time = 0
        
        
        self.image = pygame.transform.scale(self.images_right[0], (scaled_width, scaled_height))
        self.last_shot_time = 0
        self.last_dash_time = 0
        self.username = username
        self.x = x
        self.y = y
        self.width = scaled_width
        self.height = scaled_height
        self.rect = pygame.Rect(self.x, self.y, 50, 88)
        self.last_direction = [0, 0]
        self.velocity = [0, 0]
        
        self.hp_max = hp_max
        self.hp = hp_max
        self.speed = speed
        self.damage = damage
        self.cd_reload = cd_reload
        self.cd_dash = cd_dash  

    def move(self):
        new_x = self.rect.x + self.velocity[0] * self.speed
        new_y = self.rect.y + self.velocity[1] * self.speed

        if new_x < 0:
            new_x = 0
        elif new_x > Constants.PLAYABLE_AREA[0] - self.rect.width:
            new_x = Constants.PLAYABLE_AREA[0] - self.rect.width

        if new_y < 120: 
            new_y = 120
        elif new_y > Constants.PLAYABLE_AREA[1] - self.rect.height:
            new_y = Constants.PLAYABLE_AREA[1] - self.rect.height

        self.rect.x = new_x
        self.rect.y = new_y
        
        if self.velocity != [0, 0]:
            self.last_direction = self.velocity[:]
            self.update_animation()
        
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > self.animation_speed * 1000:
            self.image_index = (self.image_index + 1) % 2  # Cycle between 0 and 1
            self.last_animation_time = current_time
        
        if self.velocity[0] < 0:  # Moving left
            self.image = self.images_left[self.image_index]
        elif self.velocity[0] > 0:  # Moving right
            self.image = self.images_right[self.image_index]
        elif self.velocity[1] < 0:  # Moving up
            self.image = self.images_up[self.image_index]
        elif self.velocity[1] > 0:  # Moving down
            self.image = self.images_down[self.image_index]
    
    
    #get the center of the player to spawn the bullet
    def get_center(self):
        return self.rect.center
    
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            return False
        return True
    
    def heal(self):
        self.hp = self.hp_max

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)
        screen.blit(self.image, self.rect)
    
    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.cd_reload*1000:
            self.last_shot_time = current_time
            return True
        return False
    
    def dash(self):
        if self.can_dash():
            self.rect.x += self.last_direction[0] * 200
            self.rect.y += self.last_direction[1] * 200
            self.last_dash_time = pygame.time.get_ticks()
    
    def can_dash(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dash_time > self.cd_dash*1000:
            self.last_dash_time = current_time
            return True
        return False
    