import streamlit as st
import json

st.set_page_config(page_title="Baiboly & Strong", layout="wide")

# Chargement sécurisé
def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

bible_data = load_json('Bible_MG65.json')
dict_he = load_json('strongs_hebrew_dictionary.json')

if bible_data is None:
    st.error("Misy olana: Tsy hita ny 'Bible_MG65.json'. Hamarino ny anarany ao amin'ny GitHub.")
    st.stop()

st.title("📖 Baiboly Malagasy 1865 & Teny Fototra")

# Navigation
try:
    livres = [b['name'] for b in bible_data['books']]
    livre_nom = st.sidebar.selectbox("Fidio ny boky", livres)
    donnees_livre = next(b for b in bible_data['books'] if b['name'] == livre_nom)

    chapitres = [c['chapter'] for c in donnees_livre['chapters']]
    chap_num = st.sidebar.selectbox("Toko", chapitres)
    donnees_chapitre = next(c for c in donnees_livre['chapters'] if c['chapter'] == chap_num)

    # Affichage
    for v in donnees_chapitre['verses']:
        st.write(f"**{v['verse']}.** {v['text']}")
        
        # Si on a le dictionnaire, on peut ajouter des infos ici plus tard
        if dict_he and st.sidebar.toggle("Hizaha Hebraio", key=f"t_{v['verse']}"):
            st.info("Fikarohana teny fototra...")
except Exception as e:
    st.error(f"Olana teo am-pamakiana ny baiboly: {e}")
