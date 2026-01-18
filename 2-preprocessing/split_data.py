import pandas as pd
from sklearn.model_selection import train_test_split

# Baca dataset berlabel (1000 data)
df = pd.read_csv("tweet_label_manual.csv")

# Fitur & label
X = df.drop(columns=["label_sentimen"])
y = df["label_sentimen"]

# Split 80:20
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2, # data test ambil 20%
    random_state=42, # pola pengambilan konsisten
    stratify=y
)

# Gabungkan kembali
train_df = X_train.copy()
train_df["label_sentimen"] = y_train

test_df = X_test.copy()
test_df["label_sentimen"] = y_test

# Simpan
train_df.to_csv("train_80.csv", index=False, encoding="utf-8-sig")
test_df.to_csv("test_20.csv", index=False, encoding="utf-8-sig")

print("Split data selesai:")
print("- train_80.csv (80%)")
print("- test_20.csv (20%)")
