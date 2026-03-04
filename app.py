import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Mg1865", layout="wide")

# Fandaminana ny lalana (Paths)
DATA_FILE = "data/Mg1865.json"

@st.cache_data
def load_bible():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Fahadisoana tamin'ny famakiana JSON: {e}")
        return None

def load_strong(code):
    filename = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            dic = json.load(f)
            return dic.get(code, "Tsy hita ny dikany")
    return "Tsy hita ny rakitra diksionera"

st.title("📖 Baiboly Mg1865 Interlineaire")

bible_data = load_bible()

if bible_data:
    # Mitady ny andininy (mety ho ao anaty 'books' na mivantana)
    bible_content = bible_data.get('books', bible_data)
    
    # Safidy Boky
    books = sorted(list(bible_content.keys()))
    book_sel = st.sidebar.selectbox("Fidio ny boky", books)
    
    # Safidy Toko
    chapters = bible_content[book_sel]
    ch_list = sorted(list(chapters.keys()), key=lambda x: int(x) if x.isdigit() else 0)
    ch_sel = st.sidebar.selectbox("Toko", ch_list)
    
    st.subheader(f"{book_sel} - Toko {ch_sel}")
    
    # Fampisehoana ny andininy
    verses = chapters[ch_sel]
    for v_num in sorted(verses.keys(), key=lambda x: int(x) if x.isdigit() else 0):
        text = verses[v_num]
        st.write(f"**{v_num}.** {text}")
        
        # Karoka Strong (Bokotra)
        strong_codes = re.findall(r'[GH]\d+', text)
        if strong_codes:
            cols = st.columns(len(strong_codes))
            for i, code in enumerate(strong_codes):
                if cols[i].button(f"🔍 {code}", key=f"{ch_sel}_{v_num}_{code}"):
                    meaning = load_strong(code)
                    st.info(f"**{code}:** {meaning}")
else:
    st.error("Tsy hita ny rakitra 'data/Mg1865.json'. Hamarino ny anarany sy ny toerana misy azy.")
