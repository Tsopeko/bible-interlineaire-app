import streamlit as st
import json
import os

st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide")

DATA_PATH = "data"

def load_book(name):
    try:
        with open(f"{DATA_PATH}/{name}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

st.title("📖 Baiboly Malagasy 1865")

if os.path.exists(DATA_PATH):
    # On liste tous les fichiers dans le dossier data
    files = [f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    
    if files:
        livre_choisi = st.sidebar.selectbox("Fidio ny boky", sorted(files))
        data = load_book(livre_choisi)
        
        if data:
            # --- DÉTECTION INTELLIGENTE DE LA STRUCTURE ---
            # 1. On cherche la liste des chapitres
            if isinstance(data, list):
                chapters_list = data
            elif isinstance(data, dict):
                # On teste toutes les clés possibles (chapters, toko, etc.)
                chapters_list = data.get('chapters', data.get('toko', data.get('results', [])))
            else:
                chapters_list = []

            if chapters_list:
                nb_chaps = len(chapters_list)
                chap_num = st.sidebar.number_input("Toko", 1, nb_chaps, 1)
                
                st.header(f"{livre_choisi} - Toko {chap_num}")
                st.divider()
                
                # 2. On récupère les versets du chapitre
                versets = chapters_list[chap_num - 1]
                
                if isinstance(versets, list):
                    for i, v in enumerate(versets):
                        # Si le verset est un dictionnaire {"text": "..."} ou juste du texte
                        txt = v.get('text', v) if isinstance(v, dict) else v
                        st.write(f"**{i+1}.** {txt}")
                else:
                    st.write(versets) # Pour le texte simple
            else:
                st.error("Tsy hita ny firafitry ny toko (chapters) ato amin'ity fichier ity.")
                # Optionnel: afficher le contenu pour déboguer
                with st.expander("Hijery ny ao anaty fichier"):
                    st.json(data)
    else:
        st.info("Ampidiro ao anatin'ny dossier 'data' ny fichiers .json")
else:
    st.error("Tsy hita ny dossier 'data' ao amin'ny GitHub.")
