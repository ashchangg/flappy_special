import pygame
import os

# bob the builder hat, protects top section
class Hat:
    hat_image = pygame.image.load(os.path.join("./assets/special", "bobbox.png"))
    hats = []

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.hat_image.get_width(), self.hat_image.get_height())
        self.v = 180

    def update(self, dt):
        self.rect.x -= self.v * dt
    
    def draw(self, screen):
        screen.blit(self.hat_image, (self.rect.x, self.rect.y))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        hat_mask = pygame.mask.from_surface(self.hat_image)

        offset = (self.rect.left - bird.rect.left, self.rect.top - bird.rect.top)

        return bird_mask.overlap(hat_mask, offset)
    
    def right_x(self):
        return self.rect.right
    
    def bottom_pipe_y(self):
        return self.rect.top

    def get_mask(self):
        return pygame.mask.from_surface(Hat.hat_image)
    