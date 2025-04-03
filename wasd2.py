import pygame
import time
import RPi.GPIO as GPIO
from motor import Ordinary_Car
from picamera2 import Picamera2
import cv2

# --- Inicjalizacja GPIO dla serw ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PAN_PIN = 12
TILT_PIN = 13

GPIO.setup(PAN_PIN, GPIO.OUT)
GPIO.setup(TILT_PIN, GPIO.OUT)

pan_pwm = GPIO.PWM(PAN_PIN, 50)  # 50 Hz
tilt_pwm = GPIO.PWM(TILT_PIN, 50)

pan_pwm.start(7.5)   # środek
tilt_pwm.start(7.5)

# Funkcja do ustawiania kąta serwa (0–180)
def set_servo_angle(pwm, angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)

pan_angle = 90
tilt_angle = 90

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

        # --- Sterowanie ruchem auta ---
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

        # --- Sterowanie kamerą strzałkami ---
        if keys[pygame.K_LEFT]:
            pan_angle = max(0, pan_angle - 5)
            set_servo_angle(pan_pwm, pan_angle)
            print("Pan:", pan_angle)

        elif keys[pygame.K_RIGHT]:
            pan_angle = min(180, pan_angle + 5)
            set_servo_angle(pan_pwm, pan_angle)
            print("Pan:", pan_angle)

        elif keys[pygame.K_UP]:
            tilt_angle = max(0, tilt_angle - 5)
            set_servo_angle(tilt_pwm, tilt_angle)
            print("Tilt:", tilt_angle)

        elif keys[pygame.K_DOWN]:
            tilt_angle = min(180, tilt_angle + 5)
            set_servo_angle(tilt_pwm, tilt_angle)
            print("Tilt:", tilt_angle)

        # --- Podgląd z kamery ---
        frame = picam2.capture_array()
        cv2.imshow("Podgląd z kamery Raspberry Pi", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

        time.sleep(0.1)

finally:
    car.set_motor_model(0, 0, 0, 0)
    pan_pwm.stop()
    tilt_pwm.stop()
    GPIO.cleanup()
    pygame.quit()
    cv2.destroyAllWindows()
