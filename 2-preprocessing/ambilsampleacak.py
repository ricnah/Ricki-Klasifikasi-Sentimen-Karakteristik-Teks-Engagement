import pandas as pd
from tqdm import tqdm
import time

# Inisialisasi tqdm untuk satu proses besar
tqdm.pandas(desc="Memproses data")

# Baca file CSV hasil preprocessing
print("Membaca file ricki127_tweets-data_mentah.csv...")
df = pd.read_csv('ricki127_tweets-data_mentah.csv')

# Simulasikan proses sampling dengan bar (walau sebenarnya instan)
print("Mengambil 1400 tweet secara acak...")
for _ in tqdm(range(1), desc="Sampling tweet"):
    sampled = df.sample(n=1400, random_state=42)
    time.sleep(0.5)  # hanya untuk mensimulasikan waktu proses

# Simpan hasil ke file baru
print("Menyimpan hasil ke hasil_sampleacak_2.csv...")
for _ in tqdm(range(1), desc="Menyimpan file"):
    sampled.to_csv('hasil_sampleacak_2.csv', index=False)
    time.sleep(0.5)  # simulasi delay

print("✅ 1400 tweet acak berhasil diambil dan disimpan ke: hasil_sampleacak_2.csv")
