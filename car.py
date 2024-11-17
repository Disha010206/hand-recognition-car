import cv2
import serial
import time
import mediapipe as mp

arduino = serial.Serial('COM3', 9600)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

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

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    hand_landmarks = []
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmark.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                hand_landmarks.append((cx, cy))
            mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

    if hand_landmarks:
        fingers = count_fingers(hand_landmarks)
        if fingers == 1:
            arduino.write(b'F')
        elif fingers == 5:
            arduino.write(b'S')
        elif fingers == 2:
            arduino.write(b'H')
        elif fingers == 3:
            arduino.write(b'R')
        #print(fingers)
    cv2.imshow("Hand Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

cv2.destroyAllWindows()
