import random
import pygame
from sys import exit
from random import randint, choice
from myplayer import Player

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'soldier':
            soldier_frame1 = pygame.image.load('Graphics/soldier.png').convert_alpha()
            soldier_frame1 = pygame.transform.rotozoom(soldier_frame1, 0, 0.54) 
            soldier_frame2 = pygame.image.load('Graphics/soldier2.png').convert_alpha()
            soldier_frame2 = pygame.transform.rotozoom(soldier_frame2, 0, 0.54)
            self.frames = [soldier_frame1, soldier_frame2]
            self.animation_increment = 0.018  # soldier animation speed
            y_pos = 280
        else:
            saibaman_frame1 = pygame.image.load('Graphics/saibaman1.png').convert_alpha()
            saibaman_frame1 = pygame.transform.rotozoom(saibaman_frame1, 0, 0.22) # resize image
            saibaman_frame2 = pygame.image.load('Graphics/saibaman2.png').convert_alpha()
            saibaman_frame2 = pygame.transform.rotozoom(saibaman_frame2, 0, 0.28)
            self.frames = [saibaman_frame1, saibaman_frame2]
            self.animation_increment = 0.052  # saibaman animation speed
            y_pos = 385

        self.is_soldier = type == 'soldier'  # attribute to indicate the type of instance

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += self.animation_increment  
        if self.is_soldier and self.animation_index >= len(self.frames):
            self.animation_index = 0
        elif not self.is_soldier and self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= randint(9, 11) # Speed of objects/enemies
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int((pygame.time.get_ticks() / 1000)) - start_time
    score_surf = pixel_font.render(f'Score: {current_time}', False, (10, 10, 10))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprites():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# Starts all the important aspects of pygame
pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('DBZ Runner')
clock = pygame.time.Clock()
pixel_font = pygame.font.Font('Fonts/Pixeltype.ttf', 20)
game_active = False
start_time = 0
score = 0

# TODO - Fix music acting up when playing multiple songs
# bg_music_files = ['Sound/DBZ - We were angels.wav', 
# 'Sound/DBZ - Battle Point Unlimited (16-Bit Remix).wav', 
# 'Sound/DBZ - We Gotta Power (16-bit Style Remix).wav']
# bg_music = pygame.mixer.Sound(random.choice(bg_music_files))

bg_music = pygame.mixer.Sound('Sound/DBZ - We were angels.wav')
bg_music.set_volume(0.05)


player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('Images/bg.jpeg').convert()
ground_surface = pygame.image.load('Images/ground-dark.png').convert_alpha()

score_surface = pixel_font.render('My Game', False, (10, 10, 10))
score_rect = score_surface.get_rect(center = (400, 50))

player_walk_1 = pygame.image.load('Graphics/Krillin-remade.png').convert_alpha()
player_rect = player_walk_1.get_rect(midbottom = (80, 390))

# Intro screen
player_alt = pygame.image.load('Graphics/dbz-krillin.png').convert_alpha()
player_alt = pygame.transform.rotozoom(player_alt, 0, 0.5)
player_alt_rect = player_alt.get_rect(center = (400, 200))

game_name = pixel_font.render('DBZ runner', False, 'white')
game_name_rect = game_name.get_rect(center = (400, 50))

game_message = pixel_font.render('Press enter to run', False, 'white')
game_message_rect = game_message.get_rect(center = (400, 350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(650, 1200)) # Frequency of enemies/obstacles

saibaman_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(saibaman_animation_timer, 300)

soldier_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(soldier_animation_timer, randint(1000, 1200))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # breaks while loop when exiting so no error message
            exit()
     
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                # Frequency of enemy types - currently set at 40/60
                obstacle_group.add(Obstacle(choice(['soldier', 'soldier', 'saibaman', 'saibaman', 'saibaman'])))
            
       
    if game_active:
        bg_music.play(loops = -1) # -1 means infinite loop
        # screen block image transfer aka one surface on another surface & positioning
        screen.blit(sky_surface,(-300,0)) 
        screen.blit(ground_surface,(0,360))
        score = display_score()

        # player
        player.draw(screen)
        player.update()
 
        # obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        #collisions
        game_active = collision_sprites()
        
    else:
        bg_music.stop()
        # TODO - Fix music acting up when playing multiple songs
        # new_music = pygame.mixer.Sound(random.choice(bg_music_files))
        # new_music.set_volume(0.05)
        # bg_music = new_music
        screen.fill('black')
        screen.blit(player_alt, player_alt_rect)
        player.sprite.rect.midbottom = (80, 390)
        player_gravity = 0

        score_message = pixel_font.render(f'Your score: {score}', False, 'white')
        score_message_rect = score_message.get_rect(center = (400, 350))
        screen.blit(game_name, game_name_rect)
        
        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60) # Frame rate