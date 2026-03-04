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
            # Ny andininy dia ao anatin'ny objects[0] -> rows (Sary 5db10129)
            # Isaky ny row: [id, book_number, chapter, verse, text]
            rows = data["objects"][0]["rows"]
            
            # Ovaina ho rafitra madio azo ampiasaina (Boky -> Toko -> Andininy)
            structured_bible = {}
            for r in rows:
                book = str(r[1]) # Anaran'ny boky na laharana
                ch = str(r[2])   # Toko
                v_num = str(r[3]) # Andininy
                text = r[4]      # Ny soratra masina misy kaody Strong
                
                if book not in structured_bible: structured_bible[book] = {}
                if ch not in structured_bible[book]: structured_bible[book][ch] = {}
                structured_bible[book][ch][v_num] = text
            return structured_bible
    except Exception as e:
        st.error(f"Fahadisoana tamin'ny famakiana: {e}")
        return None

st.title("📖 Baiboly Mg1865 Interlineaire")

bible = load_bible_data()

if bible:
    # 1. Safidy Boky eo amin'ny Sidebar
    books = sorted(list(bible.keys()), key=lambda x: int(x) if x.isdigit() else 0)
    selected_book = st.sidebar.selectbox("Fidio ny boky", books)
    
    # 2. Safidy Toko
    chapters = bible[selected_book]
    ch_list = sorted(list(chapters.keys()), key=lambda x: int(x) if x.isdigit() else 0)
    selected_ch = st.sidebar.selectbox("Toko", ch_list)
    
    st.subheader(f"Boky {selected_book} - Toko {selected_ch}")
    
    # 3. Fampisehoana ny andininy
    verses = chapters[selected_ch]
    for v_num in sorted(verses.keys(), key=lambda x: int(x) if x.isdigit() else 0):
        txt = verses[v_num]
        st.write(f"**{v_num}.** {txt}")
        
        # Fikarohana kaody Strong (G na H arahina isa)
        strong_codes = re.findall(r'[GH]\d+', txt)
        if strong_codes:
            cols = st.columns(len(strong_codes))
            for i, code in enumerate(strong_codes):
                if cols[i].button(f"🔍 {code}", key=f"{selected_ch}_{v_num}_{code}"):
                    dict_file = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
                    if os.path.exists(dict_file):
                        with open(dict_file, 'r', encoding='utf-8') as df:
                            s_dict = json.load(df)
                            st.info(f"**{code}:** {s_dict.get(code, 'Tsy hita ny dikan-teny')}")
else:
    st.info("Mampiditra ny rakitra 'Mg1865.json' (8.46 MB)... Andraso kely.")
