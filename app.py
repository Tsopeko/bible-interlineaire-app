import streamlit as st
import json
import os

# Configuration de la page
st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide", page_icon="📖")

DATA_PATH = "data"

@st.cache_data
def load_book(name):
    try:
        with open(f"{DATA_PATH}/{name}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

# Titre principal
st.title("📖 Baiboly Malagasy 1865")

if os.path.exists(DATA_PATH):
    # Liste des livres (.json) dans le dossier data
    files = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')])
    
    if files:
        # Menu de sélection du livre
        livre_choisi = st.sidebar.selectbox("Fidio ny boky", files)
        data = load_book(livre_choisi)
        
        if data:
            # Récupération des chapitres (clés numériques comme "1", "2")
            toko_keys = sorted([k for k in data.keys() if k.isdigit()], key=int)
            
            if toko_keys:
                chap_num = st.sidebar.selectbox("Toko", toko_keys)
                
                # Affichage du titre du chapitre
                st.subheader(f"{livre_choisi} - Toko {chap_num}")
                st.divider()
                
                # Affichage des versets
                versets_dict = data[chap_num]
                v_keys = sorted([v for v in versets_dict.keys() if v.isdigit()], key=int)
                
                for v_num in v_keys:
                    st.write(f"**{v_num}.** {versets_dict[v_num]}")
            else:
                st.warning("Tsy hita ny toko ato amin'ity boky ity.")
    else:
        st.info("Ampidiro ao amin'ny dossier 'data' ireo fichiers .json")
else:
    st.error("Tsy hita ny dossier 'data' ao amin'ny GitHub-nao.")
