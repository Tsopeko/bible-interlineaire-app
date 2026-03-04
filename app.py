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
        st.error(f"Fahadisoana tamin'ny famakiana: {e}")
        return None

st.title("📖 Baiboly Malagasy Interlineaire")

# --- LECTURE ---
if os.path.exists(DATA_PATH):
    files = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    if files:
        selected_file = st.sidebar.selectbox("Fidio ny Baiboly", files)
        bible_data = load_json(os.path.join(DATA_PATH, selected_file))
        
        if bible_data:
            # ADAPTER HO AN'NY RAFIKRA MAVESATRA (SQL-TO-JSON FORMAT)
            # Raha mivoaka ny 'type', 'name', 'objects', dia ao anaty 'objects' ny andininy
            if isinstance(bible_data, dict) and 'objects' in bible_data:
                # Eto no misy ny andininy rehetra
                raw_verses = bible_data['objects']
                
                # Alahatra isaky ny boky, toko, andininy
                organized = {}
                for entry in raw_verses:
                    # Ireto anarana ireto dia miankina amin'ny rakitra anananao (matetika 'book', 'chapter', 'verse')
                    b = entry.get('book_name', entry.get('book', 'Baiboly'))
                    c = str(entry.get('chapter', '1'))
                    v = str(entry.get('verse', '1'))
                    t = entry.get('text', entry.get('content', '...'))
                    
                    if b not in organized: organized[b] = {}
                    if c not in organized[b]: organized[b][c] = {}
                    organized[b][c][v] = t
                bible_content = organized
            else:
                bible_content = bible_data.get('books', bible_data)

            # Fampisehoana ny andininy
            if isinstance(bible_content, dict):
                books_list = sorted(list(bible_content.keys()))
                book_name = st.sidebar.selectbox("Fidio ny boky", books_list)
                
                chapters = bible_content.get(book_name, {})
                ch_list = sorted([k for k in chapters.keys() if str(k).isdigit()], key=int)
                
                if ch_list:
                    ch_sel = st.sidebar.selectbox("Toko", ch_list)
                    st.header(f"{book_name} - Toko {ch_sel}")
                    
                    verses = chapters.get(ch_sel, {})
                    v_list = sorted([v for v in verses.keys() if str(v).isdigit()], key=int)
                    
                    for n in v_list:
                        txt = str(verses[n])
                        st.write(f"**{n}.** {txt}")
                        
                        # INTERLINEAIRE: Fikarohana Strong
                        strong_codes = re.findall(r'[GH]\d+', txt)
                        if strong_codes:
                            cols = st.columns(len(strong_codes))
                            for i, code in enumerate(strong_codes):
                                if cols[i].button(f"🔍 {code}", key=f"{book_name}_{ch_sel}_{n}_{code}"):
                                    fn = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
                                    s_data = load_json(fn)
                                    if s_data and code in s_data:
                                        st.info(f"**{code}:** {s_data[code]}")
    else:
        st.warning("Ampidiro ny rakitra JSON ao anaty dossier 'data'.")
