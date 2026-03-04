import streamlit as st
import json

st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide")

def load_data(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

# Chargement du fichier
bible_data = load_data('Bible_MG65.json')

st.title("📖 Baiboly Malagasy 1865")

if bible_data is None:
    st.error("Tsy hita ny fichier 'Bible_MG65.json' ao amin'ny GitHub.")
    st.stop()

# --- DÉTECTION AUTOMATIQUE DE LA STRUCTURE ---
liste_livres_data = []

# Si c'est un dictionnaire, on cherche 'books' ou on prend les valeurs
if isinstance(bible_data, dict):
    if 'books' in bible_data:
        liste_livres_data = bible_data['books']
    else:
        # On essaie de voir si les livres sont directement les clés
        liste_livres_data = list(bible_data.values())
# Si c'est déjà une liste
elif isinstance(bible_data, list):
    liste_livres_data = bible_data

if not liste_livres_data or not isinstance(liste_livres_data, list):
    st.error("Tsy fantatra ny firafitry ny JSON. Hamarino ny fichier-nao.")
    st.stop()

# --- NAVIGATION ---
try:
    # On récupère les noms (on gère 'name' ou 'label')
    noms_livres = [b.get('name', b.get('label', f"Boky {i+1}")) for i, b in enumerate(liste_livres_data)]
    livre_nom = st.sidebar.selectbox("Fidio ny boky", noms_livres)
    
    # On récupère le livre choisi
    idx = noms_livres.index(livre_nom)
    donnees_livre = liste_livres_data[idx]
    
    # On cherche les chapitres
    chapitres_list = donnees_livre.get('chapters', [])
    noms_chapitres = [str(c.get('chapter', i+1)) for i, c in enumerate(chapitres_list)]
    chap_num = st.sidebar.selectbox("Toko", noms_chapitres)
    
    # On récupère le chapitre choisi
    c_idx = noms_chapitres.index(chap_num)
    donnees_chapitre = chapitres_list[c_idx]

    # --- AFFICHAGE ---
    st.header(f"{livre_nom} - Toko {chap_num}")
    st.divider()
    
    for v in donnees_chapitre.get('verses', []):
        num = v.get('verse', '?')
        txt = v.get('text', '')
        st.write(f"**{num}.** {txt}")

except Exception as e:
    st.warning(f"Nisy olana kely: {e}")
