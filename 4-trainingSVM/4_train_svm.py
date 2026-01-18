# ==========================
# File: 4_train_svm.py
# ==========================
import pickle
from sklearn.svm import LinearSVC

# Load data TRAIN
with open("X_train_tfidf.pkl", "rb") as f:
    X_train = pickle.load(f)

with open("y_train.pkl", "rb") as f:
    y_train = pickle.load(f)

# ===============================
# Latih model SVM
# ===============================
model = LinearSVC(random_state=42)
model.fit(X_train, y_train)

# Simpan model
with open("svm_linear_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model SVM Linear berhasil dilatih (80% data)")
