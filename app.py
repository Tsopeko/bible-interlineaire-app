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
# --- DICTIONNAIRE STRONG ---
st.sidebar.divider()
st.sidebar.header("📚 Diksionera Strong")
strong_code = st.sidebar.text_input("Hampidiro ny code (ohatra: G2424 na H7225)")

if strong_code:
    # Mamaritra raha Grika na Hebreo ny code
    is_greek = strong_code.upper().startswith('G')
    is_hebrew = strong_code.upper().startswith('H')
    
    dict_file = "strongs-greek-dictionary.json" if is_greek else "strongs-hebrew-dictionary.json"
    
    try:
        with open(f"{dict_file}.json", 'r', encoding='utf-8') as f:
            strong_data = json.load(f)
            
        if clean_code in strong_data:
            info = strong_data[clean_code]
            st.info(f"**Strong {clean_code}**")
            # Afaka ovaina arakaraka ny firafitry ny JSON-nao ireto fields ireto
            st.write(f"**Dikany:** {info.get('lemma', '')} - {info.get('translit', '')}")
            st.write(f"**Mombamomba:** {info.get('definition', '')}")
        else:
            st.sidebar.error("Tsy hita io code io.")
    except Exception as e:
        st.sidebar.warning("Tsy mbola vaky ny diksionera. Hamarino ny anaran'ny fichier.")
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
