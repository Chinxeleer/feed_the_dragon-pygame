
import pygame,random
pygame.init()

WIN_WIDTH = 1200
WIN_HIEGHT = 600
FPS = 60
VELOCITY = 10
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (200, 200, 200)
APP_BAR_COLOR = (240, 0, 0)
RUNNING = True
PLAYER_STARTING_LIVES = 5
COIN_STARTING_VELOCITY = 20
COIN_ACCELERATION = .5
SCORE = 0
BUFFER_DISTANCE = 100
pause = False

# GAME DISPLAY
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HIEGHT))
pygame.display.set_caption('Feed the dragon')
# game speed
clock = pygame.time.Clock()
# loading images
# DRAGON
dragon = pygame.image.load('dragon_right.png')
dragon_rect = dragon.get_rect()
dragon_rect.x = 32
dragon_rect.y = WIN_HIEGHT//2
# POINTS IMAGE
points_image = pygame.image.load('points_image.png')
points_image = pygame.transform.scale(points_image, (99, 99))
points_rect = points_image.get_rect()
points_rect.center = (99/2, 99/2)
# COIN
coin_image = pygame.image.load('coin.png')
coin_image = pygame.transform.scale(coin_image, (50, 50))
coin_rect = coin_image.get_rect()
coin_rect.x = WIN_WIDTH-100
coin_rect.y = random.randint(120, WIN_HIEGHT-32)

# loading sounds
coin_sound = pygame.mixer.Sound('coin_sound.wav')
missed_sound = pygame.mixer.Sound('miss_sound.wav')
missed_sound.set_volume(.1)
background_music = pygame.mixer.music.load('ftd_background_music.wav')


# loading fonts
# declaring the font to be used
fonts = pygame.font.Font('Hobeaux Rococeaux Regular.ttf', 50)

# rendering the score text
score_text = fonts.render('SCORE : ' + str(SCORE),
                          True, (0, 0, 0), APP_BAR_COLOR)
score_rect = score_text.get_rect()
score_rect.topleft = (100, 25)

# rendering the title text
title_fonts = pygame.font.Font('Hobeaux Rococeaux Regular.ttf', 70)
title_text = title_fonts.render('FEED ME', True, (0, 0, 0), APP_BAR_COLOR)
title_rect = title_text.get_rect()
title_rect.center = ((WIN_WIDTH)//2, 50)

# rendering the lives text
lives_text = fonts.render(
    f'LIVES : {PLAYER_STARTING_LIVES}', True, (0, 0, 0), APP_BAR_COLOR)
lives_rect = lives_text.get_rect()
lives_rect.topright = ((WIN_WIDTH-20), 25)
# game over font
gover_fonts = pygame.font.Font('Hobeaux Rococeaux Regular.ttf', 150)
game_over_text = gover_fonts.render(
    'GAME OVER !', True, (166, 16, 30), BACKGROUND_COLOR)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WIN_WIDTH//2, (WIN_HIEGHT-100)//2)

#
game_paused = fonts.render('Paused', True, (0, 0, 0), BACKGROUND_COLOR)
game_paused_rect = game_paused.get_rect()
game_paused_rect.center = (WIN_WIDTH//2, (WIN_HIEGHT-100)//2)

# MAIN LOOP
pygame.mixer.music.play(-1, 0.0)

while RUNNING:

    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            RUNNING = False

        # KEY MOVEMENT
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and dragon_rect.top > 100:
        dragon_rect.y -= VELOCITY
    if keys[pygame.K_s] and dragon_rect.bottom < WIN_HIEGHT:
        dragon_rect.y += VELOCITY
# collision detection
    if dragon_rect.colliderect(coin_rect):
        SCORE += 1
        coin_rect.x = WIN_WIDTH+BUFFER_DISTANCE
        coin_rect.y = random.randint(120, WIN_HIEGHT-32)
        COIN_STARTING_VELOCITY += COIN_ACCELERATION
        coin_sound.play()
    if coin_rect.x < 0:
        PLAYER_STARTING_LIVES -= 1
        missed_sound.play()
        coin_rect.x = WIN_WIDTH+BUFFER_DISTANCE
        coin_rect.y = random.randint(120, WIN_HIEGHT-32)
    else:
        coin_rect.x -= COIN_STARTING_VELOCITY

    if keys[pygame.K_p]:
        pause = True
        pygame.mixer.music.stop()
        coin_rect.x = coin_rect.x
        coin_rect.y = coin_rect.y
        while pause:
            WIN.blit(game_paused, game_paused_rect)
            pygame.display.update()
            if keys[pygame.K_c]:
                pause = False
                break

    WIN.fill(BACKGROUND_COLOR)

    if PLAYER_STARTING_LIVES == 0:
        WIN.blit(game_over_text, game_over_rect)
        COIN_STARTING_VELOCITY = 0
        pygame.display.update()
        pygame.mixer.music.stop()
# color of the surface

    # game aspects
    pygame.draw.rect(WIN, (APP_BAR_COLOR), (0, 0, WIN_WIDTH, 100))
    pygame.draw.line(WIN, LINE_COLOR, (0, 100), (WIN_WIDTH, 100), 1)
    lives_text = fonts.render(
        f'LIVES : {PLAYER_STARTING_LIVES}', True, (0, 0, 0), APP_BAR_COLOR)
    score_text = fonts.render(
        f'SCORE : {SCORE}', True, (0, 0, 0), APP_BAR_COLOR)

    WIN.blit(score_text, score_rect)
    WIN.blit(title_text, title_rect)
    WIN.blit(lives_text, lives_rect)
    WIN.blit(dragon, dragon_rect)
    WIN.blit(points_image, points_rect)
    WIN.blit(coin_image, coin_rect)
    # WIN.blit(game_over_text, game_over_rect)

    pygame.display.flip()
    pygame.display.update()
# quit the game
pygame.quit()
