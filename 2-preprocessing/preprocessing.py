    # Import pustaka yang diperlukan
import pandas as pd                          # Untuk membaca dan menyimpan data dalam format tabel (DataFrame)
import re                                    # Untuk operasi regex (pola teks)
from tqdm import tqdm                        # Untuk menampilkan progress bar saat proses berlangsung
from nltk.tokenize import RegexpTokenizer    # Untuk tokenisasi (memecah teks menjadi kata-kata)
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory  # Untuk stemming Bahasa Indonesia

# --- Setup awal ---

# Daftar stopword ringan, kata-kata umum yang tidak terlalu penting untuk analisis
stop_words = {
    'yang', 'dan','aku', 'saya', 'di', 'ke', 'dari', 'pada', 'untuk', 'dengan', 'nya', 'rep', 'la',
    'sebagai', 'oleh', 'dalam', 'atau', 'karena', 'agar', 'itu', 'klo', 'kalo', 'kalau',
    'ini', 'ni', 'adalah', 'tetapi', 'sehingga', 'gitu', 'smh',
    'ya', 'aja', 'juga', 'kok', 'ko', 'dong', 'deh', 'nih', 'sih', 'si', 'sm', 'aj', 'je',
    'biar', 'lah', 'lh', 'toh', 'jadi', 'kah', 'ah', 'oh', 'o', 'apaahh', 'apa',
    'kayak', 'karna', 'tp', 'trs', 'pls', 'k', 'krn', 'ow', 'wkwkwkwk', 'wkwkwkwkw',
    'yg', 'spt', 'dr', 'dgn', 'udh', 'skrg', 'trus', 'btw', 'halo', 'hi', 'wkw','wkwkw',
    'hai', 'x', 'y', 'ka', 'yaelah', 'eh', 'doang', 'ok', 'okay', 'yaela', 'aku', 'gue', 'saya',
    'oke', 'coy', 'bro', 'sis', 'min', 'admin', 'bang', 'kak', 'wkwk', 'wkwkwk', 'oalah',
    'haha', 'hahaha', 'hehe', 'hehehe', 'xixixi', 'alay', 'lu', 'lo', 'loh', 'oala', 'heleh', 
    'hehe', 'haha', 'yah', 'wow', 'weh', 'weleh', 'wle', 'yaa', 'yaaa', 'hele',
    'lah', 'yaudah', 'nih', 'dong', 'deh', 'plis', 'tuh', 'cie', 'ciee'
}


# Inisialisasi stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Inisialisasi tokenizer menggunakan regex untuk hanya mengambil kata (tanpa simbol/punctuation)
tokenizer = RegexpTokenizer(r'\w+')

# --- Fungsi preprocessing ---

def preprocess(text):
    if pd.isna(text):
        return ""  # Jika nilai kosong/NaN, kembalikan string kosong
    # Case Folding
    text = text.lower()  # Case folding: ubah semua huruf jadi kecil
    # Cleaning
    text = re.sub(r'http\S+|www.\S+', '', text)         # Hapus URL
    text = re.sub(r'#\w+', '', text)                    # Hapus hashtag
    text = re.sub(r'@\w+', '', text)                    # Hapus mention
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)          # Selain huruf angka dan spasi akan dihapus termasuk simbol, tanda baca, emoji
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text) # Hapus emoji dan simbol unicode tambahan
    # Tokenisasi
    tokens = tokenizer.tokenize(text)  # Tokenisasi: pecah teks jadi daftar kata
    # StopWords
    tokens = [word for word in tokens if word not in stop_words]  # Hapus stopword ringan
    # Stemming
    stemmed = [stemmer.stem(word) for word in tokens]  # Stemming: ubah kata ke bentuk dasarnya
    return ' '.join(stemmed)  # Gabungkan kembali hasil menjadi string

# --- Baca dan proses data ---

df = pd.read_csv('hasil_sampleacak_2.csv')  # Baca file CSV berisi tweet

tqdm.pandas(desc="Preprocessing tweets")  # Integrasi tqdm agar bisa tampil progress bar di apply
df['Preprocessed'] = df['Content'].progress_apply(preprocess)  # Terapkan fungsi preprocess ke kolom 'Content'

# --- Simpan hasil ke file baru ---

df.to_csv('tweet_preprocessed_2.csv', index=False)  # Simpan DataFrame ke CSV tanpa index

print("Preprocessing selesai! File hasil: tweet_preprocessed_2.csv")  # Tampilkan notifikasi selesai
