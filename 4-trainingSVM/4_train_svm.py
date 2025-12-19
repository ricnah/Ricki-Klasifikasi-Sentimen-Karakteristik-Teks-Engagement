# ==========================
# File: 4_train_svm.py
# ==========================
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

# Load TF-IDF dan label
df = pd.read_csv("tweet_tfidf.csv")

with open("X_tfidf.pkl", "rb") as f:
    X = pickle.load(f)

with open("y_labels.pkl", "rb") as f:
    y = pickle.load(f)

# Split data latih dan data uji (80:20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Inisialisasi model SVM dengan kernel linear
model = LinearSVC(random_state=42)

# Latih model
model.fit(X_train, y_train)

# Simpan model SVM
with open("svm_linear_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Simpan data uji untuk evaluasi
with open("X_test_svm.pkl", "wb") as f:
    pickle.dump(X_test, f)

with open("y_test_svm.pkl", "wb") as f:
    pickle.dump(y_test, f)

print("✅ Model SVM Linear selesai dilatih dan disimpan.")
