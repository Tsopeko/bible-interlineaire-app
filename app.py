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
    # Lister les fichiers .json dans le dossier data
    files = [f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    
    if files:
        # 1. CHOIX DU LIVRE
        livre_choisi = st.sidebar.selectbox("Fidio ny boky", sorted(files))
        data = load_book(livre_choisi)
        
        if data:
            # 2. EXTRACTION DES TOKO (Chapitres)
            # On récupère toutes les clés qui sont des numéros (ex: "1", "2")
            toko_keys = sorted([k for k in data.keys() if k.isdigit()], key=int)
            
            if toko_keys:
                chap_num = st.sidebar.selectbox("Toko", toko_keys)
                
                st.header(f"{livre_choisi} - Toko {chap_num}")
                st.divider()
                
                # 3. EXTRACTION DES VERSETS
                versets_data = data[chap_num]
                
                if isinstance(versets_data, dict):
                    # Si les versets sont aussi des clés "1", "2"...
                    verset_keys = sorted([v for v in versets_data.keys() if v.isdigit()], key=int)
                    for v_num in verset_keys:
                        txt = versets_data[v_num]
                        st.write(f"**{v_num}.** {txt}")
                elif isinstance(versets_data, list):
                    # Si les versets sont une simple liste
                    for i, txt in enumerate(versets_data):
                        st.write(f"**{i+1}.** {txt}")
            else:
                st.error("Tsy hita ny toko ato amin'ity fichier ity.")
    else:
        st.info("Ampidiro ao amin'ny dossier 'data' ny fichiers .json")
else:
    st.error("Tsy hita ny dossier 'data' ao amin'ny GitHub.")
