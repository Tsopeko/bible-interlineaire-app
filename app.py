import streamlit as st
import json

st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide")

# On charge le gros fichier Malagasy
try:
    with open('Bible_MG65.json', 'r', encoding='utf-8') as f:
        bible_complete = json.load(f)
except FileNotFoundError:
    st.error("Erreur : Le fichier Bible_MG65.json est introuvable sur GitHub.")
    st.stop()

st.title("📖 Baiboly Malagasy 1865")

# 1. Sélection du Livre
livres = [b['name'] for b in bible_complete['books']]
livre_nom = st.sidebar.selectbox("Fidio ny boky (Livre)", livres)

# Trouver le livre sélectionné
livre_data = next(b for b in bible_complete['books'] if b['name'] == livre_nom)

# 2. Sélection du Chapitre
chapitres = [c['chapter'] for c in livre_data['chapters']]
chap_num = st.sidebar.selectbox("Fidio ny toko (Chapitre)", chapitres)

# Trouver le chapitre sélectionné
chap_data = next(c for c in livre_data['chapters'] if c['chapter'] == chap_num)

# Affichage des versets
st.subheader(f"{livre_nom} Toko {chap_num}")

for v in chap_data['verses']:
    st.write(f"**{v['verse']}.** {v['text']}")
