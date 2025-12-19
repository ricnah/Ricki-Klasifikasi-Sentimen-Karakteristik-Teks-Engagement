import pandas as pd
from tqdm import tqdm
import time

# Inisialisasi tqdm untuk satu proses besar
tqdm.pandas(desc="Memproses data")

# Baca file CSV hasil preprocessing
print("Membaca file tweet_preprocessed.csv...")
df = pd.read_csv('rickipositif_tweets_raw.csv')

# Simulasikan proses sampling dengan bar (walau sebenarnya instan)
print("Mengambil 400 tweet secara acak...")
for _ in tqdm(range(1), desc="Sampling tweet"):
    sampled = df.sample(n=400, random_state=42)
    time.sleep(0.5)  # hanya untuk mensimulasikan waktu proses

# Simpan hasil ke file baru
print("Menyimpan hasil ke tweet_for_labeling.csv...")
for _ in tqdm(range(1), desc="Menyimpan file"):
    sampled.to_csv('sampleacak.csv', index=False)
    time.sleep(0.5)  # simulasi delay

print("✅ 400 tweet acak berhasil diambil dan disimpan ke: sampleacak.csv")
