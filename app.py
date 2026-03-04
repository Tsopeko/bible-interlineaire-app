import streamlit as st
import json
import os

st.set_page_config(page_title="Baiboly Interlineaire", layout="wide")

DATA_PATH = "data"

@st.cache_data
def load_json(path):
    if not os.path.exists(path): return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return None

st.title("📖 Baiboly Malagasy Interlineaire")

# --- LECTURE ---
if os.path.exists(DATA_PATH):
    files = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    if files:
        selected_file = st.sidebar.selectbox("Fidio ny Baiboly", files)
        bible_data = load_json(os.path.join(DATA_PATH, selected_file))
        
        if bible_data:
            # MITADY NY VOTOATINY (Finding where the books are)
            # Ny Mg1865 dia matetika manana 'books' na 'content'
            if isinstance(bible_data, dict) and 'books' in bible_data:
                bible_content = bible_data['books']
            else:
                bible_content = bible_data

            if isinstance(bible_content, dict):
                books_list = list(bible_content.keys())
                book_name = st.sidebar.selectbox("Boky", books_list)
                
                chapters = bible_content[book_name]
                
                if isinstance(chapters, dict):
                    ch_list = sorted([k for k in chapters.keys() if str(k).isdigit()], key=int)
                    if ch_list:
                        ch_sel = st.sidebar.selectbox("Toko", ch_list)
                        st.header(f"{book_name} - Toko {ch_sel}")
                        
                        verses = chapters[ch_sel]
                        if isinstance(verses, dict):
                            v_list = sorted([v for v in verses.keys() if str(v).isdigit()], key=int)
                            for n in v_list:
                                txt = str(verses[n])
                                st.write(f"**{n}.** {txt}")
                                
                                # Fikarohana Strong
                                import re
                                codes = re.findall(r'[GH]\d+', txt)
                                if codes:
                                    cols = st.columns(len(codes))
                                    for i, c in enumerate(codes):
                                        if cols[i].button(f"🔍 {c}", key=f"{book_name}_{ch_sel}_{n}_{c}"):
                                            fn = "strongs-greek-dictionary.json" if c.startswith('G') else "strongs-hebrew-dictionary.json"
                                            s_data = load_json(fn)
                                            if s_data and c in s_data:
                                                st.info(f"**{c}:** {s_data[c]}")
            else:
                st.error("Tsy azo vakiana ny rafitra ao anatin'ity JSON ity.")
    else:
        st.warning("Ampidiro ao anaty dossier 'data' ny rakitra JSON-nao.")
