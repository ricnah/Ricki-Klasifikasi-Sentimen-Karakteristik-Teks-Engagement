# ==========================
# File: 5_evaluate_model.py
# ==========================
import pickle
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# ===============================
# Load model (NB atau SVM)
# ===============================
with open("svm_linear_model.pkl", "rb") as f:
    model = pickle.load(f)

# ===============================
# Load data TEST (20%)
# ===============================
with open("X_test_tfidf.pkl", "rb") as f:
    X_test = pickle.load(f)

with open("y_test.pkl", "rb") as f:
    y_test = pickle.load(f)

# ===============================
# Prediksi & evaluasi
# ===============================
y_pred = model.predict(X_test)

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)

print("\n🧱 Confusion Matrix:")
print(cm)

# Visualisasi
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.show()
