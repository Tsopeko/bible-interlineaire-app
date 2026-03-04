import streamlit as st
import json
import os
import re

# 1. Fikirana fototra
st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide", page_icon="📖")

DATA_PATH = "data"

# Fonction manokana hamakiana ny JSON (miady amin'ny "Extra Data")
def load_json_safe(filename):
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # Raha toa ka misy JSON maromaro mifanesy ao anaty fichier iray
            if content.startswith('{') and content.count('}{') > 0:
                # Maka ny {} voalohany fotsiny amin'ny alalan'ny Regex
                match = re.search(r'(\{.*?\})(?=\s*\{|$)', content, re.DOTALL)
                if match:
                    return json.loads(match.group(1))
            return json.loads(content)
    except Exception:
        return None

st.title("📖 Baiboly Malagasy 1865")

# --- SIDEBAR: FIKIRANA ---
st.sidebar.header("⚙️ Fikirana")
st.sidebar.success("Miasa ny fikarohana, ny famakiana, ary ny Strong.")

# --- DICTIONNAIRE STRONG ---
st.sidebar.divider()
st.sidebar.header("📚 Diksionera Strong")
strong_input = st.sidebar.text_input("Hampidiro ny code (ohatra: G2424 na H7225)")

if strong_input:
    code = strong_input.upper().strip()
    # Fidio ny fichier araka ny litera voalohany
    dict_filename = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
    
    strong_data = load_json_safe(dict_filename)
    
    if strong_data and code in strong_data:
        info = strong_data[code]
        st.markdown("---")
        st.header(f"🔍 Diksionera: {code}")
        
        # Fampisehoana ny antsipiriany rehetra hita ao anaty JSON
        if isinstance(info, dict):
            for k, v in info.items():
                st.write(f"**{k.capitalize()}:** {v}")
        else:
            st.write(str(info))
    else:
        st.sidebar.error(f"Tsy hita ny code {code} ato amin'ny {dict_filename}")

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
        files = sorted([f for f in os.listdir(DATA_PATH) if f.endswith('.json')])
        for f_name in files:
            b_name = f_name.replace('.json', '')
            b_data = load_json_safe(f"{DATA_PATH}/{f_name}")
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
    books = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')])
    if books:
        livre_choisi = st.sidebar.selectbox("Fidio ny boky", books)
        data = load_json_safe(f"{DATA_PATH}/{livre_choisi}.json")
        if data:
            toko_keys = sorted([k for k in data.keys() if k.isdigit()], key=int)
            if toko_keys:
                chap_num = st.sidebar.selectbox("Toko", toko_keys)
                st.subheader(f"{livre_choisi} - Toko {chap_num}")
                
                versets_dict = data[chap_num]
                v_keys = sorted([v for v in versets_dict.keys() if v.isdigit()], key=int)
                for v_num in v_keys:
                    st.write(f"**{v_num}.** {versets_dict[v_num]}")
