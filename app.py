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
            # Ny andininy dia ao amin'ny objects[0] -> rows (Sary 5db10129)
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
            return data
    except Exception as e:
        st.error(f"Fahadisoana: {e}")
        return None

st.title("📖 Baiboly Mg1865 Interlineaire")

bible = load_bible_data()

if bible:
    # Sidebar: Fidio ny Boky
    books = sorted(list(bible.keys()), key=lambda x: int(x) if x.isdigit() else 0)
    book_sel = st.sidebar.selectbox("Fidio ny boky", books)
    
    # Sidebar: Fidio ny Toko
    chapters = bible[book_sel]
    ch_list = sorted(list(chapters.keys()), key=lambda x: int(x) if x.isdigit() else 0)
    ch_sel = st.sidebar.selectbox("Toko", ch_list)
    
    st.subheader(f"Boky {book_sel} - Toko {ch_sel}")
    
    # Fampisehoana ny andininy
    verses = chapters[ch_sel]
    for v in sorted(verses.keys(), key=lambda x: int(x) if x.isdigit() else 0):
        t = verses[v]
        st.write(f"**{v}.** {t}")
        
        # Kaody Strong
        codes = re.findall(r'[GH]\d+', t)
        if codes:
            cols = st.columns(len(codes))
            for i, c in enumerate(codes):
                if cols[i].button(f"🔍 {c}", key=f"{ch_sel}_{v}_{c}"):
                    fn = "strongs-greek-dictionary.json" if c.startswith('G') else "strongs-hebrew-dictionary.json"
                    if os.path.exists(fn):
                        with open(fn, 'r', encoding='utf-8') as df:
                            d = json.load(df)
                            st.info(f"**{c}:** {d.get(c, 'Tsy hita')}")
else:
    st.info("Mampiditra ny rakitra 'Mg1865.json' (8.46 MB)... Andraso kely.")
