import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Mg1865", layout="wide")

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

st.title("📖 Baiboly Mg1865 Interlineaire")

# 1. Load Bible
bible_data = load_json("data/Mg1865.json")

if bible_data:
    # --- DINGANA 1: Mitady ny toerana misy ny boky ---
    # Raha misy 'books', 'vaka', na 'metadata' ny JSON
    if isinstance(bible_data, dict):
        if 'books' in bible_data:
            content = bible_data['books']
        else:
            content = bible_data
    else:
        st.error("Ny JSON dia 'List' fa tsy 'Dictionary'. Avereno jerena ny format.")
        st.stop()

    # --- DINGANA 2: Safidy Boky sy Toko ---
    try:
        books = sorted(list(content.keys()))
        book_sel = st.sidebar.selectbox("Boky", books)
        
        chapters = content[book_sel]
        ch_list = sorted(list(chapters.keys()), key=lambda x: int(x) if str(x).isdigit() else 0)
        ch_sel = st.sidebar.selectbox("Toko", ch_list)
        
        # --- DINGANA 3: Fampisehoana ---
        st.subheader(f"{book_sel} - Toko {ch_sel}")
        verses = chapters[ch_sel]
        
        for v_num in sorted(verses.keys(), key=lambda x: int(x) if str(x).isdigit() else 0):
            txt = verses[v_num]
            st.write(f"**{v_num}.** {txt}")
            
            # Strong buttons
            codes = re.findall(r'[GH]\d+', txt)
            if codes:
                cols = st.columns(len(codes))
                for i, c in enumerate(codes):
                    if cols[i].button(f"🔍 {c}", key=f"{ch_sel}_{v_num}_{c}"):
                        fn = "strongs-greek-dictionary.json" if c.startswith('G') else "strongs-hebrew-dictionary.json"
                        s_data = load_json(fn)
                        if s_data:
                            st.info(f"**{c}:** {s_data.get(c, 'Tsy hita')}")
    except Exception as e:
        st.error(f"Nisy olana teo am-pamakiana ny rafitra: {e}")
        st.write("Andramo jerena ny 'Raw' an'ny JSON-nao ao amin'ny GitHub.")
else:
    st.warning("Tsy hita ny rakitra 'data/Mg1865.json'")
