import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Interlineaire", layout="wide")

# Toerana misy ny data
DATA_PATH = "data"

@st.cache_data
def load_json(path):
    if not os.path.exists(path): return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception: return None

st.title("📖 Baiboly Malagasy Interlineaire")

if os.path.exists(DATA_PATH):
    files = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    if files:
        selected_file = st.sidebar.selectbox("Fidio ny Baiboly", files)
        raw_data = load_json(os.path.join(DATA_PATH, selected_file))
        
        if raw_data:
            bible_content = {}
            # 1. Raha format SQL (misy 'objects' sy 'rows') - Ho an'ny Bible_MG65.json
            if isinstance(raw_data, dict) and 'objects' in raw_data:
                # Mitady ny rows izay misy ny andininy
                for obj in raw_data['objects']:
                    if 'rows' in obj:
                        for row in obj['rows']:
                            # Ny laharan'ny column dia miankina amin'ny schema-nao
                            # Matetika: [id, book_id, chapter, verse, text]
                            b = "Baiboly" # Azonao ovaina ho anaran'ny boky raha misy
                            c = str(row[2]) if len(row) > 2 else "1"
                            v = str(row[3]) if len(row) > 3 else "1"
                            t = str(row[4]) if len(row) > 4 else "..."
                            if b not in bible_content: bible_content[b] = {}
                            if c not in bible_content[b]: bible_content[b][c] = {}
                            bible_content[b][c][v] = t
            # 2. Raha format tsotra (ho an'ny Mg1865.json)
            else:
                bible_content = raw_data.get('books', raw_data)

            # --- Affichage ---
            if bible_content:
                books = sorted(list(bible_content.keys()))
                book = st.sidebar.selectbox("Boky", books)
                chapters = bible_content[book]
                ch_list = sorted(list(chapters.keys()), key=lambda x: int(x) if x.isdigit() else 0)
                ch = st.sidebar.selectbox("Toko", ch_list)
                
                st.subheader(f"{book} - Toko {ch}")
                verses = chapters[ch]
                for v_num in sorted(verses.keys(), key=lambda x: int(x) if x.isdigit() else 0):
                    txt = verses[v_num]
                    st.write(f"**{v_num}.** {txt}")
                    
                    # Bokotra Strong
                    strongs = re.findall(r'[GH]\d+', txt)
                    if strongs:
                        cols = st.columns(len(strongs))
                        for i, code in enumerate(strongs):
                            if cols[i].button(f"🔍 {code}", key=f"{ch}_{v_num}_{code}"):
                                dict_file = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
                                s_data = load_json(dict_file)
                                if s_data and code in s_data:
                                    st.info(f"**{code}:** {s_data[code]}")
