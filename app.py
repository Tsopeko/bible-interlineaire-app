import streamlit as st
import json

st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide")

def load_data(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

bible_data = load_data('Bible_MG65.json')

st.title("📖 Baiboly Malagasy 1865")

if bible_data is None:
    st.error("Tsy hita ny fichier 'Bible_MG65.json'.")
    st.stop()

# --- RECHERCHE DES LIVRES ---
# Si le fichier commence par "database", on entre dedans
if isinstance(bible_data, dict) and 'database' in bible_data:
    base = bible_data['database']
    # On cherche les livres à l'intérieur
    livres_list = base.get('books', base if isinstance(base, list) else [])
else:
    livres_list = bible_data.get('books', bible_data if isinstance(bible_data, list) else [])

# --- NAVIGATION ---
try:
    if not livres_list:
        st.warning("Fichier vide ou mal lu.")
        st.json(bible_data) # Pour voir la structure si ça rate
        st.stop()

    noms_livres = [b.get('name', f"Boky {i+1}") for i, b in enumerate(livres_list)]
    livre_nom = st.sidebar.selectbox("Fidio ny boky", noms_livres)
    
    idx_livre = noms_livres.index(livre_nom)
    data_livre = livres_list[idx_livre]

    # Sélection du Chapitre
    chaps = data_livre.get('chapters', [])
    if chaps:
        chap_list = [str(c.get('chapter', i+1)) for i, c in enumerate(chaps)]
        chap_num = st.sidebar.selectbox("Toko", chap_list)
        
        idx_chap = chap_list.index(chap_num)
        versets = chaps[idx_chap].get('verses', [])

        st.header(f"{livre_nom} - Toko {chap_num}")
        for v in versets:
            st.write(f"**{v.get('verse', '')}.** {v.get('text', '')}")
    else:
        st.info("Tsy misy toko hita ato.")

except Exception as e:
    st.error(f"Olana : {e}")
