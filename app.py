import streamlit as st
import json

st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide")

def load_data(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

# Chargement du fichier principal
bible_data = load_data('Bible_MG65.json')

st.title("📖 Baiboly Malagasy 1865")

if bible_data is None:
    st.error("Tsy hita ny fichier 'Bible_MG65.json'. Hamarino ny anarany ao amin'ny GitHub.")
    st.stop()

# --- ANALYSE DE LA STRUCTURE ---
# On cherche où sont les livres dans ton fichier
livres_list = []
if isinstance(bible_data, dict):
    livres_list = bible_data.get('books', list(bible_data.values()) if not 'books' in bible_data else [])
elif isinstance(bible_data, list):
    livres_list = bible_data

# --- AFFICHAGE DE SÉCURITÉ ---
if not livres_list:
    st.warning("Fichier vide ou structure inconnue.")
    st.json(bible_data) # Ceci nous aidera à voir ce qu'il y a dedans
    st.stop()

# --- NAVIGATION ---
try:
    # On extrait les noms des livres proprement
    noms_livres = []
    for b in livres_list:
        if isinstance(b, dict):
            noms_livres.append(b.get('name', b.get('label', 'Boky')))
        else:
            noms_livres.append(str(b))

    livre_nom = st.sidebar.selectbox("Fidio ny boky", noms_livres)
    idx_livre = noms_livres.index(livre_nom)
    data_livre = livres_list[idx_livre]

    if isinstance(data_livre, dict) and 'chapters' in data_livre:
        chaps = data_livre['chapters']
        chap_num = st.sidebar.selectbox("Toko", [c.get('chapter', i+1) for i, c in enumerate(chaps)])
        
        # Affichage des versets
        st.header(f"{livre_nom} - Toko {chap_num}")
        current_chap = next(c for c in chaps if c.get('chapter') == chap_num)
        for v in current_chap.get('verses', []):
            st.write(f"**{v.get('verse', '')}.** {v.get('text', '')}")
    else:
        st.info(f"Mampiseho ny votoatin'ny {livre_nom}:")
        st.write(data_livre)

except Exception as e:
    st.error(f"Olana : {e}")
