import streamlit as st
import json

# Configuration de la page
st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide")

# Chargement du fichier complet
try:
    with open('Bible_MG65.json', 'r', encoding='utf-8') as f:
        bible_data = json.load(f)
except FileNotFoundError:
    st.error("Fichier 'Bible_MG65.json' introuvable. Vérifiez le nom sur GitHub.")
    st.stop()

st.title("📖 Baiboly Malagasy 1865")

# --- NAVIGATION ---
# 1. Sélection du Livre
liste_livres = [b['name'] for b in bible_data['books']]
livre_choisi = st.sidebar.selectbox("Fidio ny boky (Livre)", liste_livres)

# Trouver les données du livre sélectionné
donnees_livre = next(b for b in bible_data['books'] if b['name'] == livre_choisi)

# 2. Sélection du Chapitre
liste_chapitres = [c['chapter'] for c in donnees_livre['chapters']]
chapitre_choisi = st.sidebar.selectbox("Toko (Chapitre)", liste_chapitres)

# Trouver les données du chapitre sélectionné
donnees_chapitre = next(c for c in donnees_livre['chapters'] if c['chapter'] == chapitre_choisi)

# --- AFFICHAGE ---
st.header(f"{livre_choisi} - Toko {chapitre_choisi}")
st.divider()

# Affichage de chaque verset
for v in donnees_chapitre['verses']:
    st.markdown(f"**{v['verse']}.** {v['text']}")

# --- PIED DE PAGE ---
st.sidebar.divider()
st.sidebar.info("Ity baiboly ity dia dikan-teny tamin'ny 1865.")
