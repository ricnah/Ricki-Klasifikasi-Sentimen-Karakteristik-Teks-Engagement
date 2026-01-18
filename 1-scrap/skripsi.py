# ======= Versi dengan Try-Except Fallback =======

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import urllib.parse
import time
import pandas as pd
import os
import json
import re
import emoji
import unicodedata

# ===== Daftar Kata Kunci Diperbarui =====
keywords = [
    "Shopee cepat sampai", "Shopee pengiriman cepat", "Shopee memuaskan", "Shopee terbaik", 
    "Shopee pelayanan bagus", "Shopee respons cepat", "Shopee terpercaya banget", "Shopee recomended banget",
    "Shopee puas belanja", "Shopee barang sesuai", "Shopee kualitas bagus", "Shopee produk original",
    "Shopee harga terjangkau", "Shopee banyak promo", "Shopee hemat banget", "Shopee cashback besar",

    # ShopeePay dan ShopeeFood Positif
    "ShopeePay lancar", "ShopeePay cepat", "ShopeePay aman", "ShopeePay praktis", 
    "ShopeeFood enak", "ShopeeFood cepat", "ShopeeFood recommended", "ShopeeFood puas",
    "ShopeeFood promo besar", "ShopeeFood memuaskan", "ShopeeFood pelayanan bagus",

    # ShopeeLive / ShopeeVideo
    "ShopeeLive seru", "ShopeeLive menyenangkan", "ShopeeLive interaktif", "ShopeeLive lucu", 
    "ShopeeVideo menarik", "ShopeeVideo menghibur", "ShopeeVideo viral", "ShopeeVideo seru banget",

    # Shopee Affiliate (positif)
    "Shopee Affiliate berhasil", "Shopee Affiliate sukses", "Shopee Affiliate gampang", "Shopee Affiliate komisi besar",
    "Shopee Affiliate terpercaya", "Shopee Affiliate lancar", "Shopee Affiliate menguntungkan", 

    # Shopee Event & Promo
    "Shopee 11.11 diskon besar", "Shopee 12.12 promo", "Shopee 9.9 super sale", "Shopee 3.3 sale",
    "Shopee 6.6 cashback", "Shopee 8.8 hemat besar", "Shopee sale gila-gilaan", 
    "Shopee gratis ongkir", "Shopee voucher spesial", "Shopee promo menarik",

    # Shopee Mall & Produk
    "Shopee Mall original", "Shopee Mall terpercaya", "Shopee Mall cepat", "Shopee Mall memuaskan",
    "Shopee Mall berkualitas", "produk Shopee Mall bagus", "Shopee Mall recomended",
    "belanja di Shopee Mall menyenangkan", "Shopee Mall murah", "Shopee Mall aman",

    # Shopee Customer Service
    "Shopee CS ramah", "Shopee bantu cepat", "Shopee customer care baik", "Shopee solusi cepat", 
    "Shopee CS tanggap", "Shopee CS profesional", "Shopee cepat respon",

    # Umum & Loyalitas
    "Pakai Shopee nyaman", "Belanja di Shopee enak", "Shopee andalan saya", "Shopee favorit",
    "Shopee aplikasi bagus", "Shopee memudahkan", "Shopee top banget", "Shopee pengalaman positif",
    
    # Shopee Affiliate (dipersempit untuk proporsi data)
    "Shopee Affiliate susah", "Shopee Affiliate gagal", "Shopee Affiliate error", "Shopee Affiliate komisi", "Shopee Affiliate review",
    "Shopee Affiliate kecewa", "Shopee Affiliate telat", "Shopee Affiliate pending",

    # ShopeePay, ShopeeFood, ShopeeVideo, ShopeeLive (DITAMBAH NEGATIF)
    "Shopee SPX", "Shopee Express", "ShopeePay tidak bisa", "ShopeePay gagal", "ShopeePay telat", "ShopeePay tidak masuk",
    "ShopeePay dibekukan", "ShopeePay pending", "ShopeePay lambat", "ShopeePay error", "Top up Shopee",
    "ShopeeFood telat", "ShopeeFood dingin", "ShopeeFood lambat", "ShopeeFood cancel", "Transfer Shopee",
    "ShopeeFood jelek", "ShopeeFood mantap", "ShopeeFood refund", "Shopee COD", "Shopee pengiriman",
    "ShopeeLive error", "ShopeeLive macet", "ShopeeLive buffering", "Shopee Bayar ditempat", "Shopee pengembalian barang",
    "ShopeeVideo lemot", "ShopeeVideo tidak bisa dibuka", "ShopeeVideo gagal loading",

    # Event diskon besar
    "Shopee 12.12 bot", "Shopee 6.6", "Shopee 1.1", "Shopee ramadhan Sale",
    "Shopee iphone 1 rupiah", "Shopee flash sale", "Shopee rebutan barang", "Bot Shopee", "Flash Sale shopee bot",

    # Masalah UX / aplikasi berat / lemot
    "Aplikasi Shopee berat", "Shopee lemot", "Shopee crash", "Shopee error loading", "Shopee aplikasi rusak",
    "Shopee tidak responsif", "Shopee keluar sendiri", "Shopee tidak bisa dibuka",

    # Umum: pembeli, penjual, pengalaman
    "Pakai Shopee", "Shopee pembeli", "Shopee penjual", "Review Shopee", "Shopee CS", "Shopee Customer Service",
    "Shopee paket hilang", "Shopee pengiriman lama", "Shopee layanan buruk",
    "Shopee bagus", "Shopee terpercaya", "Shopee recommended", "Shopee kurir", 

    # Kata negatif umum terkait Shopee
    "Shopee id post", "Penipuan Shopee", "Shopee goblok", "Shopee dongo", "Shopee bego", "Shopee njir", "Shopee susah",
    "Shopee anjing", "Shopee nipu", "Shopee jelek", "Shopee nipu seller", "Shopee nipu pembeli", "Shopee anjir",
    "shopee suntik ulasan", "Shopee babi", "Shopee ulasan palsu", "Shopee dibekukan",
    
    # Shopee Mall / Toko Resmi
    "Shopee Mall", "belanja di Shopee Mall", "toko resmi Shopee", "Shopee Mall asli atau palsu", 
    "harga di Shopee Mall", "produk Shopee Mall rusak", "Shopee Mall mahal", "Shopee Mall worth it",
    "bedanya Shopee Mall dan biasa", "Shopee Mall penipuan", "Shopee Mall pengiriman lama",
    
    # Level pengguna Shopee
    "Akun silver Shopee", "Akun gold Shopee", "Akun platinum Shopee",
    "akun baru Shopee dibatasi", "akun lama Shopee lebih untung", 
    "akun Shopee limit voucher", "akun Shopee tidak dapat cashback",
    "Shopee tidak bisa checkout", "Shopee tidak adil akun baru",
    "Platinum Shopee tidak dapat voucher", "Pembeli Shopee gold"
]

# ===== Kata Persuasif dan Brand =====
kata_persuasif = ["gratis", "diskon", "voucher", "promo", "hemat", "cashback", "murah", "cuma", "flash sale",
                  "beli sekarang", "terbatas", "limited", "potongan", "gratis ongkir", "voucher khusus",
                  "gajian sale", "harga miring", "deal spesial", "super sale", "khusus hari ini"]
layanan_keywords = ["shopee", "shopeepay", "shopeefood", "shopeelive", "shopeevideo", "shopeeaffiliate"]

# ===== Konfigurasi Chrome =====
options = Options()
options.add_argument(r"--user-data-dir=C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\User Data Selenium")
options.add_argument(r"--profile-directory=Profile 27")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Login manual
driver.get("https://twitter.com/login")
input("Silakan login, lalu tekan Enter di sini...")

# ===== File dan Checkpoint =====
csv_file = "ricki_tweets_raw.csv"
checkpoint_file = "ricki_tweets_checkpoint.json"

if not os.path.exists(csv_file):
    pd.DataFrame(columns=['Tweet Id', 'Date', 'Display Name', 'Username', 'Replying', 'Replying To', 'Content', 'Query', 'Like', 'Retweet', 'Reply', 'views', 'Has Media', 'Total Media', 'Media Type', 'Mengandung Link', 'Jumlah Tautan', 'Link dalam Konten', 'Panjang Teks', 'Jumlah Emoji', 'Huruf Kapital', 'Kata Persuasif', 'Layanan Disebut', 'Layanan Disebut Nama', 'Hashtag', 'Jumlah Hashtags', 'Daftar Hashtags', 'Verified', 'Verified Type', 'Mention', 'Jumlah Mention', 'Daftar Mention', 'Tweet Link']).to_csv(csv_file, index=False, encoding='utf-8-sig')

# Load checkpoint
tweets_checkpoint = []
start_index = 0
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r', encoding='utf-8') as f:
        checkpoint_data = json.load(f)
        tweets_checkpoint = checkpoint_data.get("tweets", [])
        start_index = checkpoint_data.get("last_index", 0) + 1

tweet_ids = set(tweet['Tweet Id'] for tweet in tweets_checkpoint)

# ===== Fungsi Deteksi Emoji Akurat =====
def detect_emojis_unicode(text):
    emoji_chars = []
    for item in emoji.emoji_list(text):
        char = item['emoji']
        try:
            cat = unicodedata.category(char)
            name = unicodedata.name(char)
            if cat.startswith('So') or any(k in name for k in ['FACE', 'EMOJI', 'HEART', 'HAND', 'SMILE', 'FLAG', 'SYMBOL']):
                emoji_chars.append(char)
        except ValueError:
            continue
    return emoji_chars

def detect_emojis_unicode(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # geometric shapes extended
        "\U0001F800-\U0001F8FF"  # arrows
        "\U0001F900-\U0001F9FF"  # symbols & pictographs
        "\U0001FA00-\U0001FA6F"  # chess
        "\U0001FA70-\U0001FAFF"  # extended pictographs
        "\U00002600-\U000026FF"  # misc symbols
        "\U00002700-\U000027BF"  # dingbats
        "]+", flags=re.UNICODE)
    return emoji_pattern.findall(text)



# ===== Fungsi Scraping =====
def get_tweets_from_query(query_raw):
    global tweet_ids
    tweet_data = []
    query_base = urllib.parse.quote(query_raw + " since:2022-01-01 until:2025-10-13 -filter:retweets")

    scroll_pause_time = 10
    scrolls_per_mode = 20

    for mode in ['top', 'live']:
        url = f"https://twitter.com/search?q={query_base}&f={mode}"
        driver.get(url)
        time.sleep(5)
        last_height = driver.execute_script("return document.body.scrollHeight")
        scrolls = 0

        while scrolls < scrolls_per_mode:
            elements = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
            print(f"[{query_raw}] Ditemukan {len(elements)} tweet di halaman ini.")

            for elem in elements:
                try:
                    tweet_link_elem = elem.find_element(By.XPATH, './/a[contains(@href,"/status/")]')
                    tweet_link = tweet_link_elem.get_attribute('href')
                    tweet_id = tweet_link.split('/')[-1]
                    if tweet_id in tweet_ids:
                        continue
                    content = ""
                    
                    try:
                        tweet_elem = elem.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
                        content_parts = []
                        # Ambil semua child node (span untuk teks, img untuk emoji)
                        for node in tweet_elem.find_elements(By.XPATH, './*'):
                            try:
                                tag = node.tag_name.lower()
                                if tag == 'span':
                                    content_parts.append(node.text)
                                elif tag == 'img':
                                    alt = node.get_attribute('alt')
                                    if alt:
                                        content_parts.append(alt)
                                elif tag == 'a':
                                    link_text = node.text.strip()
                                    if link_text:
                                        content_parts.append(link_text)
                            except:
                                continue
                        # Gabungkan semua bagian, bersihkan karakter baris baru & separator
                        content = ' '.join(part.strip() for part in content_parts if part.strip())
                        content = content.replace('\n', ' ').replace('\r', ' ').replace('\u2028', ' ').replace('\u2029', ' ').strip()
                    except:
                        content = ""

                    def get_displayname_username(elem):
                        username = "None"
                        display_name = "None"
                        replying = False
                        replying_to = []

                        try:
                            # Display name (nama tampilan)
                            display_name_elem = elem.find_element(By.XPATH, './/div[@data-testid="User-Name"]//span[contains(@class, "r-bcqeeo") and not(starts-with(text(),"@"))]')
                            display_name = display_name_elem.text.strip()
                        
                            # Tambahkan emoji jika ada di dalam <img alt="...">
                            display_text = display_name_elem.text.strip()
                            emoji_imgs = display_name_elem.find_elements(By.TAG_NAME, 'img')
                            emoji_list = [img.get_attribute("alt") for img in emoji_imgs if img.get_attribute("alt")]
                            display_name = display_text + ''.join(emoji_list)
                        except:
                            pass

                        try:
                            # Username utama (yang ngetweet)
                            a_tag = elem.find_element(By.XPATH, './/a[contains(@href,"/status/")]')
                            tweet_url = a_tag.get_attribute('href')
                            if tweet_url:
                                username = tweet_url.split('/')[3]
                        except:
                            pass

                        try:
                            reply_links = elem.find_elements(By.XPATH, './/a[contains(@href, "/")]/span[starts-with(text(), "@")]')
                            if reply_links:
                                replying = True
                                replying_to = [a.text.replace('@', '') for a in reply_links]
                            else:
                                replying = False
                                replying_to = []
                        except:
                            replying = False
                            replying_to = []


                        return display_name, username, replying, ', '.join([f"@{u}" for u in replying_to]) if replying_to else 'None'
                    display_name, username, replying, replying_to = get_displayname_username(elem)

                    date = elem.find_element(By.XPATH, './/time').get_attribute('datetime') if elem.find_elements(By.XPATH, './/time') else "None"

                    def get_count(elem, data_testid):
                        def convert_text(text):
                            try:
                                text = text.upper().replace(',', '')
                                if 'K' in text:
                                    return int(float(text.replace('K', '')) * 1_000)
                                elif 'M' in text:
                                    return int(float(text.replace('M', '')) * 1_000_000)
                                else:
                                    return int(text)
                            except:
                                return 0

                        try:
                            button = elem.find_element(By.XPATH, f'.//button[@data-testid="{data_testid}"]')
                            spans = button.find_elements(By.XPATH, './/span')
                            for span in spans[::-1]:  # dari belakang karena value biasanya paling akhir
                                text = span.text.strip()
                                if text and (text.replace(',', '').isdigit() or 'K' in text or 'M' in text):
                                    return convert_text(text)
                            return 0
                        except:
                            return 0
                    like = get_count(elem, "like")
                    retweet = get_count(elem, "retweet")
                    reply = get_count(elem, "reply")

                    def get_views(elem):
                        def convert_views(text):
                            try:
                                text = text.upper().replace(',', '')
                                if 'K' in text:
                                    return int(float(text.replace('K', '')) * 1_000)
                                elif 'M' in text:
                                    return int(float(text.replace('M', '')) * 1_000_000)
                                else:
                                    return int(text)
                            except:
                                return 0

                        try:
                            group = elem.find_element(By.XPATH, './/div[@role="group"]')
                            label = group.get_attribute("aria-label")
                            match = re.search(r'([\d,\.KkMm]+)\s+views', label)
                            if match:
                                return convert_views(match.group(1))
                            return 0
                        except:
                            return 0
                    views = get_views(elem)


                    try:
                        # Deteksi media dan hitung jumlah
                        all_images = elem.find_elements(By.XPATH, './/img[contains(@src, "twimg.com/media")]')
                        videos = elem.find_elements(By.XPATH, './/video')
                        media_html = elem.get_attribute("innerHTML")
                        has_gif = 'animated_gif' in media_html  # gif biasanya cuma satu jenis indikator
                        
                        images = []
                        for img in all_images:
                            try:
                                parent = img.find_element(By.XPATH, './ancestor::div[contains(@aria-label, "Image")] | ./ancestor::div[@role="button"]')
                                if parent:
                                    images.append(img)
                            except:
                                continue  # abaikan img yang tidak punya parent image

                        count_images = len(images)
                        count_videos = len(videos)
                        count_gifs = 1 if has_gif else 0

                        total_media = count_images + count_videos + count_gifs
                        has_media = total_media > 0

                        media_type = []
                        if count_videos > 0: media_type.append(f'video({count_videos})')
                        if count_images > 0: media_type.append(f'image({count_images})')
                        if count_gifs > 0: media_type.append(f'gif({count_gifs})')
                        media_type = ', '.join(media_type) if media_type else 'None'
                    except Exception as e:
                        has_media = False
                        media_type = 'None'
                        total_media = 0


                    mengandung_link = 'http' in content.lower()
                    link_dalam_konten = ', '.join(re.findall(r'http[s]?://\S+', content)) or 'None'
                    jumlah_link_dalam_konten = len(re.findall(r'http[s]?://\S+', content))

                    # content_tanpa_hashtag = ' '.join(word for word in content.split() if not word.startswith('#'))
                    # panjang_teks = len(content_tanpa_hashtag)
                    panjang_teks = len(content)
                    emoji_imgs = tweet_elem.find_elements(By.XPATH, './/img[@alt]')
                    emojis = [img.get_attribute("alt") for img in emoji_imgs if img.get_attribute("alt")]
                    jumlah_emoji = len(emojis)

                    # Hapus mention dan link sebelum dihitung
                    non_link_parts = []
                    for node in tweet_elem.find_elements(By.XPATH, './*'):
                        try:
                            if node.tag_name.lower() == 'span':
                                non_link_parts.append(node.text)
                        except:
                            continue
                    # Gabungkan teks tanpa link dan tanpa hastag
                    non_link_content = ' '.join(part.strip() for part in non_link_parts if part.strip())
                    non_link_content = non_link_content.replace('\n', ' ').replace('\r', ' ').replace('\u2028', ' ').replace('\u2029', ' ').strip()
                    non_link_content = ' '.join(word for word in non_link_content.split() if not word.startswith('#'))
                    # Hitung huruf kapital HANYA dari non-link text
                    huruf_kapital = sum(1 for c in non_link_content if c.isupper())

                    kata_persu = any(kata in content.lower() for kata in kata_persuasif)
                    layanan_disebut_list = [layanan for layanan in layanan_keywords if layanan in content.lower()]
                    layanan_sebut = bool(layanan_disebut_list)
                    layanan_disebut_nama = ', '.join(layanan_disebut_list) if layanan_disebut_list else 'None'
                    hashtags = re.findall(r'#\w+', content)
                    hashtags_str = ', '.join(hashtags) if hashtags else 'None' 
                    jumlah_hashtags = len(hashtags)
                
                    # detect verified
                    def detect_verified_status(elem):
                        try:
                            # is_verified = False
                            # verified_type = 'None'
                            # Kumpulan kemungkinan XPath yang menangkap ikon verified
                            xpaths = [
                                './/svg[contains(@aria-label, "Verified account")]',
                                './/svg[contains(@aria-label, "Verified")]',
                                './/svg[@data-testid="icon-verified"]',
                                './/*[contains(@class, "verified")]',
                                './/*[@aria-label="Verified account"]',
                                './/img[contains(@alt, "Verified")]'
                            ]
                            verified_elements = []
                            for xp in xpaths:
                                try:
                                    els = elem.find_elements(By.XPATH, xp)
                                    if els:
                                        verified_elements.extend(els)
                                except:
                                    continue

                            if not verified_elements:
                                # print("[DEBUG] Tidak ditemukan ikon verified di elem ini.")
                                return False, 'None'
                            # Ambil elemen pertama untuk analisis
                            el = verified_elements[0]
                            html = el.get_attribute("outerHTML").lower()
                            # Logging nama pengguna dan isi SVG (debug)
                            # try:
                            #     username_element = elem.find_element(By.XPATH, './/span[contains(text(), "@")]')
                            #     print(f"[DEBUG] @{username_element.text.strip()} -> Verified SVG: {html[:120]}")
                            # except:
                            #     print(f"[DEBUG] Verified SVG: {html[:120]}")

                            # Deteksi berdasarkan isi
                            if 'lineargradient' in html or '#f4e72a' in html or '#cd8105' in html or 'gold' in html:
                                return True, 'Verified Organization (Gold)'
                            elif '#8b98a5' in html or 'gray' in html:
                                return True, 'Verified Government (Grey)'
                            else:
                                return True, 'Verified Premium (Blue)'

                        except Exception as e:
                            print("Detect verified error:", e)
                            return False, 'None'
                    # Contoh pemakaian
                    is_verified, verified_type = detect_verified_status(elem)


                    mention_elems = elem.find_elements(By.XPATH, './/div[@data-testid="tweetText"]//a[starts-with(@href, "/") and starts-with(text(), "@")]')
                    mention_list = [m.text.strip() for m in mention_elems if m.text.strip().startswith("@")]
                    jumlah_mention = len(mention_list)
                    semua_mention = ', '.join(mention_list) if mention_list else 'None'
                    ada_mention = jumlah_mention > 0

                    tweet_data.append({
                        'Tweet Id': tweet_id,
                        'Date': date,
                        'Display Name': display_name,
                        'Username': username,
                        'Replying': replying,
                        'Replying To': replying_to,
                        'Content': content,
                        'Query': query_raw,
                        'Like': like,
                        'Retweet': retweet,
                        'Reply': reply,
                        'views': views,
                        'Has Media': has_media,
                        'Total Media': total_media,
                        'Media Type': media_type,
                        'Mengandung Link': mengandung_link,
                        'Jumlah Tautan': jumlah_link_dalam_konten,
                        'Link dalam Konten': link_dalam_konten,
                        'Panjang Teks': panjang_teks,
                        'Jumlah Emoji': jumlah_emoji,
                        'Huruf Kapital': huruf_kapital,
                        'Kata Persuasif': kata_persu,
                        'Layanan Disebut': layanan_sebut,
                        'Layanan Disebut Nama': layanan_disebut_nama,
                        'Hashtag': str(bool(hashtags)),
                        'Jumlah Hashtags': jumlah_hashtags,
                        'Daftar Hashtags': hashtags_str,
                        'Verified': is_verified,
                        'Verified Type': verified_type,
                        'Mention': ada_mention,
                        'Jumlah Mention': jumlah_mention,
                        'Daftar Mention': semua_mention,
                        'Tweet Link': tweet_link
                    })
                    tweet_ids.add(tweet_id)

                except Exception as e:
                    print(f"Error parsing tweet: {e}")
                    continue

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scrolls += 1

    return tweet_data

# ===== Proses Scraping Utama =====
for i in range(start_index, len(keywords)):
    keyword = keywords[i]
    print(f"\n🔍 Scraping untuk kata kunci: {keyword}")

    try:
        result = get_tweets_from_query(keyword)
        print(f"✅ Ditambahkan {len(result)} tweet dari '{keyword}'")

        if result:
            df_temp = pd.DataFrame(result)
            df_temp.to_csv(csv_file, mode='a', index=False, header=False, encoding='utf-8-sig')
            print(f"📥 Data dari '{keyword}' disimpan ke {csv_file}")

        tweets_checkpoint.extend(result)
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump({"tweets": tweets_checkpoint, "last_index": i}, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"❌ Gagal pada keyword '{keyword}': {e}")
        break

    if i < len(keywords) - 1:
        print("⏳ Jeda 2 menit antar keyword...")
        time.sleep(120)
        if (i + 1) % 4 == 0:
            print("⏸️ Tambahan jeda 2 menit setiap 4 keyword...")
            time.sleep(120)

# ===== Selesai =====
driver.quit()
print(f"\n🎉 Selesai! Semua data telah disimpan di {csv_file}")
