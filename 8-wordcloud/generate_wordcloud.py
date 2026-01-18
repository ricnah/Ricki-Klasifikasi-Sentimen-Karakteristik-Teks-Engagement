# --- Import library ---
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import os
from tqdm import tqdm  # ✅ untuk progress bar

# --- 1️⃣ Baca data CSV ---
# Ganti path sesuai file kamu
df = pd.read_csv("hasil_kategori.csv")

# Pastikan kolom penting ada
required_cols = ['Preprocessed', 'label_sentimen', 'kategori_engagement']
for c in required_cols:
    if c not in df.columns:
        raise ValueError(f"Kolom '{c}' tidak ditemukan di dataset!")

# --- 2️⃣ Siapkan folder hasil ---
os.makedirs("hasil_wordcloud", exist_ok=True)
os.makedirs("hasil_kata_csv", exist_ok=True)

# --- 3️⃣ Dapatkan semua kombinasi unik sentimen × engagement ---
kombinasi = [
    (s, e)
    for s in df['label_sentimen'].unique()
    for e in df['kategori_engagement'].unique()
]

# --- 4️⃣ Loop dengan progress bar ---
for sentimen, engage in tqdm(kombinasi, desc="🔄 Membuat WordCloud", unit="kombinasi"):
    subset = df[(df['label_sentimen'] == sentimen) & (df['kategori_engagement'] == engage)]

    if subset.empty:
        continue

    # Gabungkan semua teks
    teks_gabungan = " ".join(subset['Preprocessed'].astype(str))

    # --- 5️⃣ Buat WordCloud ---
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='white',
        colormap='viridis',
        max_words=200
    ).generate(teks_gabungan)

    # --- 6️⃣ Tampilkan dan simpan gambar ---
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"WordCloud: {sentimen.upper()} - Engagement {engage.upper()}", fontsize=16)
    plt.savefig(f"hasil_wordcloud/{sentimen}_{engage}.png", bbox_inches='tight')
    plt.close()

    # --- 7️⃣ Simpan frekuensi kata ke CSV ---
    kata_list = teks_gabungan.split()
    kata_counter = Counter(kata_list)
    kata_df = pd.DataFrame(kata_counter.most_common(30), columns=['Kata', 'Frekuensi'])
    kata_df.to_csv(f"hasil_kata_csv/{sentimen}_{engage}.csv", index=False)

print("\n✅ WordCloud & CSV kata berhasil dibuat di folder 'hasil_wordcloud' dan 'hasil_kata_csv'")
