import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Mg1865", layout="wide")

# Path mankany amin'ny data
DATA_FILE = "data/Mg1865.json"

@st.cache_data
def load_bible():
    if not os.path.exists(DATA_FILE):
        st.error(f"Tsy hita ny rakitra: {DATA_FILE}")
        return None
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        st.error(f"Simbaka ny JSON eo amin'ny andalana {e.lineno}. Avereno ampidirina (Upload) ny rakitra.")
        return None
    except Exception as e:
        st.error(f"Nisy olana: {e}")
        return None

st.title("📖 Baiboly Mg1865 Interlineaire")

bible_data = load_bible()

if bible_data:
    # Mitady ny votoatiny (flexible ho an'ny rafitra samihafa)
    content = bible_data.get('books', bible_data)
    
    if isinstance(content, dict):
        # 1. Safidy Boky
        books = sorted(list(content.keys()))
        book_sel = st.sidebar.selectbox("Fidio ny boky", books)
        
        # 2. Safidy Toko
        chapters = content[book_sel]
        if isinstance(chapters, dict):
            ch_list = sorted(list(chapters.keys()), key=lambda x: int(x) if x.isdigit() else 0)
            ch_sel = st.sidebar.selectbox("Toko", ch_list)
            
            st.subheader(f"{book_sel} - Toko {ch_sel}")
            
            # 3. Fampisehoana ny andininy
            verses = chapters[ch_sel]
            for v_num in sorted(verses.keys(), key=lambda x: int(x) if x.isdigit() else 0):
                txt = verses[v_num]
                st.write(f"**{v_num}.** {txt}")
                
                # Karoka Strong
                strongs = re.findall(r'[GH]\d+', txt)
                if strongs:
                    cols = st.columns(len(strongs))
                    for i, code in enumerate(strongs):
                        if cols[i].button(f"🔍 {code}", key=f"{ch_sel}_{v_num}_{code}"):
                            # Mitady diksionera eo amin'ny root
                            dict_fn = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
                            if os.path.exists(dict_fn):
                                with open(dict_fn, 'r', encoding='utf-8') as df:
                                    s_data = json.load(df)
                                    st.info(f"**{code}:** {s_data.get(code, 'Tsy hita ny dikany')}")
                            else:
                                st.warning(f"Tsy hita ny {dict_fn}")
    else:
        st.error("Ny rafitra JSON dia tsy araka ny nantenaina (mila dictionary).")
