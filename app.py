import streamlit as st
import json
import os
import re

# 1. Fikirana fototra
st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide", page_icon="📖")

DATA_PATH = "data"

# Fonction matanjaka hamakiana JSON
def load_json_universal(filename):
    # Mitady ny fichier na dia misy litera lehibe/kely aza ny anarany
    target = filename.lower()
    actual_file = None
    for f in os.listdir('.'):
        if f.lower() == target:
            actual_file = f
            break
    
    if not actual_file or not os.path.exists(actual_file):
        return None
        
    try:
        with open(actual_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # Fisorohana ny "Extra Data" (Error tamin'ny sary f8f51790)
            if content.count('{') > 1:
                match = re.search(r'(\{.*?\})(?=\s*\{|$)', content, re.DOTALL)
                if match:
                    return json.loads(match.group(1))
            return json.loads(content)
    except:
        return None

st.title("📖 Baiboly Malagasy 1865")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Fikirana")
st.sidebar.success("Miasa ny fikarohana, ny famakiana, ary ny Strong.")

# --- DICTIONNAIRE STRONG ---
st.sidebar.divider()
st.sidebar.header("📚 Diksionera Strong")
strong_input = st.sidebar.text_input("Hampidiro ny code (ohatra: G2424 na H7225)")

if strong_input:
    code = strong_input.upper().strip()
    # Mifidy ny anaran'ny fichier (na dia misy fahasamihafana kely aza ny anarany)
    fn = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
    
    strong_data = load_json_universal(fn)
    
    if strong_data and code in strong_data:
        info = strong_data[code]
        st.markdown("---")
        st.header(f"🔍 Diksionera: {code}")
        if isinstance(info, dict):
            for k, v in info.items():
                st.write(f"**{k.upper()}:** {v}")
        else:
            st.write(str(info))
    else:
        st.sidebar.warning(f"Tsy hita ny '{code}'. Hamarino raha marina ny code na ny fichier.")

st.sidebar.divider()

# --- MOTEUR DE RECHERCHE ---
st.sidebar.header("🔍 Karoka Baiboly")
mot_cle = st.sidebar.text_input("Teny hotadiavina")

if mot_cle:
    st.header(f"Valin'ny karoka: '{mot_cle}'")
    if st.button("Hiverina hamaky"): st.rerun()
    found = 0
    if os.path.exists(DATA_PATH):
        for f_name in sorted(os.listdir(DATA_PATH)):
            if f_name.endswith('.json'):
                b_data = load_json_universal(f"{DATA_PATH}/{f_name}")
                if b_data:
                    for ch, versets in b_data.items():
                        if isinstance(versets, dict):
                            for v_num, txt in versets.items():
                                if mot_cle.lower() in txt.lower():
                                    st.write(f"**{f_name[:-5]} {ch}:{v_num}**")
                                    st.write(txt)
                                    st.divider()
                                    found += 1
    st.sidebar.info(f"Verset {found} no hita.")
    if found > 0: st.stop()

# --- LECTURE NORMALE ---
if os.path.exists(DATA_PATH):
    books = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')])
    if books:
        livre = st.sidebar.selectbox("Fidio ny boky", books)
        data = load_json_universal(f"{DATA_PATH}/{livre}.json")
        if data:
            toko_keys = sorted([k for k in data.keys() if k.isdigit()], key=int)
            if toko_keys:
                ch_num = st.sidebar.selectbox("Toko", toko_keys)
                st.subheader(f"{livre} - Toko {ch_num}")
                v_dict = data[ch_num]
                for v_num in sorted([v for v in v_dict.keys() if v.isdigit()], key=int):
                    st.write(f"**{v_num}.** {v_dict[v_num]}")
