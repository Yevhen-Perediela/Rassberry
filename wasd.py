import pygame
import time
from motor import Ordinary_Car
from picamera2 import Picamera2
import cv2

# --- Inicjalizacja kamery ---
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "BGR888"
picam2.configure("preview")
picam2.start()

# --- Inicjalizacja samochodu ---
car = Ordinary_Car()

# --- Inicjalizacja pygame ---
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

        # --- Sterowanie ruchem ---
        if keys[pygame.K_w]:
            print('jazda')
            car.set_motor_model(1000, 1000, 1000, 1000)  # Do przodu
        elif keys[pygame.K_s]:
            print('jazda')
            car.set_motor_model(-1000, -1000, -1000, -1000)  # Do tyłu
        elif keys[pygame.K_a]:
            print('jazda')
            car.set_motor_model(-1500, -1500, 1500, 1500)  # Skręt w lewo
        elif keys[pygame.K_d]:
            print('jazda')
            car.set_motor_model(1500, 1500, -1500, -1500)  # Skręt w prawo
        else:
            car.set_motor_model(0, 0, 0, 0)  # Stop

        # --- Podgląd z kamery ---
        frame = picam2.capture_array()
        cv2.imshow("Podgląd z kamery Raspberry Pi", frame)

        # Zamknięcie po naciśnięciu Q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

        time.sleep(0.1)

finally:
    car.set_motor_model(0, 0, 0, 0)
    pygame.quit()
    cv2.destroyAllWindows()
