import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Kamera znaleziona na indexie: {i}")
        cap.release()
    else:
        print(f"Brak kamery na indexie: {i}")
