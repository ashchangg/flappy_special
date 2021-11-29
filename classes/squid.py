import pygame
import os

# reverses gravity
class Squid:
    squid_image = pygame.image.load(os.path.join("./assets/special", "squid.png"))
    icons = []

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.squid_image.get_width(), self.squid_image.get_height())
        self.v = 180

    def update(self, dt):
        self.rect.x -= self.v * dt
    
    def draw(self, screen):
        screen.blit(self.squid_image, (self.rect.x, self.rect.y))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        squid_mask = pygame.mask.from_surface(self.squid_image)

        offset = (self.rect.left - bird.rect.left, self.rect.top - bird.rect.top)

        return bird_mask.overlap(squid_mask, offset)
    
    def right_x(self):
        return self.rect.right
    
    def bottom_pipe_y(self):
        return self.rect.top

    def get_mask(self):
        return pygame.mask.from_surface(Squid.squid_image)
    