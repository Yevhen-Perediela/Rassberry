import pygame
import time
from motor import Ordinary_Car
from picamera2 import Picamera2
import cv2
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# --- Inicjalizacja PCA9685 ---
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz dla serw

# --- Kanały serw ---
PAN_CHANNEL = 0
TILT_CHANNEL = 1

# --- Funkcja ustawiająca kąt (0–180) dla PCA9685 ---
def set_servo_angle(channel, angle):
    pulse = int((angle / 180.0) * 500 + 100)  # zakres 100–600 to około 0°–180°
    pulse = max(100, min(600, pulse))         # ograniczenie zakresu
    pca.channels[channel].duty_cycle = int(pulse / 20000 * 0xFFFF)

# Startowe kąty
pan_angle = 90
tilt_angle = 90
set_servo_angle(PAN_CHANNEL, pan_angle)
set_servo_angle(TILT_CHANNEL, tilt_angle)

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

        # --- Sterowanie autem ---
        if keys[pygame.K_w]:
            print('jazda')
            car.set_motor_model(1000, 1000, 1000, 1000)
        elif keys[pygame.K_s]:
            print('jazda')
            car.set_motor_model(-1000, -1000, -1000, -1000)
        elif keys[pygame.K_a]:
            print('jazda')
            car.set_motor_model(-1500, -1500, 1500, 1500)
        elif keys[pygame.K_d]:
            print('jazda')
            car.set_motor_model(1500, 1500, -1500, -1500)
        else:
            car.set_motor_model(0, 0, 0, 0)

        # --- Sterowanie kamerą (serwa przez PCA9685) ---
        if keys[pygame.K_LEFT]:
            pan_angle = max(0, pan_angle - 5)
            set_servo_angle(PAN_CHANNEL, pan_angle)
            print("Pan:", pan_angle)

        elif keys[pygame.K_RIGHT]:
            pan_angle = min(180, pan_angle + 5)
            set_servo_angle(PAN_CHANNEL, pan_angle)
            print("Pan:", pan_angle)

        elif keys[pygame.K_UP]:
            tilt_angle = max(0, tilt_angle - 5)
            set_servo_angle(TILT_CHANNEL, tilt_angle)
            print("Tilt:", tilt_angle)

        elif keys[pygame.K_DOWN]:
            tilt_angle = min(180, tilt_angle + 5)
            set_servo_angle(TILT_CHANNEL, tilt_angle)
            print("Tilt:", tilt_angle)

        # --- Podgląd z kamery ---
        frame = picam2.capture_array()
        cv2.imshow("Podgląd z kamery Raspberry Pi", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

        time.sleep(0.1)

finally:
    car.set_motor_model(0, 0, 0, 0)
    pygame.quit()
    cv2.destroyAllWindows()
    pca.deinit()
