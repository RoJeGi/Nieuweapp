
import streamlit as st
import pandas as pd

st.title("Besteladvies App – Per Artikel en Week")

@st.cache_data
def load_data():
    df = pd.read_excel("Verkoopanalyse_met_besteladvies_correct.xlsx")
    return df

df = load_data()

artikel = st.selectbox("Kies artikelnummer:", sorted(df['Referentie'].dropna().unique()))
huidige_week = st.number_input("Voer huidige week in:", min_value=1, max_value=52, value=15, step=1)

# Filter alleen op artikel
filtered = df[df['Referentie'] == artikel].copy()

# Dynamisch besteladvies per rij
filtered['Bestellen'] = (
    (filtered['Bestelweek'] == huidige_week) &
    (filtered['Aantal geleverd'] > filtered['Aanwezige voorraad'])
).map({True: 'ja', False: 'nee'})

# Toon alle regels voor dat artikel en highlight actuele besteladvies
st.subheader(f"Bestelinformatie voor artikel {artikel} (huidige week = {huidige_week})")
st.dataframe(filtered[['Week', 'Aantal geleverd', 'Aanwezige voorraad', 'Levertijd in weken',
                       'Bestelweek', 'Bestellen']])

# Toon eventueel samenvatting
advies_rijen = filtered[filtered['Bestelweek'] == huidige_week]
if not advies_rijen.empty:
    advies = advies_rijen['Bestellen'].iloc[0]
    st.markdown(f"### Advies voor week {huidige_week}: **{advies.upper()}**")
else:
    st.info("Geen verkoopregels waarvoor deze week de bestelweek is.")
