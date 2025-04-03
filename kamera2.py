from picamera2 import Picamera2
import cv2

# Inicjalizacja kamery
picam2 = Picamera2()

# Konfiguracja rozdzielczości i formatu obrazu
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "BGR888"
picam2.configure("preview")

# Start kamery
picam2.start()

# Pętla wyświetlająca obraz
while True:
    frame = picam2.capture_array()
    cv2.imshow("Podgląd z kamery Raspberry Pi", frame)

    # Naciśnij 'q', żeby zamknąć podgląd
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnienie zasobów
cv2.destroyAllWindows()
