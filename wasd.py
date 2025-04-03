import pygame
import time
from motor import Motor
from picamera2 import Picamera2
from motor import Ordinary_Car
import cv2

# --- Kamera ---
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "BGR888"
picam2.configure("preview")
picam2.start()

PwM = Ordinary_Car()

# --- Silniki ---
motor_left = Motor(forward=17, backward=18)
motor_right = Motor(forward=22, backward=23)

# --- Pygame do sterowania ---
pygame.init()
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption("Car + Camera Control")

running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Sterowanie silnikami
        if keys[pygame.K_w]:
            PwM.set_motor_model(-1000, -1000, -1000, -1000)
        elif keys[pygame.K_s]:
            PwM.set_motor_model(1000, 1000, 1000, 1000)
        elif keys[pygame.K_a]:
            PwM.set_motor_model(1000, 1000, -1000, -1000)
        elif keys[pygame.K_d]:
            PwM.set_motor_model(-1000, -1000, 1000, 1000)
        else:
            PwM.set_motor_model(0, 0, 0, 0)

        # Wyświetlanie obrazu z kamery
        frame = picam2.capture_array()
        cv2.imshow("Podgląd z kamery Raspberry Pi", frame)

        # Wyjście z programu po wciśnięciu klawisza 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

        time.sleep(0.1)

finally:
    motor_left.stop()
    motor_right.stop()
    pygame.quit()
    cv2.destroyAllWindows()
