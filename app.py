import streamlit as st
import json

st.set_page_config(page_title="Ma Bible Interlinéaire", layout="wide")

# Charger les données depuis le fichier JSON
with open('bible_data.json', 'r', encoding='utf-8') as f:
    bible_data = json.load(f)

st.title("📖 Ma Bible Interlinéaire")

# Sélection du verset
verset_key = st.sidebar.selectbox("Choisir un verset", list(bible_data.keys()))

data = bible_data[verset_key]

st.subheader(f"Texte : {verset_key}")

# Affichage Interlinéaire
cols = st.columns(len(data["hebrew"]))
for i, col in enumerate(cols):
    with col:
        st.markdown(f"### {data['hebrew'][i]}")
        st.caption(data['strongs'][i])

st.divider()

# Affichage des langues
st.write(f"**Français:** {data['french']}")
st.write(f"**English:** {data['english']}")
st.write(f"**Malagasy (1865):** {data['malagasy']}")
