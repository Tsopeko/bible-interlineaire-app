import streamlit as st
import json
import os

# Fikirana fototra ny pejy
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
# Ity ny slider hanovana ny haben'ny soratra
taille_texte = st.sidebar.slider("Haben'ny soratra", 14, 40, 20)

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
        files = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')])
        
        for file in files:
            book_data = load_book(file)
            if book_data:
                for chap_num, versets in book_data.items():
                    if isinstance(versets, dict):
                        for v_num, txt in versets.items():
                            if mot_cle.lower() in txt.lower():
                                # Fampisehoana ny vokatry ny karoka miaraka amin'ny habe voafidy
                                st.markdown(f'<div style="font-size:{taille_texte}px; border-left: 3px solid #ff4b4b; padding-left: 10px; margin-bottom: 20px;"><b>{file} {chap_num}:{v_num}</b><br>{txt}</div>', unsafe_html=True)
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
            toko_keys = sorted([k for k in data.keys() if k.isdigit()], key=int)
            if toko_keys:
                chap_num = st.sidebar.selectbox("Toko", toko_keys)
                st.subheader(f"{livre_choisi} - Toko {chap_num}")
                
                versets_dict = data[chap_num]
                v_keys = sorted([v for v in versets_dict.keys() if v.isdigit()], key=int)
                
                # Ity no mampiseho ny andininy tsirairay amin'ny habe mety
                for v_num in v_keys:
                    txt_verset = versets_dict[v_num]
                    # Nampiana <div> HTML mba ho afaka ovaina ny font-size
                    st.markdown(f'<div style="font-size:{taille_texte}px; margin-bottom:12px; line-height: 1.6;"><b>{v_num}.</b> {txt_verset}</div>', unsafe_html=True)
            else:
                st.warning("Tsy hita ny toko ato amin'ity boky ity.")
    else:
        st.info("Ampidiro ao anatin'ny dossier 'data' ireo fichiers .json")
else:
    st.error("Tsy hita ny dossier 'data' ao amin'ny GitHub-nao.")
