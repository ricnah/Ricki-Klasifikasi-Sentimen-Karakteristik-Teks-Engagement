# ==========================
# File: 7_evaluate_model.py
# ==========================
import pickle
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load model dan data uji
with open("naive_bayes_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("X_test.pkl", "rb") as f:
    X_test = pickle.load(f)

with open("y_test.pkl", "rb") as f:
    y_test = pickle.load(f)

# Prediksi
y_pred = model.predict(X_test)

# Evaluasi
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

print("\n🧱 Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Visualisasi Confusion Matrix
labels = sorted(list(set(y_test)))  # Pastikan urutan label sama
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.show()
