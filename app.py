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
    except Exception: return None

st.title("📖 Baiboly Malagasy Interlineaire")

# --- LECTURE ---
if os.path.exists(DATA_PATH):
    files = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    if files:
        selected_file = st.sidebar.selectbox("Fidio ny Baiboly", files)
        bible_data = load_json(os.path.join(DATA_PATH, selected_file))
        
        if bible_data:
            organized = {}
            # Raha format SQL-to-JSON (misy 'objects')
            if isinstance(bible_data, dict) and 'objects' in bible_data:
                for entry in bible_data['objects']:
                    # Mitady anarana malalaka (flexible keys)
                    b = str(entry.get('book_name', entry.get('book', 'Baiboly')))
                    c = str(entry.get('chapter', entry.get('chapter_number', '1')))
                    v = str(entry.get('verse', entry.get('verse_number', '1')))
                    # Mitady ny soratra (flexible text keys)
                    t = entry.get('text', entry.get('content', entry.get('body', '...')))
                    
                    if b not in organized: organized[b] = {}
                    if c not in organized[b]: organized[b][c] = {}
                    organized[b][c][v] = t
                bible_content = organized
            else:
                bible_content = bible_data.get('books', bible_data)

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
                                    s_data = load_json(fn) # Mitady ao amin'ny root folder
                                    if s_data and code in s_data:
                                        st.info(f"**{code}:** {s_data[code]}")
    else:
        st.warning("Ampidiro ny rakitra JSON ao anaty dossier 'data'.")
