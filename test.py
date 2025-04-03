import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

pwm = GPIO.PWM(12, 50)
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)

try:
    while True:
        angle = int(input("Podaj kąt (0–180): "))
        set_angle(angle)
        time.sleep(0.5)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
