import pygame
import os

# mystery box gives a randomly chosen special item
class Mystery:
    mystery_image = pygame.image.load(os.path.join("./assets/special", "mystery.png"))
    icons = []

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.mystery_image.get_width(), self.mystery_image.get_height())
        self.v = 180

    def update(self, dt):
        self.rect.x -= self.v * dt
    
    def draw(self, screen):
        screen.blit(self.mystery_image, (self.rect.x, self.rect.y))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        mystery_mask = pygame.mask.from_surface(self.mystery_image)

        offset = (self.rect.left - bird.rect.left, self.rect.top - bird.rect.top)

        return bird_mask.overlap(mystery_mask, offset)
    
    def right_x(self):
        return self.rect.right
    
    def bottom_pipe_y(self):
        return self.rect.top

    def get_mask(self):
        return pygame.mask.from_surface(Mystery.mystery_image)