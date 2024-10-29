import cv2
import numpy as np
import serial
import time
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

def count_fingers(hand_landmarks):
    fingers = 0
    if hand_landmarks[4][1] < hand_landmarks[3][1]:
        fingers += 1
    if hand_landmarks[8][1] < hand_landmarks[7][1]:
        fingers += 1
    if hand_landmarks[12][1] < hand_landmarks[11][1]:
        fingers += 1
    if hand_landmarks[16][1] < hand_landmarks[15][1]: 
        fingers += 1
    if hand_landmarks[20][1] < hand_landmarks[19][1]:
        fingers += 1
    return fingers

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hand_landmarks = []
    if hand_landmarks:
        fingers = count_fingers(hand_landmarks)

        if fingers == 0:
            arduino.write(b'F')
        elif fingers == 5:
            arduino.write(b'S')
        elif fingers == 1:
            arduino.write(b'H')
        elif fingers == 2:
            arduino.write(b'R') 

    
    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
