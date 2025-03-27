import pygame
import pigpio

pi = pigpio.pi()
pan_servo = 18   
tilt_servo = 19 

pan_angle = 90 
tilt_angle = 90

def set_servo_angle(pin, angle):
    pwm = 500 + (angle / 180.0) * 2000
    pi.set_servo_pulsewidth(pin, pwm)

display_width, display_height = 640, 480
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Sterowanie kamerą myszką")
clock = pygame.time.Clock()

set_servo_angle(pan_servo, pan_angle)
set_servo_angle(tilt_servo, tilt_angle)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            pan_angle = int((x / display_width) * 180)
            tilt_angle = int((y / display_height) * 180)
            set_servo_angle(pan_servo, pan_angle)
            set_servo_angle(tilt_servo, tilt_angle)

    screen.fill((0, 0, 0))
    pygame.display.update()
    clock.tick(30)

pi.stop()
pygame.quit()

#sudo apt install pigpio
#pip install pygame
#sudo pigpiod
#python3 camera_mouse_control.py





















