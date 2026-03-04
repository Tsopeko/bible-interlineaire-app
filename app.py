import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Mg1865 Interlineaire", layout="wide")

# Path mankany amin'ny rakitra
BIBLE_FILE = "data/Mg1865.json"

@st.cache_data
def load_bible_data():
    if not os.path.exists(BIBLE_FILE):
        return None
    try:
        # Mampiasa encoding utf-8 mba hamakiana ny teny malagasy sy ny kaody Strong
        with open(BIBLE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Fahadisoana tamin'ny famakiana ny Baiboly: {e}")
        return None

st.title("📖 Baiboly Mg1865 Interlineaire")

data = load_bible_data()

if data:
    # Ny Mg1865.json dia matetika manana rafitra { "books": { "Genesisy": { "1": { "1": "soratra" } } } }
    # Raha tsy misy 'books' dia raisina ho ny data manontolo no misy ny boky
    bible_content = data.get('books', data)
    
    if isinstance(bible_content, dict):
        # 1. Safidy ny Boky ao amin'ny sidebar
        sorted_books = sorted(list(bible_content.keys()))
        book_sel = st.sidebar.selectbox("Fidio ny boky", sorted_books)
        
        # 2. Safidy ny Toko
        chapters = bible_content[book_sel]
        if isinstance(chapters, dict):
            # Alahatra araka ny isa ny toko
            sorted_ch = sorted(list(chapters.keys()), key=lambda x: int(x) if x.isdigit() else 0)
            ch_sel = st.sidebar.selectbox("Toko", sorted_ch)
            
            st.subheader(f"{book_sel} - Toko {ch_sel}")
            
            # 3. Fampisehoana ny andininy
            verses = chapters[ch_sel]
            for v_num in sorted(verses.keys(), key=lambda x: int(x) if x.isdigit() else 0):
                verse_text = verses[v_num]
                st.write(f"**{v_num}.** {verse_text}")
                
                # Fikarohana kaody Strong (G ho an'ny Grika, H ho an'ny Hebreo)
                strong_codes = re.findall(r'[GH]\d+', verse_text)
                if strong_codes:
                    cols = st.columns(len(strong_codes))
                    for i, code in enumerate(strong_codes):
                        if cols[i].button(f"🔍 {code}", key=f"{ch_sel}_{v_num}_{code}"):
                            # Mitady ny diksionera mifanaraka aminy
                            dict_file = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
                            if os.path.exists(dict_file):
                                with open(dict_file, 'r', encoding='utf-8') as df:
                                    s_dict = json.load(df)
                                    meaning = s_dict.get(code, "Tsy hita ny dikan'io kaody io.")
                                    st.info(f"**{code}:** {meaning}")
                            else:
                                st.warning(f"Tsy hita ny rakitra {dict_file}")
    else:
        st.error("Ny rafitra ao anatin'ny Mg1865.json dia tsy hita (mila dictionary).")
else:
    st.info("Andraso kely, mbola mampiditra ny rakitra avy ao amin'ny 'data/Mg1865.json'...")
