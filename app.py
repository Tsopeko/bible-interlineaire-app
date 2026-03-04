import streamlit as st
import json
import os

st.set_page_config(page_title="Baiboly 1865 - Karoka", layout="wide", page_icon="🔍")

DATA_PATH = "data"

@st.cache_data
def load_book(name):
    try:
        with open(f"{DATA_PATH}/{name}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

st.title("📖 Baiboly Malagasy 1865")

# --- BARRE DE RECHERCHE DANS LA SIDEBAR ---
st.sidebar.header("🔍 Karoka")
mot_cle = st.sidebar.text_input("Hikaroka teny (ohatra: Jesosy)")

if mot_cle:
    st.header(f"Valin'ny karoka: '{mot_cle}'")
    found = False
    
    # On parcourt tous les fichiers .json du dossier data
    files = [f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    
    for file in files:
        book_data = load_book(file)
        if book_data:
            # On parcourt chaque chapitre
            for chap_num, versets in book_data.items():
                if isinstance(versets, dict):
                    # On parcourt chaque verset
                    for v_num, txt in versets.items():
                        if mot_cle.lower() in txt.lower():
                            st.write(f"**{file} {chap_num}:{v_num}**")
                            st.write(f"_{txt}_")
                            st.divider()
                            found = True
    
    if not found:
        st.warning("Tsy nisy valiny io karoka io.")
    st.stop() # On arrête l'affichage normal si on est en mode recherche

# --- AFFICHAGE NORMAL (LECTURE) ---
if os.path.exists(DATA_PATH):
    files = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')])
    if files:
        livre_choisi = st.sidebar.selectbox("Fidio ny boky", files)
        data = load_book(livre_choisi)
        if data:
            toko_keys = sorted([k for k in data.keys() if k.isdigit()], key=int)
            if toko_keys:
                chap_num = st.sidebar.selectbox("Toko", toko_keys)
                st.subheader(f"{livre_choisi} - Toko {chap_num}")
                versets_dict = data[chap_num]
                v_keys = sorted([v for v in versets_dict.keys() if v.isdigit()], key=int)
                for v_num in v_keys:
                    st.write(f"**{v_num}.** {versets_dict[v_num]}")
