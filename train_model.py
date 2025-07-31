import os
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Path data
DATA_DIR = 'data'
GESTURES = ['hi', 'my_name_is', 'bastian', 'nice_to_meet_u']

# Load data
X = []
y = []

for label in GESTURES:
    folder_path = os.path.join(DATA_DIR, label)
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    X.append([float(val) for val in row])
                    y.append(label)

# Convert ke numpy array
X = np.array(X)
y = np.array(y)

# Split train-test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluasi
acc = clf.score(X_test, y_test)
print(f"[✓] Akurasi model: {acc*100:.2f}%")

# Simpan model
with open('gesture_model.pkl', 'wb') as f:
    pickle.dump(clf, f)

print("[✓] Model disimpan sebagai 'gesture_model.pkl'")
