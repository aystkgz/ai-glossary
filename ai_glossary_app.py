import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

# Yeni veri: Yapay zeka terimleri ve açıklamaları
data = [
    {"English": "Artificial Intelligence", "Turkish": "Yapay Zeka", "Azerbaijani": "Süni İntellekt", "Description": "Yapay zeka, makinelerin insanlar gibi düşünmesini sağlayan bir alandır."},
    {"English": "Machine Learning", "Turkish": "Makine Öğrenmesi", "Azerbaijani": "Maşın Öyrənməsi", "Description": "Makine öğrenmesi, bilgisayarların verilerle öğrenme sürecidir."},
    {"English": "Deep Learning", "Turkish": "Derin Öğrenme", "Azerbaijani": "Dərin Öyrənmə", "Description": "Derin öğrenme, daha karmaşık modelleme ve büyük veri ile öğrenme yöntemidir."},
    {"English": "Neural Network", "Turkish": "Sinir Ağı", "Azerbaijani": "Sinir Şəbəkəsi", "Description": "Sinir ağı, insan beyninin çalışma prensibinden ilham alınarak tasarlanmış bir makine öğrenmesi modelidir."},
    {"English": "Natural Language Processing", "Turkish": "Doğal Dil İşleme", "Azerbaijani": "Təbii Dil Emalı", "Description": "Doğal dil işleme, makinelerin insan dilini anlaması ve işlemesi için kullanılan bir alandır."},
    {"English": "Reinforcement Learning", "Turkish": "Pekiştirmeli Öğrenme", "Azerbaijani": "Möhkəmləndirici Öyrənmə", "Description": "Pekiştirmeli öğrenme, ajanların bir ortamda ödüller veya cezalar alarak karar vermeyi öğrenmesidir."},
    {"English": "Computer Vision", "Turkish": "Bilgisayarla Görü", "Azerbaijani": "Kompüter Görməsi", "Description": "Bilgisayarla görü, makinelerin görüntüleri anlaması ve işlemesiyle ilgili bir alandır."},
    {"English": "Transformer", "Turkish": "Dönüştürücü", "Azerbaijani": "Transformator", "Description": "Transformer, dil modellerinde kullanılan ve büyük veri üzerinde etkili olan bir derin öğrenme modelidir."},
    {"English": "Recurrent Neural Network", "Turkish": "Tekrarlayan Sinir Ağı", "Azerbaijani": "Təkrarlanan Sinir Şəbəkəsi", "Description": "Tekrarlayan sinir ağları, sıralı veri işlemek için kullanılan bir tür sinir ağıdır."},
    {"English": "Convolutional Neural Network", "Turkish": "Konvolüsyonel Sinir Ağı", "Azerbaijani": "Konvolusyonal Sinir Şəbəkəsi", "Description": "Konvolüsyonel sinir ağları, özellikle görüntü işleme için yaygın olarak kullanılır."},
    {"English": "Generative Adversarial Networks", "Turkish": "Üretici Karşıt Ağlar", "Azerbaijani": "Nəsil Əksə Uğurlu Şəbəkələr", "Description": "Üretici karşıt ağlar, gerçekçi veriler üretmek için kullanılan bir yapay zeka modelidir."},
    {"English": "Natural Language Generation", "Turkish": "Doğal Dil Üretimi", "Azerbaijani": "Təbii Dil Yaratma", "Description": "Doğal dil üretimi, makinelerin anlamlı metinler üretmesini sağlayan bir alandır."},
    {"English": "AutoML", "Turkish": "Otomatik Makine Öğrenmesi", "Azerbaijani": "Avtomatik Maşın Öyrənməsi", "Description": "Otomatik makine öğrenmesi, makine öğrenmesi modellerini otomatik olarak oluşturmak için kullanılan bir tekniktir."},
]

df = pd.DataFrame(data)

st.title("🤖 Yapay Zeka Terimleri Sözlüğü (TR / AZ)")

# Kullanıcının arama yapacağı metin girişi
search_term = st.text_input("🔍 Bir terim girin (İngilizce / Türkçe / Azerbaycanca):").strip().lower()

# Dil seçimi
language = st.radio("Dil Seçin:", ("English", "Turkish", "Azerbaijani"))

# Favori terimler listesi
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# En çok aranan terimler
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

def search_glossary(term, language):
    if term == "":
        return df
    else:
        def is_match(row):
            return fuzz.partial_ratio(term, row[language].lower()) > 70
        return df[df.apply(is_match, axis=1)]

filtered_df = search_glossary(search_term, language)

# Sonuçları kullanıcıya göster
st.write(f"### Sonuçlar ({len(filtered_df)} terim bulundu)")
for idx, row in filtered_df.iterrows():
    st.write(f"**{row['English']}** ({row['Turkish']} / {row['Azerbaijani']})")
    st.write(f"  *Açıklama:* {row['Description']}")
    if st.button(f"Favorilere Ekle: {row['English']}", key=f"fav_{row['English']}"):
        st.session_state.favorites.append(row['English'])
        st.success(f"{row['English']} favorilerinize eklendi!")

# Favori terimleri göster
st.write("### Favori Terimler")
if st.session_state.favorites:
    st.write(", ".join(st.session_state.favorites))
else:
    st.write("Henüz favori teriminiz yok.")

# En çok aranan terimleri göster
if len(st.session_state.search_history) > 0:
    st.write("### En Çok Aranan Terimler")
    st.write(", ".join(st.session_state.search_history))

# Arama geçmişini güncelle
if search_term and search_term not in st.session_state.search_history:
    st.session_state.search_history.append(search_term)

# Yeni terim ekleme formu
st.write("### Yeni Terim Ekle")
new_english = st.text_input("İngilizce Terim:", key="new_english")
new_turkish = st.text_input("Türkçe Terim:", key="new_turkish")
new_azerbaijani = st.text_input("Azerbaycan Türkçesi Terim:", key="new_azerbaijani")
new_description = st.text_area("Açıklama:", key="new_description")

# Kullanıcı yeni terim eklerse
if st.button("Yeni Terim Ekle"):
    if new_english and new_turkish and new_azerbaijani and new_description:
        new_row = {
            "English": new_english,
            "Turkish": new_turkish,
            "Azerbaijani": new_azerbaijani,
            "Description": new_description
        }
        df = df.append(new_row, ignore_index=True)
        st.session_state.new_english = ""
        st.session_state.new_turkish = ""
        st.session_state.new_azerbaijani = ""
        st.session_state.new_description = ""
        st.success(f"Yeni terim başarıyla eklendi: {new_english}")
    else:
        st.error("Lütfen tüm alanları doldurduğunuzdan emin olun.")
