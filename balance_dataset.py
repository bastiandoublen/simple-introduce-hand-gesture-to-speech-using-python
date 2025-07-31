import os
import shutil
import time
from datetime import datetime
import random

DATA_DIR = 'dataset'

def duplicate_file(source_file, target_dir):
    """Duplikasi file dengan nama unik"""
    base_name = os.path.splitext(os.path.basename(source_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    new_name = f"{base_name}_dup_{timestamp}.csv"
    new_path = os.path.join(target_dir, new_name)
    shutil.copy2(source_file, new_path)

def balance_gesture_dataset(data_dir):
    gesture_counts = {}
    
    # Hitung file per gesture
    for folder in os.listdir(data_dir):
        gesture_path = os.path.join(data_dir, folder)
        if os.path.isdir(gesture_path):
            count = len([f for f in os.listdir(gesture_path) if f.endswith('.csv')])
            gesture_counts[folder] = count

    max_count = max(gesture_counts.values())

    print("Jumlah awal:")
    for g, c in gesture_counts.items():
        print(f" - {g}: {c} file")

    # Mulai duplikasi file untuk gesture yang jumlahnya kurang
    for gesture, count in gesture_counts.items():
        if count < max_count:
            folder_path = os.path.join(data_dir, gesture)
            files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
            print(f"\n[✓] Menyeimbangkan folder '{gesture}' ({count} → {max_count})")

            for i in range(max_count - count):
                source_file = os.path.join(folder_path, random.choice(files))
                duplicate_file(source_file, folder_path)
                time.sleep(0.01)  # biar timestamp beda

    print("\n✅ Dataset sudah seimbang.")

# Jalankan
balance_gesture_dataset(DATA_DIR)
