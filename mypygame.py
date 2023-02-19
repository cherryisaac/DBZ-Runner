import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int((pygame.time.get_ticks() / 1000)) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (10, 10, 10))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= randint(5, 9)

            if obstacle_rect.bottom == 390:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(soldier_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -50]

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

# Starts all the important aspects of pygame
pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('My Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Fonts/Pixeltype.ttf', 20)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('Images/bg.jpeg').convert()
ground_surface = pygame.image.load('Images/ground-dark.png').convert_alpha()

score_surface = test_font.render('My Game', False, (10, 10, 10))
score_rect = score_surface.get_rect(center = (400, 50))

# Obstacles
snail_surface = pygame.image.load('Graphics/snail.png').convert_alpha()
soldier_surface = pygame.image.load('Graphics/soldier.png').convert_alpha()
soldier_surface = pygame.transform.rotozoom(soldier_surface, 0, 0.54) # resize image

obstacle_rect_list = []

player_surface = pygame.image.load('Graphics/Krillin.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 390))
player_gravity = 0

# Intro screen
player_alt = pygame.image.load('Graphics/dbz-krillin.png').convert_alpha()
player_alt = pygame.transform.rotozoom(player_alt, 0, 0.5)
player_alt_rect = player_alt.get_rect(center = (400, 200))

game_name = test_font.render('DBZ runner', False, 'white')
game_name_rect = game_name.get_rect(center = (400, 50))

game_message = test_font.render('Press space to run', False, 'white')
game_message_rect = game_message.get_rect(center = (400, 350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # breaks while loop when exiting so no error message
            exit()
        if game_active:
            # Jump only once if the space bar is pressed or mouse click on the player
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 390:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 390:  
                    player_gravity = -20

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0, 2): # 0 = true, 1 = false
                obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), 390)))
            else:
                obstacle_rect_list.append(soldier_surface.get_rect(midbottom = (randint(900, 1100), 250)))

       
    if game_active:
        # screen block image transfer aka one surface on another surface & positioning
        screen.blit(sky_surface,(-300,0)) 
        screen.blit(ground_surface,(0,360))
        # pygame.draw.rect(screen, '#caf8fc', score_rect)
        # pygame.draw.rect(screen,'#caf8fc', score_rect, 10)
        # screen.blit(score_surface, score_rect)
        score = display_score()
        # snail_rect.x -=5
        # if snail_rect.x < -50:
        #     snail_rect.x = 800
        # screen.blit(snail_surface, snail_rect)
        # player_rect.left += 1

        # Player
        player_gravity +=1
        player_rect.y += player_gravity
        if player_rect.bottom >= 390:
            player_rect.bottom = 390
        screen.blit(player_surface, player_rect)

        # Obstacle movement 
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collisions
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill('black')
        screen.blit(player_alt, player_alt_rect)
        obstacle_rect_list.clear()

        score_message = test_font.render(f'Your score: {score}', False, 'white')
        score_message_rect = score_message.get_rect(center = (400, 350))
        screen.blit(game_name, game_name_rect)
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint((mouse_pos)):
    #     print(pygame.mouse.get_pressed())
    pygame.display.update()
    clock.tick(60) # Frame rate