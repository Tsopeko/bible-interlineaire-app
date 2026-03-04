import streamlit as st
import json
import os

st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide", page_icon="📖")

DATA_PATH = "data"

@st.cache_data
def load_book(name):
    try:
        with open(f"{DATA_PATH}/{name}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

st.title("📖 Baiboly Malagasy 1865")

# --- PARAMÈTRES D'AFFICHAGE ---
st.sidebar.header("⚙️ Fikirana")
st.sidebar.info("Miasa ny fikarohana sy ny famakiana.")
st.sidebar.divider()

# --- DIKSIONERA STRONG (ETO NO NAMPIDIRANA AZY) ---
st.sidebar.header("📚 Diksionera Strong")
strong_code = st.sidebar.text_input("Hampidiro ny code (ohatra: G2424 na H7225)")

if strong_code:
    code_upper = strong_code.upper().strip()
    is_greek = code_upper.startswith('G')
    filename = "strongs-greek-dictionary.json" if is_greek else "strongs-hebrew-dictionary.json"
    
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                strong_data = json.load(f)
            
            if code_upper in strong_data:
                info = strong_data[code_upper]
                st.sidebar.success(f"Hita ny code {code_upper}")
                
                st.write(f"### 📚 Diksionera: {code_upper}")
                if isinstance(info, dict):
                    # Ampiasaina ny 'lemma' na 'word' na 'xlit' arakaraka ny JSON
                    lemma = info.get('lemma', info.get('word', '---'))
                    def_text = info.get('definition', info.get('strongs_def', '---'))
                    st.write(f"**Teny fototra:** {lemma}")
                    st.write(f"**Dikany:** {def_text}")
                else:
                    st.write(info)
                st.divider() # Manisy tsipika manasaraka amin'ny Baiboly
            else:
                st.sidebar.error(f"Tsy hita ny {code_upper}")
        except Exception as e:
            st.sidebar.error(f"Nisy olana: {e}")
    else:
        st.sidebar.warning(f"Tsy hita ny fichier {filename}")

# --- MOTEUR DE RECHERCHE (BAIBOLY) ---
st.sidebar.divider()
st.sidebar.header("🔍 Karoka Baiboly")
mot_cle = st.sidebar.text_input("Hikaroka teny (Baiboly)")

if mot_cle:
    st.header(f"Valin'ny karoka: '{mot_cle}'")
    if st.button("Hiverina hamaky"):
        st.rerun()
    # ... (tohiny ny kaody teo aloha)
