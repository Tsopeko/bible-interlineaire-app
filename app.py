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
    # Lister les fichiers .json présents
    files = [f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    
    if files:
        # Sélection du livre (ex: 1-jaona, samoela...)
        livre_choisi = st.sidebar.selectbox("Fidio ny boky", sorted(files))
        data = load_book(livre_choisi)
        
        if data:
            # On cherche les chapitres (soit une liste, soit des clés "1", "2"...)
            if isinstance(data, dict):
                toko_keys = sorted([k for k in data.keys() if k.isdigit()], key=int)
            elif isinstance(data, list):
                toko_keys = [str(i+1) for i in range(len(data))]
            else:
                toko_keys = []

            if toko_keys:
                chap_num = st.sidebar.selectbox("Toko", toko_keys)
                st.header(f"{livre_choisi} - Toko {chap_num}")
                st.divider()
                
                # Récupération du contenu du chapitre
                idx = int(chap_num) - 1 if isinstance(data, list) else chap_num
                versets_data = data[idx]
                
                # Affichage des versets (format dictionnaire ou liste)
                if isinstance(versets_data, dict):
                    v_keys = sorted([v for v in versets_data.keys() if v.isdigit()], key=int)
                    for v_num in v_keys:
                        st.write(f"**{v_num}.** {versets_data[v_num]}")
                elif isinstance(versets_data, list):
                    for i, txt in enumerate(versets_data):
                        st.write(f"**{i+1}.** {txt}")
            else:
                st.warning("Tsy hita ny toko ato amin'ity fichier ity.")
    else:
        st.info("Ampidiro ao amin'ny dossier 'data' ny fichiers .json")
else:
    st.error("Tsy hita ny dossier 'data' ao amin'ny GitHub.")
