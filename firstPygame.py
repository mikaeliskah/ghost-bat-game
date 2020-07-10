import time
import pygame
import numpy as np

# initialize game surface
pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("G H O S T   N I G H T ")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
pygame.mixer.music.load('outdoors.mp3')
pygame.mixer.music.play(-1, 20)


def redrawScreen():
    # reset window after each movement
    win.fill((100, 100, 100))
    win.blit(background.img, (0, 0))
    win.blit(bat_1.img, (bat_1.x, bat_1.y))
    win.blit(ghost.img, (ghost.x, ghost.y))


def catchGhost(bat_1):
    # recalculate bat's position and check if it caught the ghost:
    ghost.width, ghost.height = ghost.img.get_size()
    ghost.center = [ghost.x + ghost.width/2, ghost.y + ghost.height/2]
    bat_1.width, bat_1.height = bat_1.img.get_size()
    bat_1.center = [bat_1.x + bat_1.width/2, bat_1.y + bat_1.height/2]
    dx = (ghost.center[0] - bat_1.center[0])
    dy = (ghost.center[1] - bat_1.center[1])
    r = np.sqrt(dx**2+dy**2)  # calculate distance between center points
    if r > 60:  # ghost is ahead of bat
        bat_1.x = bat_1.x + (dx * bat_1.vel) / r
        bat_1.y = bat_1.y + (dy * bat_1.vel) / r
        return 0
    else:  # ghost loses: game over
        print('B A T caught G H O S T  :)')
        return 1


class Character:
    def __init__(self, x_coord, y_coord, velocity, character_image):
        self.x = x_coord
        self.y = y_coord
        self.vel = velocity
        self.img = pygame.image.load(character_image)


# create characters at initial positions and define speed:
ghost = Character(250-38, 400, 10, 'ghost.png')
bat_1 = Character(10, 10, 3, 'bat_small.png')
background = Character(0, 0, [], 'forest.png')


run = True
loose = False
game_over = False
while run:
    clock.tick(27)  # 27 fps update rate
    while game_over == True:
        pygame.mixer.music.fadeout(2000)
        win.fill((0, 0, 0))
        loose_text = font.render("G A M E  O V E R", True, (255, 255, 255))
        quit_text = font.render("PRESS ANY KEY TO LEAVE", True, (255, 255, 255))
        win.blit(loose_text, (150, 200))
        win.blit(quit_text, (130, 280))
        pygame.display.update()
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN) or (event.type == pygame.QUIT):
                exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # check what key is pressed and move character accordingly
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if ghost.x > 0:
            ghost.x -= ghost.vel
    if keys[pygame.K_RIGHT]:
        if ghost.x < 500-77:
            ghost.x += ghost.vel
    if keys[pygame.K_UP]:
        if ghost.y > 0:
            ghost.y -= ghost.vel
    if keys[pygame.K_DOWN]:
        if ghost.y < 500:
            ghost.y += ghost.vel

    caught = catchGhost(bat_1)
    if caught == 1:
        game_over = True
        time.sleep(1)

    redrawScreen()
    pygame.display.update()
pygame.quit()
