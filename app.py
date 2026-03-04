import streamlit as st
import json
import os

st.set_page_config(page_title="Test Baiboly 1865", layout="wide")

# Chemin vers le dossier que tu as créé
DATA_PATH = "data"

def load_book(name):
    try:
        # On cherche le fichier dans le dossier data
        with open(f"{DATA_PATH}/{name}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

st.title("📖 Test Baiboly Malagasy 1865")

# Vérifier si le dossier existe et contient des fichiers
if os.path.exists(DATA_PATH):
    files = [f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    
    if files:
        st.sidebar.success(f"{len(files)} boky hita ao amin'ny data")
        livre_choisi = st.sidebar.selectbox("Fidio ny boky hovakiana", sorted(files))
        
        data = load_book(livre_choisi)
        
        if data:
            # Menu des chapitres
            nb_chaps = len(data['chapters'])
            chap_num = st.sidebar.slider("Toko", 1, nb_chaps, 1)
            
            st.header(f"{livre_choisi} - Toko {chap_num}")
            st.divider()
            
            # Affichage des versets
            versets = data['chapters'][chap_num - 1]
            for i, texte in enumerate(versets):
                st.write(f"**{i+1}.** {texte}")
    else:
        st.warning("Ampidiro ao amin'ny dossier 'data' ny fichier .json (ohatra: Genesisy.json)")
else:
    st.error("Tsy hita ny dossier 'data'. Créer-o ao amin'ny GitHub io dossier io.")
