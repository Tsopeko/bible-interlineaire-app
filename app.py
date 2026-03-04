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

st.title("📖 Baiboly Malagasy 1865")

# --- ANDININY KISENDRASENDRA (Verse of the Day) ---
if os.path.exists(DATA_PATH):
    books_files = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    if books_files:
        try:
            r_book_file = random.choice(books_files)
            r_data = load_json(f"{DATA_PATH}/{r_book_file}")
            # Maka toko iray izay isa (isdigit)
            toko_keys = [k for k in r_data.keys() if k.isdigit()]
            if toko_keys:
                r_toko = random.choice(toko_keys)
                v_keys = list(r_data[r_toko].keys())
                r_v_num = random.choice(v_keys)
                st.info(f"✨ **Andininy kisendrasendra:** {r_data[r_toko][r_v_num]} ({r_book_file[:-5]} {r_toko}:{r_v_num})")
        except: pass

# --- SIDEBAR: DIKSIONERA STRONG ---
st.sidebar.header("📚 Diksionera Strong")
strong_in = st.sidebar.text_input("Code (ohatra: G2424 na H7225)")

if strong_in:
    s_code = strong_in.upper().strip()
    s_file = "strongs-greek-dictionary.json" if s_code.startswith('G') else "strongs-hebrew-dictionary.json"
    s_data = load_json(s_file)
    
    if s_data:
        # Fikarohana amin'ny fomba maro (dict na list)
        valiny = None
        if isinstance(s_data, dict):
            valiny = s_data.get(s_code)
        elif isinstance(s_data, list):
            # Mitady code ao anaty lisitra
            valiny = next((i for i in s_data if i.get('strongs') == s_code or i.get('number') == s_code[1:]), None)
            
        if valiny:
            st.success(f"🔍 Strong {s_code}")
            st.write(valiny)
        else:
            st.sidebar.error(f"Tsy hita ny '{s_code}' ato anaty fichier.")
    else:
        st.sidebar.warning(f"Tsy hita ny fichier {s_file}")

st.sidebar.divider()

# --- KAROKA ---
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
                    if isinstance(vs, dict):
                        for n, txt in vs.items():
                            if mot.lower() in txt.lower():
                                st.write(f"**{f[:-5]} {t}:{n}** - {txt}")
                                st.divider()
    st.stop()

# --- FAMAKIANA (LECTURE) ---
if os.path.exists(DATA_PATH):
    all_b = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH)])
    b_sel = st.sidebar.selectbox("Boky", all_b)
    data = load_json(f"{DATA_PATH}/{b_sel}.json")
    if data:
        # Fandaminana ny toko (asiana fiarovana amin'ny ValueError)
        try:
            t_list = sorted([k for k in data.keys() if k.isdigit()], key=int)
            t_sel = st.sidebar.selectbox("Toko", t_list)
            st.header(f"{b_sel} - Toko {t_sel}")
            v_dict = data[t_sel]
            v_num_list = sorted([v for v in v_dict.keys() if v.isdigit()], key=int)
            for n in v_num_list:
                st.write(f"**{n}.** {v_dict[n]}")
        except Exception as e:
            st.error(f"Nisy olana tamin'ny fandaminana ny toko: {e}")
