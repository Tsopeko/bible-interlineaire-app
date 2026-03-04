import streamlit as st
import json
import os

st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide", page_icon="📖")

DATA_PATH = "data"

@st.cache_data
def load_book(name):
    try:
        with open(f"{DATA_PATH}/{name}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

st.title("📖 Baiboly Malagasy 1865")

# --- PARAMÈTRES D'AFFICHAGE (SideBar) ---
st.sidebar.header("⚙️ Fikirana")
# Nesorintsika aloha ilay zoom fa miteraka TypeError
st.sidebar.info("Miasa ny fikarohana sy ny famakiana.")
st.sidebar.divider()

# --- MOTEUR DE RECHERCHE ---
st.sidebar.header("🔍 Karoka")
mot_cle = st.sidebar.text_input("Hikaroka teny")

if mot_cle:
    st.header(f"Valin'ny karoka: '{mot_cle}'")
    if st.button("Hiverina hamaky"):
        st.rerun()
        
    found_count = 0
    if os.path.exists(DATA_PATH):
        files = sorted([f for f in os.listdir(DATA_PATH) if f.endswith('.json')])
        for file_name in files:
            book_name = file_name.replace('.json', '')
            book_data = load_book(book_name)
            if book_data:
                for chap_num, versets in book_data.items():
                    if isinstance(versets, dict):
                        for v_num, txt in versets.items():
                            if mot_cle.lower() in txt.lower():
                                # Fampisehoana tsotra nefa mazava
                                st.write(f"**{book_name} {chap_num}:{v_num}**")
                                st.write(txt)
                                st.divider()
                                found_count += 1
    st.sidebar.info(f"Verset {found_count} no hita.")
    st.stop() 

# --- LECTURE NORMALE ---
if os.path.exists(DATA_PATH):
    files = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')])
    if files:
        livre_choisi = st.sidebar.selectbox("Fidio ny boky", files)
        data = load_book(livre_choisi)
        if data:
            # Maka ny laharan'ny toko rehetra
            toko_keys = sorted([k for k in data.keys() if k.isdigit()], key=int)
            if toko_keys:
                chap_num = st.sidebar.selectbox("Toko", toko_keys)
                st.subheader(f"{livre_choisi} - Toko {chap_num}")
                
                versets_dict = data[chap_num]
                v_keys = sorted([v for v in versets_dict.keys() if v.isdigit()], key=int)
                
                # Fampisehoana ny andininy tsirairay amin'ny fomba tsotra
                for v_num in v_keys:
                    txt_verset = versets_dict[v_num]
                    st.write(f"**{v_num}.** {txt_verset}")
            else:
                st.warning("Tsy hita ny toko.")
    else:
        st.info("Ampidiro ao anatin'ny dossier 'data' ireo fichiers .json")
