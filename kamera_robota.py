import cv2

cap = cv2.VideoCapture(0)  

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  

while True:
    ret, frame = cap.read()  
    if not ret:
        print("Nie udało się przechwycić obrazu z kamery.")
        break
    
    cv2.imshow('Kamera Pi', frame) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release() 
cv2.destroyAllWindows()


#raspivid -t 0 -w 640 -h 480 -fps 30
#sudo apt update
#sudo apt install python3-opencv






















