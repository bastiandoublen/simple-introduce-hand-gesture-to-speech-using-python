import os

# Lokasi folder data
DATA_DIR = 'data'

# Target jumlah minimal yang diinginkan (ambil dari gesture dengan jumlah terbanyak)
def analyze_gesture_data(data_dir):
    gesture_counts = {}
    
    # Hitung jumlah file di tiap folder gesture
    for gesture_folder in os.listdir(data_dir):
        gesture_path = os.path.join(data_dir, gesture_folder)
        if os.path.isdir(gesture_path):
            file_count = len([f for f in os.listdir(gesture_path) if f.endswith('.csv')])
            gesture_counts[gesture_folder] = file_count

    # Tampilkan jumlahnya
    print("Jumlah file per gesture:")
    for gesture, count in gesture_counts.items():
        print(f" - {gesture}: {count} file")

    # Cari yang paling banyak untuk dijadikan target
    max_count = max(gesture_counts.values())

    print("\nRekomendasi penambahan data:")
    for gesture, count in gesture_counts.items():
        if count < max_count:
            print(f" - {gesture}: tambah {max_count - count} file")
        else:
            print(f" - {gesture}: cukup")

# Jalankan analisis
analyze_gesture_data(DATA_DIR)
