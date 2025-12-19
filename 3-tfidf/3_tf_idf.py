# ==========================
# File: 5_tfidf_vectorization.py
# ==========================
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np

# Load data tweet yang sudah dilabeli
df = pd.read_csv("tweet_prepro_label_manual.csv")  # Berisi 1000 tweet

# Hapus data kosong pada kolom penting di preprocessed
df = df.dropna(subset=['Preprocessed'])

# TF-IDF vektorisasi pada kolom Preprocessed
vectorizer = TfidfVectorizer(max_features=5000)
X_tfidf = vectorizer.fit_transform(df['Preprocessed'])

# Label sentimen
y = df['label_sentimen']

# ===============================
# 1️⃣ Simpan vectorizer & matriks TF-IDF
# ===============================
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("X_tfidf.pkl", "wb") as f:
    pickle.dump(X_tfidf, f)

with open("y_labels.pkl", "wb") as f:
    pickle.dump(y, f)

# ===============================
# 2️⃣ Simpan dataframe asli untuk keperluan lain
# ===============================
df.to_csv("tweet_tfidf.csv", index=False)

# ===============================
# 3️⃣ Ekspor seluruh matriks TF-IDF ke CSV
# ⚠️ Bisa besar, tapi aman untuk penelitian
# ===============================
feature_names = vectorizer.get_feature_names_out()
tfidf_dense = X_tfidf.toarray()

full_tfidf_df = pd.DataFrame(tfidf_dense, columns=feature_names)
full_tfidf_df.to_csv("tfidf_matrix_full.csv", index=False)

# ===============================
# 4️⃣ Ekspor versi ringkas untuk laporan (10 tweet × 20 kata)
# ===============================
sample_tfidf_df = pd.DataFrame(tfidf_dense[:10, :20], columns=feature_names[:20])
sample_tfidf_df.to_csv("tfidf_matrix_sample.csv", index=False)

print("=============================================")
print("✅ Semua file TF-IDF berhasil dibuat:")
print("- tfidf_vectorizer.pkl")
print("- X_tfidf.pkl")
print("- y_labels.pkl")
print("- tweet_tfidf.csv")
print("- tfidf_matrix_full.csv  (seluruh matriks TF-IDF)")
print("- tfidf_matrix_sample.csv (contoh untuk laporan)")
print("=============================================")
