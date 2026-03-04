import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Interlineaire Malagasy", layout="wide")

@st.cache_data
def load_json(path):
    if not os.path.exists(path): return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception: return None

st.title("📖 Baiboly Malagasy Interlineaire")

# Fandaminana ny rakitra ao anaty 'data'
DATA_PATH = "data"

if os.path.exists(DATA_PATH):
    files = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    if files:
        selected_file = st.sidebar.selectbox("Fidio ny Baiboly", files)
        bible_data = load_json(os.path.join(DATA_PATH, selected_file))
        
        if bible_data:
            # --- FANOMBOHANA NY SQL FORMAT (Ho an'ny Bible_MG65.json) ---
            if isinstance(bible_data, dict) and 'objects' in bible_data:
                # Mitady ny tabilao 'verses'
                for obj in bible_data['objects']:
                    if obj.get('name') == 'verses' and 'rows' in obj:
                        st.success(f"Dikan-teny: {selected_file}")
                        for row in obj['rows']:
                            # Ny index 3 no verse_number, index 4 no text
                            if len(row) > 4:
                                v_num = str(row[3])
                                txt = str(row[4])
                                st.write(f"**{v_num}.** {txt}")
                                
                                # Fikarohana Strong
                                strong_codes = re.findall(r'[GH]\d+', txt)
                                if strong_codes:
                                    cols = st.columns(len(strong_codes))
                                    for i, code in enumerate(strong_codes):
                                        if cols[i].button(f"🔍 {code}", key=f"{v_num}_{code}"):
                                            fn = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
                                            s_dict = load_json(fn)
                                            if s_dict and code in s_dict:
                                                st.info(f"**{code}:** {s_dict[code]}")
            
            # --- FANOMBOHANA NY FORMAT TSOTRA (Ho an'ny Mg1865.json) ---
            else:
                bible_content = bible_data.get('books', bible_data)
                books = sorted(list(bible_content.keys()))
                book_sel = st.sidebar.selectbox("Fidio ny boky", books)
                chapters = bible_content[book_sel]
                ch_sel = st.sidebar.selectbox("Toko", sorted(list(chapters.keys()), key=int))
                
                st.subheader(f"{book_sel} - Toko {ch_sel}")
                verses = chapters[ch_sel]
                for n in sorted(verses.keys(), key=int):
                    st.write(f"**{n}.** {verses[n]}")
    else:
        st.warning("Ampidiro ao anaty dossier 'data' ny rakitra .json")
