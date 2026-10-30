import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILE = "batiment_data.csv"

# ---------------------- Charger les données -----------------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Nom", "Type_batiment", "Etat_structure", "Commentaire"])

data = load_data()

st.title("🧱 Sondage : Évaluation d’un bâtiment")

# ----------------- FORMULAIRE : NOUVEAU COMMENTAIRE -----------------
st.subheader("➤ Donner votre avis")

nom = st.text_input("Votre nom")
type_bat = st.selectbox("Type de bâtiment", ["Maison", "Immeuble", "Bureau", "Entrepôt"])
etat = st.selectbox("État de la structure", ["Bon", "Moyen", "Mauvais"])
commentaire = st.text_area("Votre commentaire")

# Vérifier si la personne existe déjà dans le dataset
user_exists = nom in data["Nom"].values

if st.button("Soumettre"):
    if nom == "" or commentaire == "":
        st.error("❌ Aucun champ ne doit être vide !")
    else:
        if user_exists:
            st.warning("⚠ Vous avez déjà soumis un commentaire.")
        else:
            new_entry = pd.DataFrame([[nom, type_bat, etat, commentaire]],
                                     columns=data.columns)
            data = pd.concat([data, new_entry], ignore_index=True)
            data.to_csv(DATA_FILE, index=False)
            st.success("✔ Commentaire enregistré avec succès !")

# ----------------- MODIFIER SON COMMENTAIRE -----------------
st.subheader("✏ Modifier votre commentaire")

edit_name = st.text_input("Votre nom (pour modifier)", key="edit")

if edit_name in data["Nom"].values:
    idx = data[data["Nom"] == edit_name].index[0]
    old_comment = data.loc[idx, "Commentaire"]

    new_comment = st.text_area("Nouveau commentaire :", value=old_comment)

    if st.button("Mettre à jour"):
        if new_comment.strip() == "":
            st.error("❌ Le commentaire ne peut pas être vide.")
        else:
            data.loc[idx, "Commentaire"] = new_comment
            data.to_csv(DATA_FILE, index=False)
            st.success("✔ Commentaire mis à jour.")

# ----------------- STATISTIQUES DU SONDAGE -----------------
st.subheader("📊 Statistiques du sondage")

if len(data) > 0:
    counts = data["Etat_structure"].value_counts()

    plt.figure(figsize=(5, 5))
    colors = ["#4CAF50", "#FFC107", "#F44336"]  # Vert / Jaune / Rouge
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=colors)
    plt.title("État des bâtiments")
    st.pyplot(plt)

    st.subheader("📝 Avis des participants")
    st.dataframe(data[["Nom", "Commentaire"]])
else:
    st.info("Aucune donnée enregistrée pour l’instant.")
