import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashbord Etude Cafe Bean", layout="wide")

def load_data():
    fichier = 'BeansDataSet.csv'
    data = pd.read_csv(fichier)
    return data

data = load_data()

# Menu latéral
st.sidebar.title("Dashbord Etude Cafe Bean")
menu = st.sidebar.selectbox("Navigation", ["Accueil", "Exploration", "Analyse", "Analyse des Performances", "Rapport et Recommandations"])

def titreAffichage():
    return st.markdown("""
    <div style='text-align: center;'>
    <h1>Dashbord Etude Cafe Bean</h1>
    <h4 style='color:green;'>Analyse des ventes</h4>
    </div>
    """, unsafe_allow_html=True) 

# Définition des fonctions pour chaque section
def accueil():
    titreAffichage()
    st.subheader("Aperçu des Données")
    st.dataframe(data.head())

def exploration():
    titreAffichage()
    st.header("Exploration des Données")
    st.subheader("Aperçu des premières lignes")
    st.dataframe(data.head(10))
    st.subheader("Aperçu des dernières lignes")
    st.dataframe(data.tail(10))

    st.subheader("Statistiques descriptives")
    st.write(data.describe())

    st.subheader("Répartition des canaux de vente")
    fig1, ax1 = plt.subplots()
    data['Channel'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax1)
    ax1.set_ylabel('')
    st.pyplot(fig1)

    st.subheader("Répartition par région")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=data, x='Region', ax=ax2)
    st.pyplot(fig2)

def analyse():
    titreAffichage()
    st.header("Analyse")
    st.subheader("Ventes moyennes par région")
    region_moy = data.groupby('Region')[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].mean()
    st.dataframe(region_moy)

    st.subheader("Ventes moyennes par canal")
    canal_moy = data.groupby('Channel')[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].mean()
    st.dataframe(canal_moy)

def analyse_performances():
    titreAffichage()
    st.markdown("<h2 style='text-align:center; color:white;'>Analyse des Performances de Vente</h2>", unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)

    regions = ['Toutes'] + sorted(data['Region'].unique())
    channels = ['Tous'] + sorted(data['Channel'].unique())

    selected_region = col1.selectbox("Filtrer par Région", regions)
    selected_channel = col2.selectbox("Filtrer par Canal", channels)

    filtered_data = data.copy()

    if selected_region != 'Toutes':
        filtered_data = filtered_data[filtered_data['Region'] == selected_region]

    if selected_channel != 'Tous':
        filtered_data = filtered_data[filtered_data['Channel'] == selected_channel]

    st.subheader("Répartition des Ventes")
    col3, col4 = st.columns(2)

    with col3:
        ventes = filtered_data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum()
        fig_prod, ax_prod = plt.subplots()
        ventes.sort_values().plot.barh(ax=ax_prod, color=sns.color_palette("viridis", len(ventes)))
        ax_prod.set_xlabel("Total des Ventes")
        ax_prod.set_ylabel("Produits")
        ax_prod.set_title("Ventes Totales par Produit")
        st.pyplot(fig_prod)

    with col4:
        region_sales = filtered_data.groupby('Region')[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum().sum(axis=1)
        fig_reg, ax_reg = plt.subplots()
        region_sales.sort_values().plot.barh(ax=ax_reg, color=sns.color_palette("muted", len(region_sales)))
        ax_reg.set_xlabel("Total des Ventes")
        ax_reg.set_ylabel("Region")
        ax_reg.set_title("Ventes par Région")
        st.pyplot(fig_reg)

def rapport():
    titreAffichage()
    st.header("Rapport & Recommandations")

    st.subheader("Tendances Observées")
    st.markdown("""
    - Une forte progression des ventes a été constatée sur le canal **Online**.
    - Les ventes de **Robusta** et **Arabica** sont dominantes.
    - La région **South** enregistre des volumes de vente élevés.
    """)

    st.subheader("Recommandations")
    st.markdown("""
    - Accroître les investissements dans les campagnes **numériques** pour capter davantage de clients en ligne.<br>
    - Identifier les régions où la consommation est plus faible et y renforcer les actions marketing.<br>
    - Optimiser la distribution des produits à forte demande comme **Robusta** et **Arabica**.<br>
    - Étudier l'impact des variations saisonnières sur les ventes.
    """, unsafe_allow_html=True)

    st.subheader("Données à Collecter à l'Avenir")
    st.markdown("""
    - Retour d'expérience et niveau de satisfaction des clients.
    - Historique des achats individuels pour affiner la segmentation.
    - Analyse des tendances de prix pour optimiser la rentabilité.
    """)

# Dictionnaire pour émuler un switch-case
menu_fonction = {
    "Accueil": accueil,
    "Exploration": exploration,
    "Analyse": analyse,
    "Analyse des Performances": analyse_performances,
    "Rapport et Recommandations": rapport
}

# Exécution de la fonction correspondante
menu_fonction.get(menu, accueil)()
