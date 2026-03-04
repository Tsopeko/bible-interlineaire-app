import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Bible Interlinéaire Multi", layout="wide")

# Simulation d'une base de données de versets
# Dans un projet réel, vous chargeriez ceci depuis un fichier JSON ou SQL
bible_data = {
    "Genèse 1:1": {
        "hebrew": ["בְּרֵאשִׁית", "בָּרָא", "אֱלֹהִים", "אֵת", "הַשָּׁמַיִם", "וְאֵת", "הָאָרֶץ"],
        "strongs": ["H7225", "H1254", "H430", "H853", "H8064", "H853", "H776"],
        "french": "Au commencement, Dieu créa les cieux et la terre.",
        "english": "In the beginning, God created the heavens and the earth.",
        "malagasy": "Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany."
    }
}

st.title("📖 Application Biblique Interlinéaire")

# Barre latérale pour la navigation
st.sidebar.header("Navigation")
livre = st.sidebar.selectbox("Livre", ["Genèse", "Exode"])
verset_key = "Genèse 1:1" # Simplifié pour l'exemple

st.subheader(f"Traduction : {verset_key}")

# Affichage Interlinéaire (Hébreu + Strongs)
st.write("### Texte Source (Hébreu & Strongs)")
cols = st.columns(len(bible_data[verset_key]["hebrew"]))

# L'Hébreu se lit de droite à gauche (RTL)
words = bible_data[verset_key]["hebrew"]
strongs = bible_data[verset_key]["strongs"]

for i, col in enumerate(cols):
    with col:
        st.markdown(f"**{words[i]}**")
        if st.button(strongs[i], key=f"btn_{i}"):
            st.info(f"Dictionnaire : Définition pour {strongs[i]}")

st.divider()

# Affichage des versions
st.write("### Traductions")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Français**\n\n" + bible_data[verset_key]["french"])
with col2:
    st.success("**English**\n\n" + bible_data[verset_key]["english"])
with col3:
    st.warning("**Malagasy (1865)**\n\n" + bible_data[verset_key]["malagasy"])
