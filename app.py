import streamlit as st
import json
import os

st.set_page_config(page_title="Baiboly Interlineaire 1865", layout="wide", page_icon="📖")

DATA_PATH = "data"

@st.cache_data
def load_bible_data(filename):
    path = os.path.join(DATA_PATH, filename)
    if not os.path.exists(path): return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error(f"⚠️ Ny rakitra '{filename}' dia tsy feno na misy diso rafitra (JSON error). Andramo ampidirina indray.")
        return None
    except Exception as e:
        st.error(f"Fahadisoana hafa: {e}")
        return None

st.title("📖 Baiboly Malagasy 1865 Interlineaire")

if os.path.exists(DATA_PATH):
    files = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    if files:
        selected_file = st.sidebar.selectbox("Fidio ny Baiboly", files)
        bible_data = load_bible_data(selected_file)
        
        if bible_data:
            # Ny rafitra Mg1865 dia matetika misy 'metadata' sy 'books'
            books_dict = bible_data.get('books', bible_data)
            books_list = list(books_dict.keys())
            
            book_name = st.sidebar.selectbox("Fidio ny boky", books_list)
            chapters = books_dict[book_name]
            
            # Mandamina ny toko
            ch_list = sorted([k for k in chapters.keys() if str(k).isdigit()], key=int)
            if ch_list:
                ch_sel = st.sidebar.selectbox("Toko", ch_list)
                st.header(f"{book_name} - Toko {ch_sel}")
                
                verses = chapters[ch_sel]
                v_list = sorted([v for v in verses.keys() if str(v).isdigit()], key=int)
                
                for n in v_list:
                    txt = verses[n]
                    st.write(f"**{n}.** {txt}")
                    
                    # Fikarohana Strong mandeha ho azy
                    import re
                    codes = re.findall(r'[GH]\d+', txt)
                    if codes:
                        cols = st.columns(len(codes))
                        for i, c in enumerate(codes):
                            if cols[i].button(f"🔍 {c}", key=f"{book_name}_{ch_sel}_{n}_{c}"):
                                fn = "strongs-greek-dictionary.json" if c.startswith('G') else "strongs-hebrew-dictionary.json"
                                s_data = load_bible_data(fn) # Mitady ao amin'ny folder mitovy amin'ny app.py
                                if s_data and c in s_data:
                                    st.info(f"**{c}:** {s_data[c]}")
    else:
        st.warning("Tsy misy rakitra JSON hita ao anaty dossier 'data'.")
