import streamlit as st
import json

# Configuration
st.set_page_config(page_title="Baiboly Interlinéaire 1865", layout="wide")

# Chargement du fichier Malagasy 1865
try:
    with open('Bible_MG65.json', 'r', encoding='utf-8') as f:
        bible_data = json.load(f)
except FileNotFoundError:
    st.error("Fichier 'Bible_MG65.json' introuvable.")
    st.stop()

st.title("📖 Baiboly Malagasy 1865 Interlinéaire")

# --- NAVIGATION ---
liste_livres = [b['name'] for b in bible_data['books']]
livre_choisi = st.sidebar.selectbox("Fidio ny boky", liste_livres)
donnees_livre = next(b for b in bible_data['books'] if b['name'] == livre_choisi)

liste_chapitres = [c['chapter'] for c in donnees_livre['chapters']]
chapitre_choisi = st.sidebar.selectbox("Toko", liste_chapitres)
donnees_chapitre = next(c for c in donnees_livre['chapters'] if c['chapter'] == chapitre_choisi)

# --- LE BOUTON MAGIQUE ---
st.sidebar.divider()
afficher_original = st.sidebar.toggle("Afficher l'Hébreu/Grec (Strong)")

# --- AFFICHAGE ---
st.header(f"{livre_choisi} - Toko {chapitre_choisi}")

for v in donnees_chapitre['verses']:
    st.markdown(f"**{v['verse']}.** {v['text']}")
    
    # Si le bouton est activé, on affiche une ligne d'étude
    if afficher_original:
        # Simulation d'analyse (Dans une version finale, on lie ici une base de données Strong)
        with st.expander(f"Fandalinana ny andininy {v['verse']}"):
            st.info("Fikarohana ny teny fototra (Gireka/Hebreo)...")
            st.caption("Ity fizarana ity dia mampiseho ny dikan-teny tamin'ny 1865 miaraka amin'ny Strong Codes.")
