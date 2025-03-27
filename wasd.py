import pygame
import time
from gpiozero import Motor

# Ustawienie pinów GPIO dla silników
motor_left = Motor(forward=17, backward=18)
motor_right = Motor(forward=22, backward=23)

pygame.init()
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption("Car Control")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        motor_left.forward()
        motor_right.forward()
    elif keys[pygame.K_s]:
        motor_left.backward()
        motor_right.backward()
    elif keys[pygame.K_a]:
        motor_left.backward()
        motor_right.forward()
    elif keys[pygame.K_d]:
        motor_left.forward()
        motor_right.backward()
    else:
        motor_left.stop()
        motor_right.stop()

    time.sleep(0.1)

pygame.quit()
