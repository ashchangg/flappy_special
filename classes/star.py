import pygame
import os

class Star:
    star_image = pygame.image.load(os.path.join("./assets/special", "star.png"))
    stars = []

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.star_image.get_width(), self.star_image.get_height())
        self.v = 180

    def update(self, dt):
        self.rect.x -= self.v * dt
    
    def draw(self, screen):
        screen.blit(self.star_image, (self.rect.x, self.rect.y))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        star_mask = pygame.mask.from_surface(self.star_image)

        offset = (self.rect.left - bird.rect.left, self.rect.top - bird.rect.top)

        return bird_mask.overlap(star_mask, offset)

    def get_mask(self):
        return pygame.mask.from_surface(Star.star_image)
    
    def right_x(self):
        return self.rect.right
    
    def bottom_pipe_y(self):
        return self.rect.top
    