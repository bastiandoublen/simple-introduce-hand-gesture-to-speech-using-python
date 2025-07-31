import os
import cv2
import numpy as np
import mediapipe as mp
import pickle
from gtts import gTTS
import pygame
import time

# Load model gesture
with open("gesture_model.pkl", "rb") as f:
    model = pickle.load(f)

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Inisialisasi pygame mixer
pygame.init(

)
pygame.mixer.init()

# Label gesture
label_map = {
    'hi': "Hi",
    'my_name_is': "My name is",
    'your_name': "your_name",
    'nice_to_meet_u': "Nice to meet you"
}

# Generate audio jika belum ada
os.makedirs("speech", exist_ok=True)
for key, text in label_map.items():
    path = os.path.join("speech", f"{key}.mp3")
    if not os.path.exists(path):
        gTTS(text=text, lang='en').save(path)

# Cooldown audio
last_prediction = ""
last_time_spoken = time.time()
cooldown = 1.5

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    h, w, _ = frame.shape

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        # Ekstrak fitur dan prediksi
        features = []
        for lm in landmarks.landmark:
            features.extend([lm.x, lm.y, lm.z])
        prediction = model.predict([features])[0]

        if prediction != last_prediction and time.time() - last_time_spoken > cooldown:
            last_prediction = prediction
            last_time_spoken = time.time()
            pygame.mixer.music.load(os.path.join("speech", f"{prediction}.mp3"))
            pygame.mixer.music.play()

        cv2.putText(frame, label_map[prediction], (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.5, (255, 0, 0), 3)

    cv2.imshow("cam drawing", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
