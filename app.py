import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Interlineaire", layout="wide")

# 1. Fandaminana ny lalana (Paths)
DATA_PATH = "data"

@st.cache_data
def load_json(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

st.title("📖 Baiboly Malagasy Interlineaire")

# 2. Fitadiavana ny rakitra JSON
if os.path.exists(DATA_PATH):
    files = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
    if files:
        selected_file = st.sidebar.selectbox("Fidio ny Baiboly", files)
        bible_data = load_json(os.path.join(DATA_PATH, selected_file))
        
        if bible_data:
            # --- ETO ILAY AMPAHANY SQL-TO-JSON ---
            if isinstance(bible_data, dict) and 'objects' in bible_data:
                st.info(f"Mampiasa format SQL: {selected_file}")
                
                # Mitady ny andininy ao anaty 'rows'
                for obj in bible_data['objects']:
                    if obj.get('name') == 'verses' and 'rows' in obj:
                        st.subheader("Andininy rehetra")
                        for row in obj['rows']:
                            # Row format matetika: [id, book_id, chapter, verse, text]
                            # index 3 = verse, index 4 = text
                            if len(row) > 4:
                                v_num = str(row[3])
                                txt = str(row[4])
                                st.write(f"**{v_num}.** {txt}")
                                
                                # Bokotra Strong
                                strongs = re.findall(r'[GH]\d+', txt)
                                if strongs:
                                    cols = st.columns(len(strongs))
                                    for i, code in enumerate(strongs):
                                        if cols[i].button(f"🔍 {code}", key=f"{v_num}_{code}"):
                                            dict_f = "strongs-greek-dictionary.json" if code.startswith('G') else "strongs-hebrew-dictionary.json"
                                            s_data = load_json(dict_f)
                                            if s_data and code in s_data:
                                                st.success(f"**{code}:** {s_data[code]}")
            
            # --- RAHA FORMAT TSOTRA (Mg1865.json) ---
            else:
                books = sorted(list(bible_data.keys()))
                book = st.sidebar.selectbox("Boky", books)
                chapters = bible_data[book]
                ch = st.sidebar.selectbox("Toko", sorted(list(chapters.keys()), key=int))
                
                st.subheader(f"{book} - Toko {ch}")
                verses = chapters[ch]
                for v_num in sorted(verses.keys(), key=int):
                    txt = verses[v_num]
                    st.write(f"**{v_num}.** {txt}")
    else:
        st.error("Tsy misy rakitra .json ao anaty dossier 'data'")
else:
    st.warning("Ataovy azo antoka fa misy dossier 'data' ao amin'ny GitHub")
