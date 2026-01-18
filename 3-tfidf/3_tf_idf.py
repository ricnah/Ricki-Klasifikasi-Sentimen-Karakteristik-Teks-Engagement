# ==========================
# File: 5_tfidf_vectorization.py
# ==========================
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np

# ===============================
# 1️⃣ Load data TRAIN & TEST hasil split
# ===============================
train_df = pd.read_csv("train_80.csv")
test_df = pd.read_csv("test_20.csv")

# Hapus data kosong (aman)
train_df = train_df.dropna(subset=["Preprocessed", "label_sentimen"])
test_df = test_df.dropna(subset=["Preprocessed", "label_sentimen"])

X_train_text = train_df["Preprocessed"]
y_train = train_df["label_sentimen"]

X_test_text = test_df["Preprocessed"]
y_test = test_df["label_sentimen"]

# ===============================
# 2️⃣ TF-IDF (FIT HANYA DATA TRAIN)
# ===============================
vectorizer = TfidfVectorizer(max_features=5000)

X_train_tfidf = vectorizer.fit_transform(X_train_text)
X_test_tfidf = vectorizer.transform(X_test_text)

# ===============================
# 3️⃣ Simpan vectorizer & hasil TF-IDF (PKL)
# ===============================
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("X_train_tfidf.pkl", "wb") as f:
    pickle.dump(X_train_tfidf, f)

with open("X_test_tfidf.pkl", "wb") as f:
    pickle.dump(X_test_tfidf, f)

with open("y_train.pkl", "wb") as f:
    pickle.dump(y_train, f)

with open("y_test.pkl", "wb") as f:
    pickle.dump(y_test, f)

# ===============================
# 4️⃣ Ekspor FULL matriks TF-IDF ke CSV (TRAIN)
# ===============================
feature_names = vectorizer.get_feature_names_out()

tfidf_dense = X_train_tfidf.toarray()

full_tfidf_df = pd.DataFrame(
    tfidf_dense,
    columns=feature_names
)

full_tfidf_df.to_csv(
    "tfidf_matrix_train_full.csv",
    index=False,
    encoding="utf-8-sig"
)

print("=============================================")
print("✅ TF-IDF selesai (FULL matrix diekspor)")
print("- FIT hanya TRAIN (train_80.csv)")
print("- File CSV: tfidf_matrix_train_full.csv")
print("⚠️ Catatan: ukuran file bisa besar")
print("=============================================")
