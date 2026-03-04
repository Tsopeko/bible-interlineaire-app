import streamlit as st
import json
import os
import re

st.set_page_config(page_title="Baiboly Mg1865", layout="wide")

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

st.title("📖 Baiboly Mg1865 Interlineaire")

# 1. Load Bible
data = load_json("data/Mg1865.json")

if data and "objects" in data:
    # Araka ny sary 5db10129, ny angon-drakitra dia ao amin'ny objects -> rows
    try:
        # Mitady ny table misy ny Baiboly (matetika ilay misy andininy)
        # Ity dia maka ny 'rows' avy amin'ny table voalohany ao amin'ny 'objects'
        bible_rows = data["objects"][0]["rows"] 
        
        # Alahatra ny boky misy
        # Ny 'row' tsirairay dia misy [book_number, chapter, verse, text] na mitovitovy amin'izany
        # Mila fantarina ny anaran'ny boky avy amin'ny 'book_number'
        
        st.success("Tafiditra ny rakitra 8.46 MB!")
        st.write("Fanamarihana: Ny rakitrao dia 'Database Export'.")
        
        # Ity ampahany ity dia mampiseho ny andalana 10 voalohany mba hahitantsika ny firafitry ny andininy
        st.write("Ireo andalana vitsy voalohany ao amin'ny rows:")
        st.json(bible_rows[:3]) 
        
        st.info("Rehefa hitantsika ny anaran'ny 'columns' (ohatra: 'text' na 'content'), dia hamboarintsika ny fampisehoana azy.")
        
    except Exception as e:
        st.error(f"Tsy mifanaraka ny rafitra: {e}")
else:
    st.warning("Tsy hita ny rakitra na diso ny format JSON.")
