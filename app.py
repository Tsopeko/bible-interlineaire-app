import streamlit as st
import json

st.set_page_config(page_title="Bible Interlinéaire Pro", layout="wide")

# Chargement des fichiers
with open('bible_data.json', 'r', encoding='utf-8') as f:
    bible_data = json.load(f)

# On essaie de charger le dictionnaire s'il existe
try:
    with open('dictionnaire.json', 'r', encoding='utf-8') as f:
        dict_data = json.load(f)
except:
    dict_data = {}

st.title("📖 Bible Interlinéaire & Dictionnaire")

verset_key = st.sidebar.selectbox("Choisir un verset", list(bible_data.keys()))
data = bible_data[verset_key]

# Affichage Interlinéaire
st.write("### Analyse du texte original")
cols = st.columns(len(data["hebrew"]))

for i, col in enumerate(cols):
    strong_code = data["strongs"][i]
    with col:
        st.subheader(data["hebrew"][i])
        
        # Bouton Dictionnaire
        if strong_code in dict_data:
            with st.popover(strong_code):
                st.write(f"**Mot:** {dict_data[strong_code]['mot']}")
                st.write(f"**Définition:** {dict_data[strong_code]['definition']}")
                st.caption(f"Origine: {dict_data[strong_code]['origine']}")
        else:
            st.caption(strong_code)

st.divider()
st.write(f"**Français:** {data['french']}")
st.write(f"**Malagasy:** {data['malagasy']}")
