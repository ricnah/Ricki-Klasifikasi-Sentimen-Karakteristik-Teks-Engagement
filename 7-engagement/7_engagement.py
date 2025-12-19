import pandas as pd
from tqdm import tqdm
from mlxtend.frequent_patterns import fpgrowth, association_rules

# ==== 1. BACA FILE CSV ====
file_input = "predictsentiment.csv"
file_output = "engagement4.csv"

df = pd.read_csv(file_input)
print(f"✅ File '{file_input}' berhasil dibaca. Jumlah baris: {len(df)}")

# Pastikan kolom numerik
for col in ['Like', 'Retweet', 'Reply', 'views']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# ==== 2. HITUNG ANGKA ENGAGEMENT ====
df['angka_engagement'] = df['Like'] + df['Retweet'] + df['Reply'] + df['views']

# ==== 3. HITUNG KUARTIL DAN BUAT KATEGORI ====
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
print("Kategori: Rendah, Sedang, Tinggi\n")

# ==== 4. SIMPAN HASIL KE CSV BARU ====
df.to_csv(file_output, index=False, encoding='utf-8-sig')
print(f"✅ Kolom 'angka_engagement' & 'kategori_engagement' berhasil ditambahkan.")
print(f"📁 File hasil: {file_output}")

# ==== 5. ANALISIS ASOSIASI ====
fitur_asosiasi = [
    'Preprocessed','label_sentimen','Has Media','Total Media','Mengandung Link','Jumlah Tautan',
    'Panjang Teks','Jumlah Emoji','Huruf Kapital','Kata Persuasif',
    'Layanan Disebut','Layanan Disebut Nama','Hashtag','Jumlah Hashtags',
    'Verified','Mention','Jumlah Mention','kategori_engagement'
]

df_asosiasi = df[fitur_asosiasi].copy()

# Ubah kolom non-numerik → string → one-hot encoding (0/1)
df_dummies = pd.get_dummies(df_asosiasi.astype(str))

print("\n🔍 Melakukan analisis asosiasi (FP-Growth)...")

# Temukan frequent itemsets
frequent_itemsets = fpgrowth(df_dummies, min_support=0.1, use_colnames=True)

# Bentuk aturan asosiasi
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

# ==== 6. PISAHKAN ATURAN BERDASARKAN KATEGORI ENGAGEMENT ====
rules_rendah = rules[rules['consequents'].astype(str).str.contains('kategori_engagement_rendah')]
rules_sedang = rules[rules['consequents'].astype(str).str.contains('kategori_engagement_sedang')]
rules_tinggi = rules[rules['consequents'].astype(str).str.contains('kategori_engagement_tinggi')]

# Urutkan berdasarkan lift tertinggi
rules_rendah = rules_rendah.sort_values(by='lift', ascending=False)
rules_sedang = rules_sedang.sort_values(by='lift', ascending=False)
rules_tinggi = rules_tinggi.sort_values(by='lift', ascending=False)

# ==== 7. TAMPILKAN HASIL TANPA TERPOTONG ====
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_rows', None)
pd.set_option('display.colheader_justify', 'center')

print("\n📉 Aturan Engagement Rendah (Top 5):")
print(rules_rendah[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(5))

print("\n📊 Aturan Engagement Sedang (Top 5):")
print(rules_sedang[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(5))

print("\n📈 Aturan Engagement Tinggi (Top 5):")
print(rules_tinggi[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(5))

# ==== 8. SIMPAN SEMUA HASIL KE FILE CSV UNTUK SKRIPSI ====
rules_rendah.to_csv("hasil_asosiasi_rendah.csv", index=False, encoding='utf-8-sig')
rules_sedang.to_csv("hasil_asosiasi_sedang.csv", index=False, encoding='utf-8-sig')
rules_tinggi.to_csv("hasil_asosiasi_tinggi.csv", index=False, encoding='utf-8-sig')

print("\n📄 File hasil disimpan sebagai:")
print("   - hasil_asosiasi_rendah.csv")
print("   - hasil_asosiasi_sedang.csv")
print("   - hasil_asosiasi_tinggi.csv")
