'''
The Floppy Bird game in Python, a version 
of the discountinued game Flappy Bird.
'''


import pygame, sys, random

# Displays floor imaage in pygame
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,450))
    screen.blit(floor_surface,(floor_x_pos + 288,450))

# Prodces random pipe hieghts 
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 150))
    return bottom_pipe, top_pipe

# 
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Displays pipes on screen and flips the image if the pipe is on the top
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

        if bird_rect.top <= -50 or bird_rect.bottom >= 450:
            return False

    return True

pygame.init()
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()

# Game Variable
gravity = 0.25
bird_movement = 0
game_active = True

# Uploads background iamge
bg_surface = pygame.image.load('assets/background-day.png').convert()
 
# Uploads floor image
floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0 

# Uploads bird image
bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_rect = bird_surface.get_rect(center = (50,256))

# Uploads pipe image and respwans pipes 
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [200,300,400]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12  
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,256)

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface,(0,0))

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface,bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
            
    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
            floor_x_pos = 0
    screen.blit(floor_surface,(floor_x_pos,450))
    
    pygame.display.update()
    clock.tick(120)
