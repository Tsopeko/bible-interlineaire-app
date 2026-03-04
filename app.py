import streamlit as st
import json
import os

st.set_page_config(page_title="Baiboly 1865", layout="wide")

# Chemin vers ton nouveau dossier
DATA_PATH = "data"

def load_book(name):
    try:
        with open(f"{DATA_PATH}/{name}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

st.title("📖 Baiboly Malagasy 1865")

# On liste tous les fichiers .json dans le dossier 'data'
if os.path.exists(DATA_PATH):
    files = [f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    
    if files:
        livre_choisi = st.sidebar.selectbox("Fidio ny boky", sorted(files))
        data = load_book(livre_choisi)
        
        if data:
            # Navigation par chapitre
            chaps = [str(i+1) for i in range(len(data['chapters']))]
            chap_num = st.sidebar.selectbox("Toko", chaps)
            
            # Affichage
            st.header(f"{livre_choisi} - Toko {chap_num}")
            versets = data['chapters'][int(chap_num)-1]
            for i, texte in enumerate(versets):
                st.write(f"**{i+1}.** {texte}")
    else:
        st.info("Tsy misy boky hita ao amin'ny dossier 'data'. Ampidiro ao ny fichiers .json.")
else:
    st.error("Tsy hita ny dossier 'data'. Créer-o aloha io dossier io ao amin'ny GitHub.")
