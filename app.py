import streamlit as st
import json
import os
import re

# 1. Fikirana fototra ny pejy
st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide", page_icon="📖")

# Dossier misy ny boky Baiboly
DATA_PATH = "data"

# Fonction hikarakarana ny famakiana JSON (fisorohana ny Extra Data)
def load_any_json(filename):
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # Raha misy JSON maromaro mifanesy (fix ho an'ny Extra Data)
            if content.count('{') > 1:
                # Mitady ny {} voalohany fotsiny
                match = re.search(r'(\{.*?\})(?=\s*\{|$)', content, re.DOTALL)
                if match:
                    return json.loads(match.group(1))
            return json.loads(content)
    except Exception:
        return None

st.title("📖 Baiboly Malagasy 1865")

# --- SIDEBAR (Sisiny) ---
st.sidebar.header("⚙️ Fikirana")
st.sidebar.info("Miasa ny fikarohana, ny famakiana, ary ny Strong.")

# --- DICTIONNAIRE STRONG ---
st.sidebar.divider()
st.sidebar.header("📚 Diksionera Strong")
strong_input = st.sidebar.text_input("Hampidiro ny code (ohatra: G2424 na H7225)")

if strong_input:
    code = strong_input.upper().strip()
    # Mamaritra ny fichier ho vakiana
    dict_file = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
    
    strong_data = load_any_json(dict_file)
    
    if strong_data and code in strong_data:
        info = strong_data[code]
        st.markdown("---")
        st.header(f"🔍 Diksionera: {code}")
        
        if isinstance(info, dict):
            # Mampiseho ny antsipiriany rehetra hita ao anaty JSON
            for k, v in info.items():
                st.write(f"**{k.capitalize()}:** {v}")
        else:
            st.write(str(info))
    else:
        st.sidebar.error(f"Tsy hita ny code {code} na ny fichier {dict_file}")

st.sidebar.divider()

# --- MOTEUR DE RECHERCHE ---
st.sidebar.header("🔍 Karoka Baiboly")
mot_cle = st.sidebar.text_input("Teny hotadiavina")

if mot_cle:
    st.header(f"Valin'ny karoka: '{mot_cle}'")
    if st.button("Hiverina hamaky"):
        st.rerun()
        
    found_count = 0
    if os.path.exists(DATA_PATH):
        books = sorted([f for f in os.listdir(DATA_PATH) if f.endswith('.json')])
        for b_file in books:
            b_name = b_file.replace('.json', '')
            b_data = load_any_json(f"{DATA_PATH}/{b_file}")
            if b_data:
                for chap, versets in b_data.items():
                    if isinstance(versets, dict):
                        for v_num, txt in versets.items():
                            if mot_cle.lower() in txt.lower():
                                st.write(f"**{b_name} {chap}:{v_num}**")
                                st.write(txt)
                                st.divider()
                                found_count += 1
    st.sidebar.info(f"Verset {found_count} no hita.")
    st.stop()

# --- LECTURE NORMALE ---
if os.path.exists(DATA_PATH):
    files = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')])
    if files:
        livre = st.sidebar.selectbox("Fidio ny boky", files)
        data = load_any_json(f"{DATA_PATH}/{livre}.json")
        if data:
            toko_list = sorted([k for k in data.keys() if k.isdigit()], key=int)
            if toko_list:
                toko_choisi = st.sidebar.selectbox("Toko", toko_list)
                st.subheader(f"{livre} - Toko {toko_choisi}")
                
                versets = data[toko_choisi]
                v_list = sorted([v for v in versets.keys() if v.isdigit()], key=int)
                for v_num in v_list:
                    st.write(f"**{v_num}.** {versets[v_num]}")
