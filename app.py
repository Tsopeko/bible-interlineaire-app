import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Mg1865", layout="wide")

# Toerana misy ny rakitra
BIBLE_FILE = "data/Mg1865.json"

@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Fahadisoana: {e}")
        return None

st.title("📖 Baiboly Mg1865 Interlineaire")

# 1. Fametrahana ny Baiboly
bible_data = load_data(BIBLE_FILE)

if bible_data:
    # Mitady ny votoatiny (na ao anaty 'books' na mivantana)
    content = bible_data.get('books', bible_data)
    
    if isinstance(content, dict):
        # Safidy Boky (Genesisy, sns)
        books_list = sorted(list(content.keys()))
        selected_book = st.sidebar.selectbox("Fidio ny boky", books_list)
        
        # Safidy Toko
        chapters = content[selected_book]
        if isinstance(chapters, dict):
            ch_list = sorted(list(chapters.keys()), key=lambda x: int(x) if x.isdigit() else 0)
            selected_ch = st.sidebar.selectbox("Toko", ch_list)
            
            st.subheader(f"{selected_book} - Toko {selected_ch}")
            
            # Fampisehoana ny andininy
            verses = chapters[selected_ch]
            for v_num in sorted(verses.keys(), key=lambda x: int(x) if x.isdigit() else 0):
                text = verses[v_num]
                st.write(f"**{v_num}.** {text}")
                
                # Fikarohana ny kaody Strong (G... na H...)
                strong_codes = re.findall(r'[GH]\d+', text)
                if strong_codes:
                    cols = st.columns(len(strong_codes))
                    for i, code in enumerate(strong_codes):
                        if cols[i].button(f"🔍 {code}", key=f"{selected_ch}_{v_num}_{code}"):
                            # Mitady ny diksionera mifanaraka aminy
                            dict_name = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
                            s_dict = load_data(dict_name)
                            if s_dict and code in s_dict:
                                st.info(f"**{code}:** {s_dict[code]}")
                            else:
                                st.warning(f"Tsy hita ny dikan'ny {code}")
    else:
        st.error("Ny rafitra JSON dia tsy araka ny nantenaina. Hamarino ny format.")
else:
    st.warning("Andraso kely, mbola tsy mipoitra ny rakitra 'data/Mg1865.json'...")
