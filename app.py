import streamlit as st
import json
import os

# Fikirana fototra
st.set_page_config(page_title="Baiboly Interlineaire", layout="wide")

DATA_PATH = "data"

@st.cache_data
def load_json(path):
    if not os.path.exists(path): return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return None

st.title("📖 Baiboly Interlineaire Malagasy")

# --- FAMAKIANA SY INTERLINEAIRE ---
if os.path.exists(DATA_PATH):
    books = sorted([f.replace('.json', '') for f in os.listdir(DATA_PATH) if f.endswith('.json')])
    if books:
        livre = st.sidebar.selectbox("Fidio ny boky", books)
        data = load_json(f"{DATA_PATH}/{livre}.json")
        
        if data:
            # Mandamina ny toko (isdigit check mba hisorohana ny ValueError)
            t_list = sorted([k for k in data.keys() if str(k).isdigit()], key=int)
            if t_list:
                t_sel = st.sidebar.selectbox("Toko", t_list)
                st.header(f"{livre} - Toko {t_sel}")
                
                v_dict = data[t_sel]
                v_list = sorted([v for v in v_dict.keys() if str(v).isdigit()], key=int)
                
                for n in v_list:
                    st.write(f"**{n}.** {v_dict[n]}")
                    
                    # Eto no misy ny "Interlineaire": mampiseho diksionera raha misy code Strong
                    # Ity dia fikarohana mandeha ho azy raha misy code ao anaty andininy
                    import re
                    strong_codes = re.findall(r'[GH]\d+', v_dict[n])
                    if strong_codes:
                        cols = st.columns(len(strong_codes))
                        for i, code in enumerate(strong_codes):
                            with cols[i]:
                                if st.button(f"Hizaha {code}", key=f"{n}_{code}"):
                                    # Mitady ny diksiona
                                    fn = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
                                    s_data = load_json(fn)
                                    if s_data and code in s_data:
                                        st.info(f"**{code}:** {s_data[code]}")

# --- DIKSIONERA AO AMIN'NY SIDEBAR ---
st.sidebar.divider()
st.sidebar.header("📚 Karoka Strong mivantana")
manual_code = st.sidebar.text_input("Hampidiro ny code (G... na H...)")
if manual_code:
    code = manual_code.upper().strip()
    fn = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
    s_data = load_json(fn)
    if s_data and code in s_data:
        st.sidebar.success(f"{code}: {s_data[code]}")
    else:
        st.sidebar.error("Tsy hita")
