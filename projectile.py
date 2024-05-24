import pygame

class Projectile:
    def __init__(self, x, y, direction, damage, shooter):
        self.velocity = (0, -1)
        self.image = pygame.image.load("IMAGE/bullet.png")
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = 10
        self.shooter = shooter
        self.direction = direction
        self.damage = damage

    def move(self):
            # Calculate the change in position based on the direction
        if self.direction == [0,0]:
            self.direction = [1,0]
        change_x = self.direction[0] * self.speed
        change_y = self.direction[1] * self.speed

        # Update the position of the bullet
        self.rect.x += change_x
        self.rect.y += change_y

        # Check if the new position is within the screen boundaries
        if self.rect.x < 0 or self.rect.x > 1920 - self.rect.width:
            return False  # Bullet is out of bounds in the x-direction
        if self.rect.y < 0 or self.rect.y > 1080 - self.rect.height:
            return False  # Bullet is out of bounds in the y-direction

        return True

    def draw(self, screen):
        image_x = self.rect.x+20 + (self.rect.width - self.image.get_width()) / 2
        image_y = self.rect.y-5 + (self.rect.height - self.image.get_height()) / 2
        screen.blit(self.image, (image_x, image_y))
