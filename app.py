import streamlit as st
import json

st.set_page_config(page_title="Baiboly 1865", layout="wide")

def load_data(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

# Chargement
bible_data = load_data('Bible_MG65.json')

st.title("📖 Baiboly Malagasy 1865")

if bible_data is None:
    st.error("Tsy hita ny fichier 'Bible_MG65.json'. Hamarino ny anarany ao amin'ny GitHub.")
    st.stop()

# --- REPARATION DE L'ERREUR 'BOOKS' ---
# On essaie plusieurs structures possibles pour trouver les livres
if 'books' in bible_data:
    liste_livres_data = bible_data['books']
elif isinstance(bible_data, list):
    liste_livres_data = bible_data
else:
    # Si le fichier est structuré autrement (ex: directement par noms de livres)
    liste_livres_data = bible_data.get('content', [])

if not liste_livres_data:
    st.error("Tsy nety ny firafitry ny fichier JSON. Hamarino ny loharano.")
    st.stop()

# --- NAVIGATION ---
try:
    noms_livres = [b['name'] for b in liste_livres_data]
    livre_nom = st.sidebar.selectbox("Fidio ny boky", noms_livres)
    
    donnees_livre = next(b for b in liste_livres_data if b['name'] == livre_nom)
    
    chapitres = [c['chapter'] for c in donnees_livre['chapters']]
    chap_num = st.sidebar.selectbox("Toko", chapitres)
    
    donnees_chapitre = next(c for c in donnees_livre['chapters'] if c['chapter'] == chap_num)

    # --- AFFICHAGE ---
    st.header(f"{livre_nom} - Toko {chap_num}")
    for v in donnees_chapitre['verses']:
        st.write(f"**{v['verse']}.** {v['text']}")

except Exception as e:
    st.warning(f"Olana kely teo am-pamakiana: {e}")
    st.info("Andramo jerena raha mifanaraka amin'ny dikan-teny 1865 ny fichier-nao.")
