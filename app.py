import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Mg1865 Interlineaire", layout="wide")

@st.cache_data
def load_bible_data():
    path = "data/Mg1865.json"
    if not os.path.exists(path): return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Fitsidihana ny rafitra Database Export (sary 5db10129)
            # Row structure: [id, book_name, chapter, verse, text]
            if isinstance(data, dict) and "objects" in data:
                rows = data["objects"][0]["rows"]
                structured = {}
                for r in rows:
                    bk, ch, vn, txt = str(r[1]), str(r[2]), str(r[3]), r[4]
                    if bk not in structured: structured[bk] = {}
                    if ch not in structured[bk]: structured[bk][ch] = {}
                    structured[bk][ch][vn] = txt
                return structured
            return data # Raha efa structured sahady
    except Exception as e:
        st.error(f"Fahadisoana: {e}")
        return None

st.title("📖 Baiboly Mg1865 Interlineaire")

bible = load_bible_data()

if bible:
    # 1. Safidy Boky
    books = sorted(list(bible.keys()), key=lambda x: int(x) if x.isdigit() else 0)
    book_sel = st.sidebar.selectbox("Fidio ny boky", books)
    
    # 2. Safidy Toko
    chapters = bible[book_sel]
    ch_list = sorted(list(chapters.keys()), key=lambda x: int(x) if x.isdigit() else 0)
    ch_sel = st.sidebar.selectbox("Toko", ch_list)
    
    st.subheader(f"Boky {book_sel} - Toko {ch_sel}")
    
    # 3. Fampisehoana ny andininy
    verses = chapters[ch_sel]
    for v in sorted(verses.keys(), key=lambda x: int(x) if x.isdigit() else 0):
        txt = verses[v]
        st.write(f"**{v}.** {txt}")
        
        # Fikarohana kaody Strong
        codes = re.findall(r'[GH]\d+', txt)
        if codes:
            cols = st.columns(len(codes))
            for i, c in enumerate(codes):
                if cols[i].button(f"🔍 {c}", key=f"{ch_sel}_{v}_{c}"):
                    # Ampiasaina ny rakitra dictionary efa ao (sary 17ad75d4)
                    fn = "strongs-greek-dictionary.json" if c.startswith('G') else "strongs-hebrew-dictionary.json"
                    if os.path.exists(fn):
                        with open(fn, 'r', encoding='utf-8') as df:
                            s_dict = json.load(df)
                            st.info(f"**{c}:** {s_dict.get(c, 'Tsy hita')}")
else:
    st.info("Andraso kely, mbola mampiditra ny rakitra 'data/Mg1865.json'...")
