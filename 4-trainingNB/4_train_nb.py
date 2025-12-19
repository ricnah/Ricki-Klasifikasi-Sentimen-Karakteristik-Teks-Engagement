# ==========================
# File: 4_train_test_model.py
# ==========================
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Load TF-IDF dan label
df = pd.read_csv("tweet_tfidf.csv")

with open("X_tfidf.pkl", "rb") as f:
    X = pickle.load(f)

with open("y_labels.pkl", "rb") as f:
    y = pickle.load(f)

# Split data latih dan data uji (80:20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Latih model Naive Bayes Multinomial
model = MultinomialNB()
model.fit(X_train, y_train)

# Simpan model
with open("naive_bayes_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Simpan data uji untuk evaluasi
with open("X_test.pkl", "wb") as f:
    pickle.dump(X_test, f)

with open("y_test.pkl", "wb") as f:
    pickle.dump(y_test, f)

print("✅ Model Naive Bayes selesai dilatih dan disimpan.")