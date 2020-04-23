import pygame
import random
import math
from pygame import mixer

# Initialize your pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# load background image
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
# to play the music in loop pass -1
mixer.music.play(-1)

# Even is anything happening inside your game window ( eg , close -> QUITE event)

# Title and Icon
pygame.display.set_caption("Space Inveders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player

# Load Image
playerImg = pygame.image.load('space-invaders.png')
# Set co ordinates
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# List of enemies

for i in range(num_of_enemies):
    # load image
    enemyImg.append(pygame.image.load('enemy.png'))
    # Set co ordinates
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet

# Ready - You can't see the bullet on the screen

# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
# set co-ordinates
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# co-ordinate of Score
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    # rander the text on the screen
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    # blit the score in the screen
    screen.blit(score, (x, y))


# Create Player
def player(x, y):
    # draw image of the player on the screen(surface) .blit(image,(x,y))
    screen.blit(playerImg, (x, y))


# Create Enemy
def enemy(x, y, i):
    # draw image of the player on the screen(surface) .blit(image,(x,y))
    screen.blit(enemyImg[i], (x, y))


# Create Fire if space bar is pressed
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    # calculate distace between enemy and bullet
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if distance < 27:
        return True
    return False


# Game loop

running = True

while running:
    # Set  Screeen color RED GREEN BLUE
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    # grab all events happng inside your pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # QUIT -> Close window
            running = False

        # any key stroke of key board is an event
        # if keystroke is prassed check whether its right or left ( check event type)
        # KEYDOWN -> Pressing any botton in the keyboard

        if event.type == pygame.KEYDOWN:
            # if right arrow key is pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            # if right arrow is pressed
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # make sound when a bullet got fired
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Get the current x co-ordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # KEYUP ->Realising any keyboard key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # call your player (player image will get drawn by .blit method
    # Checking for boundaries of spaceship so its doesn't go out of bound
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # GAME OVER
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Fire multiple bullets ( reset the value when the bullet goes outside bound)
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    #  Update Your Display
    pygame.display.update()
