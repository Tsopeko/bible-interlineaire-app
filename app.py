import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Mg1865", layout="wide")

@st.cache_data
def load_data(path):
    if not os.path.exists(path): return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return None

st.title("📖 Baiboly Mg1865 Interlineaire")

# 1. Fametrahana ny data
data = load_data("data/Mg1865.json")

if data and "objects" in data:
    try:
        # Ny rows dia ao anatin'ny objects[0] (ny table voalohany)
        rows = data["objects"][0]["rows"]
        
        # fandaminana ny rows ho lasa Dictionary (Boky -> Toko -> Andininy)
        # Ny row tsirairay dia matetika: [id, book_name, chapter, verse, text]
        bible_dict = {}
        for r in rows:
            b_name = r[1] # column 2: Anaran'ny boky
            ch = str(r[2]) # column 3: Toko
            v_num = str(r[3]) # column 4: Andininy
            txt = r[4] # column 5: Soratra
            
            if b_name not in bible_dict: bible_dict[b_name] = {}
            if ch not in bible_dict[b_name]: bible_dict[b_name][ch] = {}
            bible_dict[b_name][ch][v_num] = txt

        # 2. Safidy eo amin'ny Sidebar
        books = sorted(list(bible_dict.keys()))
        book_sel = st.sidebar.selectbox("Fidio ny boky", books)
        
        chapters = bible_dict[book_sel]
        ch_list = sorted(list(chapters.keys()), key=lambda x: int(x) if x.isdigit() else 0)
        ch_sel = st.sidebar.selectbox("Toko", ch_list)
        
        st.subheader(f"{book_sel} - Toko {ch_sel}")
        
        # 3. Fampisehoana ny andininy
        verses = chapters[ch_sel]
        for v in sorted(verses.keys(), key=lambda x: int(x) if x.isdigit() else 0):
            text = verses[v]
            st.write(f"**{v}.** {text}")
            
            # Bokotra Strong
            codes = re.findall(r'[GH]\d+', text)
            if codes:
                cols = st.columns(len(codes))
                for i, c in enumerate(codes):
                    if cols[i].button(f"🔍 {c}", key=f"{ch_sel}_{v}_{c}"):
                        fn = "strongs-greek-dictionary.json" if c.startswith('G') else "strongs-hebrew-dictionary.json"
                        s_dict = load_data(fn)
                        if s_dict:
                            st.info(f"**{c}:** {s_dict.get(c, 'Tsy hita')}")
                            
    except Exception as e:
        st.error(f"Nisy olana tamin'ny fandaminana ny rows: {e}")
else:
    st.warning("Andraso kely, mbola mampiditra ny rakitra 'Mg1865.json'...")
