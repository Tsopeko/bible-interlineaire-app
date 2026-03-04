import streamlit as st
import json
import os
import random

# 1. Fikirana fototra
st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide", page_icon="📖")

DATA_PATH = "data"

@st.cache_data
def load_json(path):
    if not os.path.exists(path): return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return None

# --- LOhateny sy sary ---
st.title("📖 Baiboly Malagasy 1865")

# --- ANDININY HO AN'NY ANIO (Kisendrasendra) ---
if os.path.exists(DATA_PATH):
    books = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    if books:
        random_b = random.choice(books)
        b_data = load_json(f"{DATA_PATH}/{random_b}")
        if b_data:
            toko_r = random.choice(list(b_data.keys()))
            v_num_r = random.choice(list(b_data[toko_r].keys()))
            st.info(f"✨ **Andininy kisendrasendra:** {b_data[toko_r][v_num_r]} ({random_b[:-5]} {toko_r}:{v_num_r})")

# --- SIDEBAR: DIKSIONERA STRONG ---
st.sidebar.header("📚 Diksionera Strong")
strong_in = st.sidebar.text_input("Code (ohatra: G2424 na H7225)")

if strong_in:
    s_code = strong_in.upper().strip()
    # Hamarino ny anaran'ny fichier ao amin'ny GitHub-nao
    s_file = "strongs-greek-dictionary.json" if s_code.startswith('G') else "strongs-hebrew-dictionary.json"
    s_data = load_json(s_file)
    
    if s_data:
        # Fikarohana na dia ao anaty lisitra aza ilay code
        resultat = None
        if isinstance(s_data, dict):
            resultat = s_data.get(s_code)
        elif isinstance(s_data, list):
            resultat = next((item for item in s_data if item.get('strongs') == s_code or item.get('number') == s_code[1:]), None)
            
        if resultat:
            st.success(f"🔍 Valiny ho an'ny {s_code}")
            st.write(resultat)
        else:
            st.sidebar.error(f"Tsy hita ny '{s_code}' ato anaty fichier.")
    else:
        st.sidebar.warning(f"Tsy hita ny fichier {s_file}")

st.sidebar.divider()

# --- KAROKA BAIBOLY ---
st.sidebar.header("🔍 Karoka")
mot = st.sidebar.text_input("Teny hotadiavina")
if mot:
    st.subheader(f"Valin'ny karoka: '{mot}'")
    if st.button("Hiverina"): st.rerun()
    if os.path.exists(DATA_PATH):
        for f in sorted(os.listdir(DATA_PATH)):
            bd = load_json(f"{DATA_PATH}/{f}")
            if bd:
                for t, vs in bd.items():
                    for n, txt in vs.items():
                        if mot.lower() in txt.lower():
                            st.write(f"**{f[:-5]} {t}:{n}** - {txt}")
                            st.divider()
    st.stop()

# --- FAMAKIANA ---
if os.path.exists(DATA_PATH):
    all_b = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH)])
    b_sel = st.sidebar.selectbox("Boky", all_b)
    data = load_json(f"{DATA_PATH}/{b_sel}.json")
    if data:
        t_list = sorted(data.keys(), key=int)
        t_sel = st.sidebar.selectbox("Toko", t_list)
        st.header(f"{b_sel} - Toko {t_sel}")
        for n in sorted(data[t_sel].keys(), key=int):
            st.write(f"**{n}.** {data[t_sel][n]}")
