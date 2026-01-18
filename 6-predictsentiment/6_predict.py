# ==========================
# File: 6_predict.py
# ==========================
import pandas as pd
import pickle
from tqdm import tqdm

# Load data semua tweet
df_all = pd.read_csv("data_mentah_preprocessed.csv")
df_all = df_all.dropna(subset=['Preprocessed'])

# Load vectorizer dan model
with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("svm_linear_model.pkl", "rb") as f:
    model = pickle.load(f)

# Transformasi dan prediksi
print("🔄 Melakukan prediksi sentimen...")
X_all = vectorizer.transform(df_all['Preprocessed'])
df_all['sentimen_prediksi'] = list(
    tqdm(model.predict(X_all), total=X_all.shape[0])
)

# ==========================
# ANALISIS HASIL PREDIKSI
# ==========================
label_valid = ['positif', 'negatif', 'netral']

jumlah_positif = (df_all['sentimen_prediksi'] == 'positif').sum()
jumlah_negatif = (df_all['sentimen_prediksi'] == 'negatif').sum()
jumlah_netral  = (df_all['sentimen_prediksi'] == 'netral').sum()

df_belum = df_all[~df_all['sentimen_prediksi'].isin(label_valid)]
jumlah_belum = len(df_belum)

# ==========================
# PRINT KE TERMINAL
# ==========================
print("\n📊 HASIL PREDIKSI SENTIMEN")
print(f"Positif : {jumlah_positif}")
print(f"Negatif : {jumlah_negatif}")
print(f"Netral  : {jumlah_netral}")
print(f"Belum Dilabeli : {jumlah_belum}")

print("\n🆔 Tweet ID yang belum diberi label:")
if jumlah_belum > 0:
    for tweet_id in df_belum['Tweet Id'].tolist():
        print(tweet_id)
else:
    print("- Tidak ada -")

# ==========================
# SIMPAN HASIL
# ==========================
output_file = "predict_sentiment_SVM.csv"
df_all.to_csv(output_file, index=False)
print(f"\n✅ Prediksi sentimen selesai dan disimpan ke {output_file}")
