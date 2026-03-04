import streamlit as st
import json
import os

st.set_page_config(page_title="Baiboly 1865", layout="wide", page_icon="📖")

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
# Curseur pour la taille du texte
taille_texte = st.sidebar.slider("Haben'ny soratra", 12, 30, 18)

st.sidebar.divider()

# --- MOTEUR DE RECHERCHE ---
st.sidebar.header("🔍 Karoka")
mot_cle = st.sidebar.text_input("Hikaroka teny")

if mot_cle:
    st.header(f"Valin'ny karoka: '{mot_cle}'")
    if st.button("Hiverina hamaky"):
        st.rerun()
        
    found_count = 0
    files = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')])
    
    for file in files:
        book_data = load_book(file)
        if book_data:
            for chap_num, versets in book_data.items():
                if isinstance(versets, dict):
                    for v_num, txt in versets.items():
                        if mot_cle.lower() in txt.lower():
                            # Affichage avec la taille choisie
                            st.markdown(f"<p style='font-size:{taille_texte}px;'><b>{file} {chap_num}:{v_num}</b><br>{txt}</p>", unsafe_html=True)
                            st.divider()
                            found_count += 1
    st.stop() 

# --- LECTURE NORMALE ---
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
                
                # Affichage des versets avec style HTML pour la taille
                for v_num in v_keys:
                    txt_verset = versets_dict[v_num]
                    st.markdown(f"<span style='font-size:{taille_texte}px;'><b>{v_num}.</b> {txt_verset}</span>", unsafe_html=True)
    else:
        st.info("Ampidiro ao anatin'ny dossier 'data' ireo fichiers .json")
