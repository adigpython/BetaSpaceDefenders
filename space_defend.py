# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path
from pygame.locals import *
import sys


WIDTH = 800
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GREY = (200, 200, 200)
DARK_GREY = (100, 100, 100)

enemyimgs = ("enemyBlack1.png", "enemyBlack2.png", "enemyBlack3.png", "enemyBlack4.png", "enemyBlack5.png", "enemyBlue1.png",
             "enemyBlue2.png", "enemyBlue3.png", "enemyBlue4.png", "enemyBlue5.png", "enemyRed1.png", "enemyRed2.png",
             "enemyRed3.png", "enemyRed4.png", "enemyRed5.png", "enemyGreen1.png", "enemyGreen2.png", "enemyGreen3.png",
             "enemyGreen4.png", "enemyGreen5.png")
playerimgs = ("playerShip1_blue.png", "playerShip1_green.png",
              "playerShip1_orange.png", "playerShip1_red.png")
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "spaceimg")
playerimg_folder = path.join(img_folder, "PNG")
enemyimg_folder = path.join(img_folder, "Enemies")
bulletimg_folder = path.join(img_folder, "Lasers")
font_folder = path.join(img_folder, "Bonus")
UI_folder = path.join(img_folder, "UI")
music_folder = path.join(img_folder, "Bonus")


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player_Img = pygame.image.load(path.join(playerimg_folder, random.choice(playerimgs))).convert()
        self.image = pygame.transform.scale(player_Img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT - 100
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.speedx = -8
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.speedx = 8
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.speedy = -4
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.speedy = 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a\
                    or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.speedx = 0

            if event.key == pygame.K_UP or event.key == pygame.K_w \
               or event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.speedy = 0

        if self.rect.left < -64:
            self.rect.right = WIDTH + 64
        if self.rect.right > WIDTH + 64:
            self.rect.left = -64
        if self.rect.top < 400:
            self.rect.top = 400
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        enemy_Img = pygame.image.load(path.join(enemyimg_folder, random.choice(enemyimgs))).convert()
        self.image = pygame.transform.scale(enemy_Img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 30:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_Img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


# initialize pygame and create window

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Defenders")
icon = pygame.image.load(path.join(enemyimg_folder, "enemyblack1.png")).convert()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

background = pygame.image.load(path.join(img_folder, "background.png")).convert()
player_Img = pygame.image.load(path.join(playerimg_folder, random.choice(playerimgs))).convert()
bullet_Img = pygame.image.load(path.join(bulletimg_folder, "laserRed07.png")).convert()
enemy_Img = pygame.image.load(path.join(enemyimg_folder, random.choice(enemyimgs))).convert()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)


running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    screen.blit(background, (0, 0))
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:

            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()
    bullet_hits = pygame.sprite.groupcollide(bullets, mobs, True, True)
    for hit in bullet_hits:
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, (0, 0))

    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()