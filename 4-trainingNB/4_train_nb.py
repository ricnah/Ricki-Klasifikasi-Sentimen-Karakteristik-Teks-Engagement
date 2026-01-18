# ==========================
# File: 4_train_naive_bayes.py
# ==========================
import pickle
from sklearn.naive_bayes import MultinomialNB

# Load data TF-IDF TRAIN
with open("X_train_tfidf.pkl", "rb") as f:
    X_train = pickle.load(f)

with open("y_train.pkl", "rb") as f:
    y_train = pickle.load(f)

# ===============================
# Latih model Naive Bayes
# ===============================
model = MultinomialNB()
model.fit(X_train, y_train)

# Simpan model
with open("naive_bayes_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model Naive Bayes berhasil dilatih (80% data)")
