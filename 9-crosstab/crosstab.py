# --- Import library ---
import pandas as pd
from tqdm import tqdm
import os

# --- 1️⃣ Baca data ---
df = pd.read_csv("hasil_kategori.csv")

# --- 2️⃣ Pastikan kolom penting ada ---
cols = [
    'Preprocessed','label_sentimen','Has Media','Total Media','Mengandung Link','Jumlah Tautan',
    'Panjang Teks','Jumlah Emoji','Huruf Kapital','Kata Persuasif',
    'Layanan Disebut','Layanan Disebut Nama','Hashtag','Jumlah Hashtags',
    'Verified','Mention','Jumlah Mention','kategori_engagement'
]

missing = [c for c in cols if c not in df.columns]
if missing:
    raise ValueError(f"Kolom berikut tidak ditemukan di dataset: {missing}")

# --- 3️⃣ Daftar fitur yang ingin dikrosstab ---
fitur_analisis = [
    'Has Media','Total Media','Mengandung Link','Jumlah Tautan',
    'Panjang Teks','Jumlah Emoji','Huruf Kapital','Kata Persuasif',
    'Layanan Disebut','Layanan Disebut Nama','Hashtag','Jumlah Hashtags',
    'Verified','Mention','Jumlah Mention'
]

# --- 4️⃣ Siapkan list hasil ---
hasil_semua = []

print("\n🚀 Membuat Crosstab semua fitur dan summary 3 sheet...\n")

# --- 5️⃣ Loop fitur dengan progress bar ---
for fitur in tqdm(fitur_analisis, desc="Proses fitur", unit="fitur"):
    ct = pd.crosstab(
        [df['label_sentimen'], df['kategori_engagement']],
        df[fitur]
    )

    ct_reset = ct.reset_index().melt(id_vars=['label_sentimen','kategori_engagement'])
    ct_reset['fitur'] = fitur
    hasil_semua.append(ct_reset)

# --- 6️⃣ Gabungkan semua hasil ---
final_df = pd.concat(hasil_semua, ignore_index=True)
final_df = final_df.rename(columns={'variable':'Nilai', 'value':'Frekuensi'})

# --- 7️⃣ Hitung persentase per grup fitur–sentimen–engagement ---
final_df['Persentase (%)'] = (
    final_df.groupby(['fitur','label_sentimen','kategori_engagement'])['Frekuensi']
    .transform(lambda x: (x / x.sum()) * 100)
    .round(2)
)

# --- 8️⃣ Buat summary per kategori engagement ---
def buat_summary(kategori):
    df_sub = final_df[final_df['kategori_engagement'] == kategori]
    summary = (
        df_sub.groupby(['fitur','label_sentimen'], as_index=False)
        .agg({'Frekuensi':'sum','Persentase (%)':'mean'})
        .sort_values(by='Frekuensi', ascending=False)
    )
    summary['Persentase (%)'] = summary['Persentase (%)'].round(2)
    return summary

summary_tinggi = buat_summary('tinggi')
summary_sedang = buat_summary('sedang')
summary_rendah = buat_summary('rendah')

# --- 9️⃣ Simpan ke Excel dengan 3 sheet ---
os.makedirs("hasil_crosstab_allfitur", exist_ok=True)
output_path = "hasil_crosstab_allfitur/crosstab_allfitur_3sheet.xlsx"

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, sheet_name="Crosstab_AllFitur", index=False)
    summary_tinggi.to_excel(writer, sheet_name="Summary_Eng_Tinggi", index=False)
    summary_sedang.to_excel(writer, sheet_name="Summary_Eng_Sedang", index=False)
    summary_rendah.to_excel(writer, sheet_name="Summary_Eng_Rendah", index=False)

print("\n✅ Semua Crosstab dan Summary selesai dibuat!")
print(f"📁 File hasil: {output_path}")
