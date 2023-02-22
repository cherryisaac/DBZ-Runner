import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Graphics/Krillin-remade.png').convert_alpha()
        player_walk_2 = pygame.image.load('Graphics/Krillin-run.png').convert_alpha()
        player_walk_3 = pygame.image.load('Graphics/Krillin-backstep.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2] # Forward steps
        self.player_walk_bs = [player_walk_1, player_walk_3]  # Backward steps
        self.player_index = 0
        self.player_jump = pygame.image.load('Graphics/Krillin-jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.prev_x = self.rect.x

        self.jump_sound = pygame.mixer.Sound('Sound/swoosh-jump.mp3')
        self.jump_sound.set_volume(0.2)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 390:
            self.rect.bottom = 390
            self.jump_count = 0
        # Make sure the player does not move off the screen horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800

    # For back and forth movement
    def player_input(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 390:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5



    def animation_state(self):
        if self.rect.bottom < 390:
            self.image = self.player_jump
        elif self.rect.x < self.prev_x:  # Moving left
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk_bs): 
                self.player_index = 0
            self.image = self.player_walk_bs[int(self.player_index)]
        elif self.rect.x > self.prev_x:  # Moving right
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        else:
            self.image = self.player_walk[0]
            self.image = self.player_walk_bs[0]
        self.prev_x = self.rect.x
                

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_input()
        self.animation_state()