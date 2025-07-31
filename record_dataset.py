import os
import cv2
import mediapipe as mp
import csv
from datetime import datetime

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# Label mapping untuk tombol keyboard
gesture_labels = {
    'h': 'hi',
    'm': 'my_name_is',
    'b': 'bastian',
    'n': 'nice_to_meet_u'
}

# Buat folder data kalau belum ada
DATA_DIR = 'dataset'
os.makedirs(DATA_DIR, exist_ok=True)
for label in gesture_labels.values():
    os.makedirs(os.path.join(DATA_DIR, label), exist_ok=True)

# Mulai capture
cap = cv2.VideoCapture(0)
print("Tekan [h] [m] [b] [n] untuk menyimpan data gesture. Tekan [q] untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Recorder", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    if chr(key) in gesture_labels and results.multi_hand_landmarks:
        label = gesture_labels[chr(key)]
        landmark_list = []

        hand = results.multi_hand_landmarks[0]
        for lm in hand.landmark:
            landmark_list.extend([lm.x, lm.y, lm.z])

        # Simpan data ke file CSV di folder yang sesuai
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = f"{label}_{timestamp}.csv"
        filepath = os.path.join(DATA_DIR, label, filename)

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(landmark_list)

        print(f"[✓] Data '{label}' disimpan di {filepath}")

cap.release()
cv2.destroyAllWindows()
