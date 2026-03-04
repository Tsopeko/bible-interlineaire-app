import streamlit as st
import json
import os
import re

# 1. Fikirana fototra
st.set_page_config(page_title="Baiboly Malagasy 1865", layout="wide", page_icon="📖")

DATA_PATH = "data"

@st.cache_data
def load_json_file(filename):
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # Raha misy JSON maromaro mifanesy (Extra data error fix)
            if content.startswith('{') and content.count('}{') > 0:
                # Maka ny {} voalohany fotsiny
                first_obj = re.search(r'(\{.*?\})(?=\s*\{|$)', content, re.DOTALL)
                if first_obj:
                    return json.loads(first_obj.group(1))
            return json.loads(content)
    except Exception as e:
        return None

st.title("📖 Baiboly Malagasy 1865")

# --- SIDEBAR: FIKIRANA SY DIKSIONERA ---
st.sidebar.header("⚙️ Fikirana")
st.sidebar.info("Miasa ny fikarohana sy ny famakiana.")

# --- DICTIONNAIRE STRONG ---
st.sidebar.divider()
st.sidebar.header("📚 Diksionera Strong")
strong_code = st.sidebar.text_input("Hampidiro ny code (ohatra: G2424 na H7225)")

if strong_code:
    code_upper = strong_code.upper().strip()
    is_greek = code_upper.startswith('G')
    dict_filename = "strongs-greek-dictionary.json" if is_greek else "strongs-hebrew-dictionary.json"
    
    strong_data = load_json_file(dict_filename)
    
    if strong_data and code_upper in strong_data:
        info = strong_data[code_upper]
        st.markdown("---")
        st.header(f"🔍 Strong {code_upper}")
        
        if isinstance(info, dict):
            # Mampiseho izay rehetra ao anaty JSON na inona na inona anarany
            for key, value in info.items():
                st.write(f"**{key.capitalize()}:** {value}")
        else:
            st.write(str(info))
    else:
        st.sidebar.error(f"Tsy hita ny code {code_upper} na ny fichier.")

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
        for file_name in files:
            book_name = file_name.replace('.json', '')
            book_data = load_json_file(f"{DATA_PATH}/{file_name}")
            if book_data:
                for chap_num, versets in book_data.items():
                    if isinstance(versets, dict):
                        for v_num, txt in versets.items():
                            if mot_cle.lower() in txt.lower():
                                st.write(f"**{book_name} {chap_num}:{v_num}**")
                                st.write(txt)
                                st.divider()
                                found_count += 1
    st.sidebar.info(f"Verset {found_count} no hita.")
    st.stop() 

# --- LECTURE NORMALE ---
if os.path.exists(DATA_PATH):
    files = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')])
    if files:
        livre_choisi = st.sidebar.selectbox("Fidio ny boky", files)
        data = load_json_file(f"{DATA_PATH}/{livre_choisi}.json")
        if data:
            toko_keys = sorted([k for k in data.keys() if k.isdigit()], key=int)
            if toko_keys:
                chap_num = st.sidebar.selectbox("Toko", toko_keys)
                st.subheader(f"{livre_choisi} - Toko {chap_num}")
                
                versets_dict = data[chap_num]
                v_keys = sorted([v for v in versets_dict.keys() if v.isdigit()], key=int)
                for v_num in v_keys:
                    st.write(f"**{v_num}.** {versets_dict[v_num]}")
