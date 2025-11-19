import pygame
import random
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Object Catcher")

# Colors
WHITE = (255, 255, 255) # Text color
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREY = (150, 150, 150)
LIGHT_GREY = (200, 200, 200)
GREEN = (50, 255, 50) # Bullets
BLUE = (100, 100, 255) # Player
DARK_BLUE = (50, 50, 150)
NAVY = (20, 10, 40) # Screen background
YELLOW = (255, 255, 0) # Enemy
PURPLE = (200, 50, 255) # Special enemy

clock = pygame.time.Clock()

# Variables
objects = []
enemy = []
special_enemy = []
bullets = []
player_x = 375
player_y = 550
enemy_elem = 0
special_enemy_elem = 0
cooldown = 0
ammo = 50
reload_timer = 480
reload = False

font = pygame.font.Font("../pong/font/Acme 9 Regular.ttf", 18)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    screen.fill(NAVY)

    # Enemies Spawning
    if random.randint(1, 50) == 1:
        x_pos = random.randint(50, 750)
        enemy.append([x_pos, 0])

    # Special Enemies Spawning
    if random.randint(1, 100) == 1:
        x_pos = random.randint(50, 750)
        special_enemy.append([x_pos, 0])

    # Adding enemies to the list
    for en in enemy[:]:
        en[1] += 1
        if en[1] > 600:
            enemy.remove(en)
        pygame.draw.circle(screen, YELLOW, (en[0], en[1]), 20)

    # Adding special enemies to the list
    for sen in special_enemy[:]:
        sen[1] += 3
        if sen[1] > 600:
            special_enemy.remove(sen)
        pygame.draw.circle(screen, PURPLE, (sen[0], sen[1]), 25)

    # Draw the player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, 100, 20))

    # Control the player
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 10
    if keys[pygame.K_RIGHT] and player_x < 700:
        player_x += 10

    if keys[pygame.K_SPACE] and cooldown == 0 and ammo > 0 and reload_timer >= 480:
        bul_x_pos = player_x
        bullets.append([player_x + 50, player_y - 7])
        ammo -= 1

    if reload:
        if reload_timer <= 0:
            ammo = 50
            reload_timer = 480
            reload = False
            cooldown = 0
        else:
            reload_timer -= 10

    if keys[pygame.K_r] and ammo != 50:
        reload = True

    # Controlling the bullets
    for bul in bullets[:]:
        bul[1] -= 20
        if bul[1] < 0 and cooldown == 0:
            bullets.remove(bul)
            cooldown = 1
        pygame.draw.rect(screen, GREEN, (bul[0], bul[1], 5, 7))

    # Eleminating the enemies
    for bul in bullets[:]:
        for en in enemy[:]:
            if en[0] - 20 < bul[0] < en[0] + 20 and en[1] - 20 < bul[1] < en[1] + 20:
                enemy.remove(en)
                if bul in bullets:
                    bullets.remove(bul)
                    if not enemy_elem >= 50:
                        enemy_elem += 1
        for sen in special_enemy[:]:
            if sen[0] - 25 < bul[0] < sen[0] + 25 and sen[1] - 25 < bul[1] < sen[1] + 25:
                special_enemy.remove(sen)
                if bul in bullets:
                    bullets.remove(bul)
                    if not special_enemy_elem >= 20:
                        special_enemy_elem += 1

    # Drawing the hotbar
    pygame.draw.rect(screen, GREY, (680, 50, 100, 400))

    # Drawing text
    screen.blit(font.render("Enemies eleminated: " + str(enemy_elem) + " / 50", True, WHITE), (10, 10))
    screen.blit(font.render("Special Enemies eleminated: " + str(special_enemy_elem) + " / 20", True, WHITE), (10, 50))
    screen.blit(font.render("Ammo: " + str(ammo), True, WHITE), (10, 100))
    screen.blit(font.render("Reload: " + str(round(reload_timer/60, 1)), True, WHITE), (10, 150))

    # Winning limits
    if enemy_elem >= 50 and special_enemy_elem >= 20:
        pygame.time.delay(3000)
        pygame.quit()
        exit()

    # Increase cooldown
    if cooldown > 0:
        cooldown -= 0.1

    # Reset cooldown
    if cooldown < 0:
        cooldown = 0

    # Refreshing
    pygame.display.update()
    clock.tick(60)
