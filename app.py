import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Interlineaire", layout="wide", page_icon="📖")

DATA_PATH = "data"

@st.cache_data
def load_json(path):
    if not os.path.exists(path): return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Tsy azo novakiana ilay fichier: {e}")
        return None

st.title("📖 Baiboly Malagasy Interlineaire")

# --- LECTURE ---
if os.path.exists(DATA_PATH):
    files = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    if files:
        selected_file = st.sidebar.selectbox("Fidio ny Baiboly", files)
        bible_data = load_json(os.path.join(DATA_PATH, selected_file))
        
        if bible_data:
            # 1. Mitady ny boky (Adaptive search)
            # Ny JSON sasany dia manomboka amin'ny 'books', ny sasany mivantana amin'ny anaran'ny boky
            content = bible_data.get('books', bible_data)
            
            if isinstance(content, dict):
                books_list = list(content.keys())
                book_name = st.sidebar.selectbox("Fidio ny boky", books_list)
                
                # 2. Mitady ny toko (Mitandrina amin'ny AttributeError)
                chapters = content.get(book_name, {})
                
                if isinstance(chapters, dict):
                    ch_list = sorted([k for k in chapters.keys() if str(k).isdigit()], key=int)
                    if ch_list:
                        ch_sel = st.sidebar.selectbox("Toko", ch_list)
                        st.header(f"{book_name} - Toko {ch_sel}")
                        
                        # 3. Mampiseho ny andininy
                        verses = chapters.get(ch_sel, {})
                        if isinstance(verses, dict):
                            v_list = sorted([v for v in verses.keys() if str(v).isdigit()], key=int)
                            for n in v_list:
                                txt = str(verses[n])
                                st.write(f"**{n}.** {txt}")
                                
                                # 4. Fikarohana Strong (Interlineaire)
                                strong_codes = re.findall(r'[GH]\d+', txt)
                                if strong_codes:
                                    cols = st.columns(len(strong_codes))
                                    for i, code in enumerate(strong_codes):
                                        if cols[i].button(f"🔍 {code}", key=f"{book_name}_{ch_sel}_{n}_{code}"):
                                            fn = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
                                            s_data = load_json(fn) # Mitady eo akaikin'ny app.py
                                            if s_data and code in s_data:
                                                st.info(f"**{code}:** {s_data[code]}")
            else:
                st.error("Ny rafitra JSON dia tsy mifanaraka amin'ny tokony ho izy.")
    else:
        st.warning("Ampidiro ao anaty dossier 'data' ny rakitra JSON-nao.")
