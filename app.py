import streamlit as st
import json

# ... (garder le début de ton code actuel pour le chargement des fichiers)

st.sidebar.divider()
mode = st.sidebar.radio("Hetsika (Action)", ["Hamaky (Lire)", "Hikaroka (Chercher)"])

if mode == "Hikaroka (Chercher)":
    st.subheader("🔍 Hikaroka teny ao amin'ny Baiboly")
    query = st.text_input("Soraty ny teny hokarohina...")
    
    if query:
        st.write(f"Vokatry ny fikarohana ho an'ny: **{query}**")
        for book in bible_data['books']:
            for chapter in book['chapters']:
                for verse in chapter['verses']:
                    if query.lower() in verse['text'].lower():
                        st.markdown(f"**{book['name']} {chapter['chapter']}:{verse['verse']}**")
                        st.write(verse['text'])
                        st.divider()
