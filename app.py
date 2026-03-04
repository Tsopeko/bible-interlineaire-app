import streamlit as st
import json

st.set_page_config(page_title="Étude Hébreu-Malagasy", layout="wide")

# Chargement des fichiers
@st.cache_data
def load_data():
    with open('Bible_MG65.json', 'r', encoding='utf-8') as f:
        mg_bible = json.load(f)
    try:
        # On charge ton nouveau fichier hébreu
        with open('strongs_hebrew_dictionary.json', 'r', encoding='utf-8') as f:
            he_dict = json.load(f)
    except:
        he_dict = {}
    return mg_bible, he_dict

bible_data, dictionnaire_he = load_data()

st.title("📖 Étude Interlinéaire Malagasy 1865")

# Navigation
livres = [b['name'] for b in bible_data['books']]
livre_nom = st.sidebar.selectbox("Boky", livres)
donnees_livre = next(b for b in bible_data['books'] if b['name'] == livre_nom)

chapitres = [c['chapter'] for c in donnees_livre['chapters']]
chap_num = st.sidebar.selectbox("Toko", chapitres)
donnees_chapitre = next(c for c in donnees_livre['chapters'] if c['chapter'] == chap_num)

# Mode Étude
mode_etude = st.sidebar.toggle("Hizaha ny teny fototra (Hebraio)")

for v in donnees_chapitre['verses']:
    st.write(f"**{v['verse']}.** {v['text']}")
    
    if mode_etude:
        with st.expander(f"Fandalinana andininy {v['verse']}"):
            # Ici on affiche une simulation du lien avec ton dictionnaire
            st.write("---")
            st.subheader("Teny fototra hita:")
            # Exemple : si on trouve le code H7225 dans le dictionnaire
            if "H7225" in dictionnaire_he:
                st.info(f"**H7225**: {dictionnaire_he['H7225'].get('lemma', 're-shith')}")
                st.write(f"Heviny: {dictionnaire_he['H7225'].get('xlit', 'Commencement')}")
