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
            # Ny rows dia ao amin'ny objects[0] (sary 5db10129)
            # Row structure: [id, book_name, chapter, verse, text]
            rows = data["objects"][0]["rows"]
            
            # Ovaina ho rafitra madio (Boky -> Toko -> Andininy)
            structured = {}
            for r in rows:
                book = str(r[1]) # Anaran'ny boky
                ch = str(r[2])   # Toko
                v_num = str(r[3]) # Andininy
                text = r[4]      # Soratra
                
                if book not in structured: structured[book] = {}
                if ch not in structured[book]: structured[book][ch] = {}
                structured[book][ch][v_num] = text
            return structured
    except Exception as e:
        st.error(f"Fahadisoana: {e}")
        return None

st.title("📖 Baiboly Mg1865 Interlineaire")

bible = load_bible_data()

if bible:
    # 1. Safidy Boky
    books = sorted(list(bible.keys()))
    book_sel = st.sidebar.selectbox("Fidio ny boky", books)
    
    # 2. Safidy Toko
    chapters = bible[book_sel]
    ch_list = sorted(list(chapters.keys()), key=lambda x: int(x) if x.isdigit() else 0)
    ch_sel = st.sidebar.selectbox("Toko", ch_list)
    
    st.subheader(f"{book_sel} - Toko {ch_sel}")
    
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
