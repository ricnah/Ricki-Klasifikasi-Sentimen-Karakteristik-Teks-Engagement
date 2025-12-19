# ==========================
# File: 8_predict_sentimen_dan_analisis.py
# ==========================
import pandas as pd
import pickle
from tqdm import tqdm

# Load data semua tweet (18.463 tweet)
df_all = pd.read_csv("tweet_preprocessed_new.csv")
df_all = df_all.dropna(subset=['Preprocessed'])

# Load vectorizer dan model
with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("naive_bayes_model.pkl", "rb") as f:
    model = pickle.load(f)

# Transformasi dan prediksi dengan progress bar
print("🔄 Melakukan prediksi sentimen...")
X_all = vectorizer.transform(df_all['Preprocessed'])
df_all['sentimen_prediksi'] = list(tqdm(model.predict(X_all), total=X_all.shape[0]))

# Simpan hasil
df_all.to_csv("predict_tweet_sentiment.csv", index=False)

print("✅ Prediksi sentimen selesai dan disimpan ke predict_tweet_sentiment.csv")