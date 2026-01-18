import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules

# =========================
# 1️⃣ BACA DATA
# =========================
df = pd.read_csv("tweet_label_manual.csv")
print(f"\n✅ File 'tweet_label_manual.csv' berhasil dibaca. Jumlah baris: {len(df)}")

# Pastikan kolom numerik
for col in ['Like', 'Retweet', 'Reply', 'views']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# =========================
# 2️⃣ HITUNG ENGAGEMENT
# =========================
df['angka_engagement'] = df['Like'] + df['Retweet'] + df['Reply'] + df['views']

q1 = df['angka_engagement'].quantile(0.33)
q2 = df['angka_engagement'].quantile(0.66)

def kategori_engagement(x):
    if x <= q1:
        return 'rendah'
    elif x <= q2:
        return 'sedang'
    else:
        return 'tinggi'

df['kategori_engagement'] = df['angka_engagement'].apply(kategori_engagement)

print("\n📊 Batas Kuartil Engagement:")
print(f"Q1 (Rendah ≤): {q1:.2f}")
print(f"Q2 (Sedang ≤): {q2:.2f}")
print("Kategori: Rendah, Sedang, Tinggi")

# =========================
# 3️⃣ SIMPAN DATA LENGKAP
# =========================
df.to_csv("hasil_kategori.csv", index=False, encoding="utf-8-sig")
print("\n✅ File hasil_kategori.csv berhasil dibuat (data lengkap + engagement)")

# =========================
# 4️⃣ FITUR UNTUK FP-GROWTH
# =========================
fitur_fp = [
    'label_sentimen',
    'Has Media','Total Media',
    'Mengandung Link','Jumlah Tautan',
    'Hashtag','Jumlah Hashtags',
    'Mention','Jumlah Mention',
    'Verified',
    'Layanan Disebut','Layanan Disebut Nama',
    'kategori_engagement'
]

df_fp = df[fitur_fp].astype(str)
df_dummies = pd.get_dummies(df_fp)

print("\n✅ One-hot encoding selesai. Jumlah fitur:", df_dummies.shape[1])

# =========================
# 5️⃣ FP-GROWTH
# =========================
frequent_itemsets = fpgrowth(
    df_dummies,
    min_support=0.05,
    use_colnames=True
)

rules = association_rules(
    frequent_itemsets,
    metric="confidence",
    min_threshold=0.5
)

# Consequent wajib engagement
rules = rules[
    rules['consequents'].astype(str).str.contains('kategori_engagement')
]

print(f"\n📌 Total aturan asosiasi engagement: {len(rules)}")

# =========================
# 6️⃣ TOP-5 PER SENTIMEN × ENGAGEMENT (WAJIB ADA)
# =========================
hasil_final = []

for sentimen in ['negatif', 'netral', 'positif']:
    for engagement in ['rendah', 'sedang', 'tinggi']:
        subset = rules[
            rules['antecedents'].astype(str).str.contains(f"label_sentimen_{sentimen}") &
            rules['consequents'].astype(str).str.contains(f"kategori_engagement_{engagement}")
        ].sort_values(by='lift', ascending=False).head(5)

        # WALAU KURANG DARI 5 → TETAP DIMASUKKAN
        for _, row in subset.iterrows():
            hasil_final.append({
                'sentimen': sentimen,
                'kategori_engagement': engagement,
                'antecedents': row['antecedents'],
                'support': row['support'],
                'confidence': row['confidence'],
                'lift': row['lift']
            })

hasil_final = pd.DataFrame(hasil_final)

# =========================
# 7️⃣ SIMPAN HASIL FINAL
# =========================
hasil_final.to_csv("hasil_engagement.csv", index=False, encoding="utf-8-sig")

print("\n✅ Analisis FP-Growth selesai")
print("📁 File output utama:")
print("   - hasil_kategori.csv")
print("   - hasil_engagement.csv")
print(f"📊 Total rule tersimpan: {len(hasil_final)}")
