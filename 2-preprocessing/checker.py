import pandas as pd

# Baca file CSV
df = pd.read_csv("tweet_label_manual.csv")

# Hitung jumlah label sentimen
sentimen_counts = df['label_sentimen'].value_counts(dropna=False)

# Cetak jumlah masing-masing sentimen
print("Jumlah Sentimen:")
print(f"Positif : {sentimen_counts.get('positif', 0)}")
print(f"Negatif : {sentimen_counts.get('negatif', 0)}")
print(f"Netral  : {sentimen_counts.get('netral',  0)}")
print(f"Belum Dilabeli : {df['label_sentimen'].isna().sum()}")

# Ambil Tweet Id yang belum dilabeli
unlabeled_ids = df[df['label_sentimen'].isna()]['Tweet Id'].tolist()

print("\nTweet ID yang belum diberi label:")
for tweet_id in unlabeled_ids:
    print(tweet_id)