import pygame, random
from classes.background import Background 
from classes.bird import Bird
from classes.pipe import Pipe
from classes.star import Star
from classes.hat import Hat
from classes.squid import Squid
from classes.ink import Ink
from classes.mystery import Mystery
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 768
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.Font('./assets/flappy.ttf', 80)
pygame.display.set_caption("NEAT - Flappy Bird")

flap_sound = pygame.mixer.Sound("./assets/bird/wing.mp3")
point_sound = pygame.mixer.Sound("./assets/point.mp3")

def display_score(score):
    score_img = FONT.render("{}".format(score), True, (255, 255, 255))
    score_rect = score_img.get_rect()
    score_rect.center = (SCREEN_WIDTH // 2, 100)
    SCREEN.blit(score_img, score_rect)

def main():
    run = True
    clock = pygame.time.Clock()

    # Initialize a background
    bg = Background(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Init a bird
    Bird.birds = [Bird(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "yellow")]

    score = 0

    # Set invincibility
    star_inv = False
    star_passes = 0
    star_waitover = True
    Star.stars = []
    hat_on = False
    squid_on = False
    squid_passes = 0 
    squid_waitover = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in Bird.birds:
                        bird.jump()
                        flap_sound.play()

        if len(Bird.birds) == 0:
            pygame.quit()
        
        dt = 1 / 60 
        SCREEN.fill((255, 255, 255))

        if len(Pipe.pipes) == 0 or Pipe.pipes[-1].right_x() < SCREEN_WIDTH - 300:
            bottom_y = random.randint(300, SCREEN_HEIGHT - 200)
            top_y = random.randint(100, bottom_y - 200)
            pipe = Pipe(SCREEN_WIDTH, bottom_y, top_y)

        if star_inv and star_waitover == False and star_passes >= 3:
            star_waitover = True
            star_inv = False
            hat_on = False
    
        if squid_on and squid_waitover == False and squid_passes >= 3:
            squid_waitrover = True
            squid_on = False
        
        if random.randint(0, 450) == 1:
            dice = random.randint(0, 5)
            if dice == 0 and star_inv == False: 
                star = Star(SCREEN_WIDTH, random.randint(top_y + 100, bottom_y - 100))
                overlap = False
                items = Hat.hats + Star.stars + Squid.icons + Mystery.icons
                for i in items:
                    if star.collide(i):
                        overlap = True
                if overlap == False:
                    Star.stars.append(star)
            if dice == 1 and star_inv == False:  
                hat = Hat(SCREEN_WIDTH, random.randint(top_y + 100, bottom_y - 100))
                items = Hat.hats + Star.stars + Squid.icons + Mystery.icons
                overlap = False
                for i in items: 
                    if hat.collide(i):
                        overlap = True
                if overlap == False:
                    Hat.hats.append(hat)
            if dice in (2, 3, 4):
                squid = Squid(SCREEN_WIDTH, random.randint(top_y + 100, bottom_y - 100))
                items = Hat.hats + Star.stars + Squid.icons + Mystery.icons
                overlap = False
                for i in items: 
                    if squid.collide(i):
                        overlap = True
                if overlap == False:
                    Squid.icons.append(squid)
            if dice == 5 and star_inv == False:
                mystery = Mystery(SCREEN_WIDTH, random.randint(top_y + 100, bottom_y - 100))
                items = Hat.hats + Star.stars + Squid.icons + Mystery.icons
                overlap = False
                for i in items: 
                    if mystery.collide(i):
                        overlap = True
                if overlap == False:
                    Mystery.icons.append(mystery)
 
        # Update/draw background
        bg.update(dt)
        bg.draw(SCREEN)

        # Update/draw bird
        for bird in Bird.birds:

            # check for star collisions
            for star in Star.stars:
                if star.collide(bird):
                    star_inv = True
                    star_waitover = False
                    star_passes = 0
                    Star.stars.remove(star)
                    bird.change_color("inv")
            
            # check for hat box collisions
            for hat in Hat.hats:
                if hat.collide(bird):
                    star_inv = True
                    star_waitover = False
                    star_passes = 0
                    hat_on = True
                    Hat.hats.remove(hat)
                    bird.change_color("bob")

            # check for antigrav box collisions
            for squid in Squid.icons:
                if squid.collide(bird):
                    squid_on = True
                    squid_waitover = False
                    squid_passes = 0
                    Squid.icons.remove(squid)
                    bird.change_color("white")
                    ink = Ink(SCREEN_WIDTH, SCREEN_HEIGHT)

            for mystery in Mystery.icons:
                if mystery.collide(bird):
                    dice = random.randint(0, 2)
                    Mystery.icons.remove(mystery)
                    if dice == 0: 
                        star_inv = True
                        star_waitover = False
                        star_passes = 0
                        bird.change_color("inv")
                    if dice == 1:  
                        star_inv = True
                        star_waitover = False
                        star_passes = 0
                        hat_on = True
                        bird.change_color("bob")
                    if dice == 2:
                        squid_on = True
                        squid_waitover = False
                        squid_passes = 0
                        bird.change_color("white")
                        ink = Ink(SCREEN_WIDTH, SCREEN_HEIGHT)

            # check for collisions 
            if star_inv == False:
                for pipe in Pipe.pipes:
                    if pipe.collide(bird):
                        Bird.birds.remove(bird)
                    if bird.rect.top < 0 or bird.rect.bottom > SCREEN_HEIGHT:
                        Bird.birds.remove(bird)
            else:
                if bird.rect.bottom > SCREEN_HEIGHT:
                        Bird.birds.remove(bird)

            if hat_on:
                for pipe in Pipe.pipes:
                    if pipe.collide_bottom (bird): 
                        Bird.birds.remove(bird) 
            
            if bird.get_color != "yellow" and star_inv == False and hat_on == False and squid_on == False:
                bird.change_color("yellow")
        
        for star in Star.stars:
            star.update(dt)
            star.draw(SCREEN)

        for hat in Hat.hats:
            hat.update(dt)
            hat.draw(SCREEN)

        for squid in Squid.icons:
            squid.update(dt)
            squid.draw(SCREEN)
        
        for mystery in Mystery.icons:
            mystery.update(dt)
            mystery.draw(SCREEN)
        
        bird.update(dt) 
        bird.draw(SCREEN)

        for pipe in Pipe.pipes:
            pipe.update(dt)
            pipe.draw(SCREEN)

            if pipe.right_x() < SCREEN_WIDTH // 2 and not pipe.scored:
                score += 1
                pipe.scored = True
                point_sound.play()
                if star_inv:
                    star_passes += 1
                if squid_on:
                    squid_passes += 1

        if squid_on:
            ink.update(dt)
            ink.draw(SCREEN)

        display_score(score)

        pygame.display.update()
        clock.tick(60)
 
if __name__ == "__main__":
    main()