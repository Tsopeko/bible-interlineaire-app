import streamlit as st
import json

st.set_page_config(page_title="Baiboly Interlinéaire 1865", layout="wide")

# Chargement intelligent de tous les dictionnaires
@st.cache_data
def load_all_resources():
    with open('Bible_MG65.json', 'r', encoding='utf-8') as f:
        mg_bible = json.load(f)
    
    # Chargement Hébreu
    try:
        with open('strongs_hebrew_dictionary.json', 'r', encoding='utf-8') as f:
            he_dict = json.load(f)
    except:
        he_dict = {}
        
    # Chargement Grec
    try:
        with open('strongs_greek_dictionary.json', 'r', encoding='utf-8') as f:
            gr_dict = json.load(f)
    except:
        gr_dict = {}
        
    return mg_bible, he_dict, gr_dict

bible_data, dict_he, dict_gr = load_all_resources()

st.title("📖 Baiboly Malagasy 1865 & Teny Fototra")

# Navigation
livres = [b['name'] for b in bible_data['books']]
livre_nom = st.sidebar.selectbox("Boky", livres)
donnees_livre = next(b for b in bible_data['books'] if b['name'] == livre_nom)

# Détecter si c'est l'Ancien ou le Nouveau Testament
# (Exemple simple : si le livre est après Malakia, c'est le Nouveau Testament)
is_nt = livres.index(livre_nom) >= 39 

chapitres = [c['chapter'] for c in donnees_livre['chapters']]
chap_num = st.sidebar.selectbox("Toko", chapitres)
donnees_chapitre = next(c for c in donnees_livre['chapters'] if c['chapter'] == chap_num)

mode_etude = st.sidebar.toggle("Hizaha ny teny fototra (Strong)")

# Affichage des versets
for v in donnees_chapitre['verses']:
    st.write(f"**{v['verse']}.** {v['text']}")
    
    if mode_etude:
        with st.expander(f"Fandalinana {livre_nom} {chap_num}:{v['verse']}"):
            if is_nt:
                st.info("Fikarohana ao amin'ny dikan-teny Gireka (Nouveau Testament)")
                # Ici le code cherchera dans dict_gr
            else:
                st.warning("Fikarohana ao amin'ny dikan-teny Hebraio (Ancien Testament)")
                # Ici le code cherchera dans dict_he
