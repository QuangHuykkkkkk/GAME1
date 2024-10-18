import pygame
SCREEN_wIDTH = 800
SCREEN_HIGHT = SCREEN_wIDTH * 0.8

screen = pygame.display.set_mode((SCREEN_wIDTH , SCREEN_HIGHT))
Back_ground.image = pygame.image.load('image/back_ground/plx-5.png') # type: ignore
def draw_bg():
    screen.blit(Back_ground.image)
pygame.display.set_caption('back_ground')
run = True
while run:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run = False
    pygame.display.update()
pygame.quit