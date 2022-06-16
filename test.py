import pygame
from pygame import Rect
from pygame import * 
import sys
import random
import numpy as np


pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

size = [60, 80] # W, H
size2 = [300, 400] # W, H
screen = pygame.display.set_mode(size)
screen.fill(white)
pygame.display.set_caption("Vokram Environment")



def get_random_box(size):
    x = random.choice(range(0, size[0]))
    y = random.choice(range(0, size[1])) 
    w = random.choice(range(int(size[0] / 4),int(size[0] / 1.5)))
    h = random.choice(range(int(size[1] / 4),int(size[1] / 1.5)))
    return (x, y, w, h)

def get_rect_box(size, box):
    x, y, w, h = box
    if y - h < 5:
        y = 5
    if x - w < 5:
        x = 5
    if y + h > size[1] - 5:
        y = size[1] - 5 - h
    if x + w > size[0] - 5:
        x = size[0] - 5 - w

    box = [x, y, w, h]
    rect = Rect(box)
    return rect, box

def check_much_area(red_rect, green_rect):
    clip = red_rect.clip(green_rect)
    clip_area = clip.w * clip.h

    # red_rect.w * red_rect.h * 1/8
    # green_rect.w * green_rect.h
    if clip_area > 0:
        print("There are much clip area")
        return True
    else:
        return False

# * Initailize environment
done = False
clock = pygame.time.Clock()

red_box = get_random_box(size)
green_box = get_random_box(size)
red_rect, red_box = get_rect_box(size, red_box)
green_rect, green_box = get_rect_box(size, green_box)

reward = 0
steps = 0
font = pygame.font.SysFont(None,10)

check_area = False
while not done:
    clock.tick(10)


    if check_much_area(red_rect, green_rect):
        red_box = get_random_box(size)
        green_box = get_random_box(size)
        red_rect, red_box = get_rect_box(size, red_box)
        green_rect, green_box = get_rect_box(size, green_box)
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            steps += 1
            if green_rect.collidepoint(event.pos): # * Next step
                # * red box
                red_box = get_random_box(size)
                red_rect, red_box = get_rect_box(size, red_box)

                # * green box
                green_box = get_random_box(size)
                green_rect, green_box = get_rect_box(size, green_box)
                print(f'redbox: {red_box}')
                print(f'greenbox: {green_box}')
                reward += 1
            elif red_rect.collidepoint(event.pos):  # * Terminate episode
                reward -= 1
                pygame.quit()

    if check_much_area(red_rect, green_rect):
        continue
    else:
        screen.fill(white)
        pygame.draw.rect(screen, red, red_box)
        pygame.draw.rect(screen, green, green_box)
        img = font.render(f"steps: {steps}, rewards: {reward}", True, black)
        text_rect = img.get_rect()
        #pygame.draw.rect(screen, black, text_rect, 1)
        screen.blit(img, (5, 5))
        display.update()
        pygame.display.flip()

pygame.quit()