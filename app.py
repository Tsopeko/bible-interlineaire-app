import streamlit as st
import json

st.set_page_config(page_title="Baiboly Malagasy 1865 Interlinéaire", layout="wide")

# Fonction de chargement sécurisée
def load_json_data(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

# Chargement des ressources
bible_data = load_json_data('Bible_MG65.json')
dict_he = load_json_data('strongs-hebrew-dictionary.json')

st.title("📖 Baiboly Malagasy 1865 & Teny Fototra")

if bible_data is None:
    st.error("Tsy hita ny 'Bible_MG65.json'. Hamarino ny anarany ao amin'ny GitHub.")
    st.stop()

# --- NAVIGATION ---
try:
    # Adaptation à la structure du fichier de Rohan29-AN
    livres = [b['name'] for b in bible_data['books']]
    livre_nom = st.sidebar.selectbox("Fidio ny boky", livres)
    
    # Trouver le livre
    donnees_livre = next(b for b in bible_data['books'] if b['name'] == livre_nom)
    
    # Trouver le chapitre
    chapitres = [c['chapter'] for c in donnees_livre['chapters']]
    chap_num = st.sidebar.selectbox("Toko", chapitres)
    donnees_chapitre = next(c for c in donnees_livre['chapters'] if c['chapter'] == chap_num)

    # --- AFFICHAGE ---
    st.header(f"{livre_nom} - Toko {chap_num}")
    
    mode_etude = st.sidebar.toggle("Hizaha ny teny fototra (Hebraio)")

    for v in donnees_chapitre['verses']:
        st.write(f"**{v['verse']}.** {v['text']}")
        
        # Affichage du dictionnaire si activé
        if mode_etude and dict_he:
            with st.expander(f"Fandalinana andininy {v['verse']}"):
                st.write("Dikan-teny Hebraio sy Strong Codes hita eto...")
                # Ici on pourra lier les codes Strong aux mots
                
except Exception as e:
    st.error(f"Nisy olana kely: {e}")
