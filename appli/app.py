import streamlit as st
import os
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# 📂 Dossier contenant les cartes exportées
IMAGE_FOLDER = "./images"  # Assurez-vous que ce dossier est bien dans le repo GitHub

# 📌 Années disponibles
ANNEES_DISPONIBLES = ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]

# 🎨 STYLE DU SIDEBAR
st.sidebar.markdown("<h1 style='text-align: center;'>🛰️ Dashboard NDVI & NDWI</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# 📌 Sélection de la partie
partie = st.sidebar.radio(
    "📌 **Choisissez une analyse :**",
    ["📍 Visualisation", "🔄 Comparaison", "📊 Évolution des indices"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("📅 **Années disponibles :** 2014 - 2023")

st.title("🛰️ Fleuve Nakambé : Eau et végétation")

# 🔄 Fonction pour charger une image
def charger_image(annee):
    chemin = os.path.join(IMAGE_FOLDER, f"Carte_{annee}.jpg")
    if os.path.exists(chemin):  # Vérification d'existence
        return Image.open(chemin)
    else:
        st.warning(f"⚠️ L'image pour {annee} est introuvable ! Vérifiez le dossier `{IMAGE_FOLDER}`.")
        return None

# 🔹 PARTIE 1 : Visualisation simple
if partie == "📍 Visualisation":
    st.subheader("📍 Visualisation d’une carte par année")
    annee = st.select_slider("Sélectionner une année :", ANNEES_DISPONIBLES)

    img = charger_image(annee)
    if img:
        st.image(img, caption=f"🗺️ Carte - {annee}", use_column_width=True)

        # Sauvegarde correcte pour le téléchargement
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_bytes = img_buffer.getvalue()

        st.download_button(
            label=f"📥 Télécharger la carte {annee}",
            data=img_bytes,
            file_name=f"Carte_{annee}.png",
            mime="image/png"
        )

# 🔹 PARTIE 2 : Superposition de cartes
elif partie == "🔄 Comparaison":
    st.subheader("🔄 Comparaison de deux cartes")
    
    col1, col2 = st.columns(2)
    with col1:
        annee1 = st.selectbox("Sélectionner la première année :", ANNEES_DISPONIBLES, index=0)
    with col2:
        annee2 = st.selectbox("Sélectionner la deuxième année :", ANNEES_DISPONIBLES, index=1)
    
    opacity = st.slider("Ajuster l'opacité de la deuxième carte", 0.1, 1.0, 0.5)

    img1 = charger_image(annee1)
    img2 = charger_image(annee2)

    if img1 and img2:
        # Superposition avec opacité
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")

        blended = Image.blend(img1, img2, alpha=opacity)
        st.image(blended, caption=f"Comparaison {annee1} vs {annee2}", use_container_width =True)

# 🔹 PARTIE 3 : Courbes d'évolution des indices NDVI & NDWI avec valeur seuil
elif partie == "📊 Évolution des indices":
    st.subheader("📊 Évolution des indices NDVI & NDWI")

    # 🔹 Remplace ces valeurs par tes données réelles
    ndvi_min = {"2014": -0.2137,"2015": -0.1590,"2016": -0.2245,"2017": -0.2581,"2018": -0.1916,"2019": -0.2323,"2020": -0.1993, "2021": -0.2256, "2022": -0.1945, "2023": -0.2404}

    ndvi_max = {"2014": 0.3958,"2015": 0.1760,"2016": 0.2580,"2017": 0.3514,"2018": 0.4251,"2019": 0.2949,"2020": 0.3407, "2021": 0.2974, "2022": 0.3309, "2023": 0.4513}

    ndvi_seuil = {"2014": 0.17,"2015": 0.12,"2016": 0.13,"2017": 0.15,"2018": 0.15,"2019": 0.15,"2020": -0.15, "2021": 0.15, "2022": 0.13, "2023": 0.15} 

    ndwi_min = {"2014": -0.3616,"2015": -0.2307,"2016": -0.2823,"2017": -0.3632,"2018": -0.3814,"2019": -0.3633,"2020": -0.3347, "2021": -0.3108, "2022": -0.3183, "2023": -0.4208}

    ndwi_max = {"2014": 0.2727,"2015": 0.1362,"2016": 0.1864,"2017": 0.2307,"2018": 0.1717,"2019": 0.3157,"2020": 0.2737, "2021": 0.1924, "2022": 0.1465, "2023": 0.2298}

    ndwi_seuil = {"2014": 0,"2015": -0.08,"2016": 0.04,"2017": 0.05,"2018": 0.04,"2019": 0.0,"2020": 0.0, "2021": 0, "2022": 0, "2023": 0} 

    # 📈 Graphiques des plages NDVI & NDWI avec ligne rouge pour la valeur seuil
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # NDVI
    ax[0].fill_between(ANNEES_DISPONIBLES, list(ndvi_min.values()), list(ndvi_max.values()), color="#008000", alpha=0.4)
    ax[0].plot(ANNEES_DISPONIBLES, list(ndvi_min.values()), "g--", label="NDVI min")
    ax[0].plot(ANNEES_DISPONIBLES, list(ndvi_max.values()), "g-", label="NDVI max")
    ax[0].plot(ANNEES_DISPONIBLES, list(ndvi_seuil.values()), "r-", linewidth=2, label="NDVI seuil")  # 🚨 Ligne rouge
    ax[0].set_title("Évolution du NDVI")
    ax[0].legend()

    # NDWI
    ax[1].fill_between(ANNEES_DISPONIBLES, list(ndwi_min.values()), list(ndwi_max.values()), color="#00BFFF", alpha=0.4)
    ax[1].plot(ANNEES_DISPONIBLES, list(ndwi_min.values()), "b--", label="NDWI min")
    ax[1].plot(ANNEES_DISPONIBLES, list(ndwi_max.values()), "b-", label="NDWI max")
    ax[1].plot(ANNEES_DISPONIBLES, list(ndwi_seuil.values()), "r-", linewidth=2, label="NDWI seuil")  # 🚨 Ligne rouge
    ax[1].set_title("Évolution du NDWI")
    ax[1].legend()

    st.pyplot(fig)
