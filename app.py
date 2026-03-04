import streamlit as st
import json
import os

st.set_page_config(page_title="Test Baiboly 1865", layout="wide")

DATA_PATH = "data"

def load_book(name):
    try:
        with open(f"{DATA_PATH}/{name}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

st.title("📖 Baiboly Malagasy 1865")

if os.path.exists(DATA_PATH):
    files = [f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    
    if files:
        livre_choisi = st.sidebar.selectbox("Fidio ny boky", sorted(files))
        data = load_book(livre_choisi)
        
        if data:
            # --- DÉTECTION AUTOMATIQUE DES CHAPITRES ---
            # On cherche si les chapitres sont dans 'chapters' ou si le fichier est une liste directe
            chapters_data = data.get('chapters', data if isinstance(data, list) else [])
            
            if chapters_data:
                nb_chaps = len(chapters_data)
                chap_num = st.sidebar.number_input("Toko", 1, nb_chaps, 1)
                
                st.header(f"{livre_choisi} - Toko {chap_num}")
                st.divider()
                
                # Récupération des versets du chapitre choisi
                versets = chapters_data[chap_num - 1]
                
                # Si les versets sont des dictionnaires (avec 'text'), on les extrait
                for i, v in enumerate(versets):
                    txt = v.get('text', v) if isinstance(v, dict) else v
                    st.write(f"**{i+1}.** {txt}")
            else:
                st.warning("Tsy hita ny toko ato amin'ity fichier ity.")
    else:
        st.info("Ampidiro ao amin'ny dossier 'data' ny fichier .json")
else:
    st.error("Tsy hita ny dossier 'data' ao amin'ny GitHub.")
